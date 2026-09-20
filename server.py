import os
import uuid
import json
import asyncio
import shutil
import subprocess
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from f5_engine import F5IndoEngine
from gasing_pronunciation import preprocess_pronunciation, split_into_smart_chunks

app = FastAPI(title="VoiceOver Studio API (with F5-TTS Indo & Edge-TTS)", version="3.0.0")

# Enable CORS for local development & browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CATALOG_PATH = os.path.join(ASSETS_DIR, "audio_catalog.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Character Preset Configurations for Edge TTS
CHARACTER_PRESETS = {
    "prof_gasing_mentor": {
        "name": "Prof. Gasing (Mentor Masa Depan)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+2Hz",
        "rate": "+8%",
        "description": "Suara berwibawa, bijak, hangat, penuh semangat inspiratif."
    },
    "prof_gasing_anime": {
        "name": "Prof. Gasing (Anime Semangat)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+10Hz",
        "rate": "+22%",
        "description": "Intonasi dinamis dan cepat membakar antusiasme petualangan."
    },
    "prof_gasing_narasi": {
        "name": "Prof. Gasing (Narasi Bijak)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "-4Hz",
        "rate": "-5%",
        "description": "Artikulasi tenang, mendalam, dan menuntun langkah belajar."
    },
    "master_tutor": {
        "name": "Master Tutor GASING (Lirik Kanan)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+3Hz",
        "rate": "+6%",
        "description": "Fokus pada kejelasan trik hitung cepat metode GASING."
    },
    "ksatria_octagon": {
        "name": "Ksatria Octagon (Xander)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+12Hz",
        "rate": "+18%",
        "description": "Karakter pahlawan muda pemberani dan ramah anak-anak."
    },
    "blaze": {
        "name": "Blaze (Penguasa Antagonis)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "-12Hz",
        "rate": "-8%",
        "description": "Bariton berat, dominan, sinis, dan menantang."
    },
    "guru_marcia": {
        "name": "Guru Marcia (Pemandu & Tutor Game SO)",
        "voice": "id-ID-GadisNeural",
        "pitch": "+2Hz",
        "rate": "+4%",
        "description": "Suara wanita hangat, ramah, penuh semangat edukatif, membimbing siswa di Sacred Octagon."
    },
    "sang_ratu": {
        "name": "Sang Ratu Babilon",
        "voice": "id-ID-GadisNeural",
        "pitch": "-3Hz",
        "rate": "-5%",
        "description": "Suara wanita anggun, tenang, berwibawa, dan sarat rahasia."
    },
    "narator": {
        "name": "Narator Sinematik Babilon",
        "voice": "id-ID-ArdiNeural",
        "pitch": "-6Hz",
        "rate": "-2%",
        "description": "Sinematik, membangun ketegangan dan imersi dunia game."
    },
    "vo_anak_ceria": {
        "name": "👶 Suara Anak (Kids Voice)",
        "voice": "id-ID-GadisNeural",
        "pitch": "+16Hz",
        "rate": "+12%",
        "description": "Ceria, polos, penuh energi, dan ekspresif. Cocok untuk edukasi, animasi, dan kartun."
    },
    "vo_korporat_formal": {
        "name": "🏢 Suara Korporat (Corporate Voice)",
        "voice": "id-ID-ArdiNeural",
        "pitch": "-2Hz",
        "rate": "+0%",
        "description": "Tegas, jelas, profesional, dan berwibawa. Cocok untuk company profile dan presentasi bisnis."
    },
    "vo_youtube_vlog": {
        "name": "📹 Suara YouTube / Vlog",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+3Hz",
        "rate": "+10%",
        "description": "Santai, natural, terasa dekat seperti mengobrol akrab dengan teman. Cocok untuk konten digital."
    },
    "vo_audiobook_kisah": {
        "name": "📚 Suara Audiobook",
        "voice": "id-ID-GadisNeural",
        "pitch": "-3Hz",
        "rate": "-6%",
        "description": "Artikulasi jelas, ritme stabil dan mendalam, membangun emosi dan suasana imersif."
    },
    "vo_iklan_komersial": {
        "name": "🎧 Suara Iklan (Commercial Voice)",
        "voice": "id-ID-GadisNeural",
        "pitch": "+6Hz",
        "rate": "+15%",
        "description": "Persuasif, menarik perhatian seketika, dan punya impact kuat dalam waktu singkat."
    },
    "vo_motivator_pria": {
        "name": "⚡ Suara Motivator Pria Energik",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+5Hz",
        "rate": "+14%",
        "description": "Laki-laki semangat, energik, membakar semangat perjuangan, memberikan pujian dan motivasi kuat."
    },
    "custom": {
        "name": "Custom / Kustom Mandiri",
        "voice": "id-ID-ArdiNeural",
        "pitch": "+0Hz",
        "rate": "+0%",
        "description": "Konfigurasi bebas sesuai kebutuhan Anda."
    }
}

