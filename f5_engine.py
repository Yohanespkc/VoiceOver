"""
F5-TTS Indo Finetune V2 Engine Module
Integrasi model Eempostor/F5-TTS-INDO-FINETUNE-V2 untuk VoiceOver Studio.
Mendukung zero-shot voice cloning, Apple Silicon MPS/CPU acceleration,
chunking naskah panjang, dan ekspor audio ganda (WAV 16-bit PCM & MP3 320kbps).
"""

import os
import sys
import time
import uuid
import json
import random
import shutil
import urllib.request
import subprocess
from typing import Optional, Dict, Any, List

# Pastikan environment variable untuk PyTorch MPS fallback aktif
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import soundfile as sf
import torch
import torchaudio

# Patch torchaudio.load untuk menggunakan soundfile langsung (menghindari ketergantungan dylib torchcodec)
def _patched_torchaudio_load(filepath, **kwargs):
    data, samplerate = sf.read(filepath)
    tensor = torch.from_numpy(data).float()
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    elif tensor.ndim == 2:
        tensor = tensor.t()
    return tensor, samplerate

torchaudio.load = _patched_torchaudio_load

# Patch ThreadPoolExecutor in f5_tts.infer.utils_infer to max_workers=1 on MPS (mencegah tabrakan command buffer Apple Metal)
try:
    import f5_tts.infer.utils_infer as utils_infer
    import concurrent.futures

    _orig_tpe = utils_infer.ThreadPoolExecutor
    class _MPS_Safe_ThreadPoolExecutor(_orig_tpe):
        def __init__(self, max_workers=None, **kwargs):
            if torch.backends.mps.is_available():
                max_workers = 1
            super().__init__(max_workers=max_workers, **kwargs)
    utils_infer.ThreadPoolExecutor = _MPS_Safe_ThreadPoolExecutor
except Exception as e:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models", "f5_tts_indo")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CLONED_VOICES_DIR = os.path.join(BASE_DIR, "assets", "cloned_voices")
TRAINER_CATALOG_FILE = os.path.join(CLONED_VOICES_DIR, "trainers.json")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CLONED_VOICES_DIR, exist_ok=True)

CKPT_FILE = os.path.join(MODELS_DIR, "f5_tts_indo_v2.pt")
VOCAB_FILE = os.path.join(MODELS_DIR, "vocab.txt")

HF_REPO_URL = "https://huggingface.co/Eempostor/F5-TTS-INDO-FINETUNE-V2"
CKPT_DOWNLOAD_URL = f"{HF_REPO_URL}/resolve/main/f5_tts_indo_v2.pt"
VOCAB_DOWNLOAD_URL = f"{HF_REPO_URL}/raw/main/vocab.txt"

# Referensi sampel bawaan dari repo Eempostor
REF_REPORTER_URL = f"{HF_REPO_URL}/resolve/main/ref_reporter.mp3"
REF_PRABOWO_URL = f"{HF_REPO_URL}/resolve/main/ref_prabowo.mp3"
REF_WINDAH_URL = f"{HF_REPO_URL}/resolve/main/ref_windah.mp3"

from gasing_pronunciation import preprocess_pronunciation, split_into_smart_chunks

