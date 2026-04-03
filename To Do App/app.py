from flask import Flask, render_template, request, redirect
 			
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    tasks = db.execute("SELECT id, task FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            db = get_db()
            db.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            db.commit()
        return redirect("/")
    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
