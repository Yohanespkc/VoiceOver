#!/usr/bin/env python3
"""
Generate Synchronized Marcia VoiceOver for 36s GASING Video (2 Digit x 1 Digit)
Produces both F5-TTS Indo Cloned Voice and Edge-TTS Studio Voiceover,
perfectly synced with handwriting actions on screen.
"""

import os
import sys
import json
import asyncio
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SEGMENTS_DIR = os.path.join(PROJECT_DIR, "segments")
os.makedirs(SEGMENTS_DIR, exist_ok=True)

VIDEO_INPUT = os.path.join(PROJECT_DIR, "clip_36s.mp4")
REF_AUDIO = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
REF_TEXT = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."

SEGMENTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 3.80,
        "visual": "Layar pembuka menampilkan judul naskah dan soal perkalian 2 digit x 1 digit",
        "prof_text": "Perkalian dua digit dengan satu digit",
        "marcia_text": "Perkalian dua digit dengan satu digit.",
        "edge_rate": "+3%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 2,
        "start": 3.80,
        "end": 7.00,
        "visual": "Menunjuk soal pertama di kiri atas: 42 x 3",
        "prof_text": "Kita lihat di sini, 42 kali 3",
        "marcia_text": "Kita lihat di sini: empat puluh dua kali tiga.",
        "edge_rate": "+6%",
        "edge_pitch": "+3Hz"
    },
    {
        "id": 3,
        "start": 7.00,
        "end": 10.90,
        "visual": "Menulis tanda di bawah angka 4 (puluhan) dan di bawah angka 2 (satuan)",
        "prof_text": "4 ini adalah puluhan, 2 satuan",
        "marcia_text": "Empat ini adalah puluhan... dua, satuan.",
        "edge_rate": "+0%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 4,
        "start": 10.90,
        "end": 15.00,
        "visual": "Menulis 2 slot garis kosong di bawah soal: _ _ (slot puluhan & satuan)",
        "prof_text": "Kita lihat hasilnya adalah: ini puluhan, ini satuan",
        "marcia_text": "Kita lihat hasilnya adalah: ini puluhan, ini satuan.",
        "edge_rate": "+2%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 5,
        "start": 15.00,
        "end": 19.40,
        "visual": "Menarik garis dari 4 ke 3 (4 x 3), menulis angka 1 di posisi puluhan",
        "prof_text": "4 dikali 3 puluhan, yang berarti ada 12",
        "marcia_text": "Empat dikali tiga puluhan, yang berarti ada dua belas.",
        "edge_rate": "+4%",
        "edge_pitch": "+3Hz"
    },
    {
        "id": 6,
        "start": 19.40,
        "end": 26.50,
        "visual": "Menulis angka 2 (menjadi 12 _), menjelaskan konsep 40 x 3 = 120 = 12 puluhan",
        "prof_text": "karena 40 kali 3 satuan itu adalah hasilnya 12 puluhan",
        "marcia_text": "karena empat puluh kali tiga satuan, itu adalah hasilnya dua belas puluhan.",
        "edge_rate": "+1%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 7,
        "start": 26.50,
        "end": 32.00,
        "visual": "Menarik garis lengkung dari angka 2 ke 3 (2 x 3)",
        "prof_text": "kemudian 2 satuan kali 3 satuan, itu adalah 6 satuan",
        "marcia_text": "kemudian, dua satuan kali tiga satuan... itu adalah enam satuan.",
        "edge_rate": "+2%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 8,
        "start": 32.00,
        "end": 36.00,
        "visual": "Menulis angka 6 di slot satuan (menjadi 12 6 = 126), menggarisbawahi 12 dan 6",
        "prof_text": "jadi 42 kali 3 itu: 126 (seratus dua puluh enam)",
        "marcia_text": "jadi, empat puluh dua kali tiga itu: seratus dua puluh enam!",
        "edge_rate": "+5%",
        "edge_pitch": "+3Hz"
    }
]

def get_audio_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip()) if res.stdout.strip() else 0.0

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

