import sqlite3
import os

def init_db():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create aggregated_transaction
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        year INTEGER, 
        quarter INTEGER, 
        state TEXT, 
        transaction_type TEXT, 
        amount REAL, 
        count INTEGER
    )''')
    
    # 2. Create aggregated_user
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aggregated_user (
        year INTEGER, 
        quarter INTEGER, 
        state TEXT, 
        brand TEXT, 
        registered_users INTEGER, 
        app_opens INTEGER,
        count INTEGER
    )''')
    
    # Check if data exists in aggregated_transaction, if not insert dummy telemetry
    cursor.execute("SELECT COUNT(*) FROM aggregated_transaction")
    if cursor.fetchone()[0] == 0:
        tx_data = [
            (2023, 1, 'Maharashtra', 'Peer-to-peer payments', 15000000.5, 500000),
            (2023, 1, 'Maharashtra', 'Merchant payments', 20000000.0, 600000),
            (2023, 2, 'Karnataka', 'Recharge & bill payments', 18000000.0, 550000),
            (2023, 3, 'Tamil Nadu', 'Financial Services', 12000000.0, 400000),
            (2023, 4, 'Delhi', 'Peer-to-peer payments', 25000000.0, 800000),
        ]
        cursor.executemany("INSERT INTO aggregated_transaction VALUES (?, ?, ?, ?, ?, ?)", tx_data)
        
    # Check if data exists in aggregated_user, if not insert dummy telemetry
    cursor.execute("SELECT COUNT(*) FROM aggregated_user")
    if cursor.fetchone()[0] == 0:
        user_data = [
            (2023, 1, 'Maharashtra', 'Xiaomi', 5000000, 15000000, 200000),
            (2023, 2, 'Karnataka', 'Samsung', 4000000, 12000000, 150000),
            (2023, 3, 'Tamil Nadu', 'Vivo', 3000000, 9000000, 100000),
            (2023, 4, 'Delhi', 'Apple', 2000000, 6000000, 50000),
        ]
        cursor.executemany("INSERT INTO aggregated_user VALUES (?, ?, ?, ?, ?, ?, ?)", user_data)

    conn.commit()
    conn.close()
    print("Database properly rebuilt with exact 'aggregated_transaction' and 'aggregated_user' tables!")

if __name__ == "__main__":
    init_db()
