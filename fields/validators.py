import re
from email.utils import parseaddr

def validate_name(name: str) -> bool:
    """Validate the name. It should contain only letters."""
    return name.isalpha()

def validate_phone(phone: str) -> bool:
    """Validate the phone number. It should contain only digits and be at least 10 digits long."""
    return phone.isdigit() and len(phone) >= 10 and len(phone) <= 13

def validate_email(email: str) -> bool:
    """Validate the email address."""
    return "@" in parseaddr(email)[1] and "." in email

def validate_address(address: str) -> bool:
    """Validate the address. This is a basic validation and can be expanded."""
    return len(address.strip()) > 0

def validate_birthday(birthday: str) -> bool:
    """Validate the birthday. Expected format is DD.MM.YYYY"""
    pattern = r"\d{2}.\d{2}.\d{4}"
    return re.match(pattern, birthday) is not None
