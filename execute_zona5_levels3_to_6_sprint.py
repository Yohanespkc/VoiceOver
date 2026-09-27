#!/usr/bin/env python3
"""
execute_zona5_levels3_to_6_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk 7 Video Zona 5 (Pembagian Lanjut):
1. zone 5 level 3a.mp4 (46.00s) -> Pembagian 3D : 1D (873 : 3 = 291)
2. zona 5 level 3b.mp4 (58.00s) -> Pembagian 3D : 1D Bersisa (167 : 4 = 41 sisa 3)
3. zona 5 level 3c.mp4 (59.50s) -> Pembagian Puluhan Nol (818 : 8 = 102 sisa 2)
4. zona 5 level 4a.mp4 (96.00s) -> Pembagian Pembagi 2D / Tabel 11 (453 : 11 = 41 sisa 2)
5. zona 5 level 4b.mp4 (107.00s) -> Pembagian Pembagi 2D / Tabel 15 (2345 : 15 = 156 sisa 5)
6. zona 5 level 5.mp4 (145.00s) -> Trik Pembagian Cepat 10, 100, 5, 25, 125, 250
7. zone 5 level 6.mp4 (105.00s) -> Pembagian Pembagi 3D (38273 : 121 = 316 sisa 37)

Standar Kualitas Mutlak:
1. Suara Karakter: Guru Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2) + Edge-TTS Studio (id-ID-GadisNeural).
2. Artikulasi Fonetik Penuh: Semua angka dieja 100% lengkap tanpa salah sebut.
3. Zero Truncation: Segmen penutup tidak dipotong -t, terucap utuh hingga suku kata terakhir.
4. Freeze Frame Akhir (2.5 - 3.7 Detik): Menahan papan tulis lengkap dengan tpad=stop_mode=clone.
5. Canvas Widescreen 16:9 Murni Putih (#FFFFFF): scale=928:696,pad=1280:720:176:0:color=white (margin bawah ~109px).
6. Kompresi Ringan Web-Ready: H.264 tune animation CRF 28 & WebM VP9 CRF 35 (FastStart streaming).
7. Master WAV Standard: -ar 44100 pcm_s16le.
8. Sinkronisasi Multi-Tujuan:
   - Data VIdeo Marcia/ (*_ringan.mp4)
   - Hasil/videoMarcia/z5_pembagian/
   - Proyek SO: so/web/public/assets/videos/z5l3, z5l4, z5l5, z5l6
   - Web Studio: video_projects/ (/Proyek Video)
"""

import os
import sys
import json
import time
import shutil
import asyncio
import subprocess
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
VIDEO_PROJECTS_DIR = os.path.join(BASE_DIR, "video_projects")
HASIL_Z5_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z5_pembagian")
SO_BASE_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos"

os.makedirs(HASIL_Z5_DIR, exist_ok=True)

