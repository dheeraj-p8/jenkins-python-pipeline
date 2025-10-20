# Sample Python Flask Application

A simple Flask REST API application for demonstrating Jenkins CI/CD pipeline with security scanning.

## Features
- Simple REST API endpoints
- Health check endpoint
- Dockerized application
- Infrastructure as Code (Terraform)

## Endpoints
- `GET /` - Home page
- `GET /health` - Health check
- `GET /api/data` - Sample data endpoint

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
python app/main.py
```

### Run Tests
```bash
pytest tests/ -v --cov=app --cov-report=xml --cov-report=html
```

### Run with Docker
```bash
docker build -t sample-python-app .
docker run -p 8080:8080 sample-python-app
```

## Known Issues (For Testing)
This application intentionally contains:
- Vulnerable dependencies (old requests, Jinja2, urllib3)
- Security vulnerabilities (SQL injection, XSS, command injection)
- Code smells (duplicate code, high complexity)
- Weak cryptography (MD5 hashing)
- Dead code
- Security issues in Terraform configuration

These are for pipeline testing purposes.

## Test the Application
```bash
# Home
curl http://localhost:8080/

# Health check
curl http://localhost:8080/health

# Data endpoint
curl http://localhost:8080/api/data

# Test vulnerable endpoints (for learning only!)
curl "http://localhost:8080/user?id=1"
curl "http://localhost:8080/hello?name=alert('xss')"
```
```

---

## Intentional Issues for Pipeline Testing

### 1. **Dependency Vulnerabilities (SCA)**
- `requests==2.25.1` - Has known CVEs
- `Jinja2==2.11.3` - Has security vulnerabilities
- `urllib3==1.26.5` - Outdated version
- Safety/Bandit will detect these

### 2. **Security Vulnerabilities (SAST)**
- SQL Injection in `/user` endpoint
- Command Injection in `/ping` endpoint
- XSS vulnerability in `/hello` endpoint
- Insecure deserialization in `/deserialize`
- Hardcoded secret key
- MD5 password hashing (weak algorithm)

### 3. **Code Quality Issues**
- Unnecessary complexity in `unnecessary_complexity()`
- Duplicate code in `process_data_one()` and `process_data_two()`
- Dead code (`unused_function()`)
- High cognitive complexity in `complex_calculation()`

### 4. **IaC Security Issues**
- S3 bucket without encryption
- Public S3 bucket access
- Security group open to 0.0.0.0/0
- Checkov will detect these

### 5. **Container Issues**
- Using older Python 3.9 base image
- Trivy will find vulnerabilities

---

## GitHub Repository Setup

```bash
# On your local machine
mkdir sample-python-app
cd sample-python-app
git init

# Create all files with the contents above

# Commit
git add .
git commit -m "Initial commit: Python Flask app with intentional issues"

# Create repository on GitHub, then push
git remote add origin https://github.com/YOUR_USERNAME/sample-python-app.git
git branch -M main
git push -u origin main
```

---

## Testing Locally (Optional)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app/main.py

# In another terminal, test endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/data

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run security scan (Bandit)
bandit -r app/ -f json -o bandit-report.json

# Run linting (Pylint)
pylint app/ --output-format=json > pylint-report.json