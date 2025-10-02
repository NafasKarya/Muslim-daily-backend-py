from fastapi import FastAPI

# --- Import service dan repository ---
from src.application.calendar.services import CalendarService
from src.application.prayer_time.services import PrayerTimeService
from src.application.al_quran.services import AlQuranService
from src.application.dua.services import DuaService

from src.infrastructure.calendar.date_converter import HijriConverterRepository
from src.infrastructure.prayer_time.aladhan_repository import AladhanApiRepository
from src.infrastructure.al_quran.equran_repository import EQuranRepository
from src.infrastructure.dua.json_dua_repository import JSONDuaRepository

# --- Import untuk Story (fantasi/kitab/legend/mitos) ---
from src.application.story.services import StoryService
from src.infrastructure.story.json_story_repository import JSONStoryRepository

# --- Import routes dan dependencies ---
from src.presentation.calendar import calendar_routes
from src.presentation.prayer_time import prayer_time_routes
from src.presentation.al_quran import alquran_routes
from src.presentation.dua import dua_routes
from src.presentation.story import story_repository_routes

from src.dependencies import (
    get_calendar_service,
    get_prayer_service,
    get_quran_service,
    get_dua_service,
    get_story_service,
)

# --- Composition Root (Inisialisasi Semua Service dan Repository) ---
# Kalender
hijri_repository = HijriConverterRepository()
calendar_service = CalendarService(repository=hijri_repository)

# Jadwal Sholat
prayer_repository = AladhanApiRepository()
prayer_service = PrayerTimeService(repository=prayer_repository)

# Al-Quran
quran_repository = EQuranRepository()
quran_service = AlQuranService(repository=quran_repository)

# Dua
dua_repository = JSONDuaRepository()
dua_service = DuaService(repository=dua_repository)

# Story
story_repository = JSONStoryRepository()
story_service = StoryService(repository=story_repository)

# --- Buat instance FastAPI ---
app = FastAPI(
    title="Muslim Daily API",
    description="API untuk Jadwal Sholat, Kalender Hijriah, Al-Quran, Dua, dan Story Fantasi Kitab"
)

# --- Dependency Overrides ---
def get_calendar_service_override():
    return calendar_service

def get_prayer_service_override():
    return prayer_service

def get_quran_service_override():
    return quran_service

def get_dua_service_override():
    return dua_service

def get_story_service_override():
    return story_service

app.dependency_overrides[get_calendar_service] = get_calendar_service_override
app.dependency_overrides[get_prayer_service] = get_prayer_service_override
app.dependency_overrides[get_quran_service] = get_quran_service_override
app.dependency_overrides[get_dua_service] = get_dua_service_override
app.dependency_overrides[get_story_service] = get_story_service_override

# --- Memasukkan semua router ---
app.include_router(calendar_routes.router, prefix="/api", tags=["Kalender Hijriah"])
app.include_router(prayer_time_routes.router, prefix="/api", tags=["Jadwal Sholat"])
app.include_router(alquran_routes.router, prefix="/api/quran", tags=["Al-Quran"])
app.include_router(dua_routes.router, prefix="/api/dua", tags=["Dua"])
app.include_router(story_repository_routes.router, prefix="/api/story", tags=["Story"])

# --- Endpoint utama ---
@app.get("/")
def index():
    return {"message": "API is running.", "api_docs": "/docs"}
