import datetime
import os
from db_utils import get_connection

class NotificationManager:
    def __init__(self):
        pass # Schema initialization handled by db_utils.init_db()

    def schedule_notifications(self, appointment_id, user_id, appointment_date, appointment_time):
        """Schedules 1h and 1d reminders for an appointment."""
        try:
            # Parse date/time
            dt_str = f"{appointment_date} {appointment_time}"
            app_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            
            reminders = [
                ('reminder_1d', app_dt - datetime.timedelta(days=1)),
                ('reminder_1h', app_dt - datetime.timedelta(hours=1))
            ]
            
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    for r_type, send_at in reminders:
                        # Only schedule if send_at is in the future
                        if send_at > datetime.datetime.now():
                            cursor.execute("""
                                INSERT INTO notifications (user_id, appointment_id, type, channel, send_at)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (user_id, appointment_id, r_type, 'App', send_at))
                    conn.commit()
            finally:
                conn.close()
        except Exception as e:
            print(f"Error scheduling notifications: {e}")

    def get_pending_notifications(self, user_id=None):
        """Fetches pending notifications that are due to be sent."""
        now = datetime.datetime.now()
        query = """SELECT n.*, a.date, a.time, d.name as doctor_name 
                 FROM notifications n 
                 JOIN appointments a ON n.appointment_id = a.id
                 JOIN doctors d ON a.doctor_id = d.id
                 WHERE n.status = 'Pending' AND n.send_at <= %s"""
        params = [now]
        
        if user_id:
            query += " AND n.user_id = %s"
            params.append(user_id)
            
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def mark_as_sent(self, notification_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE notifications SET status = 'Sent' WHERE id = %s", (notification_id,))
                conn.commit()
        finally:
            conn.close()

notification_manager = NotificationManager()
