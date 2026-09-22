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
4. **Karakter Suara Resmi**:
   * **Guru Marcia (`so_marcia`)**: Suara asli Trainer Marcia (Wanita, mezzo-soprano ~265 Hz) yang ramah, hangat, dan mendidik.
   * **Prof. Yohanes Surya (`prof_yosu_asli` / `so_yosu`)**: Suara asli Pendiri GASING yang berwibawa, patriotik, dan membakar semangat.
   * **Tutor John (`at_john`)**: Suara tenang Tutor John (Pria, bariton ~89 Hz) pemandu video pembagian.
   * **Studio Broadcast (`guru_marcia_edge`)**: Vokal instan bebas noise 100% menggunakan neural model `id-ID-GadisNeural`.

---

## 🎬 Daftar Sprint Video Dubbing Resmi

| Sprint | Modul Pembelajaran | Durasi | Karakter Dubbing | Fitur Khusus | Akses Web |
|---|---|---|---|---|---|
| **Sprint 01** | Perkalian 2 Digit x 1 Digit (`perkalian_2digit_1digit`) | 36.00s | Prof. Yohanes Surya | Sinkronisasi 8 titik goresan pena, kanvas hening absolut | `/proyek-video` |
| **Sprint 02** | Tanya Marcia Pembagian (`z5l1_tanya_marcia`) | 22.00s | Guru Marcia | Penggantian suara tutor pria ke wanita, 7 segmen dialog | `/proyek-video` |
| **Sprint 03** | Mengenal Bilangan 6 s.d. 10 (`sprint_03_z1l1_bilangan_54s`) | 54.00s | Guru Marcia Autentik | *Unique Phrase Caching* (3x lebih cepat), resolusi `nfe_step=32`, nada stabil 264 Hz | `/proyek-video` |

---

## 📁 Struktur Direktori Proyek

```
VoiceOver/
├── .agents/skills/                   # Panduan & standar arsitektur agentik
│   ├── gds-voiceover-f5tts-studio/   # Standar resmi F5-TTS & pencegahan noise/pitch overshoot
│   └── gds-voiceover-video-cloning/  # SOP resmi 5 fase sprint video dubbing
├── assets/                           # Aset statis & audio acuan
│   ├── cloned_voices/                # Berkas WAV acuan (at_marcia_ref, yosu_ref, at_john_ref)
│   └── trainers.json                 # Basis data profil suara karakter
├── AT Marcia contoh/                 # 12 Koleksi kasus suara asli Trainer Marcia (Kasus 1–5)
├── Yosu Contoh/                      # 12 Koleksi kasus motivasi & pembelajaran Prof. Yohanes Surya
├── Hasil/                            # Berkas video hasil olahan materi game SO
│   └── videoMarcia/                  # Potongan video Tanya Marcia (Zona 1 s.d. Zona 5)
├── video_projects/                   # Proyek sprint video dubbing
│   ├── perkalian_2digit_1digit/      # Sprint 01
│   ├── z5l1_tanya_marcia/            # Sprint 02
│   └── sprint_03_z1l1_bilangan_54s/  # Sprint 03
├── f5_engine.py                      # Engine utama F5-TTS Indo V2
├── gasing_pronunciation.py           # Kamus pelafalan & normalisasi teks GASING
├── server.py                         # Backend API FastAPI & server antarmuka web
├── sprint_video_dubbing.sh           # CLI runner otomatisasi sprint video dubbing
├── video_dubbing_sprint.py           # Pipeline orkestrasi 5 fase dubbing
└── execute_sprint_03.py              # Skrip eksekusi dan perakitan Sprint 03
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
