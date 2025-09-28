# src/application/prayer_time/services.py

from typing import Optional, Dict, List
from datetime import time, date, datetime, timedelta

from src.domain.prayer_time.entities import PrayerSchedule
from src.domain.prayer_time.repositories import PrayerRepository

class PrayerTimeService:
    def __init__(self, repository: PrayerRepository):
        self._repository = repository

    def _add_sunnah_prayers(self, schedules: List[PrayerSchedule]) -> List[PrayerSchedule]:
        """
        Fungsi internal untuk menambahkan jadwal salat sunnah (Tahajud & Dhuha)
        ke dalam daftar jadwal yang sudah ada.
        """
        if not schedules:
            return []

        modified_schedules = []
        for schedule in schedules:
            today = schedule.date
            
            # 1. Tentukan waktu Tahajud
            # Rentang dari jam 02:00 hingga waktu Subuh (fajr).
            tahajjud_time_str = f"02:00 - {schedule.fajr.strftime('%H:%M')}"
            
            # 2. Hitung waktu mulai Dhuha: 15 menit setelah waktu Terbit (sunrise)
            sunrise_dt = datetime.combine(today, schedule.sunrise)
            dhuha_start_dt = sunrise_dt + timedelta(minutes=15)
            
            # 3. Hitung waktu akhir Dhuha: 10 menit sebelum waktu Zuhur
            dhuhr_dt = datetime.combine(today, schedule.dhuhr)
            dhuha_end_dt = dhuhr_dt - timedelta(minutes=10)

            # Format rentang waktu Dhuha menjadi string
            dhuha_time_str = f"{dhuha_start_dt.strftime('%H:%M')} - {dhuha_end_dt.strftime('%H:%M')}"

            # 4. Buat objek baru dengan data tambahan
            # Karena dataclass kita 'frozen' (immutable), kita tidak bisa mengubahnya.
            # Cara yang benar adalah membuat salinan baru dengan nilai yang diperbarui.
            new_schedule = PrayerSchedule(
                date=schedule.date,
                imsak=schedule.imsak,
                fajr=schedule.fajr,
                sunrise=schedule.sunrise,
                dhuhr=schedule.dhuhr,
                asr=schedule.asr,
                maghrib=schedule.maghrib,
                isha=schedule.isha,
                tahajjud=tahajjud_time_str,
                dhuha=dhuha_time_str # Menggunakan rentang waktu yang baru
            )
            modified_schedules.append(new_schedule)
            
        return modified_schedules

    def get_monthly_schedule(self, year: int, month: int, city: str) -> Optional[List[PrayerSchedule]]:
        """
        Use case: Mendapatkan jadwal sholat bulanan berdasarkan nama kota.
        """
        if not all([year, month, city]):
            return None
        
        # Panggil repository untuk mendapatkan jadwal salat wajib
        schedule_list = self._repository.get_monthly_schedule(year, month, city)
        
        # Tambahkan jadwal sunnah sebelum mengembalikannya
        return self._add_sunnah_prayers(schedule_list)

    def get_monthly_schedule_by_coordinates(self, year: int, month: int, latitude: float, longitude: float) -> Optional[List[PrayerSchedule]]:
        """
        Use case: Mendapatkan jadwal sholat bulanan berdasarkan koordinat GPS.
        """
        if not all([year, month, latitude is not None, longitude is not None]):
            return None
            
        # Panggil repository untuk mendapatkan jadwal salat wajib
        schedule_list = self._repository.get_monthly_schedule_by_coordinates(year, month, latitude, longitude)
        
        # Tambahkan jadwal sunnah sebelum mengembalikannya
        return self._add_sunnah_prayers(schedule_list)

    def get_all_provinces(self) -> Optional[Dict[str, str]]:
        return self._repository.get_all_provinces()

    def get_cities(self, province_id: str) -> Optional[Dict[str, str]]:
        if not province_id:
            return None
        return self._repository.get_cities_by_province(province_id)