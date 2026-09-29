# HIMS-Tkinter

An offline **Hospital Information Management System (HIMS)** desktop application built with **Python and Tkinter**.

The system is designed as a local, lightweight hospital-management application for learning, demonstration, and small offline environments. It does not require a web server, cloud database, or external API.

> **Important:** This project is an educational/local prototype and is **not intended for production clinical use**. Do not use it to store real patient information or other sensitive medical data without appropriate security, compliance, validation, and professional review.

---

## Features

* 🔐 Secure local user authentication
* 👤 Patient management
* 👨‍⚕️ Doctor management
* 📅 Appointment management
* 🏥 Department management
* 🛏️ Ward and bed management
* 💳 Payment and invoice management
* 🔎 Search and filtering
* 📊 Dashboard
* 📄 CSV data storage
* 📤 CSV exports
* 💾 Local backup and export functionality
* 🚪 Login and logout
* 🎨 Professional Tkinter desktop interface
* 🔒 Password hashing using PBKDF2-HMAC-SHA256
* 📁 Automatic creation of required local data directories

---

## Technology Stack

| Technology       | Purpose                          |
| ---------------- | -------------------------------- |
| Python 3         | Application programming language |
| Tkinter / ttk    | Desktop graphical user interface |
| CSV              | Local data storage               |
| pathlib          | File and directory management    |
| hashlib          | Password hashing                 |
| datetime         | Dates and timestamps             |
| shutil / zipfile | Backup and archive functionality |

The project is intentionally designed without Django, Flask, a web server, cloud database, or external API dependency.

---

## Project Structure

```text
HIMS-Tkinter/
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── signup.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── csv_manager.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── sidebar.py
│   │   ├── dashboard.py
│   │   ├── settings.py
│   │   ├── styles.py
│   │   └── table_module.py
│   │
│   ├── patients/
│   │   ├── __init__.py
│   │   └── patients.py
│   │
│   ├── doctors/
│   │   ├── __init__.py
│   │   └── doctors.py
│   │
│   ├── appointments/
│   │   ├── __init__.py
│   │   └── appointments.py
│   │
│   ├── departments/
│   │   ├── __init__.py
│   │   └── departments.py
│   │
│   ├── wards/
│   │   ├── __init__.py
│   │   └── wards.py
│   │
│   ├── payments/
│   │   ├── __init__.py
│   │   └── payments.py
│   │
│   ├── backup/
│   │   ├── __init__.py
│   │   └── backup.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
│
├── data/
│   └── .gitkeep
│
├── exports/
│   └── .gitkeep
│
├── backups/
│   └── .gitkeep
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Requirements

Before installing the project, make sure you have:

* **Python 3.10 or newer**
* Windows, Linux, or macOS
* Tkinter installed with your Python installation
* Git (optional, if you want to clone the project from GitHub)

No external database server is required.

No cloud service is required.

---

# Installation

## 1. Clone the repository

If you have Git installed:

```bash
git clone https://github.com/YOUR-USERNAME/HIMS-Tkinter.git
```

Enter the project directory:

```bash
cd HIMS-Tkinter
```

Replace `YOUR-USERNAME` with the GitHub username that owns the repository.

---

## 2. Create a virtual environment

Creating a virtual environment is recommended.

### Windows

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

The project is intentionally lightweight and primarily uses Python's standard library.

---

# Running the Application

From the project root:

```bash
python main.py
```

The Tkinter desktop application should open.

---

# First Run

On the first launch, the application initializes the required local directories and data files.

The application uses local CSV files for storage.

Typical directories include:

```text
data/
exports/
backups/
```

The application creates the required data structure when necessary.

---

# Authentication

The application includes local user authentication.

Passwords are **not stored as plaintext**.

Password protection uses salted password hashing with PBKDF2-HMAC-SHA256.

Users should always choose strong passwords.

There is no hard-coded default administrator password.

---

# Data Storage

This application uses CSV files instead of a traditional database.

This approach makes the project:

* Easy to understand
* Easy to inspect
* Portable
* Suitable for offline demonstrations
* Simple to back up

However, CSV storage is not intended to replace a production hospital database.

---

# Backup and Export

The application provides local backup/export functionality.

Generated backups and exports are stored locally.

The following directories are intentionally kept outside Git version control:

```text
data/
exports/
backups/
```

This prevents local patient records, generated reports, and backup archives from accidentally being committed to GitHub.

---

# Security

The project includes several basic security measures:

* Password hashing
* Unique password salts
* PBKDF2-HMAC-SHA256
* No plaintext password storage
* Local authentication
* Input validation
* Confirmation before destructive operations
* Local backup functionality

These measures are intended for an educational/local application and should not be considered sufficient for a production healthcare environment.

---

# Important Privacy Notice

**Do not upload real patient information to this GitHub repository.**

Do not commit:

* Patient names
* Addresses
* Phone numbers
* Medical records
* Medical histories
* Prescriptions
* Payment information
* Passwords
* Authentication data
* Local database/CSV files
* Backup archives
* Exported reports

The repository should contain **source code and documentation**, not real hospital data.

---

# Development

To work on the project locally:

```bash
git clone https://github.com/YOUR-USERNAME/HIMS-Tkinter.git
cd HIMS-Tkinter
python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

---

# Testing

A basic application test can be performed by running:

```bash
python main.py
```

You should verify:

1. The application starts.
2. The login screen appears.
3. A new local account can be created.
4. Login works.
5. The dashboard loads.
6. Patients can be added and edited.
7. Doctors can be added and edited.
8. Appointments can be created.
9. Departments can be managed.
10. Wards and beds can be managed.
11. Payments/invoices can be managed.
12. Search and filtering work.
13. CSV exports work.
14. Backups can be created.
15. Logout works.

---

# GitHub Setup

After installing Git and testing the application:

```bash
git init
git add .
git commit -m "Initial release of HIMS Tkinter application"
```

Rename the default branch:

```bash
git branch -M main
```

Add your GitHub repository:

```bash
git remote add origin https://github.com/YOUR-USERNAME/HIMS-Tkinter.git
```

Push the project:

```bash
git push -u origin main
```

Replace:

```text
YOUR-USERNAME
```

with your actual GitHub username.

---

# Recommended GitHub Repository Settings

Recommended repository visibility:

```text
Public
```

if you want others to study and contribute to the project.

Before making the repository public, make sure no sensitive information has been committed.

Check the repository with:

```bash
git status
```

You can also inspect what Git is about to commit:

```bash
git status
```

and:

```bash
git diff --cached
```

---

# Disclaimer

This software is provided for **educational, demonstration, and local-development purposes**.

It has not been certified, validated, or approved for clinical use.

It should not be used as a production hospital information system or as a substitute for professionally validated healthcare software.

Users are responsible for protecting any data entered into the application and for complying with applicable privacy, security, healthcare, and data-protection requirements.

---

# License

You may add an open-source license depending on how you want others to use the project.

For example, an MIT License can be added as:

```text
LICENSE
```

If you choose MIT, include the official license text rather than writing your own shortened version.

---

# Author

**YOUR NAME**

GitHub:

```text
https://github.com/YOUR-USERNAME
```

---

## Project Status

**Status:** Educational / Local Desktop Prototype

**Platform:** Windows, Linux, macOS

**Interface:** Tkinter Desktop GUI

**Storage:** Local CSV files

**Network:** Not required

**Database Server:** Not required

**Cloud:** Not required