class TTSRequest(BaseModel):
    text: str
    character_id: Optional[str] = "prof_gasing_mentor"
    voice: Optional[str] = "id-ID-ArdiNeural"
    pitch: Optional[str] = "+0Hz"
    rate: Optional[str] = "+0%"
    volume: Optional[str] = "+0%"

class AudioProcessRequest(BaseModel):
    rel_path: str
    pitch_semitones: Optional[float] = 0.0
    speed_factor: Optional[float] = 1.0
    bass_gain: Optional[float] = 0.0
    treble_gain: Optional[float] = 0.0
    format: Optional[str] = "wav" # "wav" or "mp3"

def build_atempo_filter(factor: float) -> str:
    """Helper to chain FFmpeg atempo filters if factor is out of [0.5, 2.0]."""
    filters = []
    val = factor
    while val > 2.0:
        filters.append("atempo=2.0")
        val /= 2.0
    while val < 0.5:
        filters.append("atempo=0.5")
        val /= 0.5
    filters.append(f"atempo={round(val, 4)}")
    return ",".join(filters)

def get_audio_sample_rate(filepath: str) -> int:
    """Detect native audio sample rate using ffprobe to prevent speed-up bugs during pitch shifting."""
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate",
            "-of", "default=noprint_wrappers=1:nokey=1", filepath
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        val = int(res.stdout.strip())
        if val > 0:
            return val
    except Exception:
        pass
    return 44100

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "presets_count": len(CHARACTER_PRESETS),
        "engine": "Edge-TTS + FFmpeg DSP"
    }

@app.get("/api/catalog")
def get_catalog():
    if not os.path.exists(CATALOG_PATH):
        raise HTTPException(status_code=404, detail="Audio catalog file not found")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "catalog": data,
        "presets": CHARACTER_PRESETS
    }

