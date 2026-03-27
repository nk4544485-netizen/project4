import sqlite3
import os

def init_db():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Dummy tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS pulse_data 
                      (year INTEGER, quarter INTEGER, state TEXT, transaction_type TEXT, amount REAL, count INTEGER)''')
    conn.commit()
    conn.close()
    print("Database initialized at:", db_path)

if __name__ == "__main__":
    init_db()
