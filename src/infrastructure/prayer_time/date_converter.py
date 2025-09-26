# src/infrastructure/prayer_time/date_converter.py

from datetime import date, datetime, timedelta
from typing import Optional
from PrayTimes import PrayTimes
from timezonefinder import TimezoneFinder
import pytz

from src.domain.prayer_time.entities import PrayerSchedule
from src.domain.prayer_time.repositories import PrayerRepository

class PrayTimesRepository(PrayerRepository):
    """
    Implementasi konkret dari PrayerRepository menggunakan mesin hitung PrayTimes.
    """
    def get_prayer_schedule(
        self, target_date: date, latitude: float, longitude: float
    ) -> Optional[PrayerSchedule]:
        
        try:
            tf = TimezoneFinder()
            timezone_name = tf.timezone_at(lng=longitude, lat=latitude)

            if timezone_name:
                tz = pytz.timezone(timezone_name)
                dt_object = datetime.combine(target_date, datetime.min.time())
                offset = tz.utcoffset(dt_object)
                timezone_offset = offset.total_seconds() / 3600.0
            else:
                timezone_offset = longitude / 15.0
            
            pt = PrayTimes()
            
            # Mengatur sudut Kemenag
            pt.fajrAngle = 20
            pt.ishaAngle = 18
            
            # 1. Hitung waktu dasar dari library
            times = pt.getTimes(
                (target_date.year, target_date.month, target_date.day),
                (latitude, longitude),
                timezone_offset
            )

            # --- DIUBAH: Menggunakan nilai ihtiyati umum (+2 menit) untuk semua lokasi ---
            offsets = {'fajr': 2, 'dhuhr': 2, 'asr': 2, 'maghrib': 2, 'isha': 2}

            # Lakukan koreksi manual untuk setiap waktu yang perlu disesuaikan
            for time_name, offset_minutes in offsets.items():
                if time_name in times: # Pastikan waktu ada sebelum dikoreksi
                    t = datetime.strptime(times[time_name], '%H:%M')
                    t += timedelta(minutes=offset_minutes)
                    times[time_name] = t.strftime('%H:%M')

            # Return hasil yang sudah dikoreksi
            return PrayerSchedule(
                date=target_date.strftime('%Y-%m-%d'),
                fajr=times['fajr'],
                sunrise=times['sunrise'],
                dhuhr=times['dhuhr'],
                asr=times['asr'],
                maghrib=times['maghrib'],
                isha=times['isha']
            )
        except Exception as e:
            print(f"DEBUG: Error dari library PrayTimes: {e}")
            return None