# src/infrastructure/calendar/date_converter.py

from datetime import date
from typing import Optional

# --- DIUBAH: Import 'Gregorian' bukan 'Hijri' ---
from hijri_converter import Gregorian

from src.domain.calendar.entities import HijriDate
from src.domain.calendar.repositories import HijriDateRepository

# Kita gabungkan semua class infrastruktur di sini sesuai struktur terakhir
from src.domain.prayer_time.entities import PrayerSchedule
from src.domain.prayer_time.repositories import PrayerRepository
from PrayTimes import PrayTimes


class HijriConverterRepository(HijriDateRepository):
    """
    Implementasi konkret dari HijriDateRepository menggunakan 'hijri-converter'.
    """
    def convert_gregorian_to_hijri(self, gregorian_date: date) -> Optional[HijriDate]:
        try:
            # --- DIUBAH: Menggunakan cara pemanggilan yang benar ---
            # 1. Buat objek Gregorian
            gregorian_obj = Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
            # 2. Konversi ke objek Hijri
            hijri_obj = gregorian_obj.to_hijri()
            
            return HijriDate(
                year=hijri_obj.year,
                month=hijri_obj.month,
                day=hijri_obj.day,
                month_name=hijri_obj.month_name(),
                day_name=hijri_obj.day_name()
            )
        except Exception as e:
            print(f"DEBUG: Error dari library hijri-converter: {e}")
            return None

# Class ini ditambahkan di sini agar sesuai dengan app.py terakhir
class PrayTimesRepository(PrayerRepository):
    """
    Implementasi konkret dari PrayerRepository menggunakan mesin hitung PrayTimes.
    """
    def get_prayer_schedule(
        self, target_date: date, latitude: float, longitude: float
    ) -> Optional[PrayerSchedule]:
        try:
            pt = PrayTimes()
            pt.set_prayer_method('MWL')
            pt.set_asr_method('Standard')
            timezone = 7 # WIB (UTC+7)

            times = pt.get_times(
                (target_date.year, target_date.month, target_date.day),
                (latitude, longitude),
                timezone
            )

            return PrayerSchedule(
                date=target_date.strftime('%Y-%m-%d'),
                fajr=times['fajr'],
                sunrise=times['sunrise'],
                dhuhr=times['dhuhr'],
                asr=times['asr'],
                maghrib=times['maghrib'],
                isha=times['isha']
            )
        except Exception:
            return None