
"""
Signal Stack AI
SQLite database management.
Compatible with Streamlit Community Cloud.
"""

import sqlite3
import hashlib

# Writable temporary storage on Streamlit Cloud
DB_PATH = "/tmp/signal_stack_ai.db"


def get_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create the signals table if it does not exist."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                source TEXT,
                category TEXT,
                relevance_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                signal_hash TEXT UNIQUE
            )
        """)

        conn.commit()

    finally:
        conn.close()


def generate_signal_hash(signal):
    """Generate a unique hash to identify duplicate signals."""

    text = (
        str(signal.get("title", "")) + " " +
        str(signal.get("content", signal.get("description", "")))
    ).lower().strip()

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def save_signal(signal):
    """Save a signal and prevent duplicate entries."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        signal_hash = generate_signal_hash(signal)

        cursor.execute("""
            INSERT INTO signals (
                title,
                content,
                source,
                category,
                relevance_score,
                signal_hash
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            signal.get("title", ""),
            signal.get("content", signal.get("description", "")),
            signal.get("source", ""),
            signal.get("category", ""),
            signal.get("relevance_score", 0),
            signal_hash
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_all_signals():
    """Retrieve all stored signals."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM signals
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    finally:
        conn.close()


# Initialize database when this module is imported
initialize_database()
