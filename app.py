"""
Prathamesh Rathod — Video Editor Portfolio
Backend: Python (Flask) + SQL (SQLite)

Run:
    pip install flask
    python app.py
Then open: http://127.0.0.1:5000
Admin dashboard: http://127.0.0.1:5000/admin  (password: pratya123 — change it below)
"""

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret_key_before_deploying")

DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "pratya123")   # set ADMIN_PASSWORD env var on your host

# --------------------------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed default services only if table is empty
    cur.execute("SELECT COUNT(*) FROM services")
    if cur.fetchone()[0] == 0:
        default_services = [
            ("Instagram Reels Editing", "High-energy, trend-ready reels edited for maximum reach and engagement.", "fa-solid fa-mobile-screen-button"),
            ("Political Campaign Videos", "Impactful political reels and campaign videos with strong messaging and pacing.", "fa-solid fa-bullhorn"),
            ("Cinematic Wedding Shoots", "Full wedding coverage shot and edited in a cinematic, storytelling style.", "fa-solid fa-ring"),
            ("Pre-Wedding & Couple Shoots", "Romantic, aesthetic pre-wedding and couple shoots planned and directed by me.", "fa-solid fa-heart"),
            ("Birthday & Event Shoots", "Fun, vibrant coverage of birthdays and celebrations, edited with energy.", "fa-solid fa-cake-candles"),
            ("All-Round Video Editing", "From raw footage to final cut — color grading, transitions, sound design, everything.", "fa-solid fa-film"),
        ]
        cur.executemany(
            "INSERT INTO services (title, description, icon) VALUES (?, ?, ?)",
            default_services
        )

    conn.commit()
    conn.close()


# --------------------------------------------------------------------
# PUBLIC ROUTES
# --------------------------------------------------------------------

@app.route("/")
def home():
    conn = get_db()
    services = conn.execute("SELECT * FROM services").fetchall()
    conn.close()
    return render_template("index.html", services=services)


@app.route("/portfolio")
def portfolio():
    conn = get_db()
    services = conn.execute("SELECT * FROM services").fetchall()
    conn.close()
    return render_template("portfolio.html", services=services)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        if name and message:
            conn = get_db()
            conn.execute(
                "INSERT INTO messages (name, email, phone, message) VALUES (?, ?, ?, ?)",
                (name, email, phone, message)
            )
            conn.commit()
            conn.close()
            flash("Thanks! Your message has been sent. I'll get back to you soon.", "success")
        else:
            flash("Please fill in your name and message.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# --------------------------------------------------------------------
# ADMIN DASHBOARD (simple password-protected panel backed by SQL)
# --------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        flash("Wrong password.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    services = conn.execute("SELECT * FROM services").fetchall()
    messages = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin.html", services=services, messages=messages)


@app.route("/admin/service/add", methods=["POST"])
def add_service():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "fa-solid fa-video").strip()

    if title and description:
        conn = get_db()
        conn.execute(
            "INSERT INTO services (title, description, icon) VALUES (?, ?, ?)",
            (title, description, icon)
        )
        conn.commit()
        conn.close()
        flash("Service added.", "success")

    return redirect(url_for("admin"))


@app.route("/admin/service/delete/<int:service_id>")
def delete_service(service_id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    conn.execute("DELETE FROM services WHERE id = ?", (service_id,))
    conn.commit()
    conn.close()
    flash("Service removed.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/message/delete/<int:message_id>")
def delete_message(message_id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
