"""
Nirikshak.AI — Feedback Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeedbackBase(BaseModel):
    trigger_id: int
    customer_id: int
    action: str  # accepted, dismissed
    reason: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
