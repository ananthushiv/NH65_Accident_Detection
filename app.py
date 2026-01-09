
from flask import Flask, render_template, jsonify, request
from utils.vehicle_count import get_vehicle_count, get_all_vehicle_records
from utils.ml_logic import accident_score
from traffic import get_all_toll_traffic, get_peak_hours_analysis, get_nh65_traffic_route, GOOGLE_API_KEY
from db import init_db, insert_crossing
import time

app = Flask(__name__)

# Ensure DB is initialized when app starts
init_db()

TOLLS = ["VJA_TOLL", "PANTHANGI_TOLL", "HYD_TOLL"]

@app.route("/")
def dashboard():
    return render_template("dashboard.html", tolls=TOLLS, google_api_key="AIzaSyAGVtVAbfR3juF-EIeAhLmJakbjuwrtBxQ")

@app.route("/api/live-data")
def live_data():
    try:
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
        return jsonify(data)
    except Exception as e:
        print(f"Error in live_data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/ingest', methods=['POST'])
def ingest():
    """Endpoint for data simulator to POST crossing records"""
    try:
        payload = request.json or {}
        vehicle_id = payload.get('vehicle_id')
        toll_id = payload.get('toll_id')
        timestamp = payload.get('timestamp')
        if not vehicle_id or not toll_id:
            return jsonify({'error': 'vehicle_id and toll_id required'}), 400
        insert_crossing(vehicle_id, toll_id, timestamp)
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Error in ingest: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/api/all-records")
def all_records():
    """Get all vehicle crossing records"""
    try:
        records = get_all_vehicle_records(100)
        return jsonify({
            "records": records,
            "total_count": len(records),
            "timestamp": int(time.time())
        })
    except Exception as e:
        print(f"Error in all_records: {e}")
        return jsonify({"error": str(e), "records": [], "total_count": 0}), 500

@app.route("/api/traffic-status")
def traffic_status():
    """Get live traffic information for all toll plazas"""
    try:
        traffic_data = get_all_toll_traffic()
        peak_analysis = get_peak_hours_analysis()
        return jsonify({
            "traffic": traffic_data,
            "peak_hours": peak_analysis,
            "timestamp": int(time.time())
        })
    except Exception as e:
        print(f"Error in traffic_status: {e}")
        return jsonify({"error": str(e), "traffic": [], "peak_hours": {}}), 500

@app.route("/api/nh65-route-traffic")
def nh65_route_traffic():
    """Get NH65 route traffic information"""
    try:
        route_data = get_nh65_traffic_route()
        return jsonify({
            "routes": route_data,
            "timestamp": int(time.time())
        })
    except Exception as e:
        print(f"Error in nh65_route_traffic: {e}")
        return jsonify({"error": str(e), "routes": []}), 500

if __name__ == "__main__":
    app.run(debug=True)
