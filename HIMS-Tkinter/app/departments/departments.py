from datetime import datetime
from app.ui.table_module import TableModuleFrame, FieldSpec
from app.database.csv_manager import CSVManager
from tkinter import messagebox


class DepartmentsFrame(TableModuleFrame):
    store_name = "departments.csv"
    id_field = "department_id"
    id_prefix = "DEP"
    title = "Department Management"
    subtitle = "Create and maintain departments without hard-coded choices."
    search_fields = ["department_id", "name", "description"]
    export_filename = "departments_export.csv"
    fields = [
        FieldSpec("name", "Department name", required=True), FieldSpec("description", "Description"),
        FieldSpec("status", "Status", "combo", ("Active", "Inactive"), True, True),
    ]
    columns = ["department_id", "name", "description", "status", "created_at"]
    column_labels = {"department_id":"ID","name":"Department","description":"Description","status":"Status","created_at":"Created"}

    def clear_form(self):
        super().clear_form(); self.vars["status"].set("Active")

    def before_save(self, record):
        for row in self.store.read():
            if row["department_id"] != self.editing_id and row.get("name", "").casefold() == record["name"].casefold():
                return record, "A department with that name already exists."
        record.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
        return record, None

    def before_delete(self, record):
        dep_id = record["department_id"]
        if any(r.get("department", "").startswith(dep_id + " —") for r in CSVManager("doctors.csv").read()):
            messagebox.showerror("Department in use", "Reassign doctors from this department before deleting it.", parent=self); return False
        if any(r.get("department", "").startswith(dep_id + " —") for r in CSVManager("wards.csv").read()):
            messagebox.showerror("Department in use", "Reassign wards from this department before deleting it.", parent=self); return False
        return True
