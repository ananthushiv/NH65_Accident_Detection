
def accident_score(vehicle_count, delay=0):
    if vehicle_count < 5 and delay > 0:
        return "High Accident Probability"
    elif vehicle_count < 20:
        return "Moderate Traffic"
    else:
        return "Normal Traffic"
