"""
Nirikshak.AI — Helper Utilities
"""

from datetime import datetime


def format_currency(amount: float) -> str:
    """Format amount in Indian Rupee notation."""
    return f"₹{amount:,.2f}"


def format_date(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%d %b %Y, %I:%M %p")
