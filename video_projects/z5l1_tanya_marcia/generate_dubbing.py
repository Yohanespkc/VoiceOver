#!/usr/bin/env python3
"""
Generate Synchronized Marcia VoiceOver for Tanya Marcia (Zone 5 Level 1 - Pembagian)
Video Source: Data VIdeo Marcia/z5l1_tanya_marcia.mp4 (22.89s)
Dubbing Character: Guru Marcia (Trainer Marcia Asli)
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

VIDEO_INPUT = os.path.join(BASE_DIR, "Data VIdeo Marcia", "z5l1_tanya_marcia.mp4")
PROJECT_VIDEO_COPY = os.path.join(PROJECT_DIR, "clip_tanya_marcia.mp4")

REF_AUDIO = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
REF_TEXT = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."

TOTAL_DURATION = 22.89

SEGMENTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 3.40,
        "visual": "Judul 'Kaitan Pembagian dan Perkalian', soal 2 x 3 = 6 dan 6 : 2 = ? tampil",
        "original_text": "ketika kita hendak menghitung 6 bagi 2",
        "marcia_text": "Ketika kita hendak menghitung enam bagi dua,",
        "edge_rate": "+3%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 2,
        "start": 3.40,
        "end": 7.50,
        "visual": "Persamaan 2 x 3 = 6 menyala, menghubungkan perkalian dengan pembagian",
        "original_text": "sama saja dengan bertanya 2 kali berapa sama dengan 6",
        "marcia_text": "sama saja dengan bertanya, dua kali berapa sama dengan enam.",
        "edge_rate": "+4%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 3,
        "start": 7.50,
        "end": 9.60,
        "visual": "Angka 3 pada 6 : 2 = 3 menyala warna kuning emas",
        "original_text": "Jawabnya 3",
        "marcia_text": "Jawabnya: tiga!",
        "edge_rate": "+0%",
        "edge_pitch": "+3Hz"
    },
    {
        "id": 4,
        "start": 9.80,
        "end": 11.90,
        "visual": "Transisi ke latihan kedua",
        "original_text": "Wah, menarik sekali",
        "marcia_text": "Wah, menarik sekali!",
        "edge_rate": "+2%",
        "edge_pitch": "+4Hz"
    },
    {
        "id": 5,
        "start": 12.00,
        "end": 14.50,
        "visual": "Soal baru 12 : 3 = ? tampil di layar",
        "original_text": "12 bagi 3",
        "marcia_text": "Dua belas bagi tiga...",
        "edge_rate": "+2%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 6,
        "start": 14.80,
        "end": 20.60,
        "visual": "Rumus kaitan 3 x ? = 12 dan 12 : 3 = ? tampil berdampingan",
        "original_text": "Mudah, Kak. Saya hanya pikir saja 3 kali berapa sama dengan 12",
        "marcia_text": "Mudah, Kak! Saya hanya pikir saja, tiga kali berapa sama dengan dua belas.",
        "edge_rate": "+3%",
        "edge_pitch": "+2Hz"
    },
    {
        "id": 7,
        "start": 20.80,
        "end": 22.88,
        "visual": "Muncul kesimpulan jawaban 4",
        "original_text": "Jawabnya 4",
        "marcia_text": "Jawabnya: empat!",
        "edge_rate": "+2%",
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
    print("\n--- 1. Generating Edge-TTS Studio Segments (id-ID-GadisNeural) ---")
    for seg in SEGMENTS:
        sid = seg["id"]
        target_dur = seg["end"] - seg["start"]
        raw_mp3 = os.path.join(SEGMENTS_DIR, f"edge_seg_{sid}_raw.mp3")
        aligned_wav = os.path.join(SEGMENTS_DIR, f"edge_seg_{sid}_aligned.wav")
        
        comm = edge_tts.Communicate(
            text=seg["marcia_text"],
            voice="id-ID-GadisNeural",
            rate=seg.get("edge_rate", "+2%"),
            pitch=seg.get("edge_pitch", "+2Hz")
        )
        await comm.save(raw_mp3)
        
        raw_dur = get_audio_duration(raw_mp3)
        tempo = raw_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.85, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)
        
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
        tempo = raw_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.85, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)
        
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
    print(f"\n--- 3. Assembling Master {TOTAL_DURATION}s Audio ({mode.upper()}) ---")
    out_wav = os.path.join(PROJECT_DIR, f"master_dubbing_{mode}.wav")
    out_mp3 = os.path.join(PROJECT_DIR, f"master_dubbing_{mode}.mp3")
    
    silence_wav = os.path.join(SEGMENTS_DIR, f"silence_{int(TOTAL_DURATION)}s.wav")
    cmd_silence = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(TOTAL_DURATION), "-c:a", "pcm_s16le", silence_wav
    ]
    subprocess.run(cmd_silence, capture_output=True, check=True)
    
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
    
    full_mix = "".join(mix_labels)
    filter_parts.append(f"{full_mix}amix=inputs={len(mix_labels)}:duration=first:dropout_transition=0,volume={len(mix_labels)}[outa]")
    filter_complex = ";".join(filter_parts)
    
    cmd_mix = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-t", str(TOTAL_DURATION),
        "-c:a", "pcm_s16le",
        out_wav
    ]
    subprocess.run(cmd_mix, capture_output=True, check=True)
    
    cmd_mp3 = [
        "ffmpeg", "-y", "-i", out_wav,
        "-c:a", "libmp3lame", "-b:a", "320k",
        out_mp3
    ]
    subprocess.run(cmd_mp3, capture_output=True, check=True)
    
    dur = get_audio_duration(out_wav)
    print(f"  Master {mode.upper()} track: {dur:.2f}s -> {out_wav}")
    return out_wav

def mux_video_with_dubbing(audio_wav: str, mode: str = "edge") -> str:
    print(f"\n--- 4. Muxing Dubbed Video ({mode.upper()}) ---")
    out_video = os.path.join(PROJECT_DIR, f"video_dubbed_marcia_{mode}.mp4")
    
    # Copy project video input
    if not os.path.exists(PROJECT_VIDEO_COPY):
        shutil.copyfile(VIDEO_INPUT, PROJECT_VIDEO_COPY)
        
    cmd = [
        "ffmpeg", "-y",
        "-i", PROJECT_VIDEO_COPY,
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
    print(f"  Dubbed MP4: {dur:.2f}s -> {out_video}")
    return out_video

async def main():
    print("==================================================================")
    print("  PROYEK VIDEO: Z5L1 TANYA MARCIA PEMBAGIAN DUBBING MARCIA        ")
    print("==================================================================")
    
    # Copy original video
    if not os.path.exists(PROJECT_VIDEO_COPY):
        shutil.copyfile(VIDEO_INPUT, PROJECT_VIDEO_COPY)
        
    # 1. Edge-TTS Studio
    await generate_edge_segments()
    edge_master = assemble_master_track("edge")
    mux_video_with_dubbing(edge_master, "edge")
    
    # 2. F5-TTS Cloned Voice
    try:
        generate_f5_segments()
        f5_master = assemble_master_track("f5")
        mux_video_with_dubbing(f5_master, "f5")
    except Exception as e:
        print(f"Warning F5 generation: {e}")
        
    # 3. Save Project Metadata
    data = {
        "title": "Tanya Marcia: Zone 5 Level 1 (Kaitan Pembagian & Perkalian)",
        "source_url": "Data VIdeo Marcia/z5l1_tanya_marcia.mp4",
        "duration_seconds": TOTAL_DURATION,
        "original_character": "Tutor Tanya Marcia (Original)",
        "dubbed_character": "Guru Marcia (Trainer Marcia Asli)",
        "files": {
            "original_video": "/video-projects/z5l1_tanya_marcia/clip_tanya_marcia.mp4",
            "original_audio": "/video-projects/z5l1_tanya_marcia/original_audio.wav",
            "dubbed_video_edge": "/video-projects/z5l1_tanya_marcia/video_dubbed_marcia_edge.mp4",
            "dubbed_audio_edge": "/video-projects/z5l1_tanya_marcia/master_dubbing_edge.mp3",
            "dubbed_video_f5": "/video-projects/z5l1_tanya_marcia/video_dubbed_marcia_f5.mp4",
            "dubbed_audio_f5": "/video-projects/z5l1_tanya_marcia/master_dubbing_f5.mp3"
        },
        "segments": [
            {
                "id": s["id"],
                "start": s["start"],
                "end": s["end"],
                "visual": s["visual"],
                "prof_text": s["original_text"],
                "marcia_text": s["marcia_text"],
                "audio_edge": f"/video-projects/z5l1_tanya_marcia/segments/edge_seg_{s['id']}_aligned.wav",
                "audio_f5": f"/video-projects/z5l1_tanya_marcia/segments/f5_seg_{s['id']}_aligned.wav"
            }
            for s in SEGMENTS
        ]
    }
    
    meta_path = os.path.join(PROJECT_DIR, "video_project_data.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Metadata berhasil disimpan di {meta_path}!")
    print("Sprint selesai dengan sukses!")

if __name__ == "__main__":
    asyncio.run(main())
