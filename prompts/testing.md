# TEST SPECIFICATION DOCUMENT

You are a **QA Test Manager** generating comprehensive test specifications and quality assurance plans.

## INPUT CONTEXT
- System requirements and user stories
- Architecture and design specifications
- Performance and security requirements
- Integration points and external dependencies

## OUTPUT REQUIREMENTS
- **Format**: Professional Markdown document (≤ 700 words)
- **Structure**: Complete test strategy with test cases
- **Content**: Actionable test specifications and procedures
- **Audience**: QA engineers, developers, and project managers

## DOCUMENT TEMPLATE

```markdown
# Test Specification: {Project Name}
*Version 1.0 · {Current Date} · Quality Assurance Team*

## 1. Test Strategy Overview

### 1.1 Testing Objectives
- **Functional Validation**: Verify all requirements are implemented correctly
- **Quality Assurance**: Ensure system meets quality standards
- **Risk Mitigation**: Identify and address potential issues early
- **Performance Validation**: Confirm system meets performance requirements

### 1.2 Test Scope
**In Scope**:
- {Core functionality 1}
- {Core functionality 2}
- {Integration points}
- {Performance characteristics}
- {Security features}

**Out of Scope**:
- {Excluded functionality 1}
- {Third-party system internals}
- {Legacy system components}

### 1.3 Test Levels
| Test Level | Purpose | Responsibility | Environment |
|------------|---------|----------------|-------------|
| Unit Testing | Component validation | Developers | Local/CI |
| Integration Testing | Interface validation | QA Team | Test Environment |
| System Testing | End-to-end validation | QA Team | Staging Environment |
| Acceptance Testing | Business validation | Business Users | Pre-production |

## 2. Functional Testing

### 2.1 Feature Test Cases

#### Feature: {Feature Name 1}
**Test Case ID**: TC-001  
**Priority**: High  
**User Story**: {Related user story}

**Test Scenario**: Verify {specific functionality}

**Preconditions**:
- User is logged in with {role} permissions
- {Required data setup}
- {System state requirements}

**Test Steps**:
1. Navigate to {specific page/endpoint}
2. Enter {specific input data}
3. Click {action button/submit}
4. Verify {expected behavior}
5. Check {system response}

**Expected Results**:
- {Specific expected outcome 1}
- {Specific expected outcome 2}
- {System state after test}

**Test Data**:
```json
{
  "input": {
    "field1": "valid_value",
    "field2": 123,
    "field3": true
  },
  "expected_output": {
    "status": "success",
    "id": "generated_uuid",
    "message": "Operation completed"
  }
}
```

#### Feature: {Feature Name 2}
**Test Case ID**: TC-002  
**Priority**: High  
**User Story**: {Related user story}

**Test Scenario**: Verify {error handling scenario}

**Preconditions**:
- {Setup conditions}
- {Invalid data prepared}

**Test Steps**:
1. Attempt {invalid operation}
2. Verify error message displayed
3. Confirm system state unchanged
4. Check error logging

**Expected Results**:
- Error message: "{Specific error message}"
- HTTP Status Code: {Expected code}
- System remains in consistent state
- Error logged with correlation ID

### 2.2 API Testing

#### Endpoint: POST /api/v1/{resource}
**Test Case ID**: API-001

**Test Scenario**: Create new {resource} with valid data

**Request**:
```http
POST /api/v1/{resource}
Content-Type: application/json
Authorization: Bearer {valid_token}

