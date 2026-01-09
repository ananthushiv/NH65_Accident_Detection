
# Accident location estimator for Vijayawada - Hyderabad NH65

TOLL_COORDS = {
    "Vijayawada Toll": (16.5062, 80.6480),   # Vijayawada
    "Hyderabad Toll": (17.3850, 78.4867),   # Hyderabad
}

def estimate_location(origin, destination):
    if origin not in TOLL_COORDS or destination not in TOLL_COORDS:
        return {"error": "Coordinates not found for tolls"}

    lat1, lon1 = TOLL_COORDS[origin]
    lat2, lon2 = TOLL_COORDS[destination]

    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2

    return {
        "lat": round(mid_lat, 6),
        "lon": round(mid_lon, 6),
        "description": "Estimated accident point on NH65 between Vijayawada and Hyderabad"
    }
