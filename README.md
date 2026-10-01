# Timesheets

A web application for logging working time, requesting holiday and reporting on hours, built for **Sefas Innovation**. Employees record hours against customers and job codes; administrators manage staff, approve leave and export data.

## Features

**Employee side (`timesheets` app)**
- Login-protected weekly timesheet with a day-by-day view for logging hours against a job code and customer, with notes
- Holiday requests with automatic working-day calculation (optionally including weekends) and a check against the remaining allowance
- Profile page showing team, allowance, remaining and pending hours
- "My requests" page for tracking the status of leave requests
- Bank holidays modelled as first-class days so they are excluded from working time

**Admin side (`sefas_admin` app, superuser only)**
- Create and modify users and teams
- Review, edit and delete holiday requests
- Manage bank holidays
- Export logged jobs to CSV, optionally filtered by date range

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8, Django 3.2 (class-based and function views, model migrations, signals, Django auth) |
| Database | MongoDB Atlas via `djongo` (Django ORM on MongoDB); `pymongo` helper module for direct access |
| Frontend | Django templates, django-crispy-forms, custom CSS; Vue 2 (Vue CLI) client scaffold in `timesheetsvue/` |
| Deployment | Heroku (Procfile), gunicorn, WhiteNoise for static files |

## Project layout

```
DjangoServer/     project settings, URLs, WSGI/ASGI
timesheets/       employee-facing app (models, views, forms, signals, 59 migrations)
sefas_admin/      admin-facing app (user, holiday and report management)
MongoDB/          pymongo helper (insert, update-or-create)
timesheetsvue/    Vue 2 front-end scaffold
```

## Running locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # set SECRET_KEY and MONGO_URI
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## My role
Developer for all application elements
