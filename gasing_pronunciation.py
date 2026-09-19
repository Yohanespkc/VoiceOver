"""
GASING & Bilingual Pronunciation Preprocessor for F5-TTS Indo
Mengoptimalkan teks bahasa Indonesia dan istilah serapan Inggris khusus game Sacred Octagon (SO)
serta metode pembelajaran matematika GASING.

Aturan Utama:
1. "AI" -> "ei-ai" (dilafalkan dalam intonasi bahasa Inggris, bukan "a-i" Indonesia).
2. "GASING" -> "Gasing" (diproteksi agar tidak terbaca bahasa Inggris "gey-sing").
3. Ekspresi Pujian GASING ("W O W", "Kasih WOW", "Hebaat", "Kereeen", "Luar biasa").
4. Smart sentence chunker agar generasi audio F5-TTS stabil dan tidak berhalusinasi.
"""

import re
from typing import List, Dict

# Kamus kata serapan / istilah teknologi & game yang harus berbunyi bahasa Inggris alami
BILINGUAL_ENGLISH_MAP: Dict[str, str] = {
    r"\bAI\b": "ei-ai",
    r"\bA\.I\.\b": "ei-ai",
    r"\bgame\b": "geim",
    r"\bgames\b": "geims",
    r"\bplayer\b": "pleyer",
    r"\bplayers\b": "pleyers",
    r"\bstage\b": "steij",
    r"\bquests?\b": "kwes",
    r"\bscores?\b": "skor",
    r"\bcombos?\b": "kombo",
    r"\bperfect\b": "perfek",
    r"\bonline\b": "onlain",
    r"\boffline\b": "oflain",
    r"\btouch\b": "tac",
    r"\bclick\b": "klik",
    r"\bsound\b": "saund",
    r"\bvoice\b": "vois",
    r"\bvoices?\b": "voises",
    r"\bvoiceover\b": "vois over",
    r"\bvoice-over\b": "vois over",
    r"\bdownload\b": "daunlod",
    r"\bupdate\b": "apdet",
    r"\bpause\b": "pos",
    r"\bresume\b": "rizyum",
    r"\bskip\b": "skip",
    r"\bstart\b": "stat",
    r"\bclear\b": "klir",
    r"\bstage clear\b": "steij klir",
    r"\bgame over\b": "geim over",
    r"\blevel up\b": "level ap",
    r"\bbonus\b": "bonus",
    r"\bcheckpoint\b": "cek poin",
    r"\bhud\b": "had",
    r"\bchallenge\b": "celenj",
    r"\bboss\b": "bos",
    r"\bsuper\b": "super",
    r"\bfantastic\b": "fantastik",
    r"\byoutube\b": "yutyub",
    r"\bvideo\b": "video",
    r"\baudio\b": "audio",
    r"\bstudio\b": "studio",
    r"\bflow\b": "flou",
}

# Proteksi istilah autentik khas GASING dan Game SO
PROTECTED_INDONESIAN_TERMS: Dict[str, str] = {
    r"\bgasing\b": "Gasing",
    r"\bGASING\b": "Gasing",
    r"\bGaber\b": "Gaber",
    r"\bgaber\b": "Gaber",
    r"\bOctagon\b": "Oktagon",
    r"\boctagon\b": "Oktagon",
    r"\bSacred Octagon\b": "Seikred Oktagon",
    r"\bBabilon\b": "Babilon",
    r"\bbabilon\b": "Babilon",
    r"\bMarcia\b": "Marsia",
    r"\bmarcia\b": "Marsia",
    r"\bXander\b": "Zander",
    r"\bxander\b": "Zander",
    r"\bBlaze\b": "Bleiz",
    r"\bblaze\b": "Bleiz",
    r"\bmencongak\b": "mencongak",
    r"\blirik kanan\b": "lirik kanan",
    r"\bkotak-kotak\b": "kotak-kotak",
    r"\bpasangan bilangan\b": "pasangan bilangan",
    r"\bpenjumlahan\b": "penjumlahan",
    r"\bpengurangan\b": "pengurangan",
    r"\bperkalian\b": "perkalian",
    r"\bpembagian\b": "pembagian",
    r"\basyik\b": "asyik",
    r"\bmenyenangkan\b": "menyenangkan",
    r"\bgampang\b": "gampang",
}

# Format Pujian Khas GASING
GASING_PRAISE_RULES = [
    (r"\bKasih\s+We\s+o\s+We\s+WOW\b!*\s*", "Kasih We, kasih O, kasih We, WOW! "),
    (r"\bKasih\s+W\s*O\s*W\b!*\s*", "Kasih We, kasih O, kasih We, WOW! "),
    (r"\bKasih\s+WOW\b!*\s*", "Kasih We, kasih O, kasih We, WOW! "),
    (r"\b(?<!kasih\s)W\s*O\s*W\b!*\s*", "We O We, WOW! "),
    (r"\b(?<!kasih\s)W-O-W\b!*\s*", "We O We, WOW! "),
    (r"\bhebaa+t\b!*\s*", "hebaat! "),
    (r"\bkereee+n\b!*\s*", "kereen! "),
    (r"\bluar\s+biasaaa*\b!*\s*", "luar biasa! "),
    (r"\bMANTAP\b!*\s*", "Mantap! "),
    (r"\bHEBAT\b!*\s*", "Hebat! "),
    (r"\bKEREN\b!*\s*", "Keren! "),
    (r"\bLUAR\s+BIASA\b!*\s*", "Luar biasa! "),
]

