"""
Nirikshak.AI — Life Event Generator
======================================
Generates synthetic life events for customers.
These events serve as additional signals for the Pattern Detection Engine.
"""

import random
from datetime import datetime, timedelta


EVENT_TYPES = [
    {
        "type": "salary_hike",
        "description_template": "{name} received a salary increase of {pct}% (new salary: ₹{amount:,.0f})",
        "weight": 30,
    },
    {
        "type": "new_emi",
        "description_template": "{name} started a new EMI of ₹{amount:,.0f}/month for {purpose}",
        "weight": 25,
    },
    {
        "type": "account_dormancy",
        "description_template": "{name}'s account has been dormant for {days} days with balance ₹{amount:,.0f}",
        "weight": 15,
    },
    {
        "type": "kyc_update",
        "description_template": "{name} updated KYC — address changed to {city}",
        "weight": 10,
    },
    {
        "type": "large_withdrawal",
        "description_template": "{name} made a large withdrawal of ₹{amount:,.0f}",
        "weight": 10,
    },
    {
        "type": "new_dependent",
        "description_template": "{name} added a new dependent ({relation}) to their account",
        "weight": 10,
    },
]

EMI_PURPOSES = ["Home Loan", "Car Loan", "Education Loan", "Personal Loan", "Two-Wheeler Loan"]
RELATIONS = ["Spouse", "Child", "Parent", "Sibling"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata"]


def generate_life_events(customers: list, max_events_per_customer: int = 3) -> list:
    """Generate life events for a subset of customers."""
    all_events = []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=180)

    for i, customer in enumerate(customers):
        customer_id = i + 1
        # Not every customer has life events
        num_events = random.choices(
            [0, 1, 2, 3],
            weights=[30, 40, 20, 10],
        )[0]

        for _ in range(min(num_events, max_events_per_customer)):
            event_template = random.choices(
                EVENT_TYPES,
                weights=[e["weight"] for e in EVENT_TYPES],
            )[0]

            event_date = start_date + timedelta(days=random.randint(0, 180))
            income = customer["monthly_income"]

            # Generate event-specific data
            event = {
                "customer_id": customer_id,
                "event_type": event_template["type"],
                "date": event_date.isoformat(),
            }

            if event_template["type"] == "salary_hike":
                pct = random.randint(15, 50)
                new_salary = income * (1 + pct / 100)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], pct=pct, amount=new_salary
                )
                event["data"] = {"percentage": pct, "new_salary": new_salary}

            elif event_template["type"] == "new_emi":
                emi_amount = round(income * random.uniform(0.10, 0.30), 2)
                purpose = random.choice(EMI_PURPOSES)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], amount=emi_amount, purpose=purpose
                )
                event["data"] = {"emi_amount": emi_amount, "purpose": purpose}

            elif event_template["type"] == "account_dormancy":
                days = random.randint(45, 120)
                balance = round(income * random.uniform(1, 5), 2)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], days=days, amount=balance
                )
                event["data"] = {"dormant_days": days, "balance": balance}

            elif event_template["type"] == "kyc_update":
                city = random.choice(CITIES)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], city=city
                )
                event["data"] = {"new_city": city}

            elif event_template["type"] == "large_withdrawal":
                amount = round(income * random.uniform(0.5, 2.0), 2)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], amount=amount
                )
                event["data"] = {"amount": amount}

            elif event_template["type"] == "new_dependent":
                relation = random.choice(RELATIONS)
                event["description"] = event_template["description_template"].format(
                    name=customer["name"], relation=relation
                )
                event["data"] = {"relation": relation}

            all_events.append(event)

    return all_events
