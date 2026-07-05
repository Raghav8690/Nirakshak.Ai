"""
Nirikshak.AI — RAG Reasoning Engine
======================================
Orchestrates the full reasoning pipeline:
  1. Retrieve customer context from DB
  2. Retrieve relevant product knowledge (mock vector DB)
  3. Call LLM to generate recommendation + explanation

This is a STUB implementation for the hackathon.
The architecture supports swapping in real ChromaDB + LangChain.
No paid services are used — everything runs locally.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.transaction import Transaction
from app.services.llm_provider import get_llm_provider
from app.services.trigger_mapper import map_signal_to_product
from app.config import settings


# ---- Mock Product Knowledge Base ----
# In production, this would be stored in ChromaDB and retrieved via similarity search.
PRODUCT_KNOWLEDGE = {
    "Insurance": (
        "SBI Arogya Premier Policy: Comprehensive health insurance plan. "
        "Coverage: ₹5 lakh to ₹5 crore. Cashless hospitalization at 10,000+ hospitals. "
        "Features: No claim bonus up to 50%, pre/post hospitalization cover for 60/180 days, "
        "daycare procedures covered, annual health check-up. "
        "Premium starts from ₹500/month for individuals aged 25-35. "
        "Tax benefit under Section 80D."
    ),
    "Investment": (
        "SBI Equity Mutual Fund SIP: Systematic Investment Plan for long-term wealth creation. "
        "Minimum SIP: ₹500/month. Average 5-year return: 12-15% CAGR. "
        "Fund managed by SBI Funds Management. SEBI regulated. "
        "SBI Fixed Deposit: Special rate of 7.1% p.a. for 444 days. "
        "Senior citizen extra 0.5%. Premature withdrawal allowed with penalty."
    ),
    "Loan": (
        "SBI Home Loan: Interest rate from 8.5% p.a. EMI starting ₹750 per lakh. "
        "Loan tenure up to 30 years. No prepayment charges for floating rate. "
        "SBI Personal Loan: Rate from 10.5% p.a. Amount ₹25K to ₹20 lakh. "
        "Same-day disbursal for existing customers. No collateral required."
    ),
    "Card": (
        "SBI Cashback Credit Card: Up to 5% cashback on online spends. "
        "1% on all other purchases. Annual fee ₹499, waived on ₹1 lakh annual spend. "
        "Welcome bonus: 2000 reward points. Fuel surcharge waiver up to ₹100/month. "
        "Contactless payments enabled."
    ),
}


class RAGReasoningEngine:
    """
    Orchestrates the RAG pipeline for generating explainable product recommendations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.llm = get_llm_provider(settings.LLM_PROVIDER)

    def evaluate(
        self,
        customer_id: int,
        signal: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Full RAG reasoning pipeline:
        1. Build customer context
        2. Retrieve product knowledge
        3. Generate recommendation via LLM

        Returns a complete recommendation with explanation and reasoning trace.
        """
        # Step 1: Build customer context
        customer_context = self._build_customer_context(customer_id)

        # Step 2: Retrieve relevant product knowledge
        product_info = map_signal_to_product(signal.get("trigger_type", ""))
        product_knowledge = self._retrieve_product_knowledge(
            product_info.get("product_category", "")
        )

        # Step 3: Generate recommendation via LLM
        recommendation = self.llm.generate_recommendation(
            customer_context=customer_context,
            signal=signal,
            product_context=product_knowledge,
        )

        # Merge product info into recommendation
        recommendation["product_details"] = product_info

        return recommendation

    def _build_customer_context(self, customer_id: int) -> Dict[str, Any]:
        """Build a rich context dictionary from customer data."""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return {}

        transactions = (
            self.db.query(Transaction)
            .filter(Transaction.customer_id == customer_id)
            .order_by(Transaction.date.desc())
            .limit(100)
            .all()
        )

        # Aggregate transaction stats
        total_credits = sum(t.amount for t in transactions if t.transaction_type == "credit")
        total_debits = sum(t.amount for t in transactions if t.transaction_type == "debit")
        categories = {}
        for t in transactions:
            if t.transaction_type == "debit":
                categories[t.category] = categories.get(t.category, 0) + t.amount

        return {
            "name": customer.name,
            "age": customer.age,
            "occupation": customer.occupation,
            "monthly_income": customer.monthly_income,
            "account_type": customer.account_type,
            "risk_profile": customer.risk_profile,
            "total_credits": total_credits,
            "total_debits": total_debits,
            "top_categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]),
            "transaction_count": len(transactions),
        }

    def _retrieve_product_knowledge(self, product_category: str) -> str:
        """
        Retrieve product knowledge for the given category.
        STUB: Returns from in-memory dict.
        PRODUCTION: Would query ChromaDB with semantic similarity search.
        """
        return PRODUCT_KNOWLEDGE.get(product_category, "No specific product knowledge available.")
