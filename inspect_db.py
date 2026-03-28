import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('c:/Users/thirumalai/Downloads/AI CHATBOT/data/doctors.db')
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables found: {tables}")
        
        for table in tables:
            print(f"\n--- {table} ---")
            cursor.execute(f"PRAGMA table_info('{table}')")
            columns = cursor.fetchall()
            for col in columns:
                print(f"Col {col[1]} ({col[2]})")
            
            # Sample data
            cursor.execute(f"SELECT * FROM '{table}' LIMIT 2")
            rows = cursor.fetchall()
            print(f"Sample data: {rows}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
