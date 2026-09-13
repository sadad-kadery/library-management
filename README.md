# Library Management System

Django + PostgreSQL library system with separate Admin, Reception, and Manager accounts, plus a public search portal.

**Live demo:** [https://library-management-wyqj.onrender.com/](https://library-management-wyqj.onrender.com/)
*(Free hosting — first load may take 30–60s if idle.)*

## Login Credentials

| Role | Login | Username | Password |
|---|---|---|---|
| Superuser | `/admin/login/` | `maher` | `Maher123@` |
| Reception | `/reception/login/` | `R2` | `Rec123@` |
| Manager | `/manager/login/` | `M2` | `Manag123@` |


**About the superuser account:** `maher` isn't a fourth role — it's an override account that bypasses the Admin/Reception/Manager checks, so one login can inspect the whole system. Real staff would only ever hold a Reception or Manager account, each restricted to its own section — `R2` and `M2` demonstrates that restricted experience.

## Features

- **Admin** — CRUD on Books, Music, Toys (all inheriting a shared `Item` class with name, description, library code, status)
- **Reception** — borrow/return items, auto-fill returning borrowers, late fines, borrower CRUD, add new items, clear paid fines
- **Manager** — borrowing/item/fine statistics with charts, create Reception accounts
- **Public** — responsive catalog search, no login needed, shows availability and who's borrowed what

## Tech Stack

Python / Django · PostgreSQL · Bootstrap 5 · Chart.js · hosted on Render

## Structure

```
librarysystem/   # settings, root URLs
catalog/         # Item, Book, Music, Toy models + admin CRUD
circulation/     # Borrower, Loan, Fine models; views, templates, role logic
```

## Run Locally

```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data      # optional sample data
python manage.py runserver
```