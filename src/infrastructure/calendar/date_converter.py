# src/infrastructure/calendar/date_converter.py

from datetime import date
from typing import Optional

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
    Menggunakan nama bulan Arab formal dari library dan nama hari yang disesuaikan.
    """
    # Pemetaan nama hari dari Bahasa Inggris ke format Arab-Indonesia
    _GREGORIAN_DAYS_ID = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Ahad",
    }

    def convert_gregorian_to_hijri(self, gregorian_date: date) -> Optional[HijriDate]:
        try:
            # 1. Lakukan konversi menggunakan library
            gregorian_obj = Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
            hijri_obj = gregorian_obj.to_hijri()
            
            # 2. Dapatkan nama hari dalam Bahasa Inggris dari tanggal Masehi
            day_name_en = gregorian_date.strftime('%A')
            
            # 3. Terjemahkan nama hari menggunakan pemetaan kustom kita
            day_name_id = self._GREGORIAN_DAYS_ID.get(day_name_en, "Tidak Diketahui")
            
            # 4. Buat objek entitas HijriDate
            return HijriDate(
                year=hijri_obj.year,
                month=hijri_obj.month,
                day=hijri_obj.day,
                # Ambil nama bulan Arab formal langsung dari library
                month_name=hijri_obj.month_name(),
                # Gunakan nama hari yang sudah disesuaikan
                day_name=day_name_id
            )
        except Exception as e:
            print(f"DEBUG: Error dari library hijri-converter: {e}")
            return None

# Class ini tidak diubah
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

            # Pastikan entitas PrayerSchedule menerima tipe data yang benar
            # Berdasarkan definisi entitas sebelumnya, 'date' harus berupa objek date
            return PrayerSchedule(
                date=target_date,
                fajr=times['fajr'],
                sunrise=times['sunrise'],
                dhuhr=times['dhuhr'],
                asr=times['asr'],
                maghrib=times['maghrib'],
                isha=times['isha']
            )
        except Exception:
            return None