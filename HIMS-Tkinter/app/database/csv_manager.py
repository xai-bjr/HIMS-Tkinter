import csv
from typing import Dict, List, Optional

from app.config import DATA_DIR, CSV_HEADERS


class CSVManager:
    """Reusable CSV CRUD helper for all local hospital data."""

    def __init__(self, filename: str):
        if filename not in CSV_HEADERS:
            raise ValueError(f"Unknown CSV file: {filename}")
        self.filename = filename
        self.headers = CSV_HEADERS[filename]
        self.path = DATA_DIR / filename
        self.ensure_file()

    def ensure_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists() or self.path.stat().st_size == 0:
            self.write([])

    def read(self) -> List[Dict[str, str]]:
        self.ensure_file()
        try:
            with self.path.open("r", newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    return []
                rows = []
                for raw in reader:
                    row = {h: (raw.get(h) or "").strip() for h in self.headers}
                    if any(row.values()):
                        rows.append(row)
                return rows
        except (OSError, UnicodeError, csv.Error):
            return []

    def write(self, rows: List[Dict[str, str]]) -> bool:
        try:
            with self.path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=self.headers, extrasaction="ignore")
                writer.writeheader()
                for row in rows:
                    writer.writerow({h: str(row.get(h, "")) for h in self.headers})
            return True
        except OSError:
            return False

    def append(self, row: Dict[str, str]) -> bool:
        rows = self.read()
        rows.append(row)
        return self.write(rows)

    def update_by_id(self, id_field: str, record_id: str, updates: Dict[str, str]) -> bool:
        rows = self.read()
        for row in rows:
            if row.get(id_field) == record_id:
                for key, value in updates.items():
                    if key in self.headers:
                        row[key] = str(value)
                return self.write(rows)
        return False

    def delete_by_id(self, id_field: str, record_id: str) -> bool:
        rows = self.read()
        filtered = [row for row in rows if row.get(id_field) != record_id]
        if len(filtered) == len(rows):
            return False
        return self.write(filtered)

    def find_by_id(self, id_field: str, record_id: str) -> Optional[Dict[str, str]]:
        return next((row for row in self.read() if row.get(id_field) == record_id), None)

    def exists(self, field: str, value: str, exclude_id: Optional[str] = None) -> bool:
        target = value.casefold()
        for row in self.read():
            if row.get(field, "").casefold() == target:
                if exclude_id is None or row.get(field) != exclude_id:
                    return True
        return False

    def generate_id(self, prefix: str, id_field: str) -> str:
        largest = 0
        for row in self.read():
            value = row.get(id_field, "")
            if value.startswith(prefix + "-"):
                try:
                    largest = max(largest, int(value.split("-", 1)[1]))
                except (ValueError, IndexError):
                    pass
        return f"{prefix}-{largest + 1:05d}"
