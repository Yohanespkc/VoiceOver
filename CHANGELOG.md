# 📜 Catatan Rilis & Riwayat Perubahan (Changelog)

Format dokumen ini mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/id-ID/1.0.0/) dan penomoran versi semantik.

---

## [2.3.0] - 2026-09-22

### ✨ Ditambahkan
* **Optimasi Kestabilan Vokal Sprint 03**:
  * Peningkatan resolusi kalkulasi ODE difusi vokal dari `nfe_step=16` ke `nfe_step=32` untuk merekonstruksi warna timbre vokal Trainer Marcia secara utuh.
  * Penyetelan kecepatan ucapan alami `speed=1.05` dan integrasi pemangkasan *silence* otomatis menggunakan `librosa.effects.trim(y, top_db=25)`.
  * Rantai pemrosesan siar *broadcast mastering*: `highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10` yang meloloskan frekuensi artikulasi 2.000 Hz – 5.000 Hz tanpa desis (*noise-free*).
* **Pemulihan Audio Acuan Autentik Guru Marcia**:
  * Pemulihan `assets/cloned_voices/at_marcia_ref.wav` ke rekaman spektrum penuh beresolusi tinggi (*Centroid* 1.906 Hz) dan penyelarasan naskah acuan resmi (*"Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."*).
* **Perbaikan Muxing Stream FFmpeg**:
  * Menambahkan `-map 0:v:0 -map 1:a:0` secara eksplisit pada perintah penggabungan video untuk mencegah perilaku default FFmpeg yang mempertahankan audio Tutor John dari berkas sumber.
* **Sinkronisasi Skil Agentik**:
  * Pembaruan menyeluruh `gds-voiceover-f5tts-studio` dan `gds-voiceover-video-cloning` pada repositori lokal maupun konfigurasi global.

### 🐛 Diperbaiki
* Mengatasi masalah lonjakan nada (*short-phrase pitch overshoot*) pada frasa pendek 2–3 kata yang sebelumnya melonjak ke 360–402 Hz menjadi stabil di register asli mezzo-soprano (**264.5 Hz**).
* Mengatasi efek vokal mendem/tumpul akibat pemfilteran denoise spektral yang terlalu agresif (`afftdn=nf=-28`).

---

## [2.2.0] - 2026-09-21

### ✨ Ditambahkan
* **Sprint 03: Video Dubbing Zona 1 Level 1 (54 Detik)**:
  * Penggantian suara Tutor John (Pria) menjadi suara Guru Marcia pada modul Mengenal Bilangan 6 s.d. 10 (`z1l1_sb1bermain1_Z1L1TB2AB2-1F_54s.mp4`).
  * Penyelarasan 27 segmen visual penunjukan kartu mencongak dan pola bilangan.
* **Pipeline Percepatan *Unique Phrase Caching***:
  * Mengidentifikasi 9 kalimat unik dari 27 segmen kartu berulang, menghemat waktu inferensi GPU hingga 66% (hanya membutuhkan 9 generasi).
* **Generasi Video Ganda (Dual Output)**:
  * Generasi simultan untuk versi F5-TTS Cloned Voice dan Edge-TTS Studio (`id-ID-GadisNeural`).

---

## [2.1.0] - 2026-09-21

### ✨ Ditambahkan
* **Antarmuka Web Video Dubbing Studio (`🎬 /Proyek Video`)**:
  * Pemutar video berdampingan dengan sinkronisasi waktu bersamaan (*Dual Sync Playback*).
  * Panel pemilihan proyek video dinamis via REST API `/api/video-project/list` dan `/api/video-project/info`.
  * Switcher instan vokal F5-TTS Cloned Voice vs Edge-TTS Studio.
  * Tabel penanda stempel waktu gerakan tulisan tangan dengan tombol loncat video (*seek*) dan pemutar segmen audio independen.
* **Sprint 01 & Sprint 02**:
  * **Sprint 01**: Modul Perkalian 2 Digit x 1 Digit (36s, Suara Yosu / Prof. Yohanes Surya) dari video YouTube GASING.
  * **Sprint 02**: Modul Tanya Marcia Pembagian (22s, Guru Marcia) dari rekaman game Sacred Octagon.
* **Skrip Otomatisasi Sprint**:
  * [`sprint_video_dubbing.sh`](file:///Users/yohanessurya/Documents/Development/VoiceOver/sprint_video_dubbing.sh) dan [`video_dubbing_sprint.py`](file:///Users/yohanessurya/Documents/Development/VoiceOver/video_dubbing_sprint.py).

---

## [2.0.0] - 2026-09-20

### ✨ Ditambahkan
* **Pemisahan Identitas Karakter Resmi**:
  * Pemisahan tegas antara suara Guru Marcia (Wanita, `so_marcia` / `at_c04618f8`) dan Tutor John (Pria, `at_john`).
  * Penambahan profil suara Suara Yosu (Prof. Yohanes Surya Asli, `prof_yosu_asli` / `so_yosu`).
* **Koleksi Contoh Studio & Panduan Situasional**:
  * Direktori `AT Marcia contoh/`: 12 file audio WAV/MP3 bimbingan remedial, petunjuk nilai tempat, dan explainer konsep matematika GASING.
  * Direktori `Yosu Contoh/`: 12 file audio motivasi kebangsaan, filosofi GASING, dan pengajaran berhitung cepat.
  * Pembaruan katalog soundboard interaktif di `assets/audio_catalog.json` dan `rekomendasi AI/katalog_rekomendasi.json`.

---

## [1.0.0] - 2026-09-18

### 🚀 Peluncuran Awal
* Implementasi dasar VoiceOver Studio SO menggunakan model `Eempostor/F5-TTS-INDO-FINETUNE-V2`.
* Dukungan hardware acceleration Apple Silicon (MPS) dan fallback CUDA/CPU.
* Modul kamus pelafalan dwi-bahasa dan normalisasi angka GASING (`gasing_pronunciation.py`).
* Integrasi alternatif Edge-TTS Studio dan Web Audio API real-time tuner.