def preprocess_pronunciation(text: str, apply_bilingual: bool = True, apply_gasing_prosody: bool = True) -> str:
    """
    Menormalkan teks masukan agar F5-TTS melafalkannya dengan aksen dan artikulasi sempurna.
    """
    if not text:
        return ""

    processed = text

    # 1. Bersihkan spasi berlebih
    processed = re.sub(r"\s+", " ", processed).strip()

    # 2. Pujian GASING (gunakan tokenisasi unik untuk mencegah tabrakan regex berulang)
    if apply_gasing_prosody:
        processed = re.sub(
            r"\bKasih\s+(?:We\s+o\s+We\s+WOW|W[\s\.\-]+O[\s\.\-]+W|W\s*O\s*W|WOW)\b!*\s*",
            "__KASIH_WOW_TOKEN__ ",
            processed,
            flags=re.IGNORECASE
        )
        processed = re.sub(
            r"\b(?:W[\s\.\-]+O[\s\.\-]+W|W-O-W)\b!*\s*",
            "We O We, WOW! ",
            processed,
            flags=re.IGNORECASE
        )
        processed = processed.replace("__KASIH_WOW_TOKEN__", "Kasih We, kasih O, kasih We, WOW!")

        for pattern, repl in [
            (r"\bhebaa+t\b!*\s*", "hebaat! "),
            (r"\bkereee+n\b!*\s*", "kereen! "),
            (r"\bluar\s+biasaaa*\b!*\s*", "luar biasa! "),
            (r"\bMANTAP\b!*\s*", "Mantap! "),
            (r"\bHEBAT\b!*\s*", "Hebat! "),
            (r"\bKEREN\b!*\s*", "Keren! "),
            (r"\bLUAR\s+BIASA\b!*\s*", "Luar biasa! "),
        ]:
            processed = re.sub(pattern, repl, processed, flags=re.IGNORECASE)

    # 3. Istilah Proteksi GASING & SO
    for pattern, repl in PROTECTED_INDONESIAN_TERMS.items():
        processed = re.sub(pattern, repl, processed, flags=re.IGNORECASE)

    # 4. Istilah Serapan Bahasa Inggris (AI dibaca "ei-ai", game dibaca "geim", dsb)
    if apply_bilingual:
        for pattern, repl in BILINGUAL_ENGLISH_MAP.items():
            processed = re.sub(pattern, repl, processed)

    # 5. Normalisasi angka dan simbol umum
    processed = re.sub(r"\b0\b", "nol", processed)
    processed = re.sub(r"\+", " tambah ", processed)
    processed = re.sub(r"\=", " sama dengan ", processed)
    processed = re.sub(r"\×|\*", " kali ", processed)
    processed = re.sub(r"\÷|\/", " bagi ", processed)
    processed = re.sub(r"\%", " persen", processed)

    # 6. Pembersihan tanda baca berulang yang menyebabkan desisan/looping pada F5-TTS
    processed = re.sub(r"\.{2,}", ".", processed)       # Ubah '....' menjadi '.'
    processed = re.sub(r"!{2,}", "!", processed)       # Ubah '!!' menjadi '!'
    processed = re.sub(r"\?{2,}", "?", processed)     # Ubah '??' menjadi '?'
    processed = re.sub(r"\s+([.,!?;:])", r"\1", processed)  # Hapus spasi sebelum tanda baca (cth: 'Hebat !' -> 'Hebat!')
    processed = re.sub(r"([.,!?;:])(?=[^\s\d])", r"\1 ", processed) # Pastikan ada spasi setelah tanda baca

    # Rapikan spasi lagi
    processed = re.sub(r"\s+", " ", processed).strip()
    return processed

def split_into_smart_chunks(text: str, max_chars: int = 180) -> List[str]:
    """
    Memecah naskah panjang menjadi potongan-potongan pendek pada batas tanda baca alami
    agar F5-TTS tidak kehilangan nafas / berhalusinasi pada kalimat panjang.
    """
    if not text:
        return []

    # Jika teks sudah cukup pendek, kembalikan langsung
    if len(text) <= max_chars:
        return [text]

    # Split berdasarkan kalimat (. ! ? ;)
    sentence_endings = re.split(r"([.!?;\n]+)", text)
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentence_endings), 2):
        sentence = sentence_endings[i].strip()
        punctuation = sentence_endings[i+1].strip() if i+1 < len(sentence_endings) else ""

        full_part = (sentence + (" " + punctuation if punctuation else "")).strip()
        if not full_part:
            continue

        if len(current_chunk) + len(full_part) + 1 <= max_chars:
            if current_chunk:
                current_chunk += " " + full_part
            else:
                current_chunk = full_part
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Jika kalimat tunggal itu sendiri lebih panjang dari max_chars, split pada koma
            if len(full_part) > max_chars:
                comma_parts = re.split(r"([,]+)", full_part)
                sub_chunk = ""
                for j in range(0, len(comma_parts), 2):
                    sub = comma_parts[j].strip()
                    comma = comma_parts[j+1].strip() if j+1 < len(comma_parts) else ""
                    piece = (sub + comma).strip()
                    if len(sub_chunk) + len(piece) + 1 <= max_chars:
                        sub_chunk = (sub_chunk + " " + piece).strip()
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        sub_chunk = piece
                if sub_chunk:
                    current_chunk = sub_chunk
                else:
                    current_chunk = ""
            else:
                current_chunk = full_part

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

if __name__ == "__main__":
    sample = "Selamat datang di game GASING! Bersama asisten AI, mari kita raih skor tertinggi. Kasih W O W! 1 + 1 = 2."
    normalized = preprocess_pronunciation(sample)
    print("Original  :", sample)
    print("Normalized:", normalized)
    chunks = split_into_smart_chunks(normalized)
    print("Chunks    :", chunks)
