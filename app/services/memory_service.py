import sqlite3
from typing import Optional, List, Dict

DB_NAME = "chat_sessions.db"


# ==============================
# INIT DATABASE
# ==============================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        vision_context TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ==============================
# SESSION MANAGEMENT
# ==============================

def create_or_update_session(session_id: str, vision_context: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO sessions (session_id, vision_context)
        VALUES (?, ?)
    """, (session_id, vision_context))

    conn.commit()
    conn.close()


def get_session_vision(session_id: str) -> Optional[str]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vision_context FROM sessions WHERE session_id = ?
    """, (session_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None


# ==============================
# MESSAGE STORAGE
# ==============================

def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    conn.commit()
    conn.close()


def get_chat_history(session_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content, timestamp
        FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "role": r[0],
            "content": r[1],
            "timestamp": r[2]
        }
        for r in rows
    ]