# Deployment Guide

Complete guide for deploying the Phishing Awareness Training Platform in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Cloud Deployments](#cloud-deployments)
6. [Monitoring Setup](#monitoring-setup)
7. [Backup and Recovery](#backup-and-recovery)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4 GB
- Storage: 20 GB
- OS: Ubuntu 20.04+, Debian 11+, RHEL 8+, or macOS

**Recommended for Production:**
- CPU: 4+ cores
- RAM: 8+ GB
- Storage: 50+ GB SSD
- OS: Ubuntu 22.04 LTS

### Software Dependencies

- Python 3.10 or higher
- Docker 20.10+ and Docker Compose 2.0+ (for containerized deployment)
- PostgreSQL 13+ (for production) or SQLite 3.35+
- Nginx 1.20+ (for reverse proxy)
- Git 2.30+

---

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/Raoof128/phishing-platform.git
cd phishing-platform

# Initialize development environment
make init

# Configure settings
cp automation/config/api_config.yaml.example automation/config/api_config.yaml
cp automation/config/smtp_config.yaml.example automation/config/smtp_config.yaml
cp .env.example .env

# Edit configuration files with your settings
nano automation/config/api_config.yaml
nano .env

# Run tests
make test

# Start dashboard
make run-dashboard
```

### Manual Setup

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v

# Start dashboard
python dashboard/app.py
```

The dashboard will be available at `http://localhost:5000`

---

## Docker Deployment

### Single Container (Development)

```bash
# Build image
docker build -t phishing-platform:latest .

# Run container
docker run -d \
  --name phishing-platform \
  -p 5000:5000 \
  -v $(pwd)/automation/config:/app/automation/config \
  -v $(pwd)/data:/app/data \
  -e FLASK_ENV=development \
  phishing-platform:latest
```

### Docker Compose (Recommended)

**1. Create docker-compose.yml:**

```yaml
version: '3.8'

services:
  # GoPhish Service
  gophish:
    image: gophish/gophish:latest
    container_name: gophish
    ports:
      - "3333:3333"  # Admin interface
      - "8080:8080"  # Phishing server
    volumes:
      - gophish-data:/app/data
    environment:
      - GOPHISH_INITIAL_ADMIN_PASSWORD=ChangeMeInProduction
    restart: unless-stopped
    networks:
      - phishing-network

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      POSTGRES_DB: gophish
      POSTGRES_USER: gophish
      POSTGRES_PASSWORD: secure_password_here
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - phishing-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gophish"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Dashboard Service
  dashboard:
    build: .
    container_name: phishing-dashboard
    ports:
      - "5000:5000"
    volumes:
      - ./automation/config:/app/automation/config
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://gophish:secure_password_here@postgres:5432/gophish
    depends_on:
      postgres:
        condition: service_healthy
      gophish:
        condition: service_started
    restart: unless-stopped
    networks:
      - phishing-network

  # Redis Cache (Optional, for v1.4.0+)
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - phishing-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - dashboard
      - gophish
    restart: unless-stopped
    networks:
      - phishing-network

volumes:
  gophish-data:
  postgres-data:
  redis-data:

networks:
  phishing-network:
    driver: bridge
```

**2. Create nginx.conf:**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream dashboard {
        server dashboard:5000;
    }

    upstream gophish {
        server gophish:3333;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=60r/m;

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Dashboard
        location / {
            proxy_pass http://dashboard;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API with rate limiting
        location /api/ {
            limit_req zone=api_limit burst=10 nodelay;
            proxy_pass http://dashboard;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # GoPhish admin interface
        location /gophish/ {
            proxy_pass http://gophish/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

**3. Start services:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## Production Deployment

### Ubuntu 22.04 Server Setup

**1. System Preparation:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    certbot \
    python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash phishing
sudo usermod -aG sudo phishing
```

**2. Database Setup:**

```bash
# Switch to postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE gophish;
CREATE USER gophish WITH ENCRYPTED PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE gophish TO gophish;
\q
```

**3. Application Setup:**

```bash
# Switch to application user
sudo su - phishing

# Clone repository
git clone https://github.com/Raoof128/phishing-platform.git
cd phishing-platform

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure application
cp automation/config/api_config.yaml.example automation/config/api_config.yaml
cp .env.example .env

# Edit configuration
nano automation/config/api_config.yaml
nano .env

# Test configuration
pytest tests/ -v
```

**4. Systemd Service Setup:**

Create `/etc/systemd/system/phishing-dashboard.service`:

```ini
[Unit]
Description=Phishing Platform Dashboard
After=network.target postgresql.service

[Service]
Type=simple
User=phishing
Group=phishing
WorkingDirectory=/home/phishing/phishing-platform
Environment="PATH=/home/phishing/phishing-platform/venv/bin"
ExecStart=/home/phishing/phishing-platform/venv/bin/python dashboard/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable phishing-dashboard
sudo systemctl start phishing-dashboard
sudo systemctl status phishing-dashboard
```

**5. Nginx Configuration:**

Create `/etc/nginx/sites-available/phishing-platform`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if any)
    location /static/ {
        alias /home/phishing/phishing-platform/dashboard/static/;
        expires 30d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/phishing-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**6. SSL Certificate Setup:**

```bash
# Obtain Let's Encrypt certificate
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

**7. Firewall Configuration:**

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

---

## Cloud Deployments

### AWS Deployment

**Architecture:**
```
Internet → ALB → ECS/Fargate → RDS (PostgreSQL) → ElastiCache (Redis)
```

**1. RDS Database:**

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier phishing-platform-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.3 \
    --master-username admin \
    --master-user-password YourSecurePassword \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-subnet-group-name your-subnet-group \
    --backup-retention-period 7 \
    --publicly-accessible false
```

**2. ECS Task Definition:**

```json
{
  "family": "phishing-platform",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "dashboard",
      "image": "your-ecr-repo/phishing-platform:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://admin:password@rds-endpoint:5432/gophish"
        },
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/phishing-platform",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

**Using Cloud Run:**

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/phishing-platform

# Deploy to Cloud Run
gcloud run deploy phishing-platform \
    --image gcr.io/PROJECT_ID/phishing-platform \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DATABASE_URL=postgresql://user:pass@/dbname?host=/cloudsql/PROJECT_ID:REGION:INSTANCE

# Connect to Cloud SQL
gcloud sql instances create phishing-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1
```

### Azure Deployment

**Using Azure Container Instances:**

```bash
# Create resource group
az group create --name phishing-platform-rg --location eastus

# Create Azure Database for PostgreSQL
az postgres server create \
    --resource-group phishing-platform-rg \
    --name phishing-platform-db \
    --location eastus \
    --admin-user phishadmin \
    --admin-password SecurePassword123 \
    --sku-name B_Gen5_1

# Deploy container
az container create \
    --resource-group phishing-platform-rg \
    --name phishing-dashboard \
    --image your-registry/phishing-platform:latest \
    --dns-name-label phishing-platform \
    --ports 5000 \
    --environment-variables \
        DATABASE_URL='postgresql://...' \
        FLASK_ENV='production'
```

---

## Monitoring Setup

### Prometheus and Grafana

**1. Add Prometheus metrics to your app:**

Install dependencies:
```bash
pip install prometheus-flask-exporter
```

Update `dashboard/app.py`:
```python
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
```

**2. Prometheus Configuration:**

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'phishing-dashboard'
    static_configs:
      - targets: ['dashboard:5000']
```

**3. Docker Compose for Monitoring:**

Add to your docker-compose.yml:
```yaml
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - phishing-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - phishing-network
```

### Health Checks

```bash
# Application health check
curl http://localhost:5000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2025-01-14T15:30:00Z",
  "services": {
    "campaign_api": true,
    "analytics": true
  }
}
```

### Log Aggregation

**Using ELK Stack:**

```yaml
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
```

---

## Backup and Recovery

### Database Backup

**Automated daily backups:**

Create `/etc/cron.daily/backup-phishing-db`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/phishing"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U gophish gophish | gzip > $BACKUP_DIR/gophish_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "gophish_*.sql.gz" -mtime +30 -delete
```

Make executable:
```bash
chmod +x /etc/cron.daily/backup-phishing-db
```

### Restore from Backup

```bash
# Restore database
gunzip < /var/backups/phishing/gophish_20250114_150000.sql.gz | psql -U gophish gophish
```

### Disaster Recovery Plan

1. **Backup Strategy:**
   - Daily automated database backups
   - Weekly full system backups
   - Off-site backup storage (AWS S3, Google Cloud Storage)

2. **Recovery Time Objective (RTO):** < 2 hours
3. **Recovery Point Objective (RPO):** < 24 hours

---

## Troubleshooting

### Common Issues

**1. Dashboard won't start:**
```bash
# Check logs
sudo journalctl -u phishing-dashboard -n 50

# Check if port is in use
sudo lsof -i :5000

# Check configuration
python dashboard/app.py
```

**2. Database connection errors:**
```bash
# Test PostgreSQL connection
psql -h localhost -U gophish -d gophish

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

**3. GoPhish API errors:**
```bash
# Verify GoPhish is running
curl http://localhost:3333/api/campaigns

# Check GoPhish logs
docker logs gophish
```

**4. Nginx errors:**
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

---

## Performance Tuning

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_results_email ON results(email);
CREATE INDEX idx_events_campaign_id ON events(campaign_id);

-- Analyze tables
ANALYZE campaigns;
ANALYZE results;
ANALYZE events;
```

### Application Optimization

- Enable caching (Redis) for frequently accessed data
- Use connection pooling for database
- Compress responses with gzip
- Implement CDN for static assets

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall rules
- [ ] Enable database encryption at rest
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Enable fail2ban for SSH protection
- [ ] Review and update security headers
- [ ] Implement authentication (v1.2.0+)
- [ ] Regular security updates

---

## Support

For deployment issues:
- GitHub Issues: https://github.com/Raoof128/phishing-platform/issues
- Documentation: https://github.com/Raoof128/phishing-platform/docs

---

**Last Updated**: 2025-01-14
