#!/usr/bin/env python3
"""
execute_zona4_level6_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk Video Zona 4 Level 6:
File: "zona 4 level 6.mp4" (186.70 detik)
Materi: Pengurangan 4 Digit dengan 4 Digit Meminjam Beruntun & Kasus Nol di Tengah
        Soal 1: 8021 - 1329 = 6692 (Cara Pecah & Mencongak)
        Soal 2: 8223 - 5224 = 2999 (Cara Pecah & Mencongak Lirik Kanan Beruntun)

Standar Kualitas Mutlak:
1. Suara Karakter: Guru Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2, nfe=32, speed=1.05) + Edge-TTS Studio (id-ID-GadisNeural).
2. Artikulasi Fonetik Penuh: Semua angka dieja 100% lengkap tanpa salah sebut ("seribu", "seratus", "delapan ribu dua puluh satu", dsb).
3. Zero-Noise Master: Rantai DSP highpass 80Hz + loudnorm broadcast -16 LUFS (meniadakan desisan & rumble).
4. Video Track Asli 100%: Menggunakan video track asli tanpa pemotongan / masking persegi buatan agar TIDAK ADA garis putus atau teks terpotong.
5. Kompresi Ringan: H.264 tune animation CRF 28 & WebM VP9 CRF 36.
6. Distribusi Otomatis ke:
   - Data VIdeo Marcia/zona 4 level 6_ringan.mp4
   - Hasil/videoMarcia/z4_pengurangan/
   - Proyek SO: web/public/assets/videos/z4l6/
   - Web Studio: video_projects/z4l6_pengurangan_4d_4d_meminjam/
"""

import os
import sys
import json
import time
import shutil
import asyncio
import subprocess
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from f5_engine import F5IndoEngine

DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
VIDEO_PROJECTS_DIR = os.path.join(BASE_DIR, "video_projects")
HASIL_Z4_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
SO_Z4L6_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l6"

os.makedirs(HASIL_Z4_DIR, exist_ok=True)
os.makedirs(SO_Z4L6_DIR, exist_ok=True)

