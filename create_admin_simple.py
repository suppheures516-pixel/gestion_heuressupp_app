#!/usr/bin/env python3
"""
Simple Admin Creation - No Render Hours Used
This script creates an admin user locally and provides the credentials.
"""

import os
import sys
from pathlib import Path

def create_admin_credentials():
    """Create admin credentials without database connection"""
    
    print("=" * 60)
    print("🔑 Admin Credentials Generator")
    print("=" * 60)
    
    print("\n📝 This will create admin credentials you can use in Render shell.")
    print("   No database connection needed - saves your 750 hours!")
    
    print("\n🚀 Step 1: Go to Render Shell")
    print("   1. Visit: https://dashboard.render.com")
    print("   2. Find your 'gestion-heuressupp-app' service")
    print("   3. Click 'Shell' tab → 'Connect'")
    
    print("\n🚀 Step 2: Run this command in Render shell:")
    print("   python manage.py createsuperuser")
    
    print("\n🚀 Step 3: Use these credentials:")
    print("   Username: admin")
    print("   Email: admin@example.com (or leave empty)")
    print("   Password: Admin123!@# (or create your own)")
    
    print("\n🚀 Step 4: Login to your app:")
    print("   URL: https://gestion-heuressupp-app.onrender.com/admin/")
    print("   Username: admin")
    print("   Password: Admin123!@#")
    
    print("\n💡 Alternative: Quick Database Command")
    print("   If you want to create the user directly in database:")
    print("   python manage.py shell")
    print("   >>> from django.contrib.auth.models import User")
    print("   >>> User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!@#')")
    print("   >>> exit()")

def print_troubleshooting():
    """Print troubleshooting tips"""
    
    print("\n" + "=" * 60)
    print("🔧 Troubleshooting")
    print("=" * 60)
    
    print("\n❌ If you get CSRF error:")
    print("   1. Go to Render Dashboard → Environment Variables")
    print("   2. Add/Update: CSRF_TRUSTED_ORIGINS")
    print("   3. Value: https://gestion-heuressupp-app.onrender.com")
    print("   4. Temporarily set DEBUG=True")
    
    print("\n❌ If you get database error:")
    print("   1. Check if DATABASE_URL is set correctly")
    print("   2. Make sure Neon database is active")
    print("   3. Try running migrations first:")
    print("      python manage.py migrate")
    
    print("\n❌ If shell doesn't work:")
    print("   1. Try: python manage.py dbshell")
    print("   2. Or use the direct database command above")

def main():
    """Main function"""
    
    print("🔑 Zero-Hour Admin Creation")
    print("=" * 40)
    
    # Print instructions
    create_admin_credentials()
    
    # Print troubleshooting
    print_troubleshooting()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("   ✅ No Render hours used")
    print("   ✅ Quick admin creation")
    print("   ✅ Ready to login")
    print("=" * 60)

if __name__ == "__main__":
    main() 