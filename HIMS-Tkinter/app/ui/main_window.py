import tkinter as tk
from tkinter import messagebox

from app.config import BACKGROUND
from app.ui.sidebar import Sidebar
from app.ui.dashboard import DashboardFrame
from app.ui.settings import SettingsFrame


class MainWindow(tk.Frame):
    def __init__(self, parent, app, account):
        super().__init__(parent, bg=BACKGROUND)
        self.app = app
        self.account = account
        self.current_view = None
        self.current_view_name = "dashboard"
        self.sidebar = Sidebar(self, self, account)
        self.sidebar.pack(side="left", fill="y")
        self.content = tk.Frame(self, bg=BACKGROUND)
        self.content.pack(side="right", fill="both", expand=True)
        self.show_view("dashboard")

    def show_view(self, view_name):
        if self.current_view is not None:
            self.current_view.destroy()
        builders = {
            "dashboard": lambda: DashboardFrame(self.content, self, self.account),
            "patients": self._patients, "doctors": self._doctors,
            "appointments": self._appointments, "departments": self._departments,
            "wards": self._wards, "payments": self._payments, "backup": self._backup,
            "settings": lambda: SettingsFrame(self.content, self, self.account),
        }
        self.current_view = builders.get(view_name, builders["dashboard"])()
        self.current_view.pack(fill="both", expand=True)
        self.current_view_name = view_name

    def _patients(self):
        from app.patients.patients import PatientsFrame
        return PatientsFrame(self.content, self)

    def _doctors(self):
        from app.doctors.doctors import DoctorsFrame
        return DoctorsFrame(self.content, self)

    def _appointments(self):
        from app.appointments.appointments import AppointmentsFrame
        return AppointmentsFrame(self.content, self)

    def _departments(self):
        from app.departments.departments import DepartmentsFrame
        return DepartmentsFrame(self.content, self)

    def _wards(self):
        from app.wards.wards import WardsBedsFrame
        return WardsBedsFrame(self.content, self)

    def _payments(self):
        from app.payments.payments import PaymentsFrame
        return PaymentsFrame(self.content, self)

    def _backup(self):
        from app.backup.backup import BackupFrame
        return BackupFrame(self.content, self)

    def refresh_dashboard(self):
        if self.current_view_name == "dashboard" and hasattr(self.current_view, "refresh"):
            self.current_view.refresh()

    def logout(self):
        if messagebox.askyesno("Logout", "Log out of the current session?", parent=self):
            self.app.logout()

    def exit_application(self):
        if messagebox.askyesno("Exit", "Exit HIMS?", parent=self):
            self.app.root.destroy()
