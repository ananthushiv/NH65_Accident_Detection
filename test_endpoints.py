import json
import time

# Simulate what the API should return
from utils.vehicle_count import get_vehicle_count, get_all_vehicle_records
from traffic import get_all_toll_traffic, get_peak_hours_analysis
from utils.ml_logic import accident_score

TOLLS = ["VJA_TOLL", "PANTHANGI_TOLL", "HYD_TOLL"]

# Test live-data endpoint
print("=== /api/live-data should return ===")
data = []
ts = int(time.time())
for t in TOLLS:
    count = get_vehicle_count(t)
    status = accident_score(count, delay=1)
    data.append({
        "toll": t,
        "count": count,
        "status": status,
        "time": ts
    })
print(json.dumps(data, indent=2))

# Test all-records endpoint
print("\n=== /api/all-records should return (first 3 records) ===")
records = get_all_vehicle_records(100)
print(f"Total records retrieved: {len(records)}")
if records:
    print(json.dumps(records[:3], indent=2))

# Test traffic-status endpoint
print("\n=== /api/traffic-status should return ===")
traffic_data = get_all_toll_traffic()
peak_analysis = get_peak_hours_analysis()
result = {
    "traffic": traffic_data,
    "peak_hours": peak_analysis,
    "timestamp": int(time.time())
}
print(json.dumps(result, indent=2))