VIDEO_CFG = {
    "id": "z4l6_pengurangan_4d_4d_meminjam",
    "source_filename": "zona 4 level 6.mp4",
    "so_dest_stem": "z4l6sb1bermain1_marcia",
    "so_game_name": "Rahasia Perpustakaan Taj Mahal (z4l6-sb1bermain1)",
    "title": "Zona 4 Level 6: Pengurangan 4D - 4D Meminjam (8021 - 1329 & 8223 - 5224)",
    "subtitle": "Pengurangan 4 digit dengan 4 digit meminjam ganda, kasus 0 di tengah, dan mencongak lirik kanan beruntun.",
    "duration": 186.70,
    "segments": [
        # SOAL 1: 8021 - 1329 = 6692 (Cara Pecah)
        {
            "id": 1,
            "start": 0.00,
            "end": 4.50,
            "text": "Delapan ribu dua puluh satu dikurang seribu tiga ratus dua puluh sembilan.",
            "display_text": "8021 dikurang 1329.",
            "visual": "Menuliskan soal 8021 - 1329"
        },
        {
            "id": 2,
            "start": 4.60,
            "end": 11.50,
            "text": "Kita lihat dulu satuannya, tidak bisa dikurangi maka ini dipecah menjadi satu puluhan dan sepuluh satuan.",
            "display_text": "Kita lihat dulu satuannya, tidak bisa dikurangi maka ini dipecah menjadi 1 puluhan dan 10 satuan.",
            "visual": "Memecah 20 menjadi 1 puluhan dan 10 satuan"
        },
        {
            "id": 3,
            "start": 11.96,
            "end": 16.80,
            "text": "Satu dikurang dua ini tidak bisa, maka nolnya ini harus dipecah.",
            "display_text": "1 dikurang 2 ini tidak bisa, maka 0-nya ini harus dipecah.",
            "visual": "Mengecek 1 puluhan tidak bisa dikurang 2"
        },
        {
            "id": 4,
            "start": 16.90,
            "end": 20.60,
            "text": "Tapi kan nol tidak bisa dipecah, jadi kita pecah dari delapan.",
            "display_text": "Tapi kan 0 tidak bisa dipecah, jadi kita pecah dari 8.",
            "visual": "Memilih memecah dari angka 8 (ribuan)"
        },
        {
            "id": 5,
            "start": 20.66,
            "end": 27.00,
            "text": "Delapan ini kita pecah menjadi tujuh ribuan di sini dan sepuluh ratusan.",
            "display_text": "8 ini kita pecah menjadi 7 ribuan dan 10 ratusan.",
            "visual": "Memecah 8 ribuan menjadi 7 ribuan dan 10 ratusan"
        },
        {
            "id": 6,
            "start": 27.30,
            "end": 34.00,
            "text": "Nah sekarang karena tadi nol tidak bisa dipecah, kita pecah sepuluhnya menjadi sembilan dan sepuluh.",
            "display_text": "Nah sekarang karena tadi 0 tidak bisa dipecah, kita pecah 10-nya menjadi 9 dan 10.",
            "visual": "Memecah 10 ratusan menjadi 9 ratusan dan 10 puluhan"
        },
        {
            "id": 7,
            "start": 34.88,
            "end": 42.20,
            "text": "Baru sekarang kita bisa kerjakan dari depan, yaitu dari ribuan: tujuh dikurang satu adalah enam.",
            "display_text": "Mulai dari depan, ribuan: 7 dikurang 1 adalah 6.",
            "visual": "Menghitung ribuan 7 - 1 = 6"
        },
        {
            "id": 8,
            "start": 42.50,
            "end": 45.60,
            "text": "Sembilan dikurang tiga adalah enam.",
            "display_text": "9 dikurang 3 adalah 6.",
            "visual": "Menghitung ratusan 9 - 3 = 6"
        },
        {
            "id": 9,
            "start": 45.80,
            "end": 50.80,
            "text": "Sepuluh dikurang dua adalah delapan, masih ada satu jadi sembilan.",
            "display_text": "10 dikurang 2 adalah 8, masih ada 1 jadi 9.",
            "visual": "Menghitung puluhan: 10 - 2 = 8, 8 + 1 = 9"
        },
        {
            "id": 10,
            "start": 51.10,
            "end": 54.10,
            "text": "Sepuluh dikurang sembilan adalah satu.",
            "display_text": "10 dikurang 9 adalah 1.",
            "visual": "Menghitung satuan: 10 - 9 = 1"
        },
        {
            "id": 11,
            "start": 54.14,
            "end": 60.50,
            "text": "Tapi ingat, di sini masih ada satu lagi, jadi hasilnya satu tambah satu yaitu dua. Jadi hasilnya enam ribu enam ratus sembilan puluh dua.",
            "display_text": "1 + 1 = 2. Jadi hasilnya 6692.",
            "visual": "Menuliskan hasil akhir 6692"
        },
        # SOAL 1: 8021 - 1329 = 6692 (Cara Mencongak)
        {
            "id": 12,
            "start": 60.66,
            "end": 63.38,
            "text": "Nah sekarang cara mencongaknya demikian.",
            "display_text": "Nah sekarang cara mencongaknya demikian.",
            "visual": "Beralih ke Cara Mencongak"
        },
        {
            "id": 13,
            "start": 63.38,
            "end": 71.80,
            "text": "Delapan dikurang satu tujuh, lirik kanan tidak bisa dikurangi maka tujuh kurang satu yaitu enam.",
            "display_text": "8 - 1 = 7, lirik kanan tidak bisa, 7 - 1 = 6.",
            "visual": "8 - 1 = 7, lirik kanan kurangi 1 jadi 6"
        },
        {
            "id": 14,
            "start": 72.00,
            "end": 77.18,
            "text": "Kemudian nol ditambah pasangan tiga. Pasangan tiga adalah tujuh.",
            "display_text": "0 + pasangan 3. Pasangan 3 adalah 7.",
            "visual": "0 + pasangan 3 (7) = 7"
        },
        {
            "id": 15,
            "start": 77.18,
            "end": 82.80,
            "text": "Nah kemudian kita lirik kanan, ternyata di sini hasilnya nol.",
            "display_text": "Lirik kanan ternyata di sini 0 (2 - 2).",
            "visual": "Lirik kanan 2 - 2 = 0"
        },
        {
            "id": 16,
            "start": 83.10,
            "end": 89.80,
            "text": "Lirik kanan lagi tidak bisa dikurangi, maka tadi tujuh itu kita kurangi satu jadi enam.",
            "display_text": "Lirik kanan lagi tidak bisa, maka 7 kurangi 1 jadi 6.",
            "visual": "Lirik kanan lagi (1 < 9), kurangi ratusan 7 - 1 = 6"
        },
        {
            "id": 17,
            "start": 89.90,
            "end": 93.64,
            "text": "Nah kemudian nol itu menjadi sembilan.",
            "display_text": "Nah kemudian 0 itu menjadi 9.",
            "visual": "Puluhan 0 menjadi 9"
        },
        {
            "id": 18,
            "start": 93.64,
            "end": 100.50,
            "text": "Lalu satu ditambah pasangan dari sembilan, yaitu satu tambah satu hasilnya dua. Jadi hasilnya enam ribu enam ratus sembilan puluh dua.",
            "display_text": "1 + pasangan 9 (1) = 2. Hasil: 6692.",
            "visual": "1 + 1 = 2, hasil akhir 6692"
        },
        # SOAL 2: 8223 - 5224 = 2999 (Cara Pecah)
        {
            "id": 19,
            "start": 100.64,
            "end": 106.00,
            "text": "Nah berikutnya kita hitung delapan ribu dua ratus dua puluh tiga dikurang lima ribu dua ratus dua puluh empat.",
            "display_text": "Berikutnya hitung 8223 dikurang 5224.",
            "visual": "Menuliskan soal 8223 - 5224"
        },
        {
            "id": 20,
            "start": 106.90,
            "end": 114.00,
            "text": "Kita lihat satuannya tidak bisa dikurangi, maka puluhannya ini kita pecah menjadi satu dan sepuluh.",
            "display_text": "Satuan tidak bisa dikurangi, pecah puluhan 2 jadi 1 dan 10.",
            "visual": "Memecah 20 menjadi 1 puluhan dan 10 satuan"
        },
        {
            "id": 21,
            "start": 114.30,
            "end": 120.80,
            "text": "Satu tidak bisa dikurangi dengan dua, sehingga dua ini kita pecah menjadi satu dan sepuluh.",
            "display_text": "1 tidak bisa dikurangi 2, pecah ratusan 2 jadi 1 dan 10.",
            "visual": "Memecah ratusan 2 menjadi 1 dan 10"
        },
        {
            "id": 22,
            "start": 121.00,
            "end": 131.50,
            "text": "Nah kemudian kita lihat satu tidak bisa dikurangi dengan dua, sehingga delapannya kita pecah menjadi tujuh dan sepuluh.",
            "display_text": "1 tidak bisa dikurangi 2, pecah 8 ribuan jadi 7 dan 10.",
            "visual": "Memecah 8 ribuan menjadi 7 dan 10"
        },
        {
            "id": 23,
            "start": 132.30,
            "end": 137.00,
            "text": "Sekarang kita kurangi dari depan, yaitu ribuannya: tujuh kurang lima, dua.",
            "display_text": "Ribuan: 7 kurang 5 = 2.",
            "visual": "Menghitung ribuan 7 - 5 = 2"
        },
        {
            "id": 24,
            "start": 137.10,
            "end": 144.20,
            "text": "Kemudian ratusannya: sepuluh kurang dua, delapan, masih ada satu jadi sembilan.",
            "display_text": "Ratusan: 10 - 2 = 8, 8 + 1 = 9.",
            "visual": "Menghitung ratusan: 10 - 2 = 8, 8 + 1 = 9"
        },
        {
            "id": 25,
            "start": 144.50,
            "end": 149.50,
            "text": "Lalu puluhannya: sepuluh kurang dua masih ada satu, sembilan.",
            "display_text": "Puluhan: 10 - 2 = 8, 8 + 1 = 9.",
            "visual": "Menghitung puluhan: 10 - 2 = 8, 8 + 1 = 9"
        },
        {
            "id": 26,
            "start": 149.90,
            "end": 158.00,
            "text": "Dan terakhir satuannya: sepuluh kurang empat, enam, masih ada tiga, sembilan. Jadi hasilnya dua ribu sembilan ratus sembilan puluh sembilan.",
            "display_text": "Satuan: 10 - 4 = 6, 6 + 3 = 9. Hasil: 2999.",
            "visual": "Menghitung satuan: 10 - 4 = 6, 6 + 3 = 9. Hasil: 2999"
        },
        # SOAL 2: 8223 - 5224 = 2999 (Cara Mencongak)
        {
            "id": 27,
            "start": 158.50,
            "end": 164.20,
            "text": "Nah sekarang kita gunakan cara mencongak: delapan dikurang lima, tiga.",
            "display_text": "Mencongak: 8 dikurang 5 = 3.",
            "visual": "Ribuan: 8 - 5 = 3"
        },
        {
            "id": 28,
            "start": 164.30,
            "end": 170.50,
            "text": "Lirik kanan nol, lirik kanan nol, lirik kanan tidak bisa.",
            "display_text": "Lirik kanan 0 (2 - 2), lirik kanan 0 (2 - 2), lirik kanan tidak bisa (3 < 4).",
            "visual": "Lirik kanan beruntun: 0, 0, tidak bisa"
        },
        {
            "id": 29,
            "start": 170.60,
            "end": 174.20,
            "text": "Berarti kita kurangi satu, tiga kurang satu, dua.",
            "display_text": "Kurangi 1, 3 kurang 1 = 2.",
            "visual": "Mengurangi ribuan 3 - 1 = 2"
        },
        {
            "id": 30,
            "start": 174.40,
            "end": 178.50,
            "text": "Nah nolnya itu menjadi sembilan, sembilan.",
            "display_text": "Nah 0-nya itu menjadi 9, 9.",
            "visual": "Ratusan dan puluhan 0 menjadi 9, 9"
        },
        {
            "id": 31,
            "start": 178.70,
            "end": 186.70,
            "text": "Nah kemudian tiga ditambah pasangan empat yaitu enam, tambah tiga jadi sembilan. Jadi hasilnya dua ribu sembilan ratus sembilan puluh sembilan.",
            "display_text": "3 + pasangan 4 (6) = 9. Hasil: 2999.",
            "visual": "3 + 6 = 9. Hasil akhir 2999"
        }
    ]
}

