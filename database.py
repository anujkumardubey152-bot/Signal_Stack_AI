
import sqlite3
import hashlib

# Streamlit Cloud writable temporary database location
DB_PATH = "/tmp/signal_stack_ai.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            source TEXT,
            category TEXT,
            relevance_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            signal_hash TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def generate_signal_hash(signal):
    text = (
        str(signal.get("title", "")) + " " +
        str(signal.get("content", ""))
    ).lower().strip()

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def save_signal(signal):
    conn = get_connection()
    cursor = conn.cursor()

    signal_hash = generate_signal_hash(signal)

    try:
        cursor.execute("""
            INSERT INTO signals
            (title, content, source, category,
             relevance_score, signal_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            signal.get("title", ""),
            signal.get("content", ""),
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM signals ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# Initialize database
initialize_database()
