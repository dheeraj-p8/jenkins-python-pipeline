#!/bin/bash

# Jenkins Installation Script for Ubuntu 22.04 - Python Version
# Run this on Jenkins EC2 instance

set -e  # Exit on any error

echo "=========================================="
echo "Jenkins Installation Script (Python Setup)"
echo "=========================================="

# Update system
echo "[1/9] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Java (Jenkins requires Java 11 or 17)
echo "[2/9] Installing Java 17..."
sudo apt install -y openjdk-17-jdk

# Verify Java installation
java -version

# Install Python 3 and pip
echo "[3/9] Installing Python 3 and tools..."
sudo apt install -y python3 python3-pip python3-venv python3-dev
python3 --version
pip3 --version

# Add Jenkins repository
echo "[4/9] Adding Jenkins repository..."
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
echo "[5/9] Installing Jenkins..."
sudo apt update
sudo apt install -y jenkins

# Start Jenkins service
echo "[6/9] Starting Jenkins service..."
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins --no-pager

# Install Docker
echo "[7/9] Installing Docker..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add Jenkins user to docker group
echo "[8/9] Configuring Docker permissions..."
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Install security scanning tools
echo "[9/9] Installing security scanning tools..."

# Install Trivy (Container vulnerability scanner)
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy -y

# Install Checkov (IaC scanner)
sudo pip3 install checkov

# Install Python security tools (globally for Jenkins)
sudo pip3 install bandit safety pylint pytest pytest-cov

# Install curl for health checks
sudo apt install -y curl

# Get Jenkins initial admin password
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Jenkins initial admin password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo ""
echo "Access Jenkins at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
echo ""
echo "Installed Tools:"
echo "- Jenkins: $(jenkins --version 2>/dev/null || echo 'Installed')"
echo "- Java: $(java -version 2>&1 | head -n 1)"
echo "- Python: $(python3 --version)"
echo "- Pip: $(pip3 --version)"
echo "- Docker: $(docker --version)"
echo "- Trivy: $(trivy --version | head -n 1)"
echo "- Checkov: $(checkov --version)"
echo "- Bandit: $(bandit --version 2>&1 | head -n 1)"
echo "- Safety: $(safety --version)"
echo "- Pylint: $(pylint --version | head -n 1)"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "1. Open Jenkins in your browser"
echo "2. Enter the admin password shown above"
echo "3. Install suggested plugins"
echo "4. Create admin user"
echo "5. Proceed to plugin installation guide"
echo "=========================================="