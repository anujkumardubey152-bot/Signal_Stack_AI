
import sqlite3
import os

PROJECT_PATH = "/content/drive/MyDrive/Signal_Stack_AI"

DB_PATH = os.path.join(
    PROJECT_PATH, "data", "signal_stack.db"
)

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        website TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intelligence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        category TEXT,
        title TEXT,
        description TEXT,
        source_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        question TEXT,
        answer TEXT,
        is_skipped INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_answer(company_id, question, answer, is_skipped=False):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interview_answers
    (company_id, question, answer, is_skipped)
    VALUES (?, ?, ?, ?)
    """, (
        company_id,
        question,
        answer,
        int(is_skipped)
    ))

    conn.commit()
    conn.close()

def get_answers(company_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT question, answer, is_skipped
    FROM interview_answers
    WHERE company_id = ?
    ORDER BY id
    """, (company_id,))

    results = cursor.fetchall()

    conn.close()

    return results

initialize_database()
