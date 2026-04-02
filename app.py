import os
import sqlite3
from flask import Flask, request, redirect, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"

DATABASE = "log.db"

# ====== SET YOUR PASSWORD HERE (for now) ======
RAW_PASSWORD = os.environ.get("LOG_PASSWORD", "devpassword")
PASSWORD_HASH = generate_password_hash(RAW_PASSWORD)
# ==============================================


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            count INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def require_login():
    if not session.get("logged_in"):
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]

        if check_password_hash(PASSWORD_HASH, password):
            session["logged_in"] = True
            return redirect("/")
        else:
            return "Wrong password"

    return """
    <h2>Login</h2>
    <form method="POST">
        <input type="password" name="password" placeholder="Enter password">
        <button type="submit">Login</button>
    </form>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect("/login")

    return """
    <h1>Log Dashboard</h1>
    <a href="/add_log">Add Log</a><br>
    <a href="/view_logs">View Logs</a><br>
    <a href="/add_habit">Add Habit</a><br>
    <a href="/habit_summary">Habit Summary</a><br>
    <a href="/logout">Logout</a>
    """


@app.route("/add_log", methods=["GET", "POST"])
def add_log():
    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        content = request.form["content"]
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO logs (content, timestamp) VALUES (?, ?)", (content, timestamp))
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Add Log</h2>
    <form method="POST">
        <input type="text" name="content" placeholder="Write something...">
        <button type="submit">Save</button>
    </form>
    """


@app.route("/view_logs")
def view_logs():
    if not session.get("logged_in"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, content, timestamp FROM logs ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()

    output = "<h2>Your Logs</h2>"
    for log in logs:
        output += f"{log[2]} - {log[1]}<br>"

    output += "<br><a href='/'>Back</a>"
    return output


@app.route("/add_habit", methods=["GET", "POST"])
def add_habit():
    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"].lower()
        count = int(request.form.get("count", 1))
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO habits (name, count, timestamp) VALUES (?, ?, ?)", (name, count, timestamp))
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Add Habit</h2>
    <form method="POST">
        <input type="text" name="name" placeholder="Habit name">
        <input type="number" name="count" value="1">
        <button type="submit">Save</button>
    </form>
    """


@app.route("/habit_summary")
def habit_summary():
    if not session.get("logged_in"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT name, count FROM habits")
    rows = c.fetchall()
    conn.close()

    summary = {}
    for name, count in rows:
        summary[name] = summary.get(name, 0) + count

    output = "<h2>Habit Summary</h2>"
    for habit, total in summary.items():
        output += f"{habit} → {total}<br>"

    output += "<br><a href='/'>Back</a>"
    return output

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)