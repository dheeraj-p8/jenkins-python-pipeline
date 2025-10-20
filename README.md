# Production-Grade Jenkins CI/CD Pipeline - Complete Guide (Python Edition)

## 🎯 Overview

This comprehensive guide will help you build a **production-ready Jenkins CI/CD pipeline** with complete security scanning, quality gates, and automated deployment for **Python Flask applications**. Perfect for learning DevOps, CI/CD, and application security.

### What You'll Build

A complete CI/CD pipeline with:
- ✅ Automated builds and tests (Python/Flask)
- 🔒 Security scanning (SAST, SCA, DAST, IaC, Container)
- 📊 Code quality gates (SonarQube)
- 🐳 Docker containerization
- 🚀 Automated deployment
- 📧 Notifications
- 📈 Reporting and metrics

### Technologies Used

| Category | Tool | Purpose |
|----------|------|---------|
| **Language** | Python 3.9+ | Application code |
| **Framework** | Flask | Web framework |
| **CI/CD** | Jenkins | Orchestration |
| **SAST** | SonarQube + Bandit | Static code analysis |
| **SCA** | Safety | Dependency vulnerabilities |
| **Linting** | Pylint | Code quality |
| **Testing** | Pytest + Coverage | Unit tests |
| **IaC Scan** | Checkov | Infrastructure security |
| **Container Scan** | Trivy | Container vulnerabilities |
| **DAST** | OWASP ZAP | Dynamic security testing |
| **SCM** | GitHub | Source control |
| **Registry** | Docker Hub | Container registry |
| **Cloud** | AWS EC2 | Infrastructure |

---

## 📚 Documentation Structure

All guides are in separate files for easy following:

### Setup Guides (Start Here!)

1. **[01-ec2-setup.md](01-ec2-setup.md)**
   - Launch AWS EC2 instances
   - Configure security groups
   - Network setup

2. **[02-jenkins-installation.sh](02-jenkins-installation.sh)** ⭐ UPDATED FOR PYTHON
   - Automated Jenkins installation
   - Install Python security tools (Bandit, Safety, Pylint)
   - System configuration

3. **[03-sonarqube-docker-setup.sh](03-sonarqube-docker-setup.sh)**
   - SonarQube Docker deployment
   - PostgreSQL database
   - Container orchestration

4. **[04-jenkins-plugins.md](04-jenkins-plugins.md)**
   - Required plugins
   - Tool configuration
   - Credentials setup

### Application Files

5. **[05-sample-app/](05-sample-app/)** ⭐ PYTHON FLASK APP
   - Complete Flask REST API application
   - Unit tests with pytest
   - Dockerfile
   - Terraform IaC
   - Intentional vulnerabilities for testing

### Pipeline Configuration

6. **[06-Jenkinsfile](06-Jenkinsfile)** ⭐ PYTHON PIPELINE
   - Complete pipeline script (20 stages)
   - Python-specific stages (venv, pip, pytest)
   - All security scans
   - Quality gates
   - Deployment logic

7. **[07-quality-gates.md](07-quality-gates.md)**
   - SonarQube quality gate setup
   - Custom conditions
   - Multiple gate configurations

### Testing and Learning

8. **[08-testing-errors.md](08-testing-errors.md)** ⭐ PYTHON EXAMPLES
   - How to introduce Python errors
   - Testing each pipeline stage
   - Fixing issues step-by-step

9. **[09-setup-guide.md](09-setup-guide.md)**
   - Complete execution guide
   - Troubleshooting
   - Monitoring and maintenance

---

## 🚀 Quick Start (3 Steps)

### Step 1: Infrastructure Setup (30 minutes)

```bash
# 1. Launch EC2 instances
Follow: 01-ec2-setup.md

# 2. Install Jenkins (with Python tools)
ssh -i jenkins-key.pem ubuntu@JENKINS_IP
wget <your-github-raw-url>/02-jenkins-installation.sh
chmod +x 02-jenkins-installation.sh
sudo ./02-jenkins-installation.sh

# 3. Install SonarQube
ssh -i jenkins-key.pem ubuntu@SONARQUBE_IP
wget <your-github-raw-url>/03-sonarqube-docker-setup.sh
chmod +x 03-sonarqube-docker-setup.sh
sudo ./03-sonarqube-docker-setup.sh
```

### Step 2: Configuration (45 minutes)

