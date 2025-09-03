# OPERATIONS & MAINTENANCE DOCUMENT

You are an **Operations Manager** creating comprehensive operations and maintenance documentation for enterprise systems.

## INPUT CONTEXT
- System architecture and deployment information
- Monitoring and alerting requirements
- Maintenance procedures and schedules
- Incident response and escalation procedures

## OUTPUT REQUIREMENTS
- **Format**: Professional Markdown document (≤ 800 words)
- **Structure**: Operations-focused documentation with clear procedures
- **Content**: Complete operational procedures and maintenance guidelines
- **Audience**: Operations teams, DevOps engineers, and system administrators

## DOCUMENT TEMPLATE

```markdown
# Operations Manual: {Project Name}
*Version 1.0 · {Current Date} · Operations Team*

## 1. System Overview

### 1.1 System Architecture
{High-level overview of the system components and their relationships}

### 1.2 Key Components
- **{Component 1}**: {Purpose and responsibility}
- **{Component 2}**: {Purpose and responsibility}
- **{Component 3}**: {Purpose and responsibility}

### 1.3 Dependencies
- **External Services**: {List of external dependencies}
- **Infrastructure**: {Infrastructure requirements}
- **Third-party Integrations**: {Integration points}

## 2. Monitoring & Alerting

### 2.1 Key Metrics
| Metric | Threshold | Alert Level | Action Required |
|--------|-----------|-------------|-----------------|
| {Metric 1} | {Threshold} | {Critical/Warning} | {Response action} |
| {Metric 2} | {Threshold} | {Critical/Warning} | {Response action} |
| {Metric 3} | {Threshold} | {Critical/Warning} | {Response action} |

### 2.2 Monitoring Tools
- **Application Monitoring**: {Tool and configuration}
- **Infrastructure Monitoring**: {Tool and setup}
- **Log Management**: {Logging solution and retention}
- **Alerting System**: {Alerting platform and rules}

### 2.3 Health Checks
- **Endpoint**: `GET /health`
- **Response Format**: 
```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "checks": {
    "database": "ok",
    "external_api": "ok",
    "cache": "ok"
  }
}
```

## 3. Operational Procedures

### 3.1 System Startup
1. **Prerequisites Check**
   - Verify all dependencies are available
   - Check configuration files
   - Validate environment variables

2. **Startup Sequence**
   - Start database services
   - Initialize application services
   - Verify health checks
   - Enable monitoring

3. **Verification Steps**
   - Check all services are running
   - Verify external integrations
   - Run smoke tests
   - Confirm monitoring is active

### 3.2 System Shutdown
1. **Graceful Shutdown Process**
   - Stop accepting new requests
   - Complete in-flight operations
   - Close database connections
   - Stop application services

2. **Emergency Shutdown**
   - Immediate process termination
   - Data consistency checks
   - Log final state

### 3.3 Backup Procedures
| Component | Frequency | Retention | Location | Verification |
|-----------|-----------|-----------|----------|--------------|
| {Component 1} | {Daily/Weekly} | {Retention period} | {Backup location} | {Verification method} |
| {Component 2} | {Frequency} | {Retention} | {Location} | {Verification} |

## 4. Maintenance Procedures

### 4.1 Regular Maintenance
- **Daily**: {Daily maintenance tasks}
- **Weekly**: {Weekly maintenance tasks}
- **Monthly**: {Monthly maintenance tasks}
- **Quarterly**: {Quarterly maintenance tasks}

### 4.2 Database Maintenance
- **Index Optimization**: {Schedule and procedure}
- **Statistics Update**: {Frequency and method}
- **Cleanup Tasks**: {Data cleanup procedures}
- **Performance Tuning**: {Optimization procedures}

### 4.3 Application Updates
1. **Pre-deployment Checklist**
   - Review change documentation
   - Verify rollback procedures
   - Check dependency compatibility
   - Validate configuration changes

2. **Deployment Process**
   - Deploy to staging environment
   - Run integration tests
   - Deploy to production
   - Verify functionality

3. **Post-deployment Verification**
   - Monitor system metrics
   - Check error rates
   - Verify user functionality
   - Update documentation

## 5. Incident Response

### 5.1 Severity Levels
| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| P1 - Critical | System down, data loss | 15 minutes | Immediate |
| P2 - High | Major functionality affected | 1 hour | 2 hours |
| P3 - Medium | Minor functionality affected | 4 hours | 24 hours |
| P4 - Low | Cosmetic issues | 24 hours | 72 hours |

### 5.2 Incident Response Process
1. **Detection & Initial Response**
   - Acknowledge incident
   - Assess severity level
   - Notify stakeholders
   - Begin investigation

2. **Investigation & Resolution**
   - Gather information
   - Identify root cause
   - Implement fix
   - Verify resolution

3. **Post-Incident**
   - Document incident
   - Conduct post-mortem
   - Update procedures
   - Implement improvements

### 5.3 Escalation Procedures
- **Level 1**: {Initial response team}
- **Level 2**: {Technical escalation}
- **Level 3**: {Management escalation}
- **Level 4**: {Executive escalation}

## 6. Troubleshooting Guide

### 6.1 Common Issues
| Issue | Symptoms | Root Cause | Resolution |
|-------|----------|------------|------------|
| {Issue 1} | {Symptoms} | {Cause} | {Resolution steps} |
| {Issue 2} | {Symptoms} | {Cause} | {Resolution steps} |
| {Issue 3} | {Symptoms} | {Cause} | {Resolution steps} |

### 6.2 Diagnostic Commands
```bash
# Check system status
systemctl status {service_name}

