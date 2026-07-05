"""
Nirikshak.AI — Transactions Router
=====================================
Endpoints for customer transaction data.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse, TransactionCreate

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List transactions with optional filtering."""
    query = db.query(Transaction)

    if customer_id:
        query = query.filter(Transaction.customer_id == customer_id)
    if category:
        query = query.filter(Transaction.category == category)

    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a single transaction by ID."""
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.post("/", response_model=TransactionResponse)
def create_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction."""
    db_txn = Transaction(**txn.model_dump())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn
