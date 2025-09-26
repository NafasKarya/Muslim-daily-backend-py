# src/presentation/prayer_time/routes.py

from flask import Blueprint, jsonify, Response, request
from dataclasses import asdict

# Import service dari lokasinya yang sudah terpisah
from src.application.prayer_time.services import PrayerTimeService

def create_prayer_time_blueprint(service: PrayerTimeService) -> Blueprint:
    prayer_time_bp = Blueprint('prayer_time_api', __name__)

    @prayer_time_bp.route('/schedule/<int:year>/<int:month>/<int:day>', methods=['GET'])
    def get_prayer_schedule(year: int, month: int, day: int) -> Response:
        try:
            # --- DIUBAH: Default lokasi diubah sesuai lokasi Anda di Cileunyi ---
            lat = float(request.args.get('lat', -6.94))
            lon = float(request.args.get('lon', 107.76))
            
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid latitude or longitude format."}), 400

        schedule_entity = service.get_schedule_for_date(year, month, day, lat, lon)

        if not schedule_entity:
            return jsonify({"error": "Invalid date or could not calculate schedule."}), 400
            
        return jsonify(asdict(schedule_entity)), 200
        
    return prayer_time_bp