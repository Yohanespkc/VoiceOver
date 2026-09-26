# 📜 Catatan Rilis & Riwayat Perubahan (Changelog)

Format dokumen ini mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/id-ID/1.0.0/) dan penomoran versi semantik.

## [2.5.0] - 2026-09-27

### ✨ Ditambahkan
* **Suite Video Dubbing Lengkap Zona 4 (Pengurangan GASING - 12 Video)**:
  * **Level 3 (4 Video)**:
    * `z4l3_1_pengurangan_2d_1d_tanpa_meminjam` (45 - 3 = 42, Pasar Malam India Kuno / `z4l3sb1bermain2_marcia`, 19.93s)
    * `z4l3_2_pengurangan_puluhan_murni_1d` (40 - 7 = 33, Bowling Kuno India / `z4l3sb1bermain1_marcia`, 25.57s)
    * `z4l3_3_pengurangan_belasan_1d` (12 - 3 = 9, 15 - 9 = 6, Rahasia Gua Gelap / `z4l3sb2bermain2_marcia`, 40.43s)
    * `z4l3_4_pengurangan_2d_1d_meminjam` (41 - 5 = 36, Memanah Guci Kerajaan / `z4l3sb2bermain1_marcia`, 60.67s)
  * **Level 4 (3 Video)**:
    * `z4l4_1_pengurangan_2d_2d_tanpa_meminjam` (78 - 46 = 32, `z4l4sb1bermain1`, 28.77s)
    * `z4l4_2_pengurangan_puluhan_murni_2d` (80 - 34 = 46, Cara Biasa & Mencongak, `z4l4sb1bermain2`, 73.90s)
    * `z4l4_3_pengurangan_2d_2d_meminjam` (82 - 49 = 33, Tiga Cara: Pecah, Bersusun, Mencongak, `z4l4sb2bermain1`, 98.07s)
  * **Level 5 (4 Video)**:
    * `z4l5_1_pengurangan_3d_tanpa_meminjam` (389 - 2, 343 - 21, 677 - 324, `z4l5sb1bermain1`, 74.13s)
    * `z4l5_2a_pengurangan_3d_1d_meminjam` (331 - 9 = 322, Tiga Cara, `z4l5sb2bermain1`, 90.23s)
    * `z4l5_2b_pengurangan_3d_2d_meminjam` (842 - 59 = 783, Tiga Cara, `z4l5sb2bermain2`, 124.97s)
    * `z4l5_2c_pengurangan_3d_3d_meminjam` (842 - 187 = 655, Tiga Cara, `z4l5sb2bermain3`, 131.00s)
  * **Level 6 (1 Master Video)**:
    * `z4l6_pengurangan_4d_4d_meminjam` (8021 - 1329 = 6692 & 8223 - 5224 = 2999, Lirik Kanan Beruntun & Kasus Nol di Tengah, 31 Segmen, 186.70s)
* **Normalisasi Angka & Fonetik Penuh (`gasing_pronunciation.py`)**:
  * Penambahan fungsi `number_to_words_id(n)` untuk mengonversi angka ke kata bahasa Indonesia utuh.
  * Penambahan fungsi `normalize_numbers(text)` untuk menormalkan bilangan mandiri, akhiran puluhan (`40-an` -> "empat puluhan", `10-an` -> "sepuluhan"), dan simbol aritmatika (`+`, `-`, `=`, `x`). Meniadakan 100% gumaman (*mumbling* / "juang") pada model difusi.
* **Pipeline Otomatisasi Sprint & Multi-Sync**:
  * Skrip orkestrasi `execute_zona4_level3_sprint.py` s.d. `execute_zona4_level6_sprint.py`.
  * Distribusi otomatis hasil dubbing ke 4 direktori: Berkas ringan, Arsip Hasil, Web Studio `/Proyek Video`, dan proyek game Sacred Octagon (`so/web/public/assets/videos/z4l*/`).
  * Skrip remastering dan tuning presisi: `remaster_zona4_level5.py`, `render_flawless_52c.py`, `update_all_qc_and_remux.py`.
* **Ekspor Ganda Web-Ready (MP4 + WebM)**:
  * Optimasi kompresi animasi: MP4 (H.264 tune animation CRF 28, AAC 48k Mono, FastStart) dan WebM (VP9 CRF 36, Opus).
* **Pembaruan Skil Standar Agentik**:
  * Sinkronisasi lokal dan global untuk `gds-voiceover-f5tts-studio` dan `gds-voiceover-video-cloning`.

### 🐛 Diperbaiki
* Mengatasi masalah lonjakan ukuran file WAV uncompressed pada video panjang (>3 menit) dengan menetapkan `-ar 44100` secara eksplisit pada perakitan master timeline audio (mencegah penolakan ukuran file >100MB di GitHub).
* Mempertahankan integritas video track asli 100% tanpa crop atau masking persegi buatan yang dapat memotong tulisan rumus di sudut visual layar.

---

## [2.4.0] - 2026-09-22

### ✨ Ditambahkan
* **Sistem Penghematan GPU Otomatis (*Auto GPU Saving*)**:
  * *Transparent Disk Phrase Caching*: Penambahan direktori `output/.phrase_cache/` dan hashing cerdas untuk mencegah inferensi ulang pada kalimat yang identik (menghemat 100% GPU / respon instan 0.1s).
  * *Auto VRAM Cache Purge*: Penambahan metode `free_gpu_memory()` yang otomatis memanggil `torch.mps.empty_cache()` (Apple Silicon), `torch.cuda.empty_cache()` (CUDA), dan `gc.collect()` di setiap akhir inferensi.
* **Metode 1-Baris Suara Karakter Autentik**:
  * `engine.generate_marcia(teks)`: Menghubungkan otomatis ke audio acuan autentik Guru Marcia dengan parameter optimal (nfe=32, speed=1.05, trim silence, broadcast mastering) sehingga kolaborator tidak perlu menyetel parameter manual.
  * `engine.generate_yosu(teks)`: Menghubungkan otomatis ke audio acuan Prof. Yohanes Surya asli.
* **Panduan Pengembang & Kolaborator**:
  * Pembuatan dokumen [`COLLABORATOR_GUIDE.md`](file:///Users/yohanessurya/Documents/Development/VoiceOver/COLLABORATOR_GUIDE.md) dan pembaruan `README.md`.
* **Optimasi Pipeline Video Dubbing**:
  * Pembaruan `video_dubbing_sprint.py` dengan *unique phrase caching*, *silence trimming*, dan pembersihan VRAM GPU otomatis.

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
