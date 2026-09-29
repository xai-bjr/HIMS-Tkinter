from datetime import date
import tkinter as tk
from tkinter import ttk

from app.database.csv_manager import CSVManager
from app.utils.helpers import clear_tree


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller, account):
        super().__init__(parent, padding=24)
        self.controller = controller
        self.account = account
        self._build()
        self.refresh()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        ttk.Label(self, text="Dashboard", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text=f"Welcome back, {self.account.get('full_name', self.account.get('username', 'User'))}. Today is {date.today().strftime('%d %b %Y')}.", style="SubHeader.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 15))
        cards = ttk.Frame(self)
        cards.grid(row=2, column=0, sticky="ew")
        for i in range(5): cards.columnconfigure(i, weight=1)
        titles = ["Total Patients", "Total Doctors", "Today's Appointments", "Pending Appointments", "Departments", "Wards", "Occupied Beds", "Available Beds", "Total Invoices", "Total Revenue"]
        self.card_values = {}
        for index, title in enumerate(titles):
            r, c = divmod(index, 5)
            card = ttk.Frame(cards, style="Card.TFrame", padding=15)
            card.grid(row=r, column=c, sticky="ew", padx=4, pady=4)
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            value = ttk.Label(card, text="0", style="CardValue.TLabel")
            value.pack(anchor="w", pady=(6, 0))
            self.card_values[title] = value
        recent = ttk.Frame(self, style="Card.TFrame", padding=14)
        recent.grid(row=3, column=0, sticky="nsew", pady=(14, 0))
        recent.columnconfigure(0, weight=1); recent.rowconfigure(1, weight=1)
        ttk.Label(recent, text="Today's appointments", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 7))
        columns = ("time", "patient", "doctor", "status")
        self.tree = ttk.Treeview(recent, columns=columns, show="headings")
        for key, label in [("time", "Time"), ("patient", "Patient"), ("doctor", "Doctor"), ("status", "Status")]:
            self.tree.heading(key, text=label); self.tree.column(key, width=180, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(recent, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns"); self.tree.configure(yscrollcommand=scrollbar.set)

    def refresh(self):
        patients = CSVManager("patients.csv").read()
        doctors = CSVManager("doctors.csv").read()
        appointments = CSVManager("appointments.csv").read()
        departments = CSVManager("departments.csv").read()
        wards = CSVManager("wards.csv").read()
        beds = CSVManager("beds.csv").read()
        invoices = CSVManager("invoices.csv").read()
        today = date.today().isoformat()
        today_appointments = [a for a in appointments if a.get("date") == today]
        pending = [a for a in appointments if a.get("status") in ("Scheduled", "Pending")]
        revenue = sum(float(i.get("total") or 0) for i in invoices if i.get("payment_status") == "Paid" and (i.get("total") or "").replace('.', '', 1).isdigit())
        metrics = {
            "Total Patients": len(patients), "Total Doctors": len(doctors), "Today's Appointments": len(today_appointments),
            "Pending Appointments": len(pending), "Departments": len(departments), "Wards": len(wards),
            "Occupied Beds": sum(b.get("status") == "Occupied" for b in beds),
            "Available Beds": sum(b.get("status") == "Available" for b in beds), "Total Invoices": len(invoices),
            "Total Revenue": f"{revenue:,.2f}",
        }
        for title, value in metrics.items(): self.card_values[title].configure(text=str(value))
        clear_tree(self.tree)
        for row in sorted(today_appointments, key=lambda x: x.get("time", ""))[:100]:
            self.tree.insert("", "end", values=(row.get("time", ""), row.get("patient", ""), row.get("doctor", ""), row.get("status", "")))
