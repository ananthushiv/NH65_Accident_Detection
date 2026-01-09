
AI/ML Accident Detection on NH65 (Vijayawada - Hyderabad)
======================================================

This project is customized for the NH65 highway stretch between:
- Vijayawada, Andhra Pradesh
- Hyderabad, Telangana

Features:
- Toll crossing anomaly detection using ML
- Google Maps live traffic delay
- Estimated accident midpoint on NH65
- Web dashboard with delay chart

Setup:
1. Enable Google Directions API.
2. Set API key:
   Windows: set GOOGLE_MAPS_API_KEY=YOUR_KEY
   Linux/Mac: export GOOGLE_MAPS_API_KEY=YOUR_KEY

Run:
pip install -r requirements.txt
python main.py
python data_simulator.py

Open dashboard:
http://127.0.0.1:5000/

You can update exact toll plaza coordinates in location.py.