VIDEOS_CONFIG = [
    # 1. Zone 5 Level 3a
    {
        "id": "z5l3a_pembagian_3digit_1digit_873_bagi_3",
        "source_filename": "zone 5 level 3a.mp4",
        "data_ringan_name": "zone 5 level 3a_ringan.mp4",
        "alias_data_name": "zona 5 level 3a_ringan.mp4",
        "hasil_stem": "z5l3a_pembagian_3digit_1digit_873_bagi_3_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l3"),
        "so_dest_stem": "z5l3a_pembagian_873_bagi_3_marcia",
        "title": "Zona 5 Level 3a: Pembagian 3-Digit dengan 1-Digit (873 : 3 = 291)",
        "subtitle": "Pembagian 3 digit dengan 1 digit secara konkret dan nilai tempat: 800an bagi 3 sisa 200an, 27 puluhan bagi 3 dapat 90an, 3 satuan bagi 3 dapat 1.",
        "duration": 46.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.50,
                "text": "Berapa delapan ratus tujuh puluh tiga dibagi tiga?",
                "display_text": "Berapa 873 dibagi 3?",
                "visual": "Menampilkan soal 873 : 3"
            },
            {
                "id": 2,
                "start": 3.60,
                "end": 6.80,
                "text": "Di sini ratusannya ada delapan.",
                "display_text": "Di sini ratusannya ada 8.",
                "visual": "Menunjuk angka 8 pada posisi ratusan"
            },
            {
                "id": 3,
                "start": 7.00,
                "end": 13.80,
                "text": "Delapan ratusan ini kalau kita bagi tiga, tentu hasilnya dua ratusan, tapi masih sisa dua ratusan.",
                "display_text": "8 ratusan bagi 3 hasilnya 2 ratusan, sisa 2 ratusan.",
                "visual": "Menulis angka 2 pada hasil ratusan dan sisa 2"
            },
            {
                "id": 4,
                "start": 13.90,
                "end": 21.00,
                "text": "Nah, kemudian dua ratusan ini dengan tujuh puluhan akan membentuk dua puluh tujuh puluhan.",
                "display_text": "2 ratusan dan 7 puluhan membentuk 27 puluhan.",
                "visual": "Menggabungkan sisa 2 dengan angka 7 menjadi 27 puluhan"
            },
            {
                "id": 5,
                "start": 21.20,
                "end": 26.50,
                "text": "Dua puluh tujuh puluhan ini kalau dibagi tiga, hasilnya adalah sembilan puluhan.",
                "display_text": "27 puluhan dibagi 3 adalah 9 puluhan.",
                "visual": "Menulis angka 9 pada posisi puluhan hasil"
            },
            {
                "id": 6,
                "start": 26.80,
                "end": 31.80,
                "text": "Nah, kemudian sisanya adalah nol puluhan.",
                "display_text": "Sisanya adalah 0 puluhan.",
                "visual": "Menunjukkan sisa pembagian 27 : 3 adalah 0"
            },
            {
                "id": 7,
                "start": 32.00,
                "end": 37.80,
                "text": "Kemudian nol puluhan dan tiga satuan membentuk tiga satuan, kalau dibagi tiga hasilnya adalah satu satuan.",
                "display_text": "3 satuan dibagi 3 hasilnya 1 satuan.",
                "visual": "Menulis angka 1 pada posisi satuan hasil"
            },
            {
                "id": 8,
                "start": 38.00,
                "end": 43.50,
                "text": "Sehingga delapan ratus tujuh puluh tiga dibagi tiga adalah dua ratus sembilan puluh satu.",
                "display_text": "Sehingga 873 dibagi 3 adalah 291.",
                "visual": "Kesimpulan hasil akhir 873 : 3 = 291"
            }
        ]
    },

    # 2. Zona 5 Level 3b
    {
        "id": "z5l3b_pembagian_bersisa_167_bagi_4",
        "source_filename": "zona 5 level 3b.mp4",
        "data_ringan_name": "zona 5 level 3b_ringan.mp4",
        "alias_data_name": None,
        "hasil_stem": "z5l3b_pembagian_bersisa_167_bagi_4_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l3"),
        "so_dest_stem": "z5l3b_pembagian_167_bagi_4_marcia",
        "title": "Zona 5 Level 3b: Pembagian 3-Digit Bersisa (167 : 4 = 41 sisa 3)",
        "subtitle": "Pembagian 3 digit dengan 1 digit yang menghasilkan sisa: 16 puluhan bagi 4 dapat 4 puluhan, 7 satuan bagi 4 dapat 1 satuan sisa 3.",
        "duration": 58.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.00,
                "text": "Berapa seratus enam puluh tujuh dibagi empat?",
                "display_text": "Berapa 167 dibagi 4?",
                "visual": "Menuliskan soal 167 : 4"
            },
            {
                "id": 2,
                "start": 3.20,
                "end": 10.50,
                "text": "Di sini kita buat dulu nilai tempat hasilnya, yaitu ratusan, puluhan, dan satuan.",
                "display_text": "Buat nilai tempat: ratusan, puluhan, satuan.",
                "visual": "Menulis label R P S di atas tempat jawaban"
            },
            {
                "id": 3,
                "start": 10.80,
                "end": 13.40,
                "text": "Kita lihat di sini ratusannya.",
                "display_text": "Kita lihat ratusannya.",
                "visual": "Menunjuk angka 1 pada ratusan"
            },
            {
                "id": 4,
                "start": 13.60,
                "end": 17.50,
                "text": "Ratusannya satu, dibagi empat adalah nol.",
                "display_text": "1 dibagi 4 adalah 0.",
                "visual": "Menulis 0 pada ratusan hasil"
            },
            {
                "id": 5,
                "start": 17.80,
                "end": 20.00,
                "text": "Sisanya adalah satu ratusan.",
                "display_text": "Sisanya 1 ratusan.",
                "visual": "Menulis sisa 1 di samping ratusan"
            },
            {
                "id": 6,
                "start": 20.20,
                "end": 25.20,
                "text": "Nah, satu ratusan ini akan bergabung dengan enam puluhan membentuk enam belas puluhan.",
                "display_text": "1 ratusan dan 6 puluhan membentuk 16 puluhan.",
                "visual": "Menggabungkan sisa 1 dengan 6 menjadi 16 puluhan"
            },
            {
                "id": 7,
                "start": 25.40,
                "end": 29.20,
                "text": "Enam belas puluhan dibagi empat adalah empat puluhan.",
                "display_text": "16 puluhan dibagi 4 adalah 4 puluhan.",
                "visual": "Menulis angka 4 pada puluhan hasil"
            },
            {
                "id": 8,
                "start": 29.40,
                "end": 32.60,
                "text": "Sisanya adalah nol puluhan.",
                "display_text": "Sisanya 0 puluhan.",
                "visual": "Menunjukkan sisa 0 puluhan"
            },
            {
                "id": 9,
                "start": 32.90,
                "end": 38.00,
                "text": "Nol puluhan ini akan bergabung dengan tujuh satuan membentuk tujuh satuan.",
                "display_text": "0 puluhan dan 7 satuan membentuk 7 satuan.",
                "visual": "Menunjuk angka 7 pada satuan"
            },
            {
                "id": 10,
                "start": 38.20,
                "end": 42.20,
                "text": "Dan tujuh satuan dibagi empat adalah satu satuan.",
                "display_text": "7 satuan dibagi 4 adalah 1 satuan.",
                "visual": "Menulis angka 1 pada satuan hasil"
            },
            {
                "id": 11,
                "start": 42.50,
                "end": 45.80,
                "text": "Sisanya adalah tiga satuan.",
                "display_text": "Sisanya 3 satuan.",
                "visual": "Menulis sisa 3"
            },
            {
                "id": 12,
                "start": 46.00,
                "end": 51.00,
                "text": "Sehingga seratus enam puluh tujuh dibagi empat adalah empat puluh satu,",
                "display_text": "Sehingga 167 dibagi 4 adalah 41,",
                "visual": "Menegaskan hasil 41"
            },
            {
                "id": 13,
                "start": 51.50,
                "end": 55.20,
                "text": "sisanya tiga.",
                "display_text": "sisanya 3.",
                "visual": "Menuliskan keterangan sisa 3"
            }
        ]
    },

    # 3. Zona 5 Level 3c
    {
        "id": "z5l3c_pembagian_puluhan_nol_818_bagi_8",
        "source_filename": "zona 5 level 3c.mp4",
        "data_ringan_name": "zona 5 level 3c_ringan.mp4",
        "alias_data_name": None,
        "hasil_stem": "z5l3c_pembagian_puluhan_nol_818_bagi_8_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l3"),
        "so_dest_stem": "z5l3c_pembagian_818_bagi_8_marcia",
        "title": "Zona 5 Level 3c: Pembagian Puluhan Nol (818 : 8 = 102 sisa 2)",
        "subtitle": "Pembagian 3 digit yang menghasilkan angka nol di posisi puluhan: 8 ratusan bagi 8 dapat 1, 1 puluhan bagi 8 dapat 0 sisa 1, 18 satuan bagi 8 dapat 2 sisa 2.",
        "duration": 59.50,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.20,
                "text": "Delapan ratus delapan belas dibagi delapan.",
                "display_text": "818 dibagi 8.",
                "visual": "Menuliskan soal 818 : 8"
            },
            {
                "id": 2,
                "start": 3.40,
                "end": 10.20,
                "text": "Pertama kita buat dulu nilai tempat hasilnya, yaitu ratusan, puluhan, dan satuan.",
                "display_text": "Buat nilai tempat: ratusan, puluhan, satuan.",
                "visual": "Menulis nilai tempat R P S"
            },
            {
                "id": 3,
                "start": 10.60,
                "end": 19.40,
                "text": "Lalu kita bagi ratusannya. Delapan ratusan dibagi delapan adalah satu ratusan, sisanya nol ratusan.",
                "display_text": "8 ratusan bagi 8 adalah 1 ratusan, sisa 0.",
                "visual": "Menulis 1 pada ratusan hasil"
            },
            {
                "id": 4,
                "start": 19.60,
                "end": 24.80,
                "text": "Nah, kemudian nol ratusan dan satu puluhan ini akan bergabung menjadi satu puluhan.",
                "display_text": "0 ratusan dan 1 puluhan menjadi 1 puluhan.",
                "visual": "Menunjuk 1 puluhan"
            },
            {
                "id": 5,
                "start": 24.80,
                "end": 33.20,
                "text": "Kemudian satu puluhan ini dibagi delapan adalah nol puluhan, sisanya satu puluhan.",
                "display_text": "1 puluhan bagi 8 adalah 0 puluhan, sisa 1 puluhan.",
                "visual": "Menulis 0 pada puluhan hasil dan sisa 1"
            },
            {
                "id": 6,
                "start": 33.80,
                "end": 39.00,
                "text": "Satu puluhan ini akan bergabung dengan delapan satuan membentuk delapan belas satuan.",
                "display_text": "1 puluhan dan 8 satuan membentuk 18 satuan.",
                "visual": "Menggabungkan sisa 1 dengan 8 menjadi 18 satuan"
            },
            {
                "id": 7,
                "start": 39.30,
                "end": 46.80,
                "text": "Delapan belas satuan dibagi delapan adalah dua satuan, sisanya dua satuan.",
                "display_text": "18 satuan bagi 8 adalah 2 satuan, sisa 2 satuan.",
                "visual": "Menulis angka 2 pada satuan hasil dan sisa 2"
            },
            {
                "id": 8,
                "start": 47.00,
                "end": 56.20,
                "text": "Jadi delapan ratus delapan belas kalau kita bagi delapan, hasilnya adalah seratus dua, sisanya dua.",
                "display_text": "Jadi 818 dibagi 8 hasilnya 102, sisa 2.",
                "visual": "Kesimpulan hasil akhir 818 : 8 = 102 sisa 2"
            }
        ]
    },

    # 4. Zona 5 Level 4a
    {
        "id": "z5l4a_pembagian_pembagi_11_453_bagi_11",
        "source_filename": "zona 5 level 4a.mp4",
        "data_ringan_name": "zona 5 level 4a_ringan.mp4",
        "alias_data_name": None,
        "hasil_stem": "z5l4a_pembagian_pembagi_11_453_bagi_11_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l4"),
        "so_dest_stem": "z5l4a_pembagian_453_bagi_11_marcia",
        "title": "Zona 5 Level 4a: Pembagian Pembagi 2-Digit / Tabel 11 (453 : 11 = 41 sisa 2)",
        "subtitle": "Metode tabel perkalian bantu 11 untuk membagi bilangan ratusan dengan pembagi 2 digit: 45 bagi 11 dapat 4 sisa 1, 13 bagi 11 dapat 1 sisa 2.",
        "duration": 96.00,
        "segments": [
            {
                "id": 1,
                "start": 0.80,
                "end": 3.00,
                "text": "Empat ratus lima puluh tiga dibagi sebelas.",
                "display_text": "453 dibagi 11.",
                "visual": "Menuliskan soal 453 : 11"
            },
            {
                "id": 2,
                "start": 3.10,
                "end": 6.80,
                "text": "Untuk menghitung ini, kita harus tahu perkalian dengan sebelas.",
                "display_text": "Kita harus tahu perkalian 11.",
                "visual": "Menjelaskan pentingnya perkalian 11"
            },
            {
                "id": 3,
                "start": 7.00,
                "end": 11.20,
                "text": "Bagi yang belum tahu perkalian sebelas, kita buat dulu tabel perkalian sebelas.",
                "display_text": "Kita buat dulu tabel perkalian 11.",
                "visual": "Mulai menulis deret penjumlahan berulang 11"
            },
            {
                "id": 4,
                "start": 11.30,
                "end": 24.30,
                "text": "Sebelas tambah sebelas dua puluh dua, tambah sebelas lagi tiga puluh tiga, tambah sebelas lagi empat puluh empat, dan seterusnya sampai seratus sepuluh, yaitu sepuluh kali lipat dari sebelas.",
                "display_text": "11 + 11 = 22, + 11 = 33, + 11 = 44, ... sampai 110.",
                "visual": "Menuliskan deret kelipatan 11 sampai 110 di sisi papan"
            },
            {
                "id": 5,
                "start": 24.30,
                "end": 33.50,
                "text": "Nah, ini kita beri nama dua, lalu tiga artinya tiga kali sebelas tiga puluh tiga, kemudian empat, lima, enam,",
                "display_text": "Beri nomor pengali 2, 3 (3x11=33), 4, 5, 6,",
                "visual": "Memberi nomor urut pengali di samping kelipatan"
            },
            {
                "id": 6,
                "start": 33.80,
                "end": 43.50,
                "text": "kemudian ini tujuh, tujuh kali sebelas tujuh puluh tujuh, delapan, dan sembilan. Ini tentu sepuluh.",
                "display_text": "7 (7x11=77), 8, 9, dan 10.",
                "visual": "Melengkapi nomor urut pengali sampai 10"
            },
            {
                "id": 7,
                "start": 43.80,
                "end": 49.70,
                "text": "Nah, setelah itu kita langsung menghitung. Kita ambil langsung saja dua digit, tapi ke belakangnya harus satu digit, satu digit ya.",
                "display_text": "Ambil 2 digit pertama (45), selanjutnya 1 digit.",
                "visual": "Menandai 2 digit pertama 45 pada soal"
            },
            {
                "id": 8,
                "start": 49.70,
                "end": 58.00,
                "text": "Empat puluh lima dibagi sebelas, kita cari berapa kali sebelas yang mendekati empat puluh lima, tentu ini empat puluh empat.",
                "display_text": "45 bagi 11: cari kelipatan mendekati 45, yaitu 44.",
                "visual": "Menunjuk angka 44 pada tabel perkalian"
            },
            {
                "id": 9,
                "start": 58.50,
                "end": 61.00,
                "text": "Jadi empat puluh empat adalah empat.",
                "display_text": "44 adalah pengali 4.",
                "visual": "Menunjuk pengali 4 pada tabel"
            },
            {
                "id": 10,
                "start": 61.30,
                "end": 66.80,
                "text": "Jadi di sini kita tulis empat, kemudian empat kali sebelas kan empat puluh empat.",
                "display_text": "Tulis 4 pada hasil. 4 x 11 = 44.",
                "visual": "Menulis angka 4 pada digit pertama hasil"
            },
            {
                "id": 11,
                "start": 67.00,
                "end": 72.00,
                "text": "Jadi kita punya empat puluh lima, sisanya adalah empat puluh lima dikurang empat puluh empat, yaitu satu.",
                "display_text": "Sisa: 45 - 44 = 1.",
                "visual": "Menuliskan sisa 1 di depan angka 3 berikutnya"
            },
            {
                "id": 12,
                "start": 72.40,
                "end": 77.50,
                "text": "Nah, berikutnya tiga belas kita bagi dengan sebelas, tentu satu.",
                "display_text": "13 dibagi 11 adalah 1.",
                "visual": "Menulis angka 1 pada digit kedua hasil"
            },
            {
                "id": 13,
                "start": 77.60,
                "end": 83.80,
                "text": "Sisanya adalah tentu tiga belas dikurang sebelas, yaitu sisa dua.",
                "display_text": "Sisa: 13 - 11 = 2.",
                "visual": "Menghitung sisa 2"
            },
            {
                "id": 14,
                "start": 84.00,
                "end": 92.50,
                "text": "Jadi empat ratus lima puluh tiga kalau kita bagi sebelas, hasilnya adalah empat puluh satu sisa dua.",
                "display_text": "Jadi 453 : 11 = 41 sisa 2.",
                "visual": "Kesimpulan hasil akhir 41 sisa 2"
            }
        ]
    },

    # 5. Zona 5 Level 4b
    {
        "id": "z5l4b_pembagian_pembagi_15_2345_bagi_15",
        "source_filename": "zona 5 level 4b.mp4",
        "data_ringan_name": "zona 5 level 4b_ringan.mp4",
        "alias_data_name": None,
        "hasil_stem": "z5l4b_pembagian_pembagi_15_2345_bagi_15_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l4"),
        "so_dest_stem": "z5l4b_pembagian_2345_bagi_15_marcia",
        "title": "Zona 5 Level 4b: Pembagian 4-Digit dengan Pembagi 15 (2345 : 15 = 156 sisa 5)",
        "subtitle": "Metode tabel bantu kelipatan 15 untuk pembagian 4 digit: 23 ratusan bagi 15 dapat 1 sisa 8, 84 puluhan bagi 15 dapat 5 sisa 9, 95 satuan bagi 15 dapat 6 sisa 5.",
        "duration": 107.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.80,
                "text": "Kita akan hitung dua ribu tiga ratus empat puluh lima dibagi lima belas.",
                "display_text": "Kita akan hitung 2345 dibagi 15.",
                "visual": "Menuliskan soal 2345 : 15"
            },
            {
                "id": 2,
                "start": 3.90,
                "end": 7.80,
                "text": "Langkah pertama adalah kita buat dulu tabel perkalian lima belas.",
                "display_text": "Langkah pertama: buat tabel perkalian 15.",
                "visual": "Mulai membuat tabel kelipatan 15"
            },
            {
                "id": 3,
                "start": 7.90,
                "end": 11.00,
                "text": "Caranya ada lima belas ditambah lima belas, tiga puluh.",
                "display_text": "15 + 15 = 30.",
                "visual": "Menulis 15 dan 30"
            },
            {
                "id": 4,
                "start": 11.20,
                "end": 13.80,
                "text": "Kemudian kita tambahkan lima belas, empat puluh lima.",
                "display_text": "+ 15 = 45.",
                "visual": "Menulis 45"
            },
            {
                "id": 5,
                "start": 14.00,
                "end": 18.00,
                "text": "Tambahkan lima belas lagi, enam puluh, dan seterusnya.",
                "display_text": "+ 15 lagi = 60, dan seterusnya.",
                "visual": "Menulis 60 dan melanjutkan deret"
            },
            {
                "id": 6,
                "start": 18.30,
                "end": 23.20,
                "text": "Kemudian kita tulis di sini satu, yang menunjukkan satu kali lima belas sama dengan lima belas.",
                "display_text": "Tulis 1 (1 x 15 = 15).",
                "visual": "Memberi nomor pengali 1"
            },
            {
                "id": 7,
                "start": 23.30,
                "end": 26.00,
                "text": "Ini dua, kemudian tiga.",
                "display_text": "Ini 2, kemudian 3.",
                "visual": "Memberi nomor 2 dan 3"
            },
            {
                "id": 8,
                "start": 26.40,
                "end": 29.80,
                "text": "Ini empat kali lima belas sama dengan enam puluh.",
                "display_text": "4 x 15 = 60.",
                "visual": "Memberi nomor 4 di samping 60"
            },
            {
                "id": 9,
                "start": 30.20,
                "end": 34.60,
                "text": "Lima kali lima belas sama dengan tujuh puluh lima, dan seterusnya.",
                "display_text": "5 x 15 = 75, dan seterusnya.",
                "visual": "Melengkapi tabel kelipatan 15"
            },
            {
                "id": 10,
                "start": 34.80,
                "end": 42.50,
                "text": "Kemudian kita ambil di sini dua puluh tiga ratusan. Kita bagi dengan lima belas tentu satu, sisanya tentu delapan.",
                "display_text": "23 ratusan bagi 15 dapat 1, sisa 8.",
                "visual": "Menulis 1 pada ratusan hasil dan sisa 8"
            },
            {
                "id": 11,
                "start": 42.80,
                "end": 51.80,
                "text": "Nah, ini adalah ratusan. Jadi kita punya sisa delapan ratusan akan bergabung dengan empat puluhan membentuk delapan puluh empat puluhan.",
                "display_text": "Sisa 8 ratusan dan 4 puluhan membentuk 84 puluhan.",
                "visual": "Menggabungkan sisa 8 dengan 4 menjadi 84"
            },
            {
                "id": 12,
                "start": 52.10,
                "end": 61.80,
                "text": "Delapan puluh empat puluhan kalau kita bagi lima belas, cari bilangan yang dikalikan lima belas mendekati delapan puluh empat, jawabannya adalah tujuh puluh lima.",
                "display_text": "84 bagi 15: cari kelipatan mendekati 84, yaitu 75.",
                "visual": "Menunjuk angka 75 pada tabel"
            },
            {
                "id": 13,
                "start": 62.20,
                "end": 66.00,
                "text": "Jadi di sini lima, berarti puluhannya ada lima.",
                "display_text": "Jadi di sini 5 (puluhan ada 5).",
                "visual": "Menulis angka 5 pada puluhan hasil"
            },
            {
                "id": 14,
                "start": 66.20,
                "end": 71.00,
                "text": "Nah, kemudian sisanya berapa? Delapan puluh empat dikurang tujuh puluh lima, yaitu sembilan.",
                "display_text": "Sisa: 84 - 75 = 9.",
                "visual": "Menghitung sisa 9"
            },
            {
                "id": 15,
                "start": 71.70,
                "end": 80.00,
                "text": "Berikutnya sembilan puluhan ini akan bergabung dengan lima satuan menjadi sembilan puluh lima satuan.",
                "display_text": "9 puluhan dan 5 satuan menjadi 95 satuan.",
                "visual": "Menggabungkan sisa 9 dengan 5 menjadi 95"
            },
            {
                "id": 16,
                "start": 80.30,
                "end": 87.50,
                "text": "Kalau kita bagi lima belas, hasilnya adalah di sini, yaitu enam satuan. Sisanya berapa?",
                "display_text": "95 bagi 15 dapat 6 satuan. Sisanya berapa?",
                "visual": "Menulis 6 pada satuan hasil"
            },
            {
                "id": 17,
                "start": 87.90,
                "end": 93.30,
                "text": "Tentu sembilan puluh lima dikurang sembilan puluh, yaitu sisanya adalah lima.",
                "display_text": "95 - 90 = sisa 5.",
                "visual": "Menghitung sisa 5"
            },
            {
                "id": 18,
                "start": 93.50,
                "end": 101.00,
                "text": "Jadi dua ribu tiga ratus empat puluh lima kalau kita bagi lima belas, hasilnya adalah seratus lima puluh enam,",
                "display_text": "Jadi 2345 : 15 = 156,",
                "visual": "Menegaskan hasil 156"
            },
            {
                "id": 19,
                "start": 101.20,
                "end": 103.60,
                "text": "sisanya lima.",
                "display_text": "sisanya 5.",
                "visual": "Menuliskan keterangan sisa 5"
            }
        ]
    },

    # 6. Zona 5 Level 5
    {
        "id": "z5l5_trik_pembagian_cepat_10_100_1000",
        "source_filename": "zona 5 level 5.mp4",
        "data_ringan_name": "zona 5 level 5_ringan.mp4",
        "alias_data_name": None,
        "hasil_stem": "z5l5_trik_pembagian_cepat_10_100_1000_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l5"),
        "so_dest_stem": "z5l5_trik_pembagian_cepat_marcia",
        "title": "Zona 5 Level 5: Trik Pembagian Cepat dengan 10, 100, 5, 25, 125, 250",
        "subtitle": "Trik cerdas pembagian cepat: bagi 5 ubah jadi kali 2 bagi 10, bagi 25 ubah jadi kali 4 bagi 100, bagi 125 ubah jadi kali 8 bagi 1000.",
        "duration": 145.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 4.20,
                "text": "Coba kita hitung ini dengan trik pembagian cepat.",
                "display_text": "Trik pembagian cepat.",
                "visual": "Menampilkan deretan soal pembagian cepat"
            },
            {
                "id": 2,
                "start": 4.50,
                "end": 12.00,
                "text": "Empat ratus lima puluh lima dibagi sepuluh adalah empat puluh lima, sisanya lima.",
                "display_text": "455 : 10 = 45 sisa 5.",
                "visual": "Menulis hasil 45 sisa 5"
            },
            {
                "id": 3,
                "start": 12.70,
                "end": 17.80,
                "text": "Karena di sini empat ratus lima puluh dibagi sepuluh adalah empat puluh lima, sisanya tentu lima.",
                "display_text": "Karena 450 : 10 = 45, sisanya 5.",
                "visual": "Menjelaskan konsep pemisahan nilai tempat"
            },
            {
                "id": 4,
                "start": 18.00,
                "end": 26.50,
                "text": "Nah, untuk tujuh ribu delapan ratus lima puluh tiga dibagi seratus adalah tujuh puluh delapan, sisanya adalah lima puluh tiga.",
                "display_text": "7853 : 100 = 78 sisa 53.",
                "visual": "Menulis hasil 78 sisa 53"
            },
            {
                "id": 5,
                "start": 26.60,
                "end": 36.80,
                "text": "Karena di sini kita lihat tujuh puluh delapan kali seratus adalah tujuh ribu delapan ratus, ditambah sisanya lima puluh tiga, jadi tujuh ribu delapan ratus lima puluh tiga.",
                "display_text": "78 x 100 = 7800 + 53 = 7853.",
                "visual": "Menjelaskan relasi perkalian seratus"
            },
            {
                "id": 6,
                "start": 37.00,
                "end": 43.80,
                "text": "Nah, kalau empat ratus tujuh puluh delapan dibagi lima, kita kalikan dulu empat ratus tujuh puluh delapan dengan dua.",
                "display_text": "478 : 5 -> kalikan 478 dengan 2.",
                "visual": "Menulis langkah x 2 untuk pembagian 5"
            },
            {
                "id": 7,
                "start": 44.00,
                "end": 49.30,
                "text": "Jadi ini hasilnya sembilan ratus lima puluh enam, kita bagi dengan sepuluh.",
                "display_text": "Hasilnya 956, lalu bagi 10.",
                "visual": "Menulis 956 : 10"
            },
            {
                "id": 8,
                "start": 49.70,
                "end": 55.00,
                "text": "Nah, hasilnya sembilan puluh lima, sisanya enam.",
                "display_text": "Hasilnya 95 sisa 6.",
                "visual": "Menulis 95 sisa 6"
            },
            {
                "id": 9,
                "start": 55.50,
                "end": 66.80,
                "text": "Nah, kalau pembagian dua puluh lima ini paling cepat adalah kita kalikan dulu empat ribu tujuh ratus delapan puluh empat dengan empat, kemudian kita bagi dengan seratus.",
                "display_text": "4784 : 25 -> kalikan 4 lalu bagi 100.",
                "visual": "Menulis trik pembagian 25 dengan x 4 : 100"
            },
            {
                "id": 10,
                "start": 67.10,
                "end": 73.80,
                "text": "Jadi kalau empat ribu tujuh ratus delapan puluh empat dikali empat, hasilnya adalah sembilan belas ribu seratus tiga puluh enam.",
                "display_text": "4784 x 4 = 19136.",
                "visual": "Menulis hasil perkalian 19136"
            },
            {
                "id": 11,
                "start": 74.40,
                "end": 82.50,
                "text": "Kalau kita bagi seratus, hasilnya adalah seratus sembilan puluh satu, sisa tiga puluh enam.",
                "display_text": "Bagi 100 = 191 sisa 36.",
                "visual": "Menulis hasil 191 sisa 36"
            },
            {
                "id": 12,
                "start": 83.50,
                "end": 94.20,
                "text": "Berikutnya lima ribu seratus tujuh puluh delapan dibagi seratus dua puluh lima, ini cara cepatnya adalah lima ribu seratus tujuh puluh delapan kita kalikan dengan delapan, kemudian kita bagi dengan seribu.",
                "display_text": "5178 : 125 -> kalikan 8 lalu bagi 1000.",
                "visual": "Menulis trik pembagian 125 dengan x 8 : 1000"
            },
            {
                "id": 13,
                "start": 94.60,
                "end": 102.00,
                "text": "Nah, lima ribu seratus tujuh puluh delapan dikali delapan adalah empat puluh satu ribu empat ratus dua puluh empat.",
                "display_text": "5178 x 8 = 41424.",
                "visual": "Menulis hasil 41424"
            },
            {
                "id": 14,
                "start": 102.40,
                "end": 111.00,
                "text": "Kalau ini kita bagi seribu, maka hasilnya adalah empat puluh satu, sisanya empat ratus dua puluh empat.",
                "display_text": "Bagi 1000 = 41 sisa 424.",
                "visual": "Menulis 41 sisa 424"
            },
            {
                "id": 15,
                "start": 111.80,
                "end": 123.50,
                "text": "Nah, bagaimana dengan seribu dua ratus tiga puluh enam dibagi dua ratus lima puluh? Ini sama saja, dengan seribu dua ratus tiga puluh enam kita kalikan empat dibagi dengan seribu.",
                "display_text": "1236 : 250 -> kalikan 4 lalu bagi 1000.",
                "visual": "Menulis trik pembagian 250 dengan x 4 : 1000"
            },
            {
                "id": 16,
                "start": 123.80,
                "end": 133.30,
                "text": "Nah, kita tahu seribu dua ratus tiga puluh enam dikali empat adalah empat ribu sembilan ratus empat puluh empat, kemudian kita bagi dengan seribu.",
                "display_text": "1236 x 4 = 4944, lalu bagi 1000.",
                "visual": "Menulis 4944 : 1000"
            },
            {
                "id": 17,
                "start": 133.30,
                "end": 141.40,
                "text": "Hasilnya adalah empat, sisanya adalah sembilan ratus empat puluh empat.",
                "display_text": "Hasilnya 4 sisa 944.",
                "visual": "Kesimpulan hasil 4 sisa 944"
            }
        ]
    },

    # 7. Zone 5 Level 6
    {
        "id": "z5l6_pembagian_pembagi_3digit_38273_bagi_121",
        "source_filename": "zone 5 level 6.mp4",
        "data_ringan_name": "zone 5 level 6_ringan.mp4",
        "alias_data_name": "zona 5 level 6_ringan.mp4",
        "hasil_stem": "z5l6_pembagian_pembagi_3digit_38273_bagi_121_marcia",
        "so_dir": os.path.join(SO_BASE_DIR, "z5l6"),
        "so_dest_stem": "z5l6_pembagian_38273_bagi_121_marcia",
        "title": "Zona 5 Level 6: Pembagian Bilangan Besar dengan Pembagi 3-Digit (38273 : 121 = 316 sisa 37)",
        "subtitle": "Metode tabel perkalian bantu 121 untuk membagi bilangan 5 digit: 382 bagi 121 dapat 3 sisa 19, 197 bagi 121 dapat 1 sisa 76, 763 bagi 121 dapat 6 sisa 37.",
        "duration": 105.00,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 5.20,
                "text": "Sekarang kita hitung tiga puluh delapan ribu dua ratus tujuh puluh tiga dibagi seratus dua puluh satu.",
                "display_text": "Sekarang kita hitung 38273 dibagi 121.",
                "visual": "Menuliskan soal 38273 : 121"
            },
            {
                "id": 2,
                "start": 5.40,
                "end": 9.00,
                "text": "Tentu pertama kita bikin tabel perkalian seratus dua puluh satu.",
                "display_text": "Pertama kita buat tabel perkalian 121.",
                "visual": "Mulai menulis deret penjumlahan 121"
            },
            {
                "id": 3,
                "start": 9.10,
                "end": 22.00,
                "text": "Di sini seratus dua puluh satu tambah seratus dua puluh satu, dua ratus empat puluh dua, tambah seratus dua puluh satu, tiga ratus enam puluh tiga, tambah seratus dua puluh satu, empat ratus delapan puluh empat, dan seterusnya.",
                "display_text": "121 + 121 = 242, + 121 = 363, + 121 = 484, dan seterusnya.",
                "visual": "Menuliskan kelipatan 121 di sisi papan"
            },
            {
                "id": 4,
                "start": 22.00,
                "end": 32.00,
                "text": "Kemudian kita tulis di sini satu, yaitu menunjukkan satu kali seratus dua puluh satu adalah seratus dua puluh satu, ini dua, tiga, dan seterusnya.",
                "display_text": "Tulis nomor pengali 1, 2, 3, dan seterusnya.",
                "visual": "Memberi nomor pengali di samping kelipatan"
            },
            {
                "id": 5,
                "start": 32.30,
                "end": 37.20,
                "text": "Kemudian kita ambil tiga digit pertama, di sini dibagi seratus dua puluh satu.",
                "display_text": "Ambil 3 digit pertama (382) dibagi 121.",
                "visual": "Menandai 3 digit pertama 382"
            },
            {
                "id": 6,
                "start": 37.30,
                "end": 43.80,
                "text": "Cari seratus dua puluh satu kali berapa sama dengan tiga ratus delapan puluh dua atau mendekati tiga ratus delapan puluh dua.",
                "display_text": "Cari kelipatan 121 mendekati 382.",
                "visual": "Mencocokkan ke tabel perkalian"
            },
            {
                "id": 7,
                "start": 44.00,
                "end": 46.80,
                "text": "Nah, di sini yang tepat adalah tiga.",
                "display_text": "Yang tepat adalah 3 (3 x 121 = 363).",
                "visual": "Menulis angka 3 pada hasil"
            },
            {
                "id": 8,
                "start": 47.10,
                "end": 54.40,
                "text": "Sisanya adalah tiga ratus delapan puluh dua dikurang tiga ratus enam puluh tiga, yaitu sembilan belas.",
                "display_text": "Sisa: 382 - 363 = 19.",
                "visual": "Menghitung sisa 19"
            },
            {
                "id": 9,
                "start": 54.60,
                "end": 59.50,
                "text": "Nah, kemudian kita punya seratus sembilan puluh tujuh, kita bagi dengan seratus dua puluh satu.",
                "display_text": "197 dibagi 121.",
                "visual": "Menggabungkan sisa 19 dengan 7 menjadi 197"
            },
            {
                "id": 10,
                "start": 59.90,
                "end": 68.00,
                "text": "Tentu hasilnya satu, sisanya adalah seratus sembilan puluh tujuh dikurang seratus dua puluh satu, yaitu tujuh puluh enam.",
                "display_text": "Dapat 1, sisa: 197 - 121 = 76.",
                "visual": "Menulis angka 1 pada hasil dan menghitung sisa 76"
            },
            {
                "id": 11,
                "start": 68.20,
                "end": 75.30,
                "text": "Nah, sekarang kita punya tujuh ratus enam puluh tiga dibagi dengan seratus dua puluh satu, tentu hasilnya di sini enam.",
                "display_text": "763 dibagi 121 adalah 6.",
                "visual": "Menggabungkan 76 dengan 3 menjadi 763, hasil dapat 6"
            },
            {
                "id": 12,
                "start": 75.30,
                "end": 84.00,
                "text": "Kita tulis di sini enam. Nah, sisanya adalah tujuh ratus enam puluh tiga dikurang tujuh ratus dua puluh enam, yaitu tiga puluh tujuh.",
                "display_text": "Tulis 6. Sisa: 763 - 726 = 37.",
                "visual": "Menulis angka 6 pada hasil dan menghitung sisa 37"
            },
            {
                "id": 13,
                "start": 84.40,
                "end": 96.00,
                "text": "Jadi tiga puluh delapan ribu dua ratus tujuh puluh tiga kalau kita bagi dengan seratus dua puluh satu, hasilnya tiga ratus enam belas, sisanya tiga puluh tujuh.",
                "display_text": "Jadi 38273 : 121 = 316 sisa 37.",
                "visual": "Kesimpulan hasil akhir 38273 : 121 = 316 sisa 37"
            }
        ]
    }
]

