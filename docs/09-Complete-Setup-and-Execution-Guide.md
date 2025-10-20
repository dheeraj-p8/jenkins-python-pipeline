# Step 9: Complete Setup and Execution Guide (Python Edition)

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] AWS Account with EC2 access
- [ ] GitHub Account
- [ ] Docker Hub Account
- [ ] SSH client installed
- [ ] Git installed locally
- [ ] Basic understanding of Linux commands
- [ ] Basic Python knowledge

---

## Complete Setup Timeline

**Total Time**: ~2-3 hours for first-time setup

| Task | Estimated Time |
|------|---------------|
| EC2 Setup | 15 minutes |
| Jenkins Installation | 20 minutes |
| SonarQube Setup | 15 minutes |
| Plugin Configuration | 30 minutes |
| Create Python Flask App | 20 minutes |
| First Pipeline Run | 20 minutes |
| Testing & Learning | 1-2 hours |

---

## Step-by-Step Execution

### Step 1: Launch EC2 Instances (15 min)

```bash
# Follow: 01-ec2-setup.md

1. Launch Jenkins EC2 (t3.medium, Ubuntu 22.04)
2. Launch SonarQube EC2 (t3.medium, Ubuntu 22.04)
3. Configure security groups
4. Note down IP addresses:
   - Jenkins Public IP: _______________
   - SonarQube Public IP: _______________
   - SonarQube Private IP: _______________
```

### Step 2: Install Jenkins with Python Tools (20 min)

```bash
# SSH into Jenkins EC2
ssh -i jenkins-key.pem ubuntu@<JENKINS_PUBLIC_IP>

# Download and run installation script
wget https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/scripts/02-jenkins-installation.sh
chmod +x 02-jenkins-installation.sh
sudo ./02-jenkins-installation.sh

# Save the initial admin password shown at the end
# Important: Script installs Python 3, pip, Bandit, Safety, Pylint, pytest
```

**What gets installed:**
- Jenkins
- Java 17
- Python 3.9+
- Docker
- Trivy (container scanner)
- Checkov (IaC scanner)
- Bandit (Python security scanner)
- Safety (Python dependency checker)
- Pylint (Python linter)
- pytest & pytest-cov (testing)

### Step 3: Configure Jenkins Web UI (15 min)

```bash
# Open browser
http://<JENKINS_PUBLIC_IP>:8080

1. Enter initial admin password (from Step 2)
2. Click "Install suggested plugins"
3. Wait for plugins to install (~5 minutes)
4. Create admin user:
   - Username: admin
   - Password: <strong-password>
   - Full name: Your Name
   - Email: your.email@example.com
5. Save and Continue
6. Confirm Jenkins URL
7. Start using Jenkins
```

### Step 4: Install SonarQube (15 min)

```bash
# SSH into SonarQube EC2
ssh -i jenkins-key.pem ubuntu@<SONARQUBE_PUBLIC_IP>

# Download and run installation script
wget https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/scripts/03-sonarqube-docker-setup.sh
chmod +x 03-sonarqube-docker-setup.sh
sudo ./03-sonarqube-docker-setup.sh

# Wait 2-3 minutes for SonarQube to start

# Check status
sudo docker compose ps
```

### Step 5: Configure SonarQube (10 min)

```bash
# Open browser
http://<SONARQUBE_PUBLIC_IP>:9000

1. Login:
   - Username: admin
   - Password: admin
   
2. Change password when prompted:
   - New password: <strong-password>
   - Confirm

3. Generate Token:
   - Click user icon (top right) → My Account
   - Security tab → Generate Tokens
   - Name: jenkins-token
   - Type: User Token
   - Expires in: No expiration
   - Click Generate
   - **COPY AND SAVE THIS TOKEN** (you can't see it again)
```

### Step 6: Install Jenkins Plugins (20 min)

```bash
# In Jenkins UI: Manage Jenkins → Manage Plugins → Available

Search and install (check boxes and click "Install without restart"):
1. ✅ SonarQube Scanner
2. ✅ Docker
3. ✅ Docker Pipeline
4. ✅ Email Extension Plugin
5. ✅ Config File Provider
6. ✅ Pipeline
7. ✅ Git
8. ✅ GitHub
9. ✅ HTML Publisher (for reports)
10. ✅ Warnings Next Generation (for code analysis)

Wait for all plugins to install (~5-10 minutes)
```

### Step 7: Configure Jenkins Tools (15 min)

```bash
# Manage Jenkins → Global Tool Configuration

1. SonarQube Scanner:
   - Click "Add SonarQube Scanner"
   - Name: SonarScanner
   - Check "Install automatically"
   - Version: Latest
   - Save

2. Docker:
   - Click "Add Docker"
   - Name: docker
   - Check "Install automatically"
   - Docker version: latest
   - Save

Note: Python, pip, and security tools are already installed system-wide from Step 2
```

### Step 8: Configure Jenkins Credentials (10 min)

```bash
# Manage Jenkins → Manage Credentials → (global) → Add Credentials

1. GitHub Credentials:
   - Kind: Username with password
   - Username: <github-username>
   - Password: <github-personal-access-token>
   - ID: github-credentials
   - Description: GitHub Access Token
   - Save

   How to create GitHub PAT:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token
   - Select scopes: repo, admin:repo_hook
   - Copy token

2. Docker Hub Credentials:
   - Kind: Username with password
   - Username: <dockerhub-username>
   - Password: <dockerhub-password>
   - ID: dockerhub-credentials
   - Description: Docker Hub Credentials
   - Save

3. SonarQube Token:
   - Kind: Secret text
   - Secret: <paste-sonarqube-token-from-step-5>
   - ID: sonarqube-token
   - Description: SonarQube Authentication Token
   - Save
```