```bash
# 1. Configure Jenkins
http://JENKINS_IP:8080
- Install plugins (04-jenkins-plugins.md)
- Add credentials (GitHub, Docker Hub, SonarQube)
- Configure tools

# 2. Configure SonarQube
http://SONARQUBE_IP:9000
- Change default password
- Generate token
- Create quality gate

# 3. Connect Jenkins to SonarQube
Jenkins → Configure System → SonarQube Servers
```

### Step 3: Create and Run Pipeline (30 minutes)

```bash
# 1. Create GitHub repository with Python Flask app (05-sample-app/)

# 2. Create Jenkins pipeline job
Jenkins → New Item → Pipeline
- Configure GitHub repo
- Point to Jenkinsfile

# 3. Run pipeline
Click "Build Now" and watch it execute!
```

---

## 📋 Pipeline Stages Explained

The pipeline has **20 comprehensive stages** (Python-specific):

### 🏗️ Setup & Build (Stages 1-7)
1. **Initialization** - Clean workspace, setup
2. **Checkout Code** - Clone from GitHub
3. **Verify Trigger** - Confirm build cause
4. **Environment Check** - Verify Python, pip, Docker
5. **Setup Virtual Environment** - Create Python venv
6. **Install Dependencies** - pip install requirements.txt
7. **Dry Run / Syntax Check** - py_compile validation

### 🔍 Code Quality & Testing (Stages 8-9)
8. **Code Linting (Pylint)** - Code quality analysis
9. **Unit Tests with Coverage** - pytest with coverage reports

### 🔒 Security Scanning (Stages 10-14, 16, 19)
10. **SCA (Safety)** - Check vulnerable dependencies
11. **SAST (Bandit)** - Python security issues scanner
12. **SAST (SonarQube)** - Comprehensive static analysis
13. **Quality Gate** - Enforce code quality standards
14. **IaC Scan (Checkov)** - Terraform security
16. **Container Scan (Trivy)** - Docker image vulnerabilities
19. **DAST (OWASP ZAP)** - Runtime vulnerabilities

### 🐳 Build & Deploy (Stages 15, 17-18, 20)
15. **Docker Build** - Create container image
17. **Docker Push** - Push to registry
18. **Deploy** - Run container
20. **Smoke Tests** - Verify deployment

---

## 🎓 Learning Objectives

By completing this guide, you'll learn:

### Python Development
- ✅ Flask web application development
- ✅ Python virtual environments
- ✅ Package management with pip
- ✅ Unit testing with pytest
- ✅ Code coverage analysis
- ✅ Python security best practices

### DevOps Skills
- ✅ CI/CD pipeline design for Python
- ✅ Jenkins pipeline as code (Groovy)
- ✅ Infrastructure as Code with Terraform
- ✅ Docker containerization for Python apps
- ✅ Git workflow automation

### Security Skills
- ✅ Python-specific SAST (Bandit)
- ✅ Dependency vulnerability scanning (Safety)
- ✅ Dynamic Application Security Testing (DAST)
- ✅ Infrastructure as Code security
- ✅ Container security scanning
- ✅ Vulnerability management

### Quality Assurance
- ✅ Code quality metrics for Python
- ✅ Test coverage analysis
- ✅ Quality gates implementation
- ✅ Technical debt management
- ✅ Code linting with Pylint

---

## 💡 Key Features

### 1. Python-Specific Security Scanning

Every aspect of your Python application is scanned:
```
Code → Dependencies → Infrastructure → Container → Running App
Bandit    Safety         Checkov        Trivy        ZAP
Pylint                                              
SonarQube                                            
```

### 2. Quality Gates at Multiple Levels

```
Syntax → Tests → Linting → Security → Quality → Deployment
 ✓ PASS   ✓ PASS   ✓ PASS   ✓ PASS    ✓ PASS    ✓ PASS
```

If any stage fails, pipeline stops immediately.

### 3. Intentional Vulnerabilities for Learning

The sample Flask app includes:
- 🐛 Vulnerable dependencies (old requests, Jinja2, urllib3)
- 💉 SQL Injection vulnerabilities
- 🔓 XSS (Cross-Site Scripting) issues
- 💣 Command Injection flaws
- 🔑 Hardcoded secrets
- 🔐 Weak cryptography (MD5)
- 💩 Code smells (duplication, complexity)
- 🐳 Container vulnerabilities

