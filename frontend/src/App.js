import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Header from './components/Header';

// Configure axios defaults
axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setIsAuthenticated(true);
      // You could verify the token here
    }
    setLoading(false);
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setIsAuthenticated(false);
    setUser(null);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading Privacy Analytics Platform...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Header user={user} onLogout={isAuthenticated ? handleLogout : null} />
        <Routes>
          <Route
            path="/login"
            element={<Navigate to="/dashboard" replace />}
          />
          <Route
            path="/dashboard"
            element={<Dashboard />}
          />
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 