### Step 9: Configure SonarQube Server in Jenkins (5 min)

```bash
# Manage Jenkins → Configure System → SonarQube servers

1. Check: "Enable injection of SonarQube server configuration"

2. Click "Add SonarQube":
   - Name: SonarQube
   - Server URL: http://<SONARQUBE_PRIVATE_IP>:9000
   - Server authentication token: Select "sonarqube-token" from dropdown

3. Click "Save"

# Test connection by clicking "Test Connection" button
```

### Step 10: Create Python Flask Application (20 min)

```bash
# On your local machine

# Create directory structure
mkdir sample-python-app
cd sample-python-app

# Create directory structure
mkdir -p app tests terraform

# Create files (content from 05-sample-app/)
# Create the following files with content from the sample app guide:

touch app/__init__.py
touch app/main.py
touch app/utils.py
touch tests/__init__.py
touch tests/test_main.py
touch requirements.txt
touch Dockerfile
touch docker-compose.yml
touch terraform/main.tf
touch .coveragerc
touch sonar-project.properties
touch Jenkinsfile
touch README.md
touch .gitignore

# Add .gitignore content
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.xml

# IDEs
.vscode/
.idea/
*.swp

# Reports
*-report.*
bandit-report.*
safety-report.*
trivy-report.*
pylint-report.*

# OS
.DS_Store
Thumbs.db
EOF
```

**Copy all file contents from the "05 - Python Flask Sample Application" artifact**

### Step 11: Initialize Git and Push to GitHub (10 min)

```bash
# Still in sample-python-app directory

# Initialize git
git init
git add .
git commit -m "Initial commit: Python Flask app with intentional vulnerabilities"

# Create repository on GitHub:
# 1. Go to github.com
# 2. Click "+" → New repository
# 3. Name: sample-python-app
# 4. Description: CI/CD Pipeline Demo with Python Flask
# 5. Public or Private (your choice)
# 6. Do NOT initialize with README (we already have one)
# 7. Click "Create repository"

# Push to GitHub
git remote add origin https://github.com/<YOUR_USERNAME>/sample-python-app.git
git branch -M main
git push -u origin main

# Verify files are on GitHub
```

### Step 12: Create Quality Gate in SonarQube (10 min)

```bash
# In SonarQube: http://<SONARQUBE_PUBLIC_IP>:9000

1. Go to Quality Gates (top menu)
2. Click "Create"
3. Name: Python-Quality-Gate
4. Add Conditions:
   
   Overall Code:
   - Coverage is less than 80%
   - Duplicated Lines (%) is greater than 3%
   - Maintainability Rating is worse than A
   - Reliability Rating is worse than A
   - Security Rating is worse than A
   - Bugs is greater than 0
   - Vulnerabilities is greater than 0
   
   New Code:
   - Coverage on New Code is less than 80%
   - Duplicated Lines (%) on New Code is greater than 3%

5. Click "Set as Default" OR assign to your project specifically
```

### Step 13: Create Jenkins Pipeline Job (10 min)

```bash
# In Jenkins: http://<JENKINS_PUBLIC_IP>:8080

1. Click "New Item"
2. Enter name: sample-python-app-pipeline
3. Select: Pipeline
4. Click OK

5. Configure:
   General:
   - Description: "CI/CD pipeline for Python Flask application"
   - Check: "GitHub project"
   - Project url: https://github.com/<YOUR_USERNAME>/sample-python-app
   
   Build Triggers:
   - Check: "Poll SCM"
   - Schedule: H/5 * * * *  (every 5 minutes)
   - OR check: "GitHub hook trigger for GITScm polling" (if webhook configured)

   Pipeline:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: https://github.com/<YOUR_USERNAME>/sample-python-app.git
   - Credentials: Select "github-credentials"
   - Branch Specifier: */main
   - Script Path: Jenkinsfile

6. Click "Save"
```

### Step 14: Update Jenkinsfile with Your Settings (5 min)

```bash
# Edit Jenkinsfile in your repository

# Update these variables at the top:
environment {
    PROJECT_NAME = 'sample-python-app'
    DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/sample-python-app"  # ← CHANGE THIS
    EMAIL_RECIPIENTS = 'your-email@example.com'  # ← CHANGE THIS
}

# Commit and push
git add Jenkinsfile
git commit -m "Update Jenkinsfile with personal settings"
git push
```

### Step 15: Run Your First Pipeline (10 min)

```bash
# In Jenkins:
1. Click on "sample-python-app-pipeline"
2. Click "Build Now"
3. Watch the pipeline execute in Blue Ocean or Stage View
4. Click on build #1
5. Click "Console Output" to see detailed logs

Expected first run results:
✓ Stages 1-9: PASS (Setup, dependencies, tests)
⚠ Stage 10 (Safety): UNSTABLE (vulnerable dependencies detected)
⚠ Stage 11 (Bandit): UNSTABLE (security issues detected)
✓ Stage 12 (SonarQube): PASS (analysis sent)
✗ Stage 13 (Quality Gate): FAIL (code smells, security issues)

Build Status: FAILED (expected!)
This is intentional - the app has vulnerabilities for learning!
```

---

## Post-Setup Configuration

### Configure GitHub Webhook (Optional - Automatic Triggers)

