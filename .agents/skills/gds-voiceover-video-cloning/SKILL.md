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

Gunakan runner script otomatis [`sprint_video_dubbing.sh`](file:///Users/yohanessurya/Documents/Development/VoiceOver/sprint_video_dubbing.sh) atau skrip sprint individual:

### A. Dari Video YouTube
```bash
./sprint_video_dubbing.sh \
  --url "https://www.youtube.com/watch?v=t630efAuHPU" \
  --start 0 \
  --duration 36 \
  --voice "so_yosu" \
  --project-name "perkalian_2digit_1digit"
```

### B. Dari Berkas Video MP4 Lokal
```bash
./sprint_video_dubbing.sh \
  --video "Hasil/videoMarcia/z1_bilangan/z1l1_sb1bermain1_Z1L1TB2AB2-1F_54s.mp4" \
  --start 0 \
  --duration 54 \
  --voice "so_marcia" \
  --project-name "sprint_03_z1l1_bilangan_54s"
```

---

## 3. SOP Standar 5 Fase Video Dubbing

### Fase 1: Ingest & Pemotongan Presisi Video
1. Unduh format video terbaik:
   ```bash
   yt-dlp --no-playlist -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o source.mp4 "<URL>"
   ```
2. Potong rentang waktu yang diinginkan dengan re-encoding video H.264:
   ```bash
   ffmpeg -y -ss 00:00:00 -t 54 -i source.mp4 -c:v libx264 -c:a aac clip_original.mp4
   ```
3. Ekstrak audio referensi asli ke WAV 24,000 Hz Mono (standar ASR & DiT):
   ```bash
   ffmpeg -y -i clip_original.mp4 -vn -ar 24000 -ac 1 original_audio_24k.wav
   ```

---

### Fase 2: Transkripsi Whisper & Penyelarasan Gerakan Tulisan (Visual Cues)
1. Jalankan Whisper (`small` atau `medium`) dengan parameter `word_timestamps=True`:
   ```python
   import whisper
   model = whisper.load_model("medium")
   result = model.transcribe("original_audio_24k.wav", language="id", word_timestamps=True)
   ```
2. Ekstrak frame visual (1 fps) untuk mencocokkan momen coretan pena/tangan:
   ```bash
   ffmpeg -y -i clip_original.mp4 -vf "fps=1" frames/frame_%02d.jpg
   ```
3. Identifikasi titik kunci tulisan (penulisan angka nilai tempat, penarikan garis penghubung, penulisan hasil, penunjukan kartu bilangan).

---

### Fase 3: Sintesis Suara Karakter (F5-TTS & Edge-TTS)

#### A. Optimasi Caching Frasa Unik (*Unique Phrase Caching*)
* Jika video memiliki banyak segmen berulang (misal pada drill mencongak 27 kartu angka):
  1. Kumpulkan daftar kalimat unik: `unique_phrases = sorted(list(set(item[3] for item in RAW_SEGMENTS)))`.
  2. Sintesis F5-TTS **hanya sekali** untuk setiap kalimat unik.
  3. Pangkas silence awal & akhir (`librosa.effects.trim(y, top_db=25)`).
  4. Manfaat: Menghemat waktu pemrosesan GPU hingga **66%** (misal 9 sintesis alih-alih 27 sintesis).

#### B. Parameter F5-TTS Kualitas Tinggi (Anti-Pitch Overshoot)
* **Model**: `F5TTS_v1_Base` (Wajib! Mencegah white noise).
* **Audio Ref**: `assets/cloned_voices/at_marcia_ref.wav` (Trainer Marcia wanita autentik).
* **Ref Text**: *"Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."*
* **Parameter**: `nfe_step=32`, `speed=1.05` untuk kestabilan nada vokal mezzo-soprano (~261 Hz).

#### C. Edge-TTS Studio Alternative (Zero Noise)
* Generate alternatif instan tanpa noise menggunakan model studio:
  ```python
  import edge_tts
  comm = edge_tts.Communicate(text=text, voice="id-ID-GadisNeural", rate="+4%", pitch="+2Hz")
  await comm.save(edge_raw)
  ```

---

### Fase 4: Perakitan Master Timeline Tanpa Jeda Geser
1. Buat kanvas audio hening (*silent track*) sepanjang durasi video (misal 54.00s):
   ```bash
   ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t 54.00 silence.wav
   ```
2. Pasang setiap segmen audio pada stempel waktu mulai yang tepat menggunakan filter `adelay` absolut milidetik dan gabungkan dengan `amix`:
   ```bash
   ffmpeg -y -i silence.wav -i seg1.wav -i seg2.wav ... \
     -filter_complex "[1:a]adelay=0|0[d1];[2:a]adelay=1850|1850[d2];[0:a][d1][d2]amix=inputs=3:duration=first:dropout_transition=0,volume=3.0[outa]" \
     -map "[outa]" -t 54.00 master_dubbing.wav
   ```

---

### Fase 5: Muxing Video MP4 & Integrasi Antarmuka Web
1. **Muxing Eksplisit Dual Stream**:
   ```bash
   ffmpeg -y -i clip_original.mp4 -i master_dubbing.wav \
     -map 0:v:0 -map 1:a:0 \
     -c:v copy -c:a aac -b:a 192k \
     -shortest -movflags +faststart video_dubbed.mp4
   ```
   *Wajib menyertakan `-map 0:v:0 -map 1:a:0` agar FFmpeg tidak memilih audio rekaman sumber asli secara otomatis.*

2. **Metadata & Antarmuka Studio SO**:
   * Simpan metadata ke `video_projects/<project_name>/video_project_data.json`.
   * Akses melalui antarmuka web tab **`🎬 /Proyek Video`** di `http://localhost:8765/#/proyek-video`.

---

## 4. Daftar Proyek Sprint Video Dubbing Resmi

| ID Sprint | Judul Modul | Durasi | Sumber Asli | Karakter Dubbing | Jumlah Segmen |
|---|---|---|---|---|---|
| **`perkalian_2digit_1digit`** | Perkalian 2 Digit x 1 Digit (Sprint 01) | 36.00s | YouTube GASING | Prof. Yohanes Surya (`prof_yosu_asli`) | 8 Segmen Coretan |
| **`z5l1_tanya_marcia`** | Tanya Marcia Pembagian (Sprint 02) | 22.00s | Tutor John (Game SO) | Guru Marcia (`so_marcia`) | 7 Segmen Dialog |
| **`sprint_03_z1l1_bilangan_54s`** | Mengenal Bilangan 6–10 (Sprint 03) | 54.00s | Tutor John (Game SO) | Guru Marcia Autentik (`so_marcia`) | 27 Segmen Kartu Pola |

---

## 5. Troubleshooting Cepat Video Dubbing

| Masalah | Penyebab | Solusi |
|---|---|---|
| **Video tetap bersuara asli setelah dubbing** | Perintah muxing tidak menetapkan `-map` secara eksplisit | Gunakan `-map 0:v:0 -map 1:a:0` |
| **Suara terdengar melengking/cempreng pada frasa pendek** | Jendela durasi sempit membuat DiT melonjakkan nada $F_0$ | Gunakan `nfe_step=32`, `speed=1.05`, dan pangkas silence dengan librosa |
| **Suara terasa mendem / artikulasi hilang** | Penggunaan `afftdn=nf=-28` memotong frekuensi >1.500 Hz | Gunakan filter siar `highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10` |
| **Generasi 20+ segmen memakan waktu lama** | Model difusi dipanggil berulang kali untuk frasa yang sama | Terapkan *Unique Phrase Caching* (3x lebih cepat) |
