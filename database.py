import sqlite3

conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
date TEXT,
category TEXT,
amount REAL,
description TEXT
)
""")

conn.commit()


def create_user(username,password):

    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )
        conn.commit()
        return True

    except:
        return False


def login_user(username,password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    return cursor.fetchone()


def add_expense(username,date,category,amount,description):

    cursor.execute(
        "INSERT INTO expenses(username,date,category,amount,description) VALUES(?,?,?,?,?)",
        (username,str(date),category,amount,description)
    )

    conn.commit()


def get_expenses(username):

    cursor.execute(
        "SELECT date,category,amount,description FROM expenses WHERE username=?",
        (username,)
    )

    return cursor.fetchall()


def reset_user_data(username):

    cursor.execute(
        "DELETE FROM expenses WHERE username=?",
        (username,)
    )

    conn.commit()