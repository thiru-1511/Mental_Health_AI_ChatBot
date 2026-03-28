import sqlite3
import os

DB_PATH = 'data/doctors.db'

def setup_doctors_db():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clean recreate
    cursor.execute("DROP TABLE IF EXISTS doctors")
    cursor.execute("DROP TABLE IF EXISTS facilities")
    cursor.execute("DROP TABLE IF EXISTS appointments")
    
    # 1. Update/Create Doctors Table
    cursor.execute('''
        CREATE TABLE doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            location TEXT NOT NULL,
            languages TEXT NOT NULL,
            fees REAL NOT NULL,
            availability TEXT NOT NULL,
            rating REAL DEFAULT 5.0,
            experience INTEGER,
            latitude REAL,
            longitude REAL,
            image_url TEXT
        )
    ''')
    
    # 2. Create Facilities (Hospitals/Clinics) Table
    cursor.execute('''
        CREATE TABLE facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- Hospital, Clinic, Wellness Center
            location TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            contact TEXT,
            description TEXT
        )
    ''')
    
    # 3. Create Appointments Table
    cursor.execute('''
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            user_id INTEGER,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # Seed Sample Data
    doctors_data = [
        ('Dr. Aruna Ragavan', 'Psychiatrist', 'Chennai', 'Tamil, English', 800, 'Today', 4.9, 15, 13.0827, 80.2707, ''),
        ('Dr. Suresh Kumar', 'Psychologist', 'Bangalore', 'Kannada, English', 600, 'Tomorrow', 4.7, 10, 12.9716, 77.5946, ''),
        ('Dr. Meena Iyer', 'Therapist', 'Chennai', 'Tamil, Hindi', 500, 'Today', 4.8, 8, 13.0475, 80.2089, ''),
        ('Dr. Rajesh Pillai', 'Psychiatrist', 'Kochi', 'Malayalam, English', 900, 'Today', 4.6, 20, 9.9312, 76.2673, ''),
        ('Dr. Kavitha Reddy', 'Psychologist', 'Hyderabad', 'Telugu, English', 750, 'Tomorrow', 4.9, 12, 17.3850, 78.4867, ''),
    ]
    cursor.executemany("INSERT INTO doctors (name, specialization, location, languages, fees, availability, rating, experience, latitude, longitude, image_url) VALUES (?,?,?,?,?,?,?,?,?,?,?)", doctors_data)
    
    facilities_data = [
        ('Apollo Health City', 'Hospital', 'Chennai', 13.0827, 80.2707, '044-28293333', 'Specialized mental health wing.'),
        ('NIMHANS', 'Hospital', 'Bangalore', 12.9362, 77.5910, '080-26995000', 'Top premier mental health institute.'),
        ('Serene Minds Clinic', 'Clinic', 'Chennai', 13.0475, 80.2089, '044-4567890', 'Boutique therapy center.'),
        ('Life Care Center', 'Wellness Center', 'Kochi', 9.9312, 76.2673, '0484-123456', 'Holistic mental wellness.'),
    ]
    cursor.executemany("INSERT INTO facilities (name, type, location, latitude, longitude, contact, description) VALUES (?,?,?,?,?,?,?)", facilities_data)
    
    conn.commit()
    conn.close()
    print("Doctor Database Setup Complete!")

if __name__ == "__main__":
    setup_doctors_db()
