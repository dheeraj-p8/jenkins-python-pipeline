"""
Unit tests for Flask application
"""
import pytest
from app.main import app, unnecessary_complexity, process_data_one
from app.utils import validate_input, sanitize_input

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data

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

def test_unnecessary_complexity():
    """Test unnecessary complexity function"""
    assert unnecessary_complexity('test') == 'test'
    assert unnecessary_complexity('') == ''
    assert unnecessary_complexity(None) == ''

def test_process_data():
    """Test process data function"""
    result = process_data_one([1, 2, -1, 3])
    assert result == [2, 4, 0, 6]

def test_validate_input():
    """Test input validation"""
    assert validate_input('test') == True
    assert validate_input('') == False
    assert validate_input(None) == False

def test_sanitize_input():
    """Test input sanitization"""
    result = sanitize_input('alert("xss")')
    assert '' not in result