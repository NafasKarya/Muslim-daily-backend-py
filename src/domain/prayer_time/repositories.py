from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Dict, List # Import Dict dan List

# --- Path import untuk entitas jadwal sholat ---
from src.domain.prayer_time.entities import PrayerSchedule

class PrayerRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk repository yang menyediakan
    data jadwal sholat dan informasi terkait lokasi dari Kemenag.
    """
    
    # --- METODE BARU ---
    @abstractmethod
    def get_all_provinces(self) -> Optional[Dict[str, str]]:
        """
        Mengambil daftar semua provinsi dari sumber data.

        Returns:
            Dict[str, str]: Sebuah dictionary yang memetakan 
                            nama provinsi ke ID provinsi. Contoh: {'JAWA BARAT': '12'}.
                            None jika terjadi kegagalan.
        """
        pass

    # --- METODE BARU ---
    @abstractmethod
    def get_cities_by_province(self, province_id: str) -> Optional[Dict[str, str]]:
        """
        Mengambil daftar kota/kabupaten untuk ID provinsi tertentu.

        Args:
            province_id (str): ID unik provinsi dari sumber data.

        Returns:
            Dict[str, str]: Sebuah dictionary yang memetakan 
                            nama kota ke ID kota. Contoh: {'KOTA BANDUNG': '322'}.
                            None jika terjadi kegagalan.
        """
        pass

    # --- METODE LAMA DIHAPUS DAN DIGANTI DENGAN YANG BARU INI ---
    @abstractmethod
    def get_monthly_schedule(self, year: int, month: int, city_id: str) -> Optional[List[PrayerSchedule]]:
        """
        Mengambil jadwal sholat untuk satu bulan penuh berdasarkan ID kota.

        Args:
            year (int): Tahun yang diinginkan.
            month (int): Bulan yang diinginkan (1-12).
            city_id (str): ID unik kota/kabupaten dari sumber data.

        Returns:
            List[PrayerSchedule]: Sebuah list berisi objek PrayerSchedule untuk setiap hari 
                                 dalam bulan tersebut. None jika terjadi kegagalan.
        """
        pass