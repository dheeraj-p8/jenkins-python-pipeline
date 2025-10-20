# Step 8: Testing Errors and Pipeline Scenarios (Python)

## Overview

This guide shows you how to introduce various errors in your Python application to test different pipeline stages and how to fix them.

---

## Scenario 1: Syntax Error

### Purpose
Test that pipeline catches Python syntax errors early.

### How to Introduce

Edit `app/main.py`:

```python
@app.route('/broken')
def broken_method():
    # Missing colon
    if True
        return "This will fail"
```

### Expected Result
- ✗ Stage 7 (Dry Run / Syntax Check) fails
- Pipeline stops immediately
- Error message shows syntax issue

### How to Fix
Add the colon:
```python
if True:
    return "This will fail"
```

---

## Scenario 2: Test Failure

### Purpose
Test that failing unit tests stop the pipeline.

### How to Introduce

Edit `tests/test_main.py`:

```python
def test_that_fails(client):
    """This test will fail"""
    response = client.get('/')
    data = response.get_json()
    assert data['status'] == 'WRONG_STATUS'  # This will fail
```

### Expected Result
- ✗ Stage 9 (Unit Tests) fails
- Test report shows failed test
- Pipeline stops

### How to Fix
Fix the assertion:
```python
def test_that_passes(client):
    """This test passes"""
    response = client.get('/')
    data = response.get_json()
    assert data['status'] == 'success'
```

---

## Scenario 3: Vulnerable Dependencies (SCA Failure)

### Purpose
Test Safety dependency checker.

### Already Present
The sample app already has vulnerable dependencies:

```txt
requests==2.25.1     # Has CVEs
Jinja2==2.11.3       # Has security issues
urllib3==1.26.5      # Outdated
```

### Expected Result
- ⚠ Stage 10 (SCA) completes but marks build unstable
- Safety report shows CVE details
- Build continues but marked as unstable

### How to Fix

Update `requirements.txt`:
```txt
# Updated secure versions
requests==2.31.0
Jinja2==3.1.3
urllib3==2.2.0
```

### Make It Worse (More Vulnerabilities)

Add more vulnerable packages:
```txt
# Add these vulnerable versions
Django==2.2.0          # Very old, many CVEs
Pillow==8.0.0          # Has vulnerabilities
cryptography==2.8      # Outdated crypto
pyyaml==5.1            # Unsafe loading
```

---

## Scenario 4: Security Vulnerabilities (SAST Failure)

### Purpose
Test Bandit security scanner and SonarQube.

### Already Present
The app has intentional security issues:

```python
# SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    query = f"SELECT * FROM users WHERE id = {user_id}"  # Vulnerable!
    return jsonify({'query': query})

# Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)  # Vulnerable!
    return jsonify({'result': result.decode()})

# XSS Vulnerability
@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    template = f"<html><body><h1>Hello {name}!</h1></body></html>"  # Vulnerable!
    return render_template_string(template)

# Hardcoded Secret
app.config['SECRET_KEY'] = 'hardcoded-secret-key-12345'  # Security issue!

# Weak Cryptography
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is weak!
```

### Add More Security Issues

#### 1. Path Traversal
```python
@app.route('/read-file')
def read_file():
    filename = request.args.get('file', 'data.txt')
    # Path traversal vulnerability
    with open(f"/app/files/{filename}", 'r') as f:
        return f.read()
```

#### 2. Insecure Random
```python
import random

@app.route('/token')
def generate_token():
    # Using insecure random for security-sensitive operation
    token = random.randint(1000, 9999)
    return jsonify({'token': token})
```

#### 3. Debug Mode in Production
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Debug=True is dangerous!
```

### Expected Result
- ⚠ Stage 11 (Bandit) reports HIGH severity issues
- ✗ Stage 13 (Quality Gate) fails
- Bandit shows:
  - B608: SQL injection
  - B602: Shell injection
  - B201: Flask debug mode
  - B303: MD5 usage
  - B311: Insecure random

### How to Fix

#### Fix SQL Injection
```python
from flask_sqlalchemy import SQLAlchemy

