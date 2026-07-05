"""
Nirikshak.AI — Database Connection
====================================
SQLAlchemy engine, session factory, and base model.
Defaults to SQLite for zero-config dev; switch to PostgreSQL via DATABASE_URL env var.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# ---- Engine Setup ----
# SQLite needs connect_args for thread safety; PostgreSQL does not.
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

# ---- Session Factory ----
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---- Base Model ----
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session per request.
    Usage in routers: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
