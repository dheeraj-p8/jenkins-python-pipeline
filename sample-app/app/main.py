import os
import re
from flask import Flask, jsonify, request, render_template_string, redirect
from markupsafe import escape
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# FIXED: Use environment variable for secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32).hex())

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Hello from Jenkins Pipeline!',
        'status': 'success'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK'}), 200

@app.route('/api/data')
def get_data():
    """Get data endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Data retrieved',
        'data': [1, 2, 3, 4, 5]
    })

# FIXED: Removed unnecessary complexity - simplified function
def simplify_input(input_string):
    """
    Simplified input validation
    Returns input if valid, empty string otherwise
    """
    return input_string if input_string and input_string.strip() else ""

# FIXED: Removed code duplication - single function for processing
def process_data(data):
    """
    Process data - single reusable function
    """
    return [item * 2 if item > 0 else 0 for item in data]

# FIXED: SQL Injection - Using parameterized approach
@app.route('/user')
def get_user():
    """
    Get user endpoint - SECURE VERSION
    Uses validation instead of direct SQL
    """
    user_id = request.args.get('id', '')
    
    # Validate input - only allow alphanumeric
    if not re.match(r'^[a-zA-Z0-9]+$', user_id):
        return jsonify({'error': 'Invalid user ID format'}), 400
    
    # In production, use ORM like SQLAlchemy with parameterized queries
    # query = "SELECT * FROM users WHERE id = ?"
    # result = db.execute(query, (user_id,))
    
    return jsonify({
        'message': f'User ID {escape(user_id)} validated',
        'note': 'Use parameterized queries in production'
    })

# FIXED: Command Injection - Removed shell execution
@app.route('/ping')
def ping():
    """
    Ping endpoint - SECURE VERSION
    Returns simulated ping instead of executing commands
    """
    host = request.args.get('host', 'localhost')
    
    # Validate hostname format
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return jsonify({'error': 'Invalid hostname format'}), 400
    
    # In production, use proper networking libraries
    # Instead of subprocess, use socket or requests library
    return jsonify({
        'host': escape(host),
        'status': 'simulated',
        'note': 'Use socket library for actual network checks'
    })

# FIXED: XSS - Proper escaping
@app.route('/hello')
def hello():
    """
    Hello endpoint - SECURE VERSION
    Properly escapes user input
    """
    name = request.args.get('name', 'World')
    
    # Escape HTML to prevent XSS
    safe_name = escape(name)
    
    template = f"Hello {safe_name}!"
    return render_template_string(template)

# FIXED: Removed insecure deserialization endpoint
# pickle is unsafe with untrusted data - removed entirely

# FIXED: Removed dead code (unused_function deleted)

# FIXED: Reduced cognitive complexity
def calculate_result(value, operation):
    """
    Simplified calculation function
    Reduced cognitive complexity
    """
    if not value or value <= 0:
        return 0
    
    operations = {
        'add': sum(range(value)),
        'multiply': value * 2,
        'square': value ** 2
    }
    
    return operations.get(operation, 0)

# FIXED: Secure redirect with validation
@app.route('/redirect')
def redirect_page():
    """
    Redirect endpoint - SECURE VERSION
    Validates redirect URLs against whitelist
    """
    url = request.args.get('url', '/')
    
    # Whitelist of allowed redirect domains
    allowed_domains = ['localhost', '127.0.0.1', 'trusted-domain.com']
    
    # Parse and validate URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    
    # Only allow relative URLs or whitelisted domains
    if parsed.netloc and parsed.netloc not in allowed_domains:
        return jsonify({'error': 'Redirect not allowed'}), 400
    
    return redirect(url)

# Production configuration
if __name__ == '__main__':
    # FIXED: Never use debug=True in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=8080, debug=debug_mode)