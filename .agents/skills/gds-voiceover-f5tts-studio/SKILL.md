---
name: gds-voiceover-f5tts-studio
description: Standar arsitektur teknis VoiceOver Studio SO, voice cloning F5-TTS Indonesian Finetune V2, pencegahan desisan/white noise (arsitektur F5TTS_v1_Base, alignment teks acuan, pembersihan tanda baca), dan aturan pelafalan GASING.
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

## 2. Penyebab Suara Mendesis (White Noise) & Solusi Wajib

Jika audio hasil generate hanya berbunyi **desisan statis**, **suara robotik mendengung**, atau **perulangan suku kata di akhir kalimat**:

### A. Wajib Menggunakan Arsitektur `F5TTS_v1_Base`
* **Masalah**: Menginisialisasi model dengan `model="F5TTS_Base"` memicu desisan 100% (*0.0% voiced frames*). Pada `F5TTS_Base`, DiT mengaktifkan `pe_attn_head: 1` (*positional encoding* tambahan pada *cross-attention*) dan `text_mask_padding: False`.
* **Aturan Mutlak**: Model fine-tune Indonesia V2 dilatih di atas **`F5TTS_v1_Base`** (`pe_attn_head: null`, `text_mask_padding: True`).
* **Implementasi di `f5_engine.py`**:
  ```python
  self.model = F5TTS(
      model="F5TTS_v1_Base", # JANGAN F5TTS_Base!
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

### 1. Guru Marcia (`so_marcia`)
* **Role**: Pemandu & Tutor Utama Sacred Octagon (Tanya Marcia)
* **Karakter**: Ramah, hangat, penuh empati, memandu petualangan matematika anak.
* **Audio Ref**: `assets/cloned_voices/marcia_ref.wav` (24kHz Mono, durasi ~7.3 detik, dipotong dari dialog pembuka video Zone 5 Level 1).
* **Teks Ref Resmi**:
  > *"Ketika kita hendak menghitung enam bagi dua, sama saja dengan bertanya dua kali berapa sama dengan enam."*

### 2. Prof. Yohanes Surya (`prof_yosu_asli`)
* **Role**: Pendiri & Guru Besar GASING
* **Karakter**: Berwibawa, inspiratif, membakar semangat berhitung.
* **Audio Ref**: `assets/cloned_voices/prof_yosu_ref.wav`
* **Teks Ref Resmi**:
  > *"Salam Ksatria Gaber, saya Profesor GASING Yosu dari masa depan."*

### 3. Studio Broadcast Alternative (Nol Noise)
* Jika dibutuhkan audio instan 100% bebas noise untuk aset game PWA (tanpa beban GPU difusi lokal), gunakan neural model studio `id-ID-GadisNeural` yang dipetakan pada preset `guru_marcia`.

---

## 4. Standar Naskah Pujian GASING

Saat menghasilkan audio game GASING, pastikan frasa jingle berikut ditranskripsi sesuai pola:
* Jingle WOW: `"Kasih We, kasih O, kasih We, WOW! Hebat sekali!"`
* Ucapan Tepat: `"Jawaban tepat! Kamu luar biasa!"`
* Anak Cerdas: `"Hebat! Kamu anak cerdas kebanggaan Indonesia!"`
* Slogan GASING: `"Gampang, Asyik, dan Menyenangkan!"`
