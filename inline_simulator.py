import requests
import time
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--rate', type=float, default=15.0, help='posts per minute')
parser.add_argument('--duration', type=int, default=0, help='duration in seconds (0 = indefinite)')
args = parser.parse_args()

URL = "http://127.0.0.1:5000/ingest"
TOLLS = ["VJA_TOLL", "PANTHANGI_TOLL", "HYD_TOLL", "SEC_TOLL", "NH65_TOLL", "NH16_TOLL"]
interval = 60.0 / max(0.1, args.rate)

start = time.time()
count = 0
print(f"Starting inline simulator: {args.rate} posts/min ({interval:.2f}s interval)")
try:
    while True:
        vid = f"SIM{random.randint(1000,9999)}"
        toll = random.choice(TOLLS)
        ts = int(time.time())
        payload = {"vehicle_id": vid, "toll_id": toll, "timestamp": ts}
        try:
            requests.post(URL, json=payload, timeout=2)
            count += 1
            if count % 10 == 0:
                print(f"Posted {count} records. Last: {payload}")
        except Exception as e:
            print('post error', e)
        if args.duration > 0 and (time.time() - start) > args.duration:
            break
        time.sleep(interval)
except KeyboardInterrupt:
    print('Simulator stopped by user')

print('Simulator exiting')
