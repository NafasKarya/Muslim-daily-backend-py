from typing import Optional, List

# --- Path import baru, spesifik untuk Al-Quran ---
from src.domain.al_quran.entities import Surah, SurahDetail, Ayah, TafsirDetail
from src.domain.al_quran.repositories import AlQuranRepository

class AlQuranService:
    """
    Application service yang mengatur use case terkait Al-Quran.
    """
    
    def __init__(self, repository: AlQuranRepository):
        self._repository = repository
        
    def get_all_surahs(self) -> Optional[List[Surah]]:
        """
        Use case: Mendapatkan daftar semua surah dalam Al-Quran.
        
        Mengembalikan daftar ringkas berisi nomor, nama, arti, dan jumlah ayat
        dari setiap surah.
        """
        return self._repository.get_all_surahs()

    def get_surah_detail(self, surah_number: int) -> Optional[SurahDetail]:
        """
        Use case: Mendapatkan detail lengkap sebuah surah berdasarkan nomornya,
        termasuk semua ayat di dalamnya.
        
        Args:
            surah_number (int): Nomor urut surah (1 sampai 114).
            
        Returns:
            Optional[SurahDetail]: Objek detail surah jika ditemukan, jika tidak None.
        """
        # Validasi sederhana untuk memastikan nomor surah valid
        if not 1 <= surah_number <= 114:
            return None
        
        return self._repository.get_surah_by_number(surah_number)

    def get_specific_ayah(self, surah_number: int, ayah_number: int) -> Optional[Ayah]:
        """
        Use case: Mendapatkan satu ayat spesifik dari sebuah surah.
        
        Args:
            surah_number (int): Nomor urut surah (1 sampai 114).
            ayah_number (int): Nomor urut ayat di dalam surah tersebut.
            
        Returns:
            Optional[Ayah]: Objek ayat jika ditemukan, jika tidak None.
        """
        # Pertama, ambil seluruh detail surah menggunakan metode yang sudah ada.
        surah_detail = self.get_surah_detail(surah_number)
        
        if not surah_detail:
            return None
        
        # Kemudian, cari ayat yang cocok di dalam daftar ayat surah tersebut.
        for ayah in surah_detail.ayahs:
            if ayah.numberInSurah == ayah_number:
                return ayah
        
        # Kembalikan None jika nomor ayat tidak ditemukan di surah tersebut.
        return None

    def get_tafsir(self, surah_number: int) -> Optional[TafsirDetail]:
        """
        Use case: Mendapatkan detail tafsir dari sebuah surah.

        Args:
            surah_number (int): Nomor urut surah (1 sampai 114).

        Returns:
            Optional[TafsirDetail]: Objek detail tafsir jika ditemukan, jika tidak None.
        """
        # Validasi sederhana untuk memastikan nomor surah valid
        if not 1 <= surah_number <= 114:
            return None
        
        # Panggil metode repository yang sesuai untuk mengambil data tafsir
        return self._repository.get_tafsir_by_surah_number(surah_number)
