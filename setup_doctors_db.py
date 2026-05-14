import os
from db_utils import get_connection, init_db

def setup_doctors_db():
    # First ensure all tables exist
    init_db()
        
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Clear existing data for fresh seed
            cursor.execute("TRUNCATE TABLE doctors")
            cursor.execute("TRUNCATE TABLE facilities")
            
            # Seed Sample Data
            doctors_data = [
                ('Dr. Aruna Ragavan', 'Psychiatrist', 'Chennai', 'Tamil, English', 800, 'Today', 4.9, 15, 13.0827, 80.2707, ''),
                ('Dr. Suresh Kumar', 'Psychologist', 'Bangalore', 'Kannada, English', 600, 'Tomorrow', 4.7, 10, 12.9716, 77.5946, ''),
                ('Dr. Meena Iyer', 'Therapist', 'Chennai', 'Tamil, Hindi', 500, 'Today', 4.8, 8, 13.0475, 80.2089, ''),
                ('Dr. Rajesh Pillai', 'Psychiatrist', 'Kochi', 'Malayalam, English', 900, 'Today', 4.6, 20, 9.9312, 76.2673, ''),
                ('Dr. Kavitha Reddy', 'Psychologist', 'Hyderabad', 'Telugu, English', 750, 'Tomorrow', 4.9, 12, 17.3850, 78.4867, ''),
            ]
            cursor.executemany("INSERT INTO doctors (name, specialization, location, languages, fees, availability, rating, experience, latitude, longitude, image_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", doctors_data)
            
            facilities_data = [
                ('Apollo Health City', 'Hospital', 'Chennai', 13.0827, 80.2707, '044-28293333', 'Specialized mental health wing.'),
                ('NIMHANS', 'Hospital', 'Bangalore', 12.9362, 77.5910, '080-26995000', 'Top premier mental health institute.'),
                ('Serene Minds Clinic', 'Clinic', 'Chennai', 13.0475, 80.2089, '044-4567890', 'Boutique therapy center.'),
                ('Life Care Center', 'Wellness Center', 'Kochi', 9.9312, 76.2673, '0484-123456', 'Holistic mental wellness.'),
            ]
            cursor.executemany("INSERT INTO facilities (name, type, location, latitude, longitude, contact, description) VALUES (%s,%s,%s,%s,%s,%s,%s)", facilities_data)
            
            conn.commit()
            print("Doctor Database Setup Complete!")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_doctors_db()
