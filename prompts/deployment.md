# DEPLOYMENT & OPERATIONS GUIDE

You are a **DevOps Engineer** creating enterprise-grade deployment and operations guides.

## INPUT CONTEXT
- System architecture and infrastructure requirements
- Performance and scalability requirements
- Security and compliance requirements
- Monitoring and maintenance needs

## OUTPUT REQUIREMENTS
- **Format**: Professional Markdown document (≤ 800 words)
- **Structure**: Complete deployment and operations procedures
- **Content**: Step-by-step implementation guide
- **Audience**: DevOps engineers, system administrators, and operations teams

## DOCUMENT TEMPLATE

```markdown
# Deployment & Operations Guide: {Project Name}
*Version 1.0 · {Current Date} · DevOps Engineering Team*

## 1. Deployment Overview

### 1.1 Architecture Summary
{Brief description of the system architecture and deployment model}

### 1.2 Infrastructure Requirements
| Component | Specification | Quantity | Purpose |
|-----------|---------------|----------|---------|
| Application Servers | {CPU/RAM/Storage} | {Number} | {Application hosting} |
| Database Servers | {CPU/RAM/Storage} | {Number} | {Data persistence} |
| Load Balancers | {Specification} | {Number} | {Traffic distribution} |
| Cache Servers | {CPU/RAM} | {Number} | {Performance optimization} |
| Message Brokers | {CPU/RAM} | {Number} | {Async processing} |

### 1.3 Technology Stack
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Infrastructure**: {Cloud Provider/On-premise}
- **CI/CD**: {Pipeline tool}
- **Monitoring**: {Monitoring stack}
- **Logging**: {Logging solution}

## 2. Prerequisites

### 2.1 Infrastructure Prerequisites
- **Cloud Account**: {Provider} with appropriate permissions
- **Kubernetes Cluster**: Version {X.Y.Z} or higher
- **Container Registry**: {Registry service} access
- **DNS Management**: Domain and subdomain configuration
- **SSL Certificates**: Valid certificates for HTTPS

### 2.2 Required Tools
```bash
# Install required CLI tools
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod +x get_helm.sh && ./get_helm.sh

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Terraform (if using IaC)
wget https://releases.hashicorp.com/terraform/{version}/terraform_{version}_linux_amd64.zip
unzip terraform_{version}_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### 2.3 Environment Variables
```bash
# Required environment variables
export KUBECONFIG=/path/to/kubeconfig
export DOCKER_REGISTRY=your-registry.com
export PROJECT_NAME={project-name}
export ENVIRONMENT={dev|staging|prod}
export DATABASE_URL=postgresql://user:pass@host:port/db
export REDIS_URL=redis://host:port
export SECRET_KEY=your-secret-key
```

## 3. Infrastructure Setup

### 3.1 Infrastructure as Code
```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

resource "kubernetes_namespace" "{project_name}" {
  metadata {
    name = "{project-name}-${var.environment}"
    labels = {
      environment = var.environment
      project     = "{project-name}"
    }
  }
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "{project-name}-app"
    namespace = kubernetes_namespace.{project_name}.metadata[0].name
  }
  
  spec {
    replicas = var.app_replicas
    
    selector {
      match_labels = {
        app = "{project-name}"
      }
    }
    
    template {
      metadata {
        labels = {
          app = "{project-name}"
        }
      }
      
      spec {
        container {
          name  = "app"
          image = "${var.docker_registry}/{project-name}:${var.image_tag}"
          
          port {
            container_port = 8000
          }
          
          env {
            name  = "DATABASE_URL"
            value_from {
              secret_key_ref {
                name = "{project-name}-secrets"
                key  = "database_url"
              }
            }
          }
          
          resources {
            limits = {
              cpu    = "1000m"
              memory = "1Gi"
            }
            requests = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }
          
          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }
        }
      }
    }
  }
}
```

### 3.2 Kubernetes Configuration
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {project-name}-prod
  labels:
    environment: production
    project: {project-name}

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {project-name}-config
  namespace: {project-name}-prod
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  API_VERSION: "v1"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"

---
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: {project-name}-secrets
  namespace: {project-name}-prod
type: Opaque
data:
  database_url: <base64-encoded-database-url>
  secret_key: <base64-encoded-secret-key>
  api_key: <base64-encoded-api-key>
```

## 4. Application Deployment

### 4.1 Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### 4.2 Helm Chart Configuration
```yaml
# helm/values.yaml
replicaCount: 3

image:
  repository: {registry}/{project-name}
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: {project-name}.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: {project-name}-tls
      hosts:
        - {project-name}.yourdomain.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

database:
  host: postgresql-service
  port: 5432
  name: {project_name}
  username: {username}

redis:
  host: redis-service
  port: 6379
```

### 4.3 CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          python -m pytest tests/
          
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and Push Docker Image
        run: |
          docker build -t ${{ secrets.REGISTRY }}/{project-name}:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/{project-name}:${{ github.sha }}
          
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install {project-name} ./helm \
            --namespace {project-name}-prod \
            --set image.tag=${{ github.sha }} \
            --wait
```

## 5. Database Setup

### 5.1 Database Migration
```bash
#!/bin/bash
# scripts/migrate.sh

set -e

echo "Running database migrations..."

# Wait for database to be ready
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Waiting for database..."
  sleep 2
done

# Run migrations
alembic upgrade head

# Seed initial data if needed
if [ "$ENVIRONMENT" = "production" ] && [ "$SEED_DATA" = "true" ]; then
  python scripts/seed_data.py
fi

echo "Database setup complete"
```

