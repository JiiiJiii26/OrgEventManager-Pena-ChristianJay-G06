# OrgEventManager

> **Repository Name: OrgEventManager-Pena-ChristianJay-G06**  
> Student Organization Event & Attendance Management System  
> Phase 1: Project Setup + Account Feature

---

## 📖 Project Overview

**OrgEventManager** is a web application tailored for student organizations to coordinate campus events, maintain real-time attendee roll-calls, and manage member participation.

Phase 1 establishes the foundational architecture and complete **Account Feature**, incorporating secure role-based access control, dual-identifier authentication, and dedicated self-service user profiles.

---

## 🛠️ Tech Stack

- **Backend & Web Framework**: Python 3.12+ / Django 5.x (`django.contrib.auth`, `django.contrib.messages`)
- **Database**: **Supabase PostgreSQL** (Strictly NOT SQLite)
- **Database Connectors**: `psycopg2-binary>=2.9.9`, `dj-database-url>=2.1.0`
- **Environment & Secrets**: `python-dotenv>=1.0.1` (managed via `.env`, excluded in `.gitignore`)
- **Image Processing**: `Pillow>=10.2.0` (for user profile avatars)
- **Frontend**: Django Templates with clean responsive custom CSS (no heavy external CSS/JS frameworks)

---

## ✨ Phase 1 Features

1. **Custom User Model (`CustomUser`)**:
   - Subclasses `AbstractUser`.
   - Incorporates organization roles: **Officer** (`OFFICER`) and **Member** (`MEMBER`).
   - Fields: `username` (unique), `email` (unique), `full_name`, `contact_number`, and optional `profile_photo`.
   - Strict password hashing via Django's PBKDF2-SHA256 algorithm.

2. **Dual Authentication & Session Management**:
   - Allows users to sign in using either their **Username OR Email Address**.
   - Custom backend (`EmailOrUsernameModelBackend`) ensures seamless case-insensitive matching.
   - Clean logout workflow destroying session data and redirecting with flash feedback.

3. **Role-Based Access Control (RBAC)**:
   - Dedicated `@role_required`, `@officer_required`, and `@member_required` decorators.
   - Unauthorized access attempts are rejected, triggering an error message and redirecting the user to their authorized dashboard.
   - **Officer Dashboard (`/dashboard/officer/`)**: Create Event, Track Attendance, Export Reports, and event management rosters.
   - **Member Dashboard (`/dashboard/member/`)**: Upcoming campus events, RSVP management, and participation status.

4. **Self-Service User Profile**:
   - Located at `/profile/`, accessible strictly to the authenticated user (no arbitrary ID querying).
   - Allows users to view and update full name, email, contact number, and upload avatar photos (`media/profile_photos/`).

---

## 🔑 Pre-Seeded Test Accounts

| Role | Username | Email Address | Password | Default Dashboard |
| :--- | :--- | :--- | :--- | :--- |
| **Officer** (Admin) | `officer_alex` | `officer@university.edu` | `Password123!` | `/dashboard/officer/` |
| **Member** (Student) | `member_taylor` | `member@university.edu` | `Password123!` | `/dashboard/member/` |

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
> *Tooling note*: Standard Windows PowerShell and CMD handle the existing path when quoted.

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
Ensure your `.env` contains your active Supabase connection string:
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
*(If dependencies need to be reinstalled)*:
```powershell
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Runs migrations for the custom user model (`accounts.CustomUser`) and Phase 2 stub (`events.Event`) against Supabase:
```powershell
python manage.py migrate
```

### 5. Seed Test Accounts
Create the default Officer and Member accounts with pre-hashed credentials:
```powershell
python manage.py seed_data
```

### 6. Create Superuser (Optional)
To access the Django Administration interface at `/admin/`:
```powershell
python manage.py createsuperuser
```

### 7. Run the Development Server
```powershell
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.
