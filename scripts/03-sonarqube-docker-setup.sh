#!/bin/bash

# SonarQube Docker Installation Script for Ubuntu 22.04
# Run this on SonarQube EC2 instance

set -e  # Exit on any error

echo "=========================================="
echo "SonarQube Docker Installation Script"
echo "=========================================="

# Update system
echo "[1/6] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "[2/6] Installing Docker..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Configure system settings for SonarQube
echo "[3/6] Configuring system settings for SonarQube..."
sudo sysctl -w vm.max_map_count=524288
sudo sysctl -w fs.file-max=131072
ulimit -n 131072
ulimit -u 8192

# Make settings persistent
echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf
echo "fs.file-max=131072" | sudo tee -a /etc/sysctl.conf

# Create docker-compose file for SonarQube
echo "[4/6] Creating SonarQube docker-compose configuration..."
mkdir -p ~/sonarqube
cd ~/sonarqube

cat > docker-compose.yml <<'EOF'
version: "3.8"

services:
  sonarqube:
    image: sonarqube:community
    container_name: sonarqube
    depends_on:
      - db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
    ports:
      - "9000:9000"
    networks:
      - sonarnet

  db:
    image: postgres:15
    container_name: sonarqube_db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - postgresql_data:/var/lib/postgresql/data
    networks:
      - sonarnet

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  postgresql_data:

networks:
  sonarnet:
    driver: bridge
EOF

# Start SonarQube
echo "[5/6] Starting SonarQube containers..."
sudo docker compose up -d

# Wait for SonarQube to start
echo "[6/6] Waiting for SonarQube to start (this may take 2-3 minutes)..."
sleep 30

# Check container status
echo ""
echo "Container Status:"
sudo docker compose ps

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
echo "SonarQube URL (Public): http://${PUBLIC_IP}:9000"
echo "SonarQube URL (Private - for Jenkins): http://${PRIVATE_IP}:9000"
echo ""
echo "Default Credentials:"
echo "Username: admin"
echo "Password: admin"
echo ""
echo "IMPORTANT: You will be forced to change the password on first login"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "1. Wait 2-3 minutes for SonarQube to fully start"
echo "2. Access SonarQube at the URL above"
echo "3. Login with default credentials"
echo "4. Change the admin password"
echo "5. Generate an authentication token for Jenkins"
echo "=========================================="
echo ""
echo "Useful Commands:"
echo "- View logs: sudo docker compose logs -f sonarqube"
echo "- Stop: sudo docker compose down"
echo "- Start: sudo docker compose up -d"
echo "- Restart: sudo docker compose restart"
echo "=========================================="