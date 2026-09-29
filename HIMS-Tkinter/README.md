# HIMS-Tkinter — Hospital Information Management System

> Offline desktop Hospital Information Management System built with Python and Tkinter.

## Important medical-data warning

This repository is an **educational/local prototype**. It has **not** been validated for production clinical use, regulated healthcare deployment, or real patient-data handling. Real-world deployment requires appropriate security, privacy/compliance review, access control, auditing, backup/restore testing, software testing, clinical validation, and applicable legal/regulatory review.

**Do not commit real patient or account data to GitHub.** Use synthetic/sample data for demonstrations.

## Features

- Local login and sign-up
- First-run administrator setup with no hard-coded password
- PBKDF2-HMAC-SHA256 salted password hashes
- Dashboard summary cards
- Patient management: add, edit, delete, search, filter, export
- Doctor management: add, edit, delete, search, export
- Appointment management with date/doctor/status filters and basic active double-booking prevention
- Department management
- Ward and bed management with occupancy information, assignment, release, search, and export
- Payments/invoices with automatic totals
- Search/filtering across major modules
- CSV export from every major management module
- ZIP backup and restore
- Logout without closing the whole application
- Professional ttk-based interface with sidebar, cards, Treeviews, consistent spacing, and responsive resizing
- Standard-library only; no Django, web server, cloud database, or external API is required

## Requirements

- Windows 10/11
- Python 3.10+ recommended
- Tkinter/ttk (normally included with the Windows Python installer)

## Windows PowerShell setup

```powershell
cd HIMS-Tkinter

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks environment activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run

```powershell
python main.py
```

On the first launch the application automatically creates `data/`, `exports/`, and `backups/`, plus the required CSV files. If no account exists, the first-run setup screen asks you to create the administrator account.

## Project structure

```text
HIMS-Tkinter/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── app/
│   ├── app.py
│   ├── config.py
│   ├── database/
│   │   └── csv_manager.py
│   ├── auth/
│   │   ├── login.py
│   │   ├── signup.py
│   │   └── security.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── sidebar.py
│   │   ├── dashboard.py
│   │   ├── settings.py
│   │   ├── styles.py
│   │   └── table_module.py
│   ├── patients/
│   │   └── patients.py
│   ├── doctors/
│   │   └── doctors.py
│   ├── appointments/
│   │   └── appointments.py
│   ├── departments/
│   │   └── departments.py
│   ├── wards/
│   │   └── wards.py
│   ├── payments/
│   │   └── payments.py
│   ├── backup/
│   │   └── backup.py
│   └── utils/
│       ├── validators.py
│       └── helpers.py
├── data/
├── exports/
└── backups/
```

## Local CSV data

The application stores UTF-8 CSV files under `data/`:

```text
data/accounts.csv
data/patients.csv
data/doctors.csv
data/appointments.csv
data/departments.csv
data/wards.csv
data/beds.csv
data/invoices.csv
```

`app/database/csv_manager.py` is the shared persistence layer. It creates missing/empty files, reads and writes records, appends, updates, deletes, checks duplicates, and generates IDs.

## Password security

Passwords are never saved as plaintext. The application uses salted PBKDF2-HMAC-SHA256 password hashes with a unique random salt per password and constant-time comparison during login.

No default administrator password is hard-coded. The first administrator is created through the first-run setup screen.

## Account creation

1. Start HIMS.
2. On first run, create the administrator account.
3. After an account exists, use **Create account** on the login screen for additional local users.
4. Select an appropriate role such as Staff, Doctor, Receptionist, or Manager.

## Modules

### Patients

Patient fields include identity, DOB/age, gender, blood group, contact details, emergency contact, medical history, allergies, doctor/department/ward/bed assignments, admission/discharge dates, and status.

Search covers patient ID, name, phone, and blood group. Status filtering is available. DOB and admission/discharge dates are validated and age is calculated automatically.

### Doctors

Doctor fields include identity, specialization, department, phone/email, license number, availability, joining date, and status. License numbers are checked for duplicates.

### Appointments

Appointment fields include patient, doctor, department, date, time, reason, status, and notes. The interface supports searching plus doctor, date, and status filtering. Active duplicate doctor/date/time appointments are rejected.

### Departments

Departments are user-defined. The application does not hard-code a fixed list, and it prevents deleting departments that are still assigned to doctors or wards.

### Wards & beds

Wards include ward name, department, floor, capacity, and status. Beds include ward, bed number, type, status, assigned patient, and updated time.

The ward table shows capacity, occupied beds, and available beds. Beds can be assigned and released. Patients linked to an assigned bed are updated automatically.

### Payments / invoices

Invoice totals are calculated as:

```text
total = amount - discount + tax
```

Dashboard revenue is the sum of invoice totals whose status is `Paid`.

### Backup / restore

The backup screen creates ZIP files such as:

```text
HIMS_Backup_2026-09-29_120000.zip
```

The archive contains:

```text
data/
    accounts.csv
    patients.csv
    doctors.csv
    appointments.csv
    departments.csv
    wards.csv
    beds.csv
    invoices.csv
```

Restore replaces the local CSV files. Always create a fresh backup before restoring. Restore only accepts recognized HIMS CSV members and checks ZIP paths to prevent path traversal.

## CSV export

Every major management module has an **Export CSV** button and asks where to save the exported file. Existing files are not overwritten silently.

## Error handling

Normal user mistakes and storage problems use Tkinter message boxes. CSV files are initialized automatically if missing/empty, and malformed input is rejected without exposing raw Python tracebacks to ordinary users.

## GitHub privacy

Do not commit:

- real patient records
- real accounts/password hashes
- generated exports
- backup ZIP files
- `.venv/`
- `.env`

The included `.gitignore` ignores local CSV data and generated exports/backups while preserving the directory placeholders.

## Testing / verification checklist

Run the application with `python main.py` and verify:

1. First-run setup creates an administrator.
2. Login succeeds with the correct password.
3. A wrong password is rejected.
4. `data/accounts.csv` contains a `password_hash` value instead of a plaintext password.
5. A second local account can be created.
6. A patient can be added, selected, edited, searched, filtered, exported, and deleted.
7. A doctor can be added, edited, searched, exported, and deleted.
8. An appointment can be added and the same active doctor/date/time appointment is rejected.
9. Appointments can be filtered by doctor, date, and status.
10. A department can be created, used by a doctor or ward, and protected from deletion while still in use.
11. A ward can be created and its occupancy is displayed.
12. Beds can be created, assigned to patients, released, filtered, and exported.
13. An invoice total changes when amount, discount, or tax changes.
14. A `Paid` invoice changes dashboard revenue.
15. Every major module exports a valid CSV.
16. Backup creates a ZIP and restore replaces local CSV data after confirmation.
17. Logout returns to the login screen without closing the application.
18. Exit closes the application.

For a syntax check:

```powershell
python -m compileall .
```

## Development

The architecture intentionally uses a reusable `TableModuleFrame` so future modules can add a field definition, columns, and validation hooks instead of duplicating all CRUD code.

Recommended future improvements include audit/event logs, granular role permissions, receipt/report generation, CSV import validation, automated tests, encrypted local storage, stronger backup versioning, configurable hospital branding, detailed clinical records, accessibility work, and Windows packaging.

## License

Choose a license suitable for your project. For example, MIT:

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
