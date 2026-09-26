#!/usr/bin/env python3
"""
render_flawless_52c.py

Perbaikan visual dan penggabungan video Zona 4 Level 5.2c secara sempurna:
1. Audio: Menggunakan master audio Marcia F5-TTS yang sudah divalidasi dan disetujui 100% oleh user ("Suara sudah benar").
2. Video: Meniadakan seluruh cacat garis putus / broken strokes:
   - Menggunakan video track asli dari 'Data VIdeo Marcia/zona 4 level 5-2c.mp4'.
   - Cara 1 (t=0s - 44.0s): Mengikuti video asli 1:1 tanpa pemotongan / masking buatan.
     Pada t=37s, tampilan bersih sesuai rekaman asli (angka pecahan 7, 10, 3, 10 dan garis bawah).
     Tepat saat kesimpulan "Jadi hasilnya 655" (t=43.4s), diagram lengkap Cara 1 muncul utuh.
   - Cara 2 (t=44.0s - 100.5s): Pada saat Marcia selesai menjelaskan Cara 2 (t=84.0s: "jadi hasilnya juga 655"),
     baris kedua menampilkan diagram Cara 2 lengkap dan utuh dari rekaman asli (orig frame 101s).
     Tidak ada garis yang terputus, tidak ada angka yang hilang.
   - Cara 3 (t=100.5s - 130.37s): Rekaman asli 1:1 di mana coretan mencongak ditulis bertahap secara alami.
3. Encoding ringan & distribusi ke seluruh direktori target.
"""

import os
import sys
import shutil
import subprocess
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "video_projects", "z4l5_2c_pengurangan_3d_3d_meminjam")
ORIG_VIDEO = os.path.join(BASE_DIR, "Data VIdeo Marcia", "zona 4 level 5-2c.mp4")
SO_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l5"
HASIL_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")

MASTER_AUDIO = os.path.join(PROJECT_DIR, "master_dubbing_f5.wav")
TEMP_VIDEO = os.path.join(PROJECT_DIR, "video_flawless_strokes.mp4")

def render_video():
    print("🎬 Mengekstrak frame master Cara 2 utuh dari video asli...")
    # Ekstrak frame 101s dari video asli untuk mengambil diagram Cara 2 yang utuh dan bersih
    frame101_path = "/tmp/f_orig_101.png"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-ss", "101.0", "-i", ORIG_VIDEO,
        "-vframes", "1", frame101_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f101_img = Image.open(frame101_path).convert("RGB")
    f101_arr = np.array(f101_img)

    # Area Cara 2 baris 2: y 270 sampai 450, x 100 sampai 650
    r2_y1, r2_y2 = 270, 450
    r2_x1, r2_x2 = 100, 650
    c2_complete_rgb = f101_arr[r2_y1:r2_y2, r2_x1:r2_x2, :]
    c2_complete_bgr = c2_complete_rgb[:, :, [2, 1, 0]]

    print("🎞️ Merender video dengan frame asli tanpa garis putus (1024x768 30fps)...")
    width, height, fps = 1024, 768, 30
    frame_bytes = width * height * 3

    in_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-i", ORIG_VIDEO,
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"
    ]
    pipe_in = subprocess.Popen(in_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    out_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{width}x{height}", "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        TEMP_VIDEO
    ]
    pipe_out = subprocess.Popen(out_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    frame_idx = 0
    while True:
        raw_frame = pipe_in.stdout.read(frame_bytes)
        if not raw_frame or len(raw_frame) < frame_bytes:
            break

        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3)).copy()
        t = frame_idx / fps

        # Antara t=84.0s (saat Marcia selesai membacakan hasil Cara 2) dan t=100.5s (saat Cara 2 asli muncul):
        # Tampilkan diagram Cara 2 utuh dari frame asli tanpa memotong garis apapun
        if 84.0 <= t < 100.5:
            frame[r2_y1:r2_y2, r2_x1:r2_x2] = c2_complete_bgr

        pipe_out.stdin.write(frame.tobytes())
        frame_idx += 1

    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()

    print(f"✅ Video berhasil dirender: {TEMP_VIDEO} ({frame_idx} frame)")

def encode_and_distribute():
    print("\n📦 Mengompresi video ringan (H.264 tune animation & WebM VP9)...")
    out_mp4 = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.mp4")
    out_webm = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.webm")

    # 1. MP4 H.264 Tune Animation CRF 28 + AAC 48k
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", TEMP_VIDEO,
        "-i", MASTER_AUDIO,
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation",
        "-c:a", "aac", "-b:a", "48k", "-ac", "1",
        "-movflags", "+faststart",
        out_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. WebM VP9 CRF 36 + Opus 48k
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", TEMP_VIDEO,
        "-i", MASTER_AUDIO,
        "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-deadline", "good", "-cpu-used", "2",
        "-c:a", "libopus", "-b:a", "48k", "-ac", "1",
        out_webm
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sz_mp4 = os.path.getsize(out_mp4) / (1024 * 1024)
    sz_webm = os.path.getsize(out_webm) / (1024 * 1024)
    print(f"  ✓ MP4 Ringan : {sz_mp4:.2f} MB")
    print(f"  ✓ WebM Ringan: {sz_webm:.2f} MB")

    # Distribusi
    # A. Data VIdeo Marcia
    dest_data_video = os.path.join(DATA_VIDEO_DIR, "zona 4 level 5-2c_ringan.mp4")
    shutil.copyfile(out_mp4, dest_data_video)
    print(f"  🚀 Disalin ke Data VIdeo Marcia: {dest_data_video}")

    # B. Hasil/videoMarcia/z4_pengurangan
    shutil.copyfile(out_mp4, os.path.join(HASIL_DIR, "z4l5_2c_pengurangan_3d_3d_meminjam_marcia_ringan.mp4"))
    shutil.copyfile(out_webm, os.path.join(HASIL_DIR, "z4l5_2c_pengurangan_3d_3d_meminjam_marcia_ringan.webm"))
    print(f"  🚀 Disalin ke Hasil/videoMarcia/z4_pengurangan/")

    # C. Proyek SO (Smart Otonomi)
    so_mp4 = os.path.join(SO_DIR, "z4l5sb2bermain2_marcia.mp4")
    so_webm = os.path.join(SO_DIR, "z4l5sb2bermain2_marcia.webm")
    shutil.copyfile(out_mp4, so_mp4)
    shutil.copyfile(out_webm, so_webm)
    print(f"  🚀 DISINKRONKAN KE PROYEK SO:")
    print(f"     -> {so_mp4}")
    print(f"     -> {so_webm}")

if __name__ == "__main__":
    render_video()
    encode_and_distribute()
    print("\n🎉 SELURUH PROSES SELESAI DENGAN SEMPURNA!")
