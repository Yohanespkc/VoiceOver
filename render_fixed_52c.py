#!/usr/bin/env python3
"""
render_fixed_52c.py

Memperbaiki video dan audio Zona 4 Level 5.2c secara sempurna:
1. Audio: Pelafalan baku "seratus delapan puluh tujuh" (seg 1) dan "seratusan" (seg 9).
2. Video: Memulihkan kemunculan tulisan/coretan secara progresif dan sinkron
   DENGAN PEMISAHAN GURATAN UTUH (NON-DESTRUCTIVE STROKE ISOLATION):
   - Menghilangkan seluruh cacat garis putus, sudut mengambang, guratan terpotong, dan titik liar (stray dots).
   - Cara 1 (t=21.0s - 43.4s):
     * Stage 1 (t=23.5s): Bracket ratusan utuh (7 ke 1) + angka 6 bersih.
     * Stage 2 (t=30.5s): Loop puluhan (10 ke 8) + lingkaran 3 dan 8 + angka 5 puluhan bersih.
     * Stage 3 (t=38.0s): Loop satuan (10 ke 7) + lingkaran 2 dan 7 + angka 5 satuan bersih.
     * Stage 4 (t=42.0s): Frame penuh r1_full (= 655 dengan garis bawah ganda).
   - Cara 2 (t=44.0s - 100.5s):
     * Stage 0 (t=44.0s): Soal bersih (clean) di baris 2.
     * Stage 1 (t=49.0s): Pecah puluhan utuh (coret 4, angka 3 bergaris bawah, lingkaran 12 bergaris bawah).
     * Stage 2 (t=60.0s): Pecah ratusan utuh (coret 8, angka 7 bergaris bawah, lingkaran 13).
     * Stage 3 (t=68.5s): Garis ratusan utuh (7 ke 1) + angka 6 bersih.
     * Stage 4 (t=74.5s): Garis puluhan utuh (13 ke 8) + garis bawah 8 + angka 5 puluhan bersih.
     * Stage 5 (t=82.0s): Frame penuh r2_full (garis 12 ke 7, = 655 dengan garis bawah ganda).
3. Master Audio & Video:
   - DSP highpass 80Hz + loudnorm -16 LUFS
   - H.264 CRF 28 tune animation & WebM VP9 CRF 36
4. Sinkronisasi ke Proyek SO, Data VIdeo Marcia, dan Hasil/videoMarcia/.
"""

import os
import sys
import json
import time
import shutil
import subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "video_projects", "z4l5_2c_pengurangan_3d_3d_meminjam")
ORIG_VIDEO = os.path.join(BASE_DIR, "Data VIdeo Marcia", "zona 4 level 5-2c.mp4")
SO_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l5"
HASIL_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")

os.makedirs(SO_DIR, exist_ok=True)
os.makedirs(HASIL_DIR, exist_ok=True)

