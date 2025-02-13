import re

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email address")

def validate_phone(phone):
    if not re.match(r"^\d{10}$", phone):
        raise ValueError("Invalid phone number")

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

def validate_aaa_card(aaa_card):
    if not re.match(r"^\d{12}$", aaa_card):
        raise ValueError("Invalid AAA card number")