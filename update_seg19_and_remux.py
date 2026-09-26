#!/usr/bin/env python3
"""
update_seg19_and_remux.py

Memperbarui segmen 19 dengan audio F5-TTS yang sudah terbukti 100% presisi fonetik
("delapan ribu dua ratus dua puluh tiga, dikurang lima ribu dua ratus dua puluh empat"),
merakit ulang master audio timeline, dan me-remux video ringan.
"""

import os
import sys
import shutil
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "video_projects", "z4l6_pengurangan_4d_4d_meminjam")
SEGMENTS_DIR = os.path.join(PROJECT_DIR, "segments")
DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
HASIL_Z4_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
SO_Z4L6_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l6"

MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"
total_dur = 186.70

def run_ffmpeg(cmd, desc="FFmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg Gagal [{desc}]: {res.stderr[-400:]}")
        raise RuntimeError(f"FFmpeg error: {res.stderr[-400:]}")
    return res

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

def update_seg19():
    print("🎙️ Memperbarui segmen 19 dengan F5-TTS artikulasi presisi...")
    src_wav = "/tmp/test_seg19_f5.wav"
    target_dur = 106.00 - 100.64  # 5.36s
    dur = get_audio_duration(src_wav)
    tempo = max(0.85, min(1.25, dur / target_dur))
    atempo = build_atempo_filter(tempo)

    aligned_wav = os.path.join(SEGMENTS_DIR, "f5_seg_19_aligned.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", src_wav,
        "-af", f"{atempo},{MASTER_FILTER}",
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
        aligned_wav
    ], "Align F5 seg 19")
    print(f"  ✓ Segmen 19 terpasang: {get_audio_duration(aligned_wav):.2f}s")

def remux_master():
    print("🎛️ Merakit ulang Master Timeline Audio...")
    meta_path = os.path.join(PROJECT_DIR, "video_project_data.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    segments = meta["segments"]
    silence_wav = os.path.join(SEGMENTS_DIR, "silence.wav")

    master_wav = os.path.join(PROJECT_DIR, "master_dubbing_f5.wav")
    master_mp3 = os.path.join(PROJECT_DIR, "master_dubbing_f5.mp3")

    inputs = ["-i", silence_wav]
    delays = []
    for idx, s in enumerate(segments):
        seg_path = os.path.join(SEGMENTS_DIR, f"f5_seg_{s['id']}_aligned.wav")
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
        master_wav
    ], "Mix master F5")

    run_ffmpeg([
        "ffmpeg", "-y", "-i", master_wav,
        "-c:a", "libmp3lame", "-b:a", "320k",
        master_mp3
    ], "Master MP3 F5")
    print(f"  ✓ Master Audio selesai: {master_mp3}")

    print("🎞️ Me-remux video ringan dengan audio F5-TTS sempurna...")
    clip_orig = os.path.join(PROJECT_DIR, "clip_original.mp4")
    out_mp4 = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.mp4")
    out_webm = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.webm")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", master_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation",
        "-c:a", "aac", "-b:a", "48k", "-ac", "1",
        "-movflags", "+faststart",
        out_mp4
    ], "Encode MP4 Ringan")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", master_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-deadline", "good", "-cpu-used", "2",
        "-c:a", "libopus", "-b:a", "48k", "-ac", "1",
        out_webm
    ], "Encode WebM Ringan")

    sz_mp4 = os.path.getsize(out_mp4) / (1024 * 1024)
    sz_webm = os.path.getsize(out_webm) / (1024 * 1024)
    print(f"  ✓ MP4 Ringan : {sz_mp4:.2f} MB")
    print(f"  ✓ WebM Ringan: {sz_webm:.2f} MB")

    # Distribusi
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

if __name__ == "__main__":
    update_seg19()
    remux_master()
    print("🎉 PEMBARUAN AUDIO SELESAI DENGAN SEMPURNA!")
