# Step 4: Jenkins Plugins Configuration

## Required Plugins

### Install These Plugins via Jenkins UI

1. **Navigate to**: Jenkins Dashboard → Manage Jenkins → Manage Plugins → Available

2. **Search and Install** the following plugins:

#### Source Code Management
- [x] **Git** - For GitHub integration
- [x] **GitHub** - GitHub specific features
- [x] **GitHub Branch Source** - Multi-branch pipeline support

#### Pipeline & Build
- [x] **Pipeline** - Pipeline as code
- [x] **Pipeline: Stage View** - Visualize pipeline stages
- [x] **Blue Ocean** (Optional) - Modern UI for pipelines

#### Code Quality & Security
- [x] **SonarQube Scanner** - SAST integration
- [x] **OWASP Dependency-Check** - Dependency vulnerability scanning
- [x] **Docker** - Docker build and publish
- [x] **Docker Pipeline** - Docker commands in pipeline

#### Notifications
- [x] **Email Extension** - Email notifications
- [x] **Slack Notification** (Optional) - Slack integration

#### Utilities
- [x] **Config File Provider** - Manage config files
- [x] **Credentials Binding** - Secure credential management
- [x] **Workspace Cleanup** - Clean workspace

---

## Plugin Installation Steps

### Method 1: Via UI (Recommended)
```
1. Go to: Manage Jenkins → Manage Plugins
2. Click "Available" tab
3. Use filter box to search for each plugin
4. Check the box next to the plugin
5. Click "Install without restart" or "Download now and install after restart"
6. Wait for installation to complete
```

### Method 2: Via Jenkins CLI (Advanced)
```bash
# SSH into Jenkins server
# Run these commands

JENKINS_URL="http://localhost:8080"
ADMIN_USER="admin"
ADMIN_PASSWORD="your-password"

# Install plugins
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -s $JENKINS_URL \
  -auth $ADMIN_USER:$ADMIN_PASSWORD install-plugin \
  git github github-branch-source pipeline-stage-view \
  sonar owasp-dependency-check docker-plugin docker-workflow \
  email-ext config-file-provider credentials-binding ws-cleanup

# Restart Jenkins
sudo systemctl restart jenkins
```

---

## Configure Jenkins Tools

### 1. Configure JDK
```
Manage Jenkins → Global Tool Configuration → JDK
- Name: JDK17
- JAVA_HOME: /usr/lib/jvm/java-17-openjdk-amd64
- Uncheck "Install automatically"
```

### 2. Configure Maven (for Java projects)
```
Manage Jenkins → Global Tool Configuration → Maven
- Name: Maven3
- Check "Install automatically"
- Version: 3.9.6
```

### 3. Configure Docker
```
Manage Jenkins → Global Tool Configuration → Docker
- Name: docker
- Check "Install automatically"
- Docker version: latest
```

### 4. Configure SonarQube Scanner
```
Manage Jenkins → Global Tool Configuration → SonarQube Scanner
- Name: SonarScanner
- Check "Install automatically"
- Version: SonarQube Scanner 5.0.1.3006
```

### 5. Configure Dependency-Check
```
Manage Jenkins → Global Tool Configuration → Dependency-Check
- Name: DP-Check
- Installation directory: /opt/dependency-check
- Uncheck "Install automatically"
```

---

## Configure Jenkins Credentials

### 1. GitHub Credentials
```
Manage Jenkins → Manage Credentials → (global) → Add Credentials

Type: Username with password (or Personal Access Token)
Username: <your-github-username>
Password: <your-github-token>
ID: github-credentials
Description: GitHub Access Token
```

**How to create GitHub Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes: `repo`, `admin:repo_hook`
3. Copy token and paste in Jenkins

### 2. Docker Hub Credentials
```
Manage Jenkins → Manage Credentials → (global) → Add Credentials

Type: Username with password
Username: <your-dockerhub-username>
Password: <your-dockerhub-password>
ID: dockerhub-credentials
Description: Docker Hub Credentials
```

### 3. SonarQube Token
First, generate token in SonarQube:
```
1. Login to SonarQube
2. Go to: Administration → Security → Users
3. Click on your user → Tokens
4. Generate Token
5. Copy the token
```

Then add to Jenkins:
```
Manage Jenkins → Manage Credentials → (global) → Add Credentials

Type: Secret text
Secret: <sonarqube-token>
ID: sonarqube-token
Description: SonarQube Authentication Token
```

---

## Configure SonarQube Server in Jenkins

```
Manage Jenkins → Configure System → SonarQube servers

Check: Enable injection of SonarQube server configuration
Add SonarQube:
- Name: SonarQube
- Server URL: http://<SONARQUBE_PRIVATE_IP>:9000
- Server authentication token: Select 'sonarqube-token' from dropdown

Click "Save"
```

---

## Configure Email Notifications (Optional)

```
Manage Jenkins → Configure System → Extended E-mail Notification

SMTP server: smtp.gmail.com (for Gmail)
SMTP Port: 465
Credentials: Add Gmail app password
Use SSL: Yes

Default Content Type: HTML
Default Subject: $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password: Google Account → Security → 2-Step Verification → App passwords
3. Use app password in Jenkins credentials

---

## Verification Checklist

- [ ] All required plugins installed
- [ ] JDK configured
- [ ] Maven configured
- [ ] Docker configured
- [ ] SonarQube Scanner configured
- [ ] Dependency-Check configured
- [ ] GitHub credentials added
- [ ] Docker Hub credentials added
- [ ] SonarQube token added
- [ ] SonarQube server configured in Jenkins
- [ ] Email notifications configured (optional)

---

## Troubleshooting

### Plugin Installation Fails
```bash
# Check Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Restart Jenkins
sudo systemctl restart jenkins
```

### SonarQube Connection Issues
- Verify security group allows port 9000
- Check SonarQube is running: `sudo docker compose ps`
- Verify private IP is correct
- Test connection: `curl http://<SONARQUBE_PRIVATE_IP>:9000`

### Docker Permission Issues
```bash
# Ensure jenkins user is in docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

## Next Steps
Proceed to `05-sample-app/` to create a sample application for the pipeline.