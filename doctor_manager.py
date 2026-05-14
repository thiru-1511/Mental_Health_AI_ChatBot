import math
import os
from db_utils import get_connection

class DoctorManager:
    def __init__(self):
        pass # Schema initialization is handled by db_utils.init_db()

    def get_all_doctors(self):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM doctors")
                return cursor.fetchall()
        finally:
            conn.close()

    def search_doctors(self, filters):
        """
        Search doctors based on multiple criteria:
        specialization, location, language, max_fees, availability
        """
        query = "SELECT * FROM doctors WHERE 1=1"
        params = []
        
        if filters.get('specialization'):
            query += " AND specialization = %s"
            params.append(filters['specialization'])
        
        if filters.get('location'):
            query += " AND location LIKE %s"
            params.append(f"%{filters['location']}%")
            
        if filters.get('language'):
            query += " AND languages LIKE %s"
            params.append(f"%{filters['language']}%")
            
        if filters.get('max_fees'):
            query += " AND fees <= %s"
            params.append(float(filters['max_fees']))
            
        if filters.get('availability'):
            query += " AND availability = %s"
            params.append(filters['availability'])

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def get_nearby_facilities(self, user_lat, user_lon, radius_km=50):
        """
        Returns facilities within a certain radius using Haversine formula.
        """
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM facilities")
                all_facilities = cursor.fetchall()
        finally:
            conn.close()
            
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
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO appointments (doctor_id, user_id, date, time, type) VALUES (%s, %s, %s, %s, %s)",
                    (doctor_id, user_id, date, time, session_type)
                )
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    def get_doctor_appointments(self, doctor_user_id):
        """Fetches appointments for a specialist based on their user_id."""
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # First find the doctor_id for this user_id
                cursor.execute("SELECT id FROM doctors WHERE user_id = %s", (doctor_user_id,))
                dr = cursor.fetchone()
                if not dr: return []
                dr_id = dr['id']
                
                # Now get appointments joined with patient info (from usersTable - we'll handle this join in app.py or here)
                cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s ORDER BY date DESC, time DESC", (dr_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def get_patient_appointments(self, user_id):
        """Fetches all appointments for a patient (Medical History)."""
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT a.*, d.name as doctor_name, d.specialization 
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    WHERE a.user_id = %s 
                    ORDER BY a.date DESC, a.time DESC
                """, (user_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def get_appointment_by_id(self, app_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT a.*, d.name as doctor_name, d.specialization 
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    WHERE a.id = %s
                """, (app_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    def update_appointment(self, app_id, status=None, notes=None, prescription=None):
        updates = []
        params = []
        if status:
            updates.append("status = %s")
            params.append(status)
        if notes:
            updates.append("notes = %s")
            params.append(notes)
        if prescription:
            updates.append("prescription = %s")
            params.append(prescription)
        
        if not updates: return False
        
        params.append(app_id)
        query = f"UPDATE appointments SET {', '.join(updates)} WHERE id = %s"
        
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return True
        finally:
            conn.close()

    def get_patient_mood_summary(self, patient_id):
        """Fetches recent mood history for a specialist to review."""
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                # We fetch moods matching this patient_id (assuming mood_events.user_id = patient_id, though user_id might be missing in older logs)
                # But since we just added user_id to mood_events, let's query it
                cursor.execute("""
                    SELECT emotion, timestamp 
                    FROM mood_events
                    WHERE user_id = %s OR user_id IS NULL
                    ORDER BY timestamp DESC LIMIT 50
                """, (patient_id,))
                return cursor.fetchall()
        except:
            return []
        finally:
            try:
                conn.close()
            except:
                pass

doctor_manager = DoctorManager()
