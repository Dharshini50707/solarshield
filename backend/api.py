from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch_solar import fetch_solar_wind, fetch_kp_index
from risk_calculator import calculate_risk_score, get_risk_label, calculate_eta_minutes
from database import init_db, save_reading, get_latest_readings
from datetime import datetime

app = FastAPI(title="SolarShield API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/")
def root():
    return {"message": "SolarShield API is live", "status": "operational"}

@app.get("/current-risk")
def get_current_risk():
    solar_data = fetch_solar_wind()
    kp_data = fetch_kp_index()

    wind_speed = solar_data.get('proton_speed') or 400
    density = solar_data.get('proton_density') or 5
    temperature = solar_data.get('proton_temp') or 0
    kp = kp_data.get('kp_index') or 0

    risk_score = calculate_risk_score(kp, wind_speed, density)
    label, message = get_risk_label(risk_score)
    eta = calculate_eta_minutes(wind_speed)

    save_reading(wind_speed, density, temperature, kp, risk_score)

    return {
        "timestamp": datetime.now().isoformat(),
        "solar_wind_speed": wind_speed,
        "density": density,
        "kp_index": kp,
        "risk_score": risk_score,
        "risk_level": label,
        "message": message,
        "eta_minutes": eta,
        "early_warning": f"Solar wind reaches Earth in {eta} minutes"
    }

@app.get("/forecast")
def get_forecast():
    solar_data = fetch_solar_wind()
    kp_data = fetch_kp_index()
    
    wind_speed = solar_data.get('proton_speed') or 400
    density = solar_data.get('proton_density') or 5
    kp = kp_data.get('kp_index') or 0
    
    forecast = []
    for hour in range(6):
        simulated_kp = kp + (hour * 0.1)
        score = calculate_risk_score(simulated_kp, wind_speed, density)
        label, message = get_risk_label(score)
        forecast.append({
            "hour": f"+{hour}h",
            "risk_score": score,
            "risk_level": label
        })
    
    return {"forecast": forecast}

@app.get("/history")
def get_history():
    rows = get_latest_readings(50)
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "timestamp": row[1],
            "solar_wind_speed": row[2],
            "density": row[3],
            "kp_index": row[5],
            "risk_score": row[6]
        })
    return {"history": history}
@app.get("/storm-replay")
def get_storm_replay():
    storm_data = [
        {"time": "May 10 06:00", "kp": 3, "wind_speed": 650, "risk_score": 4.2, "risk_level": "MODERATE"},
        {"time": "May 10 08:00", "kp": 5, "wind_speed": 720, "risk_score": 6.5, "risk_level": "HIGH"},
        {"time": "May 10 10:00", "kp": 7, "wind_speed": 780, "risk_score": 8.0, "risk_level": "HIGH"},
        {"time": "May 10 12:00", "kp": 8, "wind_speed": 850, "risk_score": 9.0, "risk_level": "HIGH"},
        {"time": "May 10 14:00", "kp": 9, "wind_speed": 900, "risk_score": 10.0, "risk_level": "HIGH"},
        {"time": "May 10 16:00", "kp": 8, "wind_speed": 820, "risk_score": 9.0, "risk_level": "HIGH"},
        {"time": "May 10 18:00", "kp": 7, "wind_speed": 750, "risk_score": 7.5, "risk_level": "HIGH"},
        {"time": "May 10 20:00", "kp": 6, "wind_speed": 680, "risk_score": 6.5, "risk_level": "HIGH"},
        {"time": "May 10 22:00", "kp": 5, "wind_speed": 620, "risk_score": 5.5, "risk_level": "MODERATE"},
        {"time": "May 11 00:00", "kp": 4, "wind_speed": 550, "risk_score": 4.0, "risk_level": "MODERATE"},
        {"time": "May 11 06:00", "kp": 3, "wind_speed": 480, "risk_score": 3.0, "risk_level": "MODERATE"},
        {"time": "May 11 12:00", "kp": 2, "wind_speed": 420, "risk_score": 2.0, "risk_level": "LOW"},
        {"time": "May 11 18:00", "kp": 1, "wind_speed": 380, "risk_score": 1.5, "risk_level": "LOW"},
    ]
    return {
        "event": "May 2024 Solar Storm - G5 Class",
        "description": "Strongest geomagnetic storm in 20 years. Kp reached 9/9. GPS errors exceeded 50 metres globally.",
        "peak_kp": 9,
        "peak_wind_speed": 900,
        "duration_hours": 36,
        "data": storm_data
    }