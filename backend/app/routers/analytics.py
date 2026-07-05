"""
Nirikshak.AI — Analytics Router
==================================
Endpoints for the Admin/Analyst dashboard — aggregate stats and charts.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict

from app.database import get_db
from app.models.customer import Customer
from app.models.trigger import Trigger
from app.models.feedback import Feedback
from app.models.transaction import Transaction

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class AnalyticsOverview(BaseModel):
    """Aggregate stats for the admin dashboard."""
    total_customers: int
    total_triggers: int
    total_accepted: int
    total_dismissed: int
    acceptance_rate: float
    total_transactions: int
    trigger_type_breakdown: List[Dict]
    recent_triggers: List[Dict]
    conversion_trend: List[Dict]


@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(db: Session = Depends(get_db)):
    """
    Get aggregate analytics for the admin dashboard.
    Shows nudges triggered, conversion rate, top trigger types.
    """
    total_customers = db.query(Customer).count()
    total_triggers = db.query(Trigger).count()
    total_accepted = db.query(Trigger).filter(Trigger.status == "accepted").count()
    total_dismissed = db.query(Trigger).filter(Trigger.status == "dismissed").count()
    total_transactions = db.query(Transaction).count()

    # Acceptance rate
    total_responded = total_accepted + total_dismissed
    acceptance_rate = (total_accepted / total_responded * 100) if total_responded > 0 else 0.0

    # Trigger type breakdown
    type_counts = defaultdict(lambda: {"total": 0, "accepted": 0, "dismissed": 0, "pending": 0})
    all_triggers = db.query(Trigger).all()
    for t in all_triggers:
        type_counts[t.trigger_type]["total"] += 1
        type_counts[t.trigger_type][t.status] = type_counts[t.trigger_type].get(t.status, 0) + 1

    trigger_type_breakdown = [
        {"trigger_type": k, **v}
        for k, v in sorted(type_counts.items(), key=lambda x: x[1]["total"], reverse=True)
    ]

    # Recent triggers (last 10)
    recent = db.query(Trigger).order_by(Trigger.created_at.desc()).limit(10).all()
    recent_triggers = [
        {
            "id": t.id,
            "customer_id": t.customer_id,
            "trigger_type": t.trigger_type,
            "product_recommended": t.product_recommended,
            "status": t.status,
            "confidence": t.confidence,
            "created_at": t.created_at.isoformat() if t.created_at else "",
        }
        for t in recent
    ]

    # Mock conversion trend (daily for last 7 days)
    conversion_trend = [
        {"day": f"Day {i+1}", "nudges": max(0, total_triggers // 7 + (i % 3)), "accepted": max(0, total_accepted // 7 + (i % 2))}
        for i in range(7)
    ]

    return AnalyticsOverview(
        total_customers=total_customers,
        total_triggers=total_triggers,
        total_accepted=total_accepted,
        total_dismissed=total_dismissed,
        acceptance_rate=round(acceptance_rate, 1),
        total_transactions=total_transactions,
        trigger_type_breakdown=trigger_type_breakdown,
        recent_triggers=recent_triggers,
        conversion_trend=conversion_trend,
    )
