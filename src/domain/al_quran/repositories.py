# src/domain/al_quran/repositories.py

from abc import ABC, abstractmethod
from typing import Optional, List

# --- Path import baru, spesifik untuk entitas Al-Quran ---
from src.domain.al_quran.entities import Surah, SurahDetail

class AlQuranRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk mendapatkan data Al-Quran.
    
    Lapisan aplikasi (services) akan bergantung pada abstraksi ini,
    bukan pada implementasi konkret (misal: dari API mana data diambil).
    Ini memungkinkan kita untuk menukar sumber data di masa depan tanpa
    mengubah logika bisnis di service.
    """
    
    @abstractmethod
    def get_all_surahs(self) -> Optional[List[Surah]]:
        """
        Mengambil daftar ringkas semua surah dalam Al-Quran.
        """
        pass

    @abstractmethod
    def get_surah_by_number(self, surah_number: int) -> Optional[SurahDetail]:
        """
        Mengambil detail lengkap sebuah surah berdasarkan nomornya,
        termasuk semua ayat di dalamnya.
        """
        pass