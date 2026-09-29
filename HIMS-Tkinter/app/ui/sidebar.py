from tkinter import ttk


class Sidebar(ttk.Frame):
    def __init__(self, parent, controller, account):
        super().__init__(parent, style="Sidebar.TFrame", width=228)
        self.controller = controller
        self.account = account
        self.pack_propagate(False)
        self._build()

    def _build(self):
        ttk.Label(self, text="HIMS", style="Sidebar.TLabel", font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=18, pady=(24, 0))
        ttk.Label(self, text="Hospital Information\nManagement System", style="Sidebar.TLabel", font=("Segoe UI", 8)).pack(anchor="w", padx=19, pady=(0, 22))
        for label, view in [
            ("Dashboard", "dashboard"), ("Patients", "patients"), ("Doctors", "doctors"),
            ("Appointments", "appointments"), ("Departments", "departments"), ("Wards & Beds", "wards"),
            ("Payments / Invoices", "payments"), ("Backup / Restore", "backup"), ("Settings", "settings"),
        ]:
            ttk.Button(self, text=label, style="Sidebar.TButton", command=lambda v=view: self.controller.show_view(v)).pack(fill="x", padx=4, pady=1)
        ttk.Frame(self, style="Sidebar.TFrame").pack(fill="both", expand=True)
        ttk.Label(self, text=f"{self.account.get('full_name', self.account.get('username', 'User'))}\n{self.account.get('role', 'Staff')}", style="Sidebar.TLabel").pack(anchor="w", padx=18, pady=(0, 10))
        ttk.Button(self, text="Logout", style="Sidebar.TButton", command=self.controller.logout).pack(fill="x", padx=4, pady=1)
        ttk.Button(self, text="Exit application", style="Sidebar.TButton", command=self.controller.exit_application).pack(fill="x", padx=4, pady=(1, 12))
