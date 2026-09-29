from datetime import datetime
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def parse_date(value):
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def is_valid_date(value):
    return parse_date(value) is not None


def normalize_date(value):
    parsed = parse_date(value)
    return parsed.strftime("%Y-%m-%d") if parsed else ""


def calculate_age(value):
    parsed = parse_date(value)
    if not parsed:
        return ""
    now = datetime.now()
    return str(now.year - parsed.year - ((now.month, now.day) < (parsed.month, parsed.day)))


def is_valid_email(value):
    return bool(EMAIL_RE.match((value or "").strip()))


def valid_number(value):
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False
