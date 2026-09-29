import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

from app.database.csv_manager import CSVManager
from app.utils.helpers import clear_tree, sort_tree, export_rows_to_csv


@dataclass
class FieldSpec:
    key: str
    label: str
    kind: str = "entry"          # entry, combo, text
    values: object = ()          # tuple/list or callable returning values
    required: bool = False
    readonly: bool = False


class TableModuleFrame(ttk.Frame):
    """Generic search/filter + form + Treeview CRUD module."""

    store_name = ""
    id_field = ""
    id_prefix = "REC"
    title = "Records"
    subtitle = "Manage local records."
    fields = []
    columns = []
    column_labels = {}
    search_fields = []
    filters = []               # (field, label, values)
    filter_entries = []        # (field, label) text filters
    export_filename = "export.csv"

    def __init__(self, parent, controller):
        super().__init__(parent, padding=22)
        self.controller = controller
        self.store = CSVManager(self.store_name)
        self.editing_id = None
        self.vars = {field.key: tk.StringVar() for field in self.fields}
        self.search_var = tk.StringVar()
        self.filter_vars = {field: tk.StringVar(value="All") for field, _label, _values in self.filters}
        self.filter_entry_vars = {}
        self.text_widgets = {}
        self.widgets = {}
        self._build()
        self.refresh_references()
        self.clear_form()
        self.refresh_tree()

    def _build(self):
        self.columnconfigure(0, weight=1); self.rowconfigure(3, weight=1)
        ttk.Label(self, text=self.title, style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text=self.subtitle, style="SubHeader.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 10))
        form = ttk.Frame(self, style="Card.TFrame", padding=14)
        form.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        for col in range(4): form.columnconfigure(col, weight=1)
        for index, field in enumerate(self.fields):
            r, c = divmod(index, 4)
            ttk.Label(form, text=field.label).grid(row=r*2, column=c, sticky="w", padx=5, pady=(2, 2))
            if field.kind == "combo":
                widget = ttk.Combobox(form, textvariable=self.vars[field.key], values=self._field_values(field), state="readonly" if field.readonly else "normal")
                self.widgets[field.key] = widget
            elif field.kind == "text":
                widget = tk.Text(form, height=2, wrap="word")
                self.text_widgets[field.key] = widget
            else:
                widget = ttk.Entry(form, textvariable=self.vars[field.key], state="readonly" if field.readonly else "normal")
            widget.grid(row=r*2+1, column=c, sticky="ew", padx=5, pady=(0, 7), ipady=2)
        action_row = (len(self.fields) + 3) // 4 * 2
        actions = ttk.Frame(form); actions.grid(row=action_row, column=0, columnspan=4, sticky="ew", pady=(4, 0))
        ttk.Button(actions, text="Add record", style="Primary.TButton", command=self.save).pack(side="left", padx=3)
        ttk.Button(actions, text="Update selected", command=self.save).pack(side="left", padx=3)
        ttk.Button(actions, text="Delete", style="Danger.TButton", command=self.delete).pack(side="left", padx=3)
        ttk.Button(actions, text="Clear form", command=self.clear_form).pack(side="left", padx=3)
        ttk.Button(actions, text="Export CSV", command=self.export_csv).pack(side="left", padx=3)
        table = ttk.Frame(self, style="Card.TFrame", padding=12)
        table.grid(row=3, column=0, sticky="nsew")
        table.columnconfigure(0, weight=1); table.rowconfigure(1, weight=1)
        bar = ttk.Frame(table); bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(bar, text="Search").pack(side="left")
        ttk.Entry(bar, textvariable=self.search_var, width=30).pack(side="left", padx=7)
        for field, label, values in self.filters:
            ttk.Label(bar, text=label).pack(side="left", padx=(8, 4))
            vals = values() if callable(values) else values
            ttk.Combobox(bar, textvariable=self.filter_vars[field], values=("All",) + tuple(vals), state="readonly", width=15).pack(side="left")
        for field, label in self.filter_entries:
            self.filter_entry_vars.setdefault(field, tk.StringVar())
            ttk.Label(bar, text=label).pack(side="left", padx=(8, 4))
            ttk.Entry(bar, textvariable=self.filter_entry_vars[field], width=12).pack(side="left")
        ttk.Button(bar, text="Apply", command=self.refresh_tree).pack(side="left", padx=6)
        ttk.Button(bar, text="Clear", command=self.clear_filters).pack(side="left")
        self.tree = ttk.Treeview(table, columns=self.columns, show="headings", selectmode="browse")
        for column in self.columns:
            self.tree.heading(column, text=self.column_labels.get(column, column.title()), command=lambda c=column: sort_tree(self.tree, c))
            self.tree.column(column, width=145 if column != self.id_field else 100, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns"); self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self.load_selected())

    def _field_values(self, field):
        return field.values() if callable(field.values) else field.values

    def refresh_references(self):
        for field in self.fields:
            if field.kind == "combo" and field.key in self.widgets:
                self.widgets[field.key]["values"] = self._field_values(field)

    def get_rows(self):
        rows = self.store.read()
        query = self.search_var.get().strip().casefold()
        if query:
            rows = [r for r in rows if query in " ".join(r.get(k, "") for k in self.search_fields).casefold()]
        for field, _label, _values in self.filters:
            selected = self.filter_vars[field].get()
            if selected != "All":
                rows = [r for r in rows if r.get(field, "") == selected]
        for field, _label in self.filter_entries:
            selected = self.filter_entry_vars[field].get().strip().casefold()
            if selected:
                rows = [r for r in rows if selected in r.get(field, "").casefold()]
        return rows

    def refresh_tree(self):
        self.refresh_references()
        clear_tree(self.tree)
        for row in self.get_rows():
            values = [self.format_column(row, col) for col in self.columns]
            self.tree.insert("", "end", iid=row.get(self.id_field, ""), values=values)

    def format_column(self, row, column):
        return row.get(column, "")

    def clear_filters(self):
        self.search_var.set("")
        for variable in self.filter_vars.values(): variable.set("All")
        for variable in self.filter_entry_vars.values(): variable.set("")
        self.refresh_tree()

    def collect_form(self):
        record = {}
        for field in self.fields:
            if field.kind == "text":
                record[field.key] = self.text_widgets[field.key].get("1.0", "end").strip()
            else:
                record[field.key] = self.vars[field.key].get().strip()
        return record

    def set_form(self, row):
        for field in self.fields:
            if field.kind == "text":
                self.text_widgets[field.key].delete("1.0", "end")
                self.text_widgets[field.key].insert("1.0", row.get(field.key, ""))
            else:
                self.vars[field.key].set(row.get(field.key, ""))

    def before_save(self, record):
        return record, None

    def after_save(self):
        pass

    def before_delete(self, record):
        return True

    def save(self):
        record = self.collect_form()
        missing = [f.label for f in self.fields if f.required and not record.get(f.key, "").strip()]
        if missing:
            messagebox.showwarning("Missing fields", "Required fields:\n• " + "\n• ".join(missing), parent=self)
            return
        record, error = self.before_save(record)
        if error:
            messagebox.showerror("Could not save", error, parent=self); return
        now = datetime.now().isoformat(timespec="seconds")
        record[self.id_field] = self.editing_id or self.store.generate_id(self.id_prefix, self.id_field)
        if "created_at" in self.store.headers and not record.get("created_at"):
            existing = self.store.find_by_id(self.id_field, self.editing_id) if self.editing_id else None
            record["created_at"] = existing.get("created_at", now) if existing else now
        if "updated_at" in self.store.headers:
            record["updated_at"] = now
        ok = self.store.update_by_id(self.id_field, self.editing_id, record) if self.editing_id else self.store.append(record)
        if not ok:
            messagebox.showerror("Storage error", "The record could not be saved.", parent=self); return
        messagebox.showinfo("Saved", "Record saved successfully.", parent=self)
        self.clear_form(); self.refresh_tree(); self.after_save()
        self.controller.refresh_dashboard()

    def load_selected(self):
        selected = self.tree.selection()
        if not selected: return
        row = self.store.find_by_id(self.id_field, selected[0])
        if not row: return
        self.editing_id = row[self.id_field]
        self.set_form(row)

    def clear_form(self):
        self.editing_id = None
        for var in self.vars.values(): var.set("")
        for widget in self.text_widgets.values(): widget.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection()) if hasattr(self, "tree") else None

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select a record", "Select a record first.", parent=self); return
        record_id = selected[0]
        record = self.store.find_by_id(self.id_field, record_id)
        if not record or not self.before_delete(record): return
        if not messagebox.askyesno("Confirm delete", f"Delete record {record_id}?", parent=self): return
        if self.store.delete_by_id(self.id_field, record_id):
            self.clear_form(); self.refresh_tree(); self.after_save(); self.controller.refresh_dashboard()
        else:
            messagebox.showerror("Delete failed", "The record no longer exists.", parent=self)

    def export_csv(self):
        export_rows_to_csv(self, self.get_rows(), self.store.headers, self.export_filename)
