# src/domain/calendar/entities.py

from dataclasses import dataclass

@dataclass(frozen=True)
class HijriDate:
    """
    Mewakili tanggal Hijriah. Ini adalah entitas domain murni.
    'frozen=True' membuatnya tidak bisa diubah (immutable),
    yang merupakan praktik yang baik untuk entitas.
    """
    year: int
    month: int
    day: int
    month_name: str
    day_name: str