# app.py

from flask import Flask

# Import service
from src.application.calendar.services import CalendarService
from src.application.prayer_time.services import PrayerTimeService

# Import repository dari lokasi yang benar
from src.infrastructure.calendar.date_converter import HijriConverterRepository
from src.infrastructure.prayer_time.date_converter import PrayTimesRepository

# --- DIUBAH: Path import disesuaikan dengan struktur folder Anda ---
from src.presentation.calendar.calendar_routes import create_calendar_blueprint
from src.presentation.prayer_time.prayer_time_routes import create_prayer_time_blueprint

# 1. Create a Flask app instance
app = Flask(__name__)

# 2. Composition Root: Inisialisasi semua dependency
# Konteks Kalender Hijriah
hijri_repository = HijriConverterRepository()
calendar_service = CalendarService(repository=hijri_repository)

# Konteks Jadwal Sholat
prayer_repository = PrayTimesRepository()
prayer_service = PrayerTimeService(repository=prayer_repository)

# 3. Buat dan daftarkan SETIAP blueprint secara terpisah
# Membuat blueprint kalender
calendar_api_bp = create_calendar_blueprint(calendar_service)
app.register_blueprint(calendar_api_bp, url_prefix='/api')

# Membuat blueprint jadwal sholat
prayer_time_api_bp = create_prayer_time_blueprint(prayer_service)
app.register_blueprint(prayer_time_api_bp, url_prefix='/api')


@app.route("/")
def index():
    return (
        "API is running. <br>"
        "Use <b>/api/convert/YYYY/MM/DD</b> for Hijri conversion. <br>"
        "Use <b>/api/schedule/YYYY/MM/DD?lat=LAT&lon=LON</b> for prayer schedule."
    )

# 4. Run the app
if __name__ == '__main__':
    app.run(debug=True)