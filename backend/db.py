# backend/db.py
import sqlite3

DB_PATH = "potd.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        last_seen TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        platform TEXT,
        time TEXT,
        repeat TEXT,
        enabled INTEGER,
        last_executed TEXT,
        FOREIGN KEY(user_email) REFERENCES users(email)
    )
    """)

    conn.commit()
    conn.close()
