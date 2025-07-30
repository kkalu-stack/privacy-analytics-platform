from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://privacy_user:secure_password@localhost/privacy_analytics")

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

class Customer(Base):
    """Customer data model with PII fields"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True)
    name = Column(String)  # Will be masked in responses
    email = Column(String)  # Will be masked in responses
    phone = Column(String)  # Will be masked in responses
    age = Column(Integer)
    income = Column(Float)
    purchase_frequency = Column(Integer)
    avg_order_value = Column(Float)
    last_purchase = Column(DateTime)
    region = Column(String)
    product_category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    """Audit log for compliance tracking"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = Column(String)
    action = Column(String)
    resource = Column(String)
    privacy_budget_used = Column(Float, default=0.0)
    ip_address = Column(String)
    user_agent = Column(String)

class PrivacyBudget(Base):
    """Privacy budget tracking"""
    __tablename__ = "privacy_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, index=True)
    total_budget = Column(Float, default=1.0)
    used_budget = Column(Float, default=0.0)
    epsilon = Column(Float, default=0.1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    """User authentication model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # admin, analyst, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data for initialization
def initialize_sample_data():
    """Initialize database with sample customer data"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Customer).count() > 0:
        db.close()
        return
    
    # Sample customer data
    customers = [
        {
            "customer_id": "CUST001",
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "555-0123",
            "age": 35,
            "income": 75000,
            "purchase_frequency": 12,
            "avg_order_value": 150.50,
            "last_purchase": datetime(2024, 1, 15),
            "region": "North",
            "product_category": "Electronics"
        },
        {
            "customer_id": "CUST002",
            "name": "Sarah Johnson",
            "email": "sarah.j@email.com",
            "phone": "555-0124",
            "age": 28,
            "income": 65000,
            "purchase_frequency": 8,
            "avg_order_value": 89.75,
            "last_purchase": datetime(2024, 1, 10),
            "region": "South",
            "product_category": "Clothing"
        },
        {
            "customer_id": "CUST003",
            "name": "Michael Brown",
            "email": "michael.b@email.com",
            "phone": "555-0125",
            "age": 42,
            "income": 95000,
            "purchase_frequency": 15,
            "avg_order_value": 225.00,
            "last_purchase": datetime(2024, 1, 20),
            "region": "West",
            "product_category": "Home & Garden"
        },
        {
            "customer_id": "CUST004",
            "name": "Emily Davis",
            "email": "emily.d@email.com",
            "phone": "555-0126",
            "age": 31,
            "income": 72000,
            "purchase_frequency": 6,
            "avg_order_value": 75.25,
            "last_purchase": datetime(2024, 1, 5),
            "region": "East",
            "product_category": "Books"
        },
        {
            "customer_id": "CUST005",
            "name": "David Wilson",
            "email": "david.w@email.com",
            "phone": "555-0127",
            "age": 38,
            "income": 88000,
            "purchase_frequency": 18,
            "avg_order_value": 180.00,
            "last_purchase": datetime(2024, 1, 18),
            "region": "North",
            "product_category": "Sports"
        }
    ]
    
    # Add customers to database
    for customer_data in customers:
        customer = Customer(**customer_data)
        db.add(customer)
    
    # Initialize privacy budgets
    privacy_budgets = [
        {"user": "admin", "total_budget": 1.0, "used_budget": 0.0, "epsilon": 0.1},
        {"user": "analyst", "total_budget": 1.0, "used_budget": 0.0, "epsilon": 0.1},
        {"user": "viewer", "total_budget": 1.0, "used_budget": 0.0, "epsilon": 0.1}
    ]
    
    for budget_data in privacy_budgets:
        budget = PrivacyBudget(**budget_data)
        db.add(budget)
    
    db.commit()
    db.close() 