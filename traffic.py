import sqlite3
import time
import requests
from datetime import datetime, timedelta

DB = "database.db"
GOOGLE_API_KEY = "AIzaSyAGVtVAbfR3juF-EIeAhLmJakbjuwrtBxQ"

def get_traffic_status(toll_id):
    """
    Determine traffic status based on vehicle count
    Returns: status, density (as percentage)
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Get vehicle count in last 60 minutes
    now = int(time.time())
    start_time = now - (60 * 60)
    
    cur.execute(
        "SELECT COUNT(*) FROM crossings WHERE toll_id=? AND timestamp >= ?",
        (toll_id, start_time)
    )
    result = cur.fetchone()
    count = result[0] if result else 0
    conn.close()
    
    # Determine traffic status
    if count < 10:
        status = "Light"
        density = (count / 10) * 100
    elif count < 30:
        status = "Moderate"
        density = (count / 30) * 100
    elif count < 60:
        status = "Heavy"
        density = (count / 60) * 100
    else:
        status = "Congested"
        density = min(100, (count / 60) * 100)
    
    return {
        "status": status,
        "density": round(density, 2),
        "vehicle_count": count,
        "toll_id": toll_id
    }

def get_all_toll_traffic():
    """Get traffic status for all toll plazas"""
    toll_stations = ["VJA_TOLL", "HYD_TOLL", "SEC_TOLL", "NH65_TOLL", "NH16_TOLL"]
    traffic_data = []
    
    for toll in toll_stations:
        traffic_data.append(get_traffic_status(toll))
    
    return traffic_data

def get_peak_hours_analysis():
    """Analyze peak hours from historical data"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Get average vehicles per hour for the last 24 hours
    now = int(time.time())
    start_time = now - (24 * 60 * 60)
    
    cur.execute(
        """
        SELECT 
            COUNT(*) as hourly_count
        FROM crossings 
        WHERE timestamp >= ?
        """,
        (start_time,)
    )
    result = cur.fetchone()
    total_vehicles = result[0] if result else 0
    conn.close()
    
    avg_hourly = total_vehicles / 24 if total_vehicles > 0 else 0
    
    return {
        "total_vehicles_24h": total_vehicles,
        "avg_hourly": round(avg_hourly, 2),
        "peak_status": "High" if avg_hourly > 20 else "Moderate" if avg_hourly > 10 else "Low"
    }

def get_traffic_delay(origin, destination):
    """Get real-time traffic information using Google Maps API"""
    if not GOOGLE_API_KEY:
        return {"error": "Google Maps API key not set"}

    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_time": int(time.time()),
            "traffic_model": "best_guess",
            "key": GOOGLE_API_KEY
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if data.get("status") != "OK":
            return {"error": data.get("status")}

        leg = data["routes"][0]["legs"][0]
        normal = leg["duration"]["value"]
        traffic = leg.get("duration_in_traffic", {}).get("value", normal)

        return {
            "origin": origin,
            "destination": destination,
            "distance_km": round(leg["distance"]["value"] / 1000, 2),
            "normal_time_min": round(normal / 60, 2),
            "traffic_time_min": round(traffic / 60, 2),
            "delay_min": round((traffic - normal) / 60, 2),
            "polyline": data["routes"][0].get("overview_polyline", {}).get("points", ""),
            "status": "OK"
        }
    except Exception as e:
        return {"error": str(e)}

def get_nh65_traffic_route():
    """Get specific NH65 route traffic information (Vijayawada to Hyderabad)"""
    # Approximate coordinates for NH65 locations
    routes = [
        {
            "name": "Vijayawada to Hyderabad",
            "origin": "Vijayawada, Andhra Pradesh, India",
            "destination": "Hyderabad, Telangana, India",
            "center": {"lat": 16.5, "lng": 79.5}
        }
    ]
    
    result = []
    for route in routes:
        traffic_info = get_traffic_delay(route["origin"], route["destination"])
        traffic_info["route_name"] = route["name"]
        traffic_info["center"] = route["center"]
        result.append(traffic_info)
    
    return result
