from datetime import datetime
from app.ui.table_module import TableModuleFrame, FieldSpec
from app.database.csv_manager import CSVManager
from app.utils.validators import is_valid_date, normalize_date


def patient_values():
    rows = CSVManager("patients.csv").read()
    return [f"{r['patient_id']} — {r['first_name']} {r['last_name']}".strip() for r in rows]


def doctor_values():
    rows = CSVManager("doctors.csv").read()
    return [f"{r['doctor_id']} — Dr. {r['first_name']} {r['last_name']}".strip() for r in rows]


def department_values():
    rows = CSVManager("departments.csv").read()
    return [f"{r['department_id']} — {r['name']}" for r in rows]


class AppointmentsFrame(TableModuleFrame):
    store_name = "appointments.csv"
    id_field = "appointment_id"
    id_prefix = "APT"
    title = "Appointment Management"
    subtitle = "Schedule visits, prevent obvious double-booking, and filter by date and status."
    search_fields = ["appointment_id", "patient", "doctor", "department", "date", "status"]
    filters = [("status", "Status", ("Scheduled", "Completed", "Cancelled", "Pending")), ("doctor", "Doctor", doctor_values)]
    filter_entries = [("date", "Date")]
    export_filename = "appointments_export.csv"
    fields = [
        FieldSpec("patient", "Patient", "combo", patient_values, True), FieldSpec("doctor", "Doctor", "combo", doctor_values, True),
        FieldSpec("department", "Department", "combo", department_values), FieldSpec("date", "Date (YYYY-MM-DD)", required=True),
        FieldSpec("time", "Time (HH:MM)", required=True), FieldSpec("reason", "Reason"),
        FieldSpec("status", "Status", "combo", ("Scheduled", "Completed", "Cancelled", "Pending"), True, True),
        FieldSpec("notes", "Notes", "text"),
    ]
    columns = ["appointment_id", "patient", "doctor", "department", "date", "time", "status", "reason"]
    column_labels = {"appointment_id":"ID","patient":"Patient","doctor":"Doctor","department":"Department","date":"Date","time":"Time","status":"Status","reason":"Reason"}

    def clear_form(self):
        super().clear_form(); self.vars["status"].set("Scheduled")

    def before_save(self, record):
        if not is_valid_date(record["date"]): return record, "Appointment date must use YYYY-MM-DD or DD/MM/YYYY."
        record["date"] = normalize_date(record["date"])
        try:
            datetime.strptime(record["time"], "%H:%M")
        except ValueError:
            return record, "Time must use HH:MM, for example 14:30."
        for row in self.store.read():
            if row["appointment_id"] == self.editing_id: continue
            if row.get("doctor") == record["doctor"] and row.get("date") == record["date"] and row.get("time") == record["time"] and row.get("status") not in ("Cancelled", "Completed"):
                return record, "That doctor already has an active appointment at this date and time."
        return record, None