@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    # Use parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    # Or better, use ORM:
    # user = User.query.get(user_id)
    return jsonify({'message': 'Safe query'})
```

#### Fix Command Injection
```python
import shlex

@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Validate and sanitize input
    if not re.match(r'^[a-zA-Z0-9.-]+, host):
        return jsonify({'error': 'Invalid host'}), 400
    # Use list instead of shell=True
    result = subprocess.check_output(['ping', '-c', '1', host])
    return jsonify({'result': result.decode()})
```

#### Fix XSS
```python
from markupsafe import escape

@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    # Escape user input
    safe_name = escape(name)
    template = f"<html><body><h1>Hello {safe_name}!</h1></body></html>"
    return render_template_string(template)
```

#### Fix Hardcoded Secret
```python
import os

# Use environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(32)
```

#### Fix Weak Cryptography
```python
from werkzeug.security import generate_password_hash

def hash_password(password):
    # Use strong hashing (bcrypt via werkzeug)
    return generate_password_hash(password)
```

#### Fix Debug Mode
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)  # Never debug in production!
```

---

## Scenario 5: Code Quality Issues

### Purpose
Test SonarQube quality gate failures.

### Already Present

```python
# High Cognitive Complexity
def complex_calculation(value, operation):
    result = 0
    if operation == 'add':
        if value > 0:
            for i in range(value):
                if i % 2 == 0:
                    if i % 3 == 0:
                        result += i * 2
                    else:
                        result += i
                else:
                    if i % 5 == 0:
                        result -= i
    # ... more nesting
    return result

# Duplicate Code
def process_data_one(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        else:
            result.append(0)
    return result

def process_data_two(data):  # Exact duplicate!
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        else:
            result.append(0)
    return result

# Dead Code
def unused_function():
    print("This is never called")
    return None
```

### Add More Code Smells

#### 1. Too Many Parameters
```python
def complex_function(a, b, c, d, e, f, g, h, i, j):
    """Function with too many parameters"""
    return a + b + c + d + e + f + g + h + i + j
```

#### 2. Long Function
```python
def very_long_function():
    """Function with 100+ lines"""
    x = 1
    y = 2
    # ... 90 more lines of code
    return x + y
```

#### 3. Magic Numbers
```python
def calculate_price(quantity):
    if quantity > 100:
        return quantity * 0.85  # Magic number!
    elif quantity > 50:
        return quantity * 0.90  # Magic number!
    else:
        return quantity * 1.0
```

### Expected Result
- ✗ Stage 13 (Quality Gate) fails
- SonarQube shows:
  - Code Smells: 10+
  - Cognitive Complexity: High
  - Duplicated code: >3%
  - Technical Debt: Hours

### How to Fix

#### Fix Complexity
```python
def simplified_calculation(value, operation):
    """Simplified with early returns and list comprehension"""
    if operation != 'add' or value <= 0:
        return 0
    
    return sum(
        i * 2 if i % 2 == 0 and i % 3 == 0 else i 
        for i in range(value) 
        if i % 2 == 0 or i % 5 != 0
    )
```

#### Fix Duplication
```python
def process_data(data):
    """Single reusable function"""
    return [item * 2 if item > 0 else 0 for item in data]

# Use it for both cases
def process_data_one(data):
    return process_data(data)

def process_data_two(data):
    return process_data(data)
```

#### Remove Dead Code
Simply delete `unused_function()`.

#### Fix Magic Numbers
```python
# Use constants
BULK_DISCOUNT = 0.85
MEDIUM_DISCOUNT = 0.90
BULK_THRESHOLD = 100
MEDIUM_THRESHOLD = 50

def calculate_price(quantity):
    if quantity > BULK_THRESHOLD:
        return quantity * BULK_DISCOUNT
    elif quantity > MEDIUM_THRESHOLD:
        return quantity * MEDIUM_DISCOUNT
    else:
        return quantity
```

---

## Scenario 6: Low Test Coverage

### Purpose
Test quality gate failure due to insufficient coverage.

### How to Introduce

Remove tests from `tests/test_main.py`:

```python
# Comment out all tests
"""
def test_home(client):
    pass
"""
```

Or only test one function:
```python
def test_only_home(client):
    response = client.get('/')
    assert response.status_code == 200
```

### Expected Result
- ✗ Quality Gate fails
- Coverage drops to <20%
- Build fails at Stage 13

### How to Fix

Add comprehensive tests:

```python
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'OK'

def test_get_data(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert len(data['data']) == 5

def test_user_endpoint(client):
    response = client.get('/user?id=1')
    assert response.status_code == 200

def test_hello_endpoint(client):
    response = client.get('/hello?name=Test')
    assert response.status_code == 200
    assert 'Test' in response.get_data(as_text=True)

# Test utility functions
from app.utils import validate_input, sanitize_input

def test_validate_input():
    assert validate_input('test') == True
    assert validate_input('') == False
    assert validate_input(None) == False

def test_sanitize_input():
    result = sanitize_input('<script>alert("xss")</script>')
    assert '<script>' not in result
```

---

## Scenario 7: IaC Security Issues

### Purpose
Test Checkov IaC scanner.

### Already Present
The `terraform/main.tf` has intentional issues (same as before):

```hcl
# S3 bucket without encryption
resource "aws_s3_bucket" "app_bucket" {
  bucket = "my-app-bucket"
}

# Security group open to world
resource "aws_security_group" "app_sg" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### How to Fix
(Same fixes as Java version - see previous guide)

---

## Scenario 8: Container Vulnerabilities

### Purpose
Test Trivy container scanner.

### How to Introduce

Change base image in `Dockerfile` to vulnerable version:

```dockerfile
FROM python:3.6-slim  # Very old, many CVEs
```

Or use alpine with known issues:
```dockerfile
FROM python:3.9-alpine3.13  # Older alpine version
```

### Expected Result
- ⚠ Stage 16 (Container Scan) completes
- Trivy report shows HIGH/CRITICAL vulnerabilities
- Build marked unstable

### How to Fix

```dockerfile
# Use latest secure minimal image
FROM python:3.11-slim-bookworm

# Or use alpine latest
FROM python:3.11-alpine

# Best: Use distroless for security
FROM gcr.io/distroless/python3-debian12
```

---

## Scenario 9: Deployment Failure

### Purpose
Test deployment stage error handling.

### How to Introduce

#### Option 1: Port Already in Use
```bash
# Before running pipeline, manually start container on port 8080
docker run -d -p 8080:8080 nginx
```

#### Option 2: Break Health Check

Edit `app/main.py`:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'FAILED'}), 500  # Wrong status code
```

#### Option 3: Application Crash on Startup
```python
# Add this at the top of main.py
raise Exception("Application failed to start!")
```

### Expected Result
- ✗ Stage 18 (Deploy) fails
- Health check times out or fails
- Pipeline stops

### How to Fix

#### Option 1:
```bash
# Stop conflicting container
docker ps
docker stop <container-id>
```

#### Option 2:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'OK'}), 200  # Correct response
```

#### Option 3:
Remove the exception.

---

## Scenario 10: DAST Vulnerabilities

### Purpose
Test OWASP ZAP dynamic scanner.

### Already Present
The vulnerable endpoints will be detected:
- XSS in `/hello`
- SQL injection in `/user`
- Command injection in `/ping`

### Add More Issues

```python
@app.route('/redirect')
def redirect_page():
    url = request.args.get('url', '/')
    # Open redirect vulnerability
    return redirect(url)

@app.route('/download')
def download():
    file = request.args.get('file', 'data.txt')
    # Path traversal
    return send_file(f'/app/files/{file}')
```

### Expected Result
- ⚠ Stage 19 (DAST) completes
- ZAP report shows vulnerabilities
- Build marked unstable

### How to Fix

```python
from urllib.parse import urlparse

@app.route('/redirect')
def redirect_page():
    url = request.args.get('url', '/')
    # Validate against whitelist
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc not in ['trusted-domain.com']:
        return jsonify({'error': 'Invalid redirect'}), 400
    return redirect(url)

@app.route('/download')
def download():
    file = request.args.get('file', 'data.txt')
    # Sanitize filename
    safe_file = os.path.basename(file)
    filepath = os.path.join('/app/files', safe_file)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath)
