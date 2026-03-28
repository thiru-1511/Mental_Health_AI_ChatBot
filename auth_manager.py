import sqlite3
import os
import werkzeug.security as security
from datetime import datetime

DB_PATH = "users.db"

class AuthManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    occupation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Add new columns for doctor booking system if they don't exist
            columns = [
                ("mental_health_history", "TEXT"),
                ("emergency_contact_name", "TEXT"),
                ("emergency_contact_phone", "TEXT"),
                ("phone_number", "TEXT"),
                ("email_notifications", "INTEGER DEFAULT 1"),
                ("sms_notifications", "INTEGER DEFAULT 0"),
                ("app_notifications", "INTEGER DEFAULT 1"),
                ("role", "TEXT DEFAULT 'Patient'")
            ]
            for col_name, col_type in columns:
                try:
                    conn.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass
            conn.commit()

    def register_user(self, username, email, password, full_name=None, age=None, gender=None, occupation=None, role='Patient'):
        """Registers a new user. Returns (success, message)."""
        password_hash = security.generate_password_hash(password)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO users (username, email, password_hash, full_name, age, gender, occupation, role, email_notifications, app_notifications) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, email, password_hash, full_name, age, gender, occupation, role, 1, 1)
                )
                conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username or Email already exists."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username_or_email, password):
        """Verifies credentials. Returns (user_dict or None)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?",
                (username_or_email, username_or_email)
            )
            user = cursor.fetchone()
            
            if user and security.check_password_hash(user['password_hash'], password):
                return dict(user)
        return None

    def get_user_by_id(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None

    def update_profile(self, user_id, mental_health_history, emergency_contact_name, emergency_contact_phone):
        """Updates user profile with medical info and emergency contact."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE users SET 
                mental_health_history = ?, 
                emergency_contact_name = ?, 
                emergency_contact_phone = ? 
                WHERE id = ?
            ''', (mental_health_history, emergency_contact_name, emergency_contact_phone, user_id))
            conn.commit()
            return True

    def update_full_profile(self, user_id, data):
        """Updates all profile fields including medical info."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE users SET 
                full_name = ?, 
                age = ?, 
                gender = ?, 
                occupation = ?,
                mental_health_history = ?, 
                emergency_contact_name = ?, 
                emergency_contact_phone = ?,
                phone_number = ?,
                email_notifications = ?,
                sms_notifications = ?,
                app_notifications = ?
                WHERE id = ?
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

auth_manager = AuthManager()
