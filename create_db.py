import sqlite3
import os
import json
import glob

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PULSE_DIR  = os.path.join(BASE_DIR, "pulse_data", "data")
DB_PATH    = os.path.join(BASE_DIR, "data", "phonepe_pulse.db")

def slugify(name):
    """Convert folder slug like 'andhra-pradesh' → 'Andhra Pradesh'"""
    return name.replace("-", " ").title()

# ─────────────────────────────────────────────
# SETUP DB
# ─────────────────────────────────────────────
def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables(cursor):
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
    print("✅ Tables created.")

# ─────────────────────────────────────────────
# 1. AGGREGATED TRANSACTION
# ─────────────────────────────────────────────
def load_agg_transaction(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "aggregated", "transaction", "country", "india", "state", "*", "*", "*.json")
    files = glob.glob(pattern)
    for f in files:
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        tx_data = data.get("data", {}).get("transactionData", [])
        for tx in tx_data:
            name = tx.get("name", "")
            instruments = tx.get("paymentInstruments", [])
            for inst in instruments:
                if inst.get("type") == "TOTAL":
                    rows.append((year, quarter, state, name, inst.get("amount", 0), inst.get("count", 0)))
    cursor.executemany("INSERT INTO agg_transaction VALUES (?,?,?,?,?,?)", rows)
    print(f"✅ agg_transaction: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# 2. AGGREGATED USER
# ─────────────────────────────────────────────
def load_agg_user(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "aggregated", "user", "country", "india", "state", "*", "*", "*.json")
    for f in glob.glob(pattern):
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        agg = data.get("data", {}).get("aggregated", {})
        reg_users  = agg.get("registeredUsers", 0)
        app_opens  = agg.get("appOpens", 0)
        devices = data.get("data", {}).get("usersByDevice", []) or []
        if devices:
            for d in devices:
                rows.append((year, quarter, state, reg_users, app_opens,
                             d.get("brand", "Unknown"), d.get("count", 0), d.get("percentage", 0.0)))
        else:
            rows.append((year, quarter, state, reg_users, app_opens, "Unknown", 0, 0.0))
    cursor.executemany("INSERT INTO agg_user VALUES (?,?,?,?,?,?,?,?)", rows)
    print(f"✅ agg_user: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# 3. MAP TRANSACTION
# ─────────────────────────────────────────────
def load_map_transaction(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "map", "transaction", "hover", "country", "india", "state", "*", "*", "*.json")
    for f in glob.glob(pattern):
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        districts = data.get("data", {}).get("hoverDataList", []) or []
        for d in districts:
            district = d.get("name", "").replace(" district", "").title()
            for m in d.get("metric", []):
                if m.get("type") == "TOTAL":
                    rows.append((year, quarter, state, district, m.get("amount", 0), m.get("count", 0)))
    cursor.executemany("INSERT INTO map_transaction VALUES (?,?,?,?,?,?)", rows)
    print(f"✅ map_transaction: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# 4. MAP USER
# ─────────────────────────────────────────────
def load_map_user(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "map", "user", "hover", "country", "india", "state", "*", "*", "*.json")
    for f in glob.glob(pattern):
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        districts = data.get("data", {}).get("hoverData", {}) or {}
        for district_key, val in districts.items():
            district = district_key.replace(" district", "").title()
            rows.append((year, quarter, state, district,
                         val.get("registeredUsers", 0), val.get("appOpens", 0)))
    cursor.executemany("INSERT INTO map_user VALUES (?,?,?,?,?,?)", rows)
    print(f"✅ map_user: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# 5. TOP TRANSACTION
# ─────────────────────────────────────────────
def load_top_transaction(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "top", "transaction", "country", "india", "state", "*", "*", "*.json")
    for f in glob.glob(pattern):
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        entities = data.get("data", {}) or {}
        for entity_type in ["districts", "pincodes"]:
            for item in entities.get(entity_type, []) or []:
                name   = item.get("entityName", "")
                metric = item.get("metric", {}) or {}
                rows.append((year, quarter, state, entity_type.rstrip("s"),
                             name, metric.get("amount", 0), metric.get("count", 0)))
    cursor.executemany("INSERT INTO top_transaction VALUES (?,?,?,?,?,?,?)", rows)
    print(f"✅ top_transaction: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# 6. TOP USER
# ─────────────────────────────────────────────
def load_top_user(cursor):
    rows = []
    pattern = os.path.join(PULSE_DIR, "top", "user", "country", "india", "state", "*", "*", "*.json")
    for f in glob.glob(pattern):
        parts = f.replace("\\", "/").split("/")
        state   = slugify(parts[-3])
        year    = int(parts[-2])
        quarter = int(parts[-1].replace(".json", ""))
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        entities = data.get("data", {}) or {}
        for entity_type in ["districts", "pincodes"]:
            for item in entities.get(entity_type, []) or []:
                name  = item.get("name", "")
                users = item.get("registeredUsers", 0)
                rows.append((year, quarter, state, entity_type.rstrip("s"), name, users))
    cursor.executemany("INSERT INTO top_user VALUES (?,?,?,?,?,?)", rows)
    print(f"✅ top_user: {len(rows)} rows inserted.")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"📂 Pulse data directory: {PULSE_DIR}")
    print(f"💾 Database path: {DB_PATH}")
    conn   = get_conn()
    cursor = conn.cursor()

    create_tables(cursor)
    load_agg_transaction(cursor)
    load_agg_user(cursor)
    load_map_transaction(cursor)
    load_map_user(cursor)
    load_top_transaction(cursor)
    load_top_user(cursor)

    conn.commit()
    conn.close()
    print("\n🎉 All done! Database rebuilt with real PhonePe Pulse data.")
