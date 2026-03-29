import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "phonepe_pulse.db")

def create_mock_db():
    data_dir = os.path.join(BASE_DIR, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript("""
        DROP TABLE IF EXISTS agg_transaction;
        DROP TABLE IF EXISTS agg_user;
        DROP TABLE IF EXISTS map_transaction;
        DROP TABLE IF EXISTS map_user;
        DROP TABLE IF EXISTS top_transaction;
        DROP TABLE IF EXISTS top_user;

        CREATE TABLE agg_transaction (
            year INTEGER, quarter INTEGER, state TEXT,
            transaction_type TEXT, amount REAL, count INTEGER
        );
        CREATE TABLE agg_user (
            year INTEGER, quarter INTEGER, state TEXT,
            registered_users INTEGER, app_opens INTEGER,
            brand TEXT, brand_count INTEGER, brand_pct REAL
        );
        CREATE TABLE map_transaction (
            year INTEGER, quarter INTEGER, state TEXT,
            district TEXT, amount REAL, count INTEGER
        );
        CREATE TABLE map_user (
            year INTEGER, quarter INTEGER, state TEXT,
            district TEXT, registered_users INTEGER, app_opens INTEGER
        );
        CREATE TABLE top_transaction (
            year INTEGER, quarter INTEGER, state TEXT,
            entity_type TEXT, entity_name TEXT, amount REAL, count INTEGER
        );
        CREATE TABLE top_user (
            year INTEGER, quarter INTEGER, state TEXT,
            entity_type TEXT, entity_name TEXT, registered_users INTEGER
        );
    """)

    states = ["Andaman & Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", 
              "Chandigarh", "Chhattisgarh", "Dadra & Nagar Haveli & Daman & Diu", "Delhi", "Goa", 
              "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand", "Karnataka", 
              "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", 
              "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", 
              "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
    
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    quarters = [1, 2, 3, 4]
    tx_types = ["Peer-to-peer payments", "Merchant payments", "Recharge & bill payments", "Financial Services", "Others"]
    brands = ["Xiaomi", "Samsung", "Vivo", "Oppo", "Realme", "Apple", "Others"]

    # 1. agg_transaction
    tx_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                for txtype in tx_types:
                    count = random.randint(10000, 1000000)
                    amount = count * random.uniform(500, 1500)
                    tx_rows.append((year, q, state, txtype, amount, count))
    cursor.executemany("INSERT INTO agg_transaction VALUES (?,?,?,?,?,?)", tx_rows)

    # 2. agg_user
    user_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                reg_users = random.randint(50000, 10000000)
                app_opens = reg_users * random.randint(5, 50)
                for brand in brands:
                    brand_count = int(reg_users * random.uniform(0.01, 0.3))
                    user_rows.append((year, q, state, reg_users, app_opens, brand, brand_count, 0.0))
    cursor.executemany("INSERT INTO agg_user VALUES (?,?,?,?,?,?,?,?)", user_rows)

    # 3. map_transaction
    map_tx_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                for d in range(1, 4):
                    district = f"{state} District {d}"
                    count = random.randint(1000, 50000)
                    amount = count * random.uniform(500, 1500)
                    map_tx_rows.append((year, q, state, district, amount, count))
    cursor.executemany("INSERT INTO map_transaction VALUES (?,?,?,?,?,?)", map_tx_rows)

    # 4. map_user
    map_user_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                for d in range(1, 4):
                    district = f"{state} District {d}"
                    reg_users = random.randint(10000, 500000)
                    app_opens = reg_users * random.randint(5, 50)
                    map_user_rows.append((year, q, state, district, reg_users, app_opens))
    cursor.executemany("INSERT INTO map_user VALUES (?,?,?,?,?,?)", map_user_rows)

    # 5. top_transaction
    top_tx_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                for entity in ["district", "pincode"]:
                    for i in range(1, 6):
                        name = f"{entity}_{i}"
                        count = random.randint(1000, 50000)
                        amount = count * random.uniform(500, 1500)
                        top_tx_rows.append((year, q, state, entity, name, amount, count))
    cursor.executemany("INSERT INTO top_transaction VALUES (?,?,?,?,?,?,?)", top_tx_rows)

    # 6. top_user
    top_user_rows = []
    for year in years:
        for q in quarters:
            for state in states:
                for entity in ["district", "pincode"]:
                    for i in range(1, 6):
                        name = f"{entity}_{i}"
                        reg_users = random.randint(10000, 500000)
                        top_user_rows.append((year, q, state, entity, name, reg_users))
    cursor.executemany("INSERT INTO top_user VALUES (?,?,?,?,?,?)", top_user_rows)

    conn.commit()
    conn.close()
    print("✅ Mock database created successfully with representative data!")

if __name__ == "__main__":
    create_mock_db()
