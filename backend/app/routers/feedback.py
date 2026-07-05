"""
Nirikshak.AI — Feedback Router
=================================
Endpoints for the accept/dismiss feedback loop on nudges.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.feedback import Feedback
from app.models.trigger import Trigger
from app.schemas.feedback import FeedbackResponse, FeedbackCreate

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.get("/", response_model=List[FeedbackResponse])
def list_feedback(
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List feedback entries."""
    query = db.query(Feedback)
    if customer_id:
        query = query.filter(Feedback.customer_id == customer_id)
    return query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=FeedbackResponse)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Submit feedback (accept/dismiss) on a trigger.
    Also updates the trigger status accordingly.
    """
    # Verify trigger exists
    trigger = db.query(Trigger).filter(Trigger.id == feedback.trigger_id).first()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")

    # Create feedback record
    db_feedback = Feedback(**feedback.model_dump())
    db.add(db_feedback)

    # Update trigger status
    trigger.status = feedback.action  # "accepted" or "dismissed"
    db.commit()
    db.refresh(db_feedback)

    return db_feedback
