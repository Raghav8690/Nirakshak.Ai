"""
Nirikshak.AI — FastAPI Application Entry Point
=================================================
Proactive Intelligence for Life-Stage Banking
SBI Hackathon — PS-3

Starts the FastAPI server with all routers, CORS, and auto-seeding.
"""

import json
import os
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.models.trigger import Trigger
from app.models.feedback import Feedback
from app.routers import customers, transactions, triggers, feedback, reasoning, analytics


# ---- Lifespan: DB Setup + Seed Data ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup and optionally seed with demo data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    # Seed data if DB is empty
    db = SessionLocal()
    try:
        if db.query(Customer).count() == 0:
            seed_database(db)
            print("✅ Database seeded with demo data")
        else:
            print("ℹ️  Database already contains data, skipping seed")
    finally:
        db.close()

    yield  # App runs here

    print("👋 Shutting down Nirikshak.AI")


def seed_database(db):
    """Load seed data from JSON files into the database."""
    seed_dir = Path(settings.SEED_DATA_DIR)

    # Seed customers
    customers_file = seed_dir / "customers.json"
    if customers_file.exists():
        with open(customers_file, "r", encoding="utf-8") as f:
            customers_data = json.load(f)
        for c in customers_data:
            customer = Customer(
                name=c["name"],
                age=c["age"],
                gender=c["gender"],
                occupation=c["occupation"],
                monthly_income=c["monthly_income"],
                account_type=c["account_type"],
                account_number=c["account_number"],
                phone=c.get("phone"),
                email=c.get("email"),
                city=c.get("city"),
                risk_profile=c.get("risk_profile", "moderate"),
                kyc_status=c.get("kyc_status", "verified"),
                financial_health_score=c.get("financial_health_score", 65.0),
            )
            db.add(customer)
        db.commit()
        print(f"  📋 Loaded {len(customers_data)} customers")

    # Seed transactions
    transactions_file = seed_dir / "transactions.json"
    if transactions_file.exists():
        with open(transactions_file, "r", encoding="utf-8") as f:
            transactions_data = json.load(f)
        for t in transactions_data:
            txn = Transaction(
                customer_id=t["customer_id"],
                amount=t["amount"],
                transaction_type=t["transaction_type"],
                category=t["category"],
                merchant=t.get("merchant"),
                description=t.get("description"),
                date=datetime.fromisoformat(t["date"]),
                balance_after=t.get("balance_after"),
            )
            db.add(txn)
        db.commit()
        print(f"  💰 Loaded {len(transactions_data)} transactions")

    # Seed triggers (pre-generated nudges for demo)
    triggers_file = seed_dir / "triggers.json"
    if triggers_file.exists():
        with open(triggers_file, "r", encoding="utf-8") as f:
            triggers_data = json.load(f)
        for tr in triggers_data:
            trigger = Trigger(
                customer_id=tr["customer_id"],
                trigger_type=tr["trigger_type"],
                signal_detected=tr["signal_detected"],
                product_recommended=tr["product_recommended"],
                product_category=tr["product_category"],
                explanation=tr["explanation"],
                reasoning_trace=tr.get("reasoning_trace"),
                confidence=tr.get("confidence", 0.8),
                status=tr.get("status", "pending"),
            )
            db.add(trigger)
        db.commit()
        print(f"  🔔 Loaded {len(triggers_data)} triggers")


# ---- FastAPI App ----
app = FastAPI(
    title="Nirikshak.AI",
    description="Proactive Intelligence for Life-Stage Banking — SBI Hackathon PS-3",
    version="1.0.0",
    lifespan=lifespan,
)

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Register Routers ----
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(triggers.router)
app.include_router(feedback.router)
app.include_router(reasoning.router)
app.include_router(analytics.router)


@app.get("/", tags=["Health"])
def root():
    """Health check / welcome endpoint."""
    return {
        "project": "Nirikshak.AI",
        "tagline": "Proactive Intelligence for Life-Stage Banking",
        "hackathon": "SBI Hackathon — PS-3",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Simple health check."""
    return {"status": "healthy"}
