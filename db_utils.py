import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# MySQL configuration from environment variables or defaults
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
DB_NAME = os.getenv('MYSQL_DATABASE', 'chatbot_db')
DB_PORT = int(os.getenv('MYSQL_PORT', '3306'))

def get_connection():
    """
    Returns a PyMySQL connection object.
    It automatically creates the database if it does not exist.
    """
    # First, connect without a specific database to ensure it exists
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

    # Now return the actual connection to the database
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    """
    Initialize all necessary tables in the MySQL database.
    This replaces the individual SQLite initialization scripts.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    age INT,
                    gender VARCHAR(50),
                    occupation VARCHAR(255),
                    mental_health_history TEXT,
                    emergency_contact_name VARCHAR(255),
                    emergency_contact_phone VARCHAR(50),
                    phone_number VARCHAR(50),
                    email_notifications BOOLEAN DEFAULT TRUE,
                    sms_notifications BOOLEAN DEFAULT FALSE,
                    app_notifications BOOLEAN DEFAULT TRUE,
                    role VARCHAR(50) DEFAULT 'Patient',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Mood Events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    timestamp VARCHAR(50) NOT NULL,
                    date VARCHAR(20) NOT NULL,
                    emotion VARCHAR(50) NOT NULL,
                    confidence FLOAT,
                    source VARCHAR(50),
                    trigger_text TEXT
                )
            ''')
            
            # Doctors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(255),
                    specialization VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    languages VARCHAR(255),
                    fees FLOAT,
                    availability VARCHAR(50),
                    rating FLOAT DEFAULT 5.0,
                    experience INT DEFAULT 0,
                    latitude FLOAT,
                    longitude FLOAT,
                    image_url TEXT,
                    status VARCHAR(50) DEFAULT 'offline',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    date VARCHAR(20) NOT NULL,
                    time VARCHAR(20) NOT NULL,
                    type VARCHAR(50) DEFAULT 'Online',
                    status VARCHAR(50) DEFAULT 'Pending',
                    notes TEXT,
                    prescription TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sender VARCHAR(255) NOT NULL,
                    receiver VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Notifications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    appointment_id INT,
                    type VARCHAR(50),
                    channel VARCHAR(50),
                    send_at DATETIME,
                    status VARCHAR(50) DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Medical Records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_username VARCHAR(255) NOT NULL,
                    record_type VARCHAR(100) NOT NULL,
                    description TEXT,
                    date VARCHAR(20) NOT NULL,
                    doctor_username VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Facilities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facilities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    type VARCHAR(100),
                    location VARCHAR(255),
                    latitude FLOAT,
                    longitude FLOAT,
                    contact VARCHAR(100),
                    description TEXT
                )
            ''')
            
        conn.commit()
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
