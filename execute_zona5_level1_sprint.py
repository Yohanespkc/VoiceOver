#!/usr/bin/env python3
"""
execute_zona5_level1_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk 3 Video Zona 5 Level 1 (Pembagian Dasar):
1. zona 5 level 1a.mp4 (64.50s) -> Pembagian Konkret & Mencongak (8 : 2 = 4)
2. zona 5 level 1b.mp4 (14.00s) -> Mencongak Pembagian (54 : 6 = 9)
3. zona 5 level 1c.mp4 (77.00s) -> Pembagian Mencari Banyaknya Kotak (18 : [ ] = 6)

Standar Kualitas & Perbaikan Tampilan:
1. Suara Karakter: Guru Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2) + Edge-TTS Studio (id-ID-GadisNeural).
2. Artikulasi Fonetik Penuh: Semua angka dieja 100% lengkap tanpa salah sebut ("delapan", "dua", "empat", "lima puluh empat", "enam", "sembilan", "delapan belas", "tiga", "dua belas", dsb).
3. Zero Audio Truncation: Segmen terakhir ("kotak itu", "mudah sekali", "sembilan") diberi durasi alami dan tanpa pemotongan -t sehingga tidak terpotong satu suku kata pun.
4. Freeze Frame Akhir (2.6 - 3.5s): Menggunakan tpad=stop_mode=clone untuk menahan frame papan tulis lengkap sehingga video tidak berakhir mendadak.
5. Canvas Widescreen 16:9 Murni Putih (#FFFFFF): Filter scale=928:696,pad=1280:720:176:0:color=white menghilangkan seluruh garis/border hitam di semua sisi serta memberikan margin bawah ~109px agar kontrol player tidak menutupi tulisan ("banyak kotak", "Isi tiap kotak").
6. Kompresi Ringan Web-Ready: H.264 tune animation CRF 28 & WebM VP9 CRF 35 (FastStart streaming).
7. Master WAV Standard: -ar 44100 pcm_s16le.
8. Distribusi Otomatis ke:
   - Data VIdeo Marcia/ (*_ringan.mp4)
   - Hasil/videoMarcia/z5_pembagian/
   - Proyek SO: so/web/public/assets/videos/z5l1/
   - Web Studio: video_projects/ (/Proyek Video)
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

DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
VIDEO_PROJECTS_DIR = os.path.join(BASE_DIR, "video_projects")
HASIL_Z5_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z5_pembagian")
SO_Z5L1_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z5l1"

os.makedirs(HASIL_Z5_DIR, exist_ok=True)
os.makedirs(SO_Z5L1_DIR, exist_ok=True)

VIDEOS_CONFIG = [
    {
        "id": "z5l1a_pembagian_konkret_8_bagi_2",
        "source_filename": "zona 5 level 1a.mp4",
        "data_ringan_name": "zona 5 level 1a_ringan.mp4",
        "hasil_stem": "z5l1a_pembagian_konkret_8_bagi_2_marcia",
        "so_dest_stem": "z5l1a_pembagian_8_bagi_2_marcia",
        "title": "Zona 5 Level 1a: Pembagian Konkret & Mencongak (8 : 2 = 4)",
        "subtitle": "Konsep dasar pembagian konkret memasukkan 8 benda ke dalam 2 kotak dan mencongak 2 x berapa = 8.",
        "duration": 64.50,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.40,
                "text": "Bagaimana menghitung delapan dibagi dua?",
                "display_text": "Bagaimana menghitung 8 dibagi 2?",
                "visual": "Menampilkan soal 8 dibagi 2 dan dua kotak kosong"
            },
            {
                "id": 2,
                "start": 3.80,
                "end": 6.00,
                "text": "Kita lihat dulu konkretnya.",
                "display_text": "Kita lihat dulu konkretnya.",
                "visual": "Menunjuk deretan 8 benda konkret di atas kotak"
            },
            {
                "id": 3,
                "start": 6.20,
                "end": 10.40,
                "text": "Di sini ada delapan benda hendak dimasukkan ke dalam dua kotak.",
                "display_text": "Di sini ada 8 benda hendak dimasukkan ke dalam 2 kotak.",
                "visual": "Menghitung 8 benda dan menunjuk ke 2 kotak"
            },
            {
                "id": 4,
                "start": 10.70,
                "end": 15.00,
                "text": "Masing-masing kotak akan menerima berapa benda supaya adil.",
                "display_text": "Masing-masing kotak akan menerima berapa benda supaya adil.",
                "visual": "Menekankan pembagian adil pada kedua kotak"
            },
            {
                "id": 5,
                "start": 15.20,
                "end": 23.70,
                "text": "Jadi kalau kita lihat, ini kita masukkan ke sini, ini kita masukkan ke sini, ini kita masukkan ke sini, dan seterusnya.",
                "display_text": "Jadi kalau kita lihat, ini kita masukkan ke sini, ini kita masukkan ke sini, ini kita masukkan ke sini, dan seterusnya.",
                "visual": "Benda-benda berpindah satu demi satu masuk ke kotak kiri dan kanan bergantian"
            },
            {
                "id": 6,
                "start": 23.70,
                "end": 30.70,
                "text": "Dan ini yang terakhir di sini, kita lihat bahwa tiap kotak menerima empat benda.",
                "display_text": "Dan ini yang terakhir di sini, kita lihat bahwa tiap kotak menerima 4 benda.",
                "visual": "Benda terakhir masuk ke kotak dan masing-masing kotak berisi 4 benda"
            },
            {
                "id": 7,
                "start": 31.00,
                "end": 33.50,
                "text": "Jadi delapan dibagi dua adalah empat.",
                "display_text": "Jadi 8 dibagi 2 adalah 4.",
                "visual": "Menulis hasil 8 : 2 = 4"
            },
            {
                "id": 8,
                "start": 33.70,
                "end": 41.20,
                "text": "Untuk mencongak, delapan dibagi dua sama dengan berapa, itu sama saja dengan menanyakan dua kali berapa sama dengan delapan.",
                "display_text": "Untuk mencongak, 8 dibagi 2 sama dengan berapa, itu sama saja dengan menanyakan 2 kali berapa sama dengan 8.",
                "visual": "Menulis relasi mencongak 2 x [ ] = 8 di bawah soal pembagian"
            },
            {
                "id": 9,
                "start": 41.50,
                "end": 48.80,
                "text": "Karena di sini ada dua kotak, berapa isi tiap kotak supaya total benda ada delapan.",
                "display_text": "Karena di sini ada 2 kotak, berapa isi tiap kotak supaya total benda ada 8.",
                "visual": "Mengaitkan 2 kotak dan isi per kotak dengan total 8 benda"
            },
            {
                "id": 10,
                "start": 49.00,
                "end": 56.00,
                "text": "Jadi di sini kita mengubah pembagian ini menjadi soal perkalian.",
                "display_text": "Jadi di sini kita mengubah pembagian ini menjadi soal perkalian.",
                "visual": "Menegaskan transformasi pembagian ke perkalian"
            },
            {
                "id": 11,
                "start": 57.00,
                "end": 61.20,
                "text": "Bagi anak yang sudah belajar perkalian, tentu ini sangat mudah sekali.",
                "display_text": "Bagi anak yang sudah belajar perkalian, tentu ini sangat mudah sekali.",
                "visual": "Kesimpulan bahwa pembagian terasa mudah setelah menguasai perkalian"
            }
        ]
    },
    {
        "id": "z5l1b_mencongak_54_bagi_6",
        "source_filename": "zona 5 level 1b.mp4",
        "data_ringan_name": "zona 5 level 1b_ringan.mp4",
        "hasil_stem": "z5l1b_mencongak_54_bagi_6_marcia",
        "so_dest_stem": "z5l1b_mencongak_54_bagi_6_marcia",
        "title": "Zona 5 Level 1b: Mencongak Pembagian (54 : 6 = 9)",
        "subtitle": "Menghitung 54 dibagi 6 dengan mencongak perkalian 6 x berapa sama dengan 54.",
        "duration": 14.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 2.40,
                "text": "Berapa lima puluh empat dibagi enam?",
                "display_text": "Berapa 54 dibagi 6?",
                "visual": "Menuliskan soal 54 dibagi 6 sama dengan titik-titik"
            },
            {
                "id": 2,
                "start": 2.60,
                "end": 7.80,
                "text": "Ini sama saja dengan menanyakan enam kali berapa sama dengan lima puluh empat.",
                "display_text": "Ini sama saja dengan menanyakan 6 kali berapa sama dengan 54.",
                "visual": "Menuliskan relasi perkalian 6 x [ ] = 54"
            },
            {
                "id": 3,
                "start": 8.50,
                "end": 11.20,
                "text": "Jawabnya adalah sembilan.",
                "display_text": "Jawabnya adalah 9.",
                "visual": "Menuliskan jawaban angka 9 di kotak jawaban"
            }
        ]
    },
    {
        "id": "z5l1c_mencari_kotak_18_bagi_berapa",
        "source_filename": "zona 5 level 1c.mp4",
        "data_ringan_name": "zona 5 level 1c_ringan.mp4",
        "hasil_stem": "z5l1c_mencari_kotak_18_bagi_berapa_marcia",
        "so_dest_stem": "z5l1c_mencari_kotak_18_bagi_berapa_marcia",
        "title": "Zona 5 Level 1c: Pembagian Mencari Banyaknya Kotak (18 : [ ] = 6)",
        "subtitle": "Pembagian 18 benda dengan isi tiap kotak 6 benda untuk mencari banyaknya kotak yang dibutuhkan.",
        "duration": 77.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.00,
                "text": "Delapan belas dibagi berapa sama dengan enam.",
                "display_text": "18 dibagi berapa sama dengan 6.",
                "visual": "Menuliskan soal 18 : [ ] = 6"
            },
            {
                "id": 2,
                "start": 3.30,
                "end": 6.70,
                "text": "Ini sama saja dengan menanyakan ada delapan belas benda,",
                "display_text": "Ini sama saja dengan menanyakan ada 18 benda,",
                "visual": "Menunjuk 18 lingkaran benda di papan"
            },
            {
                "id": 3,
                "start": 6.90,
                "end": 12.20,
                "text": "hendak dimasukkan ke dalam berapa kotak agar tiap kotak menerima enam benda.",
                "display_text": "hendak dimasukkan ke dalam berapa kotak agar tiap kotak menerima 6 benda.",
                "visual": "Menguraikan pertanyaan mencari banyaknya kotak jika tiap kotak berisi 6"
            },
            {
                "id": 4,
                "start": 12.60,
                "end": 15.80,
                "text": "Pertama kita isi dulu kotak pertama dengan enam benda.",
                "display_text": "Pertama kita isi dulu kotak pertama dengan 6 benda.",
                "visual": "Enam benda pertama dimasukkan ke kotak 1"
            },
            {
                "id": 5,
                "start": 16.00,
                "end": 20.80,
                "text": "Kemudian kotak kedua kita isi dengan enam benda, sudah dua belas.",
                "display_text": "Kemudian kotak kedua kita isi dengan 6 benda, sudah 12.",
                "visual": "Enam benda berikutnya dimasukkan ke kotak 2, terhitung 12 benda"
            },
            {
                "id": 6,
                "start": 21.30,
                "end": 24.40,
                "text": "Berikutnya kita isi lagi dengan enam benda.",
                "display_text": "Berikutnya kita isi lagi dengan 6 benda.",
                "visual": "Enam benda terakhir dimasukkan ke kotak 3"
            },
            {
                "id": 7,
                "start": 24.50,
                "end": 26.80,
                "text": "Ternyata sekarang totalnya sudah delapan belas.",
                "display_text": "Ternyata sekarang totalnya sudah 18.",
                "visual": "Semua 18 benda telah habis terbagi ke dalam kotak"
            },
            {
                "id": 8,
                "start": 26.80,
                "end": 34.80,
                "text": "Jadi di sini dibutuhkan tiga kotak. Jadi jawabnya delapan belas dibagi tiga sama dengan enam.",
                "display_text": "Jadi di sini dibutuhkan 3 kotak. Jadi jawabnya 18 dibagi 3 sama dengan 6.",
                "visual": "Menulis angka 3 di dalam kotak titik-titik (18 : 3 = 6)"
            },
            {
                "id": 9,
                "start": 35.20,
                "end": 42.80,
                "text": "Nah, sekarang untuk mencongak, pertanyaan yang relevan dengan delapan belas dibagi berapa sama dengan enam,",
                "display_text": "Nah, sekarang untuk mencongak, pertanyaan yang relevan dengan 18 dibagi berapa sama dengan 6,",
                "visual": "Menuliskan relasi mencongak di bawah soal pembagian"
            },
            {
                "id": 10,
                "start": 42.80,
                "end": 48.80,
                "text": "adalah berapa dikali enam sama dengan delapan belas.",
                "display_text": "adalah berapa dikali 6 sama dengan 18.",
                "visual": "Menulis [ ] x 6 = 18"
            },
            {
                "id": 11,
                "start": 49.20,
                "end": 55.00,
                "text": "Jadi jawabnya di sini adalah tiga, karena di sini kita menanyakan banyaknya kotak.",
                "display_text": "Jadi jawabnya di sini adalah 3, karena di sini kita menanyakan banyaknya kotak.",
                "visual": "Mengisi angka 3 pada perkalian (3 x 6 = 18)"
            },
            {
                "id": 12,
                "start": 55.20,
                "end": 61.00,
                "text": "Sekadar mengingatkan, dalam perkalian kalau kita punya tiga kali enam sama dengan delapan belas,",
                "display_text": "Sekadar mengingatkan, dalam perkalian kalau kita punya 3 x 6 sama dengan 18,",
                "visual": "Menegaskan kembali struktur perkalian 3 x 6 = 18"
            },
            {
                "id": 13,
                "start": 61.10,
                "end": 64.60,
                "text": "ini artinya tiga itu adalah banyaknya kotak.",
                "display_text": "ini artinya 3 itu adalah banyaknya kotak.",
                "visual": "Menunjuk angka 3 yang melambangkan banyaknya kotak"
            },
            {
                "id": 14,
                "start": 64.70,
                "end": 68.20,
                "text": "Sedangkan enam ini adalah isi tiap kotak.",
                "display_text": "Sedangkan 6 ini adalah isi tiap kotak.",
                "visual": "Menunjuk angka 6 yang melambangkan isi tiap kotak"
            },
            {
                "id": 15,
                "start": 68.40,
                "end": 74.40,
                "text": "Dan delapan belas ini adalah jumlah seluruh benda yang ada di dalam semua kotak itu.",
                "display_text": "Dan 18 ini adalah jumlah seluruh benda yang ada di dalam semua kotak itu.",
                "visual": "Menunjuk angka 18 yang melambangkan total seluruh benda"
            }
        ]
    }
]

def run_ffmpeg(cmd, desc="ffmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error during {desc}:")
        print(res.stderr[-600:])
        sys.exit(1)
    return res

def get_audio_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_atempo_filter(tempo: float) -> str:
    parts = []
    while tempo > 2.0:
        parts.append("atempo=2.0")
        tempo /= 2.0
    while tempo < 0.5:
        parts.append("atempo=0.5")
        tempo /= 0.5
    parts.append(f"atempo={tempo:.4f}")
    return ",".join(parts)

async def synthesize_edge_segment(text: str, output_path: str):
    import edge_tts
    comm = edge_tts.Communicate(text=text, voice="id-ID-GadisNeural", rate="+4%", pitch="+2Hz")
    await comm.save(output_path)

async def process_video(cfg, get_engine_fn, marcia_ref, marcia_ref_text):
    vid_id = cfg["id"]
    source_filename = cfg["source_filename"]
    src_file = os.path.join(DATA_VIDEO_DIR, source_filename)
    total_dur = cfg["duration"]
    segments = cfg["segments"]

    print("\n" + "="*80)
    print(f"🎬 MEMPROSES: {cfg['title']}")
    print(f"   Sumber File: {src_file} ({total_dur:.2f}s, {len(segments)} segmen ucapan)")
    print("="*80)

    if not os.path.exists(src_file):
        print(f"❌ File sumber tidak ditemukan: {src_file}")
        sys.exit(1)

    project_dir = os.path.join(VIDEO_PROJECTS_DIR, vid_id)
    segments_dir = os.path.join(project_dir, "segments")
    frames_dir = os.path.join(project_dir, "frames")
    os.makedirs(segments_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    # 1. Copy original video
    clip_orig = os.path.join(project_dir, "clip_original.mp4")
    shutil.copyfile(src_file, clip_orig)

    # 2. Extract original audio 24k
    orig_wav = os.path.join(project_dir, "original_audio_24k.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
        orig_wav
    ], "Extract 24k audio")
    orig_dur = get_audio_duration(orig_wav)

    # Calculate freeze frame duration
    freeze_dur = max(0.0, total_dur - orig_dur)
    print(f"   ⏱️ Durasi Asli: {orig_dur:.2f}s | Target Canvas: {total_dur:.2f}s | Freeze Frame Akhir: {freeze_dur:.2f}s")

    # 3. Extract 1fps frames
    print("   📷 Mengekstrak frame visual untuk thumbnail scrubber...")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-vf", "fps=1",
        os.path.join(frames_dir, "frame_%02d.jpg")
    ], "Extract frames")

    # 4. F5-TTS Synthesis
    import librosa
    import soundfile as sf
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"

    print(f"\n▶ Fase 1: Sintesis & Alignment F5-TTS Trainer Marcia ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        is_last = (sid == segments[-1]["id"])
        trim_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_trimmed.wav")
        aligned_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_aligned.wav")

        t0 = time.time()
        if not os.path.exists(trim_f5):
            print(f"  [{sid}/{len(segments)}] F5-TTS Synthesizing: \"{text}\"...", end="", flush=True)
            engine = get_engine_fn()
            res_f5 = engine.generate(
                ref_audio_path=marcia_ref,
                ref_text=marcia_ref_text,
                gen_text=text,
                speed=1.05,
                nfe_step=32,
                output_format="wav"
            )
            raw_f5 = os.path.join(BASE_DIR, res_f5["audio_url"].lstrip("/"))
            y, sr = librosa.load(raw_f5, sr=24000)
            y_trim, _ = librosa.effects.trim(y, top_db=25)
            sf.write(trim_f5, y_trim, sr)
        else:
            print(f"  [{sid}/{len(segments)}] F5-TTS Cached: \"{text}\"...", end="", flush=True)

        y_trim, sr = librosa.load(trim_f5, sr=24000)
        trim_dur = len(y_trim) / sr

        tempo = trim_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        cmd_align = [
            "ffmpeg", "-y", "-i", trim_f5,
            "-af", f"{atempo},{MASTER_FILTER}",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le"
        ]
        # Segmen terakhir tidak boleh di-hard-clip dengan -t agar suku kata akhir ("kotak itu") tidak terpotong!
        if not is_last:
            cmd_align.extend(["-t", str(target_dur)])
        cmd_align.append(aligned_f5)

        run_ffmpeg(cmd_align, f"Align F5 seg {sid}")
        s["audio_f5"] = f"/video-projects/{vid_id}/segments/f5_seg_{sid}_aligned.wav"
        print(f" ✓ ({time.time()-t0:.2f}s | aktif: {trim_dur:.2f}s -> target: {target_dur:.2f}s)")

    # 5. Edge-TTS Synthesis
    print(f"\n▶ Fase 2: Sintesis & Alignment Edge-TTS Studio ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        is_last = (sid == segments[-1]["id"])
        raw_edge = os.path.join(segments_dir, f"edge_seg_{sid}_raw.mp3")
        aligned_edge = os.path.join(segments_dir, f"edge_seg_{sid}_aligned.wav")

        if not os.path.exists(raw_edge):
            await synthesize_edge_segment(text, raw_edge)
        edge_dur = get_audio_duration(raw_edge)

        tempo = edge_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        cmd_align_edge = [
            "ffmpeg", "-y", "-i", raw_edge,
            "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le"
        ]
        if not is_last:
            cmd_align_edge.extend(["-t", str(target_dur)])
        cmd_align_edge.append(aligned_edge)

        run_ffmpeg(cmd_align_edge, f"Align Edge seg {sid}")
        s["audio_edge"] = f"/video-projects/{vid_id}/segments/edge_seg_{sid}_aligned.wav"

    # 6. Assemble Master Timelines
    print(f"\n▶ Fase 3: Merakit Master Timeline Audio & Video Padded Widescreen ({total_dur:.2f}s)...")
    silence_wav = os.path.join(segments_dir, "silence.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(total_dur),
        silence_wav
    ], "Generate silence")

    # Filter canvas 16:9 murni putih (#FFFFFF) dengan freeze frame akhir
    vf_pad_freeze = f"scale=928:696,pad=1280:720:176:0:color=white,tpad=stop_mode=clone:stop_duration={freeze_dur:.2f}"

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

        # Mix master wav (Wajib -ar 44100 pcm_s16le)
        run_ffmpeg([
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[outa]",
            "-t", str(total_dur),
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            master_wav
        ], f"Mix {mode}")

        # Convert master mp3
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", master_wav,
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            master_mp3
        ], f"MP3 {mode}")

        # Mux dubbed video dengan canvas 16:9 putih & freeze frame
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", clip_orig,
            "-i", master_wav,
            "-vf", vf_pad_freeze,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-t", str(total_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            video_dubbed
        ], f"Mux {mode} video")

        output_files[mode] = {
            "video": video_dubbed,
            "audio": master_mp3,
            "master_wav": master_wav
        }

    # 7. Kompresi Video Ringan Berkualitas Tinggi Sesuai Standar SO (Canvas Putih 16:9)
    print(f"\n▶ Fase 4: Optimasi Ukuran File Ringan (H.264 Tune Animation & WebM VP9 Canvas Putih)...")
    orig_size = os.path.getsize(src_file)

    # 7A. Lightweight MP4 (F5)
    f5_light_mp4 = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.mp4")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", output_files["f5"]["master_wav"],
        "-vf", vf_pad_freeze,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", str(total_dur),
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-ar", "44100",
        "-movflags", "+faststart",
        f5_light_mp4
    ], "Encode F5 lightweight MP4")

    # 7B. Lightweight WebM (F5)
    f5_light_webm = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.webm")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", f5_light_mp4,
        "-c:v", "libvpx-vp9", "-crf", "35", "-b:v", "0",
        "-c:a", "libopus", "-b:a", "36k",
        f5_light_webm
    ], "Encode F5 lightweight WebM")

    # 7C. Lightweight MP4 (Edge Studio)
    edge_light_mp4 = os.path.join(project_dir, f"video_dubbed_marcia_edge_ringan.mp4")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", output_files["edge"]["master_wav"],
        "-vf", vf_pad_freeze,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", str(total_dur),
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-ar", "44100",
        "-movflags", "+faststart",
        edge_light_mp4
    ], "Encode Edge lightweight MP4")

    # 8. Multi-Destination Synchronization
    print(f"\n▶ Fase 5: Sinkronisasi Multi-Tujuan...")
    # A. Salin ke Data VIdeo Marcia/
    data_ringan_dest = os.path.join(DATA_VIDEO_DIR, cfg["data_ringan_name"])
    shutil.copyfile(f5_light_mp4, data_ringan_dest)
    print(f"   ✓ Disalin ke Data VIdeo Marcia: {data_ringan_dest}")

    # B. Salin ke Hasil/videoMarcia/z5_pembagian/
    hasil_stem = cfg["hasil_stem"]
    hasil_mp4 = os.path.join(HASIL_Z5_DIR, f"{hasil_stem}_ringan.mp4")
    hasil_webm = os.path.join(HASIL_Z5_DIR, f"{hasil_stem}_ringan.webm")
    shutil.copyfile(f5_light_mp4, hasil_mp4)
    shutil.copyfile(f5_light_webm, hasil_webm)
    print(f"   ✓ Disalin ke Hasil: {hasil_mp4} & {hasil_webm}")

    # C. Salin ke Proyek SO (web/public/assets/videos/z5l1/)
    so_dest_stem = cfg["so_dest_stem"]
    so_mp4 = os.path.join(SO_Z5L1_DIR, f"{so_dest_stem}.mp4")
    so_webm = os.path.join(SO_Z5L1_DIR, f"{so_dest_stem}.webm")
    shutil.copyfile(f5_light_mp4, so_mp4)
    shutil.copyfile(f5_light_webm, so_webm)
    print(f"   ✓ Disalin ke Proyek SO: {so_mp4} & {so_webm}")

    # 9. Simpan Metadata Web Studio (/Proyek Video)
    metadata = {
        "id": vid_id,
        "title": cfg["title"],
        "subtitle": cfg["subtitle"],
        "total_duration": total_dur,
        "media": {
            "original_video": f"/video-projects/{vid_id}/clip_original.mp4",
            "dubbed_video_f5": f"/video-projects/{vid_id}/video_dubbed_marcia_f5_ringan.mp4",
            "dubbed_video_edge": f"/video-projects/{vid_id}/video_dubbed_marcia_edge_ringan.mp4",
            "dubbed_audio_f5": f"/video-projects/{vid_id}/master_dubbing_f5.mp3",
            "dubbed_audio_edge": f"/video-projects/{vid_id}/master_dubbing_edge.mp3"
        },
        "stats": {
            "original_bytes": orig_size,
            "light_mp4_bytes": os.path.getsize(f5_light_mp4),
            "light_webm_bytes": os.path.getsize(f5_light_webm),
            "compression_ratio": f"{((1 - os.path.getsize(f5_light_mp4)/orig_size)*100):.1f}%" if orig_size > 0 else "0%"
        },
        "segments": segments
    }

    meta_file = os.path.join(project_dir, "video_project_data.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Metadata Web Studio tersimpan: {meta_file}")

    print(f"\n📊 HASIL KOMPRESI: {vid_id}")
    print(f"   Original:  {orig_size / (1024*1024):.2f} MB")
    print(f"   F5 MP4:    {metadata['stats']['light_mp4_bytes'] / (1024*1024):.2f} MB (Hemat {metadata['stats']['compression_ratio']})")
    print(f"   F5 WebM:   {metadata['stats']['light_webm_bytes'] / (1024*1024):.2f} MB")

async def main():
    print("="*80)
    print("🎙️ SPRINT VIDEO DUBBING: ZONA 5 LEVEL 1 (PEMBAGIAN DASAR)")
    print("   Fix: Durasi Akhir Penuh, Bebas Terpotong, Canvas Putih 16:9 Bebas Hitam")
    print("="*80)

    # Lazy F5 Engine Loader
    engine_holder = {"engine": None}
    def get_engine():
        if engine_holder["engine"] is None:
            print("\n[Init] Memuat Model F5-TTS Indo V2...")
            from f5_engine import F5IndoEngine
            engine_holder["engine"] = F5IndoEngine()
            print("✓ Model F5-TTS siap digunakan pada:", engine_holder["engine"].device)
        return engine_holder["engine"]

    # Identitas Suara Marcia
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."
    print("✓ Audio Acuan Guru Marcia:", marcia_ref)

    start_all = time.time()
    for cfg in VIDEOS_CONFIG:
        await process_video(cfg, get_engine, marcia_ref, marcia_ref_text)

    if engine_holder["engine"] is not None:
        engine_holder["engine"].free_gpu_memory()

    total_time = time.time() - start_all
    print("\n" + "="*80)
    print(f"🎉 SELURUH 3 VIDEO ZONA 5 LEVEL 1 SELESAI DIDUBBING DALAM {total_time/60:.2f} MENIT!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