```

---

## Complete Test Workflow

### Phase 1: Make Everything Fail
```
1. Add syntax error → Fails at Stage 7
2. Add failing test → Fails at Stage 9
3. Keep vulnerable dependencies → Stage 10 unstable
4. Keep security issues → Stage 11 warnings, Stage 13 fails
5. Reduce test coverage → Stage 13 fails
6. Keep IaC issues → Stage 14 warnings
7. Use vulnerable base image → Stage 16 warnings
```

**Expected**: Pipeline fails at various stages

### Phase 2: Fix Issues One by One
```
1. Fix syntax → Build passes Stage 7
2. Fix tests → Build passes Stage 9
3. Update dependencies → SCA warnings reduced
4. Fix security issues → Bandit warnings reduced
5. Add tests → Coverage increases
6. Fix IaC → Checkov warnings reduced
7. Update base image → Container scan improves
```

### Phase 3: Achieve Full Success
```
All stages: ✓ Green
Quality Gate: PASSED
Security Scans: No HIGH/CRITICAL issues
Deployment: SUCCESS
DAST: Minor or no issues
```

---

## Python-Specific Testing Tips

### Test Individual Tools Locally

```bash
# Activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=app

# Run Bandit
bandit -r app/ -f txt

# Run Safety
safety check

