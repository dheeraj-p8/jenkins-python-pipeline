# Step 1: AWS EC2 Setup

## EC2 Instance 1 - Jenkins Server

### Launch Configuration
1. **AMI**: Ubuntu 22.04 LTS
2. **Instance Type**: t3.medium (2 vCPU, 4GB RAM)
   - Minimum: t3.small, but medium recommended for better performance
3. **Storage**: 30 GB gp3
4. **Security Group**: Create "jenkins-sg"

### Security Group Rules (jenkins-sg)
```
Inbound Rules:
- SSH (22) - Your IP
- HTTP (8080) - Your IP (Jenkins Web UI)
- Custom TCP (9000) - SonarQube EC2 Security Group (for communication)

Outbound Rules:
- All traffic - 0.0.0.0/0
```

### Steps to Launch:
```bash
# 1. Go to AWS Console > EC2 > Launch Instance
# 2. Name: jenkins-server
# 3. Select Ubuntu 22.04 LTS
# 4. Instance type: t3.medium
# 5. Create new key pair: jenkins-key.pem (download and save)
# 6. Network settings:
#    - Create security group: jenkins-sg
#    - Add rules as specified above
# 7. Configure storage: 30 GB gp3
# 8. Launch instance
```

---

## EC2 Instance 2 - SonarQube Server

### Launch Configuration
1. **AMI**: Ubuntu 22.04 LTS
2. **Instance Type**: t3.medium (2 vCPU, 4GB RAM)
   - SonarQube requires minimum 2GB RAM
3. **Storage**: 30 GB gp3
4. **Security Group**: Create "sonarqube-sg"

### Security Group Rules (sonarqube-sg)
```
Inbound Rules:
- SSH (22) - Your IP
- HTTP (9000) - Your IP (SonarQube Web UI)
- HTTP (9000) - jenkins-sg (Allow Jenkins to communicate)

Outbound Rules:
- All traffic - 0.0.0.0/0
```

### Steps to Launch:
```bash
# 1. Go to AWS Console > EC2 > Launch Instance
# 2. Name: sonarqube-server
# 3. Select Ubuntu 22.04 LTS
# 4. Instance type: t3.medium
# 5. Use same key pair: jenkins-key.pem
# 6. Network settings:
#    - Create security group: sonarqube-sg
#    - Add rules as specified above
# 7. Configure storage: 30 GB gp3
# 8. Launch instance
```

---

## Connect to Instances

### Set correct permissions for your key
```bash
chmod 400 jenkins-key.pem
```

### Connect to Jenkins Server
```bash
ssh -i jenkins-key.pem ubuntu@<JENKINS_PUBLIC_IP>
```

### Connect to SonarQube Server
```bash
ssh -i jenkins-key.pem ubuntu@<SONARQUBE_PUBLIC_IP>
```

---

## Post-Launch Checklist
- [ ] Both instances are running
- [ ] Security groups are properly configured
- [ ] You can SSH into both instances
- [ ] Note down both public IPs:
  - Jenkins IP: _______________
  - SonarQube IP: _______________
- [ ] Note down SonarQube private IP: _______________

---

## Important Notes

1. **Elastic IP (Optional but Recommended)**:
   - Allocate Elastic IPs for both instances to prevent IP changes on restart
   - Cost: Free if instance is running, ~$3.60/month if stopped

2. **Cost Optimization**:
   - Stop instances when not in use
   - Use t3.small if testing on a budget (will be slower)

3. **Security Best Practices**:
   - Restrict SSH to your IP only
   - Use VPC for production environments
   - Enable CloudWatch monitoring
   - Regular security updates: `sudo apt update && sudo apt upgrade -y`

---

## Next Steps
Proceed to `02-jenkins-installation.sh` to install Jenkins on the first EC2 instance.