**Perfect for learning how to detect and fix security issues in Python!**

### 4. Production-Ready Patterns

- Virtual environment isolation
- Comprehensive test coverage
- Security-first approach
- Proper error handling
- Health checks and monitoring
- Detailed reporting

---

## 📊 Expected Results

### First Pipeline Run (With Intentional Issues)

```
✓ Stages 1-7: Pass (Setup and syntax check)
✓ Stage 8 (Linting): Pass (with warnings)
✓ Stage 9 (Tests): Pass
⚠ Stage 10 (SCA/Safety): Unstable (requests, Jinja2, urllib3 CVEs)
⚠ Stage 11 (Bandit): Unstable (SQL injection, hardcoded secrets, weak crypto)
✓ Stage 12 (SonarQube): Pass (Analysis sent)
✗ Stage 13 (Quality Gate): FAIL (Security issues, code smells, low coverage)
⏸ Stages 14-20: Skipped (Pipeline stopped)

Result: FAILED
Duration: ~6-8 minutes
```

### After Fixing Issues

```
✓ All 20 Stages: Pass
✓ Quality Gate: Passed
✓ Security Scans: No critical issues
✓ Deployment: Successful
✓ Application: Running and healthy

Result: SUCCESS
Duration: ~10-15 minutes
```

---

## 🛠️ Prerequisites

### Required Accounts
- AWS Account (with EC2 access)
- GitHub Account
- Docker Hub Account

### Local Tools
- SSH client
- Git
- Text editor (VS Code recommended)
- Web browser

### Knowledge
- Basic Python programming
- Basic Linux commands
- Basic Git operations
- Understanding of CI/CD concepts (helpful but not required)

### Budget
- **AWS Cost**: ~$70/month for 2 t3.medium instances
- **Optimization**: Use t3.small (~$50/month) or stop when not in use
- **Free Tier**: t2.micro free for first year

---

## 📈 Pipeline Execution Time

| Stage | Time | Notes |
|-------|------|-------|
| Checkout & Setup | 30s | Fast |
| Venv & Dependencies | 1-2min | First run slower (downloads) |
| Tests + Coverage | 30s-1min | Depends on test suite |
| Safety (SCA) | 30s | Fast database check |
| Bandit (SAST) | 30s | Quick Python scan |
| SonarQube + Quality Gate | 1-2min | Depends on code size |
| IaC Scan | 30s | Fast |
| Docker Build | 1-2min | Cached layers help |
| Container Scan | 1min | First run slower |
| Deploy | 30s | Local deployment |
| DAST | 2-3min | Most time-consuming |
| **Total** | **10-15min** | Optimizable to 7-10min |

---

## Python Sample Application Features

### Endpoints
```python
GET  /              # Home - JSON response
GET  /health        # Health check
GET  /api/data      # Sample data endpoint

# Intentionally vulnerable endpoints (for testing)
GET  /user?id=X     # SQL Injection vulnerability
GET  /ping?host=X   # Command Injection vulnerability
GET  /hello?name=X  # XSS vulnerability
```

### Testing Locally
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/sample-python-app.git
cd sample-python-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app/main.py

# In another terminal, test
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/data

# Run tests
pytest tests/ -v --cov=app

