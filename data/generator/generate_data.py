"""
Nirikshak.AI — Synthetic Data Generator (Main Script)
=======================================================
Generates all demo data and saves to data/seed/ as JSON files.

Usage:
    cd data/generator
    python generate_data.py

This will create:
    data/seed/customers.json
    data/seed/transactions.json
    data/seed/life_events.json
    data/seed/triggers.json  (pre-generated nudges for demo)
"""

import json
import os
import sys
import random
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from customer_generator import generate_customers
from transaction_generator import generate_transactions
from life_event_generator import generate_life_events


def generate_demo_triggers(customers: list) -> list:
    """
    Pre-generate some triggers (nudges) so the demo has data to show
    immediately without needing to run the scan endpoint first.
    """
    trigger_templates = [
        {
            "trigger_type": "rent_no_insurance",
            "signal_detected": "Customer has been paying rent for 4+ months with no health insurance.",
            "product_recommended": "SBI Arogya Premier Health Insurance",
            "product_category": "Insurance",
            "explanation": "You've been consistently paying rent, showing financial discipline. However, you don't have health insurance. A medical emergency could impact your savings. SBI Arogya Premier offers coverage starting at ₹500/month.",
            "confidence": 0.87,
            "status": "pending",
            "reasoning_trace": {
                "trigger_type": "rent_no_insurance",
                "steps": [
                    "Detected consistent rent payments for 4+ months",
                    "No insurance premium transactions found",
                    "Customer profile suggests insurance gap",
                    "Retrieved SBI Arogya Premier as best-fit",
                    "Generated personalized explanation"
                ],
                "model": "MockLLM v1.0"
            }
        },
        {
            "trigger_type": "salary_hike",
            "signal_detected": "Salary increased by 30% — from ₹50,000 to ₹65,000.",
            "product_recommended": "SBI Equity Mutual Fund SIP",
            "product_category": "Investment",
            "explanation": "Congratulations on your salary increase! Start investing the extra income with an SBI Equity SIP — as little as ₹500/month for long-term wealth creation.",
            "confidence": 0.92,
            "status": "pending",
            "reasoning_trace": {
                "trigger_type": "salary_hike",
                "steps": [
                    "Detected salary increase >20%",
                    "Risk profile is moderate — equity SIP suitable",
                    "No existing investment transactions",
                    "Retrieved SBI MF SIP as best-fit",
                    "Generated explanation for incremental investment"
                ],
                "model": "MockLLM v1.0"
            }
        },
        {
            "trigger_type": "dormant_savings",
            "signal_detected": "Account shows no significant debits in 65 days. Savings may be idle.",
            "product_recommended": "SBI Fixed Deposit — Special Rate",
            "product_category": "Investment",
            "explanation": "Your savings have been idle. Idle money loses value to inflation. SBI FD offers 7.1% p.a. — your money works while staying safe.",
            "confidence": 0.78,
            "status": "accepted",
            "reasoning_trace": {
                "trigger_type": "dormant_savings",
                "steps": [
                    "No significant debits in 60+ days",
                    "Account balance suggests idle savings",
                    "Conservative risk profile",
                    "Retrieved SBI FD special rate as best-fit",
                    "Generated inflation-protection explanation"
                ],
                "model": "MockLLM v1.0"
            }
        },
        {
            "trigger_type": "emi_ending",
            "signal_detected": "Customer has 4 recurring EMI payments averaging ₹12,500/month.",
            "product_recommended": "SBI Home Loan Balance Transfer",
            "product_category": "Loan",
            "explanation": "You have active EMIs. SBI offers home loan balance transfer at 8.5% p.a. — potentially saving thousands per month.",
            "confidence": 0.72,
            "status": "dismissed",
            "reasoning_trace": {
                "trigger_type": "emi_ending",
                "steps": [
                    "Detected 4+ recurring EMI payments",
                    "Calculated EMI burden vs income",
                    "Customer may benefit from restructuring",
                    "Retrieved SBI Home Loan as best-fit",
                    "Generated savings-focused explanation"
                ],
                "model": "MockLLM v1.0"
            }
        },
        {
            "trigger_type": "high_spend_category",
            "signal_detected": "Customer spends 45% of outflow on Shopping.",
            "product_recommended": "SBI Cashback Credit Card",
            "product_category": "Card",
            "explanation": "A significant portion of your spending is on shopping. An SBI Cashback Card earns up to 5% cashback, reducing your expenses.",
            "confidence": 0.68,
            "status": "pending",
            "reasoning_trace": {
                "trigger_type": "high_spend_category",
                "steps": [
                    "Detected >40% spending in Shopping",
                    "Category matches cashback eligibility",
                    "No rewards card in portfolio",
                    "Retrieved SBI Cashback Card as best-fit",
                    "Generated savings explanation"
                ],
                "model": "MockLLM v1.0"
            }
        },
        {
            "trigger_type": "large_withdrawal",
            "signal_detected": "Large withdrawal of ₹75,000 (65% of monthly income).",
            "product_recommended": "SBI Personal Loan — Quick Disbursal",
            "product_category": "Loan",
            "explanation": "A large withdrawal was detected. If for an urgent need, SBI Personal Loan offers same-day disbursal at competitive rates to replenish savings.",
            "confidence": 0.62,
            "status": "pending",
            "reasoning_trace": {
                "trigger_type": "large_withdrawal",
                "steps": [
                    "Detected withdrawal >50% of income",
                    "Pattern suggests urgent financial need",
                    "Credit profile supports eligibility",
                    "Retrieved SBI Personal Loan as best-fit",
                    "Generated savings-replenishment explanation"
                ],
                "model": "MockLLM v1.0"
            }
        },
    ]

    triggers = []
    for i, customer in enumerate(customers):
        customer_id = i + 1
        # Assign 1-3 triggers per customer
        num_triggers = random.randint(1, min(3, len(trigger_templates)))
        selected = random.sample(trigger_templates, num_triggers)
        for template in selected:
            trigger = template.copy()
            trigger["customer_id"] = customer_id
            trigger["reasoning_trace"] = template["reasoning_trace"].copy()
            triggers.append(trigger)

    return triggers


