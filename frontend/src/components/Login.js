import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/token', credentials);
      const { access_token } = response.data;
      
      // Get user info (you might want to decode the JWT or make another API call)
      const userData = {
        username: credentials.username,
        role: credentials.username === 'admin' ? 'admin' : 
              credentials.username === 'analyst' ? 'analyst' : 'viewer',
        full_name: credentials.username === 'admin' ? 'System Administrator' :
                   credentials.username === 'analyst' ? 'Data Analyst' : 'Data Viewer'
      };
      
      onLogin(access_token, userData);
    } catch (error) {
      setError('Invalid username or password. Try: admin/admin123, analyst/analyst123, or viewer/viewer123');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Privacy Analytics Platform</h2>
        <p style={{ marginBottom: '2rem', color: '#666' }}>
          Enterprise-grade analytics with built-in privacy protections
        </p>
        
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              required
              placeholder="Enter username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              required
              placeholder="Enter password"
            />
          </div>
          
          <button 
            type="submit" 
            className="login-btn"
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>
        
        {error && <div className="error-message">{error}</div>}
        
        <div style={{ marginTop: '2rem', fontSize: '0.9rem', color: '#666' }}>
          <p><strong>Demo Credentials:</strong></p>
          <p>Admin: admin / admin123</p>
          <p>Analyst: analyst / analyst123</p>
          <p>Viewer: viewer / viewer123</p>
        </div>
      </div>
    </div>
  );
};

export default Login; 