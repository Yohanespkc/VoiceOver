---
name: gds-voiceover-video-cloning
description: Standar resmi arsitektur dan workflow Video Dubbing Sprint VoiceOver SO, kloning suara F5-TTS Indo V2 & Edge-TTS Studio, sinkronisasi presisi gerakan tulisan tangan di layar, analisis stempel waktu ASR Whisper, dan integrasi antarmuka /Proyek Video.
---

# Video Dubbing & Voice Cloning Sprint Standard (VoiceOver SO)

Dokumen ini adalah **pedoman resmi dan SOP operasional** untuk mengeksekusi proyek video dubbing dan kloning suara karakter edukasi GASING / Sacred Octagon (Guru Marcia, Prof. Yohanes Surya, Tutor John, AT Trainers).

---

## 1. Arsitektur Video Dubbing Sprint

Alur kerja otomatisasi video dubbing terbagi menjadi **5 Fase Utama**:

```
[1. Ingest & Cut] ──► [2. ASR & Cues] ──► [3. TTS Synthesis] ──► [4. Timeline Assembly] ──► [5. Mux & Studio]
   yt-dlp / MP4         Whisper Medium       F5-TTS Indo V2          Silent Canvas Mix          H.264 + AAC
   FFmpeg -ss -t       Word Timestamps      Edge-TTS Studio         atempo + loudnorm         /Proyek Video UI
```

---

## 2. Cara Cepat Eksekusi Sprint (CLI Runner)

