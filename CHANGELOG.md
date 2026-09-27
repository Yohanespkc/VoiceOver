# 📜 Catatan Rilis & Riwayat Perubahan (Changelog)

Format dokumen ini mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/id-ID/1.0.0/) dan penomoran versi semantik.

## [2.7.0] - 2026-09-27

### ✨ Ditambahkan
* **Suite Video Dubbing Lengkap Zona 5 Level 3 - 6 (Pembagian GASING Tingkat Lanjut - 7 Video)**:
  * **Video 3a: `zone 5 level 3a.mp4` -> `z5l3a_pembagian_3digit_1digit_873_bagi_3`** (46.00s, 7 segmen):
    * Pembagian 3 digit dengan 1 digit: $873 : 3 = 291$ (8 ratusan bagi 3 dapat 2 sisa 2, 27 puluhan bagi 3 dapat 9, 3 satuan bagi 3 dapat 1).
    * Kompresi ringan: 4.88 MB -> 454 KB (MP4) / 442 KB (WebM), hemat **90.9%**.
  * **Video 3b: `zona 5 level 3b.mp4` -> `z5l3b_pembagian_bersisa_167_bagi_4`** (58.00s, 9 segmen):
    * Pembagian 3 digit dengan 1 digit bersisa: $167 : 4 = 41$ sisa 3 (16 puluhan bagi 4 dapat 4, 7 satuan bagi 4 dapat 1 sisa 3).
    * Kompresi ringan: 6.27 MB -> 580 KB (MP4) / 545 KB (WebM), hemat **90.9%**.
  * **Video 3c: `zona 5 level 3c.mp4` -> `z5l3c_pembagian_puluhan_nol_818_bagi_8`** (59.50s, 11 segmen):
    * Pembagian kasus krusial puluhan nol: $818 : 8 = 102$ sisa 2 (8 ratusan bagi 8 dapat 1, 1 puluhan bagi 8 tidak cukup tulis 0 sisa 1, 18 satuan bagi 8 dapat 2 sisa 2).
    * Kompresi ringan: 6.32 MB -> 590 KB (MP4) / 555 KB (WebM), hemat **90.8%**.
  * **Video 4a: `zona 5 level 4a.mp4` -> `z5l4a_pembagian_pembagi_11_453_bagi_11`** (96.00s, 14 segmen):
    * Pembagian dengan pembagi 2 digit (tabel perkalian 11): $453 : 11 = 41$ sisa 2.
    * Kompresi ringan: 10.42 MB -> 946 KB (MP4) / 885 KB (WebM), hemat **91.1%**.
  * **Video 4b: `zona 5 level 4b.mp4` -> `z5l4b_pembagian_pembagi_15_2345_bagi_15`** (107.00s, 19 segmen):
    * Pembagian 4 digit dengan pembagi 15 (tabel kelipatan 15): $2345 : 15 = 156$ sisa 5.
    * Kompresi ringan: 11.58 MB -> 1.05 MB (MP4) / 1.01 MB (WebM), hemat **91.1%**.
  * **Video 5: `zona 5 level 5.mp4` -> `z5l5_trik_pembagian_cepat_10_100_1000`** (192.00s, 30 segmen - Video Baru Lengkap):
    * Trik pembagian super cepat GASING lengkap: bagi 10 (450 : 10 = 45), bagi 100 (7800 : 100 = 78), bagi 5 ($\times 2 : 10 \rightarrow 4775 : 5 = 955$), bagi 25 ($\times 4 : 100 \rightarrow 4775 : 25 = 191$), bagi 125 ($\times 8 : 1000 \rightarrow 5125 : 125 = 41$), bagi 250 ($\times 4 : 1000 \rightarrow 3250 : 250 = 13$), serta aturan krusial penyesuaian sisa pembagian (4776 : 25 = 191 sisa 1, bukan sisa 4).
    * Kompresi ringan: 12.92 MB -> 1.89 MB (MP4) / 2.05 MB (WebM), hemat **85.4%**.
  * **Video 6: `zone 5 level 6.mp4` -> `z5l6_pembagian_pembagi_3digit_38273_bagi_121`** (105.00s, 13 segmen):
    * Pembagian bilangan besar dengan pembagi 3 digit: $38273 : 121 = 316$ sisa 37 menggunakan tabel bantu perkalian 121.
    * Kompresi ringan: hemat ~90% dengan visual dan audio jernih.

### 🛡️ Standar Kualitas & Penyempurnaan Sistem
* **100% Zero Truncation (Anti Syllable Cut)**:
  * Semua segmen penutup dieksekusi tanpa batas paksa `-t` FFmpeg, menjamin seluruh suku kata kalimat penutup ("hasilnya tiga ratus enam belas, sisanya tiga puluh tujuh", "sisanya lima", dll.) terdengar tuntas alami.
  * Durasi video diperpanjang dengan freeze frame kloning (`tpad=stop_mode=clone`) selama 2.5 hingga 8.3 detik agar papan tulis dapat diamati dan diserap siswa.