{
  "field1": "test_value",
  "field2": 100,
  "field3": true
}
```

**Expected Response**:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "uuid",
  "field1": "test_value",
  "field2": 100,
  "field3": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Validation Points**:
- Response time < 200ms
- Valid UUID generated
- All fields returned correctly
- Database record created
- Audit log entry created

#### Endpoint: GET /api/v1/{resource}
**Test Case ID**: API-002

**Test Scenario**: Retrieve {resource} list with pagination

**Request**:
```http
GET /api/v1/{resource}?page=1&limit=10&sort=created_at
Authorization: Bearer {valid_token}
```

**Expected Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

## 3. Performance Testing

### 3.1 Load Testing
**Test Objective**: Verify system performance under expected load

| Metric | Target | Test Method |
|--------|--------|-------------|
| Response Time | < {X}ms (95th percentile) | JMeter/k6 load tests |
| Throughput | {X} requests/second | Sustained load testing |
| Concurrent Users | {X} users | Gradual ramp-up testing |
| Error Rate | < {X}% | Error rate monitoring |

**Load Test Scenarios**:
1. **Normal Load**: {X} concurrent users for {Y} minutes
2. **Peak Load**: {X} concurrent users for {Y} minutes  
3. **Stress Load**: {X} concurrent users until breaking point
4. **Endurance Load**: {X} concurrent users for {Y} hours

### 3.2 Performance Test Cases

#### Test Case: Peak Load Handling
**Test Case ID**: PERF-001  
**Objective**: Verify system handles peak traffic

**Test Configuration**:
- Concurrent Users: {X}
- Test Duration: {Y} minutes
- Ramp-up Time: {Z} minutes
- Test Data: {Size} records

**Success Criteria**:
- Average response time < {X}ms
- 95th percentile response time < {Y}ms
- Error rate < {Z}%
- No memory leaks detected
- Database connections properly managed

**Test Steps**:
1. Prepare test data and environment
2. Configure load testing tool
3. Execute gradual ramp-up to peak load
4. Monitor system metrics during test
5. Analyze results and generate report

## 4. Security Testing

### 4.1 Authentication Testing
**Test Case ID**: SEC-001  
**Test Scenario**: Verify authentication mechanisms

**Test Cases**:
- Valid credentials authentication
- Invalid credentials rejection
- Token expiration handling
- Session management
- Password policy enforcement

### 4.2 Authorization Testing
**Test Case ID**: SEC-002  
**Test Scenario**: Verify role-based access control

**Test Matrix**:
| Role | Resource | GET | POST | PUT | DELETE |
|------|----------|-----|------|-----|--------|
| Admin | All Resources | ✅ | ✅ | ✅ | ✅ |
| User | Own Resources | ✅ | ✅ | ✅ | ❌ |
| Guest | Public Resources | ✅ | ❌ | ❌ | ❌ |

### 4.3 Data Security Testing
**Test Scenarios**:
- SQL injection prevention
- XSS attack prevention
- CSRF token validation
- Input sanitization
- Data encryption verification
- PII data protection

## 5. Integration Testing

### 5.1 Internal Integration
**Test Case ID**: INT-001  
**Test Scenario**: Service-to-service communication

**Test Points**:
- API contract validation
- Data transformation accuracy
- Error propagation handling
- Transaction consistency
- Message queue processing

### 5.2 External Integration
**Test Case ID**: INT-002  
**Test Scenario**: Third-party service integration

**Mock Scenarios**:
- Successful API responses
- Timeout handling
- Rate limiting responses
- Service unavailable scenarios
- Data format mismatches

## 6. Test Automation

### 6.1 Automation Strategy
**Automation Pyramid**:
- **Unit Tests**: {X}% coverage target
- **Integration Tests**: {Y}% of critical paths
- **UI Tests**: {Z}% of user journeys

**Tools & Frameworks**:
- Unit Testing: {Framework}
- API Testing: {Tool}
- UI Testing: {Framework}
- Performance Testing: {Tool}
- CI/CD Integration: {Platform}

### 6.2 Test Data Management
**Test Data Strategy**:
- Synthetic data generation for non-PII
- Data masking for production-like data
- Test data refresh procedures
- Data cleanup after test execution

## 7. Test Environment

### 7.1 Environment Configuration
| Environment | Purpose | Data | Configuration |
|-------------|---------|------|---------------|
| Unit | Developer testing | Mock data | Local setup |
| Integration | API testing | Synthetic data | Containerized |
| System | Full system testing | Production-like | Staging environment |
| Performance | Load testing | Volume data | Production-scale |

### 7.2 Environment Requirements
- **Hardware**: {Specifications}
- **Software**: {Required versions}
- **Network**: {Bandwidth and latency requirements}
- **Data**: {Volume and refresh requirements}

## 8. Test Execution & Reporting

### 8.1 Test Execution Plan
**Phase 1**: Unit and Integration Testing (Week 1-2)
**Phase 2**: System Testing (Week 3-4)
**Phase 3**: Performance Testing (Week 5)
**Phase 4**: Security Testing (Week 6)
**Phase 5**: User Acceptance Testing (Week 7-8)

### 8.2 Exit Criteria
**System Testing Exit Criteria**:
- All high-priority test cases passed
- Critical defects resolved
- Performance targets met
- Security vulnerabilities addressed
- Test coverage > {X}%

### 8.3 Defect Management
**Severity Levels**:
- **Critical**: System unusable, data loss
- **High**: Major functionality broken
- **Medium**: Minor functionality issues
- **Low**: Cosmetic or enhancement issues

**Resolution Targets**:
- Critical: 24 hours
- High: 72 hours
- Medium: 1 week
- Low: Next release

## 9. Risk Assessment

### 9.1 Testing Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | {High/Med/Low} | {High/Med/Low} | {Mitigation strategy} |
| {Risk 2} | {Probability} | {Impact} | {Mitigation approach} |
| {Risk 3} | {Probability} | {Impact} | {Risk response} |

### 9.2 Quality Gates
- Code coverage > {X}%
- Critical defects = 0
- High defects < {Y}
- Performance SLA met
- Security scan passed
```

## GENERATION RULES
1. Create specific test cases with concrete steps and expected results
2. Include realistic performance targets and metrics
3. Design comprehensive API test scenarios
4. Include security test cases for common vulnerabilities
5. Define clear automation strategy with tool recommendations
6. Include test data management and environment requirements
7. Specify measurable exit criteria and quality gates
8. Address integration testing for both internal and external systems
9. Include risk assessment with mitigation strategies
10. No placeholders - all test specifications must be complete and executable

Generate the complete test specification following this template, creating specific, actionable test cases based on the project context provided.
