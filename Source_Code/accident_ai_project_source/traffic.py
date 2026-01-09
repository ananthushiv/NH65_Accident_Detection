
import os, requests, time

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_traffic_delay(origin, destination):
    if not GOOGLE_API_KEY:
        return {"error": "Set GOOGLE_MAPS_API_KEY env variable"}

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
        "delay_min": round((traffic - normal) / 60, 2)
    }
