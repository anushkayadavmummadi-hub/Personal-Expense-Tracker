from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        name = request.form["expense_name"]
        amount = request.form["amount"]
        category = request.form["category"]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
            (name, amount, category)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    conn.close()

    return render_template("index.html", expenses=expenses)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)