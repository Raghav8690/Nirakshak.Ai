"""
Nirikshak.AI — Transaction Data Generator
============================================
Generates realistic transaction histories for each customer.
Intentionally embeds detectable patterns (rent without insurance, salary hikes, etc.)
so the Pattern Detection Engine has signals to find during demos.
"""

import random
from datetime import datetime, timedelta

# Transaction categories with typical merchants
CATEGORY_MERCHANTS = {
    "Salary": ["Employer Payroll", "Company Direct"],
    "Rent": ["Landlord Transfer", "Housing Society"],
    "EMI": ["HDFC Home Loan", "Bajaj Finance", "SBI Auto Loan"],
    "Groceries": ["BigBasket", "DMart", "Reliance Fresh", "More Supermarket"],
    "Insurance": ["SBI Life", "LIC Premium", "Star Health"],
    "Investment": ["SBI MF SIP", "Zerodha", "Groww"],
    "Entertainment": ["Netflix", "Spotify", "PVR Cinemas", "BookMyShow"],
    "Travel": ["MakeMyTrip", "IRCTC", "Uber", "Ola"],
    "UPI": ["Google Pay Transfer", "PhonePe", "Paytm"],
    "Utilities": ["Electricity Bill", "Water Bill", "Gas Bill", "Internet Bill"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Nykaa"],
    "Other": ["ATM Withdrawal", "Cash Deposit", "Miscellaneous"],
}


def generate_transactions(customers: list, months: int = 6) -> list:
    """
    Generate transaction history for all customers over the specified months.
    Embeds patterns for the Pattern Detection Engine to discover.
    """
    all_transactions = []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=months * 30)

    for customer in customers:
        customer_id = customers.index(customer) + 1
        income = customer["monthly_income"]
        balance = income * 2  # Starting balance

        # ---- Decide which patterns to embed for this customer ----
        patterns = _decide_patterns(customer)

        # Generate month by month
        current_date = start_date
        month_count = 0
        while current_date < end_date:
            month_txns = _generate_monthly_transactions(
                customer_id, customer, income, balance, current_date, patterns, month_count
            )
            for txn in month_txns:
                if txn["transaction_type"] == "credit":
                    balance += txn["amount"]
                else:
                    balance -= txn["amount"]
                txn["balance_after"] = round(max(0, balance), 2)
                all_transactions.append(txn)

            current_date += timedelta(days=30)
            month_count += 1

    return all_transactions


def _decide_patterns(customer: dict) -> dict:
    """Decide which detectable patterns to embed for this customer."""
    return {
        "has_rent": random.random() < 0.6,        # 60% pay rent
        "has_insurance": random.random() < 0.3,    # Only 30% have insurance
        "has_emi": random.random() < 0.4,          # 40% have EMIs
        "salary_hike": random.random() < 0.3,      # 30% get a salary hike
        "has_investment": random.random() < 0.25,   # 25% invest
        "dormant_period": random.random() < 0.2,    # 20% have a dormant period
        "large_withdrawal": random.random() < 0.15, # 15% have large withdrawals
    }


def _generate_monthly_transactions(
    customer_id: int,
    customer: dict,
    income: float,
    balance: float,
    month_start: datetime,
    patterns: dict,
    month_index: int,
) -> list:
    """Generate all transactions for a single month."""
    txns = []

    # ---- Salary Credit (1st-5th of month) ----
    salary_day = random.randint(1, 5)
    salary_amount = income

    # Embed salary hike in the last month
    if patterns["salary_hike"] and month_index >= 5:
        salary_amount = income * random.uniform(1.25, 1.50)  # 25-50% hike

    txns.append({
        "customer_id": customer_id,
        "amount": round(salary_amount, 2),
        "transaction_type": "credit",
        "category": "Salary",
        "merchant": "Employer Payroll",
        "description": f"Monthly salary credit",
        "date": (month_start + timedelta(days=salary_day)).isoformat(),
    })

    # ---- Rent (if applicable) ----
    if patterns["has_rent"]:
        rent = round(income * random.uniform(0.20, 0.35), 2)
        txns.append({
            "customer_id": customer_id,
            "amount": rent,
            "transaction_type": "debit",
            "category": "Rent",
            "merchant": "Landlord Transfer",
            "description": "Monthly rent payment",
            "date": (month_start + timedelta(days=random.randint(1, 5))).isoformat(),
        })

    # ---- EMI (if applicable) ----
    if patterns["has_emi"]:
        emi = round(income * random.uniform(0.10, 0.25), 2)
        txns.append({
            "customer_id": customer_id,
            "amount": emi,
            "transaction_type": "debit",
            "category": "EMI",
            "merchant": random.choice(CATEGORY_MERCHANTS["EMI"]),
            "description": "Monthly EMI payment",
            "date": (month_start + timedelta(days=random.randint(5, 10))).isoformat(),
        })

    # ---- Insurance Premium (only if has_insurance) ----
    if patterns["has_insurance"]:
        premium = round(random.uniform(500, 3000), 2)
        txns.append({
            "customer_id": customer_id,
            "amount": premium,
            "transaction_type": "debit",
            "category": "Insurance",
            "merchant": random.choice(CATEGORY_MERCHANTS["Insurance"]),
            "description": "Insurance premium",
            "date": (month_start + timedelta(days=random.randint(10, 15))).isoformat(),
        })

    # ---- Investment (only if has_investment) ----
    if patterns["has_investment"]:
        sip = round(random.uniform(1000, 10000), 2)
        txns.append({
            "customer_id": customer_id,
            "amount": sip,
            "transaction_type": "debit",
            "category": "Investment",
            "merchant": random.choice(CATEGORY_MERCHANTS["Investment"]),
            "description": "SIP investment",
            "date": (month_start + timedelta(days=random.randint(5, 15))).isoformat(),
        })

    # ---- Skip other spending in dormant months ----
    if patterns["dormant_period"] and month_index in [3, 4]:
        return txns  # Only salary comes in, minimal spending

    # ---- Regular Spending (Groceries, Utilities, etc.) ----
    spending_categories = ["Groceries", "Utilities", "Shopping", "Entertainment", "Travel", "UPI"]
    num_txns = random.randint(5, 12)
    for _ in range(num_txns):
        category = random.choice(spending_categories)
        amount_ranges = {
            "Groceries": (200, 5000),
            "Utilities": (500, 3000),
            "Shopping": (300, 15000),
            "Entertainment": (100, 3000),
            "Travel": (200, 8000),
            "UPI": (50, 5000),
        }
        low, high = amount_ranges.get(category, (100, 3000))
        amount = round(random.uniform(low, high), 2)

        txns.append({
            "customer_id": customer_id,
            "amount": amount,
            "transaction_type": "debit",
            "category": category,
            "merchant": random.choice(CATEGORY_MERCHANTS.get(category, ["Merchant"])),
            "description": f"{category} purchase",
            "date": (month_start + timedelta(days=random.randint(1, 28))).isoformat(),
        })

    # ---- Large Withdrawal (rare) ----
    if patterns["large_withdrawal"] and month_index == 4:
        large_amount = round(income * random.uniform(0.6, 1.2), 2)
        txns.append({
            "customer_id": customer_id,
            "amount": large_amount,
            "transaction_type": "debit",
            "category": "Other",
            "merchant": "ATM Withdrawal",
            "description": "Large cash withdrawal",
            "date": (month_start + timedelta(days=random.randint(10, 20))).isoformat(),
        })

    return txns
