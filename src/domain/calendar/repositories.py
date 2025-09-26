# src/domain/calendar/repositories.py

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

# --- Path import baru, spesifik untuk entitas kalender ---
from src.domain.calendar.entities import HijriDate

class HijriDateRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk konversi tanggal.
    Lapisan domain bergantung pada abstraksi ini, bukan pada implementasi konkret.
    """
    
    @abstractmethod
    def convert_gregorian_to_hijri(self, gregorian_date: date) -> Optional[HijriDate]:
        """
        Mengonversi tanggal Masehi ke tanggal Hijriah.
        """
        pass