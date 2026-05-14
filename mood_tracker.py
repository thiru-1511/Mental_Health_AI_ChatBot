from datetime import datetime
from db_utils import get_connection

class MoodTracker:
    def __init__(self):
        pass # Schema initialization is handled by db_utils.init_db()

    def log_mood(self, emotion: str, confidence: float = None,
                 source: str = "unknown", trigger_text: str = "", user_id: int = None):
        now = datetime.now()
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO mood_events (user_id, timestamp, date, emotion, confidence, source, trigger_text) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, now.isoformat(), now.strftime("%Y-%m-%d"),
                     emotion, confidence, source, trigger_text[:100] if trigger_text else "")
                )
                conn.commit()
        finally:
            conn.close()

    def _check_for_milestones(self):
        """No-op stub to prevent breaking app.py if it's still called."""
        pass

mood_tracker = MoodTracker()
