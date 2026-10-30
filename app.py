from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)
DB = "/data/tasks.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    return conn

HTML = """
<h1>My Task Manager</h1>
<form method="POST" action="/add">
    <input type="text" name="task" placeholder="Enter a task" required>
    <button type="submit">Add Task</button>
</form>
<ul>
{% for task in tasks %}
    <li>{{ task[1] }}</li>
{% endfor %}
</ul>
"""

@app.route("/")
def home():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        conn = get_db()
        conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
