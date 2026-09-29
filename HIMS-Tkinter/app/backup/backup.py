import shutil
import tempfile
import zipfile
from pathlib import Path
from tkinter import ttk, filedialog, messagebox

from app.config import DATA_DIR, EXPORTS_DIR, BACKUPS_DIR, CSV_HEADERS, timestamp_for_filename


class BackupFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=24)
        self.controller = controller
        self._build()

    def _build(self):
        ttk.Label(self, text="Backup / Restore", style="Header.TLabel").pack(anchor="w")
        ttk.Label(self, text="Create portable ZIP snapshots of local CSV data or restore a previous backup.", style="SubHeader.TLabel").pack(anchor="w", pady=(3, 16))
        card = ttk.Frame(self, style="Card.TFrame", padding=20); card.pack(fill="x")
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text="Backup hospital data", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(card, text="The ZIP contains the local CSV data inside a data/ folder.").grid(row=1, column=0, sticky="w", pady=(5, 12))
        ttk.Button(card, text="Backup Hospital Data", style="Primary.TButton", command=self.create_backup).grid(row=2, column=0, sticky="w")
        ttk.Separator(card, orient="horizontal").grid(row=3, column=0, sticky="ew", pady=20)
        ttk.Label(card, text="Restore from backup", font=("Segoe UI", 15, "bold")).grid(row=4, column=0, sticky="w")
        ttk.Label(card, text="Restore replaces current CSV files. Create a fresh backup before using restore.").grid(row=5, column=0, sticky="w", pady=(5, 12))
        ttk.Button(card, text="Restore Backup", command=self.restore_backup).grid(row=6, column=0, sticky="w")
        ttk.Separator(card, orient="horizontal").grid(row=7, column=0, sticky="ew", pady=20)
        ttk.Label(card, text=f"Data: {DATA_DIR}\nExports: {EXPORTS_DIR}\nBackups: {BACKUPS_DIR}", justify="left").grid(row=8, column=0, sticky="w")

    def create_backup(self):
        path = filedialog.asksaveasfilename(parent=self, title="Save HIMS backup", defaultextension=".zip", filetypes=[("ZIP files", "*.zip")], initialdir=str(BACKUPS_DIR), initialfile=f"HIMS_Backup_{timestamp_for_filename()}.zip")
        if not path: return
        target = Path(path)
        if target.exists() and not messagebox.askyesno("Confirm overwrite", f"{target.name} already exists. Overwrite it?", parent=self): return
        try:
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
                for filename in CSV_HEADERS:
                    source = DATA_DIR / filename
                    if source.exists(): archive.write(source, f"data/{filename}")
            messagebox.showinfo("Backup complete", f"Backup created:\n{target}", parent=self)
        except OSError as exc:
            messagebox.showerror("Backup failed", f"Could not create the backup:\n{exc}", parent=self)

    def restore_backup(self):
        path = filedialog.askopenfilename(parent=self, title="Select HIMS backup", filetypes=[("ZIP files", "*.zip")], initialdir=str(BACKUPS_DIR))
        if not path: return
        if not messagebox.askyesno("Restore backup", "Restore will replace current CSV data. Continue?", parent=self): return
        required = {f"data/{filename}" for filename in CSV_HEADERS}
        try:
            with zipfile.ZipFile(path, "r") as archive, tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp).resolve()
                for member in archive.infolist():
                    if member.filename not in required: continue
                    destination = (tmp_path / member.filename).resolve()
                    if tmp_path not in destination.parents: continue
                    archive.extract(member, tmp_path)
                source = tmp_path / "data"
                if not source.exists(): raise ValueError("The ZIP does not contain a data/ folder.")
                DATA_DIR.mkdir(parents=True, exist_ok=True)
                restored = 0
                for filename in CSV_HEADERS:
                    src = source / filename
                    if src.exists(): shutil.copy2(src, DATA_DIR / filename); restored += 1
                if restored == 0: raise ValueError("No recognized HIMS CSV files were found in the backup.")
            messagebox.showinfo("Restore complete", "Hospital CSV data has been restored. Reopen modules to refresh them.", parent=self)
            self.controller.show_view("dashboard")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            messagebox.showerror("Restore failed", f"The backup could not be restored:\n{exc}", parent=self)
