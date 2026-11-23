# OrgEventManager

> **Repository Name: OrgEventManager-Pena-ChristianJay-G06**  
> Student Organization Event & Attendance Management System  
> Phase 1: Project Setup + Account Feature  
> Phase 2: Core Feature (Vertical Slice) — Event Management & RSVP Attendance Tracking

---

## 📖 Project Overview

**OrgEventManager** is a full-stack web application tailored for university student organizations to schedule campus events, track live attendance roll-calls, and streamline member participation.

The project is built on **Django 5** and backed by **Supabase PostgreSQL**.

---

## 🛠️ Tech Stack

- **Backend & Web Framework**: Python 3.12+ / Django 5.x (`django.contrib.auth`, `django.contrib.messages`)
- **Database Engine**: **Supabase PostgreSQL** (Strictly NOT SQLite) with SSL enforcement (`sslmode=require`)
- **Database Connectors**: `psycopg2-binary>=2.9.9`, `dj-database-url>=2.1.0`
- **Environment & Secrets**: `python-dotenv>=1.0.1` (managed via `.env`, excluded in `.gitignore`)
- **Image Processing**: `Pillow>=10.2.0` (for user profile avatars)
- **Frontend Architecture**: Django Templates styled with responsive, clean custom CSS

---

## 🚀 Core Feature: Event Management & RSVP (Vertical Slice)

### 1. Officer Event Management (CRUD)
- **Create Event (`/events/create/`)**: Officers publish events with Title, Description, Scheduled Date/Time, Venue, and Capacity. Form validation blocks any events scheduled in the past.
- **Manage Events (`/events/manage/`)**: Officer listing showing all authored events, live confirmed counts, and edit/delete actions.
- **Update Event (`/events/<id>/edit/`)**: Real-time modification of event schedules and venue details.
- **Delete Event (`/events/<id>/delete/`)**: Confirmation view allowing permanent removal of events and cascading cleanup of RSVPs.
- **Live Attendance Tracker (`/events/attendance/`)**: Overview of all sessions and attendee quotas.

### 2. Member RSVP & Attendance Tracking
- **Upcoming Events Directory (`/events/upcoming/`)**: Read-only directory of future campus events displaying venue, schedule, remaining spots, and current user RSVP status.
- **Event Detail & Interactive RSVP (`/events/<id>/`)**:
  - **Members**: Direct RSVP action card allowing members to toggle between **Going** and **Not Going**. Overbooking protection prevents RSVPs when capacity is reached.
  - **Officers**: Comprehensive **Attendee Roster** table revealing attendee full names, email addresses, contact numbers, and response timestamps.
- **My RSVPs (`/events/my-rsvps/`)**: Personal attendance history tracking confirmed events.

---

## 🌿 Git Branching Strategy

Development strictly adheres to GitFlow conventions:
- **`main`**: Production-ready branch with verified, tested features.
- **`develop`**: Persistent integration branch where feature branches merge.
- **`feature/event-crud`**: Feature branch containing Event model, Officer CRUD views, forms, and templates.
- **`feature/rsvp-tracking`**: Feature branch containing RSVP model, Member attendance views, event detail, and attendee rosters.

All feature branches are retained on the remote repository (`origin`) for review and verification.

---

## 🔑 Pre-Seeded Test Accounts

| Role | Username | Email Address | Password | Default Dashboard |
| :--- | :--- | :--- | :--- | :--- |
| **Officer** (Admin) | `officer_alex` | `officer@university.edu` | `Password123!` | `/dashboard/officer/` |
| **Member** (Student) | `member_taylor` | `member@university.edu` | `Password123!` | `/dashboard/member/` |

> Passwords in the database are securely hashed using Django's standard **PBKDF2-SHA256** algorithm. Passwords are never stored in plain text.

---

## 📁 Repository & Ignored Secrets Notice

The following directories and sensitive files are strictly excluded from version control via `.gitignore`:
- `.env` &mdash; contains database credentials, Supabase connection strings, and secret keys.
- `media/*` &mdash; uploaded member profile photos (keeps only `.gitkeep`).
- `venv/` &mdash; local Python virtual environment.
- `__pycache__/` and `*.pyc` &mdash; compiled Python bytecode.

---

## 🪟 Windows Path & Terminal Notes

The project root directory is:
`Z:\L23X07W32\Project Development 1 – Account Feature`

> **Note on Spaces and En-Dash**:  
> Always enclose the directory path in quotation marks when navigating in PowerShell or CMD:
> ```powershell
> cd "Z:\L23X07W32\Project Development 1 – Account Feature"
> ```

---

## 🚀 Local Setup & Execution Instructions

### 1. Open Terminal & Navigate to Project Root
```powershell
cd "Z:\L23X07W32\Project Development 1 – Account Feature"
```

### 2. Configure Environment Variables (`.env`)
Copy the provided `.env.example` template:
```powershell
copy .env.example .env
```
Ensure `.env` contains your active Supabase connection string:
```ini
SECRET_KEY=django-insecure-replace-with-a-secure-50-character-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
DATABASE_URL=postgresql://postgres.yourprojectref:yourpassword@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
```

### 3. Activate Virtual Environment
```powershell
# In PowerShell:
.\venv\Scripts\Activate.ps1

# In Command Prompt (CMD):
venv\Scripts\activate.bat
```

### 4. Apply Database Migrations
```powershell
python manage.py migrate
```

### 5. Seed Test Accounts
```powershell
python manage.py seed_data
```

### 6. Run the Development Server
```powershell
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.
