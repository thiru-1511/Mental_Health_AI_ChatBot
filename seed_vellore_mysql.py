from db_utils import get_connection

def seed_vellore_facilities():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            facilities = [
                ('CMC Vellore', 'Hospital', 'Ida Scudder Road, Vellore', 12.9250, 79.1350, '0416-2281000', 'CMC Vellore is a world-renowned tertiary care hospital.'),
                ('Government Vellore Medical College', 'Hospital', 'Adukkamparai, Vellore', 12.8710, 79.1250, '0416-2236000', 'Public medical college and hospital.'),
                ('Naruvi Hospitals', 'Hospital', 'Chennai-Bengaluru Hwy, Vellore', 12.9450, 79.1550, '0416-2323232', 'Multi-specialty private hospital.'),
                ('Vellore Psychiatric Centre', 'Clinic', 'Katpadi Road, Vellore', 12.9180, 79.1380, '0416-2223334', 'Specialized mental health and counseling.'),
                ('Arka Wellness Center', 'Clinic', 'Sathuvachari, Vellore', 12.9300, 79.1450, '0416-2255667', 'Holistic wellness and psychiatric support.')
            ]
            
            for fac in facilities:
                cursor.execute("SELECT id FROM facilities WHERE name = %s", (fac[0],))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO facilities (name, type, location, latitude, longitude, contact, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", fac)
                    
            conn.commit()
            print("Vellore medical facilities added successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_vellore_facilities()