# Run security scans
bandit -r app/
safety check
pylint app/
```

---

## 🔧 Customization Options

### For Different Python Frameworks

**Django**:
```groovy
stage('Tests') {
    sh '''
        . ${VENV_DIR}/bin/activate
        python manage.py test
        coverage run --source='.' manage.py test
    '''
}
```

**FastAPI**:
```groovy
stage('Tests') {
    sh '''
        . ${VENV_DIR}/bin/activate
        pytest tests/ -v --cov=app
        # FastAPI-specific
        pytest --cov=app --cov-report=html tests/
    '''
}
```

**Streamlit**:
```groovy
stage('Deploy') {
    sh '''
        docker run -d \
            -p 8501:8501 \
            ${DOCKER_IMAGE}:${DOCKER_TAG}
    '''
}
```

### For Different Deployment Targets

**Kubernetes**:
```groovy
stage('Deploy to K8s') {
    sh '''
        kubectl apply -f k8s/deployment.yaml
        kubectl rollout status deployment/sample-python-app
    '''
}
```

**AWS ECS**:
```groovy
stage('Deploy to ECS') {
    sh '''
        aws ecs update-service \
            --cluster my-cluster \
            --service sample-python-app \
            --force-new-deployment
    '''
}
```

**AWS Lambda**:
```groovy
stage('Deploy Lambda') {
    sh '''
        pip install -r requirements.txt -t ./package
        cd package && zip -r ../function.zip .
        cd .. && zip -g function.zip app/*.py
        aws lambda update-function-code \
            --function-name sample-python-app \
            --zip-file fileb://function.zip
    '''
}
```

**Heroku**:
```groovy
stage('Deploy to Heroku') {
    sh '''
        git push heroku main
    '''
}
```

---

## 📖 Documentation Best Practices

Each file follows a clear structure:
- 📝 Clear explanations
- 💻 Python code examples
- ✅ Checklists
- ⚠️ Common issues
- 💡 Tips and tricks
- 🐍 Python-specific guidance

**Start with files in order (01 → 09) for best learning experience!**

---

## 🎯 Success Metrics

Track your progress:

- [ ] EC2 instances launched and accessible
- [ ] Jenkins installed with Python tools
- [ ] SonarQube running
- [ ] Python Flask app in GitHub
- [ ] Virtual environment working
- [ ] All dependencies installed
- [ ] Pipeline created
- [ ] First build executed (even if failed)
- [ ] All security reports generated
- [ ] Quality gate configured
- [ ] Python vulnerabilities identified
- [ ] Issues fixed one by one
- [ ] Successful green build achieved
- [ ] Flask application deployed and running
- [ ] All endpoints responding

---

## 🐍 Python-Specific Tips

### Virtual Environment Management
```bash
# Always use virtual environments
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Testing Best Practices
```bash
# Run specific test
pytest tests/test_main.py::test_home -v

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Run with markers
pytest -m security tests/

# Parallel execution
pytest -n auto tests/
```

### Security Scanning
```bash
# Bandit - Security issues
bandit -r app/ -ll  # High severity only
bandit -r app/ -f json -o report.json

# Safety - Dependency check
safety check --json
safety check --full-report

# Pylint - Code quality
pylint app/ --disable=C0111  # Disable specific warnings
pylint app/ --output-format=json
```

### Docker Optimization for Python
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY app/ ./app/
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app.main:app"]
```

---

## 🤝 Contributing

This is a learning project! Feel free to:
- Add more Python frameworks (Django, FastAPI)
- Improve pipeline efficiency
- Add more security checks
- Enhance documentation
- Share your customizations

---

## 📞 Support & Resources

### Official Documentation
- [Python](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/)
- [pytest](https://docs.pytest.org/)
- [Jenkins](https://www.jenkins.io/doc/)
- [SonarQube](https://docs.sonarqube.org/)
- [Bandit](https://bandit.readthedocs.io/)
- [Safety](https://pyup.io/safety/)
- [Trivy](https://aquasecurity.github.io/trivy/)
- [Checkov](https://www.checkov.io/)
- [OWASP ZAP](https://www.zaproxy.org/docs/)

### Python Security Resources
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices/)
- [Bandit Rules](https://bandit.readthedocs.io/en/latest/plugins/index.html)

### Community
- Jenkins Community Forums
- Python Discord/Slack
- Stack Overflow (#jenkins, #python, #flask)
- DevOps subreddit
- OWASP Slack

---

## ⚠️ Important Notes

### Security Considerations
- This setup is for LEARNING purposes
- For production:
  - Use VPCs and private subnets
  - Enable HTTPS/TLS
  - Use AWS Secrets Manager or HashiCorp Vault
  - Use IAM roles instead of credentials
  - Enable audit logging
  - Regular security updates
  - Use `.env` files for sensitive data (never commit!)
  - Implement rate limiting
  - Use Web Application Firewall (WAF)

### Python Best Practices in Production
```python
# Use environment variables
import os
SECRET_KEY = os.environ.get('SECRET_KEY')

# Use proper logging
import logging
logging.basicConfig(level=logging.INFO)

# Handle exceptions
try:
    # code
except Exception as e:
    logging.error(f"Error: {e}")

# Use type hints
def process_data(items: list[int]) -> list[int]:
    return [item * 2 for item in items]
