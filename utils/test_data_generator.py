from datetime import datetime


def generate_unique_email() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"automation_{timestamp}@example.com"