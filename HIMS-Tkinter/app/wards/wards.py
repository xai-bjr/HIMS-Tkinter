import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.database.csv_manager import CSVManager
from app.utils.helpers import clear_tree, sort_tree, export_rows_to_csv
from app.utils.validators import valid_number


class WardsBedsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=22)
        self.controller = controller
        self.ward_store = CSVManager("wards.csv")
        self.bed_store = CSVManager("beds.csv")
        self.ward_editing = None
        self.bed_editing = None
        self.ward_vars = {k: tk.StringVar() for k in ("ward_name", "department", "floor", "capacity", "status", "search")}
        self.bed_vars = {k: tk.StringVar() for k in ("ward", "bed_number", "type", "status", "assigned_patient", "search")}
        self._build()
        self.refresh_refs(); self.clear_ward(); self.clear_bed(); self.refresh_wards(); self.refresh_beds()

    def _build(self):
        self.columnconfigure(0, weight=1); self.rowconfigure(1, weight=1)
        ttk.Label(self, text="Wards & Beds", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text="Manage wards, beds, occupancy, assignment, release, and exports.", style="SubHeader.TLabel").grid(row=0, column=0, sticky="e")
        notebook = ttk.Notebook(self); notebook.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        self.ward_tab = ttk.Frame(notebook, padding=12); self.bed_tab = ttk.Frame(notebook, padding=12)
        notebook.add(self.ward_tab, text="Wards"); notebook.add(self.bed_tab, text="Beds")
        self._build_wards(); self._build_beds()

    def _build_wards(self):
        self.ward_tab.columnconfigure(0, weight=1); self.ward_tab.rowconfigure(2, weight=1)
        form = ttk.Frame(self.ward_tab, style="Card.TFrame", padding=12); form.grid(row=0, column=0, sticky="ew")
        for c in range(5): form.columnconfigure(c, weight=1)
        for i, (label, key) in enumerate([("Ward name", "ward_name"), ("Department", "department"), ("Floor", "floor"), ("Capacity", "capacity"), ("Status", "status")]):
            ttk.Label(form, text=label).grid(row=0, column=i, sticky="w", padx=4)
            if key == "department": widget = ttk.Combobox(form, textvariable=self.ward_vars[key])
            elif key == "status": widget = ttk.Combobox(form, textvariable=self.ward_vars[key], values=("Active", "Inactive"), state="readonly")
            else: widget = ttk.Entry(form, textvariable=self.ward_vars[key])
            widget.grid(row=1, column=i, sticky="ew", padx=4, pady=(3, 7), ipady=2); setattr(self, f"ward_{key}_widget", widget)
        actions = ttk.Frame(form); actions.grid(row=2, column=0, columnspan=5, sticky="ew")
        for label, command, style in [("Add ward", self.save_ward, "Primary.TButton"), ("Update selected", self.save_ward, ""), ("Delete", self.delete_ward, "Danger.TButton"), ("Clear", self.clear_ward, ""), ("Export CSV", self.export_wards, "")]:
            ttk.Button(actions, text=label, command=command, style=style).pack(side="left", padx=3)
        table = ttk.Frame(self.ward_tab, style="Card.TFrame", padding=10); table.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        table.columnconfigure(0, weight=1); table.rowconfigure(1, weight=1)
        bar = ttk.Frame(table); bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(bar, text="Search").pack(side="left"); ttk.Entry(bar, textvariable=self.ward_vars["search"], width=30).pack(side="left", padx=7); ttk.Button(bar, text="Apply", command=self.refresh_wards).pack(side="left")
        cols = ("ward_id", "ward_name", "department", "floor", "capacity", "occupied", "available", "status")
        self.ward_tree = ttk.Treeview(table, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.ward_tree.heading(col, text=col.replace("_", " ").title(), command=lambda c=col: sort_tree(self.ward_tree, c))
            self.ward_tree.column(col, width=125 if col != "ward_name" else 160, anchor="w")
        self.ward_tree.grid(row=1, column=0, sticky="nsew")
        scr = ttk.Scrollbar(table, orient="vertical", command=self.ward_tree.yview); scr.grid(row=1, column=1, sticky="ns"); self.ward_tree.configure(yscrollcommand=scr.set)
        self.ward_tree.bind("<<TreeviewSelect>>", lambda _e: self.load_ward())

    def _build_beds(self):
        self.bed_tab.columnconfigure(0, weight=1); self.bed_tab.rowconfigure(2, weight=1)
        form = ttk.Frame(self.bed_tab, style="Card.TFrame", padding=12); form.grid(row=0, column=0, sticky="ew")
        for c in range(5): form.columnconfigure(c, weight=1)
        for i, (label, key) in enumerate([("Ward", "ward"), ("Bed number", "bed_number"), ("Type", "type"), ("Status", "status"), ("Assigned patient", "assigned_patient")]):
            ttk.Label(form, text=label).grid(row=0, column=i, sticky="w", padx=4)
            if key in ("ward", "status", "assigned_patient"): widget = ttk.Combobox(form, textvariable=self.bed_vars[key])
            else: widget = ttk.Entry(form, textvariable=self.bed_vars[key])
            widget.grid(row=1, column=i, sticky="ew", padx=4, pady=(3, 7), ipady=2); setattr(self, f"bed_{key}_widget", widget)
        self.bed_status_widget["values"] = ("Available", "Occupied", "Maintenance")
        actions = ttk.Frame(form); actions.grid(row=2, column=0, columnspan=5, sticky="ew")
        for label, command, style in [("Add bed", self.save_bed, "Primary.TButton"), ("Update selected", self.save_bed, ""), ("Assign / update", self.assign_bed, "Success.TButton"), ("Release", self.release_bed, ""), ("Delete", self.delete_bed, "Danger.TButton"), ("Clear", self.clear_bed, ""), ("Export CSV", self.export_beds, "")]:
            ttk.Button(actions, text=label, command=command, style=style).pack(side="left", padx=2)
        table = ttk.Frame(self.bed_tab, style="Card.TFrame", padding=10); table.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        table.columnconfigure(0, weight=1); table.rowconfigure(1, weight=1)
        bar = ttk.Frame(table); bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(bar, text="Search").pack(side="left"); ttk.Entry(bar, textvariable=self.bed_vars["search"], width=30).pack(side="left", padx=7); ttk.Button(bar, text="Apply", command=self.refresh_beds).pack(side="left")
        cols = ("bed_id", "ward", "bed_number", "type", "status", "assigned_patient", "updated_at")
        self.bed_tree = ttk.Treeview(table, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.bed_tree.heading(col, text=col.replace("_", " ").title(), command=lambda c=col: sort_tree(self.bed_tree, c))
            self.bed_tree.column(col, width=145 if col not in ("bed_id", "bed_number") else 105, anchor="w")
        self.bed_tree.grid(row=1, column=0, sticky="nsew")
        scr = ttk.Scrollbar(table, orient="vertical", command=self.bed_tree.yview); scr.grid(row=1, column=1, sticky="ns"); self.bed_tree.configure(yscrollcommand=scr.set)
        self.bed_tree.bind("<<TreeviewSelect>>", lambda _e: self.load_bed())

    def refresh_refs(self):
        departments = CSVManager("departments.csv").read()
        wards = self.ward_store.read()
        patients = CSVManager("patients.csv").read()
        self.ward_department_widget["values"] = [f"{d['department_id']} — {d['name']}" for d in departments]
        self.bed_ward_widget["values"] = [f"{w['ward_id']} — {w['ward_name']}" for w in wards]
        self.bed_assigned_patient_widget["values"] = [""] + [f"{p['patient_id']} — {p['first_name']} {p['last_name']}".strip() for p in patients]

    def ward_rows(self):
        query = self.ward_vars["search"].get().strip().casefold(); beds = self.bed_store.read()
        rows = []
        for ward in self.ward_store.read():
            if query and query not in " ".join((ward.get("ward_id", ""), ward.get("ward_name", ""), ward.get("department", ""))).casefold(): continue
            try: capacity = int(ward.get("capacity") or 0)
            except ValueError: capacity = 0
            occupied = sum(b.get("ward") == f"{ward['ward_id']} — {ward['ward_name']}" and b.get("status") == "Occupied" for b in beds)
            rows.append((ward, capacity, occupied, max(capacity - occupied, 0)))
        return rows

    def refresh_wards(self):
        self.refresh_refs(); clear_tree(self.ward_tree)
        for ward, capacity, occupied, available in self.ward_rows():
            self.ward_tree.insert("", "end", iid=ward["ward_id"], values=(ward["ward_id"], ward["ward_name"], ward["department"], ward["floor"], capacity, occupied, available, ward["status"]))

    def refresh_beds(self):
        self.refresh_refs(); clear_tree(self.bed_tree)
        query = self.bed_vars["search"].get().strip().casefold()
        for bed in self.bed_store.read():
            if query and query not in " ".join(bed.values()).casefold(): continue
            self.bed_tree.insert("", "end", iid=bed["bed_id"], values=tuple(bed.get(k, "") for k in ("bed_id", "ward", "bed_number", "type", "status", "assigned_patient", "updated_at")))

    def clear_ward(self):
        self.ward_editing = None
        for key, var in self.ward_vars.items(): var.set("")
        self.ward_vars["status"].set("Active")
        if hasattr(self, "ward_tree"): self.ward_tree.selection_remove(self.ward_tree.selection())

    def load_ward(self):
        selected = self.ward_tree.selection()
        if not selected: return
        row = self.ward_store.find_by_id("ward_id", selected[0])
        if row:
            self.ward_editing = row["ward_id"]
            for key, var in self.ward_vars.items():
                if key in row: var.set(row[key])

    def save_ward(self):
        name = self.ward_vars["ward_name"].get().strip(); capacity = self.ward_vars["capacity"].get().strip()
        if not name or not valid_number(capacity):
            messagebox.showwarning("Invalid ward", "Ward name and a non-negative numeric capacity are required.", parent=self); return
        if any(r["ward_id"] != self.ward_editing and r.get("ward_name", "").casefold() == name.casefold() for r in self.ward_store.read()):
            messagebox.showerror("Duplicate", "A ward with that name already exists.", parent=self); return
        record = {"ward_id": self.ward_editing or self.ward_store.generate_id("WRD", "ward_id"), "ward_name": name, "department": self.ward_vars["department"].get(), "floor": self.ward_vars["floor"].get().strip(), "capacity": capacity, "status": self.ward_vars["status"].get() or "Active", "created_at": datetime.now().isoformat(timespec="seconds")}
        if self.ward_editing:
            ok = self.ward_store.update_by_id("ward_id", self.ward_editing, record)
        else: ok = self.ward_store.append(record)
        if not ok: messagebox.showerror("Storage error", "The ward could not be saved.", parent=self); return
        self.clear_ward(); self.refresh_wards(); self.refresh_beds(); self.controller.refresh_dashboard()

    def delete_ward(self):
        selected = self.ward_tree.selection()
        if not selected: return messagebox.showwarning("Select a ward", "Select a ward first.", parent=self)
        ward_id = selected[0]
        if any(b.get("ward", "").startswith(ward_id + " —") for b in self.bed_store.read()):
            return messagebox.showerror("Ward in use", "Delete or move the beds in this ward first.", parent=self)
        if messagebox.askyesno("Confirm delete", f"Delete ward {ward_id}?", parent=self) and self.ward_store.delete_by_id("ward_id", ward_id):
            self.clear_ward(); self.refresh_wards(); self.refresh_refs(); self.controller.refresh_dashboard()

    def clear_bed(self):
        self.bed_editing = None
        for var in self.bed_vars.values(): var.set("")
        self.bed_vars["status"].set("Available")
        if hasattr(self, "bed_tree"): self.bed_tree.selection_remove(self.bed_tree.selection())

    def load_bed(self):
        selected = self.bed_tree.selection()
        if not selected: return
        row = self.bed_store.find_by_id("bed_id", selected[0])
        if row:
            self.bed_editing = row["bed_id"]
            for key, var in self.bed_vars.items():
                if key in row: var.set(row[key])

    def save_bed(self):
        record = {"bed_id": self.bed_editing or self.bed_store.generate_id("BED", "bed_id"), "ward": self.bed_vars["ward"].get(), "bed_number": self.bed_vars["bed_number"].get().strip(), "type": self.bed_vars["type"].get().strip(), "status": self.bed_vars["status"].get() or "Available", "assigned_patient": self.bed_vars["assigned_patient"].get(), "updated_at": datetime.now().isoformat(timespec="seconds")}
        if not record["ward"] or not record["bed_number"]: return messagebox.showwarning("Missing fields", "Ward and bed number are required.", parent=self)
        if any(b["bed_id"] != record["bed_id"] and b.get("ward") == record["ward"] and b.get("bed_number", "").casefold() == record["bed_number"].casefold() for b in self.bed_store.read()):
            return messagebox.showerror("Duplicate", "That bed number already exists in the selected ward.", parent=self)
        if record["status"] == "Occupied" and not record["assigned_patient"]: return messagebox.showwarning("Assignment required", "An occupied bed must have an assigned patient.", parent=self)
        if record["status"] != "Occupied": record["assigned_patient"] = ""
        ok = self.bed_store.update_by_id("bed_id", self.bed_editing, record) if self.bed_editing else self.bed_store.append(record)
        if not ok: return messagebox.showerror("Storage error", "The bed could not be saved.", parent=self)
        self.clear_bed(); self.refresh_beds(); self.refresh_wards(); self.controller.refresh_dashboard()

    def assign_bed(self):
        selected = self.bed_tree.selection()
        if not selected: return messagebox.showwarning("Select a bed", "Select a bed first.", parent=self)
        bed = self.bed_store.find_by_id("bed_id", selected[0]); patient = self.bed_vars["assigned_patient"].get()
        if not patient: return messagebox.showwarning("Select patient", "Choose a patient to assign.", parent=self)
        if bed.get("status") == "Maintenance": return messagebox.showerror("Unavailable", "A maintenance bed cannot be assigned.", parent=self)
        if any(b["bed_id"] != bed["bed_id"] and b.get("assigned_patient") == patient and b.get("status") == "Occupied" for b in self.bed_store.read()):
            return messagebox.showerror("Already assigned", "That patient already has another occupied bed.", parent=self)
        self.bed_store.update_by_id("bed_id", bed["bed_id"], {"status": "Occupied", "assigned_patient": patient, "updated_at": datetime.now().isoformat(timespec="seconds")})
        pid = patient.split(" —", 1)[0]
        CSVManager("patients.csv").update_by_id("patient_id", pid, {"assigned_bed": f"{bed['bed_id']} — {bed['bed_number']}", "assigned_ward": bed["ward"], "status": "Admitted"})
        self.refresh_beds(); self.refresh_wards(); self.refresh_refs(); self.controller.refresh_dashboard()

    def release_bed(self):
        selected = self.bed_tree.selection()
        if not selected: return messagebox.showwarning("Select a bed", "Select a bed first.", parent=self)
        bed = self.bed_store.find_by_id("bed_id", selected[0])
        if not bed: return
        if not messagebox.askyesno("Release bed", "Release this bed?", parent=self): return
        patient = bed.get("assigned_patient", "")
        self.bed_store.update_by_id("bed_id", bed["bed_id"], {"status": "Available", "assigned_patient": "", "updated_at": datetime.now().isoformat(timespec="seconds")})
        if patient:
            pid = patient.split(" —", 1)[0]
            CSVManager("patients.csv").update_by_id("patient_id", pid, {"assigned_bed": "", "assigned_ward": "", "status": "Active"})
        self.refresh_beds(); self.refresh_wards(); self.refresh_refs(); self.controller.refresh_dashboard()

    def delete_bed(self):
        selected = self.bed_tree.selection()
        if not selected: return messagebox.showwarning("Select a bed", "Select a bed first.", parent=self)
        bed = self.bed_store.find_by_id("bed_id", selected[0])
        if bed and bed.get("status") == "Occupied": return messagebox.showerror("Occupied bed", "Release the bed before deleting it.", parent=self)
        if messagebox.askyesno("Confirm delete", f"Delete bed {selected[0]}?", parent=self) and self.bed_store.delete_by_id("bed_id", selected[0]):
            self.clear_bed(); self.refresh_beds(); self.refresh_wards(); self.controller.refresh_dashboard()

    def export_wards(self): export_rows_to_csv(self, self.ward_store.read(), self.ward_store.headers, "wards_export.csv")
    def export_beds(self): export_rows_to_csv(self, self.bed_store.read(), self.bed_store.headers, "beds_export.csv")
