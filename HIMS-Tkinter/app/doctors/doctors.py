from app.ui.table_module import TableModuleFrame, FieldSpec
from app.database.csv_manager import CSVManager
from app.utils.validators import is_valid_date, normalize_date, is_valid_email


def department_values():
    rows = CSVManager("departments.csv").read()
    return [f"{r['department_id']} — {r['name']}" for r in rows]


class DoctorsFrame(TableModuleFrame):
    store_name = "doctors.csv"
    id_field = "doctor_id"
    id_prefix = "DOC"
    title = "Doctor Management"
    subtitle = "Maintain doctor profiles, specialization, availability, licenses, and status."
    search_fields = ["doctor_id", "first_name", "last_name", "specialization", "department"]
    export_filename = "doctors_export.csv"
    fields = [
        FieldSpec("first_name", "First name", required=True), FieldSpec("last_name", "Last name", required=True),
        FieldSpec("specialization", "Specialization", required=True), FieldSpec("department", "Department", "combo", department_values),
        FieldSpec("phone", "Phone", required=True), FieldSpec("email", "Email"), FieldSpec("license_number", "License number"),
        FieldSpec("availability", "Availability", "combo", ("Available", "Busy", "On Leave", "Unavailable")),
        FieldSpec("joining_date", "Joining date"), FieldSpec("status", "Status", "combo", ("Active", "On Leave", "Inactive"), True, True),
    ]
    columns = ["doctor_id", "name", "specialization", "department", "phone", "availability", "status"]
    column_labels = {"doctor_id":"ID","name":"Doctor","specialization":"Specialization","department":"Department","phone":"Phone","availability":"Availability","status":"Status"}

    def format_column(self, row, column):
        return f"Dr. {row.get('first_name','')} {row.get('last_name','')}".strip() if column == "name" else row.get(column, "")

    def clear_form(self):
        super().clear_form()
        self.vars["status"].set("Active"); self.vars["availability"].set("Available")

    def before_save(self, record):
        if record["joining_date"]:
            if not is_valid_date(record["joining_date"]): return record, "Joining date is invalid."
            record["joining_date"] = normalize_date(record["joining_date"])
        if record["email"] and not is_valid_email(record["email"]): return record, "Enter a valid email address or leave email blank."
        for row in self.store.read():
            if record["license_number"] and row["doctor_id"] != self.editing_id and row.get("license_number", "").casefold() == record["license_number"].casefold():
                return record, "That license number is already registered."
        return record, None
