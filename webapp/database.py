"""SQLite database for storing confirmed breaks and prompt history."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam.db")

ALLOWED_UPDATE_FIELDS = {
    "contextual_notes", "prompt_english", "attack_type",
    "risk_category", "risk_subcategory",
}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS breaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack_id TEXT NOT NULL UNIQUE,
            model_key TEXT NOT NULL,
            model_name TEXT NOT NULL,
            language TEXT NOT NULL,
            attack_type TEXT NOT NULL,
            risk_category TEXT NOT NULL,
            risk_subcategory TEXT NOT NULL,
            prompt_original TEXT NOT NULL,
            prompt_english TEXT DEFAULT '',
            response TEXT NOT NULL,
            contextual_notes TEXT DEFAULT '',
            break_count INTEGER DEFAULT 1,
            total_runs INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS prompt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_key TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            status TEXT NOT NULL,
            refusal_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    # Add UNIQUE constraint to existing databases (no-op if already present)
    try:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_breaks_attack_id ON breaks(attack_id)")
        conn.commit()
    except Exception:
        conn.rollback()
    conn.close()


def get_next_attack_id() -> str:
    """Generate the next attack ID atomically."""
    conn = get_connection()
    row = conn.execute("SELECT MAX(id) as max_id FROM breaks").fetchone()
    next_num = (row["max_id"] or 0) + 1
    conn.close()
    return f"A{next_num}"


def save_break(data: dict) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO breaks
           (attack_id, model_key, model_name, language, attack_type,
            risk_category, risk_subcategory, prompt_original, prompt_english,
            response, contextual_notes, break_count, total_runs)
           VALUES (:attack_id, :model_key, :model_name, :language, :attack_type,
                   :risk_category, :risk_subcategory, :prompt_original, :prompt_english,
                   :response, :contextual_notes, :break_count, :total_runs)""",
        data,
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_breaks(limit: int = 0, offset: int = 0) -> list[dict]:
    conn = get_connection()
    if limit > 0:
        rows = conn.execute(
            "SELECT * FROM breaks ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM breaks ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_break(break_id: int) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM breaks WHERE id = ?", (break_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_break(break_id: int, data: dict) -> bool:
    safe_data = {k: v for k, v in data.items() if k in ALLOWED_UPDATE_FIELDS}
    if not safe_data:
        return False
    conn = get_connection()
    fields = ", ".join(f"{k} = ?" for k in safe_data.keys())
    values = list(safe_data.values()) + [break_id]
    cursor = conn.execute(f"UPDATE breaks SET {fields} WHERE id = ?", values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_break(break_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM breaks WHERE id = ?", (break_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def save_prompt_history(data: dict) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO prompt_history (model_key, prompt, response, status, refusal_count)
           VALUES (:model_key, :prompt, :response, :status, :refusal_count)""",
        data,
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_prompt_history(limit: int = 50) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM prompt_history ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
