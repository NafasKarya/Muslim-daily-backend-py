# src/domain/prayer_time/entities.py

from dataclasses import dataclass, replace
from datetime import date, time, timedelta # Tambahkan timedelta
from typing import Optional

@dataclass(frozen=True)
class PrayerSchedule:
    """
    Mewakili jadwal salat harian.
    'frozen=True' membuatnya tidak bisa diubah (immutable).
    """
    date: date
    imsak: time
    fajr: time
    sunrise: time
    dhuhr: time
    asr: time
    maghrib: time
    isha: time
    
    # --- KOLOM BARU DITAMBAHKAN DI SINI ---
    # Bersifat opsional, jadi tidak akan mengganggu kode yang sudah ada.
    tahajjud: Optional[str] = None
    dhuha: Optional[str] = None

# --- ENTITAS BARU DITAMBAHKAN DI BAWAH INI ---
@dataclass(frozen=True)
class CurrentPrayerInfo:
    """
    Mewakili informasi sholat saat ini dan countdown ke sholat berikutnya.
    """
    current_prayer_time: time
    current_prayer_name: str
    next_prayer_time: time
    next_prayer_name: str
    countdown_to_next: str
    date: date