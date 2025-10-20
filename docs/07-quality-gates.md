# Step 7: SonarQube Quality Gate Configuration

## What is a Quality Gate?

A Quality Gate is a set of conditions that code must meet before being considered production-ready. It acts as a checkpoint in your CI/CD pipeline.

## Access SonarQube

1. Open browser: `http://<SONARQUBE_PUBLIC_IP>:9000`
2. Login with credentials (default: admin/admin)
3. Change password when prompted

---

## Creating Quality Gates

### Method 1: Using Default Quality Gate (Recommended for Start)

The default "Sonar way" quality gate includes:
- Code Coverage > 80%
- Duplicated Lines < 3%
- Maintainability Rating = A
- Reliability Rating = A
- Security Rating = A
- Security Hotspots Reviewed = 100%

#### Steps:
1. Go to **Quality Gates** in top menu
2. View "Sonar way" (default)
3. Click on your project
4. Under **Project Settings** → **Quality Gate**
5. Select "Sonar way"

### Method 2: Create Custom Quality Gate

#### Steps to Create Custom Quality Gate:

1. **Navigate to Quality Gates**
   ```
   SonarQube Dashboard → Quality Gates → Create
   ```

2. **Name Your Quality Gate**
   ```
   Name: Production-Ready
   Description: Strict quality gate for production deployments
   ```

3. **Add Conditions**

Click "Add Condition" and configure the following:

#### Security Conditions
```
Metric: Security Rating
Operator: is worse than
Value: A
On: Overall Code
```

```
Metric: Security Hotspots Reviewed
Operator: is less than
Value: 100
On: Overall Code
```

```
Metric: Vulnerabilities
Operator: is greater than
Value: 0
On: Overall Code
```

#### Reliability Conditions
```
Metric: Reliability Rating
Operator: is worse than
Value: A
On: Overall Code
```

```
Metric: Bugs
Operator: is greater than
Value: 0
On: Overall Code
```

#### Maintainability Conditions
```
Metric: Maintainability Rating
Operator: is worse than
Value: A
On: Overall Code
```

```
Metric: Code Smells
Operator: is greater than
Value: 5
On: Overall Code
```

```
Metric: Technical Debt Ratio
Operator: is greater than
Value: 5%
On: Overall Code
```

#### Coverage Conditions
```
Metric: Coverage
Operator: is less than
Value: 80%
On: Overall Code
```

```
Metric: Line Coverage
Operator: is less than
Value: 75%
On: Overall Code
```

#### Duplication Conditions
```
Metric: Duplicated Lines (%)
Operator: is greater than
Value: 3%
On: Overall Code
```

#### New Code Conditions (Important for CI/CD)
```
Metric: Coverage on New Code
Operator: is less than
Value: 80%
On: New Code
```

```
Metric: Duplicated Lines (%) on New Code
Operator: is greater than
Value: 3%
On: New Code
```

```
Metric: Maintainability Rating on New Code
Operator: is worse than
Value: A
On: New Code
```

```
Metric: Reliability Rating on New Code
Operator: is worse than
Value: A
On: New Code
```

```
Metric: Security Rating on New Code
Operator: is worse than
Value: A
On: New Code
```

---

## Assign Quality Gate to Project

### Option 1: Via Web UI

1. Go to your project in SonarQube
2. Click **Project Settings** → **Quality Gate**
3. Select your custom quality gate
4. Click **Save**

### Option 2: Set as Default

1. Go to **Quality Gates**
2. Click on your custom quality gate
3. Click **Set as Default**
4. All new projects will use this gate

---

## Quality Gate Levels

### Level 1: Lenient (For Learning)
```
- Code Coverage > 60%
- Duplicated Lines < 5%
- Maintainability Rating <= B
- Reliability Rating <= B
- Security Rating <= B
```

### Level 2: Moderate (For Development)
```
- Code Coverage > 70%
- Duplicated Lines < 4%
- Maintainability Rating = A
- Reliability Rating = A
- Security Rating = A
```

### Level 3: Strict (For Production)
```
- Code Coverage > 80%
- Duplicated Lines < 3%
- Maintainability Rating = A
- Reliability Rating = A
- Security Rating = A
- Zero Vulnerabilities
- Zero Bugs
- All Security Hotspots Reviewed
```

---

## Understanding Quality Gate Status

### ✓ Passed (Green)
- All conditions met
- Code is ready for deployment
- Pipeline continues

### ✗ Failed (Red)
- One or more conditions not met
- Pipeline should fail
- Code needs improvements

### ⚠ Warning (Orange)
- Some conditions on new code not met
- Review required
- Decision to proceed or fix

---

## Testing Quality Gates

### Scenario 1: Make Quality Gate Pass

To ensure your sample app passes, you need to:

1. **Fix Code Smells**
   - Remove dead code
   - Simplify complex methods
   - Remove code duplication

2. **Increase Test Coverage**
   - Add more unit tests
   - Aim for >80% coverage

3. **Fix Security Issues**
   - Update vulnerable dependencies
   - Address security hotspots

### Scenario 2: Make Quality Gate Fail (For Testing)

The sample application intentionally has issues:

1. **Code Smells**
   - `unnecessaryComplexity()` method has cognitive complexity
   - `unusedMethod()` is dead code
   - Expected: Maintainability Rating = C or D

2. **Low Coverage**
   - Only 3 tests for entire application
   - Expected: Coverage < 80%

3. **Vulnerable Dependencies**
   - Log4j 2.14.1 has CVE-2021-44228
   - Expected: Security issues detected

---