```

### Cost Management
- **Stop EC2 instances when not in use**
- Use AWS Budgets to set alerts
- Consider using AWS Free Tier
- Clean up old Docker images
- Delete old builds in Jenkins
- Use spot instances for non-critical workloads

---

## 🎉 What's Next?

After completing this guide:

1. **Customize** - Adapt pipeline for your Python projects
2. **Expand** - Add more stages (load testing with Locust, mutation testing)
3. **Scale** - Move to Kubernetes, add more Jenkins agents
4. **Secure** - Implement HashiCorp Vault, add RBAC
5. **Monitor** - Add Prometheus, Grafana, ELK stack
6. **Advanced** - Blue-green deployment, canary releases
7. **Share** - Teach others, contribute back

---

## 🚦 Let's Get Started!

Ready to build your Python CI/CD pipeline? Start with **[01-ec2-setup.md](01-ec2-setup.md)**!

### Quick Navigation
```
Setup Phase:
01-ec2-setup.md → 02-jenkins-installation.sh → 03-sonarqube-docker-setup.sh → 04-jenkins-plugins.md

Application Phase:
05-sample-app/ → 06-Jenkinsfile → 07-quality-gates.md

Testing Phase:
08-testing-errors.md → 09-setup-guide.md
```

**Estimated time to complete**: 2-3 hours for first-time setup  
**Estimated learning value**: Priceless 🚀

---

## 📊 Pipeline Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          GitHub Repository                       │
│                     (Python Flask Application)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Jenkins Server                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Stage 1-7: Setup, Checkout, Venv, Dependencies, Tests    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Stage 8-13: Pylint, Safety, Bandit, SonarQube, Quality  │  │
│  │             Gate Check                                    │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │
                          ├────────────► SonarQube Server
                          │              (Code Quality Analysis)
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Build & Scan                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Stage 14-17: IaC Scan, Docker Build, Trivy Scan, Push   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Hub / Registry                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Deploy & Test (Jenkins)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Stage 18-20: Deploy Container, DAST Scan, Smoke Tests   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Running Flask  │
                    │  Application   │
                    │  (Port 8080)   │
                    └────────────────┘
```

---

## 🏆 Key Differences from Java Version

| Aspect | Java Version | Python Version |
|--------|--------------|----------------|
| Build Tool | Maven | pip + venv |
| Language | Java + Spring Boot | Python + Flask |
| Dependency File | pom.xml | requirements.txt |
| Security Scanner | OWASP Dep-Check | Safety |
| SAST Tool | SonarQube only | Bandit + SonarQube |
| Linting | Checkstyle | Pylint |
| Testing | JUnit | pytest |
| Coverage | JaCoCo | pytest-cov |
| Package | JAR file | Python files |
| Runtime | JVM | Python interpreter |
| Container Size | ~200MB | ~100MB |
| Build Time | 3-5 min | 2-4 min |

---

## 💪 Why This Guide is Different

✅ **Complete** - Every step documented, nothing assumed  
✅ **Practical** - Real code, real vulnerabilities, real fixes  
✅ **Educational** - Learn by doing, understand by breaking  
✅ **Production-Ready** - Not toy examples, actual patterns  
✅ **Security-First** - Multiple scanning tools, comprehensive coverage  
✅ **Python-Focused** - Tailored for Python developers  
✅ **Step-by-Step** - Separate files for each component  
✅ **Troubleshooting** - Common issues and solutions included  

---

## 🎓 Certificate of Completion

After finishing this guide, you'll have hands-on experience with:

- ✅ Jenkins Pipeline as Code
- ✅ Python Application Security
- ✅ DevSecOps Practices
- ✅ Container Security
- ✅ Infrastructure as Code
- ✅ CI/CD Best Practices
- ✅ AWS Cloud Deployment
- ✅ Multiple Security Tools

**Add this to your resume and portfolio!**

---

Happy building and learning! 💪🐍🚀

**Questions? Issues? Improvements?**  
Open an issue or contribute to make this guide even better!# Production-Grade Jenkins CI/CD Pipeline - Complete Guide

## 🎯 Overview

This comprehensive guide will help you build a **production-ready Jenkins CI/CD pipeline** with complete security scanning, quality gates, and automated deployment. Perfect for learning DevOps, CI/CD, and application security.

### What You'll Build