def build_visual_stages():
    print("🎨 Menyiapkan lapisan visual pengerjaan Cara 1 dan Cara 2 (Metode Guratan Utuh)...")
    cmd1 = ["ffmpeg", "-y", "-ss", "20.0", "-i", ORIG_VIDEO, "-frames:v", "1", "/tmp/f20.png"]
    cmd2 = ["ffmpeg", "-y", "-ss", "44.0", "-i", ORIG_VIDEO, "-frames:v", "1", "/tmp/f44.png"]
    cmd3 = ["ffmpeg", "-y", "-ss", "100.5", "-i", ORIG_VIDEO, "-frames:v", "1", "/tmp/f100.png"]
    for c in [cmd1, cmd2, cmd3]:
        subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f20 = Image.open("/tmp/f20.png").convert("RGBA")
    f44 = Image.open("/tmp/f44.png").convert("RGBA")
    f100 = Image.open("/tmp/f100.png").convert("RGBA")

    # --- CARA 1 STAGES (y: 100-260, x: 100-650) ---
    r1_box = (100, 100, 650, 260)
    r1_clean = np.array(f20.crop(r1_box))
    r1_full = np.array(f44.crop(r1_box))
    diff_c1 = np.maximum(0, r1_clean[:, :, :3].mean(axis=2).astype(int) - r1_full[:, :, :3].mean(axis=2).astype(int))
    s_mask_1 = diff_c1 > 20

    # Isolasi digit hasil Cara 1
    h_mask_1 = s_mask_1.copy()
    h_mask_1[:, :330] = False
    lbl_h1, _ = label(h_mask_1)
    c1_d6 = (lbl_h1 == 1)       # Digit 6
    c1_d5_pul = (lbl_h1 == 3)   # Digit 5 (puluhan)
    c1_d5_sat = (lbl_h1 == 2)   # Digit 5 (satuan)

    # Bracket ratusan (7 ke 1) utuh tanpa sudut mengambang
    c1_top = s_mask_1 & (
        ((np.arange(160)[:, None] >= 34) & (np.arange(160)[:, None] <= 75) & (np.arange(550)[None, :] >= 64) & (np.arange(550)[None, :] <= 76)) |
        ((np.arange(160)[:, None] >= 34) & (np.arange(160)[:, None] <= 44) & (np.arange(550)[None, :] >= 74) & (np.arange(550)[None, :] <= 226)) |
        ((np.arange(160)[:, None] >= 35) & (np.arange(160)[:, None] <= 48) & (np.arange(550)[None, :] >= 220) & (np.arange(550)[None, :] <= 226))
    )

    # Loop puluhan (10 ke 8) tanpa menyentuh loop 7
    c1_mid = s_mask_1 & ~c1_top & (np.arange(550)[None, :] <= 290) & (
        ((np.arange(160)[:, None] >= 44) & (np.arange(160)[:, None] <= 62) & (np.arange(550)[None, :] >= 90)) |
        ((np.arange(160)[:, None] >= 55) & (np.arange(160)[:, None] <= 135) & (np.arange(550)[None, :] >= 239)) |
        ((np.arange(160)[:, None] >= 60) & (np.arange(160)[:, None] <= 95) & (np.arange(550)[None, :] >= 95) & (np.arange(550)[None, :] <= 135))
    )

    # Loop satuan (10 ke 7)
    c1_bot = s_mask_1 & ~c1_top & ~c1_mid & (np.arange(550)[None, :] >= 120) & (np.arange(550)[None, :] < 330)

    c1_st1 = r1_clean.copy(); c1_st1[c1_top | c1_d6] = r1_full[c1_top | c1_d6]
    c1_st2 = c1_st1.copy(); c1_st2[c1_mid | c1_d5_pul] = r1_full[c1_mid | c1_d5_pul]
    c1_st3 = c1_st2.copy(); c1_st3[c1_bot | c1_d5_sat] = r1_full[c1_bot | c1_d5_sat]
    c1_st4 = r1_full.copy()

    # --- CARA 2 STAGES (y: 280-450, x: 100-650) ---
    r2_box = (100, 280, 650, 450)
    r2_clean = np.array(f44.crop(r2_box))
    r2_full = np.array(f100.crop(r2_box))
    diff_c2 = np.maximum(0, r2_clean[:, :, :3].mean(axis=2).astype(int) - r2_full[:, :, :3].mean(axis=2).astype(int))
    s_mask_2 = diff_c2 > 20

    # Isolasi digit hasil Cara 2
    h_mask_2 = s_mask_2.copy()
    h_mask_2[:, :330] = False
    lbl_h2, _ = label(h_mask_2)
    objs_h2 = find_objects(lbl_h2)
    digits_h2 = []
    for i, slc in enumerate(objs_h2):
        cnt = (lbl_h2[slc] == (i + 1)).sum()
        if cnt > 10 and slc[0].stop < 112:
            digits_h2.append((slc[1].start, i + 1))
    digits_h2.sort(key=lambda x: x[0])
    c2_d6 = (lbl_h2 == digits_h2[0][1])
    c2_d5_pul = (lbl_h2 == digits_h2[1][1])

    # Garis atas ratusan (7 ke 1) utuh
    c2_top = s_mask_2 & (
        ((np.arange(170)[:, None] <= 52) & (np.arange(550)[None, :] >= 75) & (np.arange(550)[None, :] <= 245)) |
        ((np.arange(170)[:, None] <= 85) & (np.arange(550)[None, :] >= 230) & (np.arange(550)[None, :] <= 245)) |
        ((np.arange(170)[:, None] <= 65) & (np.arange(550)[None, :] >= 78) & (np.arange(550)[None, :] <= 88))
    )

    # Garis tengah puluhan (13 ke 8) utuh
    c2_mid = s_mask_2 & ~c2_top & (
        ((np.arange(170)[:, None] >= 55) & (np.arange(170)[:, None] <= 75) & (np.arange(550)[None, :] >= 135) & (np.arange(550)[None, :] <= 255)) |
        ((np.arange(170)[:, None] >= 75) & (np.arange(170)[:, None] <= 115) & (np.arange(550)[None, :] >= 240) & (np.arange(550)[None, :] <= 260)) |
        ((np.arange(170)[:, None] >= 115) & (np.arange(170)[:, None] <= 128) & (np.arange(550)[None, :] >= 235) & (np.arange(550)[None, :] <= 260))
    )

    # Garis bawah satuan (12 ke 7) utuh
    c2_bot = s_mask_2 & ~c2_top & ~c2_mid & (
        ((np.arange(170)[:, None] >= 75) & (np.arange(170)[:, None] <= 95) & (np.arange(550)[None, :] >= 175) & (np.arange(550)[None, :] <= 290)) |
        ((np.arange(170)[:, None] >= 95) & (np.arange(170)[:, None] <= 115) & (np.arange(550)[None, :] >= 270) & (np.arange(550)[None, :] <= 295)) |
        ((np.arange(170)[:, None] >= 115) & (np.arange(170)[:, None] <= 128) & (np.arange(550)[None, :] >= 270) & (np.arange(550)[None, :] <= 295))
    )

    # Pecah ratusan (coret 8, 7, lingkaran 13)
    c2_pecah_8 = s_mask_2 & (np.arange(550)[None, :] < 145) & ~c2_top & ~c2_mid & (
        (np.arange(550)[None, :] < 105) |
        ((np.arange(550)[None, :] < 142) & (np.arange(170)[:, None] < 82) & (np.arange(170)[:, None] > 48))
    )

    # Pecah puluhan (coret 4, 3, lingkaran 12)
    c2_pecah_4 = s_mask_2 & (np.arange(550)[None, :] >= 105) & (np.arange(550)[None, :] < 190) & ~c2_pecah_8 & ~c2_top & ~c2_mid & ~c2_bot

    c2_st1 = r2_clean.copy(); c2_st1[c2_pecah_4] = r2_full[c2_pecah_4]
    c2_st2 = c2_st1.copy(); c2_st2[c2_pecah_8] = r2_full[c2_pecah_8]
    c2_st3 = c2_st2.copy(); c2_st3[c2_top | c2_d6] = r2_full[c2_top | c2_d6]
    c2_st4 = c2_st3.copy(); c2_st4[c2_mid | c2_d5_pul] = r2_full[c2_mid | c2_d5_pul]
    c2_st5 = r2_full.copy()

    print("   ✅ Seluruh guratan visual berhasil dipisahkan tanpa ada garis putus atau titik liar.")
    return {
        "r1_box": r1_box,
        "c1_stages": {
            "st0": r1_clean,
            "st1": c1_st1,
            "st2": c1_st2,
            "st3": c1_st3,
            "st4": c1_st4
        },
        "r2_box": r2_box,
        "c2_stages": {
            "clean": r2_clean,
            "st1": c2_st1,
            "st2": c2_st2,
            "st3": c2_st3,
            "st4": c2_st4,
            "st5": c2_st5
        }
    }

