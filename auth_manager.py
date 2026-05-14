import os
import pymysql
import werkzeug.security as security
from datetime import datetime
from db_utils import get_connection

class AuthManager:
    def __init__(self):
        pass # Schema initialization is now handled by db_utils.init_db()

    def register_user(self, username, email, password, full_name=None, age=None, gender=None, occupation=None, role='Patient'):
        """Registers a new user. Returns (success, message)."""
        password_hash = security.generate_password_hash(password)
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, full_name, age, gender, occupation, role, email_notifications, app_notifications) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, email, password_hash, full_name, age, gender, occupation, role, 1, 1)
                )
                conn.commit()
            conn.close()
            return True, "Registration successful!"
        except pymysql.err.IntegrityError:
            return False, "Username or Email already exists."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username_or_email, password):
        """Verifies credentials. Returns (user_dict or None)."""
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s OR email = %s",
                    (username_or_email, username_or_email)
                )
                user = cursor.fetchone()
                
                if user and security.check_password_hash(user['password_hash'], password):
                    return user
        finally:
            conn.close()
        return None

    def get_user_by_id(self, user_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    def update_profile(self, user_id, mental_health_history, emergency_contact_name, emergency_contact_phone):
        """Updates user profile with medical info and emergency contact."""
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    UPDATE users SET 
                    mental_health_history = %s, 
                    emergency_contact_name = %s, 
                    emergency_contact_phone = %s 
                    WHERE id = %s
                ''', (mental_health_history, emergency_contact_name, emergency_contact_phone, user_id))
                conn.commit()
            return True
        finally:
            conn.close()

    def update_full_profile(self, user_id, data):
        """Updates all profile fields including medical info."""
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    UPDATE users SET 
                    full_name = %s, 
                    age = %s, 
                    gender = %s, 
                    occupation = %s,
                    mental_health_history = %s, 
                    emergency_contact_name = %s, 
                    emergency_contact_phone = %s,
                    phone_number = %s,
                    email_notifications = %s,
                    sms_notifications = %s,
                    app_notifications = %s
                    WHERE id = %s
                ''', (
                    data.get('full_name'),
                    data.get('age'),
                    data.get('gender'),
                    data.get('occupation'),
                    data.get('mental_health_history'),
                    data.get('emergency_contact_name'),
                    data.get('emergency_contact_phone'),
                    data.get('phone_number'),
                    1 if data.get('email_notifications') else 0,
                    1 if data.get('sms_notifications') else 0,
                    1 if data.get('app_notifications') else 0,
                    user_id
                ))
                conn.commit()
            return True
        finally:
            conn.close()

auth_manager = AuthManager()
