"""
Nirikshak.AI — Feedback Model
===============================
Stores customer responses (accept/dismiss) on nudges.
This data feeds the feedback loop to improve future trigger accuracy.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer, ForeignKey("triggers.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    action = Column(String(20), nullable=False)  # accepted, dismissed
    reason = Column(Text, nullable=True)  # Optional: why the customer dismissed
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trigger = relationship("Trigger", back_populates="feedbacks")
    customer = relationship("Customer", back_populates="feedbacks")

    def __repr__(self):
        return f"<Feedback(id={self.id}, trigger={self.trigger_id}, action='{self.action}')>"
