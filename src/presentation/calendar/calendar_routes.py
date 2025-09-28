# src/presentation/calendar/routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date, timedelta

from src.application.calendar.services import CalendarService
from src.domain.calendar.entities import HijriDate
from src.dependencies import get_calendar_service

router = APIRouter()

@router.get("/hijri-date/{year}/{month}/{day}", response_model=HijriDate, summary="Konversi Tanggal Masehi ke Hijriah")
def get_hijri_date(
    year: int, 
    month: int, 
    day: int,
    adj: int = Query(0, description="Penyesuaian hari. Gunakan -1 untuk sinkronisasi dengan tanggal pemerintah (Rukyat)."),
    service: CalendarService = Depends(get_calendar_service)
):
    """
    Mengonversi tanggal Masehi ke tanggal Hijriah.
    
    Tambahkan parameter `?adj=-1` untuk menyesuaikan dengan tanggal resmi pemerintah.
    """
    try:
        gregorian_date = date(year, month, day)
        
        # Terapkan penyesuaian jika ada (adj tidak sama dengan 0)
        adjusted_date = gregorian_date + timedelta(days=adj)
        
        hijri_date_entity = service.get_hijri_date_for_gregorian(
            adjusted_date.year, adjusted_date.month, adjusted_date.day
        )
        
        if not hijri_date_entity:
            raise HTTPException(status_code=400, detail="Invalid Gregorian date provided.")
        return hijri_date_entity

    except ValueError:
        raise HTTPException(status_code=400, detail="Tanggal Masehi tidak valid.")


@router.get("/hijri-date/today", response_model=HijriDate, summary="Konversi Tanggal Hari Ini ke Hijriah")
def get_hijri_today(
    adj: int = Query(0, description="Penyesuaian hari. Gunakan -1 untuk sinkronisasi dengan tanggal pemerintah (Rukyat)."),
    service: CalendarService = Depends(get_calendar_service)
):
    """
    Mengonversi tanggal hari ini ke tanggal Hijriah.
    
    Tambahkan parameter `?adj=-1` untuk menyesuaikan dengan tanggal resmi pemerintah.
    """
    today = date.today()
    
    # Terapkan penyesuaian jika ada
    adjusted_date = today + timedelta(days=adj)

    hijri_date_entity = service.get_hijri_date_for_gregorian(
        adjusted_date.year, adjusted_date.month, adjusted_date.day
    )
    
    if not hijri_date_entity:
        raise HTTPException(status_code=500, detail="Failed to convert today's date.")
    return hijri_date_entity