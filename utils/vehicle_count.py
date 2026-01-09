
import sqlite3
from datetime import datetime, timedelta
import time

def get_vehicle_count(toll_id, minutes=1440):
    """
    Get vehicle count for a toll station
    minutes parameter now defaults to 1440 (24 hours) to capture all data
    """
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    # Calculate time range in seconds (since we store timestamps as integers)
    now = int(time.time())
    start_time = now - (minutes * 60)
    
    cur.execute(
        "SELECT COUNT(*) FROM crossings WHERE toll_id=? AND timestamp >= ?",
        (toll_id, start_time)
    )
    result = cur.fetchone()
    count = result[0] if result else 0
    conn.close()
    return count

def get_all_vehicle_records(limit=100):
    """
    Get all vehicle crossing records
    """
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute(
        "SELECT vehicle_id, toll_id, timestamp FROM crossings ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    records = cur.fetchall()
    conn.close()
    
    return [
        {
            "vehicle_id": r[0],
            "toll_id": r[1],
            "timestamp": r[2]
        }
        for r in records
    ]
