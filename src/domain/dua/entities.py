from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Dua:
    """
    Mewakili ringkasan dari sebuah doa.
    Entitas ini digunakan untuk menampilkan daftar semua doa.
    """
    id: int
    title: str
    category: str
    reference: Optional[str]

@dataclass(frozen=True)
class DuaText:
    """
    Mewakili satu versi/teks dari sebuah doa (misal: arab, latin, arti).
    """
    language: str   # 'arabic', 'latin', 'translation'
    text: str

@dataclass(frozen=True)
class DuaDetail:
    """
    Mewakili data lengkap dari sebuah doa, mencakup informasi
    dasar dan daftar semua versi teks (arab, latin, terjemahan, dll).
    Bisa juga mengandung penjelasan/hikmah dan inspirasi jika ada.
    """
    id: int
    title: str
    category: str
    reference: Optional[str]
    texts: List[DuaText]
    hikmah: Optional[str] = None      # <-- field hikmah
    inspirasi: Optional[str] = None   # <-- field inspirasi

# --- ENTITAS BARU UNTUK PENJELASAN/TAFSIR DUA ---

@dataclass(frozen=True)
class DuaExplanation:
    """
    Mewakili satu entri penjelasan/tafsir untuk sebuah doa.
    """
    dua_id: int
    explanation: str

@dataclass(frozen=True)
class DuaExplanationDetail:
    """
    Mewakili data lengkap penjelasan untuk sebuah doa tertentu.
    """
    id: int
    title: str
    explanation: str
