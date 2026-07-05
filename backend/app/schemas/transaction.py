"""
Nirikshak.AI — Transaction Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    customer_id: int
    amount: float
    transaction_type: str  # credit, debit
    category: str
    merchant: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    balance_after: Optional[float] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
