import tkinter as tk
from tkinter import ttk, messagebox

from app.auth.security import verify_password
from app.database.csv_manager import CSVManager
from app.config import APP_NAME, PRIMARY, MUTED


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=35)
        self.app = app
        self.show_password = tk.BooleanVar(value=False)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        card = ttk.Frame(self, style="Auth.TFrame", padding=36)
        card.grid(row=0, column=0, sticky="nsew", padx=110, pady=80)
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text="HIMS", font=("Segoe UI", 30, "bold"), foreground=PRIMARY).grid(row=0, column=0, pady=(0, 3))
        ttk.Label(card, text=APP_NAME).grid(row=1, column=0, pady=(0, 5))
        ttk.Label(card, text="Sign in to continue", font=("Segoe UI", 15, "bold")).grid(row=2, column=0, pady=(0, 18))
        ttk.Label(card, text="Username").grid(row=3, column=0, sticky="w", pady=(0, 6))
        ttk.Entry(card, textvariable=self.username).grid(row=4, column=0, sticky="ew", ipady=4, pady=(0, 13))
        ttk.Label(card, text="Password").grid(row=5, column=0, sticky="w", pady=(0, 6))
        self.password_entry = ttk.Entry(card, textvariable=self.password, show="•")
        self.password_entry.grid(row=6, column=0, sticky="ew", ipady=4, pady=(0, 6))
        self.password_entry.bind("<Return>", lambda _event: self.login())
        ttk.Checkbutton(card, text="Show password", variable=self.show_password, command=self._toggle).grid(row=7, column=0, sticky="w", pady=(0, 14))
        ttk.Button(card, text="Login", style="Primary.TButton", command=self.login).grid(row=8, column=0, sticky="ew", ipady=5, pady=(0, 8))
        ttk.Button(card, text="Create account", command=self.app.show_signup).grid(row=9, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(card, text="Exit", command=self.app.root.destroy).grid(row=10, column=0, sticky="ew")
        ttk.Label(card, text="Offline local application", foreground=MUTED).grid(row=11, column=0, pady=(16, 0))

    def _toggle(self):
        self.password_entry.configure(show="" if self.show_password.get() else "•")

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showwarning("Missing information", "Enter your username and password.", parent=self)
            return
        account = next((r for r in CSVManager("accounts.csv").read() if r.get("username", "").casefold() == username.casefold()), None)
        if not account or not verify_password(password, account.get("password_hash", "")):
            messagebox.showerror("Login failed", "Invalid username or password.", parent=self)
            return
        self.app.login_success(account)
