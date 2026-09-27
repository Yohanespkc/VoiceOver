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

2. **Kompresi Ringan Web-Ready & Dual Format (MP4 + WebM)**:
   * **MP4 (H.264 tune animation)**:
     ```bash
     ffmpeg -y -i input_master.mp4 -c:v libx264 -preset slow -crf 28 -tune animation -pix_fmt yuv420p \
       -c:a aac -b:a 48k -ac 1 -ar 44100 -movflags +faststart output_ringan.mp4
     ```
   * **WebM (VP9 / Opus)**:
     ```bash
     ffmpeg -y -i input_master.mp4 -c:v libvpx-vp9 -crf 36 -b:v 0 \
       -c:a libopus -b:a 48k -ar 48000 output_ringan.webm
     ```
   * *FastStart* (`-movflags +faststart`) memindahkan metadata moov atom ke awal berkas untuk playback streaming instan di browser/PWA.

3. **Integritas Video Track 100% (Larangan Artificial Cropping)**:
   * Dilarang melakukan crop paksa, masking kotak, atau zoom parsial yang berisiko memotong tulisan rumus di sudut layar. Gunakan resolusi asli video sumber dengan pengkodean ulang efisien.

4. **Penyesuaian Durasi Segmen Presisi (*atempo Chaining*)**:
   * Filter `atempo` FFmpeg memiliki batas minimal 0.5x dan maksimal 2.0x per filter.
   * Untuk penyesuaian di luar batas tersebut, susun secara berantai (*chained*):
     ```python
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
     ```

5. **Metadata & Antarmuka Studio SO**:
   * Simpan metadata ke `video_projects/<project_name>/video_project_data.json`.
   * Akses melalui antarmuka web tab **`🎬 /Proyek Video`** di `http://localhost:8765/#/proyek-video`.

---

## 4. Daftar Proyek Sprint Video Dubbing Resmi

| ID Sprint / Modul | Judul Modul | Durasi | Sumber Asli | Karakter Dubbing | Segmen | Integrasi SO |
|---|---|---|---|---|---|---|
| **`perkalian_2digit_1digit`** | Perkalian 2D x 1D (Sprint 01) | 36.00s | YouTube GASING | Prof. Yohanes Surya | 8 Coretan | Studio |
| **`z5l1_tanya_marcia`** | Tanya Marcia Pembagian (Sprint 02) | 22.00s | Tutor John | Guru Marcia | 7 Dialog | Studio |
| **`sprint_03_z1l1_bilangan_54s`** | Mengenal Bilangan 6–10 (Sprint 03) | 54.00s | Tutor John | Guru Marcia | 27 Pola | Studio |
| **`z4l3_1_pengurangan_2d_1d_tanpa_meminjam`** | Z4L3.1: 2D - 1D Tanpa Meminjam (45-3=42) | 19.93s | Guru Asli | Guru Marcia | 3 Segmen | `z4l3sb1bermain2` |
| **`z4l3_2_pengurangan_puluhan_murni_1d`** | Z4L3.2: Puluhan Murni - 1D (40-7=33) | 25.57s | Guru Asli | Guru Marcia | 6 Segmen | `z4l3sb1bermain1` |
| **`z4l3_3_pengurangan_belasan_1d`** | Z4L3.3: Belasan - 1D (12-3=9, 15-9=6) | 40.43s | Guru Asli | Guru Marcia | 9 Segmen | `z4l3sb2bermain2` |
| **`z4l3_4_pengurangan_2d_1d_meminjam`** | Z4L3.4: 2D - 1D Meminjam (41-5=36) | 60.67s | Guru Asli | Guru Marcia | 11 Segmen | `z4l3sb2bermain1` |
| **`z4l4_1_pengurangan_2d_2d_tanpa_meminjam`** | Z4L4.1: 2D - 2D Tanpa Meminjam (78-46=32) | 28.77s | Guru Asli | Guru Marcia | 7 Segmen | `z4l4sb1bermain1` |
| **`z4l4_2_pengurangan_puluhan_murni_2d`** | Z4L4.2: Puluhan Murni - 2D (80-34=46) | 73.90s | Guru Asli | Guru Marcia | 14 Segmen | `z4l4sb1bermain2` |
| **`z4l4_3_pengurangan_2d_2d_meminjam`** | Z4L4.3: 2D - 2D Meminjam Tiga Cara (82-49=33) | 98.07s | Guru Asli | Guru Marcia | 17 Segmen | `z4l4sb2bermain1` |
| **`z4l5_1_pengurangan_3d_tanpa_meminjam`** | Z4L5.1: 3D Tanpa Meminjam (389-2, 677-324) | 74.13s | Guru Asli | Guru Marcia | 15 Segmen | `z4l5sb1bermain1` |
| **`z4l5_2a_pengurangan_3d_1d_meminjam`** | Z4L5.2a: 3D - 1D Meminjam (331-9=322) | 90.23s | Guru Asli | Guru Marcia | 17 Segmen | `z4l5sb2bermain1` |
| **`z4l5_2b_pengurangan_3d_2d_meminjam`** | Z4L5.2b: 3D - 2D Meminjam (842-59=783) | 124.97s | Guru Asli | Guru Marcia | 22 Segmen | `z4l5sb2bermain2` |
| **`z4l5_2c_pengurangan_3d_3d_meminjam`** | Z4L5.2c: 3D - 3D Meminjam (842-187=655) | 131.00s | Guru Asli | Guru Marcia | 22 Segmen | `z4l5sb2bermain3` |
| **`z4l6_pengurangan_4d_4d_meminjam`** | Z4L6: 4D - 4D Meminjam Beruntun (8021-1329) | 186.70s | Guru Asli | Guru Marcia | 31 Segmen | `z4l6_marcia` |
| **`z5l1a_pembagian_konkret_8_bagi_2`** | Z5L1a: Pembagian Konkret & Mencongak (8 : 2 = 4) | 64.50s | Guru Asli | Guru Marcia | 11 Segmen (16:9 Putih) | `z5l1a_pembagian_8_bagi_2_marcia` |
| **`z5l1b_mencongak_54_bagi_6`** | Z5L1b: Mencongak Pembagian (54 : 6 = 9) | 14.00s | Guru Asli | Guru Marcia | 3 Segmen (16:9 Putih) | `z5l1b_mencongak_54_bagi_6_marcia` |
| **`z5l1c_mencari_kotak_18_bagi_berapa`** | Z5L1c: Pembagian Mencari Kotak (18 : [ ] = 6) | 77.00s | Guru Asli | Guru Marcia | 15 Segmen (16:9 Putih) | `z5l1c_mencari_kotak_18_bagi_berapa_marcia` |
| **`z5l3a_pembagian_3digit_1digit_873_bagi_3`** | Z5L3a: Pembagian 3D : 1D (873 : 3 = 291) | 46.00s | Guru Asli | Guru Marcia | 7 Segmen (16:9 Putih) | `z5l3a_pembagian_873_bagi_3_marcia` |
| **`z5l3b_pembagian_bersisa_167_bagi_4`** | Z5L3b: Pembagian 3D : 1D Bersisa (167 : 4 = 41 sisa 3) | 58.00s | Guru Asli | Guru Marcia | 9 Segmen (16:9 Putih) | `z5l3b_pembagian_167_bagi_4_marcia` |
| **`z5l3c_pembagian_puluhan_nol_818_bagi_8`** | Z5L3c: Pembagian Puluhan Nol (818 : 8 = 102 sisa 2) | 59.50s | Guru Asli | Guru Marcia | 11 Segmen (16:9 Putih) | `z5l3c_pembagian_818_bagi_8_marcia` |
| **`z5l4a_pembagian_pembagi_11_453_bagi_11`** | Z5L4a: Pembagi 2D / Tabel 11 (453 : 11 = 41 sisa 2) | 96.00s | Guru Asli | Guru Marcia | 14 Segmen (16:9 Putih) | `z5l4a_pembagian_453_bagi_11_marcia` |
| **`z5l4b_pembagian_pembagi_15_2345_bagi_15`** | Z5L4b: Pembagian 4D / Tabel 15 (2345 : 15 = 156 sisa 5) | 107.00s | Guru Asli | Guru Marcia | 19 Segmen (16:9 Putih) | `z5l4b_pembagian_2345_bagi_15_marcia` |
| **`z5l5_trik_pembagian_cepat_10_100_1000`** | Z5L5: Trik Cepat 10, 100, 5, 25, 125, 250 & Sisa | 192.00s | Guru Asli | Guru Marcia | 30 Segmen (16:9 Putih) | `z5l5_trik_pembagian_cepat_marcia` |
| **`z5l6_pembagian_pembagi_3digit_38273_bagi_121`** | Z5L6 (Revisi): Pembagi 3D / Tabel 121 (38273 : 121 = 316 sisa 37) | 123.00s | Guru Asli | Guru Marcia | 26 Segmen (16:9 Putih) | `z5l6_pembagian_38273_bagi_121_marcia` |

