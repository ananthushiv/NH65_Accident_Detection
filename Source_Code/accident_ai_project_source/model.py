
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_accident(rows):
    if len(rows) < 20:
        return []

    times = {}
    for v, t, ts in rows:
        times.setdefault(v, []).append(ts)

    travel_times = []
    for v in times:
        if len(times[v]) >= 2:
            tt = abs(times[v][0] - times[v][1])
            travel_times.append(tt)

    if not travel_times:
        return []

    X = np.array(travel_times).reshape(-1, 1)
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X)
    preds = clf.predict(X)

    alerts = []
    for i, p in enumerate(preds):
        if p == -1:
            alerts.append({
                "id": i,
                "suspected_delay_sec": int(travel_times[i]),
                "message": "Abnormal delay detected on NH65"
            })
    return alerts