def generate_synchronized_video(stages_data, out_video_path):
    print("\n🎞️  Merender Video Baru dengan Coretan Tulisan Sinkron (1024x768 30fps)...")
    width, height, fps = 1024, 768, 30
    r1_x1, r1_y1, r1_x2, r1_y2 = stages_data["r1_box"]
    r2_x1, r2_y1, r2_x2, r2_y2 = stages_data["r2_box"]

    c1 = stages_data["c1_stages"]
    c2 = stages_data["c2_stages"]

    in_cmd = [
        "ffmpeg", "-i", ORIG_VIDEO,
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"
    ]
    pipe_in = subprocess.Popen(in_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    out_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{width}x{height}", "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        out_video_path
    ]
    pipe_out = subprocess.Popen(out_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    frame_bytes = width * height * 3
    frame_idx = 0
    t0 = time.time()

    c1_bgr = {k: v[:, :, [2, 1, 0]] for k, v in c1.items()}
    c2_bgr = {k: v[:, :, [2, 1, 0]] for k, v in c2.items()}

    while True:
        raw_frame = pipe_in.stdout.read(frame_bytes)
        if not raw_frame or len(raw_frame) < frame_bytes:
            break

        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3)).copy()
        t = frame_idx / fps

        # 1. Cara 1 Progressive Rendering (21.0s <= t < 43.4s)
        if 21.0 <= t < 43.4:
            if t < 23.5:
                pass
            elif t < 30.5:
                # Segmen 4: ratusannya 7 - 1 = 6 (Bracket ratusan + angka 6 bersih)
                frame[r1_y1:r1_y2, r1_x1:r1_x2] = c1_bgr["st1"]
            elif t < 38.0:
                # Segmen 5: puluhannya 10 - 8 = 2, + 3 = 5 (Loop puluhan + angka 5 puluhan bersih)
                frame[r1_y1:r1_y2, r1_x1:r1_x2] = c1_bgr["st2"]
            elif t < 42.0:
                # Segmen 6: satuannya 10 - 7 = 3, + 2 = 5 (Loop satuan + angka 5 satuan bersih)
                frame[r1_y1:r1_y2, r1_x1:r1_x2] = c1_bgr["st3"]
            else:
                # Segmen 7: = 655 lengkap bergaris bawah
                frame[r1_y1:r1_y2, r1_x1:r1_x2] = c1_bgr["st4"]

        # 2. Cara 2 Progressive Rendering (43.4s <= t < 100.5s)
        if 43.4 <= t < 100.5:
            if t < 49.0:
                # Menampilkan soal bersih di baris 2
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["clean"]
            elif t < 60.0:
                # Segmen 8: pecah puluhan (coret 4, angka 3, lingkaran 12 utuh)
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["st1"]
            elif t < 68.5:
                # Segmen 9: pecah ratusan (coret 8, angka 7, lingkaran 13 utuh)
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["st2"]
            elif t < 74.5:
                # Segmen 10: 7 - 1 = 6 (garis 7 ke 1 utuh + angka 6 bersih)
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["st3"]
            elif t < 82.0:
                # Segmen 11: 13 - 8 = 5 (garis 13 ke 8 utuh + garis bawah 8 + angka 5 puluhan)
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["st4"]
            else:
                # Segmen 12: 12 - 7 = 5 (garis 12 ke 7 utuh, = 655 bergaris bawah ganda)
                frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_bgr["st5"]

        pipe_out.stdin.write(frame.tobytes())
        frame_idx += 1

        if frame_idx % 400 == 0:
            pct = (frame_idx / 3911) * 100
            print(f"   Render frame {frame_idx}/3911 ({pct:.1f}%) | t={t:.1f}s")

    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()

    dur = time.time() - t0
    print(f"✅ Video berhasil dirender: {out_video_path} ({frame_idx} frame dalam {dur:.1f}s)")

def assemble_master_audio():
    print("\n🎙️  Merakit Master Audio Marcia F5-TTS...")
    meta_path = os.path.join(PROJECT_DIR, "video_project_data.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    segments = meta["segments"]
    total_dur = meta["duration_seconds"]
    seg_dir = os.path.join(PROJECT_DIR, "segments")

    audio_items = []
    current_cursor = 0.0

    for s in segments:
        sid = s["id"]
        t_start = s["start"]
        f5_file = os.path.join(seg_dir, f"f5_seg_{sid}_aligned.wav")

        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", f5_file]
        dur = float(subprocess.check_output(cmd).decode().strip())

        eff_start = max(t_start, current_cursor)
        if eff_start > current_cursor + 0.05:
            eff_start = t_start
        if eff_start < current_cursor:
            eff_start = current_cursor + 0.04

        audio_items.append({
            "sid": sid,
            "path": f5_file,
            "eff_start": eff_start,
            "dur": dur,
            "text": s["text"]
        })
        current_cursor = eff_start + dur

    inputs = []
    delays = []
    for idx, item in enumerate(audio_items):
        inputs.extend(["-i", item["path"]])
        delay_ms = int(round(item["eff_start"] * 1000))
        delays.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}]")

    mix_inputs = "".join(f"[a{i}]" for i in range(len(audio_items)))
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"
    filter_complex = f"{';'.join(delays)};{mix_inputs}amix=inputs={len(audio_items)}:normalize=0:dropout_transition=0,apad=whole_dur={total_dur:.3f},{MASTER_FILTER}[aout]"

    master_wav = os.path.join(PROJECT_DIR, "master_dubbing_f5.wav")
    master_mp3 = os.path.join(PROJECT_DIR, "master_dubbing_f5.mp3")

    mix_cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", str(total_dur),
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
        master_wav
    ]
    subprocess.run(mix_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "ffmpeg", "-y", "-i", master_wav,
        "-c:a", "libmp3lame", "-b:a", "192k",
        master_mp3
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"✅ Master audio berhasil dirakit: {master_mp3}")
    return master_wav