Gunakan runner script otomatis [`sprint_video_dubbing.sh`](file:///Users/yohanessurya/Documents/Development/VoiceOver/sprint_video_dubbing.sh) atau [`video_dubbing_sprint.py`](file:///Users/yohanessurya/Documents/Development/VoiceOver/video_dubbing_sprint.py):

### A. Dari Video YouTube
```bash
./sprint_video_dubbing.sh \
  --url "https://www.youtube.com/watch?v=t630efAuHPU" \
  --start 0 \
  --duration 36 \
  --voice "so_marcia" \
  --project-name "perkalian_2digit_1digit"
```

### B. Dari Berkas Video MP4 Lokal
```bash
./sprint_video_dubbing.sh \
  --video "assets/videos/modul_hitung.mp4" \
  --start 0 \
  --duration 60 \
  --voice "so_marcia" \
  --project-name "modul_hitung_marcia"
```

### C. Opsi Eksekusi Tambahan
* `--skip-f5`: Hanya gunakan Edge-TTS (id-ID-GadisNeural broadcast nol noise) untuk hasil kilat.
* `--skip-edge`: Hanya gunakan F5-TTS Indo Cloned Voice autentik.

---

## 3. SOP Standar 5 Fase Video Dubbing

### Fase 1: Ingest & Pemotongan Presisi Video
1. Unduh format video terbaik:
   ```bash
   yt-dlp --no-playlist -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o source.mp4 "<URL>"
   ```
2. Potong rentang waktu yang diinginkan dengan re-encoding video H.264:
   ```bash
   ffmpeg -y -ss 00:00:00 -t 36 -i source.mp4 -c:v libx264 -c:a aac clip_36s.mp4
   ```
3. Ekstrak audio referensi asli ke WAV 24,000 Hz Mono (standar ASR & DiT):
   ```bash
   ffmpeg -y -i clip_36s.mp4 -vn -ar 24000 -ac 1 clip_audio_24k.wav
   ```

---

### Fase 2: Transkripsi Whisper & Penyelarasan Gerakan Tulisan (Visual Cues)
1. Jalankan Whisper (`small` atau `medium`) dengan parameter `word_timestamps=True`:
   ```python
   import whisper
   model = whisper.load_model("medium")
   result = model.transcribe("clip_audio_24k.wav", language="id", word_timestamps=True)
   ```
2. Ekstrak frame visual (1 fps) untuk mencocokkan momen coretan pena/tangan:
   ```bash
   ffmpeg -y -i clip_36s.mp4 -vf "fps=1" frames/frame_%02d.jpg
   ```
3. Identifikasi titik kunci tulisan (penulisan angka nilai tempat, penarikan garis penghubung, penulisan hasil).

---

### Fase 3: Sintesis Suara Karakter (F5-TTS & Edge-TTS)
1. **F5-TTS Indo Finetune V2 (`so_marcia`)**:
   - Model: `F5TTS_v1_Base` (Wajib! Jangan gunakan `F5TTS_Base` untuk mencegah desisan).
   - Audio Ref: `assets/cloned_voices/at_marcia_ref.wav` (24kHz Mono, durasi 7.7s).
   - Ref Text: *"Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."*
2. **Penyelarasan Durasi & Ritme (Time-Stretching)**:
   - Hitung rasio tempo: `tempo = durasi_sintesis / durasi_target`.
   - Batasi faktor tempo pada rentang alami `[0.85, 1.35]`.
   - Rangkai filter FFmpeg `atempo` dan normalisasi loudness:
     ```bash
     ffmpeg -y -i raw_seg.wav -af "atempo=1.12,highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=7" -ar 44100 -ac 2 aligned_seg.wav
     ```

---

### Fase 4: Perakitan Master Timeline Tanpa Jeda Geser
1. Buat kanvas audio hening (*silent track*) sepanjang durasi video (misal 36.00s):
   ```bash
   ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t 36.00 silence.wav
   ```
2. Pasang setiap segmen audio pada stempel waktu mulai yang tepat menggunakan filter `adelay` dan gabungkan dengan `amix`:
   ```bash
   ffmpeg -y -i silence.wav -i seg1.wav -i seg2.wav ... \
     -filter_complex "[1:a]adelay=0|0[d1];[2:a]adelay=3800|3800[d2];[0:a][d1][d2]amix=inputs=3:duration=first:dropout_transition=0,volume=3[outa]" \
     -map "[outa]" -t 36.00 master_dubbing.wav
   ```

---

### Fase 5: Muxing Video MP4 & Integrasi Antarmuka Web
1. Muxing video bersih tanpa re-encode video (`-c:v copy`) dengan audio AAC 192kbps:
   ```bash
   ffmpeg -y -i clip_36s.mp4 -i master_dubbing.wav -c:v copy -c:a aac -b:a 192k -shortest video_dubbed_marcia.mp4
   ```
2. **Metadata & Antarmuka Studio SO**:
   - Simpan metadata ke `video_projects/<project_name>/video_project_data.json`.
   - Folder video diakses lewat static mount `/video-projects/` di `server.py`.
   - Tab khusus **`🎬 /Proyek Video`** di antarmuka web menampilkan:
     - Pemutar video komparasi berdampingan (Video Asli vs Video Dubbing).
     - Tombol pemutaran sinkron bersamaan (*Dual Sync Play*).
     - Switcher suara instan (F5-TTS Marcia Cloned vs Edge-TTS Studio).
     - Tabel 8 segmen gerakan tulisan dengan tombol pemutar audio per segmen dan tombol loncat video (*seek*).

---

## 4. Pencegahan Masalah Umum (Troubleshooting)

| Masalah | Penyebab | Solusi |
|---|---|---|
| **Suara mendesis / white noise** | Arsitektur salah diinisialisasi sebagai `F5TTS_Base` | Selalu gunakan `F5TTS_v1_Base` di `f5_engine.py` |
| **Suara tidak pas dengan tulisan** | Waktu awal segmen bergeser akibat akumulasi audio | Selalu gunakan koordinat waktu absolut (`adelay=<milidetik>`) pada kanvas hening |
| **Suara melengking (chipmunk)** | Menggunakan `asetrate` tanpa menghitung sampel rate asli | Gunakan filter `atempo` dan resampling 44,100 Hz standar |
| **Streaming video di browser terputus** | Server web tidak mendukung *range request* HTTP 206 | Gunakan FastAPI `StaticFiles` bawaan pada `/video-projects` |
