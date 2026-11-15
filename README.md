# TrekCentral – Trekking Management System

TrekCentral is a full-stack trekking management application that allows users to explore and book treks, trekking staff to manage assigned treks, and administrators to manage the overall platform.

The application follows a **Vue.js frontend + Flask REST API backend** architecture, with role-based access control, JWT authentication, background task processing, caching, and automated email notifications.

## Key Features

### Authentication & User Management
- User registration and login.
- JWT-based authentication.
- Role-based access for Admin, Trek Staff, and Trekker.
- Profile management and password updates.
- Account blacklisting and activation.

### Admin Dashboard
- Dashboard with user, staff, trek, and booking statistics.
- Visual representation of booking and revenue data.
- Create, update, and delete treks.
- Approve and manage trekking staff.
- Assign staff members to treks.
- Manage users, staff, and bookings.

### Trekker Features
- Browse available treks and view trek details.
- Book and cancel trek reservations.
- View booking history.
- Update profile information.
- Export trekking history as a CSV file through email.

### Trek Staff Features
- View assigned treks.
- Manage trek status.
- Update available slots.
- View registered and cancelled participants.

### Background Processing & Notifications
- Asynchronous task execution using Celery.
- Redis as the message broker.
- Scheduled daily reminders for users.
- Scheduled monthly activity reports for administrators.
- Automated HTML email notifications.
- CSV report generation and email delivery with attachments.

### Booking & Data Management
- SQLAlchemy ORM for database operations.
- Relational database models for users, treks, and bookings.
- Prevention of duplicate bookings and overbooking.
- Validation of booking and trek-related operations.
- Redis-backed response caching.

---

## Technology Stack

### Frontend

| Technology | Usage |
|---|---|
| Vue.js 3 | Frontend framework |
| JavaScript (ES Modules) | Application logic |
| Vue Composition API | Component logic and reactivity |
| Vue Router | Client-side routing |
| Pinia | State management |
| HTML5 | Application structure |
| CSS3 | Styling |
| Bootstrap 5.3 | Responsive UI and components |
| Bootstrap Icons / Font Awesome 7 | Iconography (Font Awesome is included) |
| Chart.js | Dashboard charts and data visualisation |
| Vite 8 | Development server and build tool |

### Backend

| Technology | Usage |
|---|---|
| Python | Backend programming language |
| Flask 3 | Backend web framework |
| Flask-RESTful | REST API development |
| Flask-SQLAlchemy | Flask integration with SQLAlchemy |
| SQLAlchemy 2 | ORM and database operations |
| Flask-JWT-Extended | JWT authentication |
| Flask-Caching | Application-level caching |
| Flask-CORS | Cross-Origin Resource Sharing |
| Werkzeug | Password hashing and utilities |
| python-dotenv | Environment variable management |

### Database, Caching & Background Tasks

| Technology | Usage |
|---|---|
| SQLite | Relational database |
| Redis | Message broker and caching backend |
| Celery | Asynchronous background task processing |
| Celery Beat | Periodic task scheduling |

### Email & Data Processing

| Technology | Usage |
|---|---|
| Python SMTP (`smtplib`) | Sending emails |
| Python Email MIME | HTML emails and file attachments |
| Python `csv` module | CSV report generation |
| Python `datetime` | Date and time handling |
| Celery `crontab` | Scheduled task configuration |

### Development & Code Quality Tools

| Tool | Usage |
|---|---|
| Node.js | JavaScript runtime |
| npm | Package management |
| ESLint | JavaScript and Vue linting |
| Oxlint | Fast code linting |
| Prettier | Code formatting |
| Vite Vue Plugin | Vue support in Vite |
| Vue DevTools Plugin | Vue development debugging |
| Git & GitHub | Version control and source code management |

---

## Project Architecture

```text
TrekCentral/
│
├── backend/
│   ├── app.py
│   ├── apis.py
│   ├── models.py
│   ├── config.py
│   ├── celery_app.py
│   ├── mail.py
│   ├── requirements.txt
│   └── .env.sample
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   ├── views/
    │   ├── stores/
    │   ├── router/
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or later
- Node.js (22.18+ or 24.12+)
- npm
- Redis
- requires a local SMTP service configured for localhost:1025.

### 1. Clone the Repository

```bash
git clone https://github.com/23f2001140/trekking-management-V2-project.git
cd trekking-management-V2-project
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using the provided sample:

```bash
cp .env.sample .env
```

On Windows, you can copy the file manually or use:

```powershell
copy .env.sample .env
```

Configure the required environment variables in `.env`, including `SECRET_KEY` and `JWT_SECRET_KEY`.

Start the Flask backend:

```bash
flask run
```

### 3. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

### 4. Start Redis

Make sure the Redis server is running before using caching and background tasks.

### 5. Start Celery Workers

Open a separate terminal in the backend directory and activate the virtual environment.

Start the Celery worker:

```bash
celery -A celery_app.celery worker --loglevel=info
```

Start Celery Beat for scheduled tasks:

```bash
celery -A celery_app.celery beat --loglevel=info
```

---

## Demo Administrator Account

The application initialises a default administrator account when the database is created.

| Field | Value |
|---|---|
| Email | `admin@gmail.com` |
| Password | `admin123` |

**Note:** These credentials are intended only for local demonstration. Change or disable the default account before using the application in a shared or deployed environment.

---

## Author

**Anurag Bharti**

