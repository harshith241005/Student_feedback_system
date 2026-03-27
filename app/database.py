import sqlite3
from pathlib import Path
from typing import Iterable


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_feedback(db_path: str, student_name: str, message: str) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO feedback (student_name, message) VALUES (?, ?)",
            (student_name.strip(), message.strip()),
        )
        conn.commit()


def list_feedback(db_path: str, limit: int | None = None) -> Iterable[sqlite3.Row]:
    query = "SELECT id, student_name, message, created_at FROM feedback ORDER BY created_at DESC"
    params = []

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    with get_connection(db_path) as conn:
        return conn.execute(query, params).fetchall()
