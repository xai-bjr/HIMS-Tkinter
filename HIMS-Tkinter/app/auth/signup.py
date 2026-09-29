import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.auth.security import hash_password
from app.database.csv_manager import CSVManager
from app.config import APP_NAME, PRIMARY, MUTED

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_signup(full_name, username, email, password, confirm):
    errors = []
    if not full_name.strip(): errors.append("Full name is required.")
    if len(username.strip()) < 3: errors.append("Username must be at least 3 characters.")
    if not EMAIL_RE.match(email.strip()): errors.append("Enter a valid email address.")
    if len(password) < 8: errors.append("Password must be at least 8 characters.")
    if password != confirm: errors.append("Passwords do not match.")
    return errors


class AccountForm(ttk.Frame):
    def __init__(self, parent, app, first_run=False):
        super().__init__(parent, padding=32)
        self.app = app
        self.first_run = first_run
        self.show_password = tk.BooleanVar(value=False)
        self.vars = {k: tk.StringVar() for k in ("full_name", "username", "email", "password", "confirm", "role")}
        self.vars["role"].set("Administrator" if first_run else "Staff")
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        card = ttk.Frame(self, style="Auth.TFrame", padding=34)
        card.grid(row=0, column=0, sticky="nsew", padx=70 if not self.first_run else 40, pady=35)
        card.columnconfigure(1, weight=1)
        title = "First-run administrator setup" if self.first_run else "Create local account"
        ttk.Label(card, text=title, font=("Segoe UI", 22, "bold"), foreground=PRIMARY).grid(
            row=0, column=0, columnspan=2, pady=(0, 6)
        )
        ttk.Label(card, text=APP_NAME, foreground=MUTED).grid(row=1, column=0, columnspan=2, pady=(0, 16))
        if self.first_run:
            ttk.Label(card, text="No default password is stored in the application.", foreground=MUTED).grid(
                row=2, column=0, columnspan=2, pady=(0, 10)
            )
        fields = [("Full name", "full_name"), ("Username", "username"), ("Email", "email"),
                  ("Password", "password"), ("Confirm password", "confirm")]
        if not self.first_run:
            fields.append(("Role", "role"))
        for row, (label, key) in enumerate(fields, start=3):
            ttk.Label(card, text=label).grid(row=row, column=0, sticky="w", padx=(0, 16), pady=7)
            if key == "role":
                widget = ttk.Combobox(card, textvariable=self.vars[key], values=("Staff", "Doctor", "Receptionist", "Manager"), state="readonly")
            else:
                widget = ttk.Entry(card, textvariable=self.vars[key], show="•" if key in ("password", "confirm") else "")
            widget.grid(row=row, column=1, sticky="ew", ipady=3, pady=7)
            if key == "password": self.password_entry = widget
            if key == "confirm": self.confirm_entry = widget
        check_row = 3 + len(fields)
        ttk.Checkbutton(card, text="Show passwords", variable=self.show_password, command=self._toggle).grid(
            row=check_row, column=1, sticky="w", pady=(3, 12)
        )
        button_row = check_row + 1
        ttk.Button(card, text="Create account", style="Primary.TButton", command=self.create_account).grid(
            row=button_row, column=0, columnspan=2, sticky="ew", ipady=5
        )
        if not self.first_run:
            ttk.Button(card, text="Back to login", command=self.app.show_login).grid(
                row=button_row + 1, column=0, columnspan=2, sticky="ew", pady=(8, 0)
            )

    def _toggle(self):
        show = "" if self.show_password.get() else "•"
        self.password_entry.configure(show=show)
        self.confirm_entry.configure(show=show)

    def create_account(self):
        values = {k: v.get().strip() for k, v in self.vars.items()}
        errors = validate_signup(values["full_name"], values["username"], values["email"], values["password"], values["confirm"])
        store = CSVManager("accounts.csv")
        if store.exists("username", values["username"]):
            errors.append("That username is already in use.")
        if errors:
            messagebox.showerror("Could not create account", "\n".join(errors), parent=self)
            return
        record = {
            "id": store.generate_id("USR", "id"),
            "username": values["username"],
            "password_hash": hash_password(values["password"]),
            "full_name": values["full_name"],
            "email": values["email"],
            "role": "Administrator" if self.first_run else values["role"],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        if not store.append(record):
            messagebox.showerror("Storage error", "The account could not be saved.", parent=self)
            return
        messagebox.showinfo("Account created", "Account created successfully. Please sign in.", parent=self)
        self.app.show_login()


class SignupFrame(AccountForm):
    def __init__(self, parent, app):
        super().__init__(parent, app, first_run=False)


class FirstRunSetupFrame(AccountForm):
    def __init__(self, parent, app):
        super().__init__(parent, app, first_run=True)
