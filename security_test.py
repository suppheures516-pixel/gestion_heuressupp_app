#!/usr/bin/env python3
"""
Security Test Script for Django Gestion Heures
Run this script to verify your security configuration
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings_production')
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line
from django.test import TestCase, Client
from django.urls import reverse
import requests
import json

class SecurityTest:
    def __init__(self):
        self.client = Client()
        self.failures = []
        self.warnings = []
        
    def test_debug_mode(self):
        """Test that DEBUG is False in production"""
        if settings.DEBUG:
            self.failures.append("❌ DEBUG is True - this is a security risk!")
        else:
            print("✅ DEBUG is False")
    
    def test_secret_key(self):
        """Test that SECRET_KEY is not the default"""
        default_key = "django-insecure-w9nq60lx+7vw_!stp(fn+3ci&onmp+tq02!3841(-bsl&2av_1"
        if settings.SECRET_KEY == default_key:
            self.failures.append("❌ SECRET_KEY is still the default - change this immediately!")
        else:
            print("✅ SECRET_KEY is customized")
    
    def test_allowed_hosts(self):
        """Test ALLOWED_HOSTS configuration"""
        if '*' in settings.ALLOWED_HOSTS:
            self.failures.append("❌ ALLOWED_HOSTS contains '*' - this is a security risk!")
        elif len(settings.ALLOWED_HOSTS) == 0:
            self.failures.append("❌ ALLOWED_HOSTS is empty")
        else:
            print("✅ ALLOWED_HOSTS is properly configured")
    
    def test_ssl_redirect(self):
        """Test SSL redirect settings"""
        if not settings.SECURE_SSL_REDIRECT:
            self.warnings.append("⚠️ SECURE_SSL_REDIRECT is False - consider enabling for production")
        else:
            print("✅ SECURE_SSL_REDIRECT is enabled")
    
    def test_secure_cookies(self):
        """Test secure cookie settings"""
        if not settings.SESSION_COOKIE_SECURE:
            self.failures.append("❌ SESSION_COOKIE_SECURE is False")
        else:
            print("✅ SESSION_COOKIE_SECURE is enabled")
        
        if not settings.CSRF_COOKIE_SECURE:
            self.failures.append("❌ CSRF_COOKIE_SECURE is False")
        else:
            print("✅ CSRF_COOKIE_SECURE is enabled")
    
    def test_security_headers(self):
        """Test security header settings"""
        if not settings.SECURE_BROWSER_XSS_FILTER:
            self.warnings.append("⚠️ SECURE_BROWSER_XSS_FILTER is False")
        else:
            print("✅ SECURE_BROWSER_XSS_FILTER is enabled")
        
        if not settings.SECURE_CONTENT_TYPE_NOSNIFF:
            self.warnings.append("⚠️ SECURE_CONTENT_TYPE_NOSNIFF is False")
        else:
            print("✅ SECURE_CONTENT_TYPE_NOSNIFF is enabled")
    
    def test_hsts_settings(self):
        """Test HSTS settings"""
        if not hasattr(settings, 'SECURE_HSTS_SECONDS') or settings.SECURE_HSTS_SECONDS == 0:
            self.warnings.append("⚠️ HSTS is not configured")
        else:
            print("✅ HSTS is configured")
    
    def test_xframe_options(self):
        """Test X-Frame-Options"""
        if settings.X_FRAME_OPTIONS != 'DENY':
            self.warnings.append("⚠️ X_FRAME_OPTIONS is not set to 'DENY'")
        else:
            print("✅ X_FRAME_OPTIONS is set to 'DENY'")
    
    def test_password_validators(self):
        """Test password validation settings"""
        if len(settings.AUTH_PASSWORD_VALIDATORS) < 3:
            self.warnings.append("⚠️ Password validators seem insufficient")
        else:
            print("✅ Password validators are configured")
    
    def test_database_ssl(self):
        """Test database SSL configuration"""
        db_config = settings.DATABASES.get('default', {})
        if 'OPTIONS' in db_config and 'sslmode' in db_config['OPTIONS']:
            print("✅ Database SSL is configured")
        else:
            self.warnings.append("⚠️ Database SSL is not configured")
    
    def test_file_upload_settings(self):
        """Test file upload security settings"""
        if hasattr(settings, 'MAX_UPLOAD_SIZE'):
            print(f"✅ MAX_UPLOAD_SIZE is set to {settings.MAX_UPLOAD_SIZE}")
        else:
            self.warnings.append("⚠️ MAX_UPLOAD_SIZE is not configured")
        
        if hasattr(settings, 'ALLOWED_EXCEL_EXTENSIONS'):
            print(f"✅ ALLOWED_EXCEL_EXTENSIONS is configured: {settings.ALLOWED_EXCEL_EXTENSIONS}")
        else:
            self.warnings.append("⚠️ ALLOWED_EXCEL_EXTENSIONS is not configured")
    
    def test_logging_configuration(self):
        """Test logging configuration"""
        if hasattr(settings, 'LOGGING') and settings.LOGGING:
            print("✅ Logging is configured")
        else:
            self.warnings.append("⚠️ Logging is not configured")
    
    def test_csrf_protection(self):
        """Test CSRF protection"""
        if 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE:
            print("✅ CSRF middleware is enabled")
        else:
            self.failures.append("❌ CSRF middleware is not enabled")
    
    def test_session_security(self):
        """Test session security settings"""
        if settings.SESSION_COOKIE_HTTPONLY:
            print("✅ SESSION_COOKIE_HTTPONLY is enabled")
        else:
            self.warnings.append("⚠️ SESSION_COOKIE_HTTPONLY is not enabled")
        
        if hasattr(settings, 'SESSION_COOKIE_SAMESITE'):
            print(f"✅ SESSION_COOKIE_SAMESITE is set to {settings.SESSION_COOKIE_SAMESITE}")
        else:
            self.warnings.append("⚠️ SESSION_COOKIE_SAMESITE is not configured")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔒 Running Security Tests...\n")
        
        tests = [
            self.test_debug_mode,
            self.test_secret_key,
            self.test_allowed_hosts,
            self.test_ssl_redirect,
            self.test_secure_cookies,
            self.test_security_headers,
            self.test_hsts_settings,
            self.test_xframe_options,
            self.test_password_validators,
            self.test_database_ssl,
            self.test_file_upload_settings,
            self.test_logging_configuration,
            self.test_csrf_protection,
            self.test_session_security,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.failures.append(f"❌ Test {test.__name__} failed: {str(e)}")
        
        # Print results
        print("\n" + "="*50)
        print("SECURITY TEST RESULTS")
        print("="*50)
        
        if self.failures:
            print(f"\n❌ FAILURES ({len(self.failures)}):")
            for failure in self.failures:
                print(f"  {failure}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.failures and not self.warnings:
            print("\n🎉 All security tests passed!")
        
        print(f"\n📊 Summary: {len(self.failures)} failures, {len(self.warnings)} warnings")
        
        if self.failures:
            print("\n🚨 CRITICAL: Fix all failures before deploying to production!")
            return False
        elif self.warnings:
            print("\n⚠️ Consider addressing warnings for better security")
            return True
        else:
            print("\n✅ Your application is ready for production deployment!")
            return True

def main():
    """Main function"""
    print("🔒 Django Gestion Heures Security Test")
    print("="*40)
    
    # Check if we're using production settings
    if 'settings_production' not in os.environ.get('DJANGO_SETTINGS_MODULE', ''):
        print("⚠️ Warning: Not using production settings")
        print("Set DJANGO_SETTINGS_MODULE=gestion_heures.settings_production")
        print()
    
    # Run security tests
    security_test = SecurityTest()
    success = security_test.run_all_tests()
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main() 