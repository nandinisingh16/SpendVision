import sqlite3
from datetime import datetime

conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
""")
conn.commit()

def add_expense(amount, category, description, date):
    c.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (amount, category, description, date)
    )
    conn.commit()

def get_expenses():
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    return c.fetchall()

def get_total_spent():
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]
    return total if total else 0

def get_category_summary():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    return c.fetchall()

def backup_database():
    with open("expenses.db", "rb") as f:
        return f.read()