A complete CI/CD pipeline with:
- ✅ Automated builds and tests
- 🔒 Security scanning (SAST, SCA, DAST, IaC, Container)
- 📊 Code quality gates (SonarQube)
- 🐳 Docker containerization
- 🚀 Automated deployment
- 📧 Notifications
- 📈 Reporting and metrics

### Technologies Used

| Category | Tool | Purpose |
|----------|------|---------|
| **CI/CD** | Jenkins | Orchestration |
| **SAST** | SonarQube | Static code analysis |
| **SCA** | OWASP Dependency-Check | Dependency vulnerabilities |
| **IaC Scan** | Checkov | Infrastructure security |
| **Container Scan** | Trivy | Container vulnerabilities |
| **DAST** | OWASP ZAP | Dynamic security testing |
| **SCM** | GitHub | Source control |
| **Registry** | Docker Hub | Container registry |
| **Cloud** | AWS EC2 | Infrastructure |

---

## 📚 Documentation Structure

All guides are in separate files for easy following:

### Setup Guides (Start Here!)

1. **[01-ec2-setup.md](01-ec2-setup.md)**
   - Launch AWS EC2 instances
   - Configure security groups
   - Network setup

2. **[02-jenkins-installation.sh](02-jenkins-installation.sh)**
   - Automated Jenkins installation
   - Install security tools
   - System configuration

3. **[03-sonarqube-docker-setup.sh](03-sonarqube-docker-setup.sh)**
   - SonarQube Docker deployment
   - PostgreSQL database
   - Container orchestration

4. **[04-jenkins-plugins.md](04-jenkins-plugins.md)**
   - Required plugins
   - Tool configuration
   - Credentials setup

### Application Files

5. **[05-sample-app/](05-sample-app/)**
   - Complete Java Spring Boot application
   - Unit tests
   - Dockerfile
   - Terraform IaC
   - Intentional vulnerabilities for testing

### Pipeline Configuration

6. **[06-Jenkinsfile](06-Jenkinsfile)**
   - Complete pipeline script (18 stages)
   - All security scans
   - Quality gates
   - Deployment logic

7. **[07-quality-gates.md](07-quality-gates.md)**
   - SonarQube quality gate setup
   - Custom conditions
   - Multiple gate configurations

### Testing and Learning

8. **[08-testing-errors.md](08-testing-errors.md)**
   - How to introduce errors
   - Testing each pipeline stage
   - Fixing issues step-by-step

9. **[09-setup-guide.md](09-setup-guide.md)**
   - Complete execution guide
   - Troubleshooting
   - Monitoring and maintenance

---

## 🚀 Quick Start (3 Steps)

### Step 1: Infrastructure Setup (30 minutes)

```bash
# 1. Launch EC2 instances
Follow: 01-ec2-setup.md

# 2. Install Jenkins
ssh -i jenkins-key.pem ubuntu@JENKINS_IP
wget <script-url>/02-jenkins-installation.sh
chmod +x 02-jenkins-installation.sh
sudo ./02-jenkins-installation.sh

# 3. Install SonarQube
ssh -i jenkins-key.pem ubuntu@SONARQUBE_IP
wget <script-url>/03-sonarqube-docker-setup.sh
chmod +x 03-sonarqube-docker-setup.sh
sudo ./03-sonarqube-docker-setup.sh
```

### Step 2: Configuration (45 minutes)

```bash
# 1. Configure Jenkins
http://JENKINS_IP:8080
- Install plugins (04-jenkins-plugins.md)
- Add credentials
- Configure tools

# 2. Configure SonarQube
http://SONARQUBE_IP:9000
- Change default password
- Generate token
- Create quality gate

# 3. Connect Jenkins to SonarQube
Jenkins → Configure System → SonarQube Servers
```

### Step 3: Create and Run Pipeline (30 minutes)

```bash
# 1. Create GitHub repository with sample app (05-sample-app/)

# 2. Create Jenkins pipeline job
Jenkins → New Item → Pipeline
- Configure GitHub repo
- Point to Jenkinsfile

# 3. Run pipeline
Click "Build Now" and watch it execute!
```

---

## 📋 Pipeline Stages Explained

The pipeline has **18 comprehensive stages**:

### 🏗️ Build & Test (Stages 1-7)
1. **Initialization** - Clean workspace, setup
2. **Checkout Code** - Clone from GitHub
3. **Verify Trigger** - Confirm build cause
4. **Environment Check** - Verify tools installed
5. **Dry Run** - Compilation check
6. **Dependency Resolution** - Download dependencies
7. **Unit Tests** - Run tests with coverage