def run_ffmpeg(cmd, desc="ffmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error during {desc}:")
        print(res.stderr[-600:])
        sys.exit(1)
    return res

def get_audio_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

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

async def synthesize_edge_segment(text: str, output_path: str):
    import edge_tts
    comm = edge_tts.Communicate(text=text, voice="id-ID-GadisNeural", rate="+4%", pitch="+2Hz")
    await comm.save(output_path)

async def process_video(cfg, get_engine_fn, marcia_ref, marcia_ref_text):
    vid_id = cfg["id"]
    source_filename = cfg["source_filename"]
    src_file = os.path.join(DATA_VIDEO_DIR, source_filename)
    total_dur = cfg["duration"]
    segments = cfg["segments"]

    print("\n" + "="*80)
    print(f"🎬 MEMPROSES: {cfg['title']}")
    print(f"   Sumber File: {src_file} ({total_dur:.2f}s, {len(segments)} segmen ucapan)")
    print("="*80)

    if not os.path.exists(src_file):
        print(f"❌ File sumber tidak ditemukan: {src_file}")
        sys.exit(1)

    project_dir = os.path.join(VIDEO_PROJECTS_DIR, vid_id)
    segments_dir = os.path.join(project_dir, "segments")
    frames_dir = os.path.join(project_dir, "frames")
    os.makedirs(segments_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    if cfg.get("so_dir"):
        os.makedirs(cfg["so_dir"], exist_ok=True)

    # 1. Copy original video
    clip_orig = os.path.join(project_dir, "clip_original.mp4")
    shutil.copyfile(src_file, clip_orig)

    # 2. Extract original audio 24k
    orig_wav = os.path.join(project_dir, "original_audio_24k.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
        orig_wav
    ], "Extract 24k audio")
    orig_dur = get_audio_duration(orig_wav)

    # Calculate freeze frame duration
    freeze_dur = max(0.0, total_dur - orig_dur)
    print(f"   ⏱️ Durasi Asli: {orig_dur:.2f}s | Target Canvas: {total_dur:.2f}s | Freeze Frame Akhir: {freeze_dur:.2f}s")

    # 3. Extract 1fps frames for visual scrubber
    print("   📷 Mengekstrak frame visual untuk thumbnail scrubber...")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-vf", "fps=1",
        os.path.join(frames_dir, "frame_%02d.jpg")
    ], "Extract frames")

    # 4. F5-TTS Synthesis
    import librosa
    import soundfile as sf
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"

    print(f"\n▶ Fase 1: Sintesis & Alignment F5-TTS Trainer Marcia ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        is_last = (sid == segments[-1]["id"])
        trim_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_trimmed.wav")
        aligned_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_aligned.wav")

        t0 = time.time()
        if not os.path.exists(trim_f5):
            print(f"  [{sid}/{len(segments)}] F5-TTS Synthesizing: \"{text[:35]}...\"...", end="", flush=True)
            engine = get_engine_fn()
            res_f5 = engine.generate(
                ref_audio_path=marcia_ref,
                ref_text=marcia_ref_text,
                gen_text=text,
                speed=1.05,
                nfe_step=32,
                output_format="wav"
            )
            raw_f5 = os.path.join(BASE_DIR, res_f5["audio_url"].lstrip("/"))
            y, sr = librosa.load(raw_f5, sr=24000)
            y_trim, _ = librosa.effects.trim(y, top_db=25)
            sf.write(trim_f5, y_trim, sr)
            engine.free_gpu_memory()
        else:
            print(f"  [{sid}/{len(segments)}] F5-TTS Cached: \"{text[:35]}...\"...", end="", flush=True)

        y_trim, sr = librosa.load(trim_f5, sr=24000)
        trim_dur = len(y_trim) / sr

        tempo = trim_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        cmd_align = [
            "ffmpeg", "-y", "-i", trim_f5,
            "-af", f"{atempo},{MASTER_FILTER}",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le"
        ]
        # Segmen terakhir tidak di-clip -t agar suku kata penutup tidak terpotong!
        if not is_last:
            cmd_align.extend(["-t", str(target_dur)])
        cmd_align.append(aligned_f5)

        run_ffmpeg(cmd_align, f"Align F5 seg {sid}")
        s["audio_f5"] = f"/video-projects/{vid_id}/segments/f5_seg_{sid}_aligned.wav"
        print(f" ✓ ({time.time()-t0:.2f}s | aktif: {trim_dur:.2f}s -> target: {target_dur:.2f}s)")

    # 5. Edge-TTS Synthesis
    print(f"\n▶ Fase 2: Sintesis & Alignment Edge-TTS Studio ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        is_last = (sid == segments[-1]["id"])
        raw_edge = os.path.join(segments_dir, f"edge_seg_{sid}_raw.mp3")
        aligned_edge = os.path.join(segments_dir, f"edge_seg_{sid}_aligned.wav")

        if not os.path.exists(raw_edge):
            await synthesize_edge_segment(text, raw_edge)
        edge_dur = get_audio_duration(raw_edge)

        tempo = edge_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        cmd_align_edge = [
            "ffmpeg", "-y", "-i", raw_edge,
            "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le"
        ]
        if not is_last:
            cmd_align_edge.extend(["-t", str(target_dur)])
        cmd_align_edge.append(aligned_edge)

        run_ffmpeg(cmd_align_edge, f"Align Edge seg {sid}")
        s["audio_edge"] = f"/video-projects/{vid_id}/segments/edge_seg_{sid}_aligned.wav"

    # 6. Assemble Master Timelines
    print(f"\n▶ Fase 3: Merakit Master Timeline Audio & Video Padded Widescreen ({total_dur:.2f}s)...")
    silence_wav = os.path.join(segments_dir, "silence.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(total_dur),
        silence_wav
    ], "Generate silence")

    # Filter canvas 16:9 murni putih (#FFFFFF) dengan freeze frame akhir
    vf_pad_freeze = f"scale=928:696,pad=1280:720:176:0:color=white,tpad=stop_mode=clone:stop_duration={freeze_dur:.2f}"

    output_files = {}

    for mode in ["f5", "edge"]:
        master_wav = os.path.join(project_dir, f"master_dubbing_{mode}.wav")
        master_mp3 = os.path.join(project_dir, f"master_dubbing_{mode}.mp3")
        video_dubbed = os.path.join(project_dir, f"video_dubbed_marcia_{mode}.mp4")

        inputs = ["-i", silence_wav]
        delays = []
        for idx, s in enumerate(segments):
            seg_path = os.path.join(segments_dir, f"{mode}_seg_{s['id']}_aligned.wav")
            inputs.extend(["-i", seg_path])
            delay_ms = int(s["start"] * 1000)
            delays.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[d{idx+1}]")

        filter_parts = delays
        mix_inputs = "".join([f"[d{i+1}]" for i in range(len(segments))])
        total_in = len(segments) + 1
        filter_parts.append(f"[0:a]{mix_inputs}amix=inputs={total_in}:duration=first:dropout_transition=0,volume=3.0[outa]")
        filter_str = ";".join(filter_parts)

        # Mix master wav (Wajib -ar 44100 pcm_s16le)
        run_ffmpeg([
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[outa]",
            "-t", str(total_dur),
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            master_wav
        ], f"Mix {mode}")

        # Convert master mp3
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", master_wav,
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            master_mp3
        ], f"MP3 {mode}")

        # Mux dubbed video dengan canvas 16:9 putih & freeze frame
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", clip_orig,
            "-i", master_wav,
            "-vf", vf_pad_freeze,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-t", str(total_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            video_dubbed
        ], f"Mux {mode} video")

        output_files[mode] = {
            "video": video_dubbed,
            "audio": master_mp3,
            "master_wav": master_wav
        }

    # 7. Kompresi Video Ringan Berkualitas Tinggi Sesuai Standar SO (Canvas Putih 16:9)
    print(f"\n▶ Fase 4: Optimasi Ukuran File Ringan (H.264 Tune Animation & WebM VP9 Canvas Putih)...")
    orig_size = os.path.getsize(src_file)

    # 7A. Lightweight MP4 (F5)
    f5_light_mp4 = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.mp4")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", output_files["f5"]["master_wav"],
        "-vf", vf_pad_freeze,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", str(total_dur),
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-ar", "44100",
        "-movflags", "+faststart",
        f5_light_mp4
    ], "Encode F5 lightweight MP4")

    # 7B. Lightweight WebM (F5)
    f5_light_webm = os.path.join(project_dir, f"video_dubbed_marcia_f5_ringan.webm")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", f5_light_mp4,
        "-c:v", "libvpx-vp9", "-crf", "35", "-b:v", "0",
        "-c:a", "libopus", "-b:a", "36k",
        f5_light_webm
    ], "Encode F5 lightweight WebM")

    # 7C. Lightweight MP4 (Edge Studio)
    edge_light_mp4 = os.path.join(project_dir, f"video_dubbed_marcia_edge_ringan.mp4")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", clip_orig,
        "-i", output_files["edge"]["master_wav"],
        "-vf", vf_pad_freeze,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", str(total_dur),
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-ar", "44100",
        "-movflags", "+faststart",
        edge_light_mp4
    ], "Encode Edge lightweight MP4")

    # 8. Multi-Destination Synchronization
    print(f"\n▶ Fase 5: Sinkronisasi Multi-Tujuan...")
    # A. Salin ke Data VIdeo Marcia/
    data_ringan_dest = os.path.join(DATA_VIDEO_DIR, cfg["data_ringan_name"])
    shutil.copyfile(f5_light_mp4, data_ringan_dest)
    print(f"   ✓ Disalin ke Data VIdeo Marcia: {data_ringan_dest}")
    if cfg.get("alias_data_name"):
        alias_dest = os.path.join(DATA_VIDEO_DIR, cfg["alias_data_name"])
        shutil.copyfile(f5_light_mp4, alias_dest)
        print(f"   ✓ Alias disalin ke Data VIdeo Marcia: {alias_dest}")

    # B. Salin ke Hasil/videoMarcia/z5_pembagian/
    hasil_stem = cfg["hasil_stem"]
    hasil_mp4 = os.path.join(HASIL_Z5_DIR, f"{hasil_stem}_ringan.mp4")
    hasil_webm = os.path.join(HASIL_Z5_DIR, f"{hasil_stem}_ringan.webm")
    shutil.copyfile(f5_light_mp4, hasil_mp4)
    shutil.copyfile(f5_light_webm, hasil_webm)
    print(f"   ✓ Disalin ke Hasil: {hasil_mp4} & {hasil_webm}")

    # C. Salin ke Proyek SO
    if cfg.get("so_dir") and cfg.get("so_dest_stem"):
        so_mp4 = os.path.join(cfg["so_dir"], f"{cfg['so_dest_stem']}.mp4")
        so_webm = os.path.join(cfg["so_dir"], f"{cfg['so_dest_stem']}.webm")
        shutil.copyfile(f5_light_mp4, so_mp4)
        shutil.copyfile(f5_light_webm, so_webm)
        print(f"   ✓ Disalin ke Proyek SO: {so_mp4} & {so_webm}")

    # 9. Simpan Metadata Web Studio (/Proyek Video)
    metadata = {
        "id": vid_id,
        "title": cfg["title"],
        "subtitle": cfg["subtitle"],
        "total_duration": total_dur,
        "media": {
            "original_video": f"/video-projects/{vid_id}/clip_original.mp4",
            "dubbed_video_f5": f"/video-projects/{vid_id}/video_dubbed_marcia_f5_ringan.mp4",
            "dubbed_video_edge": f"/video-projects/{vid_id}/video_dubbed_marcia_edge_ringan.mp4",
            "dubbed_audio_f5": f"/video-projects/{vid_id}/master_dubbing_f5.mp3",
            "dubbed_audio_edge": f"/video-projects/{vid_id}/master_dubbing_edge.mp3"
        },
        "stats": {
            "original_bytes": orig_size,
            "light_mp4_bytes": os.path.getsize(f5_light_mp4),
            "light_webm_bytes": os.path.getsize(f5_light_webm),
            "compression_ratio": f"{((1 - os.path.getsize(f5_light_mp4)/orig_size)*100):.1f}%" if orig_size > 0 else "0%"
        },
        "segments": segments
    }

    meta_file = os.path.join(project_dir, "video_project_data.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Metadata Web Studio tersimpan: {meta_file}")

    print(f"\n📊 HASIL KOMPRESI: {vid_id}")
    print(f"   Original:  {orig_size / (1024*1024):.2f} MB")
    print(f"   F5 MP4:    {metadata['stats']['light_mp4_bytes'] / (1024*1024):.2f} MB (Hemat {metadata['stats']['compression_ratio']})")
    print(f"   F5 WebM:   {metadata['stats']['light_webm_bytes'] / (1024*1024):.2f} MB")

