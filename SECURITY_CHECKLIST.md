# 🔒 Security Checklist for Production Deployment

## Pre-Deployment Security

### ✅ Environment Variables
- [ ] Generate a new SECRET_KEY (never use the development one)
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS with your actual domain(s)
- [ ] Set up database credentials securely
- [ ] Configure email settings for notifications

### ✅ Database Security
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable SSL connections to database
- [ ] Use strong database passwords
- [ ] Limit database user permissions
- [ ] Enable database logging

### ✅ File Upload Security
- [ ] Validate file types (MIME type checking)
- [ ] Limit file sizes (10MB max)
- [ ] Sanitize filenames
- [ ] Store files outside web root
- [ ] Set proper file permissions

## Server Security

### ✅ System Updates
- [ ] Update all system packages
- [ ] Enable automatic security updates
- [ ] Configure firewall (UFW)
- [ ] Disable unnecessary services

### ✅ SSL/TLS Configuration
- [ ] Install SSL certificates (Let's Encrypt recommended)
- [ ] Configure HTTPS redirect
- [ ] Enable HSTS headers
- [ ] Use strong SSL ciphers
- [ ] Disable SSLv3 and TLS 1.0/1.1

### ✅ Web Server Security (Nginx)
- [ ] Hide server version
- [ ] Configure security headers
- [ ] Set up rate limiting
- [ ] Enable gzip compression
- [ ] Configure proper file permissions

## Application Security

### ✅ Django Security Settings
- [ ] Use production settings file
- [ ] Enable CSRF protection
- [ ] Configure secure cookies
- [ ] Set up session security
- [ ] Enable XSS protection

### ✅ Authentication & Authorization
- [ ] Use strong password policies
- [ ] Enable account lockout
- [ ] Implement rate limiting on login
- [ ] Use HTTPS for all authentication
- [ ] Set up proper user permissions

### ✅ Monitoring & Logging
- [ ] Set up application logging
- [ ] Configure error monitoring (Sentry)
- [ ] Monitor failed login attempts
- [ ] Set up log rotation
- [ ] Configure admin email notifications

## Post-Deployment Security

### ✅ Regular Maintenance
- [ ] Set up automated backups
- [ ] Monitor security updates
- [ ] Review access logs regularly
- [ ] Test backup restoration
- [ ] Update dependencies regularly

### ✅ Security Testing
- [ ] Run security scans
- [ ] Test file upload security
- [ ] Verify HTTPS configuration
- [ ] Check for common vulnerabilities
- [ ] Test authentication flows

## Emergency Procedures

### ✅ Incident Response
- [ ] Document security incident procedures
- [ ] Set up monitoring alerts
- [ ] Have backup contact information
- [ ] Plan for data breach response
- [ ] Document rollback procedures

## Security Headers Checklist

Ensure these headers are configured in Nginx:

```nginx
# Security Headers
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

## File Permissions

```bash
# Set proper file permissions
sudo chown -R www-data:www-data /path/to/your/project
sudo chmod -R 755 /path/to/your/project
sudo chmod 600 /path/to/your/project/.env
sudo chmod 644 /path/to/your/project/staticfiles/*
```

## Database Security Commands

```sql
-- Create secure database user
CREATE USER your_app_user WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE your_database TO your_app_user;
GRANT USAGE ON SCHEMA public TO your_app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL';
```

## Monitoring Commands

```bash
# Check application status
sudo systemctl status gestion_heures

# View application logs
sudo journalctl -u gestion_heures -f

# Check Nginx status
sudo nginx -t && sudo systemctl status nginx

# Monitor system resources
htop
df -h
free -h

# Check for failed login attempts
sudo grep "Failed password" /var/log/auth.log

# Monitor file uploads
sudo tail -f /path/to/your/project/logs/django.log
```

## Backup Commands

```bash
# Database backup
pg_dump -h localhost -U your_user your_database > backup_$(date +%Y%m%d_%H%M%S).sql

# File backup
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz /path/to/your/project/uploads/

# Full project backup
tar -czf project_backup_$(date +%Y%m%d_%H%M%S).tar.gz /path/to/your/project/ --exclude=venv --exclude=*.pyc
```

## Security Tools

Consider installing these security tools:

- **Fail2ban**: Protect against brute force attacks
- **ClamAV**: Antivirus scanning for uploads
- **ModSecurity**: Web application firewall
- **Lynis**: Security auditing tool
- **Rkhunter**: Rootkit detection

## Regular Security Tasks

### Daily
- [ ] Check application logs for errors
- [ ] Monitor failed login attempts
- [ ] Verify services are running

### Weekly
- [ ] Review security logs
- [ ] Check for system updates
- [ ] Verify backup integrity
- [ ] Review user access

### Monthly
- [ ] Update dependencies
- [ ] Review security configurations
- [ ] Test disaster recovery
- [ ] Update SSL certificates

### Quarterly
- [ ] Security audit
- [ ] Penetration testing
- [ ] Review access controls
- [ ] Update security policies 