# Run Pylint
pylint app/

# Run app
python app/main.py
```

### Quick Fix Verification

```bash
# Check syntax without running
python3 -m py_compile app/main.py

# Run single test
pytest tests/test_main.py::test_home -v

# Check specific security issue
bandit -r app/ -ll  # Only high severity
```

---

## Monitoring and Learning

### Jenkins Console Output
```bash
# View real-time build output
Jenkins Job → Build #X → Console Output
```

### Security Reports
```
# Bandit Report
Jenkins Build → Artifacts → bandit-report.txt

# Safety Report
Jenkins Build → Artifacts → safety-report.txt

# Trivy Report
Jenkins Build → Artifacts → trivy-report.txt

# ZAP Report
Jenkins Build → OWASP ZAP DAST Report
```

### SonarQube Dashboard
```
# View code quality metrics
SonarQube → Projects → sample-python-app
- Security Hotspots
- Code Smells
- Coverage
- Duplications
```

---

## Quick Reference: Error → Stage Mapping

| Error Type | Fails At Stage | Fix Priority | Tool |
|------------|---------------|--------------|------|
| Syntax Error | 7 (Syntax Check) | Critical | Python |
| Import Error | 7 (Syntax Check) | Critical | Python |
| Test Failure | 9 (Unit Tests) | High | Pytest |
| Vulnerable Deps | 10 (SCA) | High | Safety |
| Security Issues | 11 (Bandit) | High | Bandit |
| Code Smells | 13 (Quality Gate) | Medium | SonarQube |
| Low Coverage | 13 (Quality Gate) | Medium | Pytest-cov |
| IaC Issues | 14 (IaC Scan) | Medium | Checkov |
| Container Vulns | 16 (Container Scan) | High | Trivy |
| Deploy Failure | 18 (Deploy) | Critical | Docker |
| DAST Issues | 19 (DAST) | Medium | OWASP ZAP |

---

## Next Steps

1. Run pipeline with intentional errors
2. Review each failure
3. Fix issues incrementally
4. Observe how each fix affects the pipeline
5. Achieve a fully passing pipeline
6. Introduce new errors for practice

This hands-on testing will help you understand each pipeline stage and how to debug Python applications in a real CI/CD workflow!