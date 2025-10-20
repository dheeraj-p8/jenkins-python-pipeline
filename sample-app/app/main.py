"""
Main Flask Application
This file intentionally contains code quality issues for testing
"""
from flask import Flask, jsonify, request, render_template_string
import subprocess
import pickle
import os

app = Flask(__name__)

# Intentional security issue: Hardcoded secret key

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

# Intentional code smell: Unnecessary complexity (for SonarQube to detect)
def unnecessary_complexity(input_string):
    """
    This function has unnecessary complexity
    SonarQube should flag this
    """
    if input_string is not None:
        if len(input_string) > 0 and input_string != "" and not input_string.isspace():
            return input_string
    return ""

# Intentional code smell: Duplicate code
def process_data_one(data):
    """Process data method 1"""
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        else:
            result.append(0)
    return result

# Intentional security issue: SQL Injection vulnerability
@app.route('/user')
def get_user():
    """
    Get user endpoint
    SECURITY ISSUE: SQL Injection vulnerability
    """
    user_id = request.args.get('id', '')
    # This is intentionally vulnerable - DO NOT USE IN PRODUCTION
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return jsonify({'query': query, 'warning': 'This is vulnerable!'})

# Intentional security issue: Command Injection
@app.route('/ping')
def ping():
    """
    Ping endpoint
    SECURITY ISSUE: Command injection vulnerability
    """
    host = request.args.get('host', 'localhost')
    # Intentionally vulnerable - subprocess with user input
    # DO NOT USE IN PRODUCTION
    try:
        result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
        return jsonify({'result': result.decode()})
    except Exception as e:
        return jsonify({'error': str(e)})

# Intentional security issue: XSS vulnerability
@app.route('/hello')
def hello():
    """
    Hello endpoint
    SECURITY ISSUE: XSS vulnerability
    """
    name = request.args.get('name', 'World')
    # Intentionally vulnerable - no escaping
    template = f"Hello {name}!"
    return render_template_string(template)

# Intentional security issue: Insecure deserialization
@app.route('/deserialize')
def deserialize():
    """
    Deserialize endpoint
    SECURITY ISSUE: Insecure deserialization
    """
    data = request.args.get('data', '')
    if data:
        # Intentionally vulnerable - pickle with user input
        try:
            obj = pickle.loads(bytes.fromhex(data))
            return jsonify({'result': str(obj)})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'message': 'No data provided'})

# Dead code - unused function

# Simplified calculation function with better structure
def complex_calculation(value, operation):
    """
    Performs calculations based on the operation type and input value.
    
    Args:
        value (int): The input value for calculation
        operation (str): Type of operation ('add' or 'multiply')
    
    Returns:
        float: The calculated result
    """
    if value <= 0:
        return 0
        
    if operation == 'add':
        return calculate_sum(value)
    elif operation == 'multiply':
        return calculate_product(value)
    return 0

def calculate_sum(value):
    """Helper function for addition operation"""
    result = 0
    for i in range(value):
        if i % 2 == 0:
            result += i * 2 if i % 3 == 0 else i
        else:
            result += -i if i % 5 == 0 else i / 2
    return result

def calculate_product(value):
    """Helper function for multiplication operation"""
    result = 1  # Changed from 0 to 1 for multiplication
    for i in range(value):
        result *= 2 if i % 2 == 0 else 1
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)