```bash
# In GitHub repository:
Settings → Webhooks → Add webhook

Payload URL: http://<JENKINS_PUBLIC_IP>:8080/github-webhook/
Content type: application/json
SSL verification: Disable (for testing) or Enable (if you have SSL)
Which events: Just the push event
Active: ✓ Checked

Save

# Test: Make a commit and push - pipeline should auto-trigger
echo "# Test" >> README.md
git add README.md
git commit -m "Test webhook"
git push

# Check Jenkins - build should start automatically
```

### Configure Email Notifications (Optional)

```bash
# For Gmail:
1. Enable 2-Step Verification in Google Account
2. Generate App Password:
   Google Account → Security → 2-Step Verification → App passwords
   App: Mail
   Device: Jenkins
   Copy the 16-character password

# In Jenkins:
Manage Jenkins → Configure System → Extended E-mail Notification

SMTP server: smtp.gmail.com
SMTP Port: 465
Use SSL: ✓ Checked

Credentials → Add:
- Kind: Username with password
- Username: your.email@gmail.com
- Password: <16-char-app-password>
- ID: gmail-credentials

Select "gmail-credentials" in dropdown

Advanced:
- Default user e-mail suffix: @gmail.com
- Default Content Type: HTML (text/html)
- Default Subject: $PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS!

Save

# Test by running a build
```

---

## Verification Checklist

After setup, verify:

- [ ] Jenkins accessible at http://JENKINS_IP:8080
- [ ] SonarQube accessible at http://SONARQUBE_IP:9000
- [ ] Jenkins can connect to SonarQube (test connection works)
- [ ] GitHub repository created and accessible
- [ ] All application files committed to GitHub
- [ ] Jenkinsfile exists in repository root
- [ ] All Jenkins plugins installed
- [ ] All credentials configured (GitHub, Docker Hub, SonarQube)
- [ ] Quality gate created in SonarQube
- [ ] Pipeline job created in Jenkins
- [ ] First pipeline run completed (even if failed)
- [ ] Can view console output and logs
- [ ] Python tools installed on Jenkins server
- [ ] Docker working on Jenkins server

---

## Python-Specific Verification

```bash
# SSH into Jenkins server
ssh -i jenkins-key.pem ubuntu@<JENKINS_PUBLIC_IP>

# Verify Python tools
python3 --version  # Should be 3.9+
pip3 --version
bandit --version
safety --version
pylint --version
pytest --version

# Verify Docker
docker --version
sudo docker ps

# Verify Trivy
trivy --version

# Verify Checkov
checkov --version

# Test Python virtual environment creation
python3 -m venv test-venv
source test-venv/bin/activate
pip install flask
deactivate
rm -rf test-venv
```

---

## Common Issues and Solutions

### Issue 1: Jenkins Won't Start

**Symptoms**: Can't access Jenkins at port 8080

**Solutions**:
```bash
# Check Jenkins status
sudo systemctl status jenkins

# Check if port is in use
sudo netstat -tulpn | grep 8080

# View logs
sudo journalctl -u jenkins -n 100 --no-pager

# Restart Jenkins
sudo systemctl restart jenkins

# Check Java
java -version

# Check disk space
df -h
```

### Issue 2: Python Module Not Found

**Symptoms**: "ModuleNotFoundError" in Jenkins console

**Solutions**:
```bash
# Ensure virtual environment is activated in Jenkinsfile
. ${VENV_DIR}/bin/activate

# Check if requirements.txt is present
ls -la requirements.txt

# Manual test on Jenkins server
cd /var/lib/jenkins/workspace/sample-python-app-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

### Issue 3: Permission Denied for Docker

**Symptoms**: "permission denied while trying to connect to Docker"

**Solutions**:
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# Verify
sudo -u jenkins docker ps
```

### Issue 4: SonarQube Quality Gate Timeout

**Symptoms**: "Timeout waiting for quality gate"

**Solutions**:
```bash
# Check SonarQube is running
curl http://<SONARQUBE_PRIVATE_IP>:9000

# Check SonarQube logs
ssh sonarqube-server
cd ~/sonarqube
sudo docker compose logs sonarqube --tail=100

# Verify webhook (optional)
SonarQube → Administration → Configuration → Webhooks

# Increase timeout in Jenkinsfile
timeout(time: 10, unit: 'MINUTES')  # Increase from 5

# Check background tasks in SonarQube
SonarQube → Administration → Projects → Background Tasks
```

### Issue 5: Safety Check Fails to Run

**Symptoms**: "safety: command not found"

**Solutions**:
```bash
# Install Safety globally
sudo pip3 install safety

# Or install in virtual environment
. ${VENV_DIR}/bin/activate
pip install safety

# Verify
safety --version
```

### Issue 6: Bandit Not Finding Issues

**Symptoms**: Bandit report is empty

**Solutions**:
```bash
# Verify Bandit is installed
bandit --version

# Test manually
cd /path/to/app
bandit -r app/ -f txt

# Check Jenkinsfile path
bandit -r app/  # Not bandit -r .

# Increase verbosity
bandit -r app/ -v
```

### Issue 7: Pytest Not Finding Tests

**Symptoms**: "no tests ran in X seconds"

**Solutions**:
```bash
# Check test file naming
# Must be: test_*.py or *_test.py
ls tests/

# Check __init__.py exists
ls tests/__init__.py

# Run manually
cd /path/to/project
python3 -m pytest tests/ -v

# Check PYTHONPATH
export PYTHONPATH="${WORKSPACE}:${PYTHONPATH}"
```

### Issue 8: Docker Build Fails

**Symptoms**: "failed to solve with frontend dockerfile.v0"

**Solutions**:
```bash
# Check Dockerfile exists
ls -la Dockerfile

# Test build manually
docker build -t test-image .

# Check for syntax errors in Dockerfile

# Check base image is accessible
docker pull python:3.11-slim

# Check Docker daemon
sudo systemctl status docker
```