def main():
    """Generate all synthetic data and save to data/seed/."""
    print("🔍 Nirikshak.AI — Synthetic Data Generator")
    print("=" * 50)

    # Output directory
    seed_dir = Path(__file__).resolve().parent.parent / "seed"
    seed_dir.mkdir(parents=True, exist_ok=True)

    # Set seed for reproducibility
    random.seed(42)

    # 1. Generate customers
    print("\n👤 Generating customers...")
    customers = generate_customers(20)
    with open(seed_dir / "customers.json", "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(customers)} customers saved to seed/customers.json")

    # 2. Generate transactions
    print("\n💰 Generating transactions...")
    transactions = generate_transactions(customers, months=6)
    with open(seed_dir / "transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(transactions)} transactions saved to seed/transactions.json")

    # 3. Generate life events
    print("\n📅 Generating life events...")
    events = generate_life_events(customers)
    with open(seed_dir / "life_events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(events)} life events saved to seed/life_events.json")

    # 4. Generate pre-made triggers for demo
    print("\n🔔 Generating demo triggers...")
    triggers = generate_demo_triggers(customers)
    with open(seed_dir / "triggers.json", "w", encoding="utf-8") as f:
        json.dump(triggers, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(triggers)} triggers saved to seed/triggers.json")

    # Summary
    print("\n" + "=" * 50)
    print("✅ All data generated successfully!")
    print(f"📁 Output: {seed_dir}")
    print(f"   • {len(customers)} customers")
    print(f"   • {len(transactions)} transactions")
    print(f"   • {len(events)} life events")
    print(f"   • {len(triggers)} demo triggers")


if __name__ == "__main__":
    main()
