"""
Nirikshak.AI — Backend Configuration
=====================================
Loads settings from environment variables / .env file.
All config is centralised here so nothing is hardcoded elsewhere.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ---- Database ----
    DATABASE_URL: str = "sqlite:///./nirikshak.db"

    # ---- LLM Provider ----
    # "mock" = free, no API key needed (default)
    # "openai" or "claude" = requires LLM_API_KEY
    LLM_PROVIDER: str = "mock"
    LLM_API_KEY: str = ""

    # ---- ChromaDB (Vector Store) ----
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # ---- App ----
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    FRONTEND_URL: str = "http://localhost:5173"

    # ---- Seed Data Path ----
    SEED_DATA_DIR: str = str(Path(__file__).resolve().parent.parent.parent / "data" / "seed")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance used throughout the app
settings = Settings()
