#!/usr/bin/env python3
"""
VoiceOver Studio SO — Video Dubbing Sprint CLI
Automated end-to-end pipeline for cloning voice and dubbing educational videos:
1. Ingest (YouTube / Local MP4) & precision cut
2. Speech transcription & timestamp analysis (Whisper)
3. Synchronized voice synthesis (F5-TTS Indo V2 & Edge-TTS)
4. Audio DSP time-stretching & master timeline assembly
5. High-definition MP4 video muxing
6. Automatic registration to VoiceOver Studio SO web app (/Proyek Video)
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

CLONED_VOICES_DIR = os.path.join(BASE_DIR, "assets", "cloned_voices")
VIDEO_PROJECTS_DIR = os.path.join(BASE_DIR, "video_projects")
os.makedirs(VIDEO_PROJECTS_DIR, exist_ok=True)


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


class VideoDubbingSprint:
    def __init__(self, project_name: str, voice_id: str = "so_marcia"):
        self.project_name = project_name
        self.voice_id = voice_id
        self.project_dir = os.path.join(VIDEO_PROJECTS_DIR, project_name)
        self.segments_dir = os.path.join(self.project_dir, "segments")
        os.makedirs(self.segments_dir, exist_ok=True)
        
        self.voice_profile = self._resolve_voice_profile(voice_id)

    def _resolve_voice_profile(self, voice_id: str) -> dict:
        trainers_json = os.path.join(CLONED_VOICES_DIR, "trainers.json")
        if os.path.exists(trainers_json):
            with open(trainers_json, "r", encoding="utf-8") as f:
                trainers = json.load(f)
                for t in trainers:
                    if t.get("id") == voice_id:
                        return t
        
        # Fallback default Marcia
        return {
            "id": "so_marcia",
            "name": "Guru Marcia (Trainer Marcia Asli)",
            "ref_audio": "/assets/cloned_voices/at_marcia_ref.wav",
            "ref_audio_abs": os.path.join(CLONED_VOICES_DIR, "at_marcia_ref.wav"),
            "ref_text": "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."
        }

    def phase_1_ingest(self, url: str = None, input_video: str = None, start: float = 0.0, duration: float = 36.0) -> str:
        print("\n=======================================================")
        print(f"  SPRINT PHASE 1: VIDEO INGESTION & PRECISION CUT")
        print(f"=======================================================")
        
        raw_video = os.path.join(self.project_dir, "source_full.mp4")
        clip_video = os.path.join(self.project_dir, "clip_original.mp4")
        clip_audio = os.path.join(self.project_dir, "clip_audio_24k.wav")
        
        if url:
            print(f"📥 Mengunduh video dari YouTube: {url}")
            cmd_yt = [
                "yt-dlp", "--no-playlist",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o", raw_video,
                url
            ]
            subprocess.run(cmd_yt, check=True)
            src_file = raw_video
        elif input_video and os.path.exists(input_video):
            print(f"📂 Menggunakan video lokal: {input_video}")
            src_file = input_video
        elif os.path.exists(os.path.join(self.project_dir, "clip_36s.mp4")):
            print(f"📂 Menggunakan video yang sudah ada di proyek: clip_36s.mp4")
            return os.path.join(self.project_dir, "clip_36s.mp4")
        else:
            raise FileNotFoundError("Video sumber (URL atau berkas lokal) tidak ditemukan.")

        print(f"✂️ Memotong video dari detik {start} sepanjang {duration}s...")
        cmd_cut = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", src_file,
            "-c:v", "libx264", "-c:a", "aac",
            clip_video
        ]
        subprocess.run(cmd_cut, capture_output=True, check=True)

        # Ekstrak audio mono 24kHz untuk ASR & analisis
        cmd_a = [
            "ffmpeg", "-y", "-i", clip_video,
            "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
            clip_audio
        ]
        subprocess.run(cmd_a, capture_output=True, check=True)
        print(f"✓ Video terpotong siap: {clip_video} ({duration:.2f}s)")
        return clip_video

    def phase_2_transcribe(self, audio_path: str = None) -> list:
        print("\n=======================================================")
        print(f"  SPRINT PHASE 2: SPEECH RECOGNITION & CUE BREAKDOWN")
        print(f"=======================================================")
        if not audio_path or not os.path.exists(audio_path):
            audio_path = os.path.join(self.project_dir, "clip_36s_audio.wav")
            if not os.path.exists(audio_path):
                audio_path = os.path.join(self.project_dir, "clip_audio_24k.wav")

        existing_meta = os.path.join(self.project_dir, "video_project_data.json")
        if os.path.exists(existing_meta):
            print(f"📖 Membaca data segmen yang telah dipetakan sebelumnya dari: {existing_meta}")
            with open(existing_meta, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("segments", [])

        print("🎙️ Menjalankan Whisper Medium ASR dengan word timestamps...")
        import whisper
        model = whisper.load_model("medium")
        res = model.transcribe(audio_path, language="id", word_timestamps=True)
        
        segments = []
        for idx, s in enumerate(res["segments"]):
            segments.append({
                "id": idx + 1,
                "start": round(s["start"], 2),
                "end": round(s["end"], 2),
                "visual": f"Gerakan dan penjelasan konsep segmen {idx + 1}",
                "prof_text": s["text"].strip(),
                "marcia_text": s["text"].strip()
            })
        print(f"✓ Berhasil mengekstrak {len(segments)} segmen ucapan.")
        return segments

    def phase_3_synthesize_f5(self, segments: list) -> None:
        print("\n=======================================================")
        print(f"  SPRINT PHASE 3: F5-TTS INDO CLONING ({self.voice_profile.get('name')})")
        print(f"=======================================================")
        from f5_engine import F5IndoEngine
        engine = F5IndoEngine.get_instance()
        
        ref_audio = self.voice_profile.get("ref_audio_abs")
        ref_text = self.voice_profile.get("ref_text")
        is_marcia = self.voice_id in ["so_marcia", "at_c04618f8", "guru_marcia"]
        synth_speed = 1.05 if is_marcia else 1.0

        # 1. Optimasi GPU: Identifikasi kalimat unik untuk sintesis tunggal (hemat komputasi)
        unique_phrases = sorted(list(set(s["marcia_text"] for s in segments)))
        print(f"⚡ [GPU Saving] Ditemukan {len(segments)} segmen visual dengan {len(unique_phrases)} kalimat unik.")
        
        phrase_cache = {}
        import librosa
        import soundfile as sf

        for idx, phrase in enumerate(unique_phrases):
            cache_file = os.path.join(self.segments_dir, f"cached_f5_{idx+1}.wav")
            print(f"  [{idx+1}/{len(unique_phrases)}] Sintesis frasa unik: \"{phrase}\"...", end="", flush=True)
            t0 = time.time()
            res = engine.generate(
                ref_audio_path=ref_audio,
                ref_text=ref_text,
                gen_text=phrase,
                speed=synth_speed,
                nfe_step=32,
                output_format="wav"
            )
            src_wav = os.path.join(BASE_DIR, res["audio_url"].lstrip("/"))
            
            # Pangkas trailing silence agar durasi ucapan pas
            y, sr = librosa.load(src_wav, sr=24000)
            y_trimmed, _ = librosa.effects.trim(y, top_db=25)
            sf.write(cache_file, y_trimmed, sr)
            phrase_cache[phrase] = cache_file
            print(f" Selesai ({time.time()-t0:.2f}s, durasi aktif: {len(y_trimmed)/sr:.2f}s)")

        # 2. Rangkai ke seluruh segmen dengan mastering siar
        MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"
        for s in segments:
            sid = s["id"]
            target_dur = s["end"] - s["start"]
            base_wav = phrase_cache[s["marcia_text"]]
            aligned_wav = os.path.join(self.segments_dir, f"f5_seg_{sid}_aligned.wav")

            raw_dur = get_audio_duration(base_wav)
            tempo = raw_dur / target_dur if target_dur > 0 else 1.0
            tempo = max(0.85, min(1.30, tempo))
            atempo = build_atempo_filter(tempo)

            cmd_align = [
                "ffmpeg", "-y", "-i", base_wav,
                "-af", f"{atempo},{MASTER_FILTER}",
                "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
                "-t", str(target_dur),
                aligned_wav
            ]
            subprocess.run(cmd_align, capture_output=True, check=True)
            s["audio_f5"] = f"/video-projects/{self.project_name}/segments/f5_seg_{sid}_aligned.wav"

        # 3. Purge alokasi memori GPU
        engine.free_gpu_memory()

    async def phase_3_synthesize_edge(self, segments: list) -> None:
        print("\n=======================================================")
        print(f"  SPRINT PHASE 3B: EDGE-TTS STUDIO ALTERNATIVE (GadisNeural)")
        print(f"=======================================================")
        import edge_tts

        for s in segments:
            sid = s["id"]
            target_dur = s["end"] - s["start"]
            raw_mp3 = os.path.join(self.segments_dir, f"edge_seg_{sid}_raw.mp3")
            aligned_wav = os.path.join(self.segments_dir, f"edge_seg_{sid}_aligned.wav")

            comm = edge_tts.Communicate(
                text=s["marcia_text"],
                voice="id-ID-GadisNeural",
                rate="+3%",
                pitch="+2Hz"
            )
            await comm.save(raw_mp3)

            raw_dur = get_audio_duration(raw_mp3)
            tempo = raw_dur / target_dur if target_dur > 0 else 1.0
            tempo = max(0.85, min(1.35, tempo))
            atempo = build_atempo_filter(tempo)

            cmd_align = [
                "ffmpeg", "-y", "-i", raw_mp3,
                "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
                "-t", str(target_dur),
                aligned_wav
            ]
            subprocess.run(cmd_align, capture_output=True, check=True)
            s["audio_edge"] = f"/video-projects/{self.project_name}/segments/edge_seg_{sid}_aligned.wav"

    def phase_4_assemble_and_mux(self, segments: list, total_duration: float = 36.0) -> dict:
        print("\n=======================================================")
        print(f"  SPRINT PHASE 4: TIMELINE ASSEMBLY & VIDEO MUXING")
        print(f"=======================================================")
        clip_video = os.path.join(self.project_dir, "clip_36s.mp4")
        if not os.path.exists(clip_video):
            clip_video = os.path.join(self.project_dir, "clip_original.mp4")

        results = {}
        for mode in ["f5", "edge"]:
            print(f"  🔨 Menyusun master audio track ({mode.upper()})...")
            out_wav = os.path.join(self.project_dir, f"master_dubbing_{mode}.wav")
            out_mp3 = os.path.join(self.project_dir, f"master_dubbing_{mode}.mp3")
            out_mp4 = os.path.join(self.project_dir, f"video_dubbed_marcia_{mode}.mp4")

            # Silent canvas
            silence_wav = os.path.join(self.segments_dir, f"silence_{int(total_duration)}s.wav")
            cmd_silence = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", str(total_duration), "-c:a", "pcm_s16le", silence_wav
            ]
            subprocess.run(cmd_silence, capture_output=True, check=True)

            inputs = ["-i", silence_wav]
            filter_parts = []
            mix_labels = ["[0:a]"]

            for idx, s in enumerate(segments):
                seg_file = os.path.join(self.project_dir, "segments", f"{mode}_seg_{s['id']}_aligned.wav")
                inputs.extend(["-i", seg_file])
                inp_idx = idx + 1
                delay_ms = int(s["start"] * 1000)
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
                "-t", str(total_duration),
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

            print(f"  🎬 Muxing ke format MP4: {out_mp4}...")
            cmd_mux = [
                "ffmpeg", "-y",
                "-i", clip_video,
                "-i", out_wav,
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                out_mp4
            ]
            subprocess.run(cmd_mux, capture_output=True, check=True)

            results[mode] = {
                "video": f"/video-projects/{self.project_name}/{os.path.basename(out_mp4)}",
                "audio": f"/video-projects/{self.project_name}/{os.path.basename(out_mp3)}"
            }

        return results

    def phase_5_save_metadata(self, segments: list, mux_results: dict, total_duration: float = 36.0, source_url: str = None):
        print("\n=======================================================")
        print(f"  SPRINT PHASE 5: SAVE METADATA & REGISTER TO STUDIO")
        print(f"=======================================================")
        meta_file = os.path.join(self.project_dir, "video_project_data.json")
        
        payload = {
            "title": f"Proyek Video VoiceOver: {self.project_name.replace('_', ' ').title()} (00:00 - {int(total_duration)}s)",
            "source_url": source_url or "https://www.youtube.com/watch?v=t630efAuHPU",
            "duration_seconds": total_duration,
            "original_character": "Prof. Yohanes Surya",
            "dubbed_character": self.voice_profile.get("name", "Guru Marcia"),
            "files": {
                "original_video": f"/video-projects/{self.project_name}/clip_36s.mp4",
                "original_audio": f"/video-projects/{self.project_name}/clip_36s_audio.wav",
                "dubbed_video_edge": mux_results.get("edge", {}).get("video"),
                "dubbed_audio_edge": mux_results.get("edge", {}).get("audio"),
                "dubbed_video_f5": mux_results.get("f5", {}).get("video"),
                "dubbed_audio_f5": mux_results.get("f5", {}).get("audio"),
            },
            "segments": segments
        }

        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"✓ Metadata berhasil disimpan: {meta_file}")
        print(f"🎉 SPRINT COMPLETE! Buka http://localhost:8765/#/proyek-video untuk meninjau hasilnya.")


async def run_sprint(args):
    sprint = VideoDubbingSprint(project_name=args.project_name, voice_id=args.voice)
    
    # 1. Ingest
    clip_path = sprint.phase_1_ingest(
        url=args.url,
        input_video=args.video,
        start=args.start,
        duration=args.duration
    )
    
    # 2. Transcribe & Segments
    segments = sprint.phase_2_transcribe()
    
    # 3. Synthesize
    if not args.skip_f5:
        sprint.phase_3_synthesize_f5(segments)
    if not args.skip_edge:
        await sprint.phase_3_synthesize_edge(segments)
        
    # 4. Assemble & Mux
    mux_res = sprint.phase_4_assemble_and_mux(segments, total_duration=args.duration)
    
    # 5. Save metadata
    sprint.phase_5_save_metadata(segments, mux_res, total_duration=args.duration, source_url=args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VoiceOver Video Dubbing Sprint CLI")
    parser.add_argument("--url", type=str, default=None, help="URL video YouTube")
    parser.add_argument("--video", type=str, default=None, help="Path berkas MP4 video lokal")
    parser.add_argument("--start", type=float, default=0.0, help="Detik awal pemotongan video (default: 0)")
    parser.add_argument("--duration", type=float, default=36.0, help="Durasi video yang dipotong dalam detik (default: 36)")
    parser.add_argument("--voice", type=str, default="so_marcia", help="ID karakter suara untuk kloning (default: so_marcia)")
    parser.add_argument("--project-name", type=str, default="perkalian_2digit_1digit", help="Nama folder proyek di video_projects/")
    parser.add_argument("--skip-f5", action="store_true", help="Lewati generasi F5-TTS jika hanya ingin Edge-TTS")
    parser.add_argument("--skip-edge", action="store_true", help="Lewati generasi Edge-TTS")

    args = parser.parse_args()
    asyncio.run(run_sprint(args))
