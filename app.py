import os
import csv
import io
import re
import sqlite3
from functools import wraps
from datetime import datetime
from flask import (
    Flask, render_template, request, jsonify, redirect, url_for, session, flash, Response, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from jinja2 import ChoiceLoader, FileSystemLoader

# Load environment variables from .env file if available
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-dev-secret-key-987654321")

# Configure Jinja to search both root directory and templates/ subfolder for HTML files
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    FileSystemLoader(BASE_DIR)
])

# Database File Configuration
def get_db_path():
    db_name = os.environ.get("DATABASE_NAME", "database.db")
    local_db = os.path.join(BASE_DIR, db_name)
    # On Vercel or read-only environments, store/copy database in /tmp
    if os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV") or not os.access(BASE_DIR, os.W_OK):
        tmp_db = os.path.join("/tmp", db_name)
        if not os.path.exists(tmp_db):
            if os.path.exists(local_db):
                try:
                    import shutil
                    shutil.copyfile(local_db, tmp_db)
                except Exception as e:
                    print(f"Error copying DB to /tmp: {e}")
                    return ":memory:"
            else:
                return ":memory:"
        return tmp_db
    return local_db

# Admin Credentials (Environment variables with safe defaults)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get("ADMIN_PASSWORD", "admin123"))
def get_db_connection():
    """
    Establishes and returns a row-factory enabled SQLite database connection.
    Falls back to in-memory DB if file access fails on serverless platforms.
    """
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"File DB failed, falling back to in-memory DB: {e}")
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    """
    Initializes the SQLite database and creates the 'feedback' table if not existing.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comments TEXT NOT NULL,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# Ensure database and table exist upon startup safely
try:
    init_db()
except Exception as e:
    print(f"Startup DB init warning: {e}")


def login_required(f):
    """
    Decorator to protect admin routes against unauthenticated users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the Admin Dashboard.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def validate_feedback_input(name, email, rating, comments):
    """
    Server-side validation for feedback input fields.
    Returns (is_valid, error_message).
    """
    if not name or not name.strip():
        return False, "Name is required and cannot be empty."
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long."
    
    if not email or not email.strip():
        return False, "Email address is required."
    
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email.strip()):
        return False, "Please provide a valid email address."
    
    try:
        rating_val = int(rating)
        if rating_val < 1 or rating_val > 5:
            return False, "Rating must be an integer between 1 and 5."
    except (ValueError, TypeError):
        return False, "Rating must be a valid number between 1 and 5."
    
    if not comments or not comments.strip():
        return False, "Comments cannot be empty."
    if len(comments.strip()) < 5:
        return False, "Comments must be at least 5 characters long."
    
    return True, None


# -----------------------------------------------------------------------------
# PUBLIC ROUTES
# -----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """
    Renders the public landing page with the feedback collection form.
    """
    return render_template("index.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    """
    Handles submission of user feedback via AJAX (JSON) or Form POST.
    Saves feedback record into SQLite database.
    """
    if request.is_json:
        data = request.get_json() or {}
        name = data.get("name", "")
        email = data.get("email", "")
        rating = data.get("rating", "")
        comments = data.get("comments", "")
    else:
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        rating = request.form.get("rating", "")
        comments = request.form.get("comments", "")

    is_valid, error_msg = validate_feedback_input(name, email, rating, comments)
    if not is_valid:
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 400
        else:
            flash(error_msg, "danger")
            return redirect(url_for("index"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO feedback (name, email, rating, comments, date_submitted)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name.strip(), email.strip(), int(rating), comments.strip(), now_str)
        )
        conn.commit()
        conn.close()

        success_msg = "Thank you! Your feedback has been submitted successfully."
        if request.is_json:
            return jsonify({"success": True, "message": success_msg}), 201
        else:
            flash(success_msg, "success")
            return redirect(url_for("index"))

    except Exception as e:
        app.logger.error(f"Database insertion error: {e}")
        err_response = "An error occurred while saving your feedback. Please try again later."
        if request.is_json:
            return jsonify({"success": False, "error": err_response}), 500
        else:
            flash(err_response, "danger")
            return redirect(url_for("index"))


# -----------------------------------------------------------------------------
# AUTHENTICATION ROUTES
# -----------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles Admin login page and authentication.
    """
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        if request.is_json:
            data = request.get_json() or {}
            username = data.get("username", "").strip()
            password = data.get("password", "")
        else:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin_logged_in"] = True
            session["admin_user"] = username
            if request.is_json:
                return jsonify({"success": True, "redirect": url_for("admin_dashboard")}), 200
            else:
                flash("Welcome back, Administrator!", "success")
                return redirect(url_for("admin_dashboard"))
        else:
            err = "Invalid username or password. Please try again."
            if request.is_json:
                return jsonify({"success": False, "error": err}), 401
            else:
                flash(err, "danger")

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logs out the admin user and clears the session.
    """
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# ADMIN DASHBOARD & CSV EXPORT
# -----------------------------------------------------------------------------

@app.route("/admin-dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    """
    Displays the summary metrics, charts, and feedback table in the Admin Dashboard.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all feedback records ordered by latest submission first
    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    feedback_list = [dict(row) for row in rows]
    total_count = len(feedback_list)

    if total_count > 0:
        avg_rating = round(sum(f["rating"] for f in feedback_list) / total_count, 2)
        five_star_count = sum(1 for f in feedback_list if f["rating"] == 5)
        one_star_count = sum(1 for f in feedback_list if f["rating"] == 1)
    else:
        avg_rating = 0.0
        five_star_count = 0
        one_star_count = 0

    stats = {
        "total_feedback": total_count,
        "avg_rating": avg_rating,
        "five_star_reviews": five_star_count,
        "one_star_reviews": one_star_count
    }

    return render_template("admin.html", stats=stats, feedback_list=feedback_list)