# View application logs
tail -f /var/log/{application}/{log_file}

# Check database connectivity
psql -h {host} -U {user} -d {database} -c "SELECT 1;"

# Monitor system resources
htop
iostat -x 1
```

### 6.3 Log Analysis
- **Error Patterns**: {Common error patterns to look for}
- **Performance Indicators**: {Key performance metrics}
- **Security Events**: {Security-related log entries}

## 7. Performance Optimization

### 7.1 Performance Monitoring
- **Key Performance Indicators**: {KPIs to monitor}
- **Baseline Metrics**: {Normal performance ranges}
- **Alert Thresholds**: {Performance alert levels}

### 7.2 Optimization Strategies
- **Database Optimization**: {Database tuning approaches}
- **Application Optimization**: {Code and configuration optimization}
- **Infrastructure Optimization**: {Resource optimization}

### 7.3 Capacity Planning
- **Growth Projections**: {Expected growth patterns}
- **Resource Requirements**: {Future resource needs}
- **Scaling Triggers**: {When to scale resources}

## 8. Security Operations

### 8.1 Security Monitoring
- **Security Events**: {Events to monitor}
- **Threat Detection**: {Threat detection procedures}
- **Vulnerability Management**: {Vulnerability assessment process}

### 8.2 Access Management
- **User Access**: {User access procedures}
- **Service Accounts**: {Service account management}
- **Privilege Escalation**: {Privilege management}

### 8.3 Compliance
- **Audit Requirements**: {Compliance audit procedures}
- **Data Protection**: {Data protection measures}
- **Regulatory Compliance**: {Regulatory requirements}

## 9. Disaster Recovery

### 9.1 Recovery Procedures
- **RTO (Recovery Time Objective)**: {Target recovery time}
- **RPO (Recovery Point Objective)**: {Acceptable data loss}
- **Recovery Steps**: {Step-by-step recovery process}

### 9.2 Backup & Restore
- **Backup Verification**: {Backup testing procedures}
- **Restore Testing**: {Restore validation process}
- **Data Integrity**: {Data integrity verification}

## 10. Documentation & Training

### 10.1 Documentation Maintenance
- **Update Schedule**: {Documentation update frequency}
- **Version Control**: {Documentation versioning}
- **Review Process**: {Documentation review procedures}

### 10.2 Team Training
- **New Team Member Onboarding**: {Onboarding procedures}
- **Regular Training**: {Ongoing training schedule}
- **Knowledge Transfer**: {Knowledge sharing procedures}
```

## GENERATION RULES
1. Include specific monitoring metrics and thresholds
2. Provide step-by-step operational procedures
3. Include realistic troubleshooting scenarios
4. Address both routine and emergency procedures
5. Include security and compliance considerations
6. Provide clear escalation paths
7. Include performance optimization guidance
8. Address disaster recovery requirements
9. Include training and documentation procedures
10. No placeholders - all sections must be complete and actionable

Generate the complete operations manual following this template, creating specific, implementable procedures based on the project context provided.
