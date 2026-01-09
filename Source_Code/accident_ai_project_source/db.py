
import sqlite3

DB = "toll.db"

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
    cur.execute("INSERT INTO crossings(vehicle_id,toll_id,timestamp) VALUES (?,?,?)",
                (vehicle_id, toll_id, timestamp))
    con.commit()
    con.close()

def get_recent_crossings(limit=500):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT vehicle_id,toll_id,timestamp FROM crossings ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows
