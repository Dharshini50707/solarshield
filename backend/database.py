import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('solarsheild.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solar_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            solar_wind_speed REAL,
            density REAL,
            temperature REAL,
            kp_index REAL,
            risk_score REAL,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            latitude REAL,
            longitude REAL,
            flight_time TEXT,
            location_name TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_reading(solar_wind_speed, density, temperature, kp_index, risk_score):
    conn = sqlite3.connect('solarsheild.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO solar_readings 
        (timestamp, solar_wind_speed, density, temperature, kp_index, risk_score, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        solar_wind_speed,
        density,
        temperature,
        kp_index,
        risk_score,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def get_latest_readings(limit=100):
    conn = sqlite3.connect('solarsheild.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM solar_readings 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    