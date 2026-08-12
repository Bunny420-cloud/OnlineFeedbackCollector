# 🚀 Online Feedback Collector with Admin Dashboard

A full-stack web application built with **Python + Flask**, **SQLite**, **Bootstrap 5**, and **Chart.js**. This application allows users to submit feedback through an interactive star-rating web form and enables administrators to view summarized metrics, interactive charts, real-time search tables, and export feedback records as CSV files.

---

## 🌟 Features

- **Public Feedback Page**:
  - Interactive 5-star rating widget with real-time star preview labels.
  - Client-side validation (JavaScript) and server-side validation (Flask).
  - Asynchronous AJAX form submission (`fetch` API) without page reload.
  - Flash toasts and success alerts.
- **Admin Authentication**:
  - Secure session-based authentication protecting admin routes (`/admin-dashboard`, `/export-csv`).
  - Passwords hashed using `werkzeug.security`.
- **Admin Analytics Dashboard**:
  - **KPI Cards**: Total Submissions, Average Rating (out of 5.0), 5-Star Reviews, 1-Star Reviews.
  - **Dynamic Charts (Chart.js)**: Rating Distribution (1★–5★ Bar/Doughnut Chart) and Submission Trend over time (Line Chart).
  - **Interactive Feedback Table**: View ID, Name, Email, Star rating (★★★★★), Comments, and Submission Timestamp.
  - **Real-Time Table Search**: Filter feedback instantly by Name, Email, or Comments keyword.
- **REST API Endpoint**:
  - `GET /api/feedback` returns JSON formatted responses with status codes.
- **CSV Data Export**:
  - One-click download of all feedback entries formatted in standard CSV format using Python's `csv` module.
- **Development Demo Data**:
  - Seeding helper via `/seed-data` route or `python seed_data.py` standalone script.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.x + Flask 3.x
- **Database**: SQLite3 (`database.db`)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+ AJAX fetch)
- **Templating**: Jinja2
- **UI & Icons**: Bootstrap 5.3 + FontAwesome 6.5
- **Data Visualization**: Chart.js 4.x
- **CSV Handling**: Python native `csv` & `io` modules

---

## 📁 Project Structure

```
OnlineFeedbackCollector/
│
├── app.py                   # Main Flask application, routes, authentication, API & CSV export
├── seed_data.py             # Script to insert demonstration feedback records into SQLite
├── requirements.txt         # Required Python packages (Flask, python-dotenv, Werkzeug)
├── database.db              # SQLite database (auto-created on startup)
├── .env.example             # Environment variable configuration template
├── .gitignore               # Excluded files and database binaries
├── README.md                # Full project documentation & instructions
│
├── static/
│   ├── css/
│   │   └── style.css        # Modern glassmorphism dark theme, star widget & custom utilities
│   └── js/
│       └── script.js        # Form validation, star rating widget logic, AJAX & Chart.js renderer
│
└── templates/
    ├── layout.html          # Base Jinja2 layout (Bootstrap 5, FontAwesome, navigation & footer)
    ├── index.html           # User landing page with 5-star feedback form
    ├── admin.html           # Admin dashboard with metric cards, charts, table & search
    └── login.html           # Admin authentication login page
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone / Open Project Directory
Navigate to the project root directory:
```bash
cd OnlineFeedbackCollector
```

### 3. Create & Activate Virtual Environment

**On Windows (PowerShell / CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🔐 Admin Credentials

To access the protected Admin Dashboard (`/admin-dashboard`), log in at `/login` using the following default development credentials:

- **Username**: `admin`
- **Password**: `admin123`

> *Note: Environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`, `SECRET_KEY`) can be customized in a `.env` file.*

---

## 🔑 Available Routes & API Specifications

| Method | Route | Protection | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Home page with 5-star user feedback form |
| `POST` | `/submit-feedback` | Public | Receives feedback data, validates, and stores in SQLite |
| `GET` | `/login` | Public | Admin login page |
| `POST` | `/login` | Public | Authenticates administrator session |
| `GET` | `/logout` | Authenticated | Clears admin session and redirects to login |
| `GET` | `/admin-dashboard` | **Protected** | Renders admin dashboard with KPI cards, charts & table |
| `GET` | `/export-csv` | **Protected** | Downloads feedback entries as a CSV file |
| `GET` | `/api/feedback` | Public | REST API returning all feedback records as JSON |
| `POST` | `/seed-data` | Public/Dev | Inserts sample demonstration records into SQLite |

---

## 🌐 REST API Usage

### Endpoint: `GET /api/feedback`

#### Example Response (200 OK):
```json
{
  "count": 2,
  "feedback": [
    {
      "comments": "The feedback form interface is super crisp and easy to use!",
      "date_submitted": "2026-08-11 10:15:00",
      "email": "sophia.m@example.com",
      "id": 1,
      "name": "Sophia Martinez",
      "rating": 5
    },
    {
      "comments": "Overall great experience. Clean presentation.",
      "date_submitted": "2026-08-11 11:30:00",
      "email": "alex.wright@techmail.com",
      "id": 2,
      "name": "Alexander Wright",
      "rating": 4
    }
  ],
  "success": true
}
```

---

## 📥 CSV Export Instructions

1. Log in to the Admin Dashboard (`/login`).
2. Click the **"Export CSV"** button in the top right header.
3. The browser will automatically download a file named `feedback_export_YYYYMMDD_HHMMSS.csv`.
4. Open the file in Microsoft Excel, Google Sheets, or any CSV viewer.

---

##  🌱 Populating Demo Data

To demonstrate the application during college project presentations or testing:

**Option A (Via Web Interface):**
Click **"Seed Sample Data"** on either the home page sidebar or admin dashboard header.

**Option B (Via Terminal Command):**
```bash
python seed_data.py
```

---

## ☁️ Deployment Instructions

### Deploying to Render / Railway / PythonAnywhere:
1. Push repository to GitHub.
2. Create a Web Service on Render or Railway.
3. Set build command: `pip install -r requirements.txt`.
4. Set start command: `gunicorn app:app` (or `python app.py`).
5. Configure environment variables (`SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`).

---

## 📜 License & Author

- **Author**: Munukuntla Bunny Narayana Naidu ([@Bunny420-cloud](https://github.com/Bunny420-cloud))
- **GitHub Repository**: [https://github.com/Bunny420-cloud/OnlineFeedbackCollector](https://github.com/Bunny420-cloud/OnlineFeedbackCollector)
- **Project**: College Full-Stack Web Application & Summer Internship Project
- **License**: MIT License

