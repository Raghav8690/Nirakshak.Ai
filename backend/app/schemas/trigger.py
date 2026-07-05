"""
Nirikshak.AI — Trigger (Nudge) Schemas
"""

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class TriggerBase(BaseModel):
    customer_id: int
    trigger_type: str
    signal_detected: str
    product_recommended: str
    product_category: str
    explanation: str
    reasoning_trace: Optional[Any] = None
    confidence: float = 0.0
    status: str = "pending"


class TriggerCreate(TriggerBase):
    pass


class TriggerResponse(TriggerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TriggerScanRequest(BaseModel):
    """Request to scan a customer's data for new triggers."""
    customer_id: int


class TriggerScanResponse(BaseModel):
    """Response from a trigger scan."""
    customer_id: int
    triggers_found: int
    triggers: list[TriggerResponse]
