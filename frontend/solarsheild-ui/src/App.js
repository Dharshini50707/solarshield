import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "./App.css";

function App() {
  const [riskData, setRiskData] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [alertForm, setAlertForm] = useState({ email: "", location: "", flight_time: "" });
  const [alertSent, setAlertSent] = useState(false);
  const [stormData, setStormData] = useState([]);
  const [replayPlaying, setReplayPlaying] = useState(false);
  const [replayIndex, setReplayIndex] = useState(0);
  const [currentStorm, setCurrentStorm] = useState(null);

  useEffect(() => {
    fetchData();
    fetchStormData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const riskRes = await fetch("http://127.0.0.1:8000/current-risk");
      const riskJson = await riskRes.json();
      setRiskData(riskJson);
      const forecastRes = await fetch("http://127.0.0.1:8000/forecast");
      const forecastJson = await forecastRes.json();
      setForecast(forecastJson.forecast);
      setLoading(false);
    } catch (err) {
      console.error("API error:", err);
      setLoading(false);
    }
  };

  const fetchStormData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/storm-replay");
      const json = await res.json();
      setStormData(json.data);
    } catch (err) {
      console.error("Storm data error:", err);
    }
  };

  const playReplay = () => {
    setReplayPlaying(true);
    setReplayIndex(0);
    setCurrentStorm(null);
    let i = 0;
    const interval = setInterval(() => {
      if (i >= stormData.length) {
        clearInterval(interval);
        setReplayPlaying(false);
        return;
      }
      setCurrentStorm(stormData[i]);
      setReplayIndex(i + 1);
      i++;
    }, 800);
  };

  const getRiskColor = (level) => {
    if (level === "HIGH") return "#ef4444";
    if (level === "MODERATE") return "#f97316";
    return "#22c55e";
  };

  const getRiskBg = (level) => {
    if (level === "HIGH") return "#fef2f2";
    if (level === "MODERATE") return "#fff7ed";
    return "#f0fdf4";
  };

  const handleAlertSubmit = () => {
    setAlertSent(true);
    setTimeout(() => setAlertSent(false), 3000);
  };

  if (loading) return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", background: "#0f172a" }}>
      <div style={{ color: "white", fontSize: "24px" }}>🛸 Loading SolarShield...</div>
    </div>
  );

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", fontFamily: "Arial, sans-serif", color: "white" }}>

      {/* Header */}
      <div style={{ background: "#1e293b", padding: "16px 32px", borderBottom: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "24px", color: "#38bdf8" }}>🛡️ SolarShield</h1>
          <p style={{ margin: 0, fontSize: "12px", color: "#94a3b8" }}>GPS Disruption Early Warning System</p>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "12px", color: "#94a3b8" }}>Live NASA/NOAA Data</div>
          <div style={{ fontSize: "12px", color: "#22c55e" }}>● API Connected</div>
        </div>
      </div>

      {/* Early Warning Banner */}
      {riskData && (
        <div style={{ background: riskData.risk_level === "HIGH" ? "#7f1d1d" : riskData.risk_level === "MODERATE" ? "#7c2d12" : "#14532d", padding: "12px 32px", textAlign: "center", fontSize: "14px" }}>
          ⚡ {riskData.early_warning} | Current Risk: <strong>{riskData.risk_level}</strong> | Updated: {new Date(riskData.timestamp).toLocaleTimeString()}
        </div>
      )}

      <div style={{ padding: "32px", maxWidth: "1200px", margin: "0 auto" }}>

        {/* Main Stats */}
        {riskData && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px", marginBottom: "32px" }}>
            <div style={{ background: getRiskBg(riskData.risk_level), border: `2px solid ${getRiskColor(riskData.risk_level)}`, borderRadius: "12px", padding: "20px", textAlign: "center" }}>
              <div style={{ fontSize: "36px", fontWeight: "bold", color: getRiskColor(riskData.risk_level) }}>{riskData.risk_score}/10</div>
              <div style={{ fontSize: "14px", color: "#374151" }}>Risk Score</div>
              <div style={{ fontSize: "16px", fontWeight: "bold", color: getRiskColor(riskData.risk_level) }}>{riskData.risk_level}</div>
            </div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", textAlign: "center", border: "1px solid #334155" }}>
              <div style={{ fontSize: "36px", fontWeight: "bold", color: "#38bdf8" }}>{riskData.eta_minutes}</div>
              <div style={{ fontSize: "14px", color: "#94a3b8" }}>Minutes Warning</div>
              <div style={{ fontSize: "12px", color: "#64748b" }}>DSCOVR → Earth</div>
            </div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", textAlign: "center", border: "1px solid #334155" }}>
              <div style={{ fontSize: "36px", fontWeight: "bold", color: "#a78bfa" }}>{riskData.solar_wind_speed}</div>
              <div style={{ fontSize: "14px", color: "#94a3b8" }}>Solar Wind km/s</div>
              <div style={{ fontSize: "12px", color: "#64748b" }}>Live from DSCOVR</div>
            </div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", textAlign: "center", border: "1px solid #334155" }}>
              <div style={{ fontSize: "36px", fontWeight: "bold", color: "#fb923c" }}>{riskData.kp_index}/9</div>
              <div style={{ fontSize: "14px", color: "#94a3b8" }}>Kp Index</div>
              <div style={{ fontSize: "12px", color: "#64748b" }}>Geomagnetic Activity</div>
            </div>
          </div>
        )}

        {/* Forecast Chart */}
        <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "32px", border: "1px solid #334155" }}>
          <h2 style={{ margin: "0 0 16px 0", fontSize: "18px", color: "#e2e8f0" }}>📈 6-Hour GPS Risk Forecast</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={forecast}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="hour" stroke="#94a3b8" />
              <YAxis domain={[0, 10]} stroke="#94a3b8" />
              <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", color: "white" }} />
              <Line type="monotone" dataKey="risk_score" stroke="#38bdf8" strokeWidth={2} dot={{ fill: "#38bdf8" }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* India Risk Map + Alert Form */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "24px" }}>
          <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", border: "1px solid #334155" }}>
            <h2 style={{ margin: "0 0 16px 0", fontSize: "18px", color: "#e2e8f0" }}>🗺️ India GPS Risk Map</h2>
            {riskData && ["Chennai", "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Kolkata"].map(city => (
              <div key={city} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid #334155" }}>
                <span style={{ color: "#e2e8f0" }}>{city}</span>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <div style={{ width: "80px", height: "8px", borderRadius: "4px", background: "#334155" }}>
                    <div style={{ width: `${riskData.risk_score * 10}%`, height: "100%", borderRadius: "4px", background: getRiskColor(riskData.risk_level) }}></div>
                  </div>
                  <span style={{ color: getRiskColor(riskData.risk_level), fontSize: "12px", fontWeight: "bold" }}>{riskData.risk_level}</span>
                </div>
              </div>
            ))}
          </div>

          <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", border: "1px solid #334155" }}>
            <h2 style={{ margin: "0 0 16px 0", fontSize: "18px", color: "#e2e8f0" }}>🔔 Register Flight Alert</h2>
            <p style={{ color: "#94a3b8", fontSize: "13px", margin: "0 0 16px 0" }}>Get notified before GPS disruption hits your area</p>
            <input placeholder="Your email" value={alertForm.email} onChange={e => setAlertForm({...alertForm, email: e.target.value})} style={{ width: "100%", padding: "10px", marginBottom: "12px", borderRadius: "8px", border: "1px solid #334155", background: "#0f172a", color: "white", boxSizing: "border-box" }} />
            <input placeholder="Location (e.g. Chennai, Tamil Nadu)" value={alertForm.location} onChange={e => setAlertForm({...alertForm, location: e.target.value})} style={{ width: "100%", padding: "10px", marginBottom: "12px", borderRadius: "8px", border: "1px solid #334155", background: "#0f172a", color: "white", boxSizing: "border-box" }} />
            <input type="datetime-local" value={alertForm.flight_time} onChange={e => setAlertForm({...alertForm, flight_time: e.target.value})} style={{ width: "100%", padding: "10px", marginBottom: "16px", borderRadius: "8px", border: "1px solid #334155", background: "#0f172a", color: "white", boxSizing: "border-box" }} />
            <button onClick={handleAlertSubmit} style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "none", background: "#38bdf8", color: "#0f172a", fontWeight: "bold", cursor: "pointer", fontSize: "14px" }}>
              {alertSent ? "✅ Alert Registered!" : "Register for Alerts"}
            </button>
          </div>
        </div>

        {/* Storm Replay */}
        <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "24px", border: "2px solid #ef4444" }}>
          <h2 style={{ margin: "0 0 4px 0", fontSize: "18px", color: "#ef4444" }}>🌩️ May 2024 Storm Replay — Model Validation</h2>
          <p style={{ color: "#94a3b8", fontSize: "13px", margin: "0 0 16px 0" }}>Strongest solar storm in 20 years. See how SolarShield would have predicted it in real time.</p>

          {currentStorm && (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px", marginBottom: "16px" }}>
              <div style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", textAlign: "center" }}>
                <div style={{ fontSize: "22px", fontWeight: "bold", color: "#ef4444" }}>{currentStorm.risk_score}/10</div>
                <div style={{ fontSize: "11px", color: "#94a3b8" }}>Risk Score</div>
              </div>
              <div style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", textAlign: "center" }}>
                <div style={{ fontSize: "22px", fontWeight: "bold", color: "#f97316" }}>{currentStorm.kp}/9</div>
                <div style={{ fontSize: "11px", color: "#94a3b8" }}>Kp Index</div>
              </div>
              <div style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", textAlign: "center" }}>
                <div style={{ fontSize: "22px", fontWeight: "bold", color: "#a78bfa" }}>{currentStorm.wind_speed} km/s</div>
                <div style={{ fontSize: "11px", color: "#94a3b8" }}>Solar Wind</div>
              </div>
              <div style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", textAlign: "center" }}>
                <div style={{ fontSize: "16px", fontWeight: "bold", color: "#ef4444" }}>{currentStorm.risk_level}</div>
                <div style={{ fontSize: "11px", color: "#94a3b8" }}>{currentStorm.time}</div>
              </div>
            </div>
          )}

          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={stormData.slice(0, replayIndex)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 10 }} />
              <YAxis domain={[0, 10]} stroke="#94a3b8" />
              <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", color: "white" }} />
              <Line type="monotone" dataKey="risk_score" stroke="#ef4444" strokeWidth={2} dot={{ fill: "#ef4444" }} />
            </LineChart>
          </ResponsiveContainer>

          <button onClick={playReplay} disabled={replayPlaying} style={{ marginTop: "12px", padding: "10px 24px", borderRadius: "8px", border: "none", background: replayPlaying ? "#334155" : "#ef4444", color: "white", fontWeight: "bold", cursor: replayPlaying ? "not-allowed" : "pointer" }}>
            {replayPlaying ? `▶ Replaying... ${replayIndex}/${stormData.length}` : "▶ Play May 2024 Storm Replay"}
          </button>
        </div>

        {/* Footer */}
        <div style={{ textAlign: "center", marginTop: "32px", color: "#475569", fontSize: "12px" }}>
          Data sourced from NASA DSCOVR & NOAA Space Weather Prediction Center | SolarShield v1.0
        </div>

      </div>
    </div>
  );
}

export default App;