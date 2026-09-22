#!/usr/bin/env python3
"""
batch_convert_marcia.py
Batch extractor and lightweight converter for all Marcia learning videos from SO project.
Optimizes video to lightweight MP4 (H.264 + AAC) with high visual clarity for text and math symbols.
"""

import os
import sys
import json
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SO_WEB_PUBLIC = "/Users/yohanessurya/Documents/Development/so/web/public"
OUTPUT_BASE = os.path.join(BASE_DIR, "Hasil", "videoMarcia")

# 1. Video List with metadata
VIDEOS = [
    # --- ZONA 1: BILANGAN ---
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L1", "topic": "Mengenal Bilangan 1-10", "rel": "assets/videos/z1l1/Z1L1TB1AB1-1A-FULL.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L1", "topic": "Mengenal Angka Konkret & Simbol", "rel": "assets/videos/z1l1/Z1L1TB2AB1-1D.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L1", "topic": "Latihan Menulis Angka", "rel": "assets/videos/z1l1/Z1L1TB2AB2-1F.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L2", "topic": "Mengenal Bilangan 11-20", "rel": "assets/videos/z1l2/Z1L2TB1AB1-2A.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L3", "topic": "Menghitung Maju & Mundur 21-99", "rel": "assets/videos/z1l3/Z1L3TB1AB1-3A.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L4", "topic": "Membaca & Menulis Bilangan Ratusan", "rel": "assets/videos/z1l4/Z1L4TB1AB1-4A.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L5", "topic": "Nilai Tempat Ribuan s.d. Ratus Ribuan", "rel": "assets/videos/z1l5/Z1L5TB1AB1-5A-FULL.webm"},
    {"zone": "z1_bilangan", "zone_num": 1, "level": "L6", "topic": "Membandingkan & Mengurutkan Bilangan", "rel": "assets/videos/z1l6/Z1L6TB1AB1-6A.webm"},

    # --- ZONA 2: PENJUMLAHAN ---
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L1", "topic": "Penjumlahan Bilangan 1 sampai 5", "rel": "assets/videos/z2l1/Z2L1TB1AB1-1A-FULL.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L1", "topic": "Penjumlahan dengan Benda Konkret", "rel": "assets/videos/z2l1/Z2L1TB2AB1-1D.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L1", "topic": "Pasangan Penjumlahan Bilangan Kecil", "rel": "assets/videos/z2l1/Z2L1TB3AB1-1G.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L2", "topic": "Penjumlahan yang Hasilnya 6", "rel": "assets/videos/z2l2/Z2L2TB1AB1-2A-FULL.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L2", "topic": "Penjumlahan yang Hasilnya 7", "rel": "assets/videos/z2l2/Z2L2TB2AB1-2F.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L2", "topic": "Penjumlahan yang Hasilnya 8", "rel": "assets/videos/z2l2/Z2L2TB3AB1-2J.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L2", "topic": "Penjumlahan yang Hasilnya 9", "rel": "assets/videos/z2l2/Z2L2TB4AB1-2O.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L2", "topic": "Penjumlahan yang Hasilnya 10", "rel": "assets/videos/z2l2/Z2L2TB5AB1-2S.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L3", "topic": "Penjumlahan 2 Digit + 1 Digit (Konsep Dasar)", "rel": "assets/videos/z2l3/z2l3sb1bermain1_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L3", "topic": "Penjumlahan 2 Digit + 2 Digit Tanpa Menyimpan", "rel": "assets/videos/z2l3/z2l3sb2bermain1_sb2bermain2_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L3", "topic": "Penjumlahan 2 Digit + 1 Digit (Variasi & Mencongak)", "rel": "assets/videos/z2l3/Z2L3TB1AB1-3C.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2D + 1D Bersimpan (Peti Koin)", "rel": "assets/videos/z2l4/z2l4sb1bermain1_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2D + 1D Bersimpan Lanjutan", "rel": "assets/videos/z2l4/z2l4sb1bermain2_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2 Digit dengan 2 Digit (Penguatan)", "rel": "assets/videos/z2l4/Z2L4TB1AB2-4B.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2 Digit + 2 Digit (Teknik Dasar Menyimpan)", "rel": "assets/videos/z2l4/Z2L4TB2AB1-4G.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2D + 2D Bersimpan Bersusun", "rel": "assets/videos/z2l4/z2l4sb2bermain2_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L4", "topic": "Penjumlahan 2D + 2D Bersimpan Tahap Akhir", "rel": "assets/videos/z2l4/z2l4sb2bermain3_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L5", "topic": "Penjumlahan 3 Bilangan (Gladiator Arena)", "rel": "assets/videos/z2l5/z2l5sb1bermain1_sb1bermain2_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L5", "topic": "Penjumlahan 3 Digit + 3 Digit Bersusun (Tahap 1 Ratusan)", "rel": "assets/videos/z2l5/z2l5sb2bermain1_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L5", "topic": "Penjumlahan 3 Digit + 3 Digit Bersusun (Tahap 2 Puluhan)", "rel": "assets/videos/z2l5/z2l5sb2bermain2_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L5", "topic": "Penjumlahan 3 Digit + 3 Digit Bersusun (Tahap 3 Satuan)", "rel": "assets/videos/z2l5/z2l5sb2bermain3_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L5", "topic": "Penjumlahan 3 Digit + 3 Digit Bersusun (Penggabungan Hasil)", "rel": "assets/videos/z2l5/z2l5sb2bermain4_marcia.webm"},
    {"zone": "z2_penjumlahan", "zone_num": 2, "level": "L6", "topic": "Penjumlahan Mencongak Cepat & 3 Digit Kilat", "rel": "assets/videos/z2l6/Z2L6TB1AB1-6A.webm"},

    # --- ZONA 3: PERKALIAN ---
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L1", "topic": "Konsep Dasar Perkalian (Penjumlahan Berulang)", "rel": "assets/videos/z3l1/Z3L1SB1-1A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 1 dan 10", "rel": "assets/videos/z3l2/Z3L2SB1-2A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 2 (Konsep Pasangan Ganda)", "rel": "assets/videos/z3l2/Z3L2SB2-3A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 3", "rel": "assets/videos/z3l2/Z3L2SB3-4A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 4", "rel": "assets/videos/z3l2/Z3L2SB4-5A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 5 dengan Metode Jari GASING", "rel": "assets/videos/z3l2/Z3L2SB5-6A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 6", "rel": "assets/videos/z3l2/Z3L2SB6-7A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 7 (Audio Quiz & Balap Kuda)", "rel": "assets/videos/z3l2/Z3L2SB7-8A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 8", "rel": "assets/videos/z3l2/Z3L2SB8-9A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L2", "topic": "Tabel Perkalian 9 (Metode Jari & Pola Angka)", "rel": "assets/videos/z3l2/Z3L2SB9-10A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L3", "topic": "Perkalian 1 Digit x 2 Digit Tanpa Menyimpan", "rel": "assets/videos/z3l3/z3l3sb1bermain1_marcia.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L3", "topic": "Perkalian 1 Digit x 2 Digit Menyimpan", "rel": "assets/videos/z3l3/Z3L3SB2-12A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L4", "topic": "Perkalian 1 Digit x 3 Digit Tanpa Menyimpan", "rel": "assets/videos/z3l4/Z3L4SB1-13A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L4", "topic": "Perkalian 1 Digit x 3 Digit Menyimpan (Benteng Terakhir)", "rel": "assets/videos/z3l4/z3l4sb2bermain1_marcia.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L5", "topic": "Perkalian 2 Digit x 2 Digit", "rel": "assets/videos/z3l5/Z3L5SB1-15A.webm"},
    {"zone": "z3_perkalian", "zone_num": 3, "level": "L6", "topic": "Perkalian Cepat & Mencongak Bilangan Besar", "rel": "assets/videos/z3l6/Z3L6SB1-16A.webm"},

    # --- ZONA 4: PENGURANGAN ---
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L1", "topic": "Pengurangan Bilangan 1 sampai 10", "rel": "assets/videos/z4l1/z4l1sb1_1a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L2", "topic": "Pengurangan 2D - 1D (Surat Rahasia & Sandi Tulang)", "rel": "assets/videos/z4l2/z4l2sb1_3a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L2", "topic": "Pengurangan 2D - 1D (Telur Emas)", "rel": "assets/videos/z4l2/z4l2sb2_4a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L3", "topic": "Pengurangan 2D - 2D (Bowling Kuno India)", "rel": "assets/videos/z4l3/z4l3sb1_5a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L3", "topic": "Pengurangan 2D - 2D Tanpa Meminjam (Memanah Guci)", "rel": "assets/videos/z4l3/z4l3sb1bermain2_marcia.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L3", "topic": "Pengurangan 2D - 2D (Lanjutan)", "rel": "assets/videos/z4l3/z4l3sb2_6a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L4", "topic": "Pengurangan Bilangan Besar (Bowling Menara)", "rel": "assets/videos/z4l4/z4l4sb1_7a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L4", "topic": "Pengurangan Bilangan Besar (Memanah Labu)", "rel": "assets/videos/z4l4/z4l4sb2_8a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L5", "topic": "Pengurangan 3 Digit dengan 2 Digit (Perburuan Kadal)", "rel": "assets/videos/z4l5/z4l5sb1_9a.webm"},
    {"zone": "z4_pengurangan", "zone_num": 4, "level": "L6", "topic": "Pengurangan 4 Digit & Teka-Teki Silang 13x13", "rel": "assets/videos/z4l6/z4l6sb1_10a.webm"},

    # --- ZONA 5: PEMBAGIAN ---
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L1", "topic": "Pembagian 1 Digit Tanpa Sisa (Tanya Marcia: Kaitan Pembagian & Perkalian)", "rel": "assets/videos/z5l1/z5l1_tanya_marcia.mp4"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L1", "topic": "Pembagian 1 Digit Konsep Dasar", "rel": "assets/videos/z5l1/sb1_1a.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L2", "topic": "Pembagian Bersisa (Konsep Sisa Pembagian)", "rel": "assets/videos/z5l2/z5l2sb1bermain3_marcia.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L2", "topic": "Pembagian Bersisa Latihan", "rel": "assets/videos/z5l2/sb1_2a.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L3", "topic": "Pembagian Bilangan 2 Digit", "rel": "assets/videos/z5l3/z5l3sb1_3a.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L4", "topic": "Pembagian Bilangan 3 Digit (Tebing Merah)", "rel": "assets/videos/z5l4/z5l4sb1_4a.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L5", "topic": "Pembagian Bilangan 4 Digit", "rel": "assets/videos/z5l5/z5l5sb1_5a.webm"},
    {"zone": "z5_pembagian", "zone_num": 5, "level": "L6", "topic": "Pembagian Bilangan 5 Digit & Lanjutan (Mencongak)", "rel": "assets/videos/z5l6/z5l6sb1_6a.webm"},
]

