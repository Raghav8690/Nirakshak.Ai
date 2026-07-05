"""
Nirikshak.AI — Customers Router
==================================
Endpoints for customer profile data and the Customer 360 view.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from collections import defaultdict

from app.database import get_db
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.models.trigger import Trigger
from app.schemas.customer import CustomerResponse, CustomerCreate, Customer360Response

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("/", response_model=List[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all customers with pagination."""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=Customer360Response)
def get_customer_360(customer_id: int, db: Session = Depends(get_db)):
    """
    Get full Customer 360 view — profile + aggregated financial data.
    This powers the Customer Dashboard page.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Aggregate transaction data
    transactions = db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).all()

    total_credits = sum(t.amount for t in transactions if t.transaction_type == "credit")
    total_debits = sum(t.amount for t in transactions if t.transaction_type == "debit")

    # Top spend categories
    category_spend = defaultdict(float)
    for t in transactions:
        if t.transaction_type == "debit":
            category_spend[t.category] += t.amount
    top_categories = [
        {"category": k, "amount": v}
        for k, v in sorted(category_spend.items(), key=lambda x: x[1], reverse=True)[:6]
    ]

    # Product holdings (derived from transaction categories)
    holdings = []
    if any(t.category == "Insurance" for t in transactions):
        holdings.append("Health Insurance")
    if any(t.category == "Investment" for t in transactions):
        holdings.append("Mutual Fund SIP")
    if any(t.category == "EMI" for t in transactions):
        holdings.append("Home Loan EMI")
    holdings.append("Savings Account")

    # Active triggers
    active_triggers = db.query(Trigger).filter(
        Trigger.customer_id == customer_id,
        Trigger.status == "pending",
    ).count()

    # Build response
    response = Customer360Response(
        id=customer.id,
        name=customer.name,
        age=customer.age,
        gender=customer.gender,
        occupation=customer.occupation,
        monthly_income=customer.monthly_income,
        account_type=customer.account_type,
        account_number=customer.account_number,
        phone=customer.phone,
        email=customer.email,
        city=customer.city,
        risk_profile=customer.risk_profile,
        kyc_status=customer.kyc_status,
        financial_health_score=customer.financial_health_score,
        created_at=customer.created_at,
        total_transactions=len(transactions),
        total_credits=total_credits,
        total_debits=total_debits,
        top_spend_categories=top_categories,
        product_holdings=holdings,
        active_triggers=active_triggers,
        recent_life_events=[],
    )
    return response


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer."""
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