def format_bytes(num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} TB"

def get_audio_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_atempo_filter(tempo: float) -> str:
    parts = []
    curr = tempo
    while curr > 2.0:
        parts.append("atempo=2.0")
        curr /= 2.0
    while curr < 0.5:
        parts.append("atempo=0.5")
        curr /= 0.5
    parts.append(f"atempo={curr:.4f}")
    return ",".join(parts)

async def synthesize_edge_segment(text: str, out_path: str, voice: str = "id-ID-GadisNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="+5%", pitch="+0Hz")
    await communicate.save(out_path)

def run_ffmpeg(cmd, desc="FFmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg Gagal [{desc}]: {res.stderr[-400:]}")
        raise RuntimeError(f"FFmpeg error: {res.stderr[-400:]}")
    return res

async def main():
    t_start = time.time()
    vid_id = VIDEO_CFG["id"]
    src_file = os.path.join(DATA_VIDEO_DIR, VIDEO_CFG["source_filename"])
    total_dur = VIDEO_CFG["duration"]
    segments = VIDEO_CFG["segments"]
    so_dest_stem = VIDEO_CFG["so_dest_stem"]

    print("\n" + "=" * 75)
    print(f"🎬 MEMPROSES ZONA 4 LEVEL 6: {VIDEO_CFG['title']}")
    print(f"   Target SO Game: {VIDEO_CFG['so_game_name']} -> {so_dest_stem}")
    print(f"   Sumber Video  : {src_file} ({format_bytes(os.path.getsize(src_file))})")
    print(f"   Durasi Total  : {total_dur:.2f} detik | {len(segments)} Segmen Dialog")
    print("=" * 75)

    # 1. Project Directory Setup
    project_dir = os.path.join(VIDEO_PROJECTS_DIR, vid_id)
    segments_dir = os.path.join(project_dir, "segments")
    os.makedirs(segments_dir, exist_ok=True)

    clip_orig = os.path.join(project_dir, "clip_original.mp4")
    shutil.copyfile(src_file, clip_orig)

    # 2. Extract original audio 24k
    orig_wav = os.path.join(project_dir, "original_audio_24k.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
        orig_wav
    ], "Extract 24k audio")

    # 3. Initialize F5-TTS Engine
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."
    engine = F5IndoEngine()

    import librosa
    import soundfile as sf
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"

    print(f"\n▶ Fase 1: Sintesis F5-TTS & Edge-TTS Trainer Marcia ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        print(f"  [{sid:02d}/{len(segments)}] \"{text[:45]}...\"")

        # A. F5-TTS
        t0 = time.time()
        res_f5 = engine.generate(
            ref_audio_path=marcia_ref,
            ref_text=marcia_ref_text,
            gen_text=text,
            speed=1.05,
            nfe_step=32,
            output_format="wav"
        )
        raw_f5 = os.path.join(BASE_DIR, res_f5["audio_url"].lstrip("/"))

        # Silence trimming
        y, sr = librosa.load(raw_f5, sr=24000)
        y_trim, _ = librosa.effects.trim(y, top_db=25)
        trim_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_trimmed.wav")
        sf.write(trim_f5, y_trim, sr)
        trim_dur = len(y_trim) / sr

        # Alignment
        tempo_f5 = trim_dur / target_dur if target_dur > 0 else 1.0
        tempo_f5 = max(0.85, min(1.25, tempo_f5))
        atempo_f5 = build_atempo_filter(tempo_f5)
        aligned_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_aligned.wav")
        run_ffmpeg([
            "ffmpeg", "-y", "-i", trim_f5,
            "-af", f"{atempo_f5},{MASTER_FILTER}",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            aligned_f5
        ], f"Align F5 seg {sid}")
        s["audio_f5"] = aligned_f5
        s["start_f5"] = s["start"]
        s["dur_f5"] = get_audio_duration(aligned_f5)

        # B. Edge-TTS Studio
        raw_edge = os.path.join(segments_dir, f"edge_seg_{sid}_raw.mp3")
        await synthesize_edge_segment(text, raw_edge)
        edge_dur = get_audio_duration(raw_edge)
        tempo_edge = edge_dur / target_dur if target_dur > 0 else 1.0
        tempo_edge = max(0.85, min(1.25, tempo_edge))
        atempo_edge = build_atempo_filter(tempo_edge)
        aligned_edge = os.path.join(segments_dir, f"edge_seg_{sid}_aligned.wav")
        run_ffmpeg([
            "ffmpeg", "-y", "-i", raw_edge,
            "-af", f"{atempo_edge},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            aligned_edge
        ], f"Align Edge seg {sid}")
        s["audio_edge"] = aligned_edge
        elapsed = time.time() - t0
        print(f"     ✓ Selesai dalam {elapsed:.1f}s | Durasi F5: {s['dur_f5']:.2f}s | Target: {target_dur:.2f}s")

    # 4. Assemble Master Timelines
    print(f"\n▶ Fase 2: Merakit Master Timeline Audio ({total_dur:.2f}s)...")
    silence_wav = os.path.join(segments_dir, "silence.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(total_dur),
        silence_wav
    ], "Generate silence")

    for mode in ["f5", "edge"]:
        master_wav = os.path.join(project_dir, f"master_dubbing_{mode}.wav")
        master_mp3 = os.path.join(project_dir, f"master_dubbing_{mode}.mp3")

        inputs = ["-i", silence_wav]
        delays = []
        for idx, s in enumerate(segments):
            seg_path = s[f"audio_{mode}"]
            inputs.extend(["-i", seg_path])
            delay_ms = int(s["start"] * 1000)
            delays.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[d{idx+1}]")

        filter_parts = delays
        mix_inputs = "".join([f"[d{i+1}]" for i in range(len(segments))])
        total_in = len(segments) + 1
        filter_parts.append(f"[0:a]{mix_inputs}amix=inputs={total_in}:duration=first:dropout_transition=0,volume=3.0,{MASTER_FILTER}[outa]")
        filter_str = ";".join(filter_parts)

        run_ffmpeg([
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[outa]",
            "-t", str(total_dur),
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            master_wav
        ], f"Mix master {mode}")

        run_ffmpeg([
            "ffmpeg", "-y", "-i", master_wav,
            "-c:a", "libmp3lame", "-b:a", "320k",
            master_mp3
        ], f"Master MP3 {mode}")

    master_f5_wav = os.path.join(project_dir, "master_dubbing_f5.wav")

    # 5. Mux to Original Video Track directly (Guaranteeing ZERO broken lines!)
    print("\n▶ Fase 3: Menggabungkan Audio Marcia dengan Video Asli (Tanpa Garis Putus)...")
    out_mp4 = os.path.join(project_dir, "video_dubbed_marcia_f5_ringan.mp4")
    out_webm = os.path.join(project_dir, "video_dubbed_marcia_f5_ringan.webm")

    # MP4 H.264 tune animation CRF 28 + AAC 48k mono
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", master_f5_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation",
        "-c:a", "aac", "-b:a", "48k", "-ac", "1",
        "-movflags", "+faststart",
        out_mp4
    ], "Encode MP4 Ringan")

    # WebM VP9 CRF 36 + Opus 48k mono
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", master_f5_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-deadline", "good", "-cpu-used", "2",
        "-c:a", "libopus", "-b:a", "48k", "-ac", "1",
        out_webm
    ], "Encode WebM Ringan")

    sz_mp4 = os.path.getsize(out_mp4) / (1024 * 1024)
    sz_webm = os.path.getsize(out_webm) / (1024 * 1024)
    orig_sz = os.path.getsize(src_file) / (1024 * 1024)
    savings = (1 - (os.path.getsize(out_mp4) / os.path.getsize(src_file))) * 100

    print(f"\n📦 Hasil Kompresi Ringan:")
    print(f"  ✓ Ukuran Asli: {orig_sz:.2f} MB")
    print(f"  ✓ MP4 Ringan : {sz_mp4:.2f} MB (Hemat {savings:.1f}%)")
    print(f"  ✓ WebM Ringan: {sz_webm:.2f} MB")

    # 6. Distribusi ke Semua Lokasi
    print("\n▶ Fase 4: Mendistribusikan Berkas ke Seluruh Proyek...")
    # A. Data VIdeo Marcia
    dest_data_video = os.path.join(DATA_VIDEO_DIR, "zona 4 level 6_ringan.mp4")
    shutil.copyfile(out_mp4, dest_data_video)
    print(f"  🚀 Disalin ke Data VIdeo Marcia: {dest_data_video}")

    # B. Hasil/videoMarcia/z4_pengurangan
    shutil.copyfile(out_mp4, os.path.join(HASIL_Z4_DIR, "z4l6_pengurangan_4d_4d_meminjam_marcia_ringan.mp4"))
    shutil.copyfile(out_webm, os.path.join(HASIL_Z4_DIR, "z4l6_pengurangan_4d_4d_meminjam_marcia_ringan.webm"))
    print(f"  🚀 Disalin ke Hasil/videoMarcia/z4_pengurangan/")

    # C. Proyek Smart Otonomi (SO)
    so_mp4 = os.path.join(SO_Z4L6_DIR, "z4l6sb1bermain1_marcia.mp4")
    so_webm = os.path.join(SO_Z4L6_DIR, "z4l6sb1bermain1_marcia.webm")
    shutil.copyfile(out_mp4, so_mp4)
    shutil.copyfile(out_webm, so_webm)
    print(f"  🚀 DISINKRONKAN KE PROYEK SO:")
    print(f"     -> {so_mp4}")
    print(f"     -> {so_webm}")

    # 7. Metadata Project Studio
    meta = {
        "id": vid_id,
        "title": VIDEO_CFG["title"],
        "subtitle": VIDEO_CFG["subtitle"],
        "so_game_name": VIDEO_CFG["so_game_name"],
        "so_dest_stem": so_dest_stem,
        "duration_seconds": total_dur,
        "source_type": "local_mp4",
        "original_file": VIDEO_CFG["source_filename"],
        "original_size_bytes": os.path.getsize(src_file),
        "compressed_mp4_bytes": os.path.getsize(out_mp4),
        "compressed_webm_bytes": os.path.getsize(out_webm),
        "compression_savings_percent": round(savings, 1),
        "original_speaker": "Prof. Yohanes Surya (Pria)",
        "dubbed_character": "Guru Marcia (Trainer Marcia Asli)",
        "voice_id": "so_marcia",
        "acceleration": "F5-TTS nfe_step=32 High-Fidelity + Spelled Out Numbers",
        "noise_filtering": "Highpass 80Hz + Loudnorm broadcast -16 LUFS",
        "files": {
            "original_video": f"/video-projects/{vid_id}/clip_original.mp4",
            "dubbed_video_f5_ringan": f"/video-projects/{vid_id}/video_dubbed_marcia_f5_ringan.mp4",
            "dubbed_audio_f5": f"/video-projects/{vid_id}/master_dubbing_f5.mp3",
            "dubbed_audio_edge": f"/video-projects/{vid_id}/master_dubbing_edge.mp3"
        },
        "so_files": {
            "mp4": f"/assets/videos/z4l6/{so_dest_stem}.mp4",
            "webm": f"/assets/videos/z4l6/{so_dest_stem}.webm"
        },
        "segments": segments
    }
    meta_path = os.path.join(project_dir, "video_project_data.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Metadata Studio tersimpan: {meta_path}")

    total_time = time.time() - t_start
    print(f"\n🎉 SPRINT ZONA 4 LEVEL 6 SELESAI DALAM {total_time:.1f} DETIK!")

if __name__ == "__main__":
    asyncio.run(main())