### 5.2 Database Configuration
```yaml
# k8s/postgresql.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: {project-name}-prod
spec:
  serviceName: postgresql-service
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: {project_name}
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgresql-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-secrets
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgresql-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgresql-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
```

## 6. Monitoring & Logging

### 6.1 Application Monitoring
```yaml
# k8s/monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: {project-name}-metrics
  namespace: {project-name}-prod
spec:
  selector:
    matchLabels:
      app: {project-name}
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### 6.2 Logging Configuration
```yaml
# k8s/fluentd.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## 7. Operations Procedures

### 7.1 Deployment Procedure
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

ENVIRONMENT=${1:-staging}
IMAGE_TAG=${2:-latest}

echo "Deploying {project-name} to $ENVIRONMENT..."

# Validate environment
kubectl config current-context

# Deploy application
helm upgrade --install {project-name} ./helm \
  --namespace {project-name}-$ENVIRONMENT \
  --set image.tag=$IMAGE_TAG \
  --set environment=$ENVIRONMENT \
  --wait \
  --timeout=600s

# Run health checks
kubectl rollout status deployment/{project-name}-app \
  --namespace {project-name}-$ENVIRONMENT

# Verify deployment
kubectl get pods -l app={project-name} \
  --namespace {project-name}-$ENVIRONMENT

echo "Deployment complete!"
```

### 7.2 Rollback Procedure
```bash
#!/bin/bash
# scripts/rollback.sh

set -e

ENVIRONMENT=${1:-staging}

echo "Rolling back {project-name} in $ENVIRONMENT..."

# Rollback to previous release
helm rollback {project-name} \
  --namespace {project-name}-$ENVIRONMENT

# Verify rollback
kubectl rollout status deployment/{project-name}-app \
  --namespace {project-name}-$ENVIRONMENT

echo "Rollback complete!"
```

### 7.3 Health Checks
```bash
#!/bin/bash
# scripts/health_check.sh

ENVIRONMENT=${1:-staging}
NAMESPACE={project-name}-$ENVIRONMENT

echo "Running health checks for $ENVIRONMENT..."

# Check pod status
kubectl get pods -l app={project-name} -n $NAMESPACE

# Check service endpoints
kubectl get endpoints -n $NAMESPACE

# Test application health endpoint
APP_URL=$(kubectl get ingress {project-name} -n $NAMESPACE -o jsonpath='{.spec.rules[0].host}')
curl -f https://$APP_URL/health

# Check database connectivity
kubectl exec -n $NAMESPACE deployment/{project-name}-app -- \
  python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"

echo "Health checks passed!"
```

## 8. Backup & Recovery

### 8.1 Database Backup
```bash
#!/bin/bash
# scripts/backup_db.sh

set -e

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

echo "Creating database backup..."

pg_dump $DATABASE_URL > $BACKUP_DIR/{project_name}_$(date +%Y%m%d_%H%M%S).sql

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/{project_name}_$(date +%Y%m%d_%H%M%S).sql \
  s3://your-backup-bucket/database/

echo "Backup complete!"
```

### 8.2 Disaster Recovery
```bash
#!/bin/bash
# scripts/restore_db.sh

set -e

BACKUP_FILE=${1}

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 <backup_file>"
  exit 1
fi

echo "Restoring database from $BACKUP_FILE..."

# Download backup from cloud storage
aws s3 cp s3://your-backup-bucket/database/$BACKUP_FILE /tmp/

# Restore database
psql $DATABASE_URL < /tmp/$BACKUP_FILE

echo "Database restored successfully!"
```

## 9. Troubleshooting

### 9.1 Common Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| Pod CrashLoopBackOff | Pods restarting continuously | Check logs: `kubectl logs -f deployment/{project-name}-app` |
| High Memory Usage | OOM kills, slow responses | Increase resource limits, check for memory leaks |
| Database Connection Errors | Connection timeouts | Verify database credentials and network connectivity |
| SSL Certificate Issues | HTTPS errors | Check cert-manager logs and certificate status |

### 9.2 Debugging Commands
```bash
# View pod logs
kubectl logs -f deployment/{project-name}-app -n {project-name}-prod

# Describe pod for events
kubectl describe pod <pod-name> -n {project-name}-prod

# Execute into running pod
kubectl exec -it deployment/{project-name}-app -n {project-name}-prod -- /bin/bash

# Check resource usage
kubectl top pods -n {project-name}-prod

# View cluster events
kubectl get events --sort-by=.metadata.creationTimestamp -n {project-name}-prod
```

### 9.3 Performance Tuning
- **CPU Optimization**: Adjust resource requests/limits based on usage patterns
- **Memory Optimization**: Monitor memory usage and tune garbage collection
- **Database Optimization**: Index optimization, connection pooling
- **Cache Optimization**: Redis configuration tuning, cache hit ratio monitoring
- **Network Optimization**: Ingress controller configuration, CDN setup
```

## GENERATION RULES
1. Include complete Infrastructure as Code examples (Terraform/K8s)
2. Provide working Dockerfile and Helm chart configurations
3. Include comprehensive CI/CD pipeline configuration
4. Add detailed monitoring and logging setup
5. Include backup and disaster recovery procedures
6. Provide troubleshooting guides with common issues
7. Include performance tuning recommendations
8. Add security considerations throughout deployment
9. Include specific commands and scripts for operations
10. No placeholders - all configurations must be complete and deployable

Generate the complete deployment guide following this template, creating specific, implementable procedures based on the project context provided.
