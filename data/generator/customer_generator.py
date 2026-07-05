"""
Nirikshak.AI — Customer Data Generator
=========================================
Generates realistic synthetic Indian bank customer profiles using Faker.
"""

from faker import Faker
import random

fake = Faker("en_IN")  # Indian locale for realistic names and cities

# Indian occupation categories
OCCUPATIONS = [
    "Software Engineer", "Data Analyst", "Teacher", "Doctor", "CA",
    "Business Owner", "Government Employee", "Marketing Manager",
    "Sales Executive", "Architect", "Lawyer", "Freelancer",
    "Startup Founder", "Bank Manager", "Civil Engineer",
    "Pharmacist", "Journalist", "Professor", "Pilot", "Chef",
]

ACCOUNT_TYPES = ["Savings", "Salary", "Current"]
RISK_PROFILES = ["conservative", "moderate", "aggressive"]
CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Bhopal", "Indore", "Nagpur", "Coimbatore",
]


def generate_customers(count: int = 20) -> list:
    """Generate a list of synthetic customer profiles."""
    customers = []
    used_account_numbers = set()

    for i in range(count):
        # Generate unique account number
        while True:
            account_number = f"SBI{random.randint(10000000, 99999999)}"
            if account_number not in used_account_numbers:
                used_account_numbers.add(account_number)
                break

        age = random.randint(22, 60)
        gender = random.choice(["Male", "Female"])

        # Income correlated with age/occupation
        base_income = random.randint(25000, 200000)
        if age > 40:
            base_income = int(base_income * 1.3)

        # Risk profile correlated with age
        if age < 30:
            risk = random.choices(RISK_PROFILES, weights=[20, 40, 40])[0]
        elif age < 45:
            risk = random.choices(RISK_PROFILES, weights=[25, 50, 25])[0]
        else:
            risk = random.choices(RISK_PROFILES, weights=[50, 35, 15])[0]

        # Financial health score (60-95 range, slightly correlated with income)
        health_score = min(95, max(40, 50 + (base_income / 5000) + random.randint(-10, 15)))

        customer = {
            "name": fake.name_male() if gender == "Male" else fake.name_female(),
            "age": age,
            "gender": gender,
            "occupation": random.choice(OCCUPATIONS),
            "monthly_income": base_income,
            "account_type": random.choice(ACCOUNT_TYPES),
            "account_number": account_number,
            "phone": fake.phone_number(),
            "email": fake.email(),
            "city": random.choice(CITIES),
            "risk_profile": risk,
            "kyc_status": random.choices(["verified", "pending"], weights=[85, 15])[0],
            "financial_health_score": round(health_score, 1),
        }
        customers.append(customer)

    return customers
