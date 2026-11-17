
import sqlite3
import os
import json
from datetime import datetime, timezone

PROJECT_PATH = "/content/drive/MyDrive/Signal_Stack_AI"

DB_PATH = os.path.join(
    PROJECT_PATH,
    "data",
    "signal_stack.db"
)

def initialize_storage():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crawl_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        source_url TEXT,
        page_title TEXT,
        content TEXT,
        content_hash TEXT,
        collected_at TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_crawl(company_name, result):

    if result.get("status") != "Success":
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Avoid saving identical content twice
    cursor.execute("""
    SELECT id FROM crawl_history
    WHERE company_name = ?
    AND source_url = ?
    AND content_hash = ?
    """, (
        company_name,
        result["url"],
        result["content_hash"]
    ))

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("""
    INSERT INTO crawl_history (
        company_name,
        source_url,
        page_title,
        content,
        content_hash,
        collected_at,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        company_name,
        result["url"],
        result["title"],
        result["content"],
        result["content_hash"],
        result["collected_at"],
        result["status"]
    ))

    conn.commit()
    conn.close()

    return True


def get_crawl_history(company_name):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT source_url, page_title, collected_at, content_hash
    FROM crawl_history
    WHERE company_name = ?
    ORDER BY id DESC
    """, (company_name,))

    records = cursor.fetchall()

    conn.close()

    return records


initialize_storage()