### Issue 9: Application Won't Start After Deployment

**Symptoms**: Health check fails

**Solutions**:
```bash
# Check if container is running
docker ps -a

# View container logs
docker logs sample-python-app

# Check if port is available
sudo netstat -tulpn | grep 8080

# Test locally
docker run -it --rm -p 8080:8080 sample-python-app:latest

# Check Flask app
curl http://localhost:8080/health
```

### Issue 10: High Memory Usage

**Symptoms**: Pipeline fails with OOM errors

**Solutions**:
```bash
# Increase EC2 instance size
t3.small → t3.medium

# Adjust Python memory
export PYTHONMALLOC=malloc

# Limit pytest workers
pytest tests/ -n 2  # Limit to 2 workers

# Clean up Docker
docker system prune -a

# Restart services
sudo systemctl restart jenkins
```

---

## Pipeline Execution Flow

### Expected First Run Results (With Intentional Issues)

```
Stage 1: Initialization ..................... ✓ PASS (2s)
Stage 2: Checkout Code ...................... ✓ PASS (5s)
Stage 3: Verify Trigger ..................... ✓ PASS (1s)
Stage 4: Environment Check .................. ✓ PASS (3s)
Stage 5: Setup Virtual Environment .......... ✓ PASS (10s)
Stage 6: Install Dependencies ............... ✓ PASS (45s)
Stage 7: Dry Run / Syntax Check ............. ✓ PASS (2s)
Stage 8: Code Linting (Pylint) .............. ⚠ UNSTABLE (15s) - Code quality issues
Stage 9: Unit Tests with Coverage .......... ✓ PASS (10s)
Stage 10: SCA - Safety Check ................ ⚠ UNSTABLE (30s) - requests, Jinja2, urllib3 CVEs
Stage 11: SAST - Bandit ..................... ⚠ UNSTABLE (10s) - Security issues
Stage 12: SAST - SonarQube .................. ✓ PASS (60s)
Stage 13: Quality Gate Check ................ ✗ FAIL (120s) - Below threshold

Pipeline Status: FAILED
Total Duration: ~6-8 minutes
Failed At: Stage 13 (Quality Gate)
Reason: Code quality and security issues
```

### After Fixing Issues

```
All 20 Stages: PASS ✓
Total Duration: ~10-15 minutes
Quality Gate: PASSED
Security Scans: No critical issues
Deployment: SUCCESS
Application: Running at http://localhost:8080

Overall Result: SUCCESS ✓
```

---

## Performance Optimization

### Speed Up Pipeline

```groovy
// In Jenkinsfile

// 1. Cache Python packages
options {
    disableConcurrentBuilds()
    // Add caching later with workspace reuse
}

// 2. Parallel stages for independent tasks
stage('Security Scans') {
    parallel {
        stage('Safety') { /* ... */ }
        stage('Bandit') { /* ... */ }
        stage('IaC Scan') { /* ... */ }
    }
}

// 3. Skip stages conditionally
when {
    branch 'main'  // Only run DAST on main branch
}

// 4. Use smaller Docker images
FROM python:3.11-slim  // Instead of python:3.11

// 5. Multi-stage Docker builds
FROM python:3.11 as builder
# Build dependencies
FROM python:3.11-slim
# Copy only built artifacts
```

### Reduce Build Times

```bash
# Use pip cache
pip install --cache-dir /tmp/pip-cache -r requirements.txt

# Parallel pytest
pytest tests/ -n auto  # Use all CPU cores

# Skip slow tests in CI
pytest -m "not slow" tests/

# Use Docker layer caching
docker build --cache-from myimage:latest -t myimage:new .
```

---

## Monitoring and Maintenance

### Daily Checks

```bash
# Jenkins health
http://JENKINS_IP:8080/manage
Check: Disk space, build queue, executors

# SonarQube health
http://SONARQUBE_IP:9000/admin/system
Check: Database, Elasticsearch, compute engine

# Application health
curl http://localhost:8080/health

# Recent builds
Jenkins → sample-python-app-pipeline → Build History
```

### Weekly Tasks

```bash
# Update Jenkins plugins
Manage Jenkins → Manage Plugins → Updates

# Update Python packages globally
sudo pip3 install --upgrade safety bandit pylint pytest

# Review security scan trends
Check: Safety reports, Bandit reports, SonarQube metrics

# Check system logs
sudo journalctl -u jenkins -n 500

# Backup Jenkins configuration
tar -czf jenkins-backup-$(date +%F).tar.gz /var/lib/jenkins/

# Clean old Docker images
docker image prune -a --filter "until=168h"
```

### Monthly Tasks

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker pull python:3.11-slim
docker pull ghcr.io/zaproxy/zaproxy:stable
docker pull sonarqube:community

# Review and clean old builds
Jenkins → Job → Configure → Discard old builds

# Update security tools databases
Safety, Trivy, Checkov update automatically

# Review AWS costs
AWS Console → Cost Explorer

# Security audit
Review all credentials, rotate if needed
Check security group rules
Review CloudWatch logs
```

---

## Learning Path

### Week 1: Basic Pipeline
```
✓ Get pipeline running end-to-end
✓ Understand each stage
✓ View all reports
✓ Fix one Python issue at a time
```

### Week 2: Security Focus
```
✓ Deep dive into Safety results (dependency CVEs)
✓ Understand Bandit findings (Python security)
✓ Analyze SonarQube metrics
✓ Fix IaC issues
✓ Review DAST findings
```

### Week 3: Optimization
```
✓ Improve test coverage (aim for >80%)
✓ Reduce pipeline execution time
✓ Add custom quality gates
✓ Implement branch strategies
✓ Add more test cases
```

### Week 4: Advanced Topics
```
✓ Multi-branch pipelines
✓ Blue-green deployment
✓ Integration with Kubernetes
✓ Add performance testing (Locust)
✓ Implement secrets management (Vault)
```

---

## Useful Commands Reference

### Jenkins CLI
```bash
# Restart Jenkins
sudo systemctl restart jenkins

