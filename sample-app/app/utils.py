from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import re

def hash_password(password):
    """
    Hash a password using secure algorithm
    FIXED: Using bcrypt via werkzeug instead of MD5
    """
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, password_hash):
    """
    Verify a password against its hash
    """
    return check_password_hash(password_hash, password)

def validate_input(user_input):
    """
    Validate user input
    Enhanced validation
    """
    if not user_input:
        return False
    
    # Check if input is not just whitespace
    if not user_input.strip():
        return False
    
    # Check length
    if len(user_input) > 1000:  # Prevent DOS attacks
        return False
    
    return True

def sanitize_input(user_input):
    """
    Sanitize user input for display
    FIXED: Proper HTML escaping using markupsafe
    """
    if not user_input:
        return ""
    
    return str(escape(user_input))
    
    # Escape HTML
    #return escape(user_input)

def validate_email(email):
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_alphanumeric(text):
    """
    Validate that text contains only alphanumeric characters
    """
    return bool(re.match(r'^[a-zA-Z0-9]+$', text))

def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal
    """
    # Remove any path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    return filename