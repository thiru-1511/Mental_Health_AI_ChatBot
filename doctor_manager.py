import sqlite3
import math
import os

DB_PATH = 'data/doctors.db'

class DoctorManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("ALTER TABLE doctors ADD COLUMN user_id INTEGER")
            except sqlite3.OperationalError:
                pass
            try:
                conn.execute("ALTER TABLE appointments ADD COLUMN type TEXT DEFAULT 'Online'")
            except sqlite3.OperationalError:
                pass
            try:
                conn.execute("ALTER TABLE appointments ADD COLUMN status TEXT DEFAULT 'Pending'")
                conn.execute("ALTER TABLE appointments ADD COLUMN notes TEXT")
                conn.execute("ALTER TABLE appointments ADD COLUMN prescription TEXT")
            except sqlite3.OperationalError:
                pass
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    appointment_id INTEGER,
                    type TEXT, 
                    channel TEXT, 
                    send_at DATETIME,
                    status TEXT DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def get_all_doctors(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM doctors")
            return [dict(row) for row in cursor.fetchall()]

    def search_doctors(self, filters):
        """
        Search doctors based on multiple criteria:
        specialization, location, language, max_fees, availability
        """
        query = "SELECT * FROM doctors WHERE 1=1"
        params = []
        
        if filters.get('specialization'):
            query += " AND specialization = ?"
            params.append(filters['specialization'])
        
        if filters.get('location'):
            query += " AND location LIKE ?"
            params.append(f"%{filters['location']}%")
            
        if filters.get('language'):
            query += " AND languages LIKE ?"
            params.append(f"%{filters['language']}%")
            
        if filters.get('max_fees'):
            query += " AND fees <= ?"
            params.append(float(filters['max_fees']))
            
        if filters.get('availability'):
            query += " AND availability = ?"
            params.append(filters['availability'])

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_nearby_facilities(self, user_lat, user_lon, radius_km=50):
        """
        Returns facilities within a certain radius using Haversine formula.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM facilities")
            all_facilities = [dict(row) for row in cursor.fetchall()]
            
        nearby = []
        for fac in all_facilities:
            dist = self._haversine(user_lat, user_lon, fac['latitude'], fac['longitude'])
            if dist <= radius_km:
                fac['distance'] = round(dist, 1)
                nearby.append(fac)
        
        return sorted(nearby, key=lambda x: x['distance'])

    def _haversine(self, lat1, lon1, lat2, lon2):
        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            return float('inf')
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def book_appointment(self, doctor_id, user_id, date, time, session_type='Online'):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO appointments (doctor_id, user_id, date, time, type) VALUES (?, ?, ?, ?, ?)",
                (doctor_id, user_id, date, time, session_type)
            )
            conn.commit()
            return cursor.lastrowid

    def get_doctor_appointments(self, doctor_user_id):
        """Fetches appointments for a specialist based on their user_id."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            # First find the doctor_id for this user_id
            cursor = conn.execute("SELECT id FROM doctors WHERE user_id = ?", (doctor_user_id,))
            dr = cursor.fetchone()
            if not dr: return []
            dr_id = dr['id']
            
            # Now get appointments joined with patient info (from usersTable - we'll handle this join in app.py or here)
            # Since users.db is separate, we'll fetch appointments first then patient details
            cursor = conn.execute("SELECT * FROM appointments WHERE doctor_id = ? ORDER BY date DESC, time DESC", (dr_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_patient_appointments(self, user_id):
        """Fetches all appointments for a patient (Medical History)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT a.*, d.name as doctor_name, d.specialization 
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.id
                WHERE a.user_id = ? 
                ORDER BY a.date DESC, a.time DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_appointment_by_id(self, app_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT a.*, d.name as doctor_name, d.specialization 
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.id
                WHERE a.id = ?
            """, (app_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_appointment(self, app_id, status=None, notes=None, prescription=None):
        updates = []
        params = []
        if status:
            updates.append("status = ?")
            params.append(status)
        if notes:
            updates.append("notes = ?")
            params.append(notes)
        if prescription:
            updates.append("prescription = ?")
            params.append(prescription)
        
        if not updates: return False
        
        params.append(app_id)
        query = f"UPDATE appointments SET {', '.join(updates)} WHERE id = ?"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, params)
            conn.commit()
            return True

    def get_patient_mood_summary(self, patient_id):
        """Fetches recent mood history for a specialist to review."""
        try:
            # Requires access to mood_history.db
            from mood_tracker import DB_PATH as MOOD_DB
            with sqlite3.connect(MOOD_DB) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT emotion, timestamp FROM moods WHERE 1=1 ORDER BY timestamp DESC LIMIT 50")
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []

doctor_manager = DoctorManager()
