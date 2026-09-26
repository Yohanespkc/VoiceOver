import os
import sys
import time
import subprocess
import shutil
import librosa
import soundfile as sf

BASE_DIR = "/Users/yohanessurya/Documents/Development/VoiceOver"
sys.path.insert(0, BASE_DIR)

from f5_engine import F5IndoEngine

PROJECT_DIR = os.path.join(BASE_DIR, "video_projects", "z4l6_pengurangan_4d_4d_meminjam")
SEGMENTS_DIR = os.path.join(PROJECT_DIR, "segments")
CLIP_ORIG = os.path.join(PROJECT_DIR, "clip_original.mp4")
DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
HASIL_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
SO_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l6"

MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"
TOTAL_DUR = 186.70

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

def run_ffmpeg(cmd, desc="FFmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error [{desc}]: {res.stderr[-400:]}")
    return res

def process_single_seg(engine, sid, text, target_start, target_end):
    target_dur = target_end - target_start
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."
    
    print(f"🎙️ Generating Segmen {sid}...")
    res = engine.generate(
        ref_audio_path=marcia_ref,
        ref_text=marcia_ref_text,
        gen_text=text,
        speed=1.02,
        nfe_step=32,
        output_format="wav"
    )
    raw = os.path.join(BASE_DIR, res["audio_url"].lstrip("/"))
    
    y, sr = librosa.load(raw, sr=24000)
    y_trim, _ = librosa.effects.trim(y, top_db=25)
    trim_path = os.path.join(SEGMENTS_DIR, f"f5_seg_{sid}_trimmed.wav")
    sf.write(trim_path, y_trim, sr)
    trim_dur = len(y_trim) / sr
    
    tempo = trim_dur / target_dur if target_dur > 0 else 1.0
    tempo = max(0.85, min(1.25, tempo))
    atempo = build_atempo_filter(tempo)
    aligned_path = os.path.join(SEGMENTS_DIR, f"f5_seg_{sid}_aligned.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", trim_path,
        "-af", f"{atempo},{MASTER_FILTER}",
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
        aligned_path
    ], f"Align F5 seg {sid}")
    
    actual_dur = get_audio_duration(aligned_path)
    print(f"  ✓ Segmen {sid} OK: {actual_dur:.2f}s (target: {target_dur:.2f}s)")
    return aligned_path

def main():
    engine = F5IndoEngine()
    
    # 1. Update seg 11 & 18
    # Seg 11: 54.14 - 60.50
    process_single_seg(
        engine, 11,
        "Tapi ingat, di sini masih ada satu lagi. Jadi hasilnya satu tambah satu, yaitu dua.",
        54.14, 60.50
    )
    
    # Seg 18: 93.64 - 100.50
    process_single_seg(
        engine, 18,
        "Lalu satu ditambah pasangan dari sembilan, yaitu satu tambah satu hasilnya dua.",
        93.64, 100.50
    )

    # 2. Reassemble Master Timeline
    print("\n🎛️ Merakit Master Timeline Audio F5-TTS...")
    import json
    meta_path = os.path.join(PROJECT_DIR, "video_project_data.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    segments = meta["segments"]
    # Update text in metadata
    for s in segments:
        if s["id"] == 11:
            s["text"] = "Tapi ingat, di sini masih ada satu lagi. Jadi hasilnya satu tambah satu, yaitu dua."
            s["display_text"] = "1 + 1 = 2."
        elif s["id"] == 18:
            s["text"] = "Lalu satu ditambah pasangan dari sembilan, yaitu satu tambah satu hasilnya dua."
            s["display_text"] = "1 + pasangan 9 (1) = 2."

    silence_wav = os.path.join(SEGMENTS_DIR, "silence.wav")
    inputs = ["-i", silence_wav]
    delays = []
    for idx, s in enumerate(segments):
        seg_file = os.path.join(SEGMENTS_DIR, f"f5_seg_{s['id']}_aligned.wav")
        inputs.extend(["-i", seg_file])
        delay_ms = int(s["start"] * 1000)
        delays.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[d{idx+1}]")

    filter_parts = delays
    mix_inputs = "".join([f"[d{i+1}]" for i in range(len(segments))])
    total_in = len(segments) + 1
    filter_parts.append(f"[0:a]{mix_inputs}amix=inputs={total_in}:duration=first:dropout_transition=0,volume=3.0,{MASTER_FILTER}[outa]")
    filter_str = ";".join(filter_parts)

    master_wav = os.path.join(PROJECT_DIR, "master_dubbing_f5.wav")
    master_mp3 = os.path.join(PROJECT_DIR, "master_dubbing_f5.mp3")

    run_ffmpeg([
        "ffmpeg", "-y"
    ] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-t", str(TOTAL_DUR),
        "-c:a", "pcm_s16le",
        master_wav
    ], "Mix master F5")

    run_ffmpeg([
        "ffmpeg", "-y", "-i", master_wav,
        "-c:a", "libmp3lame", "-b:a", "320k",
        master_mp3
    ], "Master MP3 F5")

    # 3. Re-mux video
    print("\n🎞️ Me-remux video ringan dengan master audio baru...")
    out_mp4 = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.mp4")
    out_webm = os.path.join(PROJECT_DIR, "video_dubbed_marcia_f5_ringan.webm")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", CLIP_ORIG,
        "-i", master_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation",
        "-c:a", "aac", "-b:a", "48k", "-ac", "1",
        "-movflags", "+faststart",
        out_mp4
    ], "Encode MP4")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", CLIP_ORIG,
        "-i", master_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-deadline", "good", "-cpu-used", "2",
        "-c:a", "libopus", "-b:a", "48k", "-ac", "1",
        out_webm
    ], "Encode WebM")

    # 4. Copy to destinations
    shutil.copyfile(out_mp4, os.path.join(DATA_VIDEO_DIR, "zona 4 level 6_ringan.mp4"))
    shutil.copyfile(out_mp4, os.path.join(HASIL_DIR, "z4l6_pengurangan_4d_4d_meminjam_marcia_ringan.mp4"))
    shutil.copyfile(out_webm, os.path.join(HASIL_DIR, "z4l6_pengurangan_4d_4d_meminjam_marcia_ringan.webm"))
    shutil.copyfile(out_mp4, os.path.join(SO_DIR, "z4l6sb1bermain1_marcia.mp4"))
    shutil.copyfile(out_webm, os.path.join(SO_DIR, "z4l6sb1bermain1_marcia.webm"))

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Selesai! Ukuran MP4: {os.path.getsize(out_mp4)/(1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
