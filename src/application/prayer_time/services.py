# src/application/prayer_time/services.py

from datetime import date
from typing import Optional

# --- Path import baru, spesifik untuk jadwal sholat ---
from src.domain.prayer_time.entities import PrayerSchedule
from src.domain.prayer_time.repositories import PrayerRepository

class PrayerTimeService:
    """
    Application service untuk menangani use case terkait jadwal sholat.
    """
    def __init__(self, repository: PrayerRepository):
        self._repository = repository

    def get_schedule_for_date(
        self, year: int, month: int, day: int, latitude: float, longitude: float
    ) -> Optional[PrayerSchedule]:
        """
        Use case: Mendapatkan jadwal sholat untuk tanggal dan lokasi tertentu.
        """
        try:
            target_date = date(year, month, day)
        except ValueError:
            return None # Komponen tanggal tidak valid
            
        return self._repository.get_prayer_schedule(target_date, latitude, longitude)