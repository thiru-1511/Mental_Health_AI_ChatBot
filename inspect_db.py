from db_utils import get_connection

def check_db():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Get tables
            cursor.execute("SHOW TABLES")
            tables = [list(t.values())[0] for t in cursor.fetchall()]
            print(f"Tables found: {tables}")
            
            for table in tables:
                print(f"\n--- {table} ---")
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"Col {col['Field']} ({col['Type']})")
                
                # Sample data
                cursor.execute(f"SELECT * FROM {table} LIMIT 2")
                rows = cursor.fetchall()
                print(f"Sample data: {rows}")
                
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
