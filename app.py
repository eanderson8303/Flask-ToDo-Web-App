import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call it once when the app starts
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()

    if request.method == "POST":
        task = request.form["task"]
        c.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        conn.commit()

    # Fetch all tasks to show
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
