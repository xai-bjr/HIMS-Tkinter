from pathlib import Path
from datetime import datetime
import csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EXPORTS_DIR = PROJECT_ROOT / "exports"
BACKUPS_DIR = PROJECT_ROOT / "backups"

APP_NAME = "HIMS — Hospital Information Management System"
APP_VERSION = "1.0.0"

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"
BACKGROUND = "#F8FAFC"
SIDEBAR = "#0F172A"
TEXT = "#0F172A"
MUTED = "#64748B"
CARD = "#FFFFFF"
BORDER = "#E2E8F0"

CSV_HEADERS = {
    "accounts.csv": ["id", "username", "password_hash", "full_name", "email", "role", "created_at"],
    "patients.csv": [
        "patient_id", "first_name", "last_name", "date_of_birth", "age", "gender", "blood_group",
        "phone", "email", "address", "emergency_contact", "emergency_phone", "medical_history",
        "allergies", "assigned_doctor", "assigned_department", "assigned_ward", "assigned_bed",
        "admission_date", "discharge_date", "status",
    ],
    "doctors.csv": [
        "doctor_id", "first_name", "last_name", "specialization", "department", "phone", "email",
        "license_number", "availability", "joining_date", "status",
    ],
    "appointments.csv": [
        "appointment_id", "patient", "doctor", "department", "date", "time", "reason", "status", "notes", "created_at",
    ],
    "departments.csv": ["department_id", "name", "description", "status", "created_at"],
    "wards.csv": ["ward_id", "ward_name", "department", "floor", "capacity", "status", "created_at"],
    "beds.csv": ["bed_id", "ward", "bed_number", "type", "status", "assigned_patient", "updated_at"],
    "invoices.csv": [
        "invoice_id", "patient", "invoice_date", "description", "amount", "discount", "tax", "total",
        "payment_method", "payment_status", "notes", "created_at",
    ],
}


def ensure_directories():
    for directory in (DATA_DIR, EXPORTS_DIR, BACKUPS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def initialize_data_files():
    ensure_directories()
    for filename, headers in CSV_HEADERS.items():
        path = DATA_DIR / filename
        if not path.exists() or path.stat().st_size == 0:
            with path.open("w", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=headers).writeheader()


def initialize_app():
    initialize_data_files()


def timestamp_for_filename():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")