async def main():
    print("="*80)
    print("🎙️ SPRINT VIDEO DUBBING: ZONA 5 LEVEL 3 - 6 (PEMBAGIAN LANJUT)")
    print("   Fix: Durasi Akhir Penuh, Bebas Terpotong, Canvas Putih 16:9 Bebas Hitam")
    print("="*80)

    # Lazy F5 Engine Loader
    engine_holder = {"engine": None}
    def get_engine():
        if engine_holder["engine"] is None:
            print("\n[Init] Memuat Model F5-TTS Indo V2...")
            from f5_engine import F5IndoEngine
            engine_holder["engine"] = F5IndoEngine()
            print("✓ Model F5-TTS siap digunakan pada:", engine_holder["engine"].device)
        return engine_holder["engine"]

    # Identitas Suara Marcia
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."
    print("✓ Audio Acuan Guru Marcia:", marcia_ref)

    start_all = time.time()
    for cfg in VIDEOS_CONFIG:
        await process_video(cfg, get_engine, marcia_ref, marcia_ref_text)

    if engine_holder["engine"] is not None:
        engine_holder["engine"].free_gpu_memory()

    total_time = time.time() - start_all
    print("\n" + "="*80)
    print(f"🎉 SELURUH 7 VIDEO ZONA 5 SELESAI DIDUBBING DALAM {total_time/60:.2f} MENIT!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
