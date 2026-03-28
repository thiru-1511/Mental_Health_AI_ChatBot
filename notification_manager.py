import sqlite3
import datetime
import os

DB_PATH = 'data/doctors.db'

class NotificationManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def schedule_notifications(self, appointment_id, user_id, appointment_date, appointment_time):
        """Schedules 1h and 1d reminders for an appointment."""
        try:
            # Parse date/time
            # Standardizing date format if needed, assuming %Y-%m-%d %H:%M
            dt_str = f"{appointment_date} {appointment_time}"
            app_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            
            reminders = [
                ('reminder_1d', app_dt - datetime.timedelta(days=1)),
                ('reminder_1h', app_dt - datetime.timedelta(hours=1))
            ]
            
            with sqlite3.connect(self.db_path) as conn:
                for r_type, send_at in reminders:
                    # Only schedule if send_at is in the future
                    if send_at > datetime.datetime.now():
                        # Default channels based on user preferences would be better, 
                        # but for now we'll schedule for App and later filter/process
                        conn.execute("""
                            INSERT INTO notifications (user_id, appointment_id, type, channel, send_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, (user_id, appointment_id, r_type, 'App', send_at))
                conn.commit()
        except Exception as e:
            print(f"Error scheduling notifications: {e}")

    def get_pending_notifications(self, user_id=None):
        """Fetches pending notifications that are due to be sent."""
        now = datetime.datetime.now()
        query = """SELECT n.*, a.date, a.time, d.name as doctor_name 
                 FROM notifications n 
                 JOIN appointments a ON n.appointment_id = a.id
                 JOIN doctors d ON a.doctor_id = d.id
                 WHERE n.status = 'Pending' AND n.send_at <= ?"""
        params = [now]
        
        if user_id:
            query += " AND n.user_id = ?"
            params.append(user_id)
            
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def mark_as_sent(self, notification_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE notifications SET status = 'Sent' WHERE id = ?", (notification_id,))
            conn.commit()

notification_manager = NotificationManager()
