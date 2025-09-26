# src/presentation/calendar/calendar_routes.py

from flask import Blueprint, jsonify, Response
from dataclasses import asdict
from datetime import date

# --- DIUBAH: Mengoreksi salah ketik 'calender' menjadi 'calendar' ---
from src.application.calendar.services import CalendarService

def create_calendar_blueprint(service: CalendarService) -> Blueprint:
    calendar_bp = Blueprint('calendar_api', __name__)

    @calendar_bp.route('/convert/<int:year>/<int:month>/<int:day>', methods=['GET'])
    def get_hijri_date(year: int, month: int, day: int) -> Response:
        hijri_date_entity = service.get_hijri_date_for_gregorian(year, month, day)
        if not hijri_date_entity:
            return jsonify({"error": "Invalid Gregorian date provided."}), 400
        return jsonify(asdict(hijri_date_entity)), 200

    @calendar_bp.route('/convert/today', methods=['GET'])
    def get_hijri_today() -> Response:
        today = date.today()
        hijri_date_entity = service.get_hijri_date_for_gregorian(
            today.year, today.month, today.day
        )
        if not hijri_date_entity:
            return jsonify({"error": "Failed to convert today's date."}), 500
        return jsonify(asdict(hijri_date_entity)), 200

    return calendar_bp