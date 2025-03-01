import hashlib
import secrets

def generate_salt():
    return secrets.token_hex(16)

def hash_password_with_salt(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()