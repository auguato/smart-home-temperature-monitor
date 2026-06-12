"""
storage.py
Stores sensor readings in a local SQLite database.
Also provides query helpers for the dashboard.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "readings.db")


def init_db():
    """Create the readings table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            temperature REAL    NOT NULL,
            humidity    REAL    NOT NULL,
            sensor      TEXT    DEFAULT 'DHT22-SIM'
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database ready at {DB_PATH}")


def save_reading(reading: dict):
    """Insert a single sensor reading into the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO readings (timestamp, temperature, humidity, sensor) VALUES (?, ?, ?, ?)",
        (reading["timestamp"], reading["temperature_c"],
         reading["humidity_pct"], reading["sensor"])
    )
    conn.commit()
    conn.close()


def get_recent(limit: int = 50) -> list:
    """Return the most recent N readings as a list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats() -> dict:
    """Return min, max, and average temperature from all stored readings."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT MIN(temperature), MAX(temperature), AVG(temperature) FROM readings"
    ).fetchone()
    conn.close()
    return {
        "min_temp": round(row[0] or 0, 2),
        "max_temp": round(row[1] or 0, 2),
        "avg_temp": round(row[2] or 0, 2)
    }


if __name__ == "__main__":
    init_db()
    stats = get_stats()
    print("Current stats:", stats)
    recent = get_recent(5)
    print("Last 5 readings:")
    for r in recent:
        print(" ", r)
