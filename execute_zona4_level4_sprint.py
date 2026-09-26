#!/usr/bin/env python3
"""
execute_zona4_level4_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk 3 Video Zona 4 Level 4:
1. zona 4 level 4-1.mp4 (78 - 46 = 32, Pengurangan 2D - 2D Tanpa Meminjam)
2. zona 4 level 4-2.mp4 (80 - 34 = 46, Puluhan Murni - 2D, Cara Biasa & Mencongak)
3. zona 4 level 4-3.mp4 (82 - 49 = 33, Pengurangan 2D - 2D Meminjam Tiga Cara)

Standar Mutu:
- Angka diekspansi 100% fonetik bahasa Indonesia utuh (cth: "tujuh puluh delapan", "delapan puluh", "tiga puluh tiga", dsb)
- Suara Karakter: Trainer Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2, nfe=32, speed=1.05)
- Alternatif Nol-Noise: Edge-TTS Studio (id-ID-GadisNeural)
- Broadcast DSP Mastering: highpass 80Hz + loudnorm -16 LUFS (meniadakan noise/rumble, vokal jernih)
- Kompresi Video Ringan: H.264 tune animation CRF 28, AAC 48k Mono, FastStart + WebM VP9/Opus
- Sinkronisasi Otomatis ke:
  1. Data VIdeo Marcia/ (*_ringan.mp4)
  2. Hasil/videoMarcia/z4_pengurangan/
  3. Proyek SO: /Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l4/
  4. Web Studio UI: video_projects/ (/Proyek Video)
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
SO_Z4L4_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l4"

os.makedirs(HASIL_Z4_DIR, exist_ok=True)
os.makedirs(SO_Z4L4_DIR, exist_ok=True)

VIDEOS_CONFIG = [
    {
        "id": "z4l4_1_pengurangan_2d_2d_tanpa_meminjam",
        "source_filename": "zona 4 level 4-1.mp4",
        "so_dest_stem": "z4l4sb1bermain1_marcia",
        "so_game_name": "Bowling Menara Qutub (z4l4-sb1bermain1)",
        "title": "Zona 4 Level 4.1: Pengurangan 2D - 2D Tanpa Meminjam (78 - 46 = 32)",
        "subtitle": "Pengurangan langsung puluhan dikurang puluhan dan satuan dikurang satuan karena satuan bisa langsung dikurangi.",
        "duration": 28.67,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.00,
                "text": "Berapa tujuh puluh delapan dikurang empat puluh enam?",
                "display_text": "Berapa 78 dikurang 46?",
                "visual": "Menuliskan soal 78 - 46 di papan tulis"
            },
            {
                "id": 2,
                "start": 3.76,
                "end": 7.00,
                "text": "Di sini kita lihat bahwa satuannya bisa dikurangi.",
                "display_text": "Di sini kita lihat bahwa satuannya bisa dikurangi.",
                "visual": "Menunjuk digit satuan 8 dan 6"
            },
            {
                "id": 3,
                "start": 7.98,
                "end": 13.18,
                "text": "Karena itu kita langsung, puluhan dikurang puluhan, satuan dikurang satuan.",
                "display_text": "Karena itu kita langsung puluhan dikurang puluhan, satuan kurang satuan.",
                "visual": "Menjelaskan konsep pengurangan langsung puluhan dan satuan"
            },
            {
                "id": 4,
                "start": 13.74,
                "end": 18.04,
                "text": "Puluhan dikurang puluhan, tujuh dikurang empat adalah tiga.",
                "display_text": "Puluhan dikurang puluhan, 7 dikurang 4 adalah 3.",
                "visual": "Menghitung 7 - 4 = 3 pada puluhan"
            },
            {
                "id": 5,
                "start": 18.86,
                "end": 23.10,
                "text": "Satuan dikurang satuan, delapan kurang enam adalah dua.",
                "display_text": "Satuan dikurang satuan, 8 kurang 6 adalah 2.",
                "visual": "Menghitung 8 - 6 = 2 pada satuan"
            },
            {
                "id": 6,
                "start": 23.50,
                "end": 27.50,
                "text": "Jadi tujuh puluh delapan dikurang empat puluh enam adalah tiga puluh dua.",
                "display_text": "Jadi 78 dikurang 46 adalah 32.",
                "visual": "Menuliskan hasil akhir 32"
            }
        ]
    },
    {
        "id": "z4l4_2_pengurangan_puluhan_murni_2d",
        "source_filename": "zona 4 level 4-2.mp4",
        "so_dest_stem": "z4l4sb1bermain2_marcia",
        "so_game_name": "Tantangan Menara Qutub (z4l4-sb1bermain2)",
        "title": "Zona 4 Level 4.2: Pengurangan Puluhan Murni - 2D (80 - 34 = 46)",
        "subtitle": "Pengurangan bilangan puluhan murni dengan 2 digit menggunakan cara pecah puluhan dan teknik mencongak pasangan 10.",
        "duration": 70.37,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 2.90,
                "text": "Berapa delapan puluh dikurang tiga puluh empat?",
                "display_text": "Berapa 80 dikurang 34?",
                "visual": "Menuliskan soal 80 - 34 di papan"
            },
            {
                "id": 2,
                "start": 3.62,
                "end": 7.00,
                "text": "Di sini kita lihat satuannya tidak bisa dikurangi.",
                "display_text": "Di sini kita lihat satuannya tidak bisa dikurangi.",
                "visual": "Menunjuk satuan 0 tidak bisa dikurangi 4"
            },
            {
                "id": 3,
                "start": 7.90,
                "end": 13.90,
                "text": "Itu sebabnya delapannya kita pecah menjadi tujuh puluhan dan sepuluh satuan.",
                "display_text": "Itu sebabnya 8-nya kita pecah menjadi 7 puluhan dan 10 satuan.",
                "visual": "Memecah 80 menjadi 70 dan 10"
            },
            {
                "id": 4,
                "start": 14.46,
                "end": 20.90,
                "text": "Nah, di sini kita lihat bahwa puluhannya, tujuh dikurang tiga adalah empat.",
                "display_text": "Nah, di sini kita lihat bahwa puluhannya 7 dikurang 3 adalah 4.",
                "visual": "Menghitung 7 - 3 = 4 pada puluhan"
            },
            {
                "id": 5,
                "start": 21.16,
                "end": 25.94,
                "text": "Sedangkan satuannya, sepuluh dikurang empat, yaitu enam.",
                "display_text": "Sedangkan satuannya 10 dikurang 4, yaitu 6.",
                "visual": "Menghitung 10 - 4 = 6 pada satuan"
            },
            {
                "id": 6,
                "start": 25.94,
                "end": 30.12,
                "text": "Jadi delapan puluh dikurang tiga puluh empat adalah empat puluh enam.",
                "display_text": "Jadi 80 dikurang 34 adalah 46.",
                "visual": "Menuliskan hasil akhir 46"
            },
            {
                "id": 7,
                "start": 30.78,
                "end": 32.84,
                "text": "Nah, bagaimana dengan cara mencongak?",
                "display_text": "Nah, bagaimana dengan cara mencongak?",
                "visual": "Beralih ke teknik mencongak cepat"
            },
            {
                "id": 8,
                "start": 33.08,
                "end": 37.98,
                "text": "Di sini kita lihat puluhannya, delapan dikurang tiga adalah lima.",
                "display_text": "Di sini kita lihat puluhannya 8 dikurang 3 adalah 5.",
                "visual": "Menghitung puluhan 8 - 3 = 5"
            },
            {
                "id": 9,
                "start": 38.66,
                "end": 43.06,
                "text": "Kita lirik kanan. Lirik kanan, nol dikurang empat tidak bisa.",
                "display_text": "Kita lirik kanan. Lirik kanan 0 dikurang 4 tidak bisa.",
                "visual": "Melakukan lirik kanan ke digit satuan"
            },
            {
                "id": 10,
                "start": 43.26,
                "end": 48.46,
                "text": "Karena itu kita kurangi satu. Lima kurang satu adalah empat, sehingga puluhannya jadi empat.",
                "display_text": "Karena itu kita kurangi 1. 5 kurang 1 adalah 4, sehingga puluhannya jadi 4.",
                "visual": "Mengurangi puluhan dengan 1 menjadi 4"
            },
            {
                "id": 11,
                "start": 48.92,
                "end": 50.32,
                "text": "Nah, berikutnya untuk satuan.",
                "display_text": "Nah, berikutnya untuk satuan.",
                "visual": "Beralih menghitung digit satuan"
            },
            {
                "id": 12,
                "start": 50.42,
                "end": 54.56,
                "text": "Kalau cara mencongak adalah nol ditambah pasangan empat.",
                "display_text": "Kalau cara mencongak adalah 0 ditambah pasangan 4.",
                "visual": "Menjelaskan konsep pasangan 10 dari 4"
            },
            {
                "id": 13,
                "start": 54.56,
                "end": 59.72,
                "text": "Pasangan empat adalah enam. Sehingga nol tambah enam adalah enam.",
                "display_text": "Pasangan 4 adalah 6. Sehingga 0 tambah 6 adalah 6.",
                "visual": "Menghitung 0 + 6 = 6"
            },
            {
                "id": 14,
                "start": 59.96,
                "end": 61.48,
                "text": "Jadi hasilnya empat puluh enam.",
                "display_text": "Jadi hasilnya 46.",
                "visual": "Menegaskan hasil 46"
            },
            {
                "id": 15,
                "start": 62.42,
                "end": 64.70,
                "text": "Nah, pertanyaannya dari mana pasangan empat itu?",
                "display_text": "Nah, pertanyaannya dari mana pasangan 4 itu?",
                "visual": "Mengajukan pertanyaan asal-usul pasangan 4"
            },
            {
                "id": 16,
                "start": 64.72,
                "end": 69.58,
                "text": "Pasangan empat itu dari sepuluh dikurang empat, yaitu enam.",
                "display_text": "Pasangan 4 itu dari 10 dikurang 4, yaitu 6.",
                "visual": "Menjelaskan 10 - 4 = 6"
            }
        ]
    },
    {
        "id": "z4l4_3_pengurangan_2d_2d_meminjam",
        "source_filename": "zona 4 level 4-3.mp4",
        "so_dest_stem": "z4l4sb2bermain1_marcia",
        "so_game_name": "Memanah Labu Qutub Minar (z4l4-sb2bermain1)",
        "title": "Zona 4 Level 4.3: Pengurangan 2D - 2D Meminjam (82 - 49 = 33 Tiga Cara)",
        "subtitle": "Pengurangan 2 digit meminjam dengan tiga cara: pecah 7 dan 10, pecah puluhan membentuk 12, dan mencongak pasangan 10.",
        "duration": 92.33,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.70,
                "text": "Berikutnya kita hitung delapan puluh dua dikurang empat puluh sembilan.",
                "display_text": "Berikutnya kita hitung 82 dikurang 49.",
                "visual": "Menuliskan soal 82 - 49"
            },
            {
                "id": 2,
                "start": 4.56,
                "end": 12.86,
                "text": "Kita lihat di sini, satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi tujuh dan sepuluh.",
                "display_text": "Kita lihat di sini, satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi 7 dan 10.",
                "visual": "Cara 1: Memecah puluhan 80 menjadi 70 dan 10"
            },
            {
                "id": 3,
                "start": 13.40,
                "end": 19.16,
                "text": "Nah kemudian kita kurangi, tujuh dikurang empat, puluhannya ada tiga.",
                "display_text": "Nah kemudian kita kurangi, 7 dikurang 4 puluhannya ada 3.",
                "visual": "Menghitung puluhan 7 - 4 = 3"
            },
            {
                "id": 4,
                "start": 19.58,
                "end": 24.54,
                "text": "Lalu satuannya, sepuluh kurang sembilan adalah satu, tapi ingat masih ada dua.",
                "display_text": "Lalu satuannya 10 kurang 9 adalah 1, tapi ingat masih ada 2.",
                "visual": "Menghitung 10 - 9 = 1 dan mengingat sisa 2 satuan"
            },
            {
                "id": 5,
                "start": 24.54,
                "end": 31.34,
                "text": "Jadi satu tambah dua adalah tiga. Hasilnya delapan puluh dua kurang empat puluh sembilan adalah tiga puluh tiga.",
                "display_text": "Jadi 1 tambah 2 adalah 3. Hasilnya 82 kurang 49 adalah 33.",
                "visual": "Menghitung 1 + 2 = 3 dan menulis hasil akhir 33"
            },
            {
                "id": 6,
                "start": 32.30,
                "end": 36.44,
                "text": "Cara lain adalah sebagai berikut, di sini delapan puluh dua kurang empat puluh sembilan.",
                "display_text": "Cara lain adalah sebagai berikut, di sini 82 kurang 49.",
                "visual": "Beralih ke Cara 2"
            },
            {
                "id": 7,
                "start": 37.34,
                "end": 44.84,
                "text": "Satuannya tidak bisa dikurangi, sehingga puluhannya kita pecah menjadi tujuh puluhan dan satu puluhan.",
                "display_text": "Satuannya tidak bisa dikurangi, sehingga puluhannya kita pecah menjadi 7 puluhan dan 1 puluhan.",
                "visual": "Memecah 80 menjadi 7 puluhan dan 1 puluhan"
            },
            {
                "id": 8,
                "start": 45.54,
                "end": 50.80,
                "text": "Nah kemudian di sini puluhannya kita kurangi, tujuh kurang empat adalah tiga.",
                "display_text": "Nah kemudian di sini puluhannya kita kurangi, 7 kurang 4 adalah 3.",
                "visual": "Menghitung puluhan 7 - 4 = 3"
            },
            {
                "id": 9,
                "start": 50.80,
                "end": 55.94,
                "text": "Lalu puluhannya ini akan bergabung dengan satuan menjadi dua belas.",
                "display_text": "Lalu puluhannya ini akan bergabung dengan satuan menjadi 12.",
                "visual": "Menggabungkan 1 puluhan dan 2 satuan menjadi 12"
            },
            {
                "id": 10,
                "start": 56.32,
                "end": 59.10,
                "text": "Dua belas dikurang sembilan adalah tiga.",
                "display_text": "12 dikurang 9 adalah 3.",
                "visual": "Menghitung 12 - 9 = 3"
            },
            {
                "id": 11,
                "start": 59.56,
                "end": 62.38,
                "text": "Jadi delapan puluh dua dikurang empat puluh sembilan adalah tiga puluh tiga.",
                "display_text": "Jadi 82 dikurang 49 adalah 33.",
                "visual": "Menulis hasil 33 pada Cara 2"
            },
            {
                "id": 12,
                "start": 63.34,
                "end": 65.90,
                "text": "Nah, berikutnya adalah cara mencongak, cara cepatnya.",
                "display_text": "Nah berikutnya adalah cara mencongak, cara cepatnya.",
                "visual": "Beralih ke Cara 3: Mencongak"
            },
            {
                "id": 13,
                "start": 66.26,
                "end": 71.80,
                "text": "Delapan puluh dua dikurang empat puluh sembilan. Di sini kita lihat delapan dikurang empat adalah empat.",
                "display_text": "82 dikurang 49, di sini kita lihat 8 dikurang 4 adalah 4.",
                "visual": "Menghitung puluhan 8 - 4 = 4"
            },
            {
                "id": 14,
                "start": 72.76,
                "end": 77.80,
                "text": "Lirik kanan, satuannya tidak bisa dikurangi, maka kita kurangi satu menjadi tiga.",
                "display_text": "Lirik kanan, satuannya tidak bisa dikurangi, maka kita kurangi 1 menjadi 3.",
                "visual": "Melakukan lirik kanan dan mengurangkan 1"
            },
            {
                "id": 15,
                "start": 77.80,
                "end": 83.80,
                "text": "Lalu dua ditambah pasangan sembilan. Pasangan sembilan adalah satu, dua tambah satu adalah tiga.",
                "display_text": "Lalu 2 ditambah pasangan 9. Pasangan 9 adalah 1, 2 tambah 1 adalah 3.",
                "visual": "Menghitung 2 + 1 = 3 menggunakan pasangan 9"
            },
            {
                "id": 16,
                "start": 84.50,
                "end": 85.94,
                "text": "Jadi hasilnya tiga puluh tiga.",
                "display_text": "Jadi hasilnya 33.",
                "visual": "Menegaskan hasil 33"
            },
            {
                "id": 17,
                "start": 86.70,
                "end": 91.64,
                "text": "Dari mana itu pasangan sembilan? Dari sepuluh kurang sembilan.",
                "display_text": "Dari mana itu pasangan 9? Dari 10 kurang 9.",
                "visual": "Menjelaskan asal pasangan 9 adalah 10 - 9"
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
    print(f"🎬 MEMPROSES ZONA 4 LEVEL 4: {cfg['title']}")
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
        text = s["text"]  # Ejaan kata bahasa Indonesia utuh
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
    so_mp4_target = os.path.join(SO_Z4L4_DIR, f"{so_dest_stem}.mp4")
    so_webm_target = os.path.join(SO_Z4L4_DIR, f"{so_dest_stem}.webm")
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
            "mp4": f"/assets/videos/z4l4/{so_dest_stem}.mp4",
            "webm": f"/assets/videos/z4l4/{so_dest_stem}.webm"
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
    print("  SPRINT VIDEO DUBBING MARCIA ZONA 4 LEVEL 4 (3 VIDEO) & SYNC SO")
    print("  Pelafalan Angka Fonetik Sempurna, Noise-Free, & Kompresi Ringan Prima")
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
    print("🎉 SELURUH 3 VIDEO ZONA 4 LEVEL 4 BERHASIL DIDUBBING, DIKOMPRESI, DAN DIMASUKKAN KE SO!")
    print(f"Total Waktu Eksekusi : {total_time:.1f} detik ({total_time/60:.1f} menit)")
    print(f"Total Ukuran Asli    : {format_bytes(total_orig)}")
    print(f"Total Ukuran Ringan  : {format_bytes(total_light)}")
    print(f"Total Penghematan    : {total_savings:.1f}% LEBIH KECIL!")
    print("=" * 80)

    print("\n📋 Integrasi Proyek SO (/assets/videos/z4l4/):")
    for r in results:
        print(f"  • {r['title']}")
        print(f"    - Game SO       : {r['so_game_name']}")
        print(f"    - Berkas MP4 SO : {r['so_mp4_target']} ({format_bytes(r['light_mp4_size'])})")
        print(f"    - Berkas WebM SO: {r['so_webm_target']} ({format_bytes(r['light_webm_size'])})")

if __name__ == "__main__":
    asyncio.run(main())