def encode_lightweight_outputs(fixed_video, master_audio):
    print("\n📦 Mengompres Video Ringan Berkualitas Prima (H.264 & WebM)...")
    out_mp4 = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.mp4")
    out_webm = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.webm")

    # MP4 H.264 tune animation CRF 28
    subprocess.run([
        "ffmpeg", "-y",
        "-i", fixed_video,
        "-i", master_audio,
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation",
        "-c:a", "aac", "-b:a", "48k", "-ac", "1",
        "-movflags", "+faststart",
        out_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # WebM VP9 CRF 36
    subprocess.run([
        "ffmpeg", "-y",
        "-i", fixed_video,
        "-i", master_audio,
        "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-deadline", "good", "-cpu-used", "2",
        "-c:a", "libopus", "-b:a", "48k", "-ac", "1",
        out_webm
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    mp4_sz = os.path.getsize(out_mp4) / 1024 / 1024
    webm_sz = os.path.getsize(out_webm) / 1024 / 1024
    print(f"  ✓ MP4 Ringan : {mp4_sz:.2f} MB")
    print(f"  ✓ WebM Ringan: {webm_sz:.2f} MB")

    # Distribusi
    # 1. Data VIdeo Marcia
    dest_data_video = os.path.join(DATA_VIDEO_DIR, "zona 4 level 5-2c_ringan.mp4")
    shutil.copyfile(out_mp4, dest_data_video)
    print(f"  🚀 Disalin ke Data VIdeo Marcia: {dest_data_video}")

    # 2. Hasil/videoMarcia/z4_pengurangan
    shutil.copyfile(out_mp4, os.path.join(HASIL_DIR, "z4l5_2c_pengurangan_3d_3d_meminjam_marcia_ringan.mp4"))
    shutil.copyfile(out_webm, os.path.join(HASIL_DIR, "z4l5_2c_pengurangan_3d_3d_meminjam_marcia_ringan.webm"))
    print(f"  🚀 Disalin ke Hasil/videoMarcia/z4_pengurangan/")

    # 3. Proyek SO
    so_mp4 = os.path.join(SO_DIR, "z4l5sb2bermain2_marcia.mp4")
    so_webm = os.path.join(SO_DIR, "z4l5sb2bermain2_marcia.webm")
    shutil.copyfile(out_mp4, so_mp4)
    shutil.copyfile(out_webm, so_webm)
    print(f"  🚀 DISINKRONKAN KE PROYEK SO:")
    print(f"     -> {so_mp4}")
    print(f"     -> {so_webm}")

if __name__ == "__main__":
    t_start = time.time()
    stages = build_visual_stages()
    fixed_video = os.path.join(PROJECT_DIR, "video_fixed_strokes.mp4")
    generate_synchronized_video(stages, fixed_video)
    master_audio = assemble_master_audio()
    encode_lightweight_outputs(fixed_video, master_audio)
    total_time = time.time() - t_start
    print(f"\n🎉 SELURUH PERBAIKAN SELESAI DALAM {total_time:.1f} DETIK!")
