"""
Nirikshak.AI — Customer Schemas
=================================
Pydantic models for API request validation and response serialization.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CustomerBase(BaseModel):
    """Fields shared between create and read."""
    name: str
    age: int
    gender: str
    occupation: str
    monthly_income: float
    account_type: str
    account_number: str
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    risk_profile: str = "moderate"
    kyc_status: str = "verified"


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""
    pass


class CustomerResponse(CustomerBase):
    """Schema for returning a customer."""
    id: int
    financial_health_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class Customer360Response(CustomerResponse):
    """
    Full Customer 360 view — includes aggregated financial data.
    Used by the Dashboard page.
    """
    total_transactions: int = 0
    total_credits: float = 0.0
    total_debits: float = 0.0
    top_spend_categories: List[dict] = []
    product_holdings: List[str] = []
    active_triggers: int = 0
    recent_life_events: List[str] = []

    class Config:
        from_attributes = True
