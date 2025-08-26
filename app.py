from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)

DB_PATH = os.path.join(app.instance_path, "bbs.db")
os.makedirs(app.instance_path, exist_ok=True)

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username") or "anon"
        message = request.form.get("message", "").strip()
        if message:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO posts (username, message, timestamp) VALUES (?, ?, ?)",
                      (username, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
        return redirect(url_for("index"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
