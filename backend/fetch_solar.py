import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetch_solar_wind():
    url = "https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json"
    response = requests.get(url)
    data = response.json()
    latest = data[-1]
    
    print("=== LIVE SOLAR WIND DATA ===")
    print(f"Time: {latest.get('time_tag')}")
    print(f"Solar Wind Speed: {latest.get('proton_speed')} km/s")
    print(f"Density: {latest.get('proton_density')} p/cc")
    print(f"Temperature: {latest.get('proton_temp')} K")
    print("============================")
    return latest

def fetch_kp_index():
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    response = requests.get(url)
    data = response.json()
    latest = data[-1]
    kp = latest.get('kp_index', 0)
    
    print(f"\nCurrent Kp Index: {kp} / 9")
    if kp >= 5:
        print("WARNING: High geomagnetic activity - GPS disruption likely!")
    elif kp >= 3:
        print("Moderate activity - Minor GPS disruption possible")
    else:
        print("GPS conditions normal")
    return latest

if __name__ == "__main__":
    print(f"Fetching live data at {datetime.now()}\n")
    fetch_solar_wind()
    fetch_kp_index()
