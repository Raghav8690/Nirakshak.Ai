"""
Nirikshak.AI — Customer Model
===============================
Represents a bank customer with demographic and financial profile data.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    occupation = Column(String(100), nullable=False)
    monthly_income = Column(Float, nullable=False)
    account_type = Column(String(50), nullable=False)  # Savings, Current, Salary
    account_number = Column(String(20), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    risk_profile = Column(String(20), default="moderate")  # conservative, moderate, aggressive
    kyc_status = Column(String(20), default="verified")
    financial_health_score = Column(Float, default=0.0)  # 0-100 computed score
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="customer")
    triggers = relationship("Trigger", back_populates="customer")
    feedbacks = relationship("Feedback", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', income={self.monthly_income})>"