### 🔒 Security Scanning (Stages 8-11, 14, 17)
8. **SCA** - OWASP Dependency-Check for vulnerable libraries
9. **SAST** - SonarQube static analysis
10. **Quality Gate** - Enforce code quality standards
11. **IaC Scan** - Checkov for infrastructure security
14. **Container Scan** - Trivy for Docker image vulnerabilities
17. **DAST** - OWASP ZAP for runtime vulnerabilities

### 🐳 Build & Deploy (Stages 12-16, 18)
12. **Package** - Build application JAR
13. **Docker Build** - Create container image
15. **Docker Push** - Push to registry
16. **Deploy** - Run container
18. **Smoke Tests** - Verify deployment

---

## 🎓 Learning Objectives

By completing this guide, you'll learn:

### DevOps Skills
- ✅ CI/CD pipeline design and implementation
- ✅ Jenkins pipeline as code (Groovy)
- ✅ Infrastructure as Code with Terraform
- ✅ Docker containerization
- ✅ Git workflow automation

### Security Skills
- ✅ Static Application Security Testing (SAST)
- ✅ Software Composition Analysis (SCA)
- ✅ Dynamic Application Security Testing (DAST)
- ✅ Infrastructure as Code security
- ✅ Container security scanning
- ✅ Vulnerability management

### Quality Assurance
- ✅ Code quality metrics
- ✅ Test coverage analysis
- ✅ Quality gates implementation
- ✅ Technical debt management

### Cloud & Infrastructure
- ✅ AWS EC2 deployment
- ✅ Security group configuration
- ✅ Multi-tier architecture
- ✅ Resource management

---

## 💡 Key Features

### 1. Comprehensive Security Scanning

Every aspect of your application is scanned:
```
Code → Dependencies → Infrastructure → Container → Running App
SAST     SCA            IaC            Trivy        DAST
```

### 2. Quality Gates at Multiple Levels

```
Compilation → Tests → Code Quality → Security → Deployment
   ✓ PASS     ✓ PASS     ✓ PASS      ✓ PASS     ✓ PASS
```

If any stage fails, pipeline stops immediately.

### 3. Intentional Vulnerabilities for Learning

The sample app includes:
- 🐛 Vulnerable Log4j dependency (CVE-2021-44228)
- 💩 Code smells (complex methods, dead code)
- 🔓 Insecure IaC (public S3, open security groups)
- 🐳 Container vulnerabilities (base image issues)

**Perfect for learning how to detect and fix security issues!**

### 4. Production-Ready Patterns

- Parallel stages for faster execution
- Proper error handling and rollback
- Comprehensive reporting
- Email notifications
- Health checks
- Smoke tests

---

## 📊 Expected Results

### First Pipeline Run (With Intentional Issues)

```
✓ Stages 1-7: Pass (Build and test)
⚠ Stage 8 (SCA): Unstable (Log4j vulnerability detected)
✓ Stage 9 (SAST): Pass (Analysis sent to SonarQube)
✗ Stage 10 (Quality Gate): FAIL (Code smells, low coverage)
⏸ Stages 11-18: Skipped (Pipeline stopped)

Result: FAILED
Duration: ~5-8 minutes
```

### After Fixing Issues

```
✓ All 18 Stages: Pass
✓ Quality Gate: Passed
✓ Security Scans: No critical issues
✓ Deployment: Successful
✓ Application: Running and healthy

Result: SUCCESS
Duration: ~8-12 minutes
```

---

## 🛠️ Prerequisites

### Required Accounts
- AWS Account (with EC2 access)
- GitHub Account
- Docker Hub Account

### Local Tools
- SSH client
- Git
- Text editor (VS Code recommended)
- Web browser

### Knowledge
- Basic Linux commands
- Basic Git operations
- Understanding of CI/CD concepts (helpful but not required)

### Budget
- **AWS Cost**: ~$70/month for 2 t3.medium instances
- **Optimization**: Use t3.small (~$50/month) or stop when not in use
- **Free Tier**: t2.micro free for first year

---

## 📈 Pipeline Execution Time