def format_bytes(num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} TB"

def convert_video(item, index, total):
    src_path = os.path.join(SO_WEB_PUBLIC, item["rel"])
    if not os.path.exists(src_path):
        # Check alternative in VoiceOver Data VIdeo Marcia
        local_alt = os.path.join(BASE_DIR, "Data VIdeo Marcia", os.path.basename(item["rel"]))
        if os.path.exists(local_alt):
            src_path = local_alt
        else:
            print(f"[{index}/{total}] ⚠️ FILE TIDAK DITEMUKAN: {src_path}")
            return None

    orig_size = os.path.getsize(src_path)
    base_name = os.path.splitext(os.path.basename(item["rel"]))[0]
    out_dir = os.path.join(OUTPUT_BASE, item["zone"])
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{base_name}.mp4")

    print(f"[{index}/{total}] ⏳ Mengompresi: {base_name} ({format_bytes(orig_size)})...")
    start_t = time.time()

    # Highly optimized FFmpeg command:
    # 1. Scale max width 1280 while keeping even dimensions and aspect ratio
    # 2. H.264 CRF 26 for razor-sharp vector/text quality and high compression
    # 3. Preset fast + yuv420p for fast execution and universal compatibility
    # 4. AAC 96k stereo for clear sound
    # 5. faststart for zero-delay streaming
    cmd = [
        "ffmpeg", "-y", "-i", src_path,
        "-vf", "scale='min(1280,iw)':-2",
        "-c:v", "libx264", "-crf", "26", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        out_file
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.time() - start_t

    if res.returncode != 0:
        print(f"[{index}/{total}] ❌ GAGAL: {base_name}\nError: {res.stderr.decode('utf-8', errors='ignore')[-300:]}")
        return None

    new_size = os.path.getsize(out_file)
    ratio = (1 - (new_size / orig_size)) * 100

    # Probe duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        out_file
    ]
    try:
        dur_str = subprocess.check_output(probe_cmd, text=True).strip()
        dur = float(dur_str)
    except Exception:
        dur = 0.0

    print(f"[{index}/{total}] ✅ SELESAI: {base_name}.mp4 | {format_bytes(orig_size)} ➜ {format_bytes(new_size)} (Hemat {ratio:.1f}%) | {dur:.1f}s | {elapsed:.1f}s")

    return {
        "id": base_name,
        "filename": f"{base_name}.mp4",
        "zone": item["zone"],
        "zone_num": item["zone_num"],
        "level": item["level"],
        "topic": item["topic"],
        "original_path": src_path,
        "output_path": os.path.relpath(out_file, BASE_DIR),
        "original_size_bytes": orig_size,
        "compressed_size_bytes": new_size,
        "compression_savings_percent": round(ratio, 1),
        "duration_seconds": round(dur, 2)
    }

