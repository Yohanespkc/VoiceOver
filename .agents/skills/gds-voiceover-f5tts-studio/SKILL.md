---
name: gds-voiceover-f5tts-studio
description: Standar arsitektur teknis VoiceOver Studio SO, voice cloning F5-TTS Indonesian Finetune V2, pencegahan desisan/white noise, nada melengking (pitch overshoot), pemisahan AT Marcia vs AT John, dan aturan pelafalan GASING.
---

# VoiceOver Studio SO & F5-TTS Voice Cloning Standard

Dokumen ini adalah **pedoman resmi arsitektur teknis dan troubleshooting** VoiceOver Studio SO untuk generasi narasi, voice cloning, audio tuning DSP, dan integrasi aset suara karakter Sacred Octagon serta Trainer GASING (Guru Marcia, Prof. Yohanes Surya, dsb).

---

## 1. Arsitektur Inti & Model Stack

1. **Diffusion Transformer**: `Eempostor/F5-TTS-INDO-FINETUNE-V2`
   - Checkpoint: `models/f5_tts_indo/f5_tts_indo_v2.pt` (~1.34 GB)
   - Vocab: `models/f5_tts_indo/vocab.txt` (2,546 token pinyin + karakter alfabet)
2. **Neural Vocoder**: Vocos Mel 24kHz (`charactr/vocos-mel-24khz`)
3. **Audio Preprocessor & Normalizer**:
   - `gasing_pronunciation.py`: Kamus bilingual ("geim", "ei-ai"), jingle pujian GASING, angka, serta normalisasi tanda baca.
4. **DSP Audio Engine & Resampler**:
   - Web Audio API (real-time browser tuner) & FFmpeg LAME (master MP3 320kbps / 16-bit PCM WAV).

---

## 2. Pencegahan Masalah Akustik & Desisan (White Noise)

### A. Wajib Menggunakan Arsitektur `F5TTS_v1_Base`
* **Masalah**: Menginisialisasi model dengan `model="F5TTS_Base"` memicu desisan 100% (*0.0% voiced frames*). Pada `F5TTS_Base`, DiT mengaktifkan `pe_attn_head: 1` (*positional encoding* tambahan pada *cross-attention*) dan `text_mask_padding: False`.
* **Aturan Mutlak**: Model fine-tune Indonesia V2 dilatih di atas **`F5TTS_v1_Base`** (`pe_attn_head: null`, `text_mask_padding: True`).
* **Implementasi di `f5_engine.py`**:
  ```python
  self.model = F5TTS(
      model="F5TTS_v1_Base",  # JANGAN F5TTS_Base!
      ckpt_file=CKPT_FILE,
      vocab_file=VOCAB_FILE,
      device=self.device
  )
  ```

### B. Mismatch 100% Antara Teks Acuan dan Audio Referensi
* **Masalah**: Pada *flow-matching ODE*, teks acuan (*reference text*) dan audio referensi (*reference audio*) harus **100% selaras kata demi kata**. Jika teks acuan berbeda dari apa yang diucapkan di audio, *cross-attention* gagal memetakan fonem dan trajektori difusi kolaps menjadi *white noise*.
* **Solusi**: Selalu verifikasi audio acuan menggunakan model ASR (Whisper) sebelum menyimpannya ke `trainers.json`.

### C. Normalisasi Tanda Baca Berulang
* **Masalah**: Simbol titik ganda seperti `....` atau tanda seru berulang `!!` membingungkan estimator durasi F5-TTS. Kalimat selesai diucapkan namun durasi belum habis, sehingga model difusi melakukan *infinite loop* pada suku kata terakhir (misal: "wih, wih, wih..." atau desis buzzing).
* **Solusi di `gasing_pronunciation.py`**:
  ```python
  processed = re.sub(r"\.{2,}", ".", processed)       # '....' -> '.'
  processed = re.sub(r"!{2,}", "!", processed)       # '!!' -> '!'
  processed = re.sub(r"\s+([.,!?;:])", r"\1", processed)  # Spasi sebelum tanda baca
  processed = re.sub(r"([.,!?;:])(?=[^\s\d])", r"\1 ", processed) # Spasi sesudah tanda baca
  ```
* **Pemotongan Silence Otomatis**:
  Selalu panggil `tts_model.infer(..., remove_silence=True)` untuk memangkas sisa durasi kosong di akhir rekaman.

### D. Pencegahan Korupsi Sample Rate
* Audio asli F5-TTS adalah **24,000 Hz Mono**.
* DILARANG menggunakan filter `asetrate` tanpa perhitungan rasio yang tepat di server karena akan mempercepat audio 1.83x menjadi suara chipmunk melengking.
* Konversi ke MP3 dilakukan dengan:
  ```bash
  ffmpeg -y -i input_24k.wav -ar 44100 -ac 2 -c:a libmp3lame -b:a 320k output.mp3
  ```

---

## 3. Profil Karakter Suara Resmi VoiceOver Studio SO

### 1. Guru Marcia (`so_marcia` / `at_c04618f8`)
* **Identitas**: Trainer Marcia Asli — Guru Pembimbing & Narator Utama Modul Hitung GASING (Wanita).
* **Karakter**: Ramah, hangat, penuh empati, mendidik, mezzo-soprano ($F_0 \approx 260 - 295$ Hz).
* **Audio Ref**: `assets/cloned_voices/at_marcia_ref.wav` (24kHz Mono, durasi 7.70s, dipotong dari video master 6 menit Trainer Marcia).
* **Teks Ref Wajib**:
  > *"Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."*
