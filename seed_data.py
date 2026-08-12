import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def seed_demo_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure table exists
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

    sample_feedbacks = [
        ("Sarah Jenkins", "sarah.j@example.com", 5, "An exceptionally designed application! The star rating system is smooth and responsive.", (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Michael Chang", "mchang@techhub.org", 4, "Great platform for gathering feedback. Navigation is clean and simple.", (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Emily Watson", "emily.watson@designco.com", 5, "Loved the live dashboard analytics and instant table search features!", (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")),
        ("David Miller", "david.m@devstudio.net", 3, "Good submission system. Would appreciate more chart export options in future.", (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Amanda Torres", "amanda.t@cloudworks.io", 5, "Super slick dark mode design and CSV export works seamlessly. 10/10!", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Robert Brooks", "rbrooks@enterprise.com", 2, "Form is intuitive, but noticed a slight delay when testing on low bandwidth network.", (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Rachel Green", "rachel.g@fashionstyle.org", 5, "Fantastic user experience! The admin login and security controls work flawlessly.", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ]

    cursor.executemany("""
        INSERT INTO feedback (name, email, rating, comments, date_submitted)
        VALUES (?, ?, ?, ?, ?)
    """, sample_feedbacks)

    conn.commit()
    conn.close()
    print(f"[OK] Successfully seeded {len(sample_feedbacks)} sample feedback entries into database.db!")

if __name__ == "__main__":
    seed_demo_data()

