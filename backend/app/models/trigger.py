"""
Nirikshak.AI — Trigger (Nudge) Model
======================================
Represents a proactive product recommendation triggered by a detected pattern or life event.
Each trigger includes the reasoning trace for full explainability.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)

    # What was detected
    trigger_type = Column(String(50), nullable=False)
    # Types: rent_no_insurance, salary_hike, dormant_savings, emi_ending,
    #        high_spend_category, new_dependent, large_withdrawal
    signal_detected = Column(Text, nullable=False)  # Human-readable signal description

    # What is recommended
    product_recommended = Column(String(100), nullable=False)
    product_category = Column(String(50), nullable=False)  # Insurance, Investment, Loan, Card

    # Explainability
    explanation = Column(Text, nullable=False)  # "Why you're seeing this" — customer-facing
    reasoning_trace = Column(JSON, nullable=True)  # Full trace: signal → rule → LLM → product
    confidence = Column(Float, default=0.0)  # 0.0 to 1.0

    # Status
    status = Column(String(20), default="pending")  # pending, accepted, dismissed, expired

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="triggers")
    feedbacks = relationship("Feedback", back_populates="trigger")

    def __repr__(self):
        return f"<Trigger(id={self.id}, type='{self.trigger_type}', product='{self.product_recommended}')>"
