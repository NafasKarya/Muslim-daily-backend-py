# main.py

from fastapi import FastAPI

# --- Import service dan repository ---
from src.application.calendar.services import CalendarService
from src.application.prayer_time.services import PrayerTimeService
from src.application.al_quran.services import AlQuranService

from src.infrastructure.calendar.date_converter import HijriConverterRepository
from src.infrastructure.prayer_time.aladhan_repository import AladhanApiRepository
# --- PERBAIKI IMPORT DI SINI ---
from src.infrastructure.al_quran.equran_repository import EQuranRepository


# --- Import routes dan dependencies ---
from src.presentation.calendar import calendar_routes
from src.presentation.prayer_time import prayer_time_routes
from src.presentation.al_quran import alquran_routes

from src.dependencies import get_calendar_service, get_prayer_service
from src.dependencies import get_quran_service


# --- Composition Root (Inisialisasi Semua Service dan Repository) ---
# Kalender
hijri_repository = HijriConverterRepository()
calendar_service = CalendarService(repository=hijri_repository)

# Jadwal Sholat
prayer_repository = AladhanApiRepository()
prayer_service = PrayerTimeService(repository=prayer_repository)

# Al-Quran
# --- PERBAIKI INISIALISASI DI SINI ---
quran_repository = EQuranRepository() # <-- Gunakan nama kelas yang baru
quran_service = AlQuranService(repository=quran_repository)


# --- Buat instance FastAPI ---
app = FastAPI(
    title="Muslim Daily API",
    description="API untuk Jadwal Sholat, Kalender Hijriah, dan Al-Quran"
)

# --- Dependency Overrides ---
def get_calendar_service_override():
    return calendar_service

def get_prayer_service_override():
    return prayer_service

def get_quran_service_override():
    return quran_service

app.dependency_overrides[get_calendar_service] = get_calendar_service_override
app.dependency_overrides[get_prayer_service] = get_prayer_service_override
app.dependency_overrides[get_quran_service] = get_quran_service_override


# --- Memasukkan semua router ---
app.include_router(calendar_routes.router, prefix="/api", tags=["Kalender Hijriah"])
app.include_router(prayer_time_routes.router, prefix="/api", tags=["Jadwal Sholat"])
app.include_router(alquran_routes.router, prefix="/api/quran", tags=["Al-Quran"])


# --- Endpoint utama ---
@app.get("/")
def index():
    return {"message": "API is running.", "api_docs": "/docs"}