## Webhook Configuration (For Real-time Updates)

### Setup Webhook in SonarQube

1. **Navigate to Webhooks**
   ```
   Administration → Configuration → Webhooks → Create
   ```

2. **Configure Webhook**
   ```
   Name: Jenkins
   URL: http://<JENKINS_PRIVATE_IP>:8080/sonarqube-webhook/
   Secret: (Optional - generate random string)
   ```

3. **Save**

This allows SonarQube to push quality gate results to Jenkins immediately.

---

## Quality Gate in Jenkins Pipeline

The Jenkinsfile already includes quality gate checking:

```groovy
stage('10. Quality Gate Check') {
    steps {
        script {
            timeout(time: 5, unit: 'MINUTES') {
                def qg = waitForQualityGate()
                
                if (qg.status != 'OK') {
                    error("Quality Gate failed: ${qg.status}")
                }
            }
        }
    }
}
```

### How It Works:

1. **Maven Sonar Plugin** sends analysis to SonarQube
2. **SonarQube** analyzes code and applies quality gate rules
3. **Webhook** (or polling) returns results to Jenkins
4. **Jenkins** checks status and fails build if gate fails

---

## Quality Gate Reports

### View in SonarQube

1. **Project Dashboard**
   - Overall quality gate status
   - Failed conditions highlighted

2. **Measures**
   - Detailed metrics
   - Historical trends

3. **Issues**
   - All bugs, vulnerabilities, code smells
   - Severity and type

### View in Jenkins

1. **Build Page**
   - Quality gate status badge
   - Link to SonarQube report

2. **Console Output**
   - Quality gate results
   - Failed conditions

---

## Quality Gate Best Practices

### 1. Start Lenient, Get Stricter
```
Week 1-2: Lenient gate (60% coverage, Rating B)
Week 3-4: Moderate gate (70% coverage, Rating A)
Week 5+: Strict gate (80% coverage, Zero bugs)
```

### 2. Focus on New Code
```
- Always enforce strict rules on new code
- Allow technical debt on old code initially
- Gradually pay down technical debt
```

### 3. Different Gates for Different Branches
```
- feature/* branches: Lenient
- develop branch: Moderate
- main/master branch: Strict
```

### 4. Separate Gates for Different Project Types
```
- Critical services: Strictest gate
- Internal tools: Moderate gate
- POCs/experiments: Lenient gate
```

---

## Troubleshooting Quality Gates

### Issue: Quality Gate Always Passes

**Cause**: No conditions set or conditions too lenient

**Solution**:
```
1. Verify conditions are added
2. Check "On Overall Code" vs "On New Code"
3. Ensure quality gate is assigned to project
```

### Issue: Quality Gate Always Fails

**Cause**: Conditions too strict for current code

**Solution**:
```
1. Review which conditions are failing
2. Adjust thresholds temporarily
3. Create improvement plan
4. Gradually tighten conditions
```

### Issue: Jenkins Doesn't Receive Quality Gate

**Cause**: Webhook not configured or network issues

**Solution**:
```
1. Check webhook configuration in SonarQube
2. Verify Jenkins URL is accessible from SonarQube
3. Check security groups allow traffic
4. Test webhook manually
```

### Issue: Timeout Waiting for Quality Gate

**Cause**: SonarQube processing delay or webhook failure

**Solution**:
```
1. Increase timeout in Jenkinsfile
2. Check SonarQube server resources
3. Verify webhook is working
4. Check SonarQube logs
```

---

## Monitoring Quality Over Time

### SonarQube Activity Tab

View project history:
```
Project → Activity
- Quality gate status over time
- Metrics trends
- Analysis history
```

### Jenkins Build Trends

View build history:
```
Jenkins Job → Status
- Build success/failure rates
- Quality gate pass/fail trends
- Time to fix issues
```

---

## Quality Gate Metrics Explained

### Coverage
- **Line Coverage**: % of lines executed by tests
- **Branch Coverage**: % of conditional branches tested
- **Overall Coverage**: Combined metric

### Maintainability
- **Code Smells**: Maintainability issues
- **Technical Debt**: Time to fix all code smells
- **Maintainability Rating**: A-E scale

### Reliability
- **Bugs**: Coding errors that could cause failures
- **Reliability Rating**: A-E scale

### Security
- **Vulnerabilities**: Security issues
- **Security Hotspots**: Code that needs review
- **Security Rating**: A-E scale

### Duplication
- **Duplicated Lines**: Exact copies of code
- **Duplicated Blocks**: Larger sections of duplication

---

## Example Quality Gate Configurations

### For Sample Java App (Starting Point)

```yaml
Name: Learning-Gate
Conditions:
  - Code Smells <= 10
  - Bugs <= 2
  - Vulnerabilities <= 0
  - Coverage >= 60%
  - Duplicated Lines <= 5%
  - Maintainability Rating <= B
  - Reliability Rating <= B
  - Security Rating <= A
```

### For Production Application

```yaml
Name: Production-Gate
Conditions:
  - Code Smells <= 0
  - Bugs <= 0
  - Vulnerabilities <= 0
  - Security Hotspots Reviewed = 100%
  - Coverage >= 80%
  - Coverage on New Code >= 90%
  - Duplicated Lines <= 3%
  - All Ratings = A
```

---

## Next Steps

1. Create your quality gate in SonarQube
2. Assign it to your project
3. Run the pipeline and see it fail (due to intentional issues)
4. Fix issues one by one
5. Watch quality gate pass

Proceed to `08-testing-errors.md` to learn how to introduce and fix errors for testing.