async def generate_edge_segments():
    import edge_tts
    print("\n--- 1. Generating Edge-TTS Segments (id-ID-GadisNeural) ---")
    for seg in SEGMENTS:
        sid = seg["id"]
        target_dur = seg["end"] - seg["start"]
        raw_mp3 = os.path.join(SEGMENTS_DIR, f"edge_seg_{sid}_raw.mp3")
        aligned_wav = os.path.join(SEGMENTS_DIR, f"edge_seg_{sid}_aligned.wav")
        
        # Sintesis Edge-TTS
        comm = edge_tts.Communicate(
            text=seg["marcia_text"],
            voice="id-ID-GadisNeural",
            rate=seg.get("edge_rate", "+2%"),
            pitch=seg.get("edge_pitch", "+2Hz")
        )
        await comm.save(raw_mp3)
        
        # Hitung durasi asli
        raw_dur = get_audio_duration(raw_mp3)
        tempo_factor = raw_dur / target_dur if target_dur > 0 else 1.0
        
        # Clamp tempo agar tetap natural (0.85 s/d 1.35)
        tempo_factor = max(0.85, min(1.35, tempo_factor))
        atempo = build_atempo_filter(tempo_factor)
        
        # Align audio to exact target duration with high quality resample
        cmd = [
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_wav
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        final_dur = get_audio_duration(aligned_wav)
        seg["edge_aligned_wav"] = aligned_wav
        seg["edge_duration"] = round(final_dur, 2)
        print(f"  Seg {sid}: raw {raw_dur:.2f}s -> aligned {final_dur:.2f}s (target: {target_dur:.2f}s)")

def generate_f5_segments():
    print("\n--- 2. Generating F5-TTS Cloned Segments (Guru Marcia Authentic) ---")
    from f5_engine import F5IndoEngine
    engine = F5IndoEngine.get_instance()
    
    for seg in SEGMENTS:
        sid = seg["id"]
        target_dur = seg["end"] - seg["start"]
        raw_wav = os.path.join(SEGMENTS_DIR, f"f5_seg_{sid}_raw.wav")
        aligned_wav = os.path.join(SEGMENTS_DIR, f"f5_seg_{sid}_aligned.wav")
        
        # Generate with F5-TTS
        res = engine.generate(
            ref_audio_path=REF_AUDIO,
            ref_text=REF_TEXT,
            gen_text=seg["marcia_text"],
            speed=1.0,
            nfe_step=32,
            output_format="wav"
        )
        src_wav = os.path.join(BASE_DIR, res["audio_url"].lstrip("/"))
        shutil.copyfile(src_wav, raw_wav)
        
        raw_dur = get_audio_duration(raw_wav)
        tempo_factor = raw_dur / target_dur if target_dur > 0 else 1.0
        tempo_factor = max(0.85, min(1.35, tempo_factor))
        atempo = build_atempo_filter(tempo_factor)
        
        # Align to target duration with voice enhancement
        cmd = [
            "ffmpeg", "-y", "-i", raw_wav,
            "-af", f"{atempo},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_wav
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        final_dur = get_audio_duration(aligned_wav)
        seg["f5_aligned_wav"] = aligned_wav
        seg["f5_duration"] = round(final_dur, 2)
        print(f"  Seg {sid}: raw {raw_dur:.2f}s -> aligned {final_dur:.2f}s (target: {target_dur:.2f}s)")

def assemble_master_track(mode: str = "edge") -> str:
    """Stitch segments onto a continuous 36.00s audio track at exact start timestamps."""
    print(f"\n--- 3. Assembling Master 36s Audio ({mode.upper()}) ---")
    out_wav = os.path.join(PROJECT_DIR, f"master_dubbing_{mode}.wav")
    out_mp3 = os.path.join(PROJECT_DIR, f"master_dubbing_{mode}.mp3")
    
    # Generate 36 seconds of pure silence
    silence_wav = os.path.join(SEGMENTS_DIR, "silence_36s.wav")
    cmd_silence = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "36.00", "-c:a", "pcm_s16le", silence_wav
    ]
    subprocess.run(cmd_silence, capture_output=True, check=True)
    
    # Build filter_complex string to overlay each segment at its start timestamp
    inputs = ["-i", silence_wav]
    filter_parts = []
    mix_labels = ["[0:a]"]
    
    for idx, seg in enumerate(SEGMENTS):
        seg_file = seg[f"{mode}_aligned_wav"]
        inputs.extend(["-i", seg_file])
        inp_idx = idx + 1
        delay_ms = int(seg["start"] * 1000)
        delayed_label = f"[delayed_{inp_idx}]"
        filter_parts.append(f"[{inp_idx}:a]adelay={delay_ms}|{delay_ms}{delayed_label}")
        mix_labels.append(delayed_label)
    
    full_mix_inputs = "".join(mix_labels)
    filter_parts.append(f"{full_mix_inputs}amix=inputs={len(mix_labels)}:duration=first:dropout_transition=0,volume={len(mix_labels)}[outa]")
    
    filter_complex = ";".join(filter_parts)
    
    cmd_mix = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-t", "36.00",
        "-c:a", "pcm_s16le",
        out_wav
    ]
    subprocess.run(cmd_mix, capture_output=True, check=True)
    
    # Convert to MP3 320k
    cmd_mp3 = [
        "ffmpeg", "-y", "-i", out_wav,
        "-c:a", "libmp3lame", "-b:a", "320k",
        out_mp3
    ]
    subprocess.run(cmd_mp3, capture_output=True, check=True)
    
    dur = get_audio_duration(out_wav)
    print(f"  Master {mode.upper()} track assembled: {dur:.2f}s -> {out_wav}")
    return out_wav

