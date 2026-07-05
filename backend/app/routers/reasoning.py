"""
Nirikshak.AI — Reasoning Router
==================================
Endpoint for the RAG-based reasoning evaluation.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.database import get_db
from app.services.rag_engine import RAGReasoningEngine

router = APIRouter(prefix="/api/reasoning", tags=["Reasoning"])


class ReasoningRequest(BaseModel):
    """Request to evaluate a signal through the RAG reasoning pipeline."""
    customer_id: int
    signal: Dict[str, Any]


class ReasoningResponse(BaseModel):
    """Response from RAG reasoning evaluation."""
    product_recommended: str
    product_category: str
    explanation: str
    confidence: float
    reasoning_trace: Optional[Dict[str, Any]] = None
    product_details: Optional[Dict[str, Any]] = None


@router.post("/evaluate", response_model=ReasoningResponse)
def evaluate_reasoning(request: ReasoningRequest, db: Session = Depends(get_db)):
    """
    Run the full RAG reasoning pipeline for a given signal.
    Returns the product recommendation, explanation, and reasoning trace.
    """
    engine = RAGReasoningEngine(db)
    result = engine.evaluate(request.customer_id, request.signal)
    return result
