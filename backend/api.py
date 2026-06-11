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