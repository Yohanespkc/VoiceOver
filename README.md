# 🎙️ VoiceOver Studio — Sacred Octagon & Metode GASING

> **Studio Voice Cloning & Video Dubbing AI Berkecepatan Tinggi untuk Pembelajaran GASING dan Ekosistem Game Sacred Octagon (SO)**

---

## 🌟 Fitur Utama

1. **Voice Cloning Berpresisi Tinggi (F5-TTS Indo Finetune V2)**:
   * Kloning suara berbasis difusi transformer (*Diffusion Transformer - DiT*) `F5TTS_v1_Base` dengan vocoder neural *Vocos Mel 24kHz*.
   * Rekonstruksi warna vokal autentik, desah napas alami, dan nada hangat karakter edukasi Indonesia.
2. **Studio Video Dubbing Sinkron (`🎬 /Proyek Video`)**:
   * Antarmuka web interaktif untuk perbandingan berdampingan (*Dual Sync Video Player*).
   * Penggantian audio vokal instan (*Switcher*: F5-TTS Cloned Voice vs Edge-TTS Studio).
   * Navigasi stempel waktu (*seek*) dan penanda segmen visual tulisan tangan presisi milidetik.
3. **Penyelarasan Tulisan Tangan & Gerakan Visual**:
   * Analisis stempel waktu kata demi kata menggunakan ASR Whisper (`medium` / `small`).
   * *Canvas Audio Assembly*: Menempatkan segmen vokal pada koordinat waktu absolut (`adelay`) tanpa jeda geser (*zero drift*).
4. **Normalisasi Angka Fonetik Penuh (`gasing_pronunciation.py`)**:
   * Konversi otomatis angka bulat, bilangan belasan/puluhan/ratusan/ribuan, serta akhiran puluhan (`40-an` -> "empat puluhan").
   * Meniadakan 100% efek gumaman (*mumbling*) atau pemenggalan kata tidak jelas pada model difusi DiT dan Edge-TTS.
5. **Karakter Suara Resmi**:
   * **Guru Marcia (`so_marcia`)**: Suara asli Trainer Marcia (Wanita, mezzo-soprano ~265 Hz) yang ramah, hangat, dan mendidik.
   * **Prof. Yohanes Surya (`prof_yosu_asli` / `so_yosu`)**: Suara asli Pendiri GASING yang berwibawa, patriotik, dan membakar semangat.
   * **Tutor John (`at_john`)**: Suara tenang Tutor John (Pria, bariton ~89 Hz) pemandu video pembagian.
   * **Studio Broadcast (`guru_marcia_edge`)**: Vokal instan bebas noise 100% menggunakan neural model `id-ID-GadisNeural`.
6. **Ekspor Video Ganda Ringan & Multi-Target Sync**:
   * Kompresi video animasi optimal: MP4 (H.264 CRF 28 tune animation, FastStart) + WebM (VP9 CRF 36, Opus).
   * Distribusi otomatis ke 4 destinasi: Berkas ringan lokal, Arsip Master Hasil, Web Studio `/Proyek Video`, dan repositori PWA game Sacred Octagon.

---

## ⚡ Optimalisasi GPU & Panduan Kolaborator

Proyek ini telah dilengkapi **sistem penghematan GPU otomatis** dan **metode 1 baris** untuk menghasilkan suara Guru Marcia yang 100% mirip dengan rekaman aslinya:
* **`engine.generate_marcia(teks)`**: Otomatis mengunci ke acuan autentik, naskah nilai tempat, $F_0 \approx 264$ Hz (anti-melengking), silence trimming, dan mastering siar.
* **Transparent Phrase Caching**: Menghindari inferensi ulang pada kalimat yang sama (menghemat 100% GPU / waktu respon 0.1s).
* **Auto VRAM Purge**: Otomatis membersihkan alokasi memori PyTorch MPS/CUDA dan garbage collection di setiap generasi (bebas crash OOM).

