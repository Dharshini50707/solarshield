import time
from datetime import datetime
from fetch_solar import fetch_solar_wind, fetch_kp_index
from database import init_db, save_reading
from risk_calculator import calculate_risk_score, get_risk_label, calculate_eta_minutes

def run_pipeline():
    print(f"\n{'='*50}")
    print(f"SolarShield Pipeline Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    # Step 1 - Fetch live data
    print("\n[1/3] Fetching live solar wind data...")
    solar_data = fetch_solar_wind()
    
    print("\n[2/3] Fetching Kp index...")
    kp_data = fetch_kp_index()

    # Step 2 - Extract values
    wind_speed = solar_data.get('proton_speed') or 400
    density = solar_data.get('proton_density') or 5
    temperature = solar_data.get('proton_temp') or 0
    kp = kp_data.get('kp_index') or 0

    # Step 3 - Calculate risk
    print("\n[3/3] Calculating GPS disruption risk...")
    risk_score = calculate_risk_score(kp, wind_speed, density)
    label, message = get_risk_label(risk_score)
    eta = calculate_eta_minutes(wind_speed)

    # Step 4 - Save to database
    save_reading(wind_speed, density, temperature, kp, risk_score)

    # Step 5 - Print final report
    print(f"\n{'='*50}")
    print(f"SOLARSHEILD REPORT")
    print(f"{'='*50}")
    print(f"Solar Wind Speed : {wind_speed} km/s")
    print(f"Density          : {density} p/cc")
    print(f"Kp Index         : {kp}/9")
    print(f"Risk Score       : {risk_score}/10")
    print(f"Risk Level       : {label}")
    print(f"Message          : {message}")
    print(f"ETA to Earth     : {eta} minutes")
    
    if risk_score >= 7:
        print(f"\n🚨 ALERT: GPS disruption imminent in {eta} minutes!")
        print(f"   Drone operators should land immediately.")
    elif risk_score >= 4:
        print(f"\n⚠️  CAUTION: Moderate GPS disruption possible in {eta} minutes")
    else:
        print(f"\n✅ All clear - Safe flying conditions")
    
    print(f"{'='*50}\n")
    
    return risk_score

if __name__ == "__main__":
    # Initialize database first
    init_db()
    
    # Run once
    run_pipeline()
    
    print("Pipeline complete. In production this runs every 30 mins.")
    