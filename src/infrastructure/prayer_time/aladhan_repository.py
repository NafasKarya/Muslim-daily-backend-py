# src/infrastructure/prayer_time/aladhan_repository.py

import requests
from datetime import datetime
from typing import Optional, Dict, List

from src.domain.prayer_time.entities import PrayerSchedule
from src.domain.prayer_time.repositories import PrayerRepository

class AladhanApiRepository(PrayerRepository):
    BASE_URL = "http://api.aladhan.com/v1"

    def get_monthly_schedule(self, year: int, month: int, city: str) -> Optional[List[PrayerSchedule]]:
        """
        Mengambil jadwal sholat bulanan dari Aladhan API berdasarkan nama kota.
        """
        print(f"[REPO-ALADHAN] Mengambil jadwal untuk kota: {city}, Bulan/Tahun: {month}-{year}...")
        try:
            url = f"{self.BASE_URL}/calendarByCity"
            params = {
                # PERBAIKAN: Mengubah "bandung" -> "Bandung" secara otomatis
                "city": city.title(), 
                "country": "Indonesia",
                "month": month,
                "year": year
            }
            
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            
            api_data = response.json()
            
            if api_data.get("code") != 200 or not api_data.get("data"):
                print(f"[REPO-ALADHAN-ERROR] API tidak mengembalikan data yang valid untuk kota '{city.title()}'.")
                return None

            schedules = []
            for day_data in api_data["data"]:
                timings = day_data["timings"]
                gregorian_date_str = day_data["date"]["gregorian"]["date"]
                
                def parse_time(time_str: str) -> datetime.time:
                    clean_time_str = time_str.split(' ')[0]
                    return datetime.strptime(clean_time_str, '%H:%M').time()

                schedule_entry = PrayerSchedule(
                    date=datetime.strptime(gregorian_date_str, '%d-%m-%Y').date(),
                    imsak=parse_time(timings["Imsak"]),
                    fajr=parse_time(timings["Fajr"]),
                    sunrise=parse_time(timings["Sunrise"]),
                    dhuhr=parse_time(timings["Dhuhr"]),
                    asr=parse_time(timings["Asr"]),
                    maghrib=parse_time(timings["Maghrib"]),
                    isha=parse_time(timings["Isha"])
                )
                schedules.append(schedule_entry)
            
            print(f"[REPO-ALADHAN] Berhasil mendapatkan {len(schedules)} jadwal harian.")
            return schedules

        except requests.RequestException as e:
            print(f"[REPO-ALADHAN-ERROR] Gagal menghubungi Aladhan API: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"[REPO-ALADHAN-ERROR] Gagal mem-parsing response dari API: {e}")
            return None

    def get_monthly_schedule_by_coordinates(self, year: int, month: int, latitude: float, longitude: float) -> Optional[List[PrayerSchedule]]:
        """
        Mengambil jadwal sholat bulanan dari Aladhan API berdasarkan koordinat GPS.
        """
        print(f"[REPO-ALADHAN] Mengambil jadwal by koordinat: Lat={latitude}, Lon={longitude}...")
        try:
            url = f"{self.BASE_URL}/calendar"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "month": month,
                "year": year,
                "method": 11 # Metode perhitungan Kemenag RI
            }
            
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            
            api_data = response.json()
            
            if api_data.get("code") != 200 or not api_data.get("data"):
                print("[REPO-ALADHAN-ERROR] API tidak mengembalikan data yang valid untuk koordinat tersebut.")
                return None

            schedules = []
            for day_data in api_data["data"]:
                timings = day_data["timings"]
                gregorian_date_str = day_data["date"]["gregorian"]["date"]
                
                def parse_time(time_str: str) -> datetime.time:
                    clean_time_str = time_str.split(' ')[0]
                    return datetime.strptime(clean_time_str, '%H:%M').time()

                schedule_entry = PrayerSchedule(
                    date=datetime.strptime(gregorian_date_str, '%d-%m-%Y').date(),
                    imsak=parse_time(timings["Imsak"]),
                    fajr=parse_time(timings["Fajr"]),
                    sunrise=parse_time(timings["Sunrise"]),
                    dhuhr=parse_time(timings["Dhuhr"]),
                    asr=parse_time(timings["Asr"]),
                    maghrib=parse_time(timings["Maghrib"]),
                    isha=parse_time(timings["Isha"])
                )
                schedules.append(schedule_entry)
            
            print(f"[REPO-ALADHAN] Berhasil mendapatkan {len(schedules)} jadwal harian by GPS.")
            return schedules

        except requests.RequestException as e:
            print(f"[REPO-ALADHAN-ERROR] Gagal menghubungi Aladhan API: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"[REPO-ALADHAN-ERROR] Gagal mem-parsing response dari API: {e}")
            return None
    
    def get_all_provinces(self) -> Optional[Dict[str, str]]:
        # Metode ini tidak lagi digunakan dengan Aladhan API
        pass

    def get_cities_by_province(self, province_id: str) -> Optional[Dict[str, str]]:
        # Metode ini tidak lagi digunakan dengan Aladhan API
        pass