@app.post("/api/tts")
async def generate_tts(req: TTSRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Naskah tidak boleh kosong")

    # Determine voice parameters
    preset = CHARACTER_PRESETS.get(req.character_id, CHARACTER_PRESETS["prof_gasing_mentor"])
    voice = req.voice if req.voice else preset["voice"]
    pitch = req.pitch if req.pitch else preset["pitch"]
    rate = req.rate if req.rate else preset["rate"]
    volume = req.volume if req.volume else "+0%"

    req_id = uuid.uuid4().hex[:10]
    temp_mp3 = os.path.join(OUTPUT_DIR, f"tts_{req_id}_temp.mp3")
    final_wav = os.path.join(OUTPUT_DIR, f"SO_TTS_{req.character_id}_{req_id}.wav")
    wav_filename = os.path.basename(final_wav)

    try:
        import edge_tts
        communicate = edge_tts.Communicate(
            text=req.text,
            voice=voice,
            pitch=pitch,
            rate=rate,
            volume=volume
        )
        await communicate.save(temp_mp3)

        # Convert to standard 16-bit PCM 44.1kHz WAV
        cmd = [
            "ffmpeg", "-y", "-i", temp_mp3,
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            final_wav
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(f"FFmpeg conversion error: {res.stderr}")

        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

        # Get audio duration
        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", final_wav]
        dur_res = subprocess.run(dur_cmd, capture_output=True, text=True)
        dur = float(dur_res.stdout.strip()) if dur_res.stdout.strip() else 0.0

        return {
            "status": "success",
            "audio_url": f"/output/{wav_filename}",
            "filename": wav_filename,
            "duration": round(dur, 2),
            "character": preset["name"],
            "voice_used": voice,
            "pitch_used": pitch,
            "rate_used": rate
        }
    except Exception as e:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-audio")
def process_audio(req: AudioProcessRequest):
    # Resolve relative path
    clean_rel = req.rel_path.lstrip("/")
    if clean_rel.startswith("assets/audio/"):
        clean_rel = clean_rel[len("assets/audio/"):]
    elif clean_rel.startswith("assets/"):
        clean_rel = clean_rel[len("assets/"):]
    elif clean_rel.startswith("output/"):
        clean_rel = clean_rel[len("output/"):]

    src_file = os.path.join(AUDIO_DIR, clean_rel)
    if not os.path.exists(src_file):
        out_src = os.path.join(OUTPUT_DIR, clean_rel)
        if os.path.exists(out_src):
            src_file = out_src
        else:
            raise HTTPException(status_code=404, detail=f"File audio sumber tidak ditemukan: {clean_rel}")

    semitones = req.pitch_semitones or 0.0
    speed = req.speed_factor or 1.0

    req_id = uuid.uuid4().hex[:10]
    base_name = os.path.splitext(os.path.basename(src_file))[0]
    out_format = "mp3" if (req.format and req.format.lower() == "mp3") else "wav"
    output_filename = f"Tuned_{base_name}_p{int(semitones)}_s{int(speed*100)}_{req_id}.{out_format}"
    out_file = os.path.join(OUTPUT_DIR, output_filename)

    # Detect source sample rate to prevent chipmunk / speedup corruption on 24kHz F5-TTS audio
    in_sr = get_audio_sample_rate(src_file)
    pitch_factor = 2.0 ** (semitones / 12.0)
    effective_tempo = (1.0 / pitch_factor) * speed

    filter_chains = []

    # Only apply pitch shifting / tempo stretching if actually modified
    if abs(semitones) > 0.01 or abs(speed - 1.0) > 0.01:
        atempo_filter = build_atempo_filter(effective_tempo)
        filter_chains.append(f"asetrate={in_sr}*{round(pitch_factor, 6)}")
        filter_chains.append(atempo_filter)
        filter_chains.append("aresample=44100")

    if req.bass_gain and abs(req.bass_gain) > 0.1:
        filter_chains.append(f"equalizer=f=120:width_type=o:w=1:g={round(req.bass_gain, 1)}")
    if req.treble_gain and abs(req.treble_gain) > 0.1:
        filter_chains.append(f"equalizer=f=4000:width_type=o:w=1:g={round(req.treble_gain, 1)}")

    filter_args = []
    if filter_chains:
        full_filter = ",".join(filter_chains)
        filter_args = ["-af", full_filter]

    if out_format == "mp3":
        cmd = [
            "ffmpeg", "-y", "-i", src_file,
            *filter_args,
            "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "320k",
            out_file
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", src_file,
            *filter_args,
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            out_file
        ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise HTTPException(status_code=500, detail=f"FFmpeg DSP error: {res.stderr}")

    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_file]
    dur_res = subprocess.run(dur_cmd, capture_output=True, text=True)
    dur = float(dur_res.stdout.strip()) if dur_res.stdout.strip() else 0.0

    return {
        "status": "success",
        "audio_url": f"/output/{output_filename}",
        "filename": output_filename,
        "duration": round(dur, 2),
        "source_file": os.path.basename(src_file),
        "pitch_semitones": semitones,
        "speed_factor": speed
    }

# =========================================================================
# F5-TTS INDO FINETUNE V2 & VOICE CLONING ENDPOINTS
# =========================================================================

class F5TTSRequest(BaseModel):
    voice_id: str = "so_marcia"
    text: str
    speed: Optional[float] = 1.0
    nfe_step: Optional[int] = 32
    output_format: Optional[str] = "wav" # "wav" or "mp3"
    apply_bilingual: Optional[bool] = True
    apply_gasing: Optional[bool] = True

class PronunciationPreviewRequest(BaseModel):
    text: str
    apply_bilingual: Optional[bool] = True
    apply_gasing: Optional[bool] = True

@app.get("/api/f5/status")
def get_f5_status():
    engine = F5IndoEngine.get_instance()
    return engine.get_status()

@app.post("/api/f5/download-model")
def download_f5_model(background_tasks: BackgroundTasks):
    engine = F5IndoEngine.get_instance()
    if engine.is_model_installed():
        return {"status": "already_installed", "message": "Model F5-TTS Indo V2 sudah terpasang."}

    # Jalankan download di background thread
    background_tasks.add_task(engine.download_model_weights)
    return {"status": "download_started", "message": "Pengunduhan model F5-TTS Indo V2 (~1.34 GB) dimulai di latar belakang."}

@app.get("/api/f5/voices")
def get_f5_voices():
    engine = F5IndoEngine.get_instance()
    voices = engine.get_all_voices()
    return {
        "status": "success",
        "total": len(voices),
        "voices": voices
    }

@app.delete("/api/f5/voices/{voice_id}")
def delete_f5_voice(voice_id: str):
    """Menghapus profil kloning suara buatan pengguna / trainer."""
    protected_system_voices = ["blaze_original", "eem_reporter", "eem_prabowo", "eem_windah", "so_marcia", "at_john", "prof_yosu_asli"]
    if voice_id in protected_system_voices:
        raise HTTPException(status_code=400, detail="Model suara bawaan sistem tidak dapat dihapus.")
    
    engine = F5IndoEngine.get_instance()
    success = engine.delete_voice_profile(voice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Model suara tidak ditemukan atau sudah dihapus.")
    
    return {
        "status": "success",
        "message": f"Model suara berhasil dihapus.",
        "deleted_voice_id": voice_id
    }

@app.post("/api/f5/auto-clone-marcia")
def auto_clone_marcia_endpoint():
    engine = F5IndoEngine.get_instance()
    try:
        profile = engine.auto_clone_marcia()
        return {
            "status": "success",
            "message": "Suara Guru Marcia berhasil diekstrak otomatis dari rekaman master 6 menit!",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/f5/auto-clone-john")
def auto_clone_john_endpoint():
    engine = F5IndoEngine.get_instance()
    try:
        profile = engine.auto_clone_john()
        return {
            "status": "success",
            "message": "Suara Tutor John berhasil diekstrak otomatis dari video Tanya Marcia!",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/f5/auto-clone-prof")
def auto_clone_prof_endpoint():
    engine = F5IndoEngine.get_instance()
    try:
        profile = engine.auto_clone_prof_gasing()
        return {
            "status": "success",
            "message": "Suara Prof. Yohanes Surya berhasil di-clone dari rekaman audio autentik!",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/f5/clone-voice")
async def clone_custom_voice(
    file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
    name: str = Form(...),
    category: Optional[str] = Form("custom"),
    gender: Optional[str] = Form("Pria"),
    role: Optional[str] = Form("Narator Kustom"),
    region: Optional[str] = Form(""),
    ref_text: Optional[str] = Form(""),
    description: Optional[str] = Form("")
):
    """Menerima file rekaman mic atau upload audio, lalu menyimpannya sebagai profil kloning suara."""
    upload_f = file or audio_file
    if not upload_f:
        raise HTTPException(status_code=400, detail="File audio harus diunggah atau direkam.")

    engine = F5IndoEngine.get_instance()
    cloned_dir = os.path.join(BASE_DIR, "assets", "cloned_voices")
    os.makedirs(cloned_dir, exist_ok=True)

    voice_id = f"voice_{uuid.uuid4().hex[:8]}"
    raw_ext = os.path.splitext(upload_f.filename or "sample.wav")[1] or ".wav"
    raw_temp = os.path.join(cloned_dir, f"{voice_id}_raw{raw_ext}")
    final_wav = os.path.join(cloned_dir, f"{voice_id}.wav")

    try:
        with open(raw_temp, "wb") as f:
            shutil.copyfileobj(upload_f.file, f)

        # Standarisasi ke 24kHz mono WAV untuk F5-TTS
        engine.ensure_standard_audio_ref(raw_temp, final_wav)
        if os.path.exists(raw_temp):
            os.remove(raw_temp)

        transcript = ref_text.strip() if ref_text and ref_text.strip() else "Saya sedang merekam suara untuk panduan modul pembelajaran matematika gasing."

        profile = {
            "id": voice_id,
            "name": name.strip(),
            "role": role.strip(),
            "category": category.strip(),
            "gender": gender,
            "region": region.strip() if region else "",
            "ref_audio": f"/assets/cloned_voices/{voice_id}.wav",
            "ref_audio_abs": final_wav,
            "ref_text": transcript,
            "avatar": "🎙️" if gender == "Pria" else "🎤",
            "description": description.strip() or f"Kloning suara mandiri: {name.strip()}" + (f" ({region.strip()})" if region else "")
        }
        engine.save_voice_profile(profile)

        return {
            "status": "success",
            "message": f"Profil suara '{name}' berhasil dikloning!",
            "profile": profile
        }
    except Exception as e:
        if os.path.exists(raw_temp):
            os.remove(raw_temp)
        raise HTTPException(status_code=500, detail=f"Gagal memproses kloning suara: {str(e)}")

@app.post("/api/f5/clone-trainer")
async def clone_trainer_voice(
    file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
    trainer_name: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    region: Optional[str] = Form("GASING Nasional"),
    specialty: Optional[str] = Form("Tutor Modul Hitung"),
    narrator_role: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    gender: Optional[str] = Form("Pria"),
    ref_text: Optional[str] = Form("")
):
    """Endpoint khusus untuk kloning suara Asisten Trainer (AT) GASING dengan metadata lengkap."""
    upload_f = file or audio_file
    if not upload_f:
        raise HTTPException(status_code=400, detail="File audio harus diunggah.")

    final_name = name or trainer_name
    if not final_name or not final_name.strip():
        raise HTTPException(status_code=400, detail="Nama trainer harus diisi.")

    final_role = role or narrator_role or "Narator Modul & Game SO"

    engine = F5IndoEngine.get_instance()
    cloned_dir = os.path.join(BASE_DIR, "assets", "cloned_voices")
    os.makedirs(cloned_dir, exist_ok=True)

    trainer_id = f"at_{uuid.uuid4().hex[:8]}"
    raw_ext = os.path.splitext(upload_f.filename or "rec.wav")[1] or ".wav"
    raw_temp = os.path.join(cloned_dir, f"{trainer_id}_raw{raw_ext}")
    final_wav = os.path.join(cloned_dir, f"{trainer_id}.wav")

    try:
        with open(raw_temp, "wb") as f:
            shutil.copyfileobj(upload_f.file, f)

        engine.ensure_standard_audio_ref(raw_temp, final_wav)
        if os.path.exists(raw_temp):
            os.remove(raw_temp)

        transcript = ref_text.strip() if ref_text and ref_text.strip() else "Halo adik-adik pintar! Hari ini kita akan belajar matematika gasing bersama, gampang, asyik, dan menyenangkan!"

        profile_name = final_name.strip()
        if not profile_name.startswith("AT "):
            profile_name = f"AT {profile_name}"

        profile = {
            "id": trainer_id,
            "name": profile_name,
            "role": final_role.strip(),
            "category": "trainer_gasing",
            "gender": gender,
            "region": region.strip(),
            "specialty": specialty.strip(),
            "ref_audio": f"/assets/cloned_voices/{trainer_id}.wav",
            "ref_audio_abs": final_wav,
            "ref_text": transcript,
            "avatar": "👨‍🏫" if gender == "Pria" else "👩‍🏫",
            "description": f"Trainer GASING ({region.strip()}) — {final_role.strip()}"
        }
        engine.save_voice_profile(profile)

        return {
            "status": "success",
            "message": f"Suara {profile_name} berhasil dikloning sebagai narator!",
            "profile": profile
        }
    except Exception as e:
        if os.path.exists(raw_temp):
            os.remove(raw_temp)
        raise HTTPException(status_code=500, detail=f"Gagal mengkloning suara AT: {str(e)}")

@app.post("/api/f5/preview-pronunciation")
def preview_pronunciation(req: PronunciationPreviewRequest):
    """Menampilkan pratinjau teks hasil normalisasi fonetik bilingual & pujian GASING."""
    processed = preprocess_pronunciation(
        req.text,
        apply_bilingual=req.apply_bilingual if req.apply_bilingual is not None else True,
        apply_gasing_prosody=req.apply_gasing if req.apply_gasing is not None else True
    )
    chunks = split_into_smart_chunks(processed)
    return {
        "original_text": req.text,
        "processed_text": processed,
        "normalized_preview": processed,
        "chunks": chunks,
        "chunk_count": len(chunks),
        "chunks_count": len(chunks)
    }

@app.post("/api/f5/tts")
def generate_f5_tts(req: F5TTSRequest):
    """Menjalankan sintesis suara cloning F5-TTS Indo Finetune V2."""
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Naskah tidak boleh kosong.")

    engine = F5IndoEngine.get_instance()
    if not engine.is_model_installed():
        raise HTTPException(
            status_code=503,
            detail="Model F5-TTS Indo V2 belum terpasang. Silakan unduh model terlebih dahulu."
        )

    # Cari profil suara yang dipilih
    all_voices = engine.get_all_voices()
    selected_voice = next((v for v in all_voices if v.get("id") == req.voice_id), None)
    if not selected_voice:
        # Fallback ke Marcia atau reporter
        selected_voice = all_voices[0]

    ref_audio = selected_voice.get("ref_audio_abs")
    if not ref_audio or not os.path.exists(ref_audio):
        # Jika file path lokal relatif
        clean_ref = selected_voice.get("ref_audio", "").lstrip("/")
        candidate = os.path.join(BASE_DIR, clean_ref)
        if os.path.exists(candidate):
            ref_audio = candidate
        else:
            raise HTTPException(status_code=404, detail=f"File referensi suara tidak ditemukan: {ref_audio}")

    ref_text = selected_voice.get("ref_text", "Selamat pagi, salam sejahtera bagi kita sekalian.")

    try:
        result = engine.generate(
            ref_audio_path=ref_audio,
            ref_text=ref_text,
            gen_text=req.text,
            speed=req.speed or 1.0,
            nfe_step=req.nfe_step or 32,
            output_format=req.output_format or "wav",
            apply_bilingual=req.apply_bilingual if req.apply_bilingual is not None else True,
            apply_gasing=req.apply_gasing if req.apply_gasing is not None else True
        )
        result["character_name"] = selected_voice.get("name")
        result["character_role"] = selected_voice.get("role")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"F5-TTS Generation Error: {str(e)}")

# Mount static folders
app.mount("/models", StaticFiles(directory=os.path.join(BASE_DIR, "models")), name="models")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
REKOMENDASI_DIR = os.path.join(BASE_DIR, "rekomendasi AI")
if os.path.exists(REKOMENDASI_DIR):
    app.mount("/rekomendasi-ai", StaticFiles(directory=REKOMENDASI_DIR), name="rekomendasi-ai")
MARCIA_CONTOH_DIR = os.path.join(BASE_DIR, "AT Marcia contoh")
if os.path.exists(MARCIA_CONTOH_DIR):
    app.mount("/at-marcia-contoh", StaticFiles(directory=MARCIA_CONTOH_DIR), name="at-marcia-contoh")

# Serve UI static files with anti-cache headers
@app.get("/")
def serve_index():
    response = FileResponse(os.path.join(BASE_DIR, "index.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.get("/app.js")
def serve_js():
    response = FileResponse(os.path.join(BASE_DIR, "app.js"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/styles.css")
def serve_css():
    response = FileResponse(os.path.join(BASE_DIR, "styles.css"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8765, reload=True)
