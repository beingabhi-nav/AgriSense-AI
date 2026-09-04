import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [userId, setUserId] = useState(null);
  const [isLoginView, setIsLoginView] = useState(true);
  const [authData, setAuthData] = useState({ username: '', password: '' });
  const [authMessage, setAuthMessage] = useState('');

  const [formData, setFormData] = useState({
    nitrogen: '', phosphorus: '', potassium: '',
    temperature: '', humidity: '', ph: '', rainfall: ''
  });
  
  const [farmData, setFarmData] = useState({ farm_name: '', location: '', soil_type: '' });
  const [farms, setFarms] = useState([]);
  
  const [predictionResult, setPredictionResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    if (!userId) return;
    try {
      const histRes = await fetch(`http://localhost:5000/api/history/${userId}`);
      const histData = await histRes.json();
      setHistory(histData);
      
      const farmRes = await fetch(`http://localhost:5000/api/farms?user_id=${userId}`);
      const farmList = await farmRes.json();
      setFarms(farmList);
    } catch (err) {
      console.error("Failed to fetch dashboard data");
    }
  };

  useEffect(() => {
    fetchData();
  }, [userId]);

  const handleAuthChange = (e) => {
    setAuthData({ ...authData, [e.target.name]: e.target.value });
  };

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFarmChange = (e) => {
    setFarmData({ ...farmData, [e.target.name]: e.target.value });
  };

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setAuthMessage('Processing...');
    const endpoint = isLoginView ? '/api/login' : '/api/register';
    try {
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(authData),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Authentication failed');
      }
      setAuthMessage(data.message);
      if (data.user_id) {
        setUserId(data.user_id);
      }
    } catch (err) {
      setAuthMessage(`Error: ${err.message}`);
    }
  };

  const handleFarmSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...farmData, user_id: userId };
      await fetch('http://localhost:5000/api/farms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      setFarmData({ farm_name: '', location: '', soil_type: '' });
      fetchData(); 
    } catch (err) {
      console.error(err);
    }
  };

  const handlePredictSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPredictionResult(null);
    try {
      const payload = { ...formData, user_id: userId };
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch prediction');
      }
      setPredictionResult({
        crop: data.recommended_crop,
        yield: data.estimated_yield,
        advisory: data.advisory
      });
      fetchData(); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Safe Analytics Calculation
  let avgN = 0;
  let avgP = 0;
  let avgK = 0;

  if (history.length > 0) {
    avgN = (history.reduce((sum, item) => sum + item.n, 0) / history.length).toFixed(1);
    avgP = (history.reduce((sum, item) => sum + item.p, 0) / history.length).toFixed(1);
    avgK = (history.reduce((sum, item) => sum + item.k, 0) / history.length).toFixed(1);
  }

  // Reverse history for chronological chart display
  const chartData = [...history].reverse();

  if (!userId) {
    return (
      <div className="auth-container">
        <h1 className="brand-title">🌱 AgriSense AI</h1>
        <h2>{isLoginView ? 'Login' : 'Create Account'}</h2>
        <form onSubmit={handleAuthSubmit} className="auth-form">
          <input type="text" name="username" placeholder="Username" required value={authData.username} onChange={handleAuthChange} />
          <input type="password" name="password" placeholder="Password" required value={authData.password} onChange={handleAuthChange} />
          <button type="submit" className="submit-btn">{isLoginView ? 'Sign In' : 'Register'}</button>
        </form>
        <p className={authMessage.includes('Error') ? 'error-text' : 'success-text'}>{authMessage}</p>
        <button className="auth-toggle" onClick={() => setIsLoginView(!isLoginView)}>
          {isLoginView ? "Need an account? Register here." : "Already have an account? Login here."}
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="nav-bar">
        <h1>🌱 AgriSense AI Dashboard</h1>
        <button className="logout-btn" onClick={() => { setUserId(null); setHistory([]); setFarms([]); setPredictionResult(null); }}>Logout</button>
      </div>

      <div className="dashboard-grid">
        <div className="left-panel">
          <section className="card-section">
            <h2>🚜 Manage Farms</h2>
            <form onSubmit={handleFarmSubmit} className="farm-form">
              <input type="text" name="farm_name" placeholder="Farm Name" required value={farmData.farm_name} onChange={handleFarmChange} />
              <input type="text" name="location" placeholder="Location" required value={farmData.location} onChange={handleFarmChange} />
              <input type="text" name="soil_type" placeholder="Soil Type" required value={farmData.soil_type} onChange={handleFarmChange} />
              <button type="submit" className="submit-btn secondary">Add</button>
            </form>
            <div className="farm-list">
              {farms.map(f => (
                <div key={f.id} className="farm-badge">{f.name} - {f.location} ({f.soil})</div>
              ))}
            </div>
          </section>

          <section className="card-section">
            <h2>🔮 ML Analysis Tool</h2>
            <form onSubmit={handlePredictSubmit}>
              <div className="input-grid">
                {Object.keys(formData).map((key) => (
                  <div className="input-group" key={key}>
                    <label>{key}</label>
                    <input type="number" step="any" name={key} required value={formData[key]} onChange={handleFormChange} placeholder={`Enter ${key}`} />
                  </div>
                ))}
              </div>
              <button className="submit-btn" type="submit" disabled={loading}>
                {loading ? 'Analyzing...' : 'Generate Prediction'}
              </button>
            </form>
            {error && <div className="error-message"><strong>Error:</strong> {error}</div>}
          </section>
        </div>

        <div className="right-panel">
          {predictionResult && (
            <section className="card-section highlight-card">
              <h2>🎯 Recommendation: <span>{predictionResult.crop}</span></h2>
              <h3>📊 Est. Yield: <span>{predictionResult.yield}</span></h3>
              <div className="advisory-box">
                <h4>💡 Curated Advisory:</h4>
                <p>{predictionResult.advisory}</p>
              </div>
            </section>
          )}

          <section className="card-section">
            <h2>📈 Analytics Dashboard</h2>
            <div className="analytics-stats">
              <div className="stat-box"><h4>Avg Nitrogen</h4><p>{avgN}</p></div>
              <div className="stat-box"><h4>Avg Phosphorus</h4><p>{avgP}</p></div>
              <div className="stat-box"><h4>Avg Potassium</h4><p>{avgK}</p></div>
            </div>
            
            {history.length > 0 && (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
                    <XAxis dataKey="date" tick={{fontSize: 10}} tickFormatter={(tick) => tick.split(' ')[0]} />
                    <YAxis tick={{fontSize: 12}} />
                    <Tooltip />
                    <Legend wrapperStyle={{fontSize: '12px'}} />
                    <Line type="monotone" dataKey="n" stroke="#1976d2" name="Nitrogen" strokeWidth={2} dot={{ r: 3 }} />
                    <Line type="monotone" dataKey="p" stroke="#2e7d32" name="Phosphorus" strokeWidth={2} dot={{ r: 3 }} />
                    <Line type="monotone" dataKey="k" stroke="#fbc02d" name="Potassium" strokeWidth={2} dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}

            <h3 className="history-title">📖 Record History</h3>
            <div className="table-container">
              <table>
                <thead>
                  <tr><th>Date</th><th>Crop</th><th>N-P-K</th></tr>
                </thead>
                <tbody>
                  {history.map((r) => (
                    <tr key={r.id}>
                      <td>{r.date.split(' ')[0]}</td>
                      <td className="crop-cell">{r.crop}</td>
                      <td>{r.n}-{r.p}-{r.k}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
      
      <footer className="team-footer">
        AgriSense AI Platform • Team MNP036: Abhinav, Manasvi, Sanjeev
      </footer>
    </div>
  );
}

export default App;