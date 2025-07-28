# 🔒 Security Upgrade - Django Gestion Heures

## Overview

This Django application has been upgraded with comprehensive security measures for production deployment. All critical security vulnerabilities have been addressed.

## 🚨 Critical Security Fixes Applied

### 1. **Environment Variables & Secrets**
- ✅ Removed hardcoded SECRET_KEY from settings
- ✅ Added environment variable support
- ✅ Created `.env` template for secure configuration

### 2. **Production Settings**
- ✅ Created `settings_production.py` with security configurations
- ✅ Disabled DEBUG mode for production
- ✅ Configured proper ALLOWED_HOSTS
- ✅ Enabled HTTPS enforcement
- ✅ Added security headers (HSTS, XSS protection, etc.)

### 3. **File Upload Security**
- ✅ MIME type validation for Excel files
- ✅ File size limits (10MB max)
- ✅ Filename sanitization
- ✅ Path traversal protection
- ✅ Excel file structure validation

### 4. **Authentication & Session Security**
- ✅ Strong password validation (12+ characters)
- ✅ Session timeout (1 hour)
- ✅ Secure cookies (HTTPS only)
- ✅ CSRF protection
- ✅ Account lockout protection

## 📁 New Files Created

### Security Configuration
- `settings_production.py` - Production settings with security
- `validators.py` - Secure file upload validation
- `requirements.txt` - Updated with security packages

### Deployment & Setup
- `env.example` - Environment variables template
- `gunicorn.conf.py` - Production server configuration
- `deploy.sh` - Automated deployment script (Linux)
- `setup_windows.bat` - Windows setup script
- `install_dependencies.py` - Dependency installation helper

### Documentation
- `SECURITY_CHECKLIST.md` - Comprehensive security checklist
- `DEPLOYMENT_GUIDE.md` - Step-by-step deployment guide
- `security_test.py` - Security verification script

## 🚀 Quick Start

### For Development (Windows)

1. **Run the Windows setup script:**
   ```cmd
   setup_windows.bat
   ```

2. **Or manually install dependencies:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install Django pandas openpyxl xlrd
   ```

3. **Start the development server:**
   ```cmd
   python manage.py runserver
   ```

### For Production

1. **Copy environment template:**
   ```bash
   cp env.example .env
   ```

2. **Generate a new SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Update .env with your values**

4. **Run security tests:**
   ```bash
   python security_test.py
   ```

5. **Follow the deployment guide:**
   ```bash
   # See DEPLOYMENT_GUIDE.md for detailed instructions
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with these variables:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Settings
DB_NAME=gestion_heures
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Security Settings
SECURE_SSL_REDIRECT=True
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### Settings Files

- **Development:** `gestion_heures/settings.py` (current)
- **Production:** `gestion_heures/settings_production.py` (secure)

To use production settings:
```bash
export DJANGO_SETTINGS_MODULE=gestion_heures.settings_production
python manage.py runserver
```

## 🛡️ Security Features

### File Upload Protection
- Only Excel files (.xlsx, .xls) allowed
- Maximum file size: 10MB
- MIME type validation (if python-magic installed)
- Filename sanitization
- Path traversal protection

### Authentication Security
- Minimum password length: 12 characters
- Session timeout: 1 hour
- Secure cookies (HTTPS only)
- CSRF protection enabled
- Account lockout protection

### HTTPS & SSL
- SSL redirect enforcement
- HSTS headers (1 year)
- Secure cookie settings
- Security headers (X-Frame-Options, XSS protection, etc.)

## 🧪 Testing Security

### Run Security Tests
```bash
python security_test.py
```

This will check:
- ✅ DEBUG mode is disabled
- ✅ SECRET_KEY is customized
- ✅ ALLOWED_HOSTS is configured
- ✅ SSL redirect is enabled
- ✅ Secure cookies are configured
- ✅ Security headers are set
- ✅ CSRF protection is enabled

### Manual Security Checks
```bash
# Check for common vulnerabilities
pip install safety
safety check

# Test file upload security
# Try uploading non-Excel files
# Try uploading files larger than 10MB
# Try uploading files with malicious names
```

## 📊 Security Monitoring

### Logs to Monitor
- Application logs: `logs/django.log`
- Nginx access logs: `/var/log/nginx/access.log`
- Nginx error logs: `/var/log/nginx/error.log`
- System logs: `sudo journalctl -u gestion_heures`

### Security Events to Watch
- Failed login attempts
- File upload errors
- CSRF token failures
- SSL/TLS errors
- Database connection issues

## 🚨 Emergency Procedures

### If Compromised
1. **Stop the application:**
   ```bash
   sudo systemctl stop gestion_heures
   ```

2. **Check for unauthorized access:**
   ```bash
   sudo grep "Failed password" /var/log/auth.log
   find /path/to/project -type f -mtime -1
   ```

3. **Restore from backup:**
   ```bash
   pg_restore -h localhost -U your_user -d your_database backup_file.sql
   ```

4. **Restart with clean environment:**
   ```bash
   sudo systemctl start gestion_heures
   ```

## 📋 Maintenance Checklist

### Daily
- [ ] Check application logs for errors
- [ ] Monitor failed login attempts
- [ ] Verify services are running

### Weekly
- [ ] Review security logs
- [ ] Check for system updates
- [ ] Verify backup integrity

### Monthly
- [ ] Update dependencies
- [ ] Review security configurations
- [ ] Test disaster recovery

## 🔗 Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/)

## ⚠️ Important Notes

1. **NEVER use development settings in production**
2. **Always use HTTPS in production**
3. **Regularly update dependencies**
4. **Monitor logs for security events**
5. **Set up automated backups**
6. **Test security measures regularly**

## 🆘 Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u gestion_heures -f`
2. Verify configuration: `python security_test.py`
3. Test database connection: `python manage.py dbshell`
4. Check file permissions: `ls -la /path/to/your/project`

Your application is now significantly more secure and ready for production deployment! 🎉 