# View logs
sudo journalctl -u jenkins -f

# Check Jenkins home
ls -la /var/lib/jenkins/

# Manual plugin installation
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin <plugin-name>
```

### Python Commands
```bash
# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Run specific test
pytest tests/test_main.py::test_home -v

# Run security scan
bandit -r app/
safety check
pylint app/
```

### Docker Commands
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs sample-python-app
docker logs -f sample-python-app  # Follow

# Stop container
docker stop sample-python-app

# Remove container
docker rm sample-python-app

# Build image
docker build -t sample-python-app .

# Run container
docker run -d -p 8080:8080 --name sample-python-app sample-python-app:latest

# Execute command in container
docker exec -it sample-python-app /bin/bash

# Clean up
docker system prune -a
docker volume prune
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull latest
git pull

# View history
git log --oneline --graph

# Create branch
git checkout -b feature-branch

# Merge branch
git checkout main
git merge feature-branch
```

---

## Cost Management

### AWS Costs (Monthly Estimates)

```
Jenkins EC2 (t3.medium, 24/7): ~$30
SonarQube EC2 (t3.medium, 24/7): ~$30
Storage (60 GB EBS): ~$6
Data Transfer: ~$5
Elastic IP (2): Free when attached
-----------------------------------
Total: ~$71/month

Cost Savings Options:
1. Use t3.small instead: Save ~$20/month
2. Stop instances when not in use: Save ~60%
3. Use Reserved Instances: Save 40%
4. Use Spot Instances: Save 70% (for testing)
```

### Cost Optimization Script

```bash
#!/bin/bash
# save-costs.sh

# Stop instances at night (schedule with cron)
# Add to crontab: 0 20 * * * /path/to/save-costs.sh stop
# Add to crontab: 0 8 * * 1-5 /path/to/save-costs.sh start

ACTION=$1

if [ "$ACTION" == "stop" ]; then
    echo "Stopping EC2 instances to save costs..."
    aws ec2 stop-instances --instance-ids i-jenkins i-sonarqube
elif [ "$ACTION" == "start" ]; then
    echo "Starting EC2 instances..."
    aws ec2 start-instances --instance-ids i-jenkins i-sonarqube
fi
```

---

## Next Steps

1. ✓ Complete setup following this guide
2. ✓ Run first pipeline and observe results
3. ✓ Review all generated reports
4. ✓ Fix issues using 08-testing-errors.md (Python version)
5. ✓ Achieve successful pipeline (all green)
6. ✓ Experiment with different Python errors
7. ✓ Customize pipeline for your Flask projects
8. ✓ Add more features (database, authentication)
9. ✓ Deploy to production environment
10. ✓ Share your learning!

---

## Resources

