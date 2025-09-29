from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from src.application.prayer_time.services import PrayerTimeService
from src.domain.prayer_time.entities import PrayerSchedule, CurrentPrayerInfo
from src.dependencies import get_prayer_service

router = APIRouter()


# --- ENDPOINT COUNTDOWN YANG SUDAH DIGABUNGKAN ---
@router.get(
    "/schedule/now", 
    response_model=CurrentPrayerInfo, 
    summary="Dapatkan Info Sholat Saat Ini (by City atau GPS)"
)
def get_current_prayer_info(
    city: Optional[str] = Query(None, description="Nama kota, contoh: 'bandung'"),
    latitude: Optional[float] = Query(None, description="Koordinat Lintang (Latitude)"),
    longitude: Optional[float] = Query(None, description="Koordinat Bujur (Longitude)"),
    service: PrayerTimeService = Depends(get_prayer_service)
):
    """
    Mengambil info sholat saat ini & countdown.
    - **Gunakan parameter `city`** untuk pencarian berdasarkan nama kota.
    - **Gunakan parameter `latitude` dan `longitude`** untuk pencarian berdasarkan GPS.
    - *Jangan gunakan keduanya secara bersamaan.*
    """
    info = None
    if city:
        info = service.get_current_prayer_info(city)
    elif latitude is not None and longitude is not None:
        location_dict = {"latitude": latitude, "longitude": longitude}
        info = service.get_current_prayer_info(location_dict)
    else:
        raise HTTPException(
            status_code=400, 
            detail="Harap berikan parameter 'city' atau 'latitude' dan 'longitude'."
        )

    if not info:
        raise HTTPException(
            status_code=404, 
            detail="Jadwal tidak ditemukan untuk lokasi yang diberikan."
        )
    return info


# --- Endpoint Jadwal Bulanan (Tidak Berubah) ---
@router.get("/schedule/by-coordinates/{year}/{month}", response_model=List[PrayerSchedule], summary="Dapatkan Jadwal Sholat Bulanan by GPS")
def get_monthly_schedule_by_gps(
    year: int, month: int,
    latitude: float = Query(..., description="Koordinat Lintang (Latitude), contoh: -6.9175"),
    longitude: float = Query(..., description="Koordinat Bujur (Longitude), contoh: 107.6191"),
    service: PrayerTimeService = Depends(get_prayer_service)
):
    schedule_list = service.get_monthly_schedule_by_coordinates(year, month, latitude, longitude)
    if not schedule_list:
        raise HTTPException(status_code=404, detail=f"Jadwal tidak ditemukan untuk koordinat Lat: {latitude}, Lon: {longitude}")
    return schedule_list

@router.get("/schedule/{city}/{year}/{month}", response_model=List[PrayerSchedule], summary="Dapatkan Jadwal Sholat Bulanan by City")
def get_monthly_schedule_by_city(
    city: str, year: int, month: int, 
    service: PrayerTimeService = Depends(get_prayer_service)
):
    schedule_list = service.get_monthly_schedule(year, month, city)
    if not schedule_list:
        raise HTTPException(status_code=404, detail=f"Jadwal tidak ditemukan. Pastikan nama kota '{city}' benar dan tanggal valid.")
    return schedule_list