def main():
    print(f"=== BATCH CONVERTER VIDEO PEMBELAJARAN MARCIA (SO) ===")
    print(f"Total Target Video: {len(VIDEOS)}")
    print(f"Direktori Output: {OUTPUT_BASE}\n")

    os.makedirs(OUTPUT_BASE, exist_ok=True)
    results = []
    total = len(VIDEOS)

    # Use 3 workers for fast parallel encoding without overloading CPU
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_idx = {
            executor.submit(convert_video, item, idx + 1, total): (idx + 1, item)
            for idx, item in enumerate(VIDEOS)
        }
        for future in as_completed(future_to_idx):
            res = future.result()
            if res:
                results.append(res)

    results.sort(key=lambda x: (x["zone_num"], x["level"], x["id"]))

    total_orig = sum(r["original_size_bytes"] for r in results)
    total_new = sum(r["compressed_size_bytes"] for r in results)
    total_savings = (1 - (total_new / total_orig)) * 100 if total_orig > 0 else 0

    print("\n" + "=" * 60)
    print(f"🎉 SUKSES MEMPROSES: {len(results)} / {total} VIDEO")
    print(f"Ukuran Asli Total   : {format_bytes(total_orig)}")
    print(f"Ukuran Hasil Total  : {format_bytes(total_new)}")
    print(f"Penghematan Ukuran  : {total_savings:.1f}%")
    print("=" * 60)

    # Save catalog.json
    catalog_path = os.path.join(OUTPUT_BASE, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_videos": len(results),
            "total_original_bytes": total_orig,
            "total_compressed_bytes": total_new,
            "total_savings_percent": round(total_savings, 1),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "videos": results
        }, f, indent=2)
    print(f"💾 Katalog tersimpan di: {catalog_path}")

    # Generate README.md in Hasil/videoMarcia/
    readme_path = os.path.join(OUTPUT_BASE, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# 🎬 Koleksi Video Pembelajaran Marcia (GASING Sacred Octagon)\n\n")
        f.write(f"Koleksi seluruh video pembelajaran **Tanya Marcia** dari proyek SO dioptimasi ke format MP4 (H.264 + AAC) ukuran kecil dan ringan dengan kualitas visual & audio tetap prima.\n\n")
        f.write(f"- **Total Video**: {len(results)} berkas\n")
        f.write(f"- **Ukuran Asli**: {format_bytes(total_orig)}\n")
        f.write(f"- **Ukuran Ringan**: {format_bytes(total_new)} (Hemat **{total_savings:.1f}%**)\n\n")
        f.write("---\n\n")
        f.write("| No | Zona | Level | Topik Materi | Durasi | Asli | Kompresi | Hemat | Berkas MP4 |\n")
        f.write("|:---:|:---:|:---:|---|:---:|:---:|:---:|:---:|---|\n")
        for i, r in enumerate(results, 1):
            f.write(f"| {i} | {r['zone']} | {r['level']} | {r['topic']} | {r['duration_seconds']}s | {format_bytes(r['original_size_bytes'])} | {format_bytes(r['compressed_size_bytes'])} | {r['compression_savings_percent']}% | [{r['filename']}](file://{os.path.abspath(os.path.join(OUTPUT_BASE, r['zone'], r['filename']))}) |\n")
    print(f"📄 README dokumentasi tersimpan di: {readme_path}")

if __name__ == "__main__":
    main()
