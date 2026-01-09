
import requests, time, random

URL = "http://127.0.0.1:5000/ingest"
tolls = ["Vijayawada Toll", "Hyderabad Toll"]

while True:
    vid = f"APTS{random.randint(1000,9999)}"
    ts = int(time.time()) + random.randint(0, 300)
    data = {"vehicle_id": vid, "toll_id": random.choice(tolls), "timestamp": ts}
    try:
        requests.post(URL, json=data, timeout=2)
    except:
        pass
    time.sleep(1)
