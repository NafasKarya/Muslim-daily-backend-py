# src/application/calendar/services.py

from datetime import date
from typing import Optional

# --- Path import baru, spesifik untuk kalender ---
from src.domain.calendar.entities import HijriDate
from src.domain.calendar.repositories import HijriDateRepository

class CalendarService:
    """
    Application service yang mengatur use case terkait kalender Hijriah.
    """
    
    def __init__(self, repository: HijriDateRepository):
        self._repository = repository
        
    def get_hijri_date_for_gregorian(self, year: int, month: int, day: int) -> Optional[HijriDate]:
        """
        Use case: Mendapatkan tanggal Hijriah dari tanggal Masehi.
        """
        try:
            gregorian_date = date(year, month, day)
        except ValueError:
            # Menangani input tanggal yang tidak valid, contoh: 30 Februari
            return None
            
        return self._repository.convert_gregorian_to_hijri(gregorian_date)