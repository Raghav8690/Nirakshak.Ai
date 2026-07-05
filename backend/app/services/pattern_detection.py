"""
Nirikshak.AI — Pattern Detection Engine
==========================================
Rule-based signal scanner that detects life events and financial patterns
from customer transaction data. Designed to be pluggable for ML models.

Detected Patterns:
  1. rent_no_insurance  — 3+ months of rent payments with no insurance premium
  2. salary_hike        — Salary credit increased by >20% compared to average
  3. dormant_savings    — No significant debit activity for 60+ days
  4. emi_ending         — Recurring EMI payments about to end (last 2 months)
  5. high_spend_category — Spending >40% of income in a single category
  6. large_withdrawal   — Single withdrawal >50% of monthly income
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.transaction import Transaction
from app.models.customer import Customer


class PatternDetector:
    """
    Scans a customer's transaction history for actionable patterns.
    Each detection method returns a list of signal dictionaries.
    """

    def __init__(self, db: Session):
        self.db = db

    def scan_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """Run all detection rules for a customer and return found signals."""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return []

        transactions = (
            self.db.query(Transaction)
            .filter(Transaction.customer_id == customer_id)
            .order_by(Transaction.date.desc())
            .all()
        )

        if not transactions:
            return []

        signals = []
        signals.extend(self._detect_rent_no_insurance(customer, transactions))
        signals.extend(self._detect_salary_hike(customer, transactions))
        signals.extend(self._detect_dormant_savings(customer, transactions))
        signals.extend(self._detect_emi_ending(customer, transactions))
        signals.extend(self._detect_high_spend_category(customer, transactions))
        signals.extend(self._detect_large_withdrawal(customer, transactions))

        return signals

    def _detect_rent_no_insurance(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: Customer pays rent for 3+ months but has no insurance premium."""
        rent_months = set()
        has_insurance = False

        for txn in transactions:
            if txn.category == "Rent" and txn.transaction_type == "debit":
                rent_months.add(txn.date.strftime("%Y-%m"))
            if txn.category == "Insurance" and txn.transaction_type == "debit":
                has_insurance = True

        if len(rent_months) >= 3 and not has_insurance:
            avg_rent = sum(
                t.amount for t in transactions
                if t.category == "Rent" and t.transaction_type == "debit"
            ) / len(rent_months)
            return [{
                "trigger_type": "rent_no_insurance",
                "signal_detected": (
                    f"Customer has been paying rent (~₹{avg_rent:,.0f}/month) "
                    f"for {len(rent_months)} months with no insurance coverage detected."
                ),
                "confidence": 0.85,
                "data": {
                    "rent_months": len(rent_months),
                    "avg_rent": avg_rent,
                    "has_insurance": False,
                },
            }]
        return []

    def _detect_salary_hike(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: Recent salary credit increased by >20%."""
        salary_txns = sorted(
            [t for t in transactions if t.category == "Salary" and t.transaction_type == "credit"],
            key=lambda t: t.date,
        )

        if len(salary_txns) < 3:
            return []

        recent = salary_txns[-1].amount
        avg_previous = sum(t.amount for t in salary_txns[:-1]) / len(salary_txns[:-1])

        if avg_previous > 0 and (recent - avg_previous) / avg_previous > 0.20:
            increase_pct = ((recent - avg_previous) / avg_previous) * 100
            return [{
                "trigger_type": "salary_hike",
                "signal_detected": (
                    f"Salary increased by {increase_pct:.0f}% — "
                    f"from ₹{avg_previous:,.0f} to ₹{recent:,.0f}."
                ),
                "confidence": 0.90,
                "data": {
                    "previous_avg": avg_previous,
                    "current_salary": recent,
                    "increase_percentage": increase_pct,
                },
            }]
        return []

    def _detect_dormant_savings(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: No significant debit activity for 60+ days."""
        cutoff = datetime.utcnow() - timedelta(days=60)
        recent_debits = [
            t for t in transactions
            if t.transaction_type == "debit" and t.date >= cutoff and t.amount > 500
        ]

        if len(recent_debits) == 0:
            return [{
                "trigger_type": "dormant_savings",
                "signal_detected": (
                    "Account shows no significant debit activity in the last 60 days. "
                    "Savings may be idle and could benefit from investment."
                ),
                "confidence": 0.75,
                "data": {"days_inactive": 60, "threshold_amount": 500},
            }]
        return []

    def _detect_emi_ending(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: Recurring EMI payments — potential refinance or new loan opportunity."""
        emi_txns = [t for t in transactions if t.category == "EMI" and t.transaction_type == "debit"]

        if len(emi_txns) >= 3:
            avg_emi = sum(t.amount for t in emi_txns) / len(emi_txns)
            return [{
                "trigger_type": "emi_ending",
                "signal_detected": (
                    f"Customer has {len(emi_txns)} recurring EMI payments "
                    f"(avg ₹{avg_emi:,.0f}/month). Consider refinancing or upgrade offers."
                ),
                "confidence": 0.70,
                "data": {"emi_count": len(emi_txns), "avg_emi": avg_emi},
            }]
        return []

    def _detect_high_spend_category(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: Spending >40% of income in a single non-essential category."""
        category_spend = defaultdict(float)
        for t in transactions:
            if t.transaction_type == "debit":
                category_spend[t.category] += t.amount

        total_debits = sum(category_spend.values())
        if total_debits == 0:
            return []

        signals = []
        for category, amount in category_spend.items():
            if category in ("Salary", "Investment", "Insurance"):
                continue
            ratio = amount / total_debits
            if ratio > 0.40:
                signals.append({
                    "trigger_type": "high_spend_category",
                    "signal_detected": (
                        f"Customer spends {ratio * 100:.0f}% of outflow "
                        f"(₹{amount:,.0f}) on {category}."
                    ),
                    "confidence": 0.65,
                    "data": {"category": category, "amount": amount, "ratio": ratio},
                })
        return signals

    def _detect_large_withdrawal(
        self, customer: Customer, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect: Single withdrawal exceeding 50% of monthly income."""
        income = customer.monthly_income
        if income <= 0:
            return []

        large = [
            t for t in transactions
            if t.transaction_type == "debit" and t.amount > income * 0.5
        ]

        if large:
            biggest = max(large, key=lambda t: t.amount)
            return [{
                "trigger_type": "large_withdrawal",
                "signal_detected": (
                    f"Large withdrawal of ₹{biggest.amount:,.0f} detected "
                    f"({biggest.amount / income * 100:.0f}% of monthly income)."
                ),
                "confidence": 0.60,
                "data": {
                    "amount": biggest.amount,
                    "income_ratio": biggest.amount / income,
                    "date": biggest.date.isoformat(),
                },
            }]
        return []
