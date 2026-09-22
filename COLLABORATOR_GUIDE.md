# 🤝 Panduan Kolaborator: Optimalisasi GPU & Kloning Suara Marcia Asli

> **Panduan praktis bagi pengembang & kolaborator untuk bekerja lebih efisien, cepat, dan hemat sumber daya GPU pada proyek VoiceOver Studio SO.**

---

## 🎯 1. Menghubungkan ke Suara Guru Marcia Asli (1 Baris Kode)

Untuk memastikan suara hasil generasi **100% konsisten, hangat, dan mirip dengan Trainer Marcia asli**, gunakan metode bawaan `generate_marcia()`:

```python
from f5_engine import F5IndoEngine

# Inisialisasi engine singleton
engine = F5IndoEngine.get_instance()

# 1 Baris generasi otomatis dengan parameter vokal optimal
res = engine.generate_marcia("Halo adik-adik pintar, mari kita belajar penjumlahan gasing bersama Marcia!")

print("Audio siap:", res["audio_url"]) # Misal: /output/marcia_xxxx.wav
print("Durasi:", res["duration"], "detik")
```

### 💡 Apa yang Dikerjakan Otomatis di Balik Layar?
1. **Audio & Teks Acuan Autentik**: Mengunci ke `assets/cloned_voices/at_marcia_ref.wav` dengan teks acuan resmi (*"Pertama kita tulis dulu nilai tempat..."*). Tidak akan salah tertukar dengan suara Tutor John (pria).
2. **Anti-Melengking (*Pitch Overshoot Elimination*)**: Menggunakan `nfe_step=32` dan `speed=1.05` sehingga frekuensi vokal dasar ($F_0$) terkunci stabil di rentang **250 – 265 Hz** (mezzo-soprano dewasa), bukan 400 Hz (kartun/anak-anak).
3. **Silence Trimming Otomatis**: Memotong hening awal & akhir (`librosa.effects.trim`) agar durasi ucapan pas dan presisi.
4. **Mastering Siar Tanpa Desis (*Broadcast Standard*)**: Menerapkan filter `highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10` yang meloloskan harmonik vokal 2.000–5.000 Hz tanpa efek suara mendem.

---

## ⚡ 2. Fitur Penghematan GPU Otomatis (*Auto GPU Saving*)

Kolaborator tidak perlu khawatir kehabisan VRAM atau membebani kartu grafis (baik Apple Silicon MPS maupun NVIDIA CUDA). Proyek ini telah dilengkapi **3 Lapisan Penghemat GPU**:

### Lapisan 1: Transparent Disk Phrase Cache (Hemat 100% GPU)
* Setiap frasa yang pernah disintesis otomatis disimpan ke `output/.phrase_cache/` dengan hash MD5 parameter.
* Jika kolaborator atau skrip meminta kalimat yang sama (misal *"Ini enam."* atau narasi tombol berulang), F5-TTS **tidak akan dijalankan ulang**.
* **Kecepatan**: Selesai dalam **0.1 detik** (alih-alih 18 detik inferensi GPU), menghemat **100% komputasi GPU**.

```python
# Pemanggilan pertama: Inferensi normal pada GPU (~10s)
res1 = engine.generate_marcia("Jawaban tepat! Kamu luar biasa!")

# Pemanggilan kedua: GPU Cache Hit (0.1s, 0% beban GPU!)
res2 = engine.generate_marcia("Jawaban tepat! Kamu luar biasa!")
# Output log: ⚡ [GPU Cache Hit] Menggunakan cache suara ... (0s komputasi GPU)
```

### Lapisan 2: Automatic VRAM Cache Purge (Bebas Memory Leak)
* Setiap kali pemanggilan `generate()` selesai, blok `finally` otomatis memanggil:
  ```python
  engine.free_gpu_memory()
  ```
  yang secara aktif membersihkan alokasi cache PyTorch:
  * `torch.mps.empty_cache()` (pada Mac Apple Silicon)
  * `torch.cuda.empty_cache()` (pada Linux / NVIDIA GPU)
  * `gc.collect()` untuk membersihkan objek Python tak terpakai.
* Memori GPU langsung dikembalikan ke sistem operasi, mencegah crash *Out-of-Memory (OOM)*.

### Lapisan 3: Unique Phrase Caching pada Video Dubbing
* Pada video pembelajaran yang memiliki drill kartu mencongak berulang (seperti Sprint 03 dengan 27 penunjukan kartu angka):
* Pipeline `video_dubbing_sprint.py` secara otomatis menduplikasi naskah menjadi frasa unik:
  * 27 segmen $\rightarrow$ hanya 9 kali generasi GPU unik.
  * **Menghemat 66% waktu inferensi GPU**.

---

## 🛠️ 3. Contoh Penggunaan untuk Karakter Lain

### Kloning Suara Prof. Yohanes Surya Asli
```python
res = engine.generate_yosu("Perkalian dua digit dengan satu digit. Kita mulai selalu dari sebelah kiri!")
print("Audio Yosu:", res["audio_url"])
```

### Generasi Kustom dengan Audio Acuan Sendiri
```python
res = engine.generate(
    ref_audio_path="path/to/custom_ref.wav",
    ref_text="Teks yang diucapkan di audio referensi secara tepat.",
    gen_text="Teks baru yang ingin dihasilkan.",
    speed=1.0,
    nfe_step=32,
    output_format="wav" # atau 'mp3'
)
```

---

## 🎬 4. Menjalankan Video Dubbing Sprint

Untuk mendubbing video baru secara cepat:

```bash
# 1. Pastikan virtual environment aktif
source .venv/bin/activate

# 2. Jalankan runner sprint
./sprint_video_dubbing.sh \
  --video "Hasil/videoMarcia/z1_bilangan/z1l1_sb1bermain1_Z1L1TB2AB2-1F_54s.mp4" \
  --start 0 \
  --duration 54 \
  --voice "so_marcia" \
  --project-name "sprint_03_z1l1_bilangan_54s"

# 3. Tinjau hasil komparasi sinkron di browser
# Buka http://localhost:8765/#/proyek-video
```

---

## 📋 5. Checklist Singkat Kolaborator Sebelum Push

1. [ ] Jalankan uji singkat:
   ```bash
   python3 -c "from f5_engine import F5IndoEngine; e = F5IndoEngine.get_instance(); e.generate_marcia('Tes suara marcia')"
   ```
2. [ ] Pastikan tidak ada file model (>100MB) yang masuk ke git staging (`git status`).
3. [ ] Pastikan audio acuan `at_marcia_ref.wav` tidak tertimpa filter `afftdn`.
