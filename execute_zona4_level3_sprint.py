#!/usr/bin/env python3
"""
execute_zona4_level3_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk 4 Video Zona 4 Level 3 (Versi Diperbaiki):
- Seluruh angka dan bilangan diekspansi 100% ke ejaan fonetik bahasa Indonesia utuh:
  (cth: "7" -> "tujuh", "40" -> "empat puluh", "40-an" -> "empat puluhan", "12" -> "dua belas", "33" -> "tiga puluh tiga")
  menghilangkan 100% masalah kata tidak jelas / mumbling ("juang" dll).
- Suara Karakter: Trainer Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2, nfe=32, speed=1.05)
- Alternatif Nol-Noise: Edge-TTS Studio (id-ID-GadisNeural)
- Broadcast Mastering: highpass 80Hz + loudnorm -16 LUFS (artikulasi vokal jernih)
- Kompresi Video Ringan: H.264 tune animation CRF 28, AAC 48k Mono, FastStart + WebM VP9/Opus
- OTOMATIS DIMASUKKAN KE PROYEK SO:
  /Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l3/
  - z4l3sb1bermain2_marcia.mp4 & .webm (Video 1: 45 - 3 = 42, Pasar Malam India Kuno)
  - z4l3sb1bermain1_marcia.mp4 & .webm (Video 2: 40 - 7 = 33, Bowling Kuno India)
  - z4l3sb2bermain2_marcia.mp4 & .webm (Video 3: 12 - 3 = 9 & 15 - 9 = 6, Rahasia Gua Gelap)
  - z4l3sb2bermain1_marcia.mp4 & .webm (Video 4: 41 - 5 = 36, Memanah Guci Kerajaan)
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
SO_Z4L3_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l3"

os.makedirs(HASIL_Z4_DIR, exist_ok=True)
os.makedirs(SO_Z4L3_DIR, exist_ok=True)

VIDEOS_CONFIG = [
    {
        "id": "z4l3_1_pengurangan_2d_1d_tanpa_meminjam",
        "source_filename": "zone 4 level 3-1.mp4",
        "so_dest_stem": "z4l3sb1bermain2_marcia",
        "so_game_name": "Pasar Malam India Kuno (z4l3-sb1bermain2)",
        "title": "Zona 4 Level 3.1: Pengurangan 2D - 1D Tanpa Meminjam (45 - 3 = 42)",
        "subtitle": "Penjelasan konsep pengurangan 2 digit dengan 1 digit di mana satuan bisa langsung dikurangi (puluhan tetap).",
        "duration": 19.93,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 6.86,
                "text": "Untuk menghitung empat puluh lima kurang tiga, kita lihat dulu di sini satuannya, apakah bisa dikurangi?",
                "display_text": "Untuk menghitung 45 kurang 3, kita lihat dulu di sini satuannya, apakah bisa dikurangi?",
                "visual": "Menulis soal 45 - 3 dan menunjuk digit satuan 5 dan 3"
            },
            {
                "id": 2,
                "start": 7.24,
                "end": 12.10,
                "text": "Ya, bisa. Kalau bisa dikurangi, maka puluhannya tetap, yaitu empat.",
                "display_text": "Ya, bisa. Kalau bisa dikurangi, maka puluhannya tetap, yaitu 4.",
                "visual": "Menegaskan puluhan tetap dan menulis angka 4 pada digit puluhan jawaban"
            },
            {
                "id": 3,
                "start": 12.84,
                "end": 19.10,
                "text": "Satuannya kita kurangi, lima kurang tiga adalah dua. Jadi empat puluh lima dikurang tiga adalah empat puluh dua.",
                "display_text": "Satuannya kita kurangi, 5 kurang 3 adalah 2. Jadi 45 dikurang 3 adalah 42.",
                "visual": "Menghitung 5 - 3 = 2 dan menulis hasil akhir 42"
            }
        ]
    },
    {
        "id": "z4l3_2_pengurangan_puluhan_murni_1d",
        "source_filename": "zone 4 level 3-2.mp4",
        "so_dest_stem": "z4l3sb1bermain1_marcia",
        "so_game_name": "Bowling Kuno India (z4l3-sb1bermain1)",
        "title": "Zona 4 Level 3.2: Pengurangan Puluhan Murni - 1D (40 - 7 = 33)",
        "subtitle": "Penjelasan konsep pengurangan puluhan murni dengan 1 digit dengan memecah puluhan menjadi 30 dan 10.",
        "duration": 25.57,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 2.64,
                "text": "Sekarang kita hitung empat puluh kurang tujuh.",
                "display_text": "Sekarang kita hitung 40 kurang 7.",
                "visual": "Menuliskan soal 40 - 7 di papan"
            },
            {
                "id": 2,
                "start": 3.02,
                "end": 6.90,
                "text": "Kita lihat dulu, empat puluh terdiri dari empat puluhan dan nol satuan.",
                "display_text": "Kita lihat dulu, 40 terdiri dari 40-an dan 0 satuan.",
                "visual": "Menjelaskan nilai tempat bilangan 40 (4 puluhan dan 0 satuan)"
            },
            {
                "id": 3,
                "start": 7.28,
                "end": 13.78,
                "text": "Satuannya tidak bisa dikurangi tujuh, maka puluhannya kita pecah menjadi tiga puluhan dan sepuluh satuan.",
                "display_text": "Satuannya tidak bisa dikurangi 7, maka puluhannya kita pecah menjadi 30-an dan 10 satuan.",
                "visual": "Memecah 40 menjadi 30 dan 10 karena satuan 0 tidak bisa dikurangi 7"
            },
            {
                "id": 4,
                "start": 14.80,
                "end": 20.26,
                "text": "Nah puluhannya ada tiga, kita tulis tiga. Satuannya, sepuluh kurang tujuh adalah tiga.",
                "display_text": "Nah puluhannya ada 3, kita tulis 3. Satuannya, 10 kurang 7 adalah 3.",
                "visual": "Menuliskan puluhan 3 dan menghitung 10 - 7 = 3"
            },
            {
                "id": 5,
                "start": 20.70,
                "end": 24.54,
                "text": "Jadi di sini kita lihat, empat puluh kurang tujuh adalah tiga puluh tiga.",
                "display_text": "Jadi di sini kita lihat, 40 kurang 7 adalah 33.",
                "visual": "Menegaskan hasil akhir 40 - 7 = 33"
            }
        ]
    },
    {
        "id": "z4l3_3_pengurangan_belasan_1d",
        "source_filename": "zona 4 level 3-3.mp4",
        "so_dest_stem": "z4l3sb2bermain2_marcia",
        "so_game_name": "Rahasia Gua Gelap (z4l3-sb2bermain2)",
        "title": "Zona 4 Level 3.3: Pengurangan Belasan - 1D (12 - 3 = 9 & 15 - 9 = 6)",
        "subtitle": "Penjelasan pengurangan bilangan belasan dengan memecah puluhan menjadi 10 satuan dan menjumlahkan sisa.",
        "duration": 40.53,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 2.92,
                "text": "Bagaimana menghitung dua belas dikurang tiga?",
                "display_text": "Bagaimana menghitung 12 dikurang 3?",
                "visual": "Menulis soal 12 - 3 di papan"
            },
            {
                "id": 2,
                "start": 3.40,
                "end": 10.18,
                "text": "Di sini satuannya tidak bisa dikurangi, maka ini puluhannya kita pecah menjadi sepuluh satuan.",
                "display_text": "Di sini satuannya tidak bisa dikurangi, maka ini puluhannya kita pecah menjadi 10 satuan.",
                "visual": "Satuan 2 tidak bisa dikurangi 3, memecah 1 puluhan menjadi 10 satuan"
            },
            {
                "id": 3,
                "start": 10.76,
                "end": 17.00,
                "text": "Nah, sepuluh dikurang tiga adalah tujuh, tapi masih ada dua, jadi tujuh tambah dua adalah sembilan.",
                "display_text": "Nah, 10 dikurang 3 adalah 7, tapi masih ada 2, jadi 7 tambah 2 adalah 9.",
                "visual": "Menghitung 10 - 3 = 7, lalu 7 + 2 = 9"
            },
            {
                "id": 4,
                "start": 17.78,
                "end": 20.86,
                "text": "Dengan demikian, dua belas kurang tiga adalah sembilan.",
                "display_text": "Dengan demikian, 12 kurang 3 adalah 9.",
                "visual": "Menuliskan hasil 9 untuk soal 12 - 3"
            },
            {
                "id": 5,
                "start": 21.58,
                "end": 29.28,
                "text": "Lalu kalau lima belas kurang sembilan, lima dikurang sembilan tidak bisa, jadi puluhannya ini kita pecah menjadi sepuluh satuan.",
                "display_text": "Lalu kalau 15 kurang 9, 5 dikurang 9 tidak bisa, jadi puluhannya ini kita pecah menjadi 10 satuan.",
                "visual": "Menulis soal 15 - 9 dan memecah 1 puluhan menjadi 10 satuan"
            },
            {
                "id": 6,
                "start": 29.28,
                "end": 34.26,
                "text": "Nah, sepuluh dikurang sembilan adalah satu, tapi masih ada lima.",
                "display_text": "Nah, 10 dikurang 9 adalah 1, tapi masih ada 5.",
                "visual": "Menghitung 10 - 9 = 1, mengingatkan masih ada sisa 5 satuan"
            },
            {
                "id": 7,
                "start": 35.00,
                "end": 40.22,
                "text": "Jadi satu tambah lima adalah enam. Dengan demikian, lima belas dikurang sembilan adalah enam.",
                "display_text": "Jadi 1 tambah 5 adalah 6. Dengan demikian, 15 dikurang 9 adalah 6.",
                "visual": "Menghitung 1 + 5 = 6 dan menuliskan hasil akhir 15 - 9 = 6"
            }
        ]
    },
    {
        "id": "z4l3_4_pengurangan_2d_1d_meminjam",
        "source_filename": "zona 4 level 3-4.mp4",
        "so_dest_stem": "z4l3sb2bermain1_marcia",
        "so_game_name": "Memanah Guci Kerajaan (z4l3-sb2bermain1)",
        "title": "Zona 4 Level 3.4: Pengurangan 2D - 1D (41 - 5 = 36 Dua Cara)",
        "subtitle": "Penjelasan pengurangan 2 digit dengan 1 digit meminjam dengan dua cara: pasangan 10 dan membentuk 11 satuan.",
        "duration": 60.27,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.38,
                "text": "Sekarang kita hitung empat puluh satu kurang lima.",
                "display_text": "Sekarang kita hitung 41 kurang 5.",
                "visual": "Menuliskan soal 41 - 5 di papan"
            },
            {
                "id": 2,
                "start": 3.58,
                "end": 12.38,
                "text": "Di sini satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi tiga puluhan dan sepuluh satuan.",
                "display_text": "Di sini satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi 30-an dan 10 satuan.",
                "visual": "Cara 1: Memecah 41 menjadi 30-an dan 10 satuan"
            },
            {
                "id": 3,
                "start": 13.12,
                "end": 17.84,
                "text": "Nah kemudian, di sini kita lihat puluhannya ada tiga.",
                "display_text": "Nah kemudian, di sini kita lihat puluhannya ada 3.",
                "visual": "Menuliskan digit puluhan 3"
            },
            {
                "id": 4,
                "start": 18.18,
                "end": 26.56,
                "text": "Sedangkan satuan, sepuluh dikurang lima adalah lima, tapi ingat masih ada satu di sini, jadi hasilnya enam.",
                "display_text": "Sedangkan satuan, 10 dikurang 5 adalah 5, tapi ingat masih ada 1 di sini, jadi hasilnya 6.",
                "visual": "Menghitung 10 - 5 = 5, ditambah 1 satuan menjadi 6"
            },
            {
                "id": 5,
                "start": 26.56,
                "end": 30.90,
                "text": "Dengan demikian empat puluh satu kurang lima adalah tiga puluh enam.",
                "display_text": "Dengan demikian 41 kurang 5 adalah 36.",
                "visual": "Menegaskan hasil 41 - 5 = 36 pada cara pertama"
            },
            {
                "id": 6,
                "start": 31.46,
                "end": 33.32,
                "text": "Cara yang lain adalah sebagai berikut.",
                "display_text": "Cara yang lain adalah sebagai berikut.",
                "visual": "Beralih menjelaskan Cara 2"
            },
            {
                "id": 7,
                "start": 33.66,
                "end": 41.86,
                "text": "Di sini empat puluh satu kurang lima, empat puluh kita pecah menjadi tiga puluhan dan sepuluhan.",
                "display_text": "Di sini 41 kurang 5, 40-an kita pecah menjadi 30-an dan 10-an.",
                "visual": "Cara 2: Memecah 40 menjadi 30 dan 10"
            },
            {
                "id": 8,
                "start": 42.10,
                "end": 49.54,
                "text": "Lalu puluhannya di sini tiga, kemudian sepuluhan dan satu satuan membentuk sebelas satuan.",
                "display_text": "Lalu puluhannya di sini 3, kemudian 10-an dan 1 satuan membentuk 11 satuan.",
                "visual": "Menggabungkan 10 dan 1 menjadi 11 satuan, puluhan menjadi 3"
            },
            {
                "id": 9,
                "start": 49.54,
                "end": 56.84,
                "text": "Sebelas satuan itu dikurang lima adalah enam, jadi empat puluh satu kurang lima adalah tiga puluh enam.",
                "display_text": "11 satuan itu dikurang 5 adalah 6, jadi 41 kurang 5 adalah 36.",
                "visual": "Menghitung 11 - 5 = 6 dan menghasilkan 36"
            },
            {
                "id": 10,
                "start": 57.18,
                "end": 59.98,
                "text": "Terserah kalian mau pakai yang mana yang lebih disukai.",
                "display_text": "Terserah kalian mau pakai yang mana yang lebih disukai.",
                "visual": "Memberikan motivasi kebebasan memilih cara yang paling nyaman"
            }
        ]
    }
]

def format_bytes(num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} TB"

def get_audio_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def build_atempo_filter(factor: float) -> str:
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

async def synthesize_edge_segment(text: str, out_raw: str):
    import edge_tts
    comm = edge_tts.Communicate(text=text, voice="id-ID-GadisNeural", rate="+3%", pitch="+2Hz")
    await comm.save(out_raw)

def run_ffmpeg(cmd, desc=""):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg Gagal [{desc}]: {res.stderr[-400:]}")
        raise RuntimeError(f"FFmpeg error: {res.stderr[-400:]}")
    return res

async def process_single_video(cfg: dict, engine: F5IndoEngine, marcia_ref: str, marcia_ref_text: str):
    vid_id = cfg["id"]
    src_file = os.path.join(DATA_VIDEO_DIR, cfg["source_filename"])
    total_dur = cfg["duration"]
    segments = cfg["segments"]
    so_dest_stem = cfg["so_dest_stem"]
    
    print("\n" + "=" * 70)
    print(f"🎬 MEMPROSES (VERSI PERBAIKAN ARTIKULASI): {cfg['title']}")
    print(f"   Target SO Game: {cfg['so_game_name']} -> {so_dest_stem}")
    print(f"   Sumber Video  : {src_file} ({format_bytes(os.path.getsize(src_file))})")
    print(f"   Durasi Total  : {total_dur:.2f} detik | {len(segments)} Segmen Dialog")
    print("=" * 70)

    # 1. Project Directory
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

    # 3. F5-TTS Synthesis for each segment (using explicit spelled out text)
    import librosa
    import soundfile as sf
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"

    print(f"\n▶ Fase 1: Sintesis F5-TTS Trainer Marcia ({len(segments)} segmen ucapan fonetik lengkap)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]  # Ejaan kata bahasa Indonesia utuh (cth: "tujuh", "empat puluh", "dua belas")
        target_dur = s["end"] - s["start"]
        print(f"  [{sid}/{len(segments)}] F5-TTS: \"{text}\"...", end="", flush=True)
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

        # Time alignment & broadcast mastering
        tempo = trim_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        aligned_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_aligned.wav")
        run_ffmpeg([
            "ffmpeg", "-y", "-i", trim_f5,
            "-af", f"{atempo},{MASTER_FILTER}",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_f5
        ], f"Align F5 seg {sid}")

        s["audio_f5"] = f"/video-projects/{vid_id}/segments/f5_seg_{sid}_aligned.wav"
        print(f" Selesai ({time.time()-t0:.2f}s | aktif: {trim_dur:.2f}s -> target: {target_dur:.2f}s)")

    # 4. Edge-TTS Synthesis
    print(f"\n▶ Fase 2: Sintesis Edge-TTS Studio ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        raw_edge = os.path.join(segments_dir, f"edge_seg_{sid}_raw.mp3")
        aligned_edge = os.path.join(segments_dir, f"edge_seg_{sid}_aligned.wav")

        await synthesize_edge_segment(text, raw_edge)
        edge_dur = get_audio_duration(raw_edge)

        tempo = edge_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        run_ffmpeg([
            "ffmpeg", "-y", "-i", raw_edge,
            "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_edge
        ], f"Align Edge seg {sid}")

        s["audio_edge"] = f"/video-projects/{vid_id}/segments/edge_seg_{sid}_aligned.wav"

    # Purge VRAM
    engine.free_gpu_memory()

    # 5. Assemble Master Timelines
    print(f"\n▶ Fase 3: Merakit Master Timeline ({total_dur:.2f}s)...")
    silence_wav = os.path.join(segments_dir, "silence.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(total_dur),
        silence_wav
    ], "Generate silence")

    output_files = {}

    for mode in ["f5", "edge"]:
        master_wav = os.path.join(project_dir, f"master_dubbing_{mode}.wav")
        master_mp3 = os.path.join(project_dir, f"master_dubbing_{mode}.mp3")
        video_dubbed = os.path.join(project_dir, f"video_dubbed_marcia_{mode}.mp4")

        inputs = ["-i", silence_wav]
        delays = []
        for idx, s in enumerate(segments):
            seg_path = os.path.join(segments_dir, f"{mode}_seg_{s['id']}_aligned.wav")
            inputs.extend(["-i", seg_path])
            delay_ms = int(s["start"] * 1000)
            delays.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[d{idx+1}]")

        filter_parts = delays
        mix_inputs = "".join([f"[d{i+1}]" for i in range(len(segments))])
        total_in = len(segments) + 1
        filter_parts.append(f"[0:a]{mix_inputs}amix=inputs={total_in}:duration=first:dropout_transition=0,volume=3.0[outa]")
        filter_str = ";".join(filter_parts)

        # Mix master wav
        run_ffmpeg(["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_str, "-map", "[outa]", "-t", str(total_dur), master_wav], f"Mix {mode}")

        # Convert master mp3
        run_ffmpeg(["ffmpeg", "-y", "-i", master_wav, "-c:a", "libmp3lame", "-b:a", "256k", master_mp3], f"MP3 {mode}")

        # Mux to standard dubbed video
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", clip_orig,
            "-i", master_wav,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            video_dubbed
        ], f"Mux {mode} video")

        output_files[mode] = {
            "video": video_dubbed,
            "audio": master_mp3
        }

    # 6. Kompresi Video Ringan Berkualitas Tinggi ("Seperti Biasa")
    print(f"\n▶ Fase 4: Optimasi Ukuran File Ringan (H.264 Tune Animation & WebM VP9)...")
    dubbed_master_f5 = output_files["f5"]["video"]
    orig_size = os.path.getsize(src_file)

    # 6A. Lightweight MP4 (F5)
    f5_light_mp4 = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.mp4")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", dubbed_master_f5,
        "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10",
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-ar", "44100",
        "-movflags", "+faststart",
        f5_light_mp4
    ], "Encode F5 lightweight MP4")

    # 6B. Lightweight WebM (F5)
    f5_light_webm = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.webm")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", f5_light_mp4,
        "-c:v", "libvpx-vp9", "-crf", "35", "-b:v", "0",
        "-c:a", "libopus", "-b:a", "36k",
        f5_light_webm
    ], "Encode F5 lightweight WebM")

    f5_light_size = os.path.getsize(f5_light_mp4)
    webm_light_size = os.path.getsize(f5_light_webm)
    f5_light_pct = (1 - (f5_light_size / orig_size)) * 100

    print(f"  ✓ Ukuran Asli     : {format_bytes(orig_size)}")
    print(f"  ✓ MP4 Ringan (F5) : {format_bytes(f5_light_size)} (Hemat {f5_light_pct:.1f}%)")
    print(f"  ✓ WebM Ringan (F5): {format_bytes(webm_light_size)}")

    # 7A. Copy to Data VIdeo Marcia
    stem_name = Path(cfg["source_filename"]).stem
    data_light_target = os.path.join(DATA_VIDEO_DIR, f"{stem_name}_ringan.mp4")
    shutil.copyfile(f5_light_mp4, data_light_target)

    # 7B. Copy to Hasil/videoMarcia/z4_pengurangan
    hasil_light_mp4 = os.path.join(HASIL_Z4_DIR, f"{vid_id}_marcia_ringan.mp4")
    hasil_light_webm = os.path.join(HASIL_Z4_DIR, f"{vid_id}_marcia_ringan.webm")
    shutil.copyfile(f5_light_mp4, hasil_light_mp4)
    shutil.copyfile(f5_light_webm, hasil_light_webm)

    # 7C. AUTOMATIC INTEGRATION INTO SO PROJECT!
    so_mp4_target = os.path.join(SO_Z4L3_DIR, f"{so_dest_stem}.mp4")
    so_webm_target = os.path.join(SO_Z4L3_DIR, f"{so_dest_stem}.webm")
    shutil.copyfile(f5_light_mp4, so_mp4_target)
    shutil.copyfile(f5_light_webm, so_webm_target)
    print(f"  🚀 OTOMATIS DISINKRONKAN KE PROYEK SO:")
    print(f"     -> {so_mp4_target}")
    print(f"     -> {so_webm_target}")

    # 8. Save video_project_data.json
    meta = {
        "id": vid_id,
        "title": cfg["title"],
        "subtitle": cfg["subtitle"],
        "so_game_name": cfg["so_game_name"],
        "so_dest_stem": so_dest_stem,
        "duration_seconds": round(total_dur, 2),
        "source_type": "local_mp4",
        "original_file": cfg["source_filename"],
        "original_size_bytes": orig_size,
        "compressed_mp4_bytes": f5_light_size,
        "compressed_webm_bytes": webm_light_size,
        "compression_savings_percent": round(f5_light_pct, 1),
        "original_speaker": "Prof. Yohanes Surya (Pria)",
        "dubbed_character": "Guru Marcia (Trainer Marcia Asli)",
        "voice_id": "so_marcia",
        "acceleration": "F5-TTS nfe_step=32 High-Fidelity + Spelled Out Numbers",
        "noise_filtering": "Highpass 80Hz + Loudnorm broadcast -16 LUFS",
        "files": {
            "original_video": f"/video-projects/{vid_id}/clip_original.mp4",
            "dubbed_video_f5": f"/video-projects/{vid_id}/video_dubbed_marcia_f5.mp4",
            "dubbed_video_edge": f"/video-projects/{vid_id}/video_dubbed_marcia_edge.mp4",
            "dubbed_video_f5_ringan": f"/video-projects/{vid_id}/video_dubbed_marcia_f5_ringan.mp4",
            "dubbed_audio_f5": f"/video-projects/{vid_id}/master_dubbing_f5.mp3",
            "dubbed_audio_edge": f"/video-projects/{vid_id}/master_dubbing_edge.mp3"
        },
        "so_files": {
            "mp4": f"/assets/videos/z4l3/{so_dest_stem}.mp4",
            "webm": f"/assets/videos/z4l3/{so_dest_stem}.webm"
        },
        "segments": segments
    }

    meta_file = os.path.join(project_dir, "video_project_data.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Metadata Studio Tersimpan: {meta_file}")

    return {
        "id": vid_id,
        "title": cfg["title"],
        "filename": cfg["source_filename"],
        "so_game_name": cfg["so_game_name"],
        "duration": total_dur,
        "original_size": orig_size,
        "light_mp4_size": f5_light_size,
        "light_webm_size": webm_light_size,
        "savings_pct": f5_light_pct,
        "so_mp4_target": so_mp4_target,
        "so_webm_target": so_webm_target
    }

async def main():
    print("=" * 80)
    print("  SPRINT VIDEO DUBBING MARCIA PERBAIKAN ARTIKULASI ANGKA & SYNC PROYEK SO")
    print("  Membaca Angka Fonetik Sempurna ('tujuh', 'empat puluh', 'dua belas', dsb)")
    print("=" * 80)

    # Inisialisasi F5 Engine
    print("\n▶ Menginisialisasi F5-TTS Engine (High-Fidelity nfe_step=32)...")
    engine = F5IndoEngine.get_instance()
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."

    results = []
    total_start = time.time()

    for idx, cfg in enumerate(VIDEOS_CONFIG, 1):
        print(f"\n==================== VIDEO {idx} / {len(VIDEOS_CONFIG)} ====================")
        res = await process_single_video(cfg, engine, marcia_ref, marcia_ref_text)
        results.append(res)

    total_time = time.time() - total_start
    total_orig = sum(r["original_size"] for r in results)
    total_light = sum(r["light_mp4_size"] for r in results)
    total_savings = (1 - (total_light / total_orig)) * 100 if total_orig > 0 else 0

    print("\n" + "=" * 80)
    print("🎉 SELURUH 4 VIDEO BERHASIL DIPERBAIKI DAN DIMASUKKAN KE PROYEK SO!")
    print(f"Total Waktu Eksekusi : {total_time:.1f} detik ({total_time/60:.1f} menit)")
    print(f"Total Ukuran Asli    : {format_bytes(total_orig)}")
    print(f"Total Ukuran Ringan  : {format_bytes(total_light)}")
    print(f"Total Penghematan    : {total_savings:.1f}% LEBIH KECIL!")
    print("=" * 80)

    print("\n📋 Integrasi Proyek SO (/assets/videos/z4l3/):")
    for r in results:
        print(f"  • {r['title']}")
        print(f"    - Game SO       : {r['so_game_name']}")
        print(f"    - Berkas MP4 SO : {r['so_mp4_target']} ({format_bytes(r['light_mp4_size'])})")
        print(f"    - Berkas WebM SO: {r['so_webm_target']} ({format_bytes(r['light_webm_size'])})")

if __name__ == "__main__":
    asyncio.run(main())
