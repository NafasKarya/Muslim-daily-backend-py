from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Surah:
    """
    Mewakili ringkasan dari sebuah surah dalam Al-Quran.
    Entitas ini digunakan untuk menampilkan daftar semua surah.
    'frozen=True' membuatnya immutable, praktik yang baik untuk entitas domain.
    """
    number: int
    name: str
    englishName: str
    englishNameTranslation: str
    numberOfAyahs: int
    revelationType: str

@dataclass(frozen=True)
class Ayah:
    """
    Mewakili satu ayat di dalam sebuah surah.
    """
    numberInSurah: int
    text: str
    translation: str
    audio: Optional[str] = None # URL Audio bersifat opsional

@dataclass(frozen=True)
class SurahDetail:
    """
    Mewakili data lengkap dari sebuah surah, yang mencakup informasi
    dasar surah itu sendiri beserta daftar semua ayat di dalamnya.
    """
    # Mengandung semua informasi dari entitas Surah
    number: int
    name: str
    englishName: str
    englishNameTranslation: str
    numberOfAyahs: int
    revelationType: str
    
    # Ditambah dengan daftar lengkap semua ayatnya
    ayahs: List[Ayah]

# --- ENTITAS BARU UNTUK TAFSIR DITAMBAHKAN DI SINI ---

@dataclass(frozen=True)
class Tafsir:
    """
    Mewakili satu entri tafsir untuk satu ayat spesifik.
    """
    ayat: int
    teks: str

@dataclass(frozen=True)
class TafsirDetail:
    """
    Mewakili data lengkap dari tafsir sebuah surah, yang mencakup
    informasi dasar surah dan daftar tafsir untuk setiap ayatnya.
    """
    nomor: int
    nama: str
    namaLatin: str
    jumlahAyat: int
    tafsir: List[Tafsir]
