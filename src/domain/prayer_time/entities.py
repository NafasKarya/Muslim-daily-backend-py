# src/domain/prayer_time/entities.py

from dataclasses import dataclass

@dataclass(frozen=True)
class PrayerSchedule:
    """
    Mewakili jadwal sholat untuk satu hari penuh. 
    Ini adalah entitas domain murni.
    """
    date: str
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str