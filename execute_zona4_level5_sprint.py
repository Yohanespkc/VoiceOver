#!/usr/bin/env python3
"""
execute_zona4_level5_sprint.py

Pipeline Dubbing & Voice Cloning Guru Marcia untuk 4 Video Zona 4 Level 5:
1. zona 4 level 5-1.mp4  (389 - 2, 343 - 21, 677 - 324 | Pengurangan 3D Tanpa Meminjam)
2. zona 4 level 5-2a.mp4 (331 - 9 = 322 | Pengurangan 3D - 1D Meminjam Tiga Cara)
3. zona 4 level 5-2b.mp4 (842 - 59 = 783 | Pengurangan 3D - 2D Meminjam Tiga Cara)
4. zona 4 level 5-2c.mp4 (842 - 187 = 655 | Pengurangan 3D - 3D Meminjam Tiga Cara)

Standar Mutu:
- Angka diekspansi 100% fonetik bahasa Indonesia utuh (cth: "tiga ratus delapan puluh sembilan", "tiga ratus dua puluh dua", dsb)
- Suara Karakter: Trainer Marcia Asli (at_marcia_ref.wav, F5-TTS Indo V2, nfe=32, speed=1.05)
- Alternatif Nol-Noise: Edge-TTS Studio (id-ID-GadisNeural)
- Broadcast DSP Mastering: highpass 80Hz + loudnorm -16 LUFS (meniadakan noise/rumble, vokal jernih)
- Kompresi Video Ringan: H.264 tune animation CRF 28, AAC 48k Mono, FastStart + WebM VP9/Opus
- Sinkronisasi Otomatis ke:
  1. Data VIdeo Marcia/ (*_ringan.mp4)
  2. Hasil/videoMarcia/z4_pengurangan/
  3. Proyek SO: /Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l5/
  4. Web Studio UI: video_projects/ (/Proyek Video)
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

from f5_engine import F5IndoEngine

DATA_VIDEO_DIR = os.path.join(BASE_DIR, "Data VIdeo Marcia")
VIDEO_PROJECTS_DIR = os.path.join(BASE_DIR, "video_projects")
HASIL_Z4_DIR = os.path.join(BASE_DIR, "Hasil", "videoMarcia", "z4_pengurangan")
SO_Z4L5_DIR = "/Users/yohanessurya/Documents/Development/so/web/public/assets/videos/z4l5"

os.makedirs(HASIL_Z4_DIR, exist_ok=True)
os.makedirs(SO_Z4L5_DIR, exist_ok=True)

VIDEOS_CONFIG = [
    {
        "id": "z4l5_1_pengurangan_3d_tanpa_meminjam",
        "source_filename": "zona 4 level 5-1.mp4",
        "so_dest_stem": "z4l5sb1bermain1_marcia",
        "so_game_name": "Perburuan Kadal Savana (z4l5-sb1bermain1)",
        "title": "Zona 4 Level 5.1: Pengurangan 3 Digit Tanpa Meminjam",
        "subtitle": "Pengurangan bilangan 3 digit tanpa meminjam untuk 3D - 1D, 3D - 2D, dan 3D - 3D secara langsung.",
        "duration": 71.37,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 4.00,
                "text": "Tiga ratus delapan puluh sembilan dikurang dua.",
                "display_text": "389 dikurang 2.",
                "visual": "Menuliskan soal 389 - 2"
            },
            {
                "id": 2,
                "start": 4.08,
                "end": 7.40,
                "text": "Di sini satuannya bisa dikurangi.",
                "display_text": "Di sini satuannya bisa dikurangi.",
                "visual": "Mengecek digit satuan 9 - 2"
            },
            {
                "id": 3,
                "start": 7.44,
                "end": 11.20,
                "text": "Sehingga kita tuliskan ratusannya tiga.",
                "display_text": "Sehingga kita tuliskan ratusannya 3.",
                "visual": "Menulis angka 3 pada nilai tempat ratusan"
            },
            {
                "id": 4,
                "start": 11.30,
                "end": 13.00,
                "text": "Puluhannya delapan.",
                "display_text": "Puluhannya 8.",
                "visual": "Menulis angka 8 pada nilai tempat puluhan"
            },
            {
                "id": 5,
                "start": 13.00,
                "end": 16.04,
                "text": "Dan satuannya sembilan dikurang dua, yaitu tujuh.",
                "display_text": "Dan satuannya 9 dikurang 2, yaitu 7.",
                "visual": "Menghitung satuan 9 - 2 = 7"
            },
            {
                "id": 6,
                "start": 16.04,
                "end": 21.60,
                "text": "Jadi tiga ratus delapan puluh sembilan dikurang dua adalah tiga ratus delapan puluh tujuh.",
                "display_text": "Jadi 389 dikurang 2 adalah 387.",
                "visual": "Menuliskan hasil akhir 387"
            },
            {
                "id": 7,
                "start": 21.80,
                "end": 24.80,
                "text": "Nah berikutnya tiga ratus empat puluh tiga dikurang dua puluh satu.",
                "display_text": "Nah berikutnya 343 dikurang 21.",
                "visual": "Menuliskan soal 343 - 21"
            },
            {
                "id": 8,
                "start": 25.00,
                "end": 28.94,
                "text": "Di sini puluhannya bisa dikurangi, satuannya bisa dikurangi.",
                "display_text": "Di sini puluhannya bisa dikurangi, satuannya bisa dikurangi.",
                "visual": "Mengecek puluhan dan satuan bisa langsung dikurangi"
            },
            {
                "id": 9,
                "start": 29.00,
                "end": 32.00,
                "text": "Sehingga kita tuliskan ratusannya tiga.",
                "display_text": "Sehingga kita tuliskan ratusannya 3.",
                "visual": "Menulis ratusan 3"
            },
            {
                "id": 10,
                "start": 32.20,
                "end": 35.30,
                "text": "Puluhannya adalah empat kurang dua, yaitu dua.",
                "display_text": "Puluhannya adalah 4 kurang 2, yaitu 2.",
                "visual": "Menghitung puluhan 4 - 2 = 2"
            },
            {
                "id": 11,
                "start": 35.50,
                "end": 37.80,
                "text": "Satuannya tiga kurang satu, dua.",
                "display_text": "Satuannya 3 kurang 1, 2.",
                "visual": "Menghitung satuan 3 - 1 = 2"
            },
            {
                "id": 12,
                "start": 38.00,
                "end": 42.04,
                "text": "Jadi tiga ratus empat puluh tiga dikurang dua puluh satu adalah tiga ratus dua puluh dua.",
                "display_text": "Jadi 343 dikurang 21 adalah 322.",
                "visual": "Menuliskan hasil akhir 322"
            },
            {
                "id": 13,
                "start": 42.04,
                "end": 46.50,
                "text": "Nah berikutnya enam ratus tujuh puluh tujuh dikurang tiga ratus dua puluh empat.",
                "display_text": "Nah berikutnya 677 dikurang 324.",
                "visual": "Menuliskan soal 677 - 324"
            },
            {
                "id": 14,
                "start": 46.80,
                "end": 52.40,
                "text": "Di sini satuannya bisa dikurangi, puluhannya bisa dikurangi, ratusannya bisa dikurangi.",
                "display_text": "Di sini satuannya bisa dikurangi, puluhannya bisa dikurangi, ratusannya bisa dikurangi.",
                "visual": "Mengecek semua nilai tempat bisa langsung dikurangi"
            },
            {
                "id": 15,
                "start": 52.60,
                "end": 58.00,
                "text": "Jadi kita tuliskan ratusannya adalah enam kurang tiga, yaitu tiga.",
                "display_text": "Jadi kita tuliskan ratusannya adalah 6 kurang 3, yaitu 3.",
                "visual": "Menghitung ratusan 6 - 3 = 3"
            },
            {
                "id": 16,
                "start": 58.10,
                "end": 61.80,
                "text": "Kemudian puluhannya tujuh kurang dua adalah lima.",
                "display_text": "Kemudian puluhannya 7 kurang 2 adalah 5.",
                "visual": "Menghitung puluhan 7 - 2 = 5"
            },
            {
                "id": 17,
                "start": 62.00,
                "end": 65.50,
                "text": "Lalu satuannya tujuh kurang empat adalah tiga.",
                "display_text": "Lalu satuannya 7 kurang 4 adalah 3.",
                "visual": "Menghitung satuan 7 - 4 = 3"
            },
            {
                "id": 18,
                "start": 65.70,
                "end": 70.50,
                "text": "Jadi enam ratus tujuh puluh tujuh dikurang tiga ratus dua puluh empat adalah tiga ratus lima puluh tiga.",
                "display_text": "Jadi 677 dikurang 324 adalah 353.",
                "visual": "Menuliskan hasil akhir 353"
            }
        ]
    },
    {
        "id": "z4l5_2a_pengurangan_3d_1d_meminjam",
        "source_filename": "zona 4 level 5-2a.mp4",
        "so_dest_stem": "z4l5sb1bermain2_marcia",
        "so_game_name": "Tantangan Savana Liar (z4l5-sb1bermain2)",
        "title": "Zona 4 Level 5.2a: Pengurangan 3D - 1D Meminjam (331 - 9 = 322)",
        "subtitle": "Pengurangan 3 digit dengan 1 digit meminjam menggunakan cara pecah puluhan, cara belasan, dan mencongak.",
        "duration": 91.77,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 5.20,
                "text": "Sekarang kita hitung tiga ratus tiga puluh satu dikurang sembilan, kita cek dulu satuannya.",
                "display_text": "Sekarang kita hitung 331 dikurang 9, kita cek dulu satuannya.",
                "visual": "Menuliskan soal 331 - 9"
            },
            {
                "id": 2,
                "start": 5.50,
                "end": 12.80,
                "text": "Di sini satu dikurang sembilan tidak bisa, maka puluhannya kita pecah menjadi dua puluhan dan sepuluh satuan.",
                "display_text": "Di sini 1 dikurang 9 tidak bisa, maka puluhannya kita pecah menjadi 2 puluhan dan 10 satuan.",
                "visual": "Cara 1: Memecah puluhan 30 menjadi 2 puluhan dan 10 satuan"
            },
            {
                "id": 3,
                "start": 13.32,
                "end": 18.20,
                "text": "Nah selanjutnya kita hitung dari depan, ratusannya tiga dikurang nol adalah tiga.",
                "display_text": "Nah selanjutnya kita hitung dari depan, ratusannya 3 dikurang 0 adalah 3.",
                "visual": "Menghitung ratusan 3 - 0 = 3"
            },
            {
                "id": 4,
                "start": 18.20,
                "end": 23.50,
                "text": "Kemudian puluhannya dua dikurang nol adalah dua.",
                "display_text": "Kemudian puluhannya 2 dikurang 0 adalah 2.",
                "visual": "Menghitung puluhan 2 - 0 = 2"
            },
            {
                "id": 5,
                "start": 23.78,
                "end": 29.00,
                "text": "Lalu satuannya sepuluh dikurang sembilan adalah satu, tapi masih ada satu di sini.",
                "display_text": "Lalu satuannya 10 dikurang 9 adalah 1, tapi masih ada 1 di sini.",
                "visual": "Menghitung 10 - 9 = 1 dan mengingat sisa 1"
            },
            {
                "id": 6,
                "start": 29.00,
                "end": 33.60,
                "text": "Jadi satu tambah satu adalah dua, sehingga hasilnya tiga ratus dua puluh dua.",
                "display_text": "Jadi 1 tambah 1 adalah 2, sehingga hasilnya 322.",
                "visual": "Menghitung 1 + 1 = 2 dan menulis hasil akhir 322"
            },
            {
                "id": 7,
                "start": 34.18,
                "end": 44.30,
                "text": "Bisa juga kita gunakan cara belasan. Di sini satu dikurang sembilan tidak bisa, maka tiga puluhannya kita pecah menjadi dua puluhan dan sepuluh satuan.",
                "display_text": "Bisa juga kita gunakan cara belasan. Di sini 1 dikurang 9 tidak bisa, maka 30-annya kita pecah menjadi 20-an dan 10-an.",
                "visual": "Cara 2: Menggunakan cara belasan"
            },
            {
                "id": 8,
                "start": 44.54,
                "end": 52.96,
                "text": "Lalu di sini kita lihat ratusannya tiga, puluhannya dua, kemudian satuannya di sini kita lihat ada sebelas.",
                "display_text": "Lalu di sini kita lihat ratusannya 3, puluhannya 2, kemudian satuannya di sini kita lihat ada 11.",
                "visual": "Membentuk 11 satuan dari 10 + 1"
            },
            {
                "id": 9,
                "start": 52.96,
                "end": 59.80,
                "text": "Sebelas dikurang sembilan hasilnya adalah dua, jadi hasilnya tiga ratus dua puluh dua.",
                "display_text": "11 dikurang 9 hasilnya adalah 2, jadi hasilnya 322.",
                "visual": "Menghitung 11 - 9 = 2"
            },
            {
                "id": 10,
                "start": 60.28,
                "end": 66.50,
                "text": "Cara mencongak adalah sebagai berikut, tiga dikurang nol adalah tiga.",
                "display_text": "Cara mencongak adalah sebagai berikut, 3 dikurang 0 adalah 3.",
                "visual": "Cara 3: Mencongak, menghitung 3 - 0 = 3"
            },
            {
                "id": 11,
                "start": 66.50,
                "end": 71.50,
                "text": "Kemudian tiga dikurang nol, tiga juga, tapi lirik kanan satuannya tidak bisa dikurangi.",
                "display_text": "Kemudian 3 dikurang 0, 3 juga, tapi lirik kanan satuannya tidak bisa dikurangi.",
                "visual": "Lirik kanan pada puluhan melihat satuan tidak bisa dikurang"
            },
            {
                "id": 12,
                "start": 71.72,
                "end": 76.84,
                "text": "Maka puluhannya kita kurangi satu, yaitu tiga dikurangi satu menjadi dua.",
                "display_text": "Maka puluhannya kita kurangi 1, yaitu 3 dikurangi 1 menjadi 2.",
                "visual": "Mengurangi puluhan 3 - 1 = 2"
            },
            {
                "id": 13,
                "start": 76.84,
                "end": 82.00,
                "text": "Lalu satu satuan ini ditambah pasangan sembilan. Pasangan sembilan adalah satu.",
                "display_text": "Lalu 1 satuan ini ditambah pasangan 9. Pasangan 9 adalah 1.",
                "visual": "Menjumlahkan 1 dengan pasangan 9"
            },
            {
                "id": 14,
                "start": 82.00,
                "end": 86.62,
                "text": "Satu tambah satu adalah dua, jadi hasilnya tiga ratus dua puluh dua.",
                "display_text": "1 tambah 1 adalah 2, jadi hasilnya 322.",
                "visual": "Menghitung 1 + 1 = 2 dan menegaskan hasil 322"
            },
            {
                "id": 15,
                "start": 87.12,
                "end": 91.00,
                "text": "Nah, kenapa satu tambah pasangan sembilan? Asalnya dari sini.",
                "display_text": "Nah, kenapa 1 tambah pasangan 9? Asalnya dari sini.",
                "visual": "Menjelaskan asal konsep pasangan 9"
            }
        ]
    },
    {
        "id": "z4l5_2b_pengurangan_3d_2d_meminjam",
        "source_filename": "zona 4 level 5-2b.mp4",
        "so_dest_stem": "z4l5sb2bermain1_marcia",
        "so_game_name": "Benteng Savana Qutub (z4l5-sb2bermain1)",
        "title": "Zona 4 Level 5.2b: Pengurangan 3D - 2D Meminjam (842 - 59 = 783)",
        "subtitle": "Pengurangan 3 digit dengan 2 digit meminjam ganda (puluhan dan ratusan) dengan tiga cara.",
        "duration": 127.10,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 3.50,
                "text": "Sekarang kita hitung delapan ratus empat puluh dua dikurang lima puluh sembilan.",
                "display_text": "Sekarang kita hitung 842 dikurang 59.",
                "visual": "Menuliskan soal 842 - 59"
            },
            {
                "id": 2,
                "start": 3.88,
                "end": 12.32,
                "text": "Lihat dulu satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi tiga puluhan dan sepuluh satuan.",
                "display_text": "Lihat dulu satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi 30-an dan 10 satuan.",
                "visual": "Memecah 40 menjadi 30 dan 10"
            },
            {
                "id": 3,
                "start": 12.46,
                "end": 15.60,
                "text": "Kemudian tiga dikurang lima tidak bisa.",
                "display_text": "Kemudian 3 dikurang 5 tidak bisa.",
                "visual": "Mengecek 30 tidak bisa dikurangi 50"
            },
            {
                "id": 4,
                "start": 15.82,
                "end": 22.80,
                "text": "Maka delapan ratusan itu diubah atau dipecah menjadi tujuh ratusan dan sepuluh puluhan.",
                "display_text": "Maka 800-an itu diubah atau dipecah menjadi 700-an dan 10 puluhan.",
                "visual": "Memecah 800 menjadi 700 dan 10 puluhan (100)"
            },
            {
                "id": 5,
                "start": 23.00,
                "end": 26.10,
                "text": "Nah sekarang baru kita kerjakan dari depan.",
                "display_text": "Nah sekarang baru kita kerjakan dari depan.",
                "visual": "Mulai menghitung dari depan"
            },
            {
                "id": 6,
                "start": 26.14,
                "end": 28.00,
                "text": "Ratusannya tujuh.",
                "display_text": "Ratusannya 7.",
                "visual": "Menuliskan ratusan 7"
            },
            {
                "id": 7,
                "start": 28.34,
                "end": 36.80,
                "text": "Kemudian puluhannya di sini sepuluh kurang lima adalah lima, masih ada tiga jadi delapan.",
                "display_text": "Kemudian puluhannya di sini 10 kurang 5 adalah 5, masih ada 3 jadi 8.",
                "visual": "Menghitung puluhan: 10 - 5 = 5, 5 + 3 = 8"
            },
            {
                "id": 8,
                "start": 37.26,
                "end": 46.60,
                "text": "Lalu satuannya sepuluh dikurang sembilan satu, masih ada dua jadi tiga, hasilnya tujuh ratus delapan puluh tiga.",
                "display_text": "Lalu satuannya 10 dikurang 9, 1 masih ada 2 jadi 3, hasilnya 783.",
                "visual": "Menghitung satuan: 10 - 9 = 1, 1 + 2 = 3. Hasil: 783"
            },
            {
                "id": 9,
                "start": 46.78,
                "end": 48.80,
                "text": "Nah cara berikutnya cara belasan.",
                "display_text": "Nah cara berikutnya cara belasan.",
                "visual": "Beralih ke Cara 2: Belasan"
            },
            {
                "id": 10,
                "start": 49.00,
                "end": 56.90,
                "text": "Di sini satuannya dua dikurang sembilan tidak bisa, maka empat ini kita pecah menjadi tiga puluhan dan sepuluh satuan.",
                "display_text": "Di sini satuannya 2 dikurang 9 tidak bisa, maka 4 ini kita pecah menjadi 30-an dan 10-an.",
                "visual": "Memecah 40 menjadi 30 dan 10"
            },
            {
                "id": 11,
                "start": 56.90,
                "end": 65.50,
                "text": "Lalu tiga dikurang lima tidak bisa, maka delapan ini kita pecah menjadi tujuh ratusan dan satu ratusan.",
                "display_text": "Lalu 3 dikurang 5 tidak bisa, maka 8 ini kita pecah menjadi 700-an dan 100-an.",
                "visual": "Memecah 800 menjadi 700 dan 100"
            },
            {
                "id": 12,
                "start": 65.68,
                "end": 69.00,
                "text": "Nah selanjutnya kita hitung dari depan.",
                "display_text": "Nah selanjutnya kita hitung dari depan.",
                "visual": "Mulai menghitung nilai tempat"
            },
            {
                "id": 13,
                "start": 69.00,
                "end": 71.00,
                "text": "Ratusannya ada tujuh.",
                "display_text": "Ratusannya ada 7.",
                "visual": "Menulis ratusan 7"
            },
            {
                "id": 14,
                "start": 71.20,
                "end": 76.80,
                "text": "Kemudian puluhannya di sini ada tiga belas kurang lima hasilnya delapan.",
                "display_text": "Kemudian puluhannya di sini ada 13 kurang 5 hasilnya 8.",
                "visual": "Menghitung puluhan: 13 - 5 = 8"
            },
            {
                "id": 15,
                "start": 77.20,
                "end": 86.12,
                "text": "Kemudian di sini dua belas satuan dikurang sembilan hasilnya adalah tiga, sehingga hasilnya tujuh ratus delapan puluh tiga.",
                "display_text": "Kemudian di sini 12 satuan dikurang 9 hasilnya adalah 3, sehingga hasilnya 783.",
                "visual": "Menghitung satuan: 12 - 9 = 3. Hasil: 783"
            },
            {
                "id": 16,
                "start": 86.12,
                "end": 88.00,
                "text": "Nah sekarang cara mencongak.",
                "display_text": "Nah sekarang cara mencongak.",
                "visual": "Beralih ke Cara 3: Mencongak"
            },
            {
                "id": 17,
                "start": 88.10,
                "end": 96.50,
                "text": "Delapan dikurang nol adalah delapan, lirik kanan puluhannya tidak bisa dikurangi, maka ratusannya kita kurangi satu jadi tujuh.",
                "display_text": "8 dikurang 0 adalah 8, lirik kanan puluhannya tidak bisa dikurangi, maka ratusannya kita kurangi 1 jadi 7.",
                "visual": "8 - 0 = 8, lirik kanan kurangi 1 jadi 7"
            },
            {
                "id": 18,
                "start": 97.00,
                "end": 100.24,
                "text": "Nah kemudian empat ditambah pasangan lima.",
                "display_text": "Nah kemudian 4 ditambah pasangan 5.",
                "visual": "Menghitung puluhan: 4 + pasangan 5"
            },
            {
                "id": 19,
                "start": 100.34,
                "end": 107.04,
                "text": "Pasangan lima adalah lima, empat tambah lima jadi sembilan. Lirik kanan dan ini tidak bisa dikurangi satuannya.",
                "display_text": "Pasangan 5 adalah 5, 4 tambah 5 jadi 9. Lirik kanan dan ini tidak bisa dikurangi satuannya.",
                "visual": "4 + 5 = 9, lirik kanan satuan tidak bisa dikurang"
            },
            {
                "id": 20,
                "start": 107.16,
                "end": 112.02,
                "text": "Akibatnya puluhannya kita kurangi satu, tadi sembilan kurang satu jadi delapan.",
                "display_text": "Akibatnya puluhannya kita kurangi 1, tadi 9 kurang 1 jadi 8.",
                "visual": "Mengurangi puluhan 9 - 1 = 8"
            },
            {
                "id": 21,
                "start": 112.02,
                "end": 116.20,
                "text": "Kemudian dua kita tambahkan dengan pasangan sembilan.",
                "display_text": "Kemudian 2 kita tambahkan dengan pasangan 9.",
                "visual": "Menghitung satuan: 2 + pasangan 9"
            },
            {
                "id": 22,
                "start": 116.26,
                "end": 120.50,
                "text": "Pasangan sembilan adalah satu, dua tambah satu adalah tiga.",
                "display_text": "Pasangan 9 adalah 1, 2 tambah 1 adalah 3.",
                "visual": "2 + 1 = 3"
            },
            {
                "id": 23,
                "start": 121.00,
                "end": 126.50,
                "text": "Nah kalau kita lihat, ini adalah penyederhanaan dari sini.",
                "display_text": "Nah kalau kita lihat ini adalah penyederhanaan dari sini.",
                "visual": "Menghubungkan cara mencongak dengan cara dasar"
            }
        ]
    },
    {
        "id": "z4l5_2c_pengurangan_3d_3d_meminjam",
        "source_filename": "zona 4 level 5-2c.mp4",
        "so_dest_stem": "z4l5sb2bermain2_marcia",
        "so_game_name": "Tantangan Benteng Taj Mahal (z4l5-sb2bermain2)",
        "title": "Zona 4 Level 5.2c: Pengurangan 3D - 3D Meminjam (842 - 187 = 655)",
        "subtitle": "Pengurangan 3 digit dengan 3 digit meminjam ganda menggunakan cara pecah, cara belasan, dan mencongak.",
        "duration": 130.37,
        "segments": [
            {
                "id": 1,
                "start": 0.00,
                "end": 4.10,
                "text": "Sekarang kita hitung delapan ratus empat puluh dua dikurang satu ratus delapan puluh tujuh.",
                "display_text": "Sekarang kita hitung 842 dikurang 187.",
                "visual": "Menuliskan soal 842 - 187"
            },
            {
                "id": 2,
                "start": 4.30,
                "end": 12.20,
                "text": "Kita lihat dulu satuannya, tidak bisa dikurangi maka puluhannya kita pecah menjadi tiga puluhan dan sepuluh satuan.",
                "display_text": "Kita lihat dulu satuannya, tidak bisa dikurangi maka puluhannya kita pecah menjadi 30-an dan 10 satuan.",
                "visual": "Memecah 40 menjadi 30 dan 10"
            },
            {
                "id": 3,
                "start": 12.60,
                "end": 20.20,
                "text": "Tiga dikurang delapan tidak bisa, maka delapannya kita pecah menjadi tujuh ratusan dan sepuluh puluhan.",
                "display_text": "3 dikurang 8 tidak bisa, maka 8-nya kita pecah menjadi 700-an dan 10 puluhan.",
                "visual": "Memecah 800 menjadi 700 dan 10 puluhan"
            },
            {
                "id": 4,
                "start": 20.68,
                "end": 28.06,
                "text": "Selanjutnya kita kurangi dari depan, ratusannya tujuh dikurangi satu hasilnya enam.",
                "display_text": "Selanjutnya kita kurangi dari depan, ratusannya 7 dikurangi 1 hasilnya 6.",
                "visual": "Menghitung ratusan 7 - 1 = 6"
            },
            {
                "id": 5,
                "start": 28.06,
                "end": 35.50,
                "text": "Kemudian puluhannya sepuluh dikurang delapan dua, masih ada tiga jadi lima.",
                "display_text": "Kemudian puluhannya 10 dikurang 8, 2 masih ada 3 jadi 5.",
                "visual": "Menghitung puluhan: 10 - 8 = 2, 2 + 3 = 5"
            },
            {
                "id": 6,
                "start": 36.20,
                "end": 41.84,
                "text": "Kemudian satuannya sepuluh kurang tujuh tiga, masih ada dua jadi lima.",
                "display_text": "Kemudian satuannya 10 kurang 7, 3 masih ada 2, 5.",
                "visual": "Menghitung satuan: 10 - 7 = 3, 3 + 2 = 5"
            },
            {
                "id": 7,
                "start": 42.18,
                "end": 44.50,
                "text": "Jadi hasilnya enam ratus lima puluh lima.",
                "display_text": "Jadi hasilnya 655.",
                "visual": "Menuliskan hasil akhir 655"
            },
            {
                "id": 8,
                "start": 44.70,
                "end": 55.42,
                "text": "Nah kemudian pakai cara belasan di sini. Kita cek dulu satuannya tidak bisa dikurangi, maka puluhannya kita pecah menjadi tiga puluhan dan satu puluhan.",
                "display_text": "Nah kemudian pakai cara belasan di sini, kita cek dulu satuannya tidak bisa dikurangi maka puluhannya kita pecah menjadi 30-an dan 10-an.",
                "visual": "Cara 2: Belasan, memecah 40 menjadi 30 dan 10"
            },
            {
                "id": 9,
                "start": 55.42,
                "end": 65.50,
                "text": "Kemudian tiga puluhan ini tidak bisa dikurangi dengan delapan puluhan, kita pecah ratusannya menjadi tujuh ratusan dan satu ratusan.",
                "display_text": "Kemudian 30-an ini tidak bisa dikurangi dengan 80-an, kita pecah ratusannya menjadi 700-an dan 100-an.",
                "visual": "Memecah 800 menjadi 700 dan 100"
            },
            {
                "id": 10,
                "start": 66.08,
                "end": 71.76,
                "text": "Kemudian kita kurangi tujuh dikurang satu, ratusannya ada enam.",
                "display_text": "Kemudian kita kurangi 7 dikurang 1, ratusannya ada 6.",
                "visual": "Menghitung ratusan 7 - 1 = 6"
            },
            {
                "id": 11,
                "start": 72.04,
                "end": 78.26,
                "text": "Kemudian tiga belas puluhan dikurangi delapan puluhan hasilnya lima puluhan.",
                "display_text": "Kemudian 13-an dikurangi 80-an, hasilnya 50-an.",
                "visual": "Menghitung puluhan: 13 - 8 = 5"
            },
            {
                "id": 12,
                "start": 78.26,
                "end": 88.42,
                "text": "Kemudian dua belas satuan dikurangi tujuh satuan adalah lima satuan, jadi hasilnya juga enam ratus lima puluh lima.",
                "display_text": "Kemudian 12-an dikurangi 7-an adalah 5-an, jadi hasilnya juga 655.",
                "visual": "Menghitung satuan: 12 - 7 = 5. Hasil: 655"
            },
            {
                "id": 13,
                "start": 88.58,
                "end": 93.50,
                "text": "Nah cara mencongak, kita lihat delapan dikurangi satu adalah tujuh.",
                "display_text": "Nah cara mencongak, kita lihat 8 dikurangi 1 adalah 7.",
                "visual": "Cara 3: Mencongak, 8 - 1 = 7"
            },
            {
                "id": 14,
                "start": 93.80,
                "end": 100.84,
                "text": "Lirik kanan di sini tidak bisa dikurangi, maka tujuhnya itu kita kurangi satu jadi enam.",
                "display_text": "Lirik kanan di sini tidak bisa dikurangi, maka 7-nya itu kita kurangi 1 jadi 6.",
                "visual": "Lirik kanan, kurangi 1 menjadi 6"
            },
            {
                "id": 15,
                "start": 101.66,
                "end": 106.60,
                "text": "Selanjutnya empat ditambah pasangan delapan. Pasangan delapan adalah dua.",
                "display_text": "Selanjutnya 4 ditambah pasangan 8, pasangan 8 adalah 2.",
                "visual": "Menghitung puluhan: 4 + pasangan 8"
            },
            {
                "id": 16,
                "start": 106.60,
                "end": 109.10,
                "text": "Empat tambah dua adalah enam.",
                "display_text": "4 tambah 2 adalah 6.",
                "visual": "4 + 2 = 6"
            },
            {
                "id": 17,
                "start": 109.30,
                "end": 115.00,
                "text": "Lirik kanan tidak bisa dikurangi satuannya, jadi enam dikurangi satu yaitu lima.",
                "display_text": "Lirik kanan tidak bisa dikurangi satuannya, jadi 6 dikurangi 1, yaitu 5.",
                "visual": "Lirik kanan, 6 - 1 = 5 pada puluhan"
            },
            {
                "id": 18,
                "start": 115.60,
                "end": 124.50,
                "text": "Nah kemudian dua kita tambah pasangan tujuh. Pasangan tujuh adalah tiga, jadi dua tambah tiga yaitu lima.",
                "display_text": "Nah kemudian 2 kita tambah pasangan 7, pasangan 7 adalah 3, jadi 2 tambah 3 yaitu 5.",
                "visual": "Menghitung satuan: 2 + pasangan 7 (3) = 5"
            },
            {
                "id": 19,
                "start": 124.80,
                "end": 127.00,
                "text": "Jadi hasilnya enam ratus lima puluh lima.",
                "display_text": "Jadi hasilnya 655.",
                "visual": "Menuliskan hasil akhir 655"
            },
            {
                "id": 20,
                "start": 127.20,
                "end": 129.80,
                "text": "Ini diperoleh dari cara di atas.",
                "display_text": "Ini diperoleh dari sini.",
                "visual": "Menegaskan keterkaitan konsep"
            }
        ]
    }
]

def format_bytes(num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} TB"

def get_audio_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_atempo_filter(tempo: float) -> str:
    parts = []
    curr = tempo
    while curr > 2.0:
        parts.append("atempo=2.0")
        curr /= 2.0
    while curr < 0.5:
        parts.append("atempo=0.5")
        curr /= 0.5
    parts.append(f"atempo={curr:.4f}")
    return ",".join(parts)

async def synthesize_edge_segment(text: str, out_path: str, voice: str = "id-ID-GadisNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="+5%", pitch="+0Hz")
    await communicate.save(out_path)

def run_ffmpeg(cmd, desc="FFmpeg"):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg Gagal [{desc}]: {res.stderr[-400:]}")
        raise RuntimeError(f"FFmpeg error: {res.stderr[-400:]}")
    return res

async def process_single_video(cfg: dict, engine: F5IndoEngine, marcia_ref: str, marcia_ref_text: str):
    vid_id = cfg["id"]
    src_file = os.path.join(DATA_VIDEO_DIR, cfg["source_filename"])
    total_dur = cfg["duration"]
    segments = cfg["segments"]
    so_dest_stem = cfg["so_dest_stem"]
    
    print("\n" + "=" * 70)
    print(f"🎬 MEMPROSES ZONA 4 LEVEL 5: {cfg['title']}")
    print(f"   Target SO Game: {cfg['so_game_name']} -> {so_dest_stem}")
    print(f"   Sumber Video  : {src_file} ({format_bytes(os.path.getsize(src_file))})")
    print(f"   Durasi Total  : {total_dur:.2f} detik | {len(segments)} Segmen Dialog")
    print("=" * 70)

    # 1. Project Directory
    project_dir = os.path.join(VIDEO_PROJECTS_DIR, vid_id)
    segments_dir = os.path.join(project_dir, "segments")
    os.makedirs(segments_dir, exist_ok=True)

    clip_orig = os.path.join(project_dir, "clip_original.mp4")
    shutil.copyfile(src_file, clip_orig)

    # 2. Extract original audio 24k
    orig_wav = os.path.join(project_dir, "original_audio_24k.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-i", clip_orig,
        "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
        orig_wav
    ], "Extract 24k audio")

    # 3. F5-TTS Synthesis for each segment (using explicit spelled out text)
    import librosa
    import soundfile as sf
    MASTER_FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=10"

    print(f"\n▶ Fase 1: Sintesis F5-TTS Trainer Marcia ({len(segments)} segmen ucapan fonetik lengkap)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]  # Ejaan kata bahasa Indonesia utuh
        target_dur = s["end"] - s["start"]
        print(f"  [{sid}/{len(segments)}] F5-TTS: \"{text}\"...", end="", flush=True)
        t0 = time.time()

        res_f5 = engine.generate(
            ref_audio_path=marcia_ref,
            ref_text=marcia_ref_text,
            gen_text=text,
            speed=1.05,
            nfe_step=32,
            output_format="wav"
        )
        raw_f5 = os.path.join(BASE_DIR, res_f5["audio_url"].lstrip("/"))

        # Silence trimming
        y, sr = librosa.load(raw_f5, sr=24000)
        y_trim, _ = librosa.effects.trim(y, top_db=25)
        trim_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_trimmed.wav")
        sf.write(trim_f5, y_trim, sr)
        trim_dur = len(y_trim) / sr

        # Time alignment & broadcast mastering
        tempo = trim_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        aligned_f5 = os.path.join(segments_dir, f"f5_seg_{sid}_aligned.wav")
        run_ffmpeg([
            "ffmpeg", "-y", "-i", trim_f5,
            "-af", f"{atempo},{MASTER_FILTER}",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_f5
        ], f"Align F5 seg {sid}")

        s["audio_f5"] = f"/video-projects/{vid_id}/segments/f5_seg_{sid}_aligned.wav"
        print(f" Selesai ({time.time()-t0:.2f}s | aktif: {trim_dur:.2f}s -> target: {target_dur:.2f}s)")

    # 4. Edge-TTS Synthesis
    print(f"\n▶ Fase 2: Sintesis Edge-TTS Studio ({len(segments)} segmen)...")
    for s in segments:
        sid = s["id"]
        text = s["text"]
        target_dur = s["end"] - s["start"]
        raw_edge = os.path.join(segments_dir, f"edge_seg_{sid}_raw.mp3")
        aligned_edge = os.path.join(segments_dir, f"edge_seg_{sid}_aligned.wav")

        await synthesize_edge_segment(text, raw_edge)
        edge_dur = get_audio_duration(raw_edge)

        tempo = edge_dur / target_dur if target_dur > 0 else 1.0
        tempo = max(0.80, min(1.35, tempo))
        atempo = build_atempo_filter(tempo)

        run_ffmpeg([
            "ffmpeg", "-y", "-i", raw_edge,
            "-af", f"{atempo},loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            "-t", str(target_dur),
            aligned_edge
        ], f"Align Edge seg {sid}")

        s["audio_edge"] = f"/video-projects/{vid_id}/segments/edge_seg_{sid}_aligned.wav"

    # Purge VRAM
    engine.free_gpu_memory()

    # 5. Assemble Master Timelines
    print(f"\n▶ Fase 3: Merakit Master Timeline ({total_dur:.2f}s)...")
    silence_wav = os.path.join(segments_dir, "silence.wav")
    run_ffmpeg([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(total_dur),
        silence_wav
    ], "Generate silence")

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

        # Build mix WAV
        run_ffmpeg([
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[outa]",
            "-t", str(total_dur),
            "-c:a", "pcm_s16le",
            master_wav
        ], f"Mix master {mode}")

        # Master MP3 320k
        run_ffmpeg([
            "ffmpeg", "-y", "-i", master_wav,
            "-c:a", "libmp3lame", "-b:a", "320k",
            master_mp3
        ], f"Master MP3 {mode}")

        # Mux to original video (discarding original male audio)
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", clip_orig,
            "-i", master_wav,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            video_dubbed
        ], f"Mux video {mode}")

        output_files[mode] = {
            "master_wav": master_wav,
            "master_mp3": master_mp3,
            "video_dubbed": video_dubbed
        }

    # 6. Ultra-Lightweight Optimization (H.264 tune animation & WebM VP9)
    print(f"\n▶ Fase 4: Optimasi Ukuran File Ringan (H.264 Tune Animation & WebM VP9)...")
    f5_light_mp4 = os.path.join(project_dir, "video_dubbed_marcia_f5_ringan.mp4")
    f5_light_webm = os.path.join(project_dir, "video_dubbed_marcia_f5_ringan.webm")

    # MP4 H.264 Tune Animation CRF 28 + AAC 48k Mono 64k
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", output_files["f5"]["video_dubbed"],
        "-c:v", "libx264",
        "-preset", "veryslow",
        "-crf", "28",
        "-tune", "animation",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "64k",
        "-ar", "48000",
        "-ac", "1",
        "-movflags", "+faststart",
        f5_light_mp4
    ], "Encode Lightweight MP4")

    # WebM VP9 CRF 36 + Opus 48k Mono 48k
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", output_files["f5"]["video_dubbed"],
        "-c:v", "libvpx-vp9",
        "-b:v", "0",
        "-crf", "36",
        "-deadline", "good",
        "-cpu-used", "2",
        "-pix_fmt", "yuv420p",
        "-c:a", "libopus",
        "-b:a", "48k",
        "-ar", "48000",
        "-ac", "1",
        f5_light_webm
    ], "Encode Lightweight WebM")

    orig_size = os.path.getsize(src_file)
    f5_light_size = os.path.getsize(f5_light_mp4)
    webm_light_size = os.path.getsize(f5_light_webm)
    f5_light_pct = (1 - (f5_light_size / orig_size)) * 100

    print(f"  ✓ Ukuran Asli     : {format_bytes(orig_size)}")
    print(f"  ✓ MP4 Ringan (F5) : {format_bytes(f5_light_size)} (Hemat {f5_light_pct:.1f}%)")
    print(f"  ✓ WebM Ringan (F5): {format_bytes(webm_light_size)}")

    # 7A. Copy to Data VIdeo Marcia
    stem_name = Path(cfg["source_filename"]).stem
    data_light_target = os.path.join(DATA_VIDEO_DIR, f"{stem_name}_ringan.mp4")
    shutil.copyfile(f5_light_mp4, data_light_target)

    # 7B. Copy to Hasil/videoMarcia/z4_pengurangan
    hasil_light_mp4 = os.path.join(HASIL_Z4_DIR, f"{vid_id}_marcia_ringan.mp4")
    hasil_light_webm = os.path.join(HASIL_Z4_DIR, f"{vid_id}_marcia_ringan.webm")
    shutil.copyfile(f5_light_mp4, hasil_light_mp4)
    shutil.copyfile(f5_light_webm, hasil_light_webm)

    # 7C. AUTOMATIC INTEGRATION INTO SO PROJECT!
    so_mp4_target = os.path.join(SO_Z4L5_DIR, f"{so_dest_stem}.mp4")
    so_webm_target = os.path.join(SO_Z4L5_DIR, f"{so_dest_stem}.webm")
    shutil.copyfile(f5_light_mp4, so_mp4_target)
    shutil.copyfile(f5_light_webm, so_webm_target)
    print(f"  🚀 OTOMATIS DISINKRONKAN KE PROYEK SO:")
    print(f"     -> {so_mp4_target}")
    print(f"     -> {so_webm_target}")

    # 8. Save video_project_data.json
    meta = {
        "id": vid_id,
        "title": cfg["title"],
        "subtitle": cfg["subtitle"],
        "so_game_name": cfg["so_game_name"],
        "so_dest_stem": so_dest_stem,
        "duration_seconds": round(total_dur, 2),
        "source_type": "local_mp4",
        "original_file": cfg["source_filename"],
        "original_size_bytes": orig_size,
        "compressed_mp4_bytes": f5_light_size,
        "compressed_webm_bytes": webm_light_size,
        "compression_savings_percent": round(f5_light_pct, 1),
        "original_speaker": "Prof. Yohanes Surya (Pria)",
        "dubbed_character": "Guru Marcia (Trainer Marcia Asli)",
        "voice_id": "so_marcia",
        "acceleration": "F5-TTS nfe_step=32 High-Fidelity + Spelled Out Numbers",
        "noise_filtering": "Highpass 80Hz + Loudnorm broadcast -16 LUFS",
        "files": {
            "original_video": f"/video-projects/{vid_id}/clip_original.mp4",
            "dubbed_video_f5": f"/video-projects/{vid_id}/video_dubbed_marcia_f5.mp4",
            "dubbed_video_edge": f"/video-projects/{vid_id}/video_dubbed_marcia_edge.mp4",
            "dubbed_video_f5_ringan": f"/video-projects/{vid_id}/video_dubbed_marcia_f5_ringan.mp4",
            "dubbed_audio_f5": f"/video-projects/{vid_id}/master_dubbing_f5.mp3",
            "dubbed_audio_edge": f"/video-projects/{vid_id}/master_dubbing_edge.mp3"
        },
        "so_files": {
            "mp4": f"/assets/videos/z4l5/{so_dest_stem}.mp4",
            "webm": f"/assets/videos/z4l5/{so_dest_stem}.webm"
        },
        "segments": segments
    }

    meta_file = os.path.join(project_dir, "video_project_data.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Metadata Studio Tersimpan: {meta_file}")

    return {
        "id": vid_id,
        "title": cfg["title"],
        "filename": cfg["source_filename"],
        "so_game_name": cfg["so_game_name"],
        "duration": total_dur,
        "original_size": orig_size,
        "light_mp4_size": f5_light_size,
        "light_webm_size": webm_light_size,
        "savings_pct": f5_light_pct,
        "so_mp4_target": so_mp4_target,
        "so_webm_target": so_webm_target
    }

async def main():
    print("=" * 80)
    print("  SPRINT VIDEO DUBBING MARCIA ZONA 4 LEVEL 5 (4 VIDEO) & SYNC SO")
    print("  Pelafalan Angka Fonetik Sempurna, Noise-Free, & Kompresi Ringan Prima")
    print("=" * 80)

    # Inisialisasi F5 Engine
    print("\n▶ Menginisialisasi F5-TTS Engine (High-Fidelity nfe_step=32)...")
    engine = F5IndoEngine.get_instance()
    marcia_ref = os.path.join(BASE_DIR, "assets", "cloned_voices", "at_marcia_ref.wav")
    marcia_ref_text = "Pertama kita tulis dulu nilai tempat jawabannya, ini ada ratusan, puluhan, dan satuan."

    results = []
    total_start = time.time()

    for idx, cfg in enumerate(VIDEOS_CONFIG, 1):
        print(f"\n==================== VIDEO {idx} / {len(VIDEOS_CONFIG)} ====================")
        res = await process_single_video(cfg, engine, marcia_ref, marcia_ref_text)
        results.append(res)

    total_time = time.time() - total_start
    total_orig = sum(r["original_size"] for r in results)
    total_light = sum(r["light_mp4_size"] for r in results)
    total_savings = (1 - (total_light / total_orig)) * 100 if total_orig > 0 else 0

    print("\n" + "=" * 80)
    print("🎉 SELURUH 4 VIDEO ZONA 4 LEVEL 5 BERHASIL DIDUBBING, DIKOMPRESI, DAN DIMASUKKAN KE SO!")
    print(f"Total Waktu Eksekusi : {total_time:.1f} detik ({total_time/60:.1f} menit)")
    print(f"Total Ukuran Asli    : {format_bytes(total_orig)}")
    print(f"Total Ukuran Ringan  : {format_bytes(total_light)}")
    print(f"Total Penghematan    : {total_savings:.1f}% LEBIH KECIL!")
    print("=" * 80)

    print("\n📋 Integrasi Proyek SO (/assets/videos/z4l5/):")
    for r in results:
        print(f"  • {r['title']}")
        print(f"    - Game SO       : {r['so_game_name']}")
        print(f"    - Berkas MP4 SO : {r['so_mp4_target']} ({format_bytes(r['light_mp4_size'])})")
        print(f"    - Berkas WebM SO: {r['so_webm_target']} ({format_bytes(r['light_webm_size'])})")

if __name__ == "__main__":
    asyncio.run(main())
