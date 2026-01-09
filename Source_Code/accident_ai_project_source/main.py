
from flask import Flask, jsonify, request, render_template
from db import init_db, insert_crossing, get_recent_crossings
from model import detect_accident
from traffic import get_traffic_delay
from location import estimate_location

app = Flask(__name__)
init_db()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    insert_crossing(data["vehicle_id"], data["toll_id"], data["timestamp"])
    return jsonify({"status": "ok"})

@app.route("/detect", methods=["GET"])
def detect():
    origin = request.args.get("origin", "Vijayawada Toll")
    destination = request.args.get("destination", "Hyderabad Toll")

    rows = get_recent_crossings()
    alerts = detect_accident(rows)
    traffic_info = get_traffic_delay("Vijayawada, Andhra Pradesh", "Hyderabad, Telangana")
    location = estimate_location(origin, destination)

    return jsonify({
        "alerts": alerts,
        "traffic": traffic_info,
        "location": location
    })

if __name__ == "__main__":
    app.run(debug=True)
