import sqlite3
import os

DB_PATH = 'data/doctors.db'

def add_more_doctors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # New doctors to add matching: name, specialization, location, languages, fees, availability, rating, experience, latitude, longitude, image_url, user_id
    new_doctors = [
        # Psychiatrists
        ("Dr. Karthik Raj", "Psychiatrist", "Chennai, TN", "English, Tamil, Hindi", 1200, "Mon-Fri (10AM - 6PM)", 4.8, 15, 13.0827, 80.2707, "https://api.dicebear.com/7.x/avataaars/svg?seed=Karthik", 10),
        ("Dr. Sarah Cherian", "Psychiatrist", "Vellore, TN", "English, Tamil, Malayalam", 800, "Mon-Sat (9AM - 2PM)", 4.6, 8, 12.9165, 79.1325, "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah", 11),
        ("Dr. Rajesh Kumar", "Psychiatrist", "Bangalore, KA", "English, Hindi, Kannada", 1500, "Tue-Sun (11AM - 8PM)", 4.9, 22, 12.9716, 77.5946, "https://api.dicebear.com/7.x/avataaars/svg?seed=Rajesh", 12),
        
        # Psychologists / Therapists
        ("Ms. Divya N", "Clinical Psychologist", "Vaniyambadi, TN", "English, Tamil, Urdu", 1000, "Mon-Fri (4PM - 9PM)", 4.7, 6, 12.6822, 78.6231, "https://api.dicebear.com/7.x/avataaars/svg?seed=Divya", 13),
        ("Mr. Anbarasan V", "Therapist", "Krishnagiri, TN", "Tamil, English", 500, "Weekends (10AM - 8PM)", 4.5, 4, 12.5186, 78.2137, "https://api.dicebear.com/7.x/avataaars/svg?seed=Anbu", 14),
        ("Ms. Lakshmi Menon", "Cognitive Behavioral Therapist", "Chennai, TN", "English, Tamil, Malayalam", 1500, "Mon-Wed-Fri (10AM - 5PM)", 4.9, 12, 13.0827, 80.2707, "https://api.dicebear.com/7.x/avataaars/svg?seed=Lakshmi", 15),
        
        # General Counselors
        ("Ms. Priya S", "Counselor", "Vellore, TN", "English, Tamil", 400, "Mon-Sat (10AM - 6PM)", 4.4, 3, 12.9165, 79.1325, "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya", 16),
        ("Dr. Vikram Singh", "De-addiction Specialist", "Bangalore, KA", "English, Hindi, Kannada", 1200, "Mon-Fri (10AM - 4PM)", 4.8, 18, 12.9716, 77.5946, "https://api.dicebear.com/7.x/avataaars/svg?seed=Vikram", 17),
        ("Ms. Fathima Z", "Child Psychologist", "Vaniyambadi, TN", "English, Tamil, Urdu", 900, "Tue-Sat (2PM - 7PM)", 4.8, 9, 12.6822, 78.6231, "https://api.dicebear.com/7.x/avataaars/svg?seed=Fathima", 18)
    ]
    
    count = 0
    for doc in new_doctors:
        # Check if doctor already exists
        cursor.execute("SELECT id FROM doctors WHERE name = ?", (doc[0],))
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO doctors 
            (name, specialization, location, languages, fees, availability, rating, experience, latitude, longitude, image_url, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', doc)
            count += 1
            
    conn.commit()
    conn.close()
    
    print(f"Successfully added {count} new doctors to the database.")

if __name__ == "__main__":
    add_more_doctors()
