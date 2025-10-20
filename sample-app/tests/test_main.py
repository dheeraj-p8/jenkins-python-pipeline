import pytest
from app.main import app, simplify_input, process_data, calculate_result
from app.utils import (
    validate_input, sanitize_input, hash_password, 
    verify_password, validate_email, validate_alphanumeric,
    sanitize_filename
)

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test main endpoints
def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert 'Jenkins Pipeline' in data['message']

def test_health(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'OK'

def test_get_data(client):
    """Test data endpoint"""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'data' in data
    assert len(data['data']) == 5
    assert data['data'] == [1, 2, 3, 4, 5]

# Test user endpoint (SQL injection fix)
def test_user_valid_id(client):
    """Test user endpoint with valid ID"""
    response = client.get('/user?id=123')
    assert response.status_code == 200
    data = response.get_json()
    assert 'validated' in data['message']

def test_user_invalid_id(client):
    """Test user endpoint with invalid ID"""
    response = client.get('/user?id=123;DROP TABLE users')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_user_no_id(client):
    """Test user endpoint without ID"""
    response = client.get('/user')
    assert response.status_code == 400

# Test ping endpoint (command injection fix)
def test_ping_valid_host(client):
    """Test ping endpoint with valid host"""
    response = client.get('/ping?host=localhost')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'simulated'

def test_ping_invalid_host(client):
    """Test ping endpoint with invalid host"""
    response = client.get('/ping?host=localhost;rm -rf /')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

# Test hello endpoint (XSS fix)
def test_hello_safe_name(client):
    """Test hello endpoint with safe name"""
    response = client.get('/hello?name=World')
    assert response.status_code == 200
    assert b'Hello World!' in response.data

def test_hello_xss_attempt(client):
    """Test hello endpoint with XSS attempt"""
    response = client.get('/hello?name=alert("xss")')
    assert response.status_code == 200
    # Should escape the script tags
    assert b'' not in response.data
    assert b'<script>' in response.data

def test_hello_no_name(client):
    """Test hello endpoint without name"""
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'Hello World!' in response.data

# Test redirect endpoint
def test_redirect_valid(client):
    """Test redirect with valid relative URL"""
    response = client.get('/redirect?url=/', follow_redirects=False)
    assert response.status_code == 302

def test_redirect_invalid_domain(client):
    """Test redirect with invalid domain"""
    response = client.get('/redirect?url=http://evil.com')
    assert response.status_code == 400

# Test utility functions
def test_simplify_input_valid():
    """Test simplify_input with valid input"""
    assert simplify_input('test') == 'test'
    assert simplify_input('  test  ') == '  test  '

def test_simplify_input_invalid():
    """Test simplify_input with invalid input"""
    assert simplify_input('') == ''
    assert simplify_input('   ') == ''
    assert simplify_input(None) == ''

def test_process_data():
    """Test process_data function"""
    result = process_data([1, 2, -1, 3])
    assert result == [2, 4, 0, 6]
    
    result = process_data([0, -5, 10])
    assert result == [0, 0, 20]

def test_calculate_result():
    """Test calculate_result function"""
    assert calculate_result(5, 'add') == 10  # 0+1+2+3+4
    assert calculate_result(5, 'multiply') == 10
    assert calculate_result(5, 'square') == 25
    assert calculate_result(5, 'invalid') == 0
    assert calculate_result(0, 'add') == 0
    assert calculate_result(-5, 'add') == 0

# Test app.utils functions
def test_validate_input():
    """Test input validation"""
    assert validate_input('test') == True
    assert validate_input('') == False
    assert validate_input(None) == False
    assert validate_input('   ') == False
    assert validate_input('a' * 1001) == False  # Too long

def test_sanitize_input():
    """Test input sanitization"""
    result = sanitize_input('alert("xss")')
    assert '' not in result
    assert '<' in result or 'script' not in result
    
    assert sanitize_input('') == ''
    assert sanitize_input(None) == ''

def test_hash_password():
    """Test password hashing"""
    password = 'SecurePassword123!'
    hashed = hash_password(password)
    
    # Should not be the original password
    assert hashed != password
    
    # Should be a string
    assert isinstance(hashed, str)
    
    # Should have reasonable length
    assert len(hashed) > 20

def test_verify_password():
    """Test password verification"""
    password = 'SecurePassword123!'
    hashed = hash_password(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) == True
    
    # Wrong password should not verify
    assert verify_password('WrongPassword', hashed) == False

def test_validate_email():
    """Test email validation"""
    assert validate_email('test@example.com') == True
    assert validate_email('user.name@domain.co.uk') == True
    assert validate_email('invalid-email') == False
    assert validate_email('@example.com') == False
    assert validate_email('test@') == False

def test_validate_alphanumeric():
    """Test alphanumeric validation"""
    assert validate_alphanumeric('abc123') == True
    assert validate_alphanumeric('test') == True
    assert validate_alphanumeric('123') == True
    assert validate_alphanumeric('test@123') == False
    assert validate_alphanumeric('test 123') == False

def test_sanitize_filename():
    """Test filename sanitization"""
    assert sanitize_filename('test.txt') == 'test.txt'
    assert sanitize_filename('../../../etc/passwd') == 'passwd'
    assert sanitize_filename('file with spaces.txt') == 'filewithspaces.txt'
    assert sanitize_filename('test.txt') == 'testscript.txt'