class F5IndoEngine:
    _instance = None

    def __init__(self):
        self.model = None
        self.device = self._detect_device()
        self.is_loading = False
        self.download_progress = {"status": "idle", "percent": 0, "message": ""}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = F5IndoEngine()
        return cls._instance

    def _detect_device(self) -> str:
        try:
            import torch
            if torch.backends.mps.is_available():
                return "mps"
            elif torch.cuda.is_available():
                return "cuda"
        except Exception:
            pass
        return "cpu"

    def is_model_installed(self) -> bool:
        return os.path.exists(CKPT_FILE) and os.path.getsize(CKPT_FILE) > 100_000_000 and os.path.exists(VOCAB_FILE)

    def get_status(self) -> Dict[str, Any]:
        installed = self.is_model_installed()
        ckpt_size_mb = round(os.path.getsize(CKPT_FILE) / (1024 * 1024), 1) if os.path.exists(CKPT_FILE) else 0
        return {
            "installed": installed,
            "loaded": self.model is not None,
            "device": self.device,
            "checkpoint_size_mb": ckpt_size_mb,
            "model_path": CKPT_FILE,
            "vocab_path": VOCAB_FILE,
            "download_status": self.download_progress,
        }

    def download_model_weights(self) -> bool:
        """Mengunduh bobot f5_tts_indo_v2.pt dan vocab.txt dari Hugging Face."""
        if self.is_model_installed():
            self.download_progress = {"status": "complete", "percent": 100, "message": "Model sudah terpasang."}
            return True

        self.download_progress = {"status": "downloading", "percent": 1, "message": "Mengunduh vocab.txt..."}
        try:
            # 1. Unduh vocab.txt
            if not os.path.exists(VOCAB_FILE):
                urllib.request.urlretrieve(VOCAB_DOWNLOAD_URL, VOCAB_FILE)

            # 2. Unduh referensi contoh audio jika belum ada
            ref_rep = os.path.join(MODELS_DIR, "ref_reporter.mp3")
            if not os.path.exists(ref_rep):
                try:
                    urllib.request.urlretrieve(REF_REPORTER_URL, ref_rep)
                except Exception:
                    pass

            ref_pra = os.path.join(MODELS_DIR, "ref_prabowo.mp3")
            if not os.path.exists(ref_pra):
                try:
                    urllib.request.urlretrieve(REF_PRABOWO_URL, ref_pra)
                except Exception:
                    pass

            ref_win = os.path.join(MODELS_DIR, "ref_windah.mp3")
            if not os.path.exists(ref_win):
                try:
                    urllib.request.urlretrieve(REF_WINDAH_URL, ref_win)
                except Exception:
                    pass

            # 3. Unduh f5_tts_indo_v2.pt dengan progress
            self.download_progress = {"status": "downloading", "percent": 5, "message": "Mengunduh f5_tts_indo_v2.pt (~1.34 GB)..."}
            temp_ckpt = CKPT_FILE + ".tmp"

            def _reporthook(block_num, block_size, total_size):
                if total_size > 0:
                    downloaded = block_num * block_size
                    pct = int(5 + (downloaded / total_size) * 94)
                    mb_down = round(downloaded / (1024 * 1024), 1)
                    mb_tot = round(total_size / (1024 * 1024), 1)
                    self.download_progress = {
                        "status": "downloading",
                        "percent": min(pct, 99),
                        "message": f"Mengunduh model: {mb_down} MB / {mb_tot} MB ({min(pct, 99)}%)"
                    }

            # Gunakan curl untuk download yang lebih tangguh dan cepat jika tersedia
            curl_cmd = [
                "curl", "-L", "-o", temp_ckpt,
                "--progress-bar",
                CKPT_DOWNLOAD_URL
            ]
            res = subprocess.run(curl_cmd, capture_output=True)
            if res.returncode != 0 or not os.path.exists(temp_ckpt):
                # Fallback to python urllib
                urllib.request.urlretrieve(CKPT_DOWNLOAD_URL, temp_ckpt, reporthook=_reporthook)

            if os.path.exists(temp_ckpt) and os.path.getsize(temp_ckpt) > 100_000_000:
                os.replace(temp_ckpt, CKPT_FILE)
                self.download_progress = {"status": "complete", "percent": 100, "message": "Model berhasil diunduh dan siap digunakan!"}
                return True
            else:
                raise Exception("Ukuran file bobot model tidak valid.")
        except Exception as e:
            self.download_progress = {"status": "error", "percent": 0, "message": f"Gagal mengunduh: {str(e)}"}
            return False

    def load_model(self):
        """Memuat arsitektur model F5-TTS ke dalam memori RAM/MPS."""
        if self.model is not None:
            return self.model

        if not self.is_model_installed():
            raise FileNotFoundError("Bobot model f5_tts_indo_v2.pt belum diunduh.")

        self.is_loading = True
        try:
            from f5_tts.api import F5TTS

            print(f"Memuat F5-TTS Indo V2 pada perangkat: {self.device}...")
            self.model = F5TTS(
                model="F5TTS_v1_Base",
                ckpt_file=CKPT_FILE,
                vocab_file=VOCAB_FILE,
                device=self.device
            )
            print("F5-TTS Indo V2 berhasil dimuat ke memori!")
            return self.model
        finally:
            self.is_loading = False

    def ensure_standard_audio_ref(self, input_path: str, output_path: str) -> str:
        """Memastikan audio referensi berformat 24kHz mono WAV untuk kualitas cloning optimal."""
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path

    def auto_clone_john(self) -> Dict[str, Any]:
        """Secara otomatis mengekstrak sampel suara Tutor John (pria) dari video modul pembagian Tanya Marcia lokal."""
        so_video_path = "/Users/yohanessurya/Documents/Development/so/apps/suite/dist/assets/videos/z5l1/z5l1_tanya_marcia.mp4"
        if not os.path.exists(so_video_path):
            so_video_path = "/Users/yohanessurya/Documents/Development/so/apps/suite/dist/TanyaMarcia/zone5Level1 - Tanya Marcia.mov"

        john_wav = os.path.join(CLONED_VOICES_DIR, "at_john_ref.wav")
        if os.path.exists(so_video_path):
            # Potong segmen dialog pembuka utuh (durasi 7.33 detik: 0.12s hingga 7.45s) dengan bandpass filter dan fade in/out
            cmd = [
                "ffmpeg", "-y", "-ss", "00:00:00.12", "-to", "00:00:07.45",
                "-i", so_video_path,
                "-af", "highpass=f=80,lowpass=f=11000,afade=t=in:ss=0:d=0.02,afade=t=out:st=7.25:d=0.08",
                "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
                john_wav
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise Exception(f"Gagal mengekstrak audio John: {res.stderr}")

        john_ref_text = "Ketika kita hendak menghitung enam bagi dua, sama saja dengan bertanya dua kali berapa sama dengan enam."

        profile = {
            "id": "at_john",
            "name": "AT John (Tutor Tanya Marcia)",
            "role": "Trainer GASING / Tutor Pembagian (Pria)",
            "category": "trainer_gasing",
            "gender": "Pria",
            "ref_audio": "/assets/cloned_voices/at_john_ref.wav",
            "ref_audio_abs": john_wav,
            "ref_text": john_ref_text,
            "avatar": "👨‍🏫",
            "description": "Suara tenang, jelas, dan artikulatif Tutor John dari rekaman video pembagian Tanya Marcia."
        }
        self.save_voice_profile(profile)
        return profile

    def auto_clone_marcia(self) -> Dict[str, Any]:
        """Secara otomatis mengekstrak sampel suara autentik Trainer Marcia (wanita) dari rekaman video master 6 menit."""
        master_src = os.path.join(CLONED_VOICES_DIR, "at_c04618f8.wav")
        if not os.path.exists(master_src):
            master_src = os.path.join(BASE_DIR, "AT Marcia contoh", "00_AT_Marcia_Trainer_Suara_Asli_Master_6Min.mp3")

        marcia_wav = os.path.join(CLONED_VOICES_DIR, "at_marcia_ref.wav")
        marcia_legacy_wav = os.path.join(CLONED_VOICES_DIR, "marcia_ref.wav")

        if os.path.exists(master_src):
            # Potong segmen ucapan jernih autentik Trainer Marcia (7.7 detik: 7.15s s/d 14.85s) dengan highpass dan loudnorm
            cmd = [
                "ffmpeg", "-y", "-ss", "00:00:07.15", "-to", "00:00:14.85",
                "-i", master_src,
                "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=7,afade=t=in:ss=0:d=0.03,afade=t=out:st=7.6:d=0.08",
                "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
                marcia_wav
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                shutil.copyfile(marcia_wav, marcia_legacy_wav)

        # Transkripsi 100% akurat terverifikasi dari audio asli Trainer Marcia
        marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."

        # Simpan avatar jika ada
        avatar_src = "/Users/yohanessurya/Documents/Development/so/apps/suite/dist/assets/images/characters/avatar_marcia.png"
        avatar_dst = os.path.join(CLONED_VOICES_DIR, "marcia_avatar.png")
        if os.path.exists(avatar_src) and not os.path.exists(avatar_dst):
            try:
                shutil.copyfile(avatar_src, avatar_dst)
            except Exception:
                pass

        profile = {
            "id": "so_marcia",
            "name": "Guru Marcia (Trainer Marcia Asli)",
            "role": "Pemandu & Tutor Game SO (Wanita)",
            "category": "so_character",
            "gender": "Wanita",
            "ref_audio": "/assets/cloned_voices/at_marcia_ref.wav",
            "ref_audio_abs": marcia_wav,
            "ref_text": marcia_ref_text,
            "avatar": "/assets/cloned_voices/marcia_avatar.png" if os.path.exists(avatar_dst) else "👩‍🏫",
            "description": "Suara asli Trainer Marcia yang hangat, bersahabat, penuh empati, memandu siswa dalam petualangan matematika SO."
        }
        self.save_voice_profile(profile)
        return profile

    def auto_clone_prof_gasing(self) -> Dict[str, Any]:
        """Mengekstrak rekaman autentik Prof. Yohanes Surya sebagai profil cloning."""
        src_ogg = os.path.join(BASE_DIR, "assets", "audio", "prof_gasing", "prof_gasing_yosu_0_asli.ogg")
        dst_wav = os.path.join(CLONED_VOICES_DIR, "prof_yosu_ref.wav")

        if os.path.exists(src_ogg):
            # Ambil kalimat pembuka utuh (5.1 detik)
            cmd = [
                "ffmpeg", "-y", "-ss", "00:00:00.0", "-to", "00:00:05.1",
                "-i", src_ogg,
                "-af", "highpass=f=80,lowpass=f=11000",
                "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
                dst_wav
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            ref_text = "Salam Ksatria Gaber, saya Profesor GASING Yosu dari masa depan."
        else:
            ref_text = "Salam Ksatria Gaber, saya Profesor GASING Yosu dari masa depan."

        profile = {
            "id": "prof_yosu_asli",
            "name": "Prof. Yohanes Surya (GASING Asli)",
            "role": "Pendiri & Mentor Utama GASING",
            "category": "so_character",
            "gender": "Pria",
            "ref_audio": "/assets/cloned_voices/prof_yosu_ref.wav",
            "ref_audio_abs": dst_wav,
            "ref_text": ref_text,
            "avatar": "👨‍🏫",
            "description": "Suara asli Prof. Yohanes Surya yang hangat, inspiratif, dan membangkitkan semangat berhitung."
        }
        self.save_voice_profile(profile)
        return profile

    def get_trainers(self) -> List[Dict[str, Any]]:
        if not os.path.exists(TRAINER_CATALOG_FILE):
            return []
        try:
            with open(TRAINER_CATALOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_voice_profile(self, profile: Dict[str, Any]):
        trainers = self.get_trainers()
        # Perbarui atau tambahkan
        updated = False
        for i, t in enumerate(trainers):
            if t.get("id") == profile.get("id"):
                trainers[i] = profile
                updated = True
                break
        if not updated:
            trainers.append(profile)

        with open(TRAINER_CATALOG_FILE, "w", encoding="utf-8") as f:
            json.dump(trainers, f, ensure_ascii=False, indent=2)

    def delete_voice_profile(self, voice_id: str) -> bool:
        """Menghapus profil kloning suara dari katalog trainers.json dan menghapus file audionya."""
        trainers = self.get_trainers()
        new_trainers = []
        found = False
        audio_to_remove = None

        for t in trainers:
            if t.get("id") == voice_id:
                found = True
                audio_to_remove = t.get("ref_audio_abs") or os.path.join(CLONED_VOICES_DIR, f"{voice_id}.wav")
            else:
                new_trainers.append(t)

        if found:
            with open(TRAINER_CATALOG_FILE, "w", encoding="utf-8") as f:
                json.dump(new_trainers, f, ensure_ascii=False, indent=2)

            if audio_to_remove and os.path.exists(audio_to_remove):
                try:
                    os.remove(audio_to_remove)
                    logger.info(f"Deleted audio file for voice {voice_id}: {audio_to_remove}")
                except Exception as e:
                    logger.warning(f"Failed to delete audio file {audio_to_remove}: {e}")

            return True
        return False

    def get_all_voices(self) -> List[Dict[str, Any]]:
        """Mengembalikan seluruh koleksi model suara terbaik (Karakter SO, AT Trainer, Standar Eempostor)."""
        voices = []

        # 1. Pastikan profil Marcia, John & Prof. Gasing terdaftar
        trainers_list = self.get_trainers()
        if not any(v.get("id") == "so_marcia" for v in trainers_list):
            try:
                self.auto_clone_marcia()
            except Exception:
                pass

        if not any(v.get("id") == "at_john" for v in trainers_list):
            try:
                self.auto_clone_john()
            except Exception:
                pass

        if not any(v.get("id") == "prof_yosu_asli" for v in trainers_list):
            try:
                self.auto_clone_prof_gasing()
            except Exception:
                pass

        # 2. Preset Bawaan Eempostor Model V2
        reporter_ref = os.path.join(MODELS_DIR, "ref_reporter.mp3")
        prabowo_ref = os.path.join(MODELS_DIR, "ref_prabowo.mp3")
        windah_ref = os.path.join(MODELS_DIR, "ref_windah.mp3")

        preset_eempostor = [
            {
                "id": "eem_reporter",
                "name": "Presenter TV Formal (Wanita)",
                "role": "Narator Sinematik & Pengumuman",
                "category": "standard_indo",
                "gender": "Wanita",
                "ref_audio": "/models/f5_tts_indo/ref_reporter.mp3",
                "ref_audio_abs": reporter_ref,
                "ref_text": "dikatakan ternyata cek 3 miliar yang diberikan untuk mahar pernikahan ini adalah palsu.",
                "avatar": "🎙️",
                "description": "Artikulasi bersih, jernih, intonasi berita formal dan teratur."
            },
            {
                "id": "eem_prabowo",
                "name": "Bapak Bangsa / Pidato Berwibawa (Pria)",
                "role": "Narator Misi Akbar & Pengantar Game",
                "category": "standard_indo",
                "gender": "Pria",
                "ref_audio": "/models/f5_tts_indo/ref_prabowo.mp3",
                "ref_audio_abs": prabowo_ref,
                "ref_text": "Selamat pagi, salam sejahtera bagi kita sekalian.",
                "avatar": "🏛️",
                "description": "Suara bariton tegas, berwibawa, penuh tekad kepemimpinan."
            },
            {
                "id": "eem_windah",
                "name": "Gamer & Kreator Ceria (Pria)",
                "role": "Pemandu Game Interaktif & Kasual",
                "category": "standard_indo",
                "gender": "Pria",
                "ref_audio": "/models/f5_tts_indo/ref_windah.mp3",
                "ref_audio_abs": windah_ref,
                "ref_text": "Eh, guys, gua udah sampai nih di hotel di hari kedua lagi ngerjain beberapa hal, lagi upload-upload video YouTube.",
                "avatar": "🎮",
                "description": "Santai, gaul, fasih dalam code-switching bilingual Indonesia-Inggris."
            },
            {
                "id": "blaze_original",
                "name": "Blaze (Penguasa Antagonis SO)",
                "role": "Boss Fight & Tantangan Game",
                "category": "so_character",
                "gender": "Pria",
                "ref_audio": "/assets/audio/blaze/blaze_0.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "blaze", "blaze_0.mp3"),
                "ref_text": "Kalian pikir bisa mengalahkan kekuatan api milikku?",
                "avatar": "😈",
                "description": "Bariton berat, dominan, sinis, dan menantang."
            },
            {
                "id": "ksatria_gaber",
                "name": "Ksatria Gaber / Xander",
                "role": "Pahlawan Muda Pelindung Babilon",
                "category": "so_character",
                "gender": "Pria",
                "ref_audio": "/assets/audio/karakter_lain/ksatria_gaber_motivasi.wav",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "karakter_lain", "ksatria_gaber_motivasi.wav"),
                "ref_text": "Ayo teman-teman, jangan pernah menyerah! Kita pasti bisa!",
                "avatar": "🛡️",
                "description": "Karakter muda heroik, penuh semangat dan ramah anak."
            },
            {
                "id": "master_tutor_gasing",
                "name": "Master Tutor AT GASING (Lirik Kanan)",
                "role": "Narator Modul & Trik Hitung Cepat",
                "category": "trainer_gasing",
                "gender": "Pria",
                "ref_audio": "/assets/audio/karakter_lain/master_tutor_lirik_kanan.wav",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "karakter_lain", "master_tutor_lirik_kanan.wav"),
                "ref_text": "Sekarang kita perhatikan trik lirik kanan pada metode penjumlahan gasing.",
                "avatar": "📐",
                "description": "Trainer berpengalaman mengajar trik lirik kanan langkah demi langkah."
            },
            {
                "id": "vo_anak",
                "name": "Suara Anak Ceria (Kids Voice)",
                "role": "Konten Edukasi, Animasi & Kartun",
                "category": "voiceover_indo",
                "gender": "Anak-anak",
                "ref_audio": "/assets/audio/contoh_voiceover/01_suara_anak_ceria.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "01_suara_anak_ceria.mp3"),
                "ref_text": "Halo teman-teman cerdas! Wah, lihat ini, robot antariksa kita sudah siap meluncur ke galaksi bintang matematika! Ayo kita berpetualang dan hitung mundur bareng-bareng ya: Tiga, dua, satu... Meluncur!",
                "avatar": "👶",
                "description": "Ceria, polos, penuh energi, dan ekspresif. Cocok untuk edukasi anak dan animasi."
            },
            {
                "id": "vo_korporat",
                "name": "Suara Korporat (Corporate Voice)",
                "role": "Company Profile & Presentasi Bisnis",
                "category": "voiceover_indo",
                "gender": "Pria Formal",
                "ref_audio": "/assets/audio/contoh_voiceover/02_suara_korporat_profesional.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "02_suara_korporat_profesional.mp3"),
                "ref_text": "Selamat datang di profil inovasi berkelanjutan kami. Dengan mengedepankan integrasi teknologi digital dan integritas profesional, kami berdedikasi menciptakan solusi bernilai tambah bagi kemajuan ekosistem bisnis modern di Indonesia.",
                "avatar": "🏢",
                "description": "Tegas, jelas, profesional, dan berwibawa untuk presentasi bisnis dan e-learning."
            },
            {
                "id": "vo_youtube",
                "name": "Suara YouTube & Daily Vlog",
                "role": "Konten Kreator, Review & Tutorial",
                "category": "voiceover_indo",
                "gender": "Pria Santai",
                "ref_audio": "/assets/audio/contoh_voiceover/03_suara_youtube_vlog.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "03_suara_youtube_vlog.mp3"),
                "ref_text": "Halo guys, balik lagi di channel kita! Hari ini gua bener-bener excited banget, soalnya perangkat yang kemarin kita tunggu-tunggu akhirnya mendarat di studio. Penasaran performanya gimana? Yuk, langsung kita bahas tuntas dan jangan lupa subscribe ya!",
                "avatar": "📹",
                "description": "Santai, natural, terasa dekat seperti mengobrol akrab dengan teman."
            },
            {
                "id": "vo_audiobook",
                "name": "Suara Audiobook & Storytelling",
                "role": "Narator Buku Audio, Cerita & Podcast",
                "category": "voiceover_indo",
                "gender": "Wanita",
                "ref_audio": "/assets/audio/contoh_voiceover/04_suara_audiobook_kisah.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "04_suara_audiobook_kisah.mp3"),
                "ref_text": "Di bawah hamparan langit senja yang temaram, langkah kakinya terhenti di depan gerbang kayu tua itu. Angin pegunungan berhembus perlahan, seolah membisikkan kembali kisah masa silam yang telah lama terlelap di antara gemerisik dedaunan.",
                "avatar": "📚",
                "description": "Artikulasi jelas, ritme stabil dan mendalam, membangun emosi dan suasana imersif."
            },
            {
                "id": "vo_iklan",
                "name": "Suara Iklan Komersial (High Impact)",
                "role": "Pengisi Iklan TV, Radio & Digital Ads",
                "category": "voiceover_indo",
                "gender": "Wanita Dinamis",
                "ref_audio": "/assets/audio/contoh_voiceover/05_suara_iklan_komersial.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "05_suara_iklan_komersial.mp3"),
                "ref_text": "Mau belanja hemat tanpa repot? Sekarang saatnya beralih ke cara baru yang serba cepat dan praktis! Dapatkan diskon spesial hingga tujuh puluh persen hanya hari ini. Yuk, buka aplikasinya dan klaim promomu sekarang juga!",
                "avatar": "🎧",
                "description": "Persuasif, menarik perhatian seketika, dan punya impact kuat dalam waktu singkat."
            },
            {
                "id": "vo_motivator",
                "name": "Suara Motivator Pria Energik",
                "role": "Pemantik Semangat, Pujian & Gelora Juara",
                "category": "voiceover_indo",
                "gender": "Pria Energik",
                "ref_audio": "/assets/audio/contoh_voiceover/06_suara_motivator_pria.mp3",
                "ref_audio_abs": os.path.join(BASE_DIR, "assets", "audio", "contoh_voiceover", "06_suara_motivator_pria.mp3"),
                "ref_text": "Luar biasa! Jangan pernah ragukan kehebatan yang ada di dalam dirimu! Setiap tetes keringat dan perjuanganmu hari ini sedang membentuk masa depan yang gemilang. Bangkit, melangkah maju dengan gagah berani, dan buktikan bahwa kamu adalah sang juara!",
                "avatar": "⚡",
                "description": "Laki-laki semangat, energik, membakar motivasi perjuangan dan memberikan pujian tulus."
            }
        ]

        voices.extend(preset_eempostor)
        # 3. Tambahkan profil tersimpan dari catalog trainers
        trainers = self.get_trainers()
        for t in trainers:
            if not any(v.get("id") == t.get("id") for v in voices):
                voices.append(t)

        return voices

    def generate(
        self,
        ref_audio_path: str,
        ref_text: str,
        gen_text: str,
        speed: float = 1.0,
        nfe_step: int = 32,
        output_format: str = "wav",
        apply_bilingual: bool = True,
        apply_gasing: bool = True
    ) -> Dict[str, Any]:
        """
        Melakukan sintesis suara cloning F5-TTS untuk naskah input.
        Menghasilkan output dalam format WAV 16-bit PCM atau MP3 320kbps.
        """
        tts_model = self.load_model()

        if not os.path.exists(ref_audio_path):
            raise FileNotFoundError(f"File referensi audio tidak ditemukan: {ref_audio_path}")

        # Siapkan audio referensi standar
        temp_ref_wav = os.path.join(OUTPUT_DIR, f"temp_ref_{uuid.uuid4().hex[:8]}.wav")
        self.ensure_standard_audio_ref(ref_audio_path, temp_ref_wav)

        # Normalisasi pelafalan teks
        processed_text = preprocess_pronunciation(
            gen_text,
            apply_bilingual=apply_bilingual,
            apply_gasing_prosody=apply_gasing
        )

        chunks = split_into_smart_chunks(processed_text, max_chars=180)
        req_id = uuid.uuid4().hex[:10]
        final_wav = os.path.join(OUTPUT_DIR, f"F5_INDO_{req_id}.wav")

        chunk_wavs = []
        try:
            for idx, chunk in enumerate(chunks):
                chunk_file = os.path.join(OUTPUT_DIR, f"chunk_{req_id}_{idx}.wav")
                tts_model.infer(
                    ref_file=temp_ref_wav,
                    ref_text=ref_text,
                    gen_text=chunk,
                    speed=speed,
                    nfe_step=nfe_step,
                    file_wave=chunk_file,
                    remove_silence=True,
                    seed=random.randint(1000, 2000000000)
                )
                chunk_wavs.append(chunk_file)

            # Gabungkan jika ada lebih dari 1 chunk
            if len(chunk_wavs) == 1:
                shutil.move(chunk_wavs[0], final_wav)
            else:
                concat_list_file = os.path.join(OUTPUT_DIR, f"concat_{req_id}.txt")
                with open(concat_list_file, "w", encoding="utf-8") as f:
                    for cw in chunk_wavs:
                        f.write(f"file '{cw}'\n")

                concat_cmd = [
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", concat_list_file,
                    "-c", "copy",
                    final_wav
                ]
                subprocess.run(concat_cmd, capture_output=True, check=True)
                if os.path.exists(concat_list_file):
                    os.remove(concat_list_file)
                for cw in chunk_wavs:
                    if os.path.exists(cw):
                        os.remove(cw)

            # Jika pengguna meminta MP3
            output_filename = os.path.basename(final_wav)
            if output_format.lower() == "mp3":
                final_mp3 = os.path.join(OUTPUT_DIR, f"F5_INDO_{req_id}.mp3")
                mp3_cmd = [
                    "ffmpeg", "-y", "-i", final_wav,
                    "-codec:a", "libmp3lame", "-b:a", "320k",
                    final_mp3
                ]
                subprocess.run(mp3_cmd, capture_output=True, check=True)
                output_filename = os.path.basename(final_mp3)

            # Cek durasi audio
            target_file = os.path.join(OUTPUT_DIR, output_filename)
            dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", target_file]
            dur_res = subprocess.run(dur_cmd, capture_output=True, text=True)
            dur = float(dur_res.stdout.strip()) if dur_res.stdout.strip() else 0.0

            return {
                "status": "success",
                "audio_url": f"/output/{output_filename}",
                "filename": output_filename,
                "duration": round(dur, 2),
                "format": output_format.lower(),
                "original_text": gen_text,
                "processed_text": processed_text,
                "chunks_count": len(chunks),
                "speed": speed,
                "nfe_step": nfe_step
            }
        finally:
            if os.path.exists(temp_ref_wav):
                os.remove(temp_ref_wav)
