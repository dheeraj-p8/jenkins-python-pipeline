import hashlib

def hash_password(password):
    """
    Hash a password
    Intentional issue: Using MD5 (weak algorithm)
    """
    return hashlib.md5(password.encode()).hexdigest()

def validate_input(user_input):
    """Validate user input"""
    if user_input and len(user_input) > 0:
        return True
    return False

def sanitize_input(user_input):
    """
    Basic input sanitization
    This is incomplete - intentional for testing
    """
    return user_input.replace('', '').replace('a', '')