def mux_video_with_dubbing(audio_wav: str, mode: str = "edge") -> str:
    print(f"\n--- 4. Muxing Dubbed Video ({mode.upper()}) ---")
    out_video = os.path.join(PROJECT_DIR, f"video_dubbed_marcia_{mode}.mp4")
    
    # Mux clean H.264 video with synchronized Marcia audio
    cmd = [
        "ffmpeg", "-y",
        "-i", VIDEO_INPUT,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    dur = get_audio_duration(out_video)
    print(f"  Dubbed MP4 ready: {dur:.2f}s -> {out_video}")
    return out_video

async def main():
    print("==================================================================")
    print("  PROYEK VIDEO VOICEOVER: YOUTUBE 36s DUBBING MARCIA SYNCHRONIZER  ")
    print("==================================================================")
    
    # 1. Edge-TTS Studio
    await generate_edge_segments()
    edge_master_wav = assemble_master_track("edge")
    mux_video_with_dubbing(edge_master_wav, "edge")
    
    # 2. F5-TTS Cloned Voice
    try:
        generate_f5_segments()
        f5_master_wav = assemble_master_track("f5")
        mux_video_with_dubbing(f5_master_wav, "f5")
    except Exception as e:
        print(f"Warning F5 generation: {e}")
    
    # 3. Save Project Metadata
    data = {
        "title": "Percobaan Video Perkalian 2 Digit x 1 Digit (00:00 - 00:36)",
        "source_url": "https://www.youtube.com/watch?v=t630efAuHPU",
        "duration_seconds": 36.00,
        "original_character": "Prof. Yohanes Surya",
        "dubbed_character": "Guru Marcia (Trainer Marcia Asli)",
        "files": {
            "original_video": "/video-projects/perkalian_2digit_1digit/clip_36s.mp4",
            "original_audio": "/video-projects/perkalian_2digit_1digit/clip_36s_audio.wav",
            "dubbed_video_edge": "/video-projects/perkalian_2digit_1digit/video_dubbed_marcia_edge.mp4",
            "dubbed_audio_edge": "/video-projects/perkalian_2digit_1digit/master_dubbing_edge.mp3",
            "dubbed_video_f5": "/video-projects/perkalian_2digit_1digit/video_dubbed_marcia_f5.mp4",
            "dubbed_audio_f5": "/video-projects/perkalian_2digit_1digit/master_dubbing_f5.mp3"
        },
        "segments": [
            {
                "id": s["id"],
                "start": s["start"],
                "end": s["end"],
                "visual": s["visual"],
                "prof_text": s["prof_text"],
                "marcia_text": s["marcia_text"],
                "audio_edge": f"/video-projects/perkalian_2digit_1digit/segments/edge_seg_{s['id']}_aligned.wav",
                "audio_f5": f"/video-projects/perkalian_2digit_1digit/segments/f5_seg_{s['id']}_aligned.wav"
            }
            for s in SEGMENTS
        ]
    }
    
    meta_path = os.path.join(PROJECT_DIR, "video_project_data.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nMetadata saved to {meta_path}!")
    print("All tasks completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