### Python-Specific
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices/)
- [Flask Security Guide](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/documentation/)
- [pytest Documentation](https://docs.pytest.org/)

### General
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [SonarQube Docs](https://docs.sonarqube.org/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Python Project](https://owasp.org/www-project-python-security/)

---

## Support

If you encounter issues:
1. Check troubleshooting section above
2. Review console output in Jenkins
3. Check logs on both EC2 servers
4. Search GitHub issues
5. Ask in community forums:
   - Jenkins Community
   - Python Discord
   - Stack Overflow (#jenkins #python #flask)

---

Happy Learning with Python! 🐍🚀em ubuntu@<JENKINS_PUBLIC_IP>

# Download and run installation script
wget https://raw.githubusercontent.com/YOUR_REPO/jenkins-setup/02-jenkins-installation.sh
chmod +x 02-jenkins-installation.sh
sudo ./02-jenkins-installation.sh

# Save the initial admin password shown at the end
```

### Step 3: Configure Jenkins Web UI (15 min)

```bash
# Open browser
http://<JENKINS_PUBLIC_IP>:8080

1. Enter initial admin password
2. Click "Install suggested plugins"
3. Wait for plugins to install
4. Create admin user:
   - Username: admin
   - Password: <strong-password>
   - Full name: Your Name
   - Email: your.email@example.com
5. Save and Continue
6. Confirm Jenkins URL
7. Start using Jenkins
```

### Step 4: Install SonarQube (15 min)

```bash
# SSH into SonarQube EC2
ssh -i jenkins-key.pem ubuntu@<SONARQUBE_PUBLIC_IP>

# Download and run installation script
wget https://raw.githubusercontent.com/YOUR_REPO/jenkins-setup/03-sonarqube-docker-setup.sh
chmod +x 03-sonarqube-docker-setup.sh
sudo ./03-sonarqube-docker-setup.sh

# Wait 2-3 minutes for SonarQube to start

# Check status
sudo docker compose ps
```

### Step 5: Configure SonarQube (10 min)

```bash
# Open browser
http://<SONARQUBE_PUBLIC_IP>:9000

1. Login:
   - Username: admin
   - Password: admin
   
2. Change password when prompted:
   - New password: <strong-password>
   - Confirm

3. Generate Token:
   - Click user icon (top right) → My Account
   - Security tab → Generate Tokens
   - Name: jenkins-token
   - Type: User Token
   - Expires in: No expiration
   - Click Generate
   - **COPY AND SAVE THIS TOKEN** (you can't see it again)
```

### Step 6: Install Jenkins Plugins (20 min)

```bash
# In Jenkins UI: Manage Jenkins → Manage Plugins → Available

Search and install:
1. SonarQube Scanner
2. OWASP Dependency-Check
3. Docker
4. Docker Pipeline
5. Email Extension Plugin
6. Config File Provider
7. Pipeline
8. Git

Click "Install without restart"
Wait for all plugins to install
```

### Step 7: Configure Jenkins Tools (15 min)

```bash
# Manage Jenkins → Global Tool Configuration

1. JDK:
   - Name: JDK17
   - JAVA_HOME: /usr/lib/jvm/java-17-openjdk-amd64
   - Uncheck "Install automatically"

2. Maven:
   - Click "Add Maven"
   - Name: Maven3
   - Check "Install automatically"
   - Version: 3.9.6

3. SonarQube Scanner:
   - Click "Add SonarQube Scanner"
   - Name: SonarScanner
   - Check "Install automatically"
   - Version: Latest

4. Docker:
   - Click "Add Docker"
   - Name: docker
   - Check "Install automatically"

Click "Save"
```

### Step 8: Configure Jenkins Credentials (10 min)

```bash
# Manage Jenkins → Manage Credentials → (global) → Add Credentials

1. GitHub Credentials:
   - Kind: Username with password
   - Username: <github-username>
   - Password: <github-personal-access-token>
   - ID: github-credentials
   - Description: GitHub Access
   - Save

2. Docker Hub Credentials:
   - Kind: Username with password
   - Username: <dockerhub-username>
   - Password: <dockerhub-password>
   - ID: dockerhub-credentials
   - Description: Docker Hub
   - Save

3. SonarQube Token:
   - Kind: Secret text
   - Secret: <paste-sonarqube-token>
   - ID: sonarqube-token
   - Description: SonarQube Auth
   - Save
```

### Step 9: Configure SonarQube Server in Jenkins (5 min)

```bash
# Manage Jenkins → Configure System → SonarQube servers

Check: "Enable injection of SonarQube server configuration"

Click "Add SonarQube":
- Name: SonarQube
- Server URL: http://<SONARQUBE_PRIVATE_IP>:9000
- Server authentication token: Select "sonarqube-token"

Click "Save"
```

### Step 10: Create GitHub Repository (10 min)

```bash
# On your local machine

# Create directory
mkdir sample-java-app
cd sample-java-app

# Initialize git
git init

# Create all files from 05-sample-app/
# (Copy all files: pom.xml, App.java, AppTest.java, Dockerfile, etc.)

# Commit
git add .
git commit -m "Initial commit"

# Create repository on GitHub (via web UI)
# Then push:
git remote add origin https://github.com/<your-username>/sample-java-app.git
git branch -M main
git push -u origin main
```

### Step 11: Create Quality Gate in SonarQube (10 min)

```bash
# Follow: 07-quality-gates.md

1. In SonarQube: Quality Gates → Copy "Sonar way"
2. Name it: "My Quality Gate"
3. Optionally add custom conditions
4. Set as default OR assign to project
```

### Step 12: Create Jenkins Pipeline Job (10 min)

```bash
# In Jenkins: New Item

1. Enter name: sample-java-app-pipeline
2. Select: Pipeline
3. Click OK

4. Configure:
   - Description: "CI/CD pipeline for sample Java app"
   - Check: "GitHub project"
   - Project url: https://github.com/<your-username>/sample-java-app
   
5. Build Triggers:
   - Check: "GitHub hook trigger for GITScm polling"
   - (Or check "Poll SCM" with schedule: H/5 * * * *)

6. Pipeline:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: https://github.com/<your-username>/sample-java-app.git
   - Credentials: Select "github-credentials"
   - Branch: */main
   - Script Path: Jenkinsfile

7. Click "Save"
```

### Step 13: Update Jenkinsfile (5 min)

```bash
# Edit Jenkinsfile in your repository

# Update these variables:
DOCKER_IMAGE = "yourdockerhubusername/sample-java-app"  # Change to your Docker Hub username
EMAIL_RECIPIENTS = 'your-email@example.com'  # Change to your email

# Commit and push
git add Jenkinsfile
git commit -m "Update Jenkinsfile with personal settings"
git push
```

### Step 14: Run Your First Pipeline (10 min)

```bash
# In Jenkins:
1. Click on "sample-java-app-pipeline"
2. Click "Build Now"
3. Watch the pipeline execute (click on build #1)
4. Click "Console Output" to see logs
5. Observe each stage

Expected first run:
- Most stages will PASS ✓
- SCA will show warnings (Log4j vulnerability) ⚠
- Quality Gate will likely FAIL ✗ (due to code smells)
- Build will be UNSTABLE or FAILED
```

---

## Post-Setup Configuration

### Configure GitHub Webhook (Optional - Automatic Triggers)

```bash
# In GitHub repository:
Settings → Webhooks → Add webhook

Payload URL: http://<JENKINS_PUBLIC_IP>:8080/github-webhook/
Content type: application/json
SSL verification: Enable (or disable for testing)
Trigger: Just the push event

Save

# Test: Make a commit and push - pipeline should auto-trigger
```

### Configure Email Notifications

```bash
# Manage Jenkins → Configure System → Extended E-mail Notification

SMTP server: smtp.gmail.com
SMTP Port: 465
Credentials: Add → Gmail App Password
Use SSL: Yes

Advanced:
- Default Content Type: HTML (text/html)
- Default Subject: $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS

Save

# For Gmail:
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password
4. Use app password in Jenkins
```

---

## Verification Checklist

After setup, verify:

- [ ] Jenkins accessible at http://JENKINS_IP:8080
- [ ] SonarQube accessible at http://SONARQUBE_IP:9000
- [ ] Jenkins can connect to SonarQube
- [ ] GitHub repository created and accessible
- [ ] Jenkinsfile exists in repository
- [ ] All Jenkins plugins installed
- [ ] All credentials configured
- [ ] Docker Hub credentials work
- [ ] Quality gate created in SonarQube
- [ ] Pipeline job created in Jenkins
- [ ] First pipeline run completed

---

## Common Issues and Solutions

### Issue 1: Jenkins Won't Start

**Symptoms**: Can't access Jenkins at port 8080

**Solutions**:
```bash
# Check Jenkins status
sudo systemctl status jenkins

# Check if port is in use
sudo netstat -tulpn | grep 8080

# View logs
sudo tail -f /var/log/jenkins/jenkins.log

# Restart Jenkins
sudo systemctl restart jenkins

# Check Java installation
java -version
```

### Issue 2: SonarQube Won't Start

**Symptoms**: Can't access SonarQube at port 9000

**Solutions**:
```bash
# Check containers
sudo docker compose ps

# View logs
sudo docker compose logs sonarqube

# Check system settings
sysctl vm.max_map_count  # Should be 524288

# Restart SonarQube
cd ~/sonarqube
sudo docker compose restart

# If still failing, recreate
sudo docker compose down
sudo docker compose up -d
```

### Issue 3: Pipeline Fails at Checkout

**Symptoms**: "Failed to connect to repository"

**Solutions**:
```bash
# Verify GitHub credentials
Jenkins → Manage Credentials → Check github-credentials

# Test SSH access
ssh -T git@github.com

# Use HTTPS instead of SSH in repository URL
https://github.com/username/repo.git
```

### Issue 4: Quality Gate Timeout

**Symptoms**: "Timeout waiting for quality gate"

**Solutions**:
```bash
# Check SonarQube is running
curl http://<SONARQUBE_PRIVATE_IP>:9000

# Verify webhook (Optional)
SonarQube → Administration → Webhooks

# Increase timeout in Jenkinsfile
timeout(time: 10, unit: 'MINUTES')  # Increase from 5

# Check SonarQube analysis completed
SonarQube → Projects → Your Project → Background Tasks
```

### Issue 5: Docker Permission Denied

**Symptoms**: "permission denied while trying to connect to Docker"

**Solutions**:
```bash
# On Jenkins server
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Verify
sudo -u jenkins docker ps
```

### Issue 6: Maven Build Fails

**Symptoms**: "Could not resolve dependencies"

**Solutions**:
```bash
# Check internet connectivity
ping maven.org

# Clear Maven cache
rm -rf ~/.m2/repository

# Check Maven settings
cat ~/.m2/settings.xml

# Update pom.xml dependencies
mvn dependency:resolve
```

### Issue 7: Trivy Scan Fails

**Symptoms**: "command not found: trivy"

**Solutions**:
```bash
# Reinstall Trivy
sudo apt-get update
sudo apt-get install trivy -y

# Verify installation
trivy --version

# Check PATH
echo $PATH

# Manual scan test
trivy image nginx:latest
```

### Issue 8: DAST ZAP Scan Fails

**Symptoms**: "Cannot pull ZAP Docker image"

**Solutions**:
```bash
# Pull image manually
docker pull owasp/zap2docker-stable

# Check Docker Hub access
docker login

# Verify application is running
curl http://localhost:8080/health

# Check network
docker network ls
```

### Issue 9: SonarQube Quality Gate Not Working

**Symptoms**: Quality gate always passes or always fails

**Solutions**:
```bash
# Verify quality gate is assigned
SonarQube → Project → Settings → Quality Gate

# Check conditions
SonarQube → Quality Gates → Your Gate → Conditions

# Force re-analysis
Jenkins → Rebuild

# Check webhook
SonarQube → Administration → Configuration → Webhooks
```

### Issue 10: Out of Memory

**Symptoms**: Pipeline fails randomly, OOM errors

**Solutions**:
```bash
# Increase EC2 instance size
t3.small → t3.medium → t3.large

# Adjust Java heap for Maven
export MAVEN_OPTS="-Xmx1024m"

# Adjust Jenkins memory
sudo nano /etc/default/jenkins
JAVA_ARGS="-Xmx2048m"

# Adjust SonarQube memory
Edit docker-compose.yml:
environment:
  - SONAR_OPTS=-Xmx1024m
```

---

## Pipeline Execution Flow

### Expected First Run Results

```
Stage 1: Initialization ..................... ✓ PASS
Stage 2: Checkout Code ...................... ✓ PASS
Stage 3: Verify Trigger ..................... ✓ PASS
Stage 4: Environment Check .................. ✓ PASS
Stage 5: Dry Run / Compile Check ............ ✓ PASS
Stage 6: Dependency Resolution .............. ✓ PASS
Stage 7: Unit Tests ......................... ✓ PASS
Stage 8: SCA - Dependency Check ............. ⚠ UNSTABLE (Log4j vulnerability)
Stage 9: SAST - SonarQube Analysis .......... ✓ PASS
Stage 10: Quality Gate Check ................ ✗ FAIL (Code smells, low coverage)
Stage 11: IaC Security Scan ................. [Skipped - fails at Stage 10]
Stage 12: Build Application Package ......... [Skipped]
Stage 13: Docker Image Build ................ [Skipped]
Stage 14: Container Security Scan ........... [Skipped]
Stage 15: Push Docker Image ................. [Skipped]
Stage 16: Deploy Application ................ [Skipped]
Stage 17: DAST ............................. [Skipped]
Stage 18: Smoke Tests ....................... [Skipped]

Overall Result: FAILED
Reason: Quality Gate Failed
```

### After Fixing Issues

```
Stage 1-7: .................................. ✓ PASS
Stage 8: SCA ................................ ✓ PASS (Dependencies updated)
Stage 9-10: SAST & Quality Gate ............. ✓ PASS (Code fixed, tests added)
Stage 11: IaC Scan .......................... ⚠ WARNING (Security issues)
Stage 12-15: Build & Push ................... ✓ PASS
Stage 16: Deploy ............................ ✓ PASS
Stage 17: DAST .............................. ⚠ WARNING (Minor issues)
Stage 18: Smoke Tests ....................... ✓ PASS

Overall Result: SUCCESS (with warnings)
```

---

## Performance Optimization

### Speed Up Pipeline

```groovy
// In Jenkinsfile

// 1. Parallel stages for independent tasks
stage('Security Scans') {
    parallel {
        stage('SCA') { /* ... */ }
        stage('IaC Scan') { /* ... */ }
    }
}

// 2. Cache Maven dependencies
options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    // Cache Maven repo
}

// 3. Skip stages conditionally
when {
    branch 'main'  // Only run DAST on main branch
}

// 4. Use smaller Docker images
FROM eclipse-temurin:17-jre-alpine  // Instead of full JDK
```

### Reduce Scan Times

```bash
# OWASP Dependency-Check
--suppression suppression.xml  # Suppress known false positives

# Trivy
--severity HIGH,CRITICAL  # Skip low/medium

# SonarQube
-Dsonar.exclusions=**/test/**  # Exclude test files
```

---

## Monitoring and Maintenance

### Daily Checks

```bash
# Jenkins health
http://JENKINS_IP:8080/manage

# SonarQube health
http://SONARQUBE_IP:9000/admin/system

# Disk space
df -h

# Recent builds
Jenkins → Build History
```

### Weekly Tasks

```bash
# Update plugins
Manage Jenkins → Manage Plugins → Updates

# Review security scan results
Check trends in SCA, SAST, DAST reports

# Check logs
sudo tail -100 /var/log/jenkins/jenkins.log

# Backup Jenkins
tar -czf jenkins-backup.tar.gz /var/lib/jenkins/
```

### Monthly Tasks

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker pull owasp/zap2docker-stable
docker pull sonarqube:community

# Review and clean old builds
Jenkins → Job → Configure → Build History

# Update security tools
Trivy, Checkov, Dependency-Check databases
```

---

## Learning Path

### Week 1: Basic Pipeline
```
1. Get pipeline running end-to-end
2. Understand each stage
3. View all reports
4. Fix one issue at a time
```

### Week 2: Security Focus
```
1. Deep dive into SCA results
2. Understand SonarQube metrics
3. Fix IaC issues
4. Analyze DAST findings
```

### Week 3: Optimization
```
1. Improve test coverage
2. Reduce pipeline time
3. Add custom quality gates
4. Implement branch strategies
```

### Week 4: Advanced Topics
```
1. Multi-branch pipelines
2. Deployment strategies (blue-green, canary)
3. Integration with Kubernetes
4. Custom security scanners
```

---

## Useful Commands Reference

### Jenkins CLI
```bash
# Restart Jenkins
sudo systemctl restart jenkins

# View logs
sudo journalctl -u jenkins -f

# Reload configuration
curl -X POST http://localhost:8080/reload
```

### Docker Commands
```bash
# View running containers
docker ps

# View logs
docker logs <container-name>

# Stop/Start application
docker stop sample-java-app
docker start sample-java-app

# Clean up
docker system prune -a
```

### Maven Commands
```bash
# Clean build
mvn clean package

# Run tests
mvn test

# Skip tests
mvn package -DskipTests

# Dependency tree
mvn dependency:tree
```

### Git Commands
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "message"
git push

# View history
git log --oneline
```

---

## Cost Management

### AWS Costs (Monthly Estimates)

```
Jenkins EC2 (t3.medium): ~$30
SonarQube EC2 (t3.medium): ~$30
Storage (60 GB): ~$6
Data Transfer: ~$5
-----------------
Total: ~$71/month

Cost Savings:
- Use t3.small: Save ~$20/month
- Stop instances when not in use
- Use spot instances: Save 70%
```

### Free Tier Usage

```
- First year: Free t2.micro
- 30 GB storage free
- GitHub: Free for public repos
- Docker Hub: Free tier available
- All security tools: Free/open source
```

---

## Next Steps

1. ✓ Complete setup following this guide
2. ✓ Run first pipeline
3. ✓ Review all reports
4. ✓ Fix issues using 08-testing-errors.md
5. ✓ Achieve successful pipeline
6. ✓ Experiment with different errors
7. ✓ Customize pipeline for your needs
8. ✓ Share your learning!

## Resources

- Jenkins Documentation: https://www.jenkins.io/doc/
- SonarQube Docs: https://docs.sonarqube.org/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Docker Security: https://docs.docker.com/engine/security/
- CI/CD Best Practices: https://www.jenkins.io/doc/book/pipeline/

---

## Support

If you encounter issues:
1. Check troubleshooting section above
2. Review console output in Jenkins
3. Check logs on both servers
4. Search GitHub issues for similar problems
5. Ask in Jenkins/SonarQube community forums

Happy Learning! 🚀