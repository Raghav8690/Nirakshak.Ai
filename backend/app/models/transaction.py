"""
Nirikshak.AI — Transaction Model
==================================
Represents individual financial transactions for a customer.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # credit, debit
    category = Column(String(50), nullable=False)
    # Categories: Salary, Rent, EMI, Groceries, Insurance, Investment,
    #             Entertainment, Travel, UPI, Utilities, Shopping, Other
    merchant = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    balance_after = Column(Float, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, customer={self.customer_id}, amount={self.amount}, category='{self.category}')>"