* **Canvas Widescreen 16:9 Murni Putih (#FFFFFF)**:
  * Penerapan rantai scaling `scale=928:696,pad=1280:720:176:0:color=white` di seluruh 7 video.
  * Bebas dari border hitam (pillarbox) dan memberikan ruang bawah ~109 piksel sehingga kontrol pemutar video tidak pernah menabrak tulisan tangan materi.
* **Pelafalan Angka Fonetik Akurat 100%**:
  * Seluruh angka, puluhan, ratusan, ribuan, dan sisa dieja kata demi kata dalam bahasa Indonesia baku tanpa singkatan ("tiga puluh delapan ribu dua ratus tujuh puluh tiga", "seratus dua puluh satu", dsb.) untuk mencegah halusinasi angka pada model TTS.
* **Sinkronisasi Otomatis 4 Arah**:
  * Distribusi langsung ke folder pengguna `Data VIdeo Marcia/` (`*_ringan.mp4`), repositori arsip `Hasil/videoMarcia/z5_pembagian/` (MP4 & WebM), Web Studio `/Proyek Video` (`video_projects/`), serta modul pembelajaran Sacred Octagon (`so/web/public/assets/videos/z5l3/`, `z5l4/`, `z5l5/`, `z5l6/`).

## [2.6.1] - 2026-09-27

### 🛠️ Perbaikan & Penyempurnaan Visual (Zona 5 Level 1)
* **Penyelesaian Audio Akhir 100% Utuh & Bebas Terpotong (Zero Truncation)**:
  * Memperbaiki durasi target segmen terakhir Video 1c (`18 : [ ] = 6`) dari 4.60s menjadi 6.00s (start 68.40s, end 74.40s) dan menghapus pemotongan `-t` pada segmen penutup.
  * Kalimat penutup *"Dan delapan belas ini adalah jumlah seluruh benda yang ada di dalam semua kotak itu"* kini tersampaikan 100% utuh tanpa pemotongan suku kata *"kotak itu"*.
* **Penambahan Freeze Frame Akhir (2.6 - 3.7 Detik)**:
  * Menggunakan filter `tpad=stop_mode=clone` untuk menahan frame papan tulis yang sudah lengkap:
    * **1a**: diperpanjang dari 61.77s ke **64.50s** (freeze frame 2.73s).
    * **1b**: diperpanjang dari 11.37s ke **14.00s** (freeze frame 2.63s).
    * **1c**: diperpanjang dari 73.43s ke **77.00s** (freeze frame 3.69s).
  * Video tidak lagi berhenti mendadak tepat saat suara selesai, memberikan waktu bagi penonton untuk menyerap ringkasan materi.
* **Canvas Widescreen 16:9 Murni Putih (#FFFFFF) & Bebas Border Hitam**:
  * Mengaplikasikan rantai filter FFmpeg `scale=928:696,pad=1280:720:176:0:color=white` pada video 1a, 1b, dan 1c.
  * Menghilangkan warna hitam (pillarbox / letterbox) di seluruh sisi video saat diputar pada rasio layar 16:9 standar.
  * Memberikan margin bawah putih sebesar ~109 piksel sehingga kontrol navigasi pemutar video (play/pause bar, slider waktu) tidak lagi menutupi tulisan tangan *"banyak kotak"* dan *"Isi tiap kotak"*.
* **Pembaruan Container Pemutar Video (Web & PWA)**:
  * Mengubah container pemutar video di [`VoiceOver/index.html`](file:///Users/yohanessurya/Documents/Development/VoiceOver/index.html) dari `bg-black` / `bg-slate-950` menjadi `bg-white`.
  * Memperbarui antarmuka modal video Marcia di repositori Sacred Octagon (`so/web/src/data/marciaVideoRegistry.ts`) dengan container `bg-white` serta kontrol transparan yang tidak menggelapkan papan tulis.

## [2.6.0] - 2026-09-27

### ✨ Ditambahkan
* **Suite Video Dubbing Zona 5 Level 1 (Pembagian Dasar GASING - 3 Video)**:
  * **Video 1a: `zona 5 level 1a.mp4` -> `z5l1a_pembagian_konkret_8_bagi_2`** (61.77s):
    * Penjelasan pembagian konkret 8 benda dibagi adil ke dalam 2 kotak (tiap kotak 4 benda) dan mencongak dengan relasi perkalian $2 \times [\,] = 8$.
    * 11 segmen ucapan fonetik lengkap dieksekusi dengan F5-TTS Trainer Marcia asli dan Edge-TTS Studio.
    * Kompresi ringan: 2.8 MB -> 565 KB (MP4) / 532 KB (WebM), hemat **80.0%**.
  * **Video 1b: `zona 5 level 1b.mp4` -> `z5l1b_mencongak_54_bagi_6`** (11.37s):
    * Mencongak pembagian $54 : 6 = 9$ melalui relasi $6 \times [\,] = 54$.
    * 3 segmen ucapan fonetik penuh tanpa mumbling.
    * Kompresi ringan: 368 KB -> 95 KB (MP4) / 78 KB (WebM), hemat **74.2%**.
  * **Video 1c: `zona 5 level 1c.mp4` -> `z5l1c_mencari_kotak_18_bagi_berapa`** (73.43s):
    * Pembagian mencari banyaknya kotak ($18 : [\,] = 6$) dengan simulasi memasukkan 6 benda per kotak dan penegasan struktur perkalian ($3 \times 6 = 18$).
    * 15 segmen ucapan fonetik lengkap dengan tempo presisi coretan visual.
    * Kompresi ringan: 3.5 MB -> 675 KB (MP4) / 647 KB (WebM), hemat **80.9%**.
* **Skrip Otomasi Sprint Zona 5**:
  * Pembuatan [`execute_zona5_level1_sprint.py`](file:///Users/yohanessurya/Documents/Development/VoiceOver/execute_zona5_level1_sprint.py) yang mengorkestrasi 5 fase dubbing, ekstraksi thumbnail scrubber, perakitan master WAV 44.1kHz, dan sinkronisasi 4 arah.
* **Sinkronisasi Multi-Tujuan Otomatis**:
  * `Data VIdeo Marcia/` (`*_ringan.mp4`).
  * `Hasil/videoMarcia/z5_pembagian/` (MP4 & WebM).
  * `video_projects/` (terdaftar di Web Studio `/Proyek Video`).
  * Repositori game Sacred Octagon: `/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z5l1/`.

---

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
