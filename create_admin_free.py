#!/usr/bin/env python3
"""
Free Admin Creation - No Shell, No Upgrade Needed
Multiple solutions to create admin user without using Render shell.
"""

import os
import sys
from pathlib import Path

def print_free_solutions():
    """Print free solutions for admin creation"""
    
    print("=" * 60)
    print("🔑 FREE Admin Creation Solutions")
    print("=" * 60)
    
    print("\n🚫 Problem: Shell not available on free tier")
    print("✅ Solution: Use these FREE alternatives")
    
    print("\n" + "=" * 50)
    print("🎯 SOLUTION 1: Environment Variable Method")
    print("=" * 50)
    
    print("\n1️⃣ Go to Render Dashboard:")
    print("   https://dashboard.render.com")
    print("   → Find your 'gestion-heuressupp-app' service")
    
    print("\n2️⃣ Go to Environment Variables:")
    print("   → Click your service")
    print("   → Go to 'Environment' tab")
    print("   → Click 'Add Environment Variable'")
    
    print("\n3️⃣ Add these variables:")
    print("   🔑 DJANGO_SUPERUSER_USERNAME")
    print("   Value: admin")
    print("")
    print("   🔑 DJANGO_SUPERUSER_EMAIL")
    print("   Value: admin@example.com")
    print("")
    print("   🔑 DJANGO_SUPERUSER_PASSWORD")
    print("   Value: Admin123!@#")
    
    print("\n4️⃣ Update Build Command:")
    print("   Go to 'Settings' tab")
    print("   Update Build Command to:")
    print("   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py createsuperuser --noinput")
    
    print("\n5️⃣ Redeploy:")
    print("   → Save changes")
    print("   → App will redeploy automatically")
    print("   → Admin user will be created during build")
    
    print("\n" + "=" * 50)
    print("🎯 SOLUTION 2: Database Direct Method")
    print("=" * 50)
    
    print("\n1️⃣ Use Neon Database Console:")
    print("   → Go to https://console.neon.tech")
    print("   → Find your database")
    print("   → Click 'Query Editor'")
    
    print("\n2️⃣ Run this SQL:")
    print("   INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, date_joined) VALUES ('admin', '', '', 'admin@example.com', 'pbkdf2_sha256$600000$your_hash_here', true, true, true, NOW());")
    
    print("\n3️⃣ Generate password hash:")
    print("   → Use Django's password hasher")
    print("   → Or use the environment variable method above")

def print_alternative_solutions():
    """Print alternative solutions"""
    
    print("\n" + "=" * 50)
    print("🎯 SOLUTION 3: Temporary Upgrade (5 minutes)")
    print("=" * 50)
    
    print("\n1️⃣ Temporarily upgrade to Starter ($7/month):")
    print("   → Go to Render Dashboard")
    print("   → Click 'Upgrade' on your service")
    print("   → Choose 'Starter' plan")
    
    print("\n2️⃣ Create admin user:")
    print("   → Use shell access")
    print("   → Run: python manage.py createsuperuser")
    
    print("\n3️⃣ Downgrade back to free:")
    print("   → Immediately downgrade after creating user")
    print("   → You'll only pay for a few minutes")
    print("   → Cost: ~$0.01")
    
    print("\n" + "=" * 50)
    print("🎯 SOLUTION 4: Local Development Method")
    print("=" * 50)
    
    print("\n1️⃣ Connect local Django to production database:")
    print("   → Set DATABASE_URL in local .env")
    print("   → Run: python manage.py createsuperuser")
    print("   → User will be created in production database")

def print_login_info():
    """Print login information"""
    
    print("\n" + "=" * 50)
    print("🔑 Login Information")
    print("=" * 50)
    
    print("\n📍 Your App URLs:")
    print("   Main App: https://gestion-heuressupp-app.onrender.com/")
    print("   Admin Panel: https://gestion-heuressupp-app.onrender.com/admin/")
    print("   Login Page: https://gestion-heuressupp-app.onrender.com/accounts/login/")
    
    print("\n👤 Admin Credentials (after creation):")
    print("   Username: admin")
    print("   Password: Admin123!@#")
    print("   Email: admin@example.com")

def main():
    """Main function"""
    
    print("🔑 Free Admin Creation Guide")
    print("=" * 40)
    
    # Print solutions
    print_free_solutions()
    print_alternative_solutions()
    print_login_info()
    
    print("\n" + "=" * 60)
    print("💡 Recommendation:")
    print("   → Try SOLUTION 1 first (Environment Variables)")
    print("   → It's completely free and automatic")
    print("   → No shell access needed")
    print("   → No upgrades required")
    print("=" * 60)

if __name__ == "__main__":
    main() 