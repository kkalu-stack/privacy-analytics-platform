import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const Dashboard = () => {
  const [customerData, setCustomerData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
    // No auto-refresh - load data once on mount
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [customerResponse, trendResponse] = await Promise.all([
        axios.get('/api/analytics/customers'),
        axios.get('/api/analytics/trends')
      ]);
      
      setCustomerData(customerResponse.data);
      setTrendData(trendResponse.data);
      setError('');
    } catch (error) {
      setError('Failed to load analytics data');
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !customerData) {
    return (
      <div className="dashboard-container">
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div className="loading-spinner"></div>
          <p>Loading privacy analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div style={{ textAlign: 'center', padding: '2rem', color: '#e74c3c' }}>
          <p>{error}</p>
          <button onClick={loadData} className="login-btn" style={{ marginTop: '1rem' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  const regionalChartData = customerData ? {
    labels: Object.keys(customerData.regional_breakdown),
    datasets: [{
      data: Object.values(customerData.regional_breakdown).map(r => r.customer_count),
      backgroundColor: [
        '#667eea',
        '#764ba2',
        '#f093fb',
        '#f5576c',
        '#4facfe'
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  } : null;

  const categoryChartData = trendData ? {
    labels: Object.keys(trendData.category_performance),
    datasets: [{
      label: 'Sales Performance',
      data: Object.values(trendData.category_performance),
      backgroundColor: '#667eea',
      borderColor: '#764ba2',
      borderWidth: 1
    }]
  } : null;

  return (
    <div className="dashboard-container">
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-title">Total Customers</div>
          <div className="metric-value">
            {customerData ? customerData.total_customers.toFixed(0) : '--'}
          </div>
          <div className="metric-subtitle">Privacy-preserving count</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Average Income</div>
          <div className="metric-value">
            {customerData ? `$${customerData.average_income.toLocaleString()}` : '--'}
          </div>
          <div className="metric-subtitle">Differential privacy applied</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Purchase Frequency</div>
          <div className="metric-value">
            {customerData ? customerData.average_purchase_frequency.toFixed(1) : '--'}
          </div>
          <div className="metric-subtitle">Per customer average</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Privacy Budget</div>
          <div className="metric-value">
            {customerData ? (1.0 - customerData.privacy_budget_used).toFixed(2) : '--'}
          </div>
          <div className="metric-subtitle">Remaining budget</div>
        </div>
      </div>
      
      <div className="charts-section">
        <div className="chart-card">
          <div className="chart-title">
            Regional Distribution <span className="privacy-badge">PRIVATE</span>
          </div>
          {regionalChartData ? (
            <Doughnut 
              data={regionalChartData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'bottom',
                    labels: {
                      padding: 20,
                      usePointStyle: true
                    }
                  }
                }
              }}
            />
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <p>Loading chart...</p>
            </div>
          )}
        </div>
        
        <div className="chart-card">
          <div className="chart-title">
            Category Performance <span className="privacy-badge">PRIVATE</span>
          </div>
          {categoryChartData ? (
            <Bar 
              data={categoryChartData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      callback: function(value) {
                        return '$' + value.toLocaleString();
                      }
                    }
                  }
                },
                plugins: {
                  legend: {
                    display: false
                  }
                }
              }}
            />
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <p>Loading chart...</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="compliance-section">
        <h2>Compliance Status</h2>
        <div className="compliance-grid">
          <div className="compliance-item">
            <span className="compliance-icon">CHECK</span>
            <div className="compliance-text">
              <h4>GDPR Compliance</h4>
              <p>EU Data Protection</p>
            </div>
          </div>
          
          <div className="compliance-item">
            <span className="compliance-icon">CHECK</span>
            <div className="compliance-text">
              <h4>CCPA Compliance</h4>
              <p>California Privacy</p>
            </div>
          </div>
          
          <div className="compliance-item">
            <span className="compliance-icon">CHECK</span>
            <div className="compliance-text">
              <h4>Data Encryption</h4>
              <p>AES-256 Enabled</p>
            </div>
          </div>
          
          <div className="compliance-item">
            <span className="compliance-icon">CHECK</span>
            <div className="compliance-text">
              <h4>Audit Logging</h4>
              <p>Full Access Trail</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 