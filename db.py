
import sqlite3
import time

DB = "database.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crossings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT,
            toll_id TEXT,
            timestamp INTEGER
        )
    """)
    con.commit()
    con.close()

def insert_crossing(vehicle_id, toll_id, timestamp):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # Ensure timestamp is stored as integer
    try:
        ts = int(timestamp)
    except Exception:
        ts = int(time.time())

    cur.execute(
        "INSERT INTO crossings (vehicle_id, toll_id, timestamp) VALUES (?, ?, ?)",
        (vehicle_id, toll_id, ts)
    )
    con.commit()
    con.close()

def get_recent_crossings(limit=500):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT vehicle_id,toll_id,timestamp FROM crossings ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows

def insert_random_records(count=10):
    """Insert random crossing records into the database (utility)"""
    import random
    from datetime import datetime

    vehicle_prefixes = ["AP", "TS", "KA", "TG", "MH"]
    toll_stations = ["VJA_TOLL", "HYD_TOLL", "SEC_TOLL", "NH65_TOLL", "NH16_TOLL"]

    con = sqlite3.connect(DB)
    cur = con.cursor()

    for _ in range(count):
        vehicle_id = f"{random.choice(vehicle_prefixes)}09AB{random.randint(1000, 9999)}"
        toll_id = random.choice(toll_stations)
        timestamp = int(datetime.now().timestamp())

        cur.execute(
            "INSERT INTO crossings (vehicle_id, toll_id, timestamp) VALUES (?, ?, ?)",
            (vehicle_id, toll_id, timestamp)
        )

    con.commit()
    con.close()
    print(f"Successfully inserted {count} random records")