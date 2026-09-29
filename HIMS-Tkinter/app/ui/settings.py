from tkinter import ttk
from app.config import APP_NAME, APP_VERSION, DATA_DIR, EXPORTS_DIR, BACKUPS_DIR


class SettingsFrame(ttk.Frame):
    def __init__(self, parent, controller, account):
        super().__init__(parent, padding=24)
        ttk.Label(self, text="Settings", style="Header.TLabel").pack(anchor="w")
        ttk.Label(self, text="Application information and local storage locations.", style="SubHeader.TLabel").pack(anchor="w", pady=(3, 18))
        card = ttk.Frame(self, style="Card.TFrame", padding=18); card.pack(fill="x")
        values = [
            ("Application", APP_NAME), ("Version", APP_VERSION), ("Signed-in user", account.get("username", "")),
            ("Role", account.get("role", "")), ("Data folder", str(DATA_DIR)), ("Exports folder", str(EXPORTS_DIR)),
            ("Backups folder", str(BACKUPS_DIR)), ("Storage", "Local UTF-8 CSV files"), ("Network dependency", "None"),
        ]
        for row, (label, value) in enumerate(values):
            ttk.Label(card, text=label, style="CardTitle.TLabel").grid(row=row, column=0, sticky="w", padx=(0, 22), pady=6)
            ttk.Label(card, text=value).grid(row=row, column=1, sticky="w", pady=6)
        note = ttk.Frame(self, style="Card.TFrame", padding=18); note.pack(fill="x", pady=(16, 0))
        ttk.Label(note, text="Repository privacy", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(note, text="Keep real patient and account CSV files out of GitHub. Use synthetic sample data for demonstrations.", wraplength=850).pack(anchor="w", pady=(6, 0))