* > [!WARNING]
  > **JANGAN TERTUKAR DENGAN TUTOR JOHN**: Pada modul Tanya Marcia pembagian (`z5l1`), video dibawakan oleh Tutor John (Pria, bariton ~89 Hz). Pastikan mengambil referensi vokal wanita Trainer Marcia.

### 2. Tutor John (`at_john`)
* **Identitas**: Trainer GASING / Tutor Tanya Marcia Pembagian (Pria).
* **Karakter**: Tenang, jelas, artikulatif, bariton ($F_0 \approx 89$ Hz).
* **Audio Ref**: `assets/cloned_voices/at_john_ref.wav` (24kHz Mono).
* **Teks Ref Wajib**:
  > *"Ketika kita hendak menghitung enam bagi dua, sama saja dengan bertanya dua kali berapa sama dengan enam."*

### 3. Prof. Yohanes Surya (`prof_yosu_asli` / `so_yosu`)
* **Identitas**: Pendiri & Guru Besar GASING.
* **Karakter**: Berwibawa, inspiratif, patriotik, membakar semangat berhitung ($F_0 \approx 125 - 140$ Hz).
* **Audio Ref**: `assets/cloned_voices/yosu_ref.wav` (24kHz Mono, dari video resmi perkalian 2-digit YouTube).
* **Teks Ref Wajib**:
  > *"Perkalian dua digit dengan satu digit. Kita lihat di sini, empat puluh dua kali tiga."*

### 4. Studio Broadcast Alternative (Nol Noise)
* Jika dibutuhkan audio instan 100% bebas noise untuk aset game PWA (tanpa beban GPU difusi lokal), gunakan neural model studio `id-ID-GadisNeural` yang dipetakan pada preset `guru_marcia`.

---

## 4. Standar Akustik, Pencegahan Nada Melengking & Formant Muffling

### A. Fenomena Nada Melengking pada Frasa Pendek (*Short-Phrase Pitch Overshoot*)
* **Gejala**: Ketika diminta membacakan frasa sangat pendek (2–3 kata, misal: *"Ini enam."*, *"Ini delapan."*), suara Guru Marcia terdengar melengking tinggi (360–402 Hz) seperti suara anak-anak/kartun.
* **Penyebab**: Jendela durasi difusi default terlalu sempit untuk teks <12 karakter sehingga vocoder saraf (*Vocos Mel*) memampatkan gelombang frekuensi dasar.
* **Solusi Baku**:
  1. Gunakan resolusi difusi **`nfe_step = 32`** (bukan 16).
  2. Atur kecepatan generasi **`speed = 1.05`**.
  3. Pangkas silence awal & akhir dengan librosa:
     ```python
     y, sr = librosa.load(src_wav, sr=24000)
     y_trimmed, _ = librosa.effects.trim(y, top_db=25)
     ```
  4. Hasil: Durasi pas (0.85s – 1.05s) dan nada $F_0$ stabil pada register mezzo-soprano dewasa (**~261 – 265 Hz**).

### B. Larangan Pemfilteran Spektral Agresif (*Over-Denoising*)
* **Kesalahan Fatal**: Menerapkan `afftdn=nf=-28` atau lowpass di bawah 12.000 Hz. Filter ini memotong harmonik vokal atas di rentang 2.000 Hz – 5.000 Hz, menurunkan *spectral centroid* dari 1.900 Hz menjadi 746 Hz (suara mendem, tumpul, dan robotik).
* **Rantai Mastering Resmi**:
  ```bash
  ffmpeg -y -i input.wav -af "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10" -ar 44100 -ac 2 output.wav
  ```
  Rantai ini menghilangkan rumble frekuensi rendah (<80 Hz) dan menormalkan gain ke standar siar EBU R128 (-16 LUFS) dengan meloloskan 100% kejernihan vokal dan artikulasi napas.

### C. Pencegahan Masalah Pemetaan Audio FFmpeg saat Muxing Video
* **Masalah**: Menjalankan perintah muxing tanpa `-map` membuat FFmpeg otomatis mengambil track audio pertama (`input 0`), sehingga video hasil dubbing tetap mengeluarkan suara asli rekaman sumber (misal suara Tutor John).
* **Perintah Muxing Wajib**:
  ```bash
  ffmpeg -y -i video_sumber.mp4 -i master_dubbing.wav \
    -map 0:v:0 -map 1:a:0 \
    -c:v copy -c:a aac -b:a 192k -shortest output_dubbed.mp4
  ```

---

## 5. Standar Naskah Pujian GASING

Saat menghasilkan audio game GASING, pastikan frasa jingle berikut ditranskripsi sesuai pola:
* Jingle WOW: `"Kasih We, kasih O, kasih We, WOW! Hebat sekali!"`
* Ucapan Tepat: `"Jawaban tepat! Kamu luar biasa!"`
* Anak Cerdas: `"Hebat! Kamu anak cerdas kebanggaan Indonesia!"`
* Slogan GASING: `"Gampang, Asyik, dan Menyenangkan!"`
