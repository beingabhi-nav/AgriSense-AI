import React, { useState, useEffect } from 'react';
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
  const [predictionResult, setPredictionResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch history when user logs in or makes a new prediction
  const fetchHistory = async () => {
    if (!userId) return;
    try {
      const response = await fetch(`http://localhost:5000/api/history/${userId}`);
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error("Failed to fetch history");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [userId]);

  const handleAuthChange = (e) => setAuthData({ ...authData, [e.target.name]: e.target.value });

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
      
      if (!response.ok) throw new Error(data.error || 'Authentication failed');
      
      setAuthMessage(data.message);
      if (data.user_id) setUserId(data.user_id);
    } catch (err) {
      setAuthMessage(`Error: ${err.message}`);
    }
  };

  const handleFormChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

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
      if (!response.ok) throw new Error(data.error || 'Failed to fetch prediction');
      
      setPredictionResult({
        crop: data.recommended_crop,
        yield: data.estimated_yield
      });
      
      fetchHistory(); // Refresh table after new prediction
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!userId) {
    return (
      <div className="auth-container">
        <h1 style={{ color: '#2e7d32' }}>🌱 AgriSense AI</h1>
        <h2>{isLoginView ? 'Login' : 'Create Account'}</h2>
        
        <form onSubmit={handleAuthSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <input
            type="text" name="username" placeholder="Username" required
            value={authData.username} onChange={handleAuthChange}
            style={{ padding: '12px', borderRadius: '8px', border: '1px solid #ddd' }}
          />
          <input
            type="password" name="password" placeholder="Password" required
            value={authData.password} onChange={handleAuthChange}
            style={{ padding: '12px', borderRadius: '8px', border: '1px solid #ddd' }}
          />
          <button type="submit" className="submit-btn">
            {isLoginView ? 'Sign In' : 'Register'}
          </button>
        </form>
        
        <p style={{ marginTop: '15px', color: authMessage.includes('Error') ? 'red' : 'green' }}>
          {authMessage}
        </p>

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
        <button className="logout-btn" onClick={() => { setUserId(null); setHistory([]); setPredictionResult(null); }}>Logout</button>
      </div>

      <form onSubmit={handlePredictSubmit}>
        <div className="input-grid">
          {Object.keys(formData).map((key) => (
            <div className="input-group" key={key}>
              <label>{key}</label>
              <input
                type="number" step="any" name={key} required
                value={formData[key]} onChange={handleFormChange}
                placeholder={`Enter ${key}`}
              />
            </div>
          ))}
        </div>
        
        <button className="submit-btn" type="submit" disabled={loading}>
          {loading ? 'Analyzing Data...' : 'Generate Prediction'}
        </button>
      </form>

      {error && <div className="error-message"><strong>Error:</strong> {error}</div>}
      
      {predictionResult && (
        <div className="result-card" style={{ marginTop: '20px', padding: '20px', background: '#e8f5e9', borderRadius: '8px' }}>
          <h2>🎯 Recommended Crop: <span style={{ color: '#2e7d32' }}>{predictionResult.crop}</span></h2>
          <h3 style={{ marginTop: '10px' }}>📊 Estimated Yield: <span style={{ color: '#1565c0' }}>{predictionResult.yield}</span></h3>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section" style={{ marginTop: '40px' }}>
          <h2>📖 Your Prediction History</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
            <thead>
              <tr style={{ background: '#f5f5f5', textAlign: 'left' }}>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Date</th>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Crop</th>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>N-P-K</th>
              </tr>
            </thead>
            <tbody>
              {history.map((record) => (
                <tr key={record.id}>
                  <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{record.date}</td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #eee', fontWeight: 'bold', color: '#2e7d32' }}>{record.crop}</td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{record.n} - {record.p} - {record.k}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;