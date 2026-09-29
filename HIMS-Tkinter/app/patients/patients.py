from app.ui.table_module import TableModuleFrame, FieldSpec
from app.database.csv_manager import CSVManager
from app.utils.validators import is_valid_date, normalize_date, calculate_age, is_valid_email
from tkinter import messagebox


def doctor_values():
    rows = CSVManager("doctors.csv").read()
    return [f"{r['doctor_id']} — Dr. {r['first_name']} {r['last_name']}" for r in rows]


def department_values():
    rows = CSVManager("departments.csv").read()
    return [f"{r['department_id']} — {r['name']}" for r in rows]


def ward_values():
    rows = CSVManager("wards.csv").read()
    return [f"{r['ward_id']} — {r['ward_name']}" for r in rows]


def bed_values():
    rows = CSVManager("beds.csv").read()
    return [f"{r['bed_id']} — {r['bed_number']} ({r['status']})" for r in rows]


class PatientsFrame(TableModuleFrame):
    store_name = "patients.csv"
    id_field = "patient_id"
    id_prefix = "PAT"
    title = "Patient Management"
    subtitle = "Register, update, search, filter, and export patient records."
    search_fields = ["patient_id", "first_name", "last_name", "phone", "blood_group"]
    filters = [("status", "Status", ("Active", "Admitted", "Discharged", "Inactive"))]
    export_filename = "patients_export.csv"
    fields = [
        FieldSpec("first_name", "First name", required=True), FieldSpec("last_name", "Last name", required=True),
        FieldSpec("date_of_birth", "Date of birth (YYYY-MM-DD)"), FieldSpec("gender", "Gender", "combo", ("Male", "Female", "Other"), True, True),
        FieldSpec("blood_group", "Blood group", "combo", ("", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")),
        FieldSpec("phone", "Phone", required=True), FieldSpec("email", "Email"), FieldSpec("address", "Address", "text"),
        FieldSpec("emergency_contact", "Emergency contact"), FieldSpec("emergency_phone", "Emergency phone"),
        FieldSpec("medical_history", "Medical history", "text"), FieldSpec("allergies", "Allergies", "text"),
        FieldSpec("assigned_doctor", "Assigned doctor", "combo", doctor_values),
        FieldSpec("assigned_department", "Assigned department", "combo", department_values),
        FieldSpec("assigned_ward", "Assigned ward", "combo", ward_values),
        FieldSpec("assigned_bed", "Assigned bed", "combo", bed_values),
        FieldSpec("admission_date", "Admission date"), FieldSpec("discharge_date", "Discharge date"),
        FieldSpec("status", "Status", "combo", ("Active", "Admitted", "Discharged", "Inactive"), True, True),
    ]
    columns = ["patient_id", "name", "date_of_birth", "age", "gender", "phone", "blood_group", "assigned_doctor", "status"]
    column_labels = {"patient_id": "ID", "name": "Patient", "date_of_birth": "DOB", "age": "Age", "gender": "Gender", "phone": "Phone", "blood_group": "Blood", "assigned_doctor": "Doctor", "status": "Status"}

    def format_column(self, row, column):
        if column == "name": return f"{row.get('first_name','')} {row.get('last_name','')}".strip()
        return row.get(column, "")

    def clear_form(self):
        super().clear_form()
        if "status" in self.vars: self.vars["status"].set("Active")

    def refresh_references(self):
        super().refresh_references()

    def before_save(self, record):
        for key in ("date_of_birth", "admission_date", "discharge_date"):
            if record[key]:
                if not is_valid_date(record[key]): return record, f"{key.replace('_', ' ').title()} is not a valid date."
                record[key] = normalize_date(record[key])
        if record["date_of_birth"]:
            record["age"] = calculate_age(record["date_of_birth"])
        else:
            record["age"] = ""
        if record["admission_date"] and record["discharge_date"] and record["discharge_date"] < record["admission_date"]:
            return record, "Discharge date cannot be before admission date."
        if record["email"] and not is_valid_email(record["email"]):
            return record, "Enter a valid email address or leave the email blank."
        # A bed marked occupied should be represented in the bed module; this form does not change bed status.
        return record, None

    def before_delete(self, record):
        if record.get("assigned_bed"):
            messagebox.showerror("Patient has a bed", "Release the patient's bed before deleting this patient.", parent=self)
            return False
        return True
