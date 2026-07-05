"""
Nirikshak.AI — Trigger Mapper
===============================
Maps detected patterns/signals to specific SBI products.
Acts as the bridge between pattern detection and the engagement layer.
"""

from typing import Dict, Any, List


# Product catalog — maps trigger types to recommended products
PRODUCT_CATALOG = {
    "rent_no_insurance": {
        "product_name": "SBI Arogya Premier Health Insurance",
        "product_category": "Insurance",
        "description": "Comprehensive health insurance with cashless hospitalization at 10,000+ hospitals.",
        "starting_price": "₹500/month",
        "key_benefits": ["Cashless treatment", "No claim bonus", "Pre & post hospitalization cover"],
    },
    "salary_hike": {
        "product_name": "SBI Equity Mutual Fund SIP",
        "product_category": "Investment",
        "description": "Systematic Investment Plan for long-term wealth creation through equity markets.",
        "starting_price": "₹500/month",
        "key_benefits": ["Rupee cost averaging", "Tax benefits under 80C", "Professional management"],
    },
    "dormant_savings": {
        "product_name": "SBI Fixed Deposit — Special Rate",
        "product_category": "Investment",
        "description": "High-interest fixed deposit with guaranteed returns and capital safety.",
        "starting_price": "₹10,000 minimum",
        "key_benefits": ["7.1% p.a. interest", "Capital protection", "Flexible tenure"],
    },
    "emi_ending": {
        "product_name": "SBI Home Loan Balance Transfer",
        "product_category": "Loan",
        "description": "Transfer your existing home loan to SBI at lower interest rates.",
        "starting_price": "8.5% p.a.",
        "key_benefits": ["Lower EMI", "Top-up facility", "No prepayment charges"],
    },
    "high_spend_category": {
        "product_name": "SBI Cashback Credit Card",
        "product_category": "Card",
        "description": "Earn up to 5% cashback on your most frequent spending categories.",
        "starting_price": "₹499/year (waived on ₹1L spend)",
        "key_benefits": ["5% cashback", "Fuel surcharge waiver", "Welcome bonus points"],
    },
    "large_withdrawal": {
        "product_name": "SBI Personal Loan — Quick Disbursal",
        "product_category": "Loan",
        "description": "Instant personal loan with same-day disbursal for existing SBI customers.",
        "starting_price": "10.5% p.a.",
        "key_benefits": ["Same-day approval", "No collateral", "Flexible 12-60 month tenure"],
    },
}


def map_signal_to_product(trigger_type: str) -> Dict[str, Any]:
    """
    Given a trigger type, return the matching product from the catalog.
    Falls back to a generic recommendation if trigger type is unknown.
    """
    return PRODUCT_CATALOG.get(trigger_type, {
        "product_name": "SBI Smart Banking Suite",
        "product_category": "Digital",
        "description": "Explore SBI's full suite of digital banking products.",
        "starting_price": "Free",
        "key_benefits": ["Personalized offers", "24/7 banking", "Secure transactions"],
    })


def get_all_products() -> List[Dict[str, Any]]:
    """Return the full product catalog."""
    return [{"trigger_type": k, **v} for k, v in PRODUCT_CATALOG.items()]
