"""Utility helper functions."""

from datetime import datetime, timezone
import random
import string
from typing import Any, Dict


def now_iso():
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat() + "Z"


def generate_code(length: int = 8, prefix: str = "") -> str:
    """Generate a random alphanumeric code."""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{code}" if prefix else code


# REMOVED: hash_password() and verify_password() using SHA-256.
# These were insecure (no salt, too fast for brute-force).
# Use ONLY app.auth.security.hash_password (bcrypt) for password hashing.


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string."""
    return dt.strftime(fmt) if dt else None


def parse_datetime(date_string: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse string to datetime object."""
    try:
        return datetime.strptime(date_string, fmt)
    except ValueError:
        return None


def get_time_difference(start: datetime, end: datetime) -> Dict[str, Any]:
    """Get time difference between two datetimes."""
    diff = end - start
    return {
        "seconds": diff.total_seconds(),
        "minutes": diff.total_seconds() / 60,
        "hours": diff.total_seconds() / 3600,
        "days": diff.days,
    }


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage safely."""
    if total == 0:
        return 0
    return round((value / total) * 100, 2)


def truncate_string(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate string to specified length."""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def sanitize_email(email: str) -> str:
    """Sanitize and validate email format."""
    return email.strip().lower()


def paginate_list(items: list, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
    """Paginate a list of items."""
    total = len(items)
    paginated_items = items[skip : skip + limit]

    return {
        "items": paginated_items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "current_page": (skip // limit) + 1 if limit > 0 else 1,
    }


def merge_dicts(*dicts) -> Dict:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def get_status_color(status: str) -> str:
    """Get color code for status badges."""
    status_colors = {
        "upcoming": "blue",
        "ongoing": "green",
        "completed": "gray",
        "cancelled": "red",
        "pending": "yellow",
        "confirmed": "green",
        "rejected": "red",
    }
    return status_colors.get(status.lower(), "default")


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency."""
    currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol} {amount:,.2f}"