@app.route("/export-csv", methods=["GET"])
@login_required
def export_csv():
    """
    Exports all feedback entries as a downloadable CSV file.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, rating, comments, date_submitted FROM feedback ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        # Write CSV Header
        writer.writerow(["ID", "Name", "Email", "Rating", "Comments", "Date Submitted"])

        for row in rows:
            writer.writerow([
                row["id"],
                row["name"],
                row["email"],
                row["rating"],
                row["comments"],
                row["date_submitted"]
            ])

        csv_content = output.getvalue()
        output.close()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"feedback_export_{timestamp}.csv"

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        app.logger.error(f"CSV Export Error: {e}")
        flash("Failed to generate CSV export. Please try again.", "danger")
        return redirect(url_for("admin_dashboard"))


# -----------------------------------------------------------------------------
# REST API ENDPOINT
# -----------------------------------------------------------------------------

@app.route("/api/feedback", methods=["GET"])
def api_feedback():
    """
    Public/Protected REST API returning all feedback as JSON.
    Returns: { "success": true, "count": N, "feedback": [...] }
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, rating, comments, date_submitted FROM feedback ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        feedback_items = [
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "rating": row["rating"],
                "comments": row["comments"],
                "date_submitted": str(row["date_submitted"])
            }
            for row in rows
        ]

        return jsonify({
            "success": True,
            "count": len(feedback_items),
            "feedback": feedback_items
        }), 200

    except Exception as e:
        app.logger.error(f"API Error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve feedback data."
        }), 500


# -----------------------------------------------------------------------------
# DEMO DATA SEEDING ROUTE (Development Helper)
# -----------------------------------------------------------------------------

@app.route("/seed-data", methods=["POST", "GET"])
def seed_data():
    """
    Populates sample demonstration data into SQLite database.
    """
    sample_records = [
        ("Sophia Martinez", "sophia.m@example.com", 5, "The feedback form interface is super crisp and easy to use! Outstanding project work.", "2026-08-10 09:15:00"),
        ("Alexander Wright", "alex.wright@techmail.com", 4, "Overall great experience. Adding dark mode toggle would make it even better.", "2026-08-10 11:45:00"),
        ("Elena Rostova", "elena.r@devstudio.org", 5, "Extremely responsive UI and fast submission without page reload. Loved it!", "2026-08-11 08:30:00"),
        ("Marcus Vance", "marcus.v@enterprises.com", 2, "Form worked, but I experienced a minor lag on mobile screen width.", "2026-08-11 12:10:00"),
        ("Jessica Taylor", "jessica.t@designhub.io", 5, "The admin dashboard analytics and Chart.js integration are top-notch!", "2026-08-11 14:05:00"),
        ("David K.", "david.k@sample.net", 1, "Testing error validation response. Need faster customer support callback.", "2026-08-11 16:50:00"),
        ("Liam Patel", "liam.patel@innovate.com", 4, "Sleek presentation and clean CSV export feature. Very useful!", "2026-08-11 18:20:00")
    ]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO feedback (name, email, rating, comments, date_submitted)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_records
        )
        conn.commit()
        conn.close()

        msg = f"Successfully inserted {len(sample_records)} demonstration feedback records!"
        if request.is_json or request.args.get("format") == "json":
            return jsonify({"success": True, "message": msg}), 200
        else:
            flash(msg, "success")
            return redirect(url_for("admin_dashboard") if session.get("admin_logged_in") else url_for("index"))

    except Exception as e:
        app.logger.error(f"Seed Data Error: {e}")
        err = f"Failed to seed demo data: {str(e)}"
        if request.is_json:
            return jsonify({"success": False, "error": err}), 500
        else:
            flash(err, "danger")
            return redirect(url_for("index"))


# -----------------------------------------------------------------------------
# ERROR HANDLERS
# -----------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("layout.html", error_title="404 - Page Not Found", error_message="The page you requested does not exist."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("layout.html", error_title="500 - Server Error", error_message="An internal server error occurred."), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
