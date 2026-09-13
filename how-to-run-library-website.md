# Library Management System — Setup & Usage Guide

## 1. Install prerequisites

- **Python**: python.org/downloads — during install, check **"Add python.exe to PATH"**.
- **PostgreSQL**: postgresql.org/download — remember the password you set for the `postgres` user.

## 2. Set up the project

Unzip the project folder, open PowerShell inside it, then:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django psycopg2-binary
```

*(If PowerShell blocks the activate script: `Set-ExecutionPolicy -Scope Process RemoteSigned`, then retry.)*

## 3. Create the database

```powershell
psql -U postgres
```

```sql
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
```

> Match this username/password to whatever is in `librarysystem/settings.py`.

## 4. Build tables & create your login

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data   # optional: loads sample books/music/toys
```

## 5. Run it

```powershell
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. Stop with `Ctrl+C`. Next time, just re-activate the venv (`.\venv\Scripts\Activate.ps1`) and re-run the server command.

## 6. Using the site

| Section | Access | Purpose |
|---|---|---|
| Search Catalog | Public | Browse/search available items |
| Reception | Login required | Borrow / return items |
| Manager Stats | Login required | Borrowing, item, and fine stats |
| Admin (`/admin/`) | Superuser | Add/edit/delete items |

Log in everywhere with your superuser account — it has access to all sections.

**Quick walkthrough:** Admin → add an item → Search Catalog to find it → Reception/Borrow with its library code → Reception/Return → check Manager Stats for the updated numbers.

## Troubleshooting

| Problem | Fix |
|---|---|
| Command not recognized | Venv not active — run `.\venv\Scripts\Activate.ps1` |
| Password authentication failed | `settings.py` password ≠ Postgres password |
| Could not connect to server | PostgreSQL service isn't running |
| `TemplateDoesNotExist` | Missing template file — code issue, ask the student |
| `relation does not exist` | Run `python manage.py migrate` |