---

## 5. Troubleshooting Cepat Video Dubbing

| Masalah | Penyebab | Solusi |
|---|---|---|
| **Video tetap bersuara asli setelah dubbing** | Perintah muxing tidak menetapkan `-map` secara eksplisit | Gunakan `-map 0:v:0 -map 1:a:0` |
| **Suara terdengar melengking/cempreng pada frasa pendek** | Jendela durasi sempit membuat DiT melonjakkan nada $F_0$ | Gunakan `nfe_step=32`, `speed=1.05`, dan pangkas silence dengan librosa |
| **Suara terasa mendem / artikulasi hilang** | Penggunaan `afftdn=nf=-28` memotong frekuensi >1.500 Hz | Gunakan filter siar `highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10` |
| **Generasi 20+ segmen memakan waktu lama** | Model difusi dipanggil berulang kali untuk frasa yang sama | Terapkan *Unique Phrase Caching* (3x lebih cepat) |
| **Kata angka terdengar mumbling / tertukar ("juang")** | Angka mentah dimasukkan tanpa ekspansi fonetik kata | Terapkan `normalize_numbers()` di `gasing_pronunciation.py` |
| **File WAV master membengkak >100MB saat di-push ke GitHub** | Filter `amix` menghasilkan audio 192kHz uncompressed | Wajib sertakan `-ar 44100` pada perakitan WAV master |
| **Goresan tangan tidak pas dengan narasi ucapan** | Estimasi durasi ucapan meleset dari durasi animasi visual | Gunakan `build_atempo_filter` untuk menyelaraskan durasi vokal milidetik |
| **Detik akhir video / kata penutup terpotong** | Segmen akhir dipotong paksa dengan parameter `-t target_dur` dan video selesai mendadak | Jangan berikan `-t` pada segmen terakhir dan tambahkan freeze frame akhir 2.5–3.5s (`tpad=stop_mode=clone:stop_duration=...`) |
| **Border hitam / kontrol player menutupi tulisan bawah papan tulis** | Video 4:3 (1024x768) diletakkan di player 16:9 tanpa padding putih | Terapkan filter canvas 16:9 murni putih `#FFFFFF`: `scale=928:696,pad=1280:720:176:0:color=white` (memberikan margin bawah ~109px agar kontrol player aman) |