👉 **Panduan Lengkap Kolaborator**: Silakan pelajari panduan lengkap dan contoh kode di **[COLLABORATOR_GUIDE.md](file:///Users/yohanessurya/Documents/Development/VoiceOver/COLLABORATOR_GUIDE.md)**.

---

## 🎬 Daftar Sprint Video Dubbing Resmi

| Sprint / Modul | Judul & Materi | Durasi | Karakter Dubbing | Segmen | Integrasi Sacred Octagon |
|---|---|---|---|---|---|
| **Sprint 01** | Perkalian 2D x 1D (`perkalian_2digit_1digit`) | 36.00s | Prof. Yohanes Surya | 8 Segmen | Web Studio `/proyek-video` |
| **Sprint 02** | Tanya Marcia Pembagian (`z5l1_tanya_marcia`) | 22.00s | Guru Marcia | 7 Segmen | Web Studio `/proyek-video` |
| **Sprint 03** | Mengenal Bilangan 6–10 (`sprint_03_z1l1_bilangan_54s`) | 54.00s | Guru Marcia Autentik | 27 Segmen | Web Studio `/proyek-video` |
| **Z4L3.1** | Pengurangan 2D - 1D Tanpa Meminjam (45 - 3 = 42) | 19.93s | Guru Marcia | 3 Segmen | `z4l3sb1bermain2` (Pasar Malam India Kuno) |
| **Z4L3.2** | Pengurangan Puluhan Murni - 1D (40 - 7 = 33) | 25.57s | Guru Marcia | 6 Segmen | `z4l3sb1bermain1` (Bowling Kuno India) |
| **Z4L3.3** | Pengurangan Belasan - 1D (12 - 3 = 9, 15 - 9 = 6) | 40.43s | Guru Marcia | 9 Segmen | `z4l3sb2bermain2` (Rahasia Gua Gelap) |
| **Z4L3.4** | Pengurangan 2D - 1D Meminjam (41 - 5 = 36) | 60.67s | Guru Marcia | 11 Segmen | `z4l3sb2bermain1` (Memanah Guci Kerajaan) |
| **Z4L4.1** | Pengurangan 2D - 2D Tanpa Meminjam (78 - 46 = 32) | 28.77s | Guru Marcia | 7 Segmen | `z4l4sb1bermain1` |
| **Z4L4.2** | Puluhan Murni - 2D Cara Biasa & Mencongak (80 - 34 = 46) | 73.90s | Guru Marcia | 14 Segmen | `z4l4sb1bermain2` |
| **Z4L4.3** | Pengurangan 2D - 2D Meminjam Tiga Cara (82 - 49 = 33) | 98.07s | Guru Marcia | 17 Segmen | `z4l4sb2bermain1` |
| **Z4L5.1** | Pengurangan 3D Tanpa Meminjam (389-2, 677-324) | 74.13s | Guru Marcia | 15 Segmen | `z4l5sb1bermain1` |
| **Z4L5.2a** | Pengurangan 3D - 1D Meminjam (331 - 9 = 322) | 90.23s | Guru Marcia | 17 Segmen | `z4l5sb2bermain1` |
| **Z4L5.2b** | Pengurangan 3D - 2D Meminjam (842 - 59 = 783) | 124.97s | Guru Marcia | 22 Segmen | `z4l5sb2bermain2` |
| **Z4L5.2c** | Pengurangan 3D - 3D Meminjam (842 - 187 = 655) | 131.00s | Guru Marcia | 22 Segmen | `z4l5sb2bermain3` |
| **Z4L6** | Pengurangan 4D - 4D Meminjam Beruntun (8021-1329) | 186.70s | Guru Marcia | 31 Segmen | `z4l6_marcia` (Master 186.7s) |
| **Z5L1a** | Pembagian Konkret & Mencongak (8 : 2 = 4) | 64.50s | Guru Marcia | 11 Segmen (16:9 Canvas Putih) | `z5l1a_pembagian_8_bagi_2_marcia` |
| **Z5L1b** | Mencongak Pembagian (54 : 6 = 9) | 14.00s | Guru Marcia | 3 Segmen (16:9 Canvas Putih) | `z5l1b_mencongak_54_bagi_6_marcia` |
| **Z5L1c** | Pembagian Mencari Banyaknya Kotak (18 : [ ] = 6) | 77.00s | Guru Marcia | 15 Segmen (16:9 Canvas Putih) | `z5l1c_mencari_kotak_18_bagi_berapa_marcia` |
| **Z5L3a** | Pembagian 3D : 1D (873 : 3 = 291) | 46.00s | Guru Marcia | 7 Segmen (16:9 Canvas Putih) | `z5l3a_pembagian_873_bagi_3_marcia` |
| **Z5L3b** | Pembagian 3D : 1D Bersisa (167 : 4 = 41 sisa 3) | 58.00s | Guru Marcia | 9 Segmen (16:9 Canvas Putih) | `z5l3b_pembagian_167_bagi_4_marcia` |
| **Z5L3c** | Pembagian Kasus Puluhan Nol (818 : 8 = 102 sisa 2) | 59.50s | Guru Marcia | 11 Segmen (16:9 Canvas Putih) | `z5l3c_pembagian_818_bagi_8_marcia` |
| **Z5L4a** | Pembagian Pembagi 2D / Tabel 11 (453 : 11 = 41 sisa 2) | 96.00s | Guru Marcia | 14 Segmen (16:9 Canvas Putih) | `z5l4a_pembagian_453_bagi_11_marcia` |
| **Z5L4b** | Pembagian 4D / Tabel 15 (2345 : 15 = 156 sisa 5) | 107.00s | Guru Marcia | 19 Segmen (16:9 Canvas Putih) | `z5l4b_pembagian_2345_bagi_15_marcia` |
| **Z5L5** | Trik Cepat Pembagian 10, 100, 5, 25, 125, 250 & Penentuan Sisa | 192.00s | Guru Marcia | 30 Segmen (16:9 Canvas Putih) | `z5l5_trik_pembagian_cepat_marcia` |
| **Z5L6** | Pembagian Pembagi 3D / Tabel 121 (38273 : 121 = 316 sisa 37) | 105.00s | Guru Marcia | 13 Segmen (16:9 Canvas Putih) | `z5l6_pembagian_38273_bagi_121_marcia` |

---

## 📁 Struktur Direktori Proyek

```
VoiceOver/
├── .agents/skills/                   # Panduan & standar arsitektur agentik
│   ├── gds-voiceover-f5tts-studio/   # Standar resmi F5-TTS, DSP siar & fonetik angka
│   └── gds-voiceover-video-cloning/  # SOP resmi 5 fase sprint video dubbing & dual export
├── assets/                           # Aset statis & audio acuan
│   ├── cloned_voices/                # Berkas WAV acuan (at_marcia_ref, yosu_ref, at_john_ref)
│   └── trainers.json                 # Basis data profil suara karakter
├── AT Marcia contoh/                 # 12 Koleksi kasus suara asli Trainer Marcia (Kasus 1–5)
├── Yosu Contoh/                      # 12 Koleksi kasus motivasi & pembelajaran Prof. Yohanes Surya
├── Data VIdeo Marcia/                # Koleksi video sumber rekaman guru & versi ringan
├── Hasil/                            # Berkas video hasil akhir dubbing terintegrasi
│   └── videoMarcia/
│       ├── z1_bilangan/              # Dubbing Zona 1 (Mengenal Bilangan)
│       ├── z4_pengurangan/           # 12 Video Lengkap Zona 4 (MP4 & WebM)
│       └── z5_pembagian/             # Video Pembagian Zona 5 (MP4 & WebM)
├── video_projects/                   # Proyek sprint video dubbing (/Proyek Video)
│   ├── perkalian_2digit_1digit/      # Sprint 01
│   ├── z5l1_tanya_marcia/            # Sprint 02
│   ├── sprint_03_z1l1_bilangan_54s/  # Sprint 03
│   ├── z4l3_1 ... z4l3_4/            # Zona 4 Level 3 (4 Video)
│   ├── z4l4_1 ... z4l4_3/            # Zona 4 Level 4 (3 Video)
│   ├── z4l5_1 ... z4l5_2c/           # Zona 4 Level 5 (4 Video)
│   ├── z4l6_pengurangan_4d_4d/       # Zona 4 Level 6 (Master 4D-4D)
│   └── z5l1a ... z5l1c/              # Zona 5 Level 1 (3 Video Pembagian)
├── f5_engine.py                      # Engine utama F5-TTS Indo V2
├── gasing_pronunciation.py           # Kamus pelafalan, ejaan fonetik & normalisasi angka
├── server.py                         # Backend API FastAPI & server antarmuka web
├── sprint_video_dubbing.sh           # CLI runner otomatisasi sprint video dubbing
├── video_dubbing_sprint.py           # Pipeline orkestrasi 5 fase dubbing
├── execute_zona4_level3_sprint.py    # Skrip pipeline otomatis Zona 4 Level 3
├── execute_zona4_level4_sprint.py    # Skrip pipeline otomatis Zona 4 Level 4
├── execute_zona4_level5_sprint.py    # Skrip pipeline otomatis Zona 4 Level 5
├── execute_zona4_level6_sprint.py    # Skrip pipeline otomatis Zona 4 Level 6
├── execute_zona5_level1_sprint.py    # Skrip pipeline otomatis Zona 5 Level 1
└── execute_zona5_levels3_to_6_sprint.py # Skrip pipeline otomatis Zona 5 Level 3-6 (7 Video)
```

---

## 🚀 Panduan Penggunaan

### 1. Menjalankan Server Studio Web
```bash
# Aktifkan virtual environment
source .venv/bin/activate

# Jalankan server studio pada port 8765
python3 server.py
# atau: uvicorn server:app --host 0.0.0.0 --port 8765 --reload
```
Buka browser pada: **`http://localhost:8765/#/proyek-video`**

### 2. Menjalankan Sprint Video Dubbing Baru
Gunakan CLI runner otomatis [`sprint_video_dubbing.sh`](file:///Users/yohanessurya/Documents/Development/VoiceOver/sprint_video_dubbing.sh):

```bash
# Dubbing video lokal
./sprint_video_dubbing.sh \
  --video "Hasil/videoMarcia/z1_bilangan/z1l1_sb1bermain1_Z1L1TB2AB2-1F_54s.mp4" \
  --start 0 \
  --duration 54 \
  --voice "so_marcia" \
  --project-name "sprint_03_z1l1_bilangan_54s"

# Dubbing video YouTube
./sprint_video_dubbing.sh \
  --url "https://www.youtube.com/watch?v=t630efAuHPU" \
  --start 0 \
  --duration 36 \
  --voice "so_yosu" \
  --project-name "perkalian_2digit_1digit"
```

---

## ⚙️ Standar Akustik & Troubleshooting

* **Pencegahan White Noise**: Wajib menginisialisasi model dengan `F5TTS_v1_Base` di `f5_engine.py`.
* **Kestabilan Nada ($F_0$) pada Frasa Pendek**: Gunakan `nfe_step = 32`, `speed = 1.05`, dan pemangkasan silence otomatis dengan librosa.
* **Penyaringan Noise Tanpa Muffled**: Hindari pemfilteran spektral agresif (`afftdn=nf=-28`). Terapkan rantai siar standar: `highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10`.
* **Pemetaan Audio FFmpeg**: Selalu gunakan `-map 0:v:0 -map 1:a:0` saat muxing untuk menjamin video menggunakan audio hasil dubbing.
* **Artikulasi Angka Fonetik Penuh**: Selalu lewati teks matematika dengan `normalize_numbers()` di `gasing_pronunciation.py` untuk mencegah mumbling / salah sebut pada model difusi.
* **Sample Rate Master WAV 44.1kHz**: Selalu setel `-ar 44100` pada pembuatan master WAV uncompressed agar file tidak membengkak ke 192kHz (>100MB) dan tetap aman untuk GitHub repository.
* **Integritas Video Track Asli**: Gunakan track visual asli tanpa crop persegi atau masking buatan untuk menjaga rumus matematika di seluruh sudut layar tetap utuh.