| Stage | Time | Notes |
|-------|------|-------|
| Checkout & Setup | 30s | Fast |
| Compile & Test | 1-2min | Depends on code size |
| SCA Scan | 1-2min | First run slower (DB download) |
| SAST + Quality Gate | 1-2min | Depends on code complexity |
| IaC Scan | 30s | Fast |
| Docker Build | 1-2min | Cached layers help |
| Container Scan | 1min | First run slower |
| Deploy | 30s | Local deployment |
| DAST | 1-2min | Depends on app complexity |
| **Total** | **8-12min** | Optimizable to 5-7min |

---

## 🔧 Customization Options

### For Different Languages

**Python**:
```groovy
- Replace Maven with pip
- Use pylint/bandit for SAST
- Safety for dependency check
```

**Node.js**:
```groovy
- Replace Maven with npm/yarn
- Use ESLint for SAST
- npm audit for dependencies
```

**Go**:
```groovy
- Use go build
- gosec for SAST
- nancy for dependencies
```

### For Different Deployment Targets

**Kubernetes**:
```groovy
stage('Deploy to K8s') {
    sh 'kubectl apply -f k8s/'
}
```

**AWS ECS**:
```groovy
stage('Deploy to ECS') {
    sh 'aws ecs update-service...'
}
```

**Serverless**:
```groovy
stage('Deploy Lambda') {
    sh 'serverless deploy'
}
```

---

## 📖 Documentation Best Practices

Each file follows a clear structure:
- 📝 Clear explanations
- 💻 Code examples
- ✅ Checklists
- ⚠️ Common issues
- 💡 Tips and tricks

**Start with files in order (01 → 09) for best learning experience!**

---

## 🎯 Success Metrics

Track your progress:

- [ ] EC2 instances launched and accessible
- [ ] Jenkins installed and configured
- [ ] SonarQube running
- [ ] Sample app in GitHub
- [ ] Pipeline created
- [ ] First build executed (even if failed)
- [ ] All security reports generated
- [ ] Quality gate configured
- [ ] Issues identified and fixed
- [ ] Successful green build achieved
- [ ] Application deployed and running

---

## 🤝 Contributing

This is a learning project! Feel free to:
- Add more security tools
- Improve pipeline efficiency
- Add support for other languages
- Enhance documentation
- Share your customizations

---

## 📞 Support & Resources

### Official Documentation
- [Jenkins](https://www.jenkins.io/doc/)
- [SonarQube](https://docs.sonarqube.org/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [Trivy](https://aquasecurity.github.io/trivy/)
- [Checkov](https://www.checkov.io/1.Welcome/What%20is%20Checkov.html)
- [OWASP ZAP](https://www.zaproxy.org/docs/)

### Community
- Jenkins Community Forums
- Stack Overflow (#jenkins, #sonarqube)
- DevOps subreddit
- OWASP Slack

---

## ⚠️ Important Notes

### Security Considerations
- This setup is for LEARNING purposes
- For production:
  - Use VPCs and private subnets
  - Enable HTTPS/TLS
  - Implement proper secrets management
  - Use IAM roles instead of credentials
  - Enable audit logging
  - Regular security updates

### Cost Management
- **Stop EC2 instances when not in use**
- Use AWS Budgets to set alerts
- Consider using AWS Free Tier
- Clean up old Docker images
- Delete old builds in Jenkins

---

## 🎉 What's Next?

After completing this guide:

1. **Customize** - Adapt pipeline for your projects
2. **Expand** - Add more stages (performance testing, chaos engineering)
3. **Scale** - Move to Kubernetes, add more agents
4. **Secure** - Implement vault for secrets, add more security scans
5. **Monitor** - Add Prometheus, Grafana for metrics
6. **Share** - Teach others, contribute back

---

## 📝 License

This guide uses open-source tools:
- Jenkins: MIT License
- SonarQube Community: LGPL
- All security tools: Open source

Feel free to use, modify, and share!

---

## 👏 Acknowledgments

Built with:
- Jenkins community
- OWASP Foundation
- SonarSource
- Aqua Security (Trivy)
- Bridgecrew (Checkov)
- The amazing DevSecOps community

---

## 🚦 Let's Get Started!

Ready to build your pipeline? Start with **[01-ec2-setup.md](01-ec2-setup.md)**!

**Estimated time to complete**: 2-3 hours
**Estimated learning value**: Priceless 🚀

Happy building and learning! 💪