# src/domain/prayer_time/repositories.py

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

# --- Path import baru, spesifik untuk entitas jadwal sholat ---
from src.domain.prayer_time.entities import PrayerSchedule

class PrayerRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk mengambil jadwal sholat.
    """
    
    @abstractmethod
    def get_prayer_schedule(
        self, target_date: date, latitude: float, longitude: float
    ) -> Optional[PrayerSchedule]:
        """
        Mendapatkan jadwal sholat untuk tanggal dan lokasi tertentu.
        """
        pass