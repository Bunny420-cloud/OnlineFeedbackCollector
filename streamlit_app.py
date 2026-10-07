import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Page Configuration
st.set_page_config(
    page_title="Online Feedback Collector",
    page_icon="⭐",
    layout="wide"
)

# Database Connection Helper
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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

init_db()

# Application Title
st.title("⭐ Online Feedback Collector")
st.markdown("Submit your feedback or view admin analytics.")

# Navigation Tabs
tab1, tab2 = st.tabs(["📝 Submit Feedback", "📊 Admin Analytics Dashboard"])

# -----------------------------------------------------------------------------
# TAB 1: PUBLIC FEEDBACK FORM
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("We value your opinion!")
    
    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
        with col2:
            email = st.text_input("Email Address", placeholder="e.g. john@example.com")
            
        rating = st.select_slider(
            "Rating",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "⭐" * x + f" ({x}/5)"
        )
        
        comments = st.text_area("Your Comments / Suggestions", placeholder="Tell us about your experience...")
        
        submitted = st.form_submit_button("Submit Feedback", type="primary")
        
        if submitted:
            if not name.strip() or len(name.strip()) < 2:
                st.error("Please enter a valid name (at least 2 characters).")
            elif not email.strip() or "@" not in email:
                st.error("Please enter a valid email address.")
            elif not comments.strip() or len(comments.strip()) < 5:
                st.error("Please enter comments (at least 5 characters).")
            else:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        "INSERT INTO feedback (name, email, rating, comments, date_submitted) VALUES (?, ?, ?, ?, ?)",
                        (name.strip(), email.strip(), rating, comments.strip(), now_str)
                    )
                    conn.commit()
                    conn.close()
                    st.success("🎉 Thank you! Your feedback has been submitted successfully.")
                except Exception as e:
                    st.error(f"Failed to submit feedback: {e}")

# -----------------------------------------------------------------------------
# TAB 2: ADMIN DASHBOARD
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("🔒 Admin Dashboard & Analytics")
    
    admin_pass = st.text_input("Enter Admin Password", type="password", key="admin_pwd")
    
    if admin_pass == "admin123":
        st.success("Authenticated as Administrator")
        
        # Load feedback data
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM feedback ORDER BY id DESC", conn)
        conn.close()
        
        if df.empty:
            st.info("No feedback submissions yet.")
        else:
            # Metric KPI Cards
            total_feedback = len(df)
            avg_rating = round(df["rating"].mean(), 2)
            five_star = len(df[df["rating"] == 5])
            one_star = len(df[df["rating"] == 1])
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Submissions", total_feedback)
            m2.metric("Average Rating", f"{avg_rating} / 5.0")
            m3.metric("5-Star Reviews", five_star)
            m4.metric("1-Star Reviews", one_star)
            
            st.divider()
            
            # Charts & Table Filter
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("### Rating Distribution")
                rating_counts = df["rating"].value_counts().sort_index()
                st.bar_chart(rating_counts)
                
            with col_chart2:
                st.markdown("### Search Submissions")
                search_query = st.text_input("Filter by Name, Email, or Comment", "")
                if search_query:
                    filtered_df = df[
                        df["name"].str.contains(search_query, case=False, na=False) |
                        df["email"].str.contains(search_query, case=False, na=False) |
                        df["comments"].str.contains(search_query, case=False, na=False)
                    ]
                else:
                    filtered_df = df
                    
            st.dataframe(filtered_df, use_container_width=True)
            
            # CSV Download
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Feedback CSV",
                data=csv_data,
                file_name="feedback_export.csv",
                mime="text/csv",
                type="primary"
            )
    elif admin_pass:
        st.error("Incorrect Admin Password. Default is: admin123")
