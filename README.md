# trekking-management-V2-project
This is the Trekking management system app made with vuejs frontend and flask backend and sqlite database. In which user can book trek for themself and staff will be assigned to them as a guide . and a admin who manage all of treks and staff 

## Project Structure
trekking-management-V2-project/
├── backend/     ← Flask API, SQLite DB, Celery, Redis caching
└── frontend/    ← Vue.js app

AAll backend commands below are run **inside the `backend/` folder**.
All frontend commands are run **inside the `frontend/` folder**.

---

## Prerequisites

- Python 3.x
- Node.js + npm
- Redis (must be installed and available as `redis-server`)
- Celery (installed via `requirements.txt`)
- MailHog (for catching outgoing emails in development)

---

## ⚠️ Important: Redis Must Be Running

This app uses **Redis** for caching (Flask-Caching) and as the **message broker for Celery**.

**Redis must be running BEFORE you start the Flask server.** If Redis is not running when you load the admin, user, or staff dashboards, those pages will fail.

Always start Redis first, and keep it running in its own terminal the whole time you use the app.

---

## Environment Setup

Before running the backend, copy the sample environment file and fill in your own values:

```bash
cd backend
cp .env.sample .env       # Linux/Mac
copy .env.sample .env     # Windows
```

Then open `.env` and fill in your own values for:
- `SECRET_KEY`
- `JWT_SECRET_KEY`

The other values in `.env.sample` (database URI, Flask config) can be left as-is unless you need to change them.

## Setup & Running the App

You'll need **6 terminals open at the same time**, each doing one job. Follow them in this order.

### Terminal 1 — Backend Setup + Flask Server

```bash
cd backend
```

Create and activate a virtual environment (only needed the first time):

```bash
python -m venv venv
```

Activate it:

```bash
.\venv\Scripts\activate     # Windows
source venv/bin/activate    # Linux/Mac
```

Install dependencies (only needed the first time, or when requirements.txt changes):

```bash
pip install -r requirements.txt
```

**Do NOT start Flask yet — first confirm Redis is running (Terminal 2 below). Once Redis is confirmed running, come back here and start Flask:**

```bash
flask run
```

If you ever add a new package while working on the backend, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

### Terminal 2 — Redis Server

Open a new terminal:

```bash
cd backend
redis-server
```

Leave this running. Confirm it started successfully 
to check that Redis is running:

```bash
redis-cli ping
```

If you see `PONG`, Redis is running.

---

### Terminal 3 — Celery Worker

Open a new terminal:

```bash
cd backend
.\venv\Scripts\activate     # Windows
source venv/bin/activate    # Linux/Mac
celery -A celery_app.celery worker --loglevel=info
```

> On Windows, if the worker throws errors related to the process pool, use:
> `celery -A celery_app.celery worker --loglevel=info --pool=solo`

---

### Terminal 4 — Celery Beat (scheduler)

Open a new terminal:

```bash
cd backend
.\venv\Scripts\activate     # Windows
source venv/bin/activate    # Linux/Mac
celery -A celery_app.celery beat --loglevel=info
```

This handles the daily reminder emails and the monthly admin report on schedule.

---

### Terminal 5 — MailHog (catches outgoing emails)

Open a new terminal and start MailHog however you normally run it, for example:

```bash
MailHog
```

MailHog's web UI (usually `http://localhost:8025`) is where you'll see all emails sent by the app (daily reminders, monthly reports, CSV export emails) — the app is configured to send mail to `localhost:1025`, which MailHog listens on.

---

### Terminal 6 — Frontend (Vue.js)

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

This starts the Vue dev server. Open the URL it prints (usually `http://localhost:5173`) in your browser.

---

## Startup Order Summary

1. Terminal 2 → Redis
2. Terminal 1 → Flask (only after Redis is confirmed running)
3. Terminal 3 → Celery worker
4. Terminal 4 → Celery beat
5. Terminal 5 → MailHog
6. Terminal 6 → Frontend

## Default Admin Login

An admin account is auto-created on first run:
- Email: `admin@gmail.com`
- Password: `admin123`
