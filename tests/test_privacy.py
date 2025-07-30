import pytest
import numpy as np
from fastapi.testclient import TestClient
from main import app, apply_differential_privacy, mask_pii

client = TestClient(app)

class TestPrivacyFeatures:
    """Test privacy and security features"""
    
    def test_differential_privacy_noise(self):
        """Test that differential privacy adds appropriate noise"""
        original_value = 100.0
        private_value = apply_differential_privacy(original_value)
        
        # Value should be different due to noise
        assert private_value != original_value
        
        # Noise should be reasonable (within 3 standard deviations)
        noise = abs(private_value - original_value)
        assert noise < 30  # Reasonable noise threshold
    
    def test_pii_masking(self):
        """Test PII masking functionality"""
        test_data = {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "555-0123",
            "age": 35,
            "income": 75000
        }
        
        masked_data = mask_pii(test_data)
        
        # Name should be masked
        assert masked_data["name"] != test_data["name"]
        assert "***" in masked_data["name"]
        
        # Email should be masked
        assert masked_data["email"] != test_data["email"]
        assert "***" in masked_data["email"]
        
        # Phone should be masked
        assert masked_data["phone"] != test_data["phone"]
        assert "***-***-" in masked_data["phone"]
        
        # Non-PII fields should remain unchanged
        assert masked_data["age"] == test_data["age"]
        assert masked_data["income"] == test_data["income"]
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "privacy_budget_remaining" in data
        assert "differential_privacy_epsilon" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Privacy-Aware Data Analytics Platform" in data["message"]
    
    def test_dashboard_endpoint(self):
        """Test dashboard endpoint"""
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Privacy-Aware Data Analytics Platform" in response.text

class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_login_success(self):
        """Test successful login"""
        response = client.post("/token", data={
            "username": "admin",
            "password": "admin123"
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    def test_login_failure(self):
        """Test failed login"""
        response = client.post("/token", data={
            "username": "admin",
            "password": "wrong_password"
        })
        assert response.status_code == 401
    
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/analytics/customers")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token"""
        # First login to get token
        login_response = client.post("/token", data={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/analytics/customers", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "total_customers" in data
        assert "average_income" in data
        assert "privacy_budget_used" in data
        assert "privacy_guarantees" in data

class TestAnalyticsEndpoints:
    """Test analytics endpoints with privacy features"""
    
    def test_customer_analytics_privacy(self):
        """Test that customer analytics apply privacy protections"""
        # Login to get token
        login_response = client.post("/token", data={
            "username": "analyst",
            "password": "analyst123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get customer analytics
        response = client.get("/api/analytics/customers", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check privacy features
        assert "privacy_budget_used" in data
        assert "privacy_guarantees" in data
        assert "Differential privacy applied" in data["privacy_guarantees"]
        
        # Check that values are reasonable
        assert data["total_customers"] > 0
        assert data["average_income"] > 0
    
    def test_trend_analytics_privacy(self):
        """Test that trend analytics apply privacy protections"""
        # Login to get token
        login_response = client.post("/token", data={
            "username": "analyst",
            "password": "analyst123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get trend analytics
        response = client.get("/api/analytics/trends", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check privacy features
        assert "privacy_budget_used" in data
        assert "privacy_guarantees" in data
        assert "Differential privacy applied" in data["privacy_guarantees"]
        
        # Check data structure
        assert "category_performance" in data
        assert "age_distribution" in data
        assert "trend_insights" in data

class TestComplianceEndpoints:
    """Test compliance and audit endpoints"""
    
    def test_compliance_status(self):
        """Test compliance status endpoint"""
        # Login to get token
        login_response = client.post("/token", data={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get compliance status
        response = client.get("/api/privacy/compliance", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "gdpr_compliance" in data
        assert "ccpa_compliance" in data
        assert "data_encryption" in data
        assert "pii_masking" in data
        assert "audit_logging" in data
    
    def test_audit_log_admin_access(self):
        """Test audit log access for admin"""
        # Login as admin
        login_response = client.post("/token", data={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Access audit log
        response = client.get("/api/privacy/audit", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "audit_entries" in data
        assert "total_entries" in data
        assert "privacy_budget_remaining" in data
    
    def test_audit_log_non_admin_denied(self):
        """Test that non-admin users cannot access audit log"""
        # Login as analyst
        login_response = client.post("/token", data={
            "username": "analyst",
            "password": "analyst123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to access audit log
        response = client.get("/api/privacy/audit", headers=headers)
        assert response.status_code == 403

if __name__ == "__main__":
    pytest.main([__file__]) 