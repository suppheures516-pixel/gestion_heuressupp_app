# 🚀 Production Deployment Guide

## Overview

This guide will help you securely deploy your Django Gestion Heures application to production. The application has been configured with comprehensive security measures.

## 📋 Pre-Deployment Checklist

### 1. Environment Setup

1. **Copy environment template:**
   ```bash
   cp env.example .env
   ```

2. **Generate a new SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Update .env file with your values:**
   ```bash
   # Edit .env file with your actual values
   DJANGO_SECRET_KEY=your-generated-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DB_NAME=gestion_heures
   DB_USER=your_db_user
   DB_PASSWORD=your_secure_password
   ```

### 2. Database Setup

#### Option A: PostgreSQL (Recommended)

1. **Install PostgreSQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql postgresql-server
   sudo postgresql-setup initdb
   sudo systemctl start postgresql
   ```

2. **Create database and user:**
   ```sql
   sudo -u postgres psql
   CREATE DATABASE gestion_heures;
   CREATE USER your_app_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE gestion_heures TO your_app_user;
   ALTER USER your_app_user CREATEDB;
   \q
   ```

#### Option B: SQLite (Development only)

⚠️ **Warning:** SQLite is not recommended for production use.

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Security Tests

```bash
# Test your security configuration
python security_test.py
```

## 🔒 Security Configuration

### 1. File Upload Security

The application now includes:
- ✅ File type validation (MIME type checking)
- ✅ File size limits (10MB max)
- ✅ Filename sanitization
- ✅ Path traversal protection

### 2. Authentication Security

- ✅ Strong password validation (12+ characters)
- ✅ Session security (1-hour timeout)
- ✅ CSRF protection
- ✅ Secure cookies (HTTPS only)

### 3. HTTPS Configuration

- ✅ SSL redirect enabled
- ✅ HSTS headers
- ✅ Secure cookie settings
- ✅ Security headers

## 🚀 Deployment Options

### Option 1: Traditional VPS/Server

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx redis-server

# Install Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

#### 2. Application Setup

```bash
# Clone your application
git clone your-repository-url
cd your-project

# Set up environment
cp env.example .env
# Edit .env with your values

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
export DJANGO_SETTINGS_MODULE=gestion_heures.settings_production
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

#### 3. Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Test Gunicorn
gunicorn --config gunicorn.conf.py gestion_heures.wsgi:application

# Create systemd service
sudo nano /etc/systemd/system/gestion_heures.service
```

Add this content:
```ini
[Unit]
Description=Gestion Heures Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=gestion_heures.settings_production"
ExecStart=/path/to/your/project/venv/bin/gunicorn --config gunicorn.conf.py gestion_heures.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

#### 4. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/gestion_heures
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration (will be added by Certbot)
    # ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### 5. Enable Services

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/gestion_heures /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable Gunicorn service
sudo systemctl daemon-reload
sudo systemctl enable gestion_heures
sudo systemctl start gestion_heures

# Enable Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### 6. SSL Certificate

```bash
# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=gestion_heures.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create user
RUN useradd -m -u 1000 django
RUN chown -R django:django /app
USER django

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "gestion_heures.wsgi:application"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=gestion_heures.settings_production
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis
    volumes:
      - ./media:/app/media
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=gestion_heures
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
      - ./ssl:/etc/ssl/certs
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
```

### Option 3: Cloud Platforms

#### Heroku

1. **Create Procfile:**
   ```
   web: gunicorn --config gunicorn.conf.py gestion_heures.wsgi:application
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set DJANGO_SETTINGS_MODULE=gestion_heures.settings_production
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   git push heroku main
   ```

#### DigitalOcean App Platform

1. **Create app.yaml:**
   ```yaml
   name: gestion-heures
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/your-repo
       branch: main
     run_command: gunicorn --config gunicorn.conf.py gestion_heures.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
   ```

## 🔍 Post-Deployment Verification

### 1. Security Tests

```bash
# Run security test script
python security_test.py

# Check for common vulnerabilities
pip install safety
safety check
```

### 2. Performance Tests

```bash
# Test application response
curl -I https://yourdomain.com

# Check SSL configuration
curl -I https://yourdomain.com -H "Host: yourdomain.com"
```

### 3. Monitoring Setup

```bash
# Check application logs
sudo journalctl -u gestion_heures -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor system resources
htop
df -h
```

## 🛡️ Security Maintenance

### Daily Tasks
- [ ] Check application logs for errors
- [ ] Monitor failed login attempts
- [ ] Verify services are running

### Weekly Tasks
- [ ] Review security logs
- [ ] Check for system updates
- [ ] Verify backup integrity

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review security configurations
- [ ] Test disaster recovery

## 🚨 Emergency Procedures

### If the application is compromised:

1. **Immediate Actions:**
   ```bash
   # Stop the application
   sudo systemctl stop gestion_heures
   
   # Block suspicious IPs
   sudo ufw deny from suspicious_ip
   
   # Check logs for intrusion
   sudo grep "Failed password" /var/log/auth.log
   ```

2. **Investigation:**
   ```bash
   # Check for unauthorized files
   find /path/to/your/project -type f -mtime -1
   
   # Check for suspicious processes
   ps aux | grep -i suspicious
   
   # Check network connections
   netstat -tulpn
   ```

3. **Recovery:**
   ```bash
   # Restore from backup
   pg_restore -h localhost -U your_user -d your_database backup_file.sql
   
   # Restart with clean environment
   sudo systemctl start gestion_heures
   ```

## 📞 Support

If you encounter issues during deployment:

1. Check the logs: `sudo journalctl -u gestion_heures -f`
2. Verify configuration: `python security_test.py`
3. Test database connection: `python manage.py dbshell`
4. Check file permissions: `ls -la /path/to/your/project`

## 🔗 Useful Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/) 