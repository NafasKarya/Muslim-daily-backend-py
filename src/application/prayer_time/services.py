from typing import Optional, Dict, List, Union
from datetime import time, date, datetime, timedelta

from src.domain.prayer_time.entities import PrayerSchedule, CurrentPrayerInfo
from src.domain.prayer_time.repositories import PrayerRepository

class PrayerTimeService:
    def __init__(self, repository: PrayerRepository):
        self._repository = repository

    def _calculate_current_prayer_info(self, schedules: List[PrayerSchedule]) -> Optional[CurrentPrayerInfo]:
        """
        Metode private yang berisi logika inti untuk menghitung mundur.
        Menerima daftar jadwal yang sudah diambil dari repository.
        """
        if not schedules:
            return None

        now = datetime.now()
        today_date = now.date()
        tomorrow_date = today_date + timedelta(days=1)

        today_schedule = next((s for s in schedules if s.date == today_date), None)
        tomorrow_schedule = next((s for s in schedules if s.date == tomorrow_date), None)
        
        if not today_schedule or not tomorrow_schedule:
            return None

        prayer_times_today = {
            "Fajr": datetime.combine(today_date, today_schedule.fajr),
            "Dhuhr": datetime.combine(today_date, today_schedule.dhuhr),
            "Asr": datetime.combine(today_date, today_schedule.asr),
            "Maghrib": datetime.combine(today_date, today_schedule.maghrib),
            "Isha": datetime.combine(today_date, today_schedule.isha),
            "Next Fajr": datetime.combine(tomorrow_date, tomorrow_schedule.fajr)
        }

        sorted_prayers = sorted(prayer_times_today.items(), key=lambda item: item[1])

        current_prayer_name = "Isha"
        next_prayer_name = "Next Fajr"
        
        for i in range(len(sorted_prayers)):
            prayer_name, prayer_time = sorted_prayers[i]
            if now < prayer_time:
                next_prayer_name = prayer_name
                current_prayer_name = sorted_prayers[i-1][0] if i > 0 else "Isha"
                break
        
        next_prayer_dt = prayer_times_today[next_prayer_name]
        time_difference = next_prayer_dt - now
        
        total_seconds = int(time_difference.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        display_next_prayer_name = "Fajr" if next_prayer_name == "Next Fajr" else next_prayer_name
        current_prayer_dt = prayer_times_today[current_prayer_name] if current_prayer_name != "Isha" else prayer_times_today["Isha"]
        
        return CurrentPrayerInfo(
            current_prayer_time=current_prayer_dt.time(),
            current_prayer_name=current_prayer_name,
            next_prayer_time=next_prayer_dt.time(),
            next_prayer_name=display_next_prayer_name,
            countdown_to_next=countdown_str,
            date=today_date
        )
    
    def get_current_prayer_info(
        self, 
        location: Union[str, Dict[str, float]]
    ) -> Optional[CurrentPrayerInfo]:
        """
        Satu metode utama untuk mendapatkan info sholat saat ini.
        Bisa menerima nama kota (str) atau koordinat GPS (dict).
        """
        today_date = date.today()
        schedules = None

        # Tentukan cara mengambil data berdasarkan tipe input 'location'
        if isinstance(location, str): # Jika input adalah nama kota
            schedules = self._repository.get_monthly_schedule(today_date.year, today_date.month, location)
        elif isinstance(location, dict) and 'latitude' in location and 'longitude' in location: # Jika input adalah GPS
            schedules = self._repository.get_monthly_schedule_by_coordinates(
                today_date.year, today_date.month, location['latitude'], location['longitude']
            )
        
        if not schedules:
            return None

        # Handle jika butuh data bulan berikutnya
        tomorrow_date = today_date + timedelta(days=1)
        if tomorrow_date.month != today_date.month:
            next_month_schedules = None
            if isinstance(location, str):
                next_month_schedules = self._repository.get_monthly_schedule(tomorrow_date.year, tomorrow_date.month, location)
            elif isinstance(location, dict):
                 next_month_schedules = self._repository.get_monthly_schedule_by_coordinates(
                    tomorrow_date.year, tomorrow_date.month, location['latitude'], location['longitude']
                )
            if next_month_schedules:
                schedules.extend(next_month_schedules)

        # Serahkan ke metode private untuk dihitung
        return self._calculate_current_prayer_info(schedules)

    def _add_sunnah_prayers(self, schedules: List[PrayerSchedule]) -> List[PrayerSchedule]:
        # ... (fungsi ini tidak berubah) ...
        if not schedules:
            return []
        modified_schedules = []
        for schedule in schedules:
            today = schedule.date
            tahajjud_time_str = f"02:00 - {schedule.fajr.strftime('%H:%M')}"
            sunrise_dt = datetime.combine(today, schedule.sunrise)
            dhuha_start_dt = sunrise_dt + timedelta(minutes=15)
            dhuhr_dt = datetime.combine(today, schedule.dhuhr)
            dhuha_end_dt = dhuhr_dt - timedelta(minutes=10)
            dhuha_time_str = f"{dhuha_start_dt.strftime('%H:%M')} - {dhuha_end_dt.strftime('%H:%M')}"
            new_schedule = PrayerSchedule(
                date=schedule.date, imsak=schedule.imsak, fajr=schedule.fajr,
                sunrise=schedule.sunrise, dhuhr=schedule.dhuhr, asr=schedule.asr,
                maghrib=schedule.maghrib, isha=schedule.isha, tahajjud=tahajjud_time_str,
                dhuha=dhuha_time_str
            )
            modified_schedules.append(new_schedule)
        return modified_schedules

    def get_monthly_schedule(self, year: int, month: int, city: str) -> Optional[List[PrayerSchedule]]:
        # ... (fungsi ini tidak berubah) ...
        if not all([year, month, city]):
            return None
        schedule_list = self._repository.get_monthly_schedule(year, month, city)
        return self._add_sunnah_prayers(schedule_list)

    def get_monthly_schedule_by_coordinates(self, year: int, month: int, latitude: float, longitude: float) -> Optional[List[PrayerSchedule]]:
        # ... (fungsi ini tidak berubah) ...
        if not all([year, month, latitude is not None, longitude is not None]):
            return None
        schedule_list = self._repository.get_monthly_schedule_by_coordinates(year, month, latitude, longitude)
        return self._add_sunnah_prayers(schedule_list)