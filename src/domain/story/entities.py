from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Story:
    """
    Mewakili ringkasan dari sebuah cerita/legenda dari kitab klasik.
    Digunakan untuk daftar/list story.
    """
    id: int
    title: str
    kitab: str                # Nama kitab utama (misal: 'Ajaib al-Makhluqat', 'Nukhbat al-Dahr')
    category: str             # Kategori cerita (misal: makhluk aneh, misteri laut, dsb)
    reference: Optional[str]  # Sumber, misal: halaman, bab, atau kutipan kitab

@dataclass(frozen=True)
class StoryText:
    """
    Mewakili satu versi teks/paragraf dari story (misal: original arabic, terjemahan, ringkasan).
    """
    language: str             # 'arabic', 'translation', 'summary', dll
    text: str

@dataclass(frozen=True)
class StoryDetail:
    """
    Data lengkap satu cerita kitab: info dasar + isi cerita.
    (Bisa multibahasa).
    """
    id: int
    title: str
    kitab: str
    category: str
    reference: Optional[str]
    texts: List[StoryText]

# --- ENTITAS BARU UNTUK PENJELASAN/TAFSIR CERITA ---

@dataclass(frozen=True)
class StoryExplanation:
    """
    Satu entri penjelasan/tafsir atau konteks untuk sebuah cerita.
    """
    story_id: int
    explanation: str

@dataclass(frozen=True)
class StoryExplanationDetail:
    """
    Data lengkap penjelasan/tafsir untuk satu cerita tertentu.
    """
    id: int
    title: str
    explanation: str
