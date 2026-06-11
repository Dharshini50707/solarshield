# 🛡️ SolarShield
### GPS Disruption Early Warning System

> "We give 15–60 minutes advance warning before solar storms disrupt GPS — using NASA's own satellite data."

## 🌍 The Problem
Solar storms disrupt GPS signals for hours. In May 2024, the strongest storm in 20 years caused GPS errors exceeding 50 metres globally. Drone startups, satellite teams, and survey agencies had **zero advance warning**.

India has 300+ licensed drone startups and 50+ student satellite teams — none of them have access to any early warning system today.

## 💡 The Key Insight
NASA's DSCOVR satellite sits 1.5 million km from Earth. When solar wind hits DSCOVR, it takes **15–60 minutes** to reach Earth. That gap is our warning window.

## 🚀 What We Built
- **Live risk map** — location-specific GPS disruption risk across India
- **6-hour forecast** — updated every 30 minutes from live NASA/NOAA data
- **Early warning banner** — "Solar wind reaches Earth in 63 minutes"
- **Flight alert registration** — drone teams get automatic alerts before disruption
- **May 2024 storm replay** — model validation against the strongest storm in 20 years
- **Public REST API** — any drone app can integrate our risk scores

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Data | NASA DSCOVR API + NOAA Kp Index |
| Backend | Python + FastAPI |
| ML Model | scikit-learn Random Forest |
| Frontend | React + Recharts |
| Database | SQLite |

## 📡 API Endpoints
GET /current-risk     — Live GPS risk score for any location
GET /forecast         — 6-hour risk forecast
GET /storm-replay     — May 2024 storm historical data
GET /history          — Past readings database
GET /docs             — Interactive API documentation
## ⚙️ Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```

### Frontend
```bash
cd frontend/solarsheild-ui
npm install
npm start
```

## 🌐 Data Sources
- NASA DSCOVR Real-Time Solar Wind: https://services.swpc.noaa.gov
- NOAA Planetary K-index: https://services.swpc.noaa.gov
- All data is free and publicly available

## 🏆 FAR AWAY Hackathon 2026
Theme: Space & Aerospace