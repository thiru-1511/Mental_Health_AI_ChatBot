import sqlite3
import json
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "mood_history.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mood_events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                emotion     TEXT    NOT NULL,
                confidence  REAL,
                source      TEXT,       -- 'image', 'voice', 'text', 'fused'
                trigger_text TEXT       -- first ~100 chars of user message
            )
        """)
        conn.commit()

# Initialise on import
init_db()

class MoodTracker:
    def log_mood(self, emotion: str, confidence: float = None,
                 source: str = "unknown", trigger_text: str = ""):
        now = datetime.now()
        with get_db() as conn:
            conn.execute(
                "INSERT INTO mood_events (timestamp, date, emotion, confidence, source, trigger_text) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (now.isoformat(), now.strftime("%Y-%m-%d"),
                 emotion, confidence, source, trigger_text[:100])
            )
            conn.commit()

    def _check_for_milestones(self):
        """No-op stub to prevent breaking app.py if it's still called."""
        pass

mood_tracker = MoodTracker()
