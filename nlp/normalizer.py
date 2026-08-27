"""
Thai text normalization and typo-correction module using PyThaiNLP and custom coffee dictionaries.
"""
import re
from typing import List
from pythainlp.util import normalize as thai_normalize
from pythainlp.tokenize import word_tokenize

# Common colloquial terms, abbreviations, and typo mapping
SPELL_CORRECTION_MAP = {
    "กาเเฟ": "กาแฟ",
    "ชาเขีบว": "ชาเขียว",
    "ชาเขียวว": "ชาเขียว",
    "มัชฉะ": "มัทฉะ",
    "มัจฉะ": "มัทฉะ",
    "แมทฉะ": "มัทฉะ",
    "แฟรปเป้": "แฟรปปูชิโน่",
    "แฟรปปู": "แฟรปปูชิโน่",
    "แฟรบเป้": "แฟรปปูชิโน่",
    "แฟบปูชิโน่": "แฟรปปูชิโน่",
    "คาปู": "คาปูชิโน่",
    "คาปูชิโน": "คาปูชิโน่",
    "อเมกาโน่": "อเมริกาโน่",
    "อเมริกาโน": "อเมริกาโน่",
    "อเมริ": "อเมริกาโน่",
    "ม็อคค่า": "มอคค่า",
    "มอคคา": "มอคค่า",
    "มอคค่าา": "มอคค่า",
    "ลาเต้้": "ลาเต้",
    "ลาเต": "ลาเต้",
    "มัคคิอาโต": "มัคคิอาโต",
    "มัคคิอาโต้": "มัคคิอาโต",
    "โคลบรูว์": "โคลด์ บรูว์",
    "โคลบลู": "โคลด์ บรูว์",
    "โคลดบรู": "โคลด์ บรูว์",
    "โคลด์บรู": "โคลด์ บรูว์",
    "ครัวซองค์": "ครัวซองต์",
    "ครัวซอง": "ครัวซองต์",
    "ชีสเค้กก": "ชีสเค้ก",
    "สตอเบอรี่": "สตรอเบอร์รี่",
    "สตรอเบอรี่": "สตรอเบอร์รี่",
    "สตรอเบอรี": "สตรอเบอร์รี่",
    "คาราเมลลี่": "คาราเมล",
    "ช็อกโกแลตต": "ช็อกโกแลต",
    "ช็อคโกแลต": "ช็อกโกแลต",
    "ชอคโกแลต": "ช็อกโกแลต",
    "ชอคโกเลต": "ช็อกโกแลต",
    "โกโก้้": "โกโก้",
    "สมูทตี้": "ปั่น",
    "ฟราปเป้": "แฟรปปูชิโน่",
    "สตาร์บัค": "สตาร์บัคส์",
    "สตาร์บัคส": "สตาร์บัคส์",
    "สตาบัค": "สตาร์บัคส์",
    "สตาบัคส์": "สตาร์บัคส์",
    "โปโมชั่น": "โปรโมชั่น",
    "โปรโมชัน": "โปรโมชั่น",
    "โปรโมชี่น": "โปรโมชั่น",
    "ส่วนลดด": "ส่วนลด",
    "ปั่นน": "ปั่น",
    "เยน": "เย็น",
    "กิินไรดี": "กินอะไรดี",
    "กินไรดี": "กินอะไรดี",
    "มีไรบ้าง": "มีอะไรบ้าง",
    "มีไรใหม่": "มีอะไรใหม่",
    "สุ่มม": "สุ่ม",
}


def normalize_text(text: str) -> str:
    """
    Normalizes Thai text, fixes common typos, lowercases English characters,
    and removes repetitive punctuation.
    """
    if not text:
        return ""

    # PyThaiNLP Unicode normalization
    cleaned = thai_normalize(text.strip())

    # Lowercase Latin characters and strip accents (e.g. caffè -> caffe)
    cleaned = cleaned.lower()
    cleaned = cleaned.replace("è", "e").replace("é", "e").replace("ê", "e").replace("à", "a").replace("á", "a")

    # Replace typo tokens (sorted by length descending to prevent sub-token collisions)
    for wrong in sorted(SPELL_CORRECTION_MAP.keys(), key=len, reverse=True):
        right = SPELL_CORRECTION_MAP[wrong]
        if wrong in cleaned and right not in cleaned:
            cleaned = cleaned.replace(wrong, right)

    # Clean any accidental double tokens
    cleaned = cleaned.replace("แฟรปปูชิโน่ชิโน่", "แฟรปปูชิโน่").replace("อเมริกาโน่โน่", "อเมริกาโน่")

    # Standardize repeated characters (e.g. อร่อยยยย -> อร่อย)
    cleaned = re.sub(r'(.)\1{2,}', r'\1', cleaned)

    # Remove extra whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def tokenize_text(text: str) -> List[str]:
    """Tokenizes normalized Thai text into word tokens."""
    norm = normalize_text(text)
    return word_tokenize(norm, engine="newmm")
