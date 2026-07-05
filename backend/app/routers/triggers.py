"""
Nirikshak.AI — Triggers (Nudges) Router
==========================================
Endpoints for viewing and scanning for proactive product triggers.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.trigger import Trigger
from app.models.customer import Customer
from app.schemas.trigger import TriggerResponse, TriggerScanRequest, TriggerScanResponse
from app.services.pattern_detection import PatternDetector
from app.services.rag_engine import RAGReasoningEngine

router = APIRouter(prefix="/api/triggers", tags=["Triggers"])


@router.get("/", response_model=List[TriggerResponse])
def list_triggers(
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List all triggers/nudges with optional filtering."""
    query = db.query(Trigger)

    if customer_id:
        query = query.filter(Trigger.customer_id == customer_id)
    if status:
        query = query.filter(Trigger.status == status)

    triggers = query.order_by(Trigger.created_at.desc()).offset(skip).limit(limit).all()
    return triggers


@router.get("/{trigger_id}", response_model=TriggerResponse)
def get_trigger(trigger_id: int, db: Session = Depends(get_db)):
    """Get a single trigger with full reasoning trace."""
    trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    return trigger


@router.post("/scan", response_model=TriggerScanResponse)
def scan_for_triggers(request: TriggerScanRequest, db: Session = Depends(get_db)):
    """
    Scan a customer's data for new triggers.
    This runs the full pipeline: Pattern Detection → RAG Reasoning → Trigger Creation.
    """
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Step 1: Detect patterns
    detector = PatternDetector(db)
    signals = detector.scan_customer(request.customer_id)

    # Step 2: For each signal, run RAG reasoning and create a trigger
    rag_engine = RAGReasoningEngine(db)
    created_triggers = []

    for signal in signals:
        # Check if this trigger type already exists and is pending
        existing = db.query(Trigger).filter(
            Trigger.customer_id == request.customer_id,
            Trigger.trigger_type == signal["trigger_type"],
            Trigger.status == "pending",
        ).first()

        if existing:
            continue  # Don't create duplicate triggers

        # Run RAG reasoning
        recommendation = rag_engine.evaluate(request.customer_id, signal)

        # Create trigger
        trigger = Trigger(
            customer_id=request.customer_id,
            trigger_type=signal["trigger_type"],
            signal_detected=signal["signal_detected"],
            product_recommended=recommendation["product_recommended"],
            product_category=recommendation["product_category"],
            explanation=recommendation["explanation"],
            reasoning_trace=recommendation.get("reasoning_trace"),
            confidence=recommendation["confidence"],
            status="pending",
        )
        db.add(trigger)
        db.commit()
        db.refresh(trigger)
        created_triggers.append(trigger)

    return TriggerScanResponse(
        customer_id=request.customer_id,
        triggers_found=len(created_triggers),
        triggers=created_triggers,
    )
