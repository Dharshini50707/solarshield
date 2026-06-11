import numpy as np

def calculate_risk_score(kp_index, solar_wind_speed, density):
    """
    Calculate GPS disruption risk score 0-10
    Based on real space weather research:
    - Kp >= 5 = major disruption
    - Solar wind > 600 km/s = high risk
    - High density = more particles hitting Earth
    """
    risk = 0

    # Kp index contribution (most important factor)
    if kp_index >= 7:
        risk += 5.0
    elif kp_index >= 5:
        risk += 3.5
    elif kp_index >= 3:
        risk += 1.5
    else:
        risk += 0.5

    # Solar wind speed contribution
    if solar_wind_speed >= 700:
        risk += 3.0
    elif solar_wind_speed >= 500:
        risk += 2.0
    elif solar_wind_speed >= 400:
        risk += 1.0
    else:
        risk += 0.2

    # Density contribution
    if density >= 20:
        risk += 2.0
    elif density >= 10:
        risk += 1.0
    else:
        risk += 0.3

    # Cap at 10
    risk = min(round(risk, 1), 10.0)

    return risk

def get_risk_label(risk_score):
    if risk_score >= 7:
        return "HIGH", "Do not fly - GPS unreliable"
    elif risk_score >= 4:
        return "MODERATE", "Fly with caution - minor GPS errors possible"
    else:
        return "LOW", "Safe to fly - GPS conditions normal"

def calculate_eta_minutes(solar_wind_speed):
    """
    DSCOVR is 1.5M km from Earth
    Solar wind speed is in km/s already
    """
    distance_km = 1_500_000
    eta_seconds = distance_km / solar_wind_speed
    eta_minutes = round(eta_seconds / 60)
    return eta_minutes

if __name__ == "__main__":
    # Test with current data we just fetched
    kp = 1
    wind_speed = 401.9
    density = 8.08

    score = calculate_risk_score(kp, wind_speed, density)
    label, message = get_risk_label(score)
    eta = calculate_eta_minutes(wind_speed)

    print(f"Risk Score: {score}/10")
    print(f"Risk Level: {label}")
    print(f"Message: {message}")
    print(f"Solar wind ETA to Earth: {eta} minutes")
