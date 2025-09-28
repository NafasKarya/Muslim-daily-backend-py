# src/presentation/prayer_time/prayer_time_routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from src.application.prayer_time.services import PrayerTimeService
from src.domain.prayer_time.entities import PrayerSchedule
from src.dependencies import get_prayer_service

router = APIRouter()

# --- Endpoint Provinsi & Kota yang Dinonaktifkan ---
@router.get("/provinces", summary="[TIDAK DIGUNAKAN] Dapatkan Semua Provinsi")
def get_provinces():
    raise HTTPException(status_code=404, detail="Endpoint ini tidak lagi didukung. Silakan gunakan endpoint /schedule atau /schedule/by-coordinates.")

@router.get("/provinces/{province_id}/cities", summary="[TIDAK DIGUNAKAN] Dapatkan Kota per Provinsi")
def get_cities(province_id: str):
    raise HTTPException(status_code=404, detail="Endpoint ini tidak lagi didukung. Silakan gunakan endpoint /schedule atau /schedule/by-coordinates.")


# --- URUTAN DIPERBAIKI ---
# Endpoint yang LEBIH SPESIFIK ("by-coordinates") diletakkan PERTAMA.

@router.get("/schedule/by-coordinates/{year}/{month}", response_model=List[PrayerSchedule], summary="Dapatkan Jadwal Sholat Bulanan by GPS")
def get_monthly_schedule_by_gps(
    year: int,
    month: int,
    latitude: float = Query(..., description="Koordinat Lintang (Latitude), contoh: -6.9175"),
    longitude: float = Query(..., description="Koordinat Bujur (Longitude), contoh: 107.6191"),
    service: PrayerTimeService = Depends(get_prayer_service)
):
    """
    Mengambil jadwal sholat bulanan lengkap berdasarkan **koordinat GPS**.
    Contoh request: `GET /api/schedule/by-coordinates/2025/10?latitude=-6.9175&longitude=107.6191`
    """
    schedule_list = service.get_monthly_schedule_by_coordinates(year, month, latitude, longitude)
    
    if not schedule_list:
        raise HTTPException(
            status_code=404, 
            detail=f"Jadwal tidak ditemukan untuk koordinat Lat: {latitude}, Lon: {longitude}"
        )
    
    return schedule_list


# Endpoint yang LEBIH UMUM ("{city}") diletakkan KEDUA.

@router.get("/schedule/{city}/{year}/{month}", response_model=List[PrayerSchedule], summary="Dapatkan Jadwal Sholat Bulanan by City")
def get_monthly_schedule_by_city(
    city: str,
    year: int, 
    month: int, 
    service: PrayerTimeService = Depends(get_prayer_service)
):
    """
    Mengambil jadwal sholat bulanan lengkap (termasuk Imsak) berdasarkan **nama kota**.
    Contoh request: `GET /api/schedule/bandung/2025/9`
    """
    schedule_list = service.get_monthly_schedule(year, month, city)
    
    if not schedule_list:
        raise HTTPException(
            status_code=404, 
            detail=f"Jadwal tidak ditemukan. Pastikan nama kota '{city}' benar dan tanggal valid."
        )
    
    return schedule_list