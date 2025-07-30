#!/usr/bin/env python3
"""
Admin User Creation Script for Gestion Heures Django App
This script helps create admin users and provides login instructions.
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    # Add the project directory to Python path
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings_production')
    
    # Setup Django
    django.setup()

def create_admin_user():
    """Create admin user interactively"""
    from django.contrib.auth.models import User
    
    print("=" * 60)
    print("🔑 Create Admin User")
    print("=" * 60)
    
    print("\n📝 Enter admin credentials:")
    
    # Get username
    while True:
        username = input("Username (e.g., admin): ").strip()
        if username:
            if User.objects.filter(username=username).exists():
                print("❌ Username already exists. Try another one.")
                continue
            break
        print("❌ Username cannot be empty.")
    
    # Get email
    email = input("Email (optional): ").strip()
    
    # Get password
    while True:
        password = input("Password: ")
        if len(password) >= 8:
            break
        print("❌ Password must be at least 8 characters long.")
    
    # Confirm password
    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("❌ Passwords don't match!")
        return False
    
    try:
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print(f"\n✅ Admin user '{username}' created successfully!")
        print(f"🔗 Login URL: https://gestion-heuressupp-app.onrender.com/admin/")
        print(f"👤 Username: {username}")
        print(f"🔒 Password: {'*' * len(password)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def print_login_instructions():
    """Print login instructions"""
    
    print("\n" + "=" * 60)
    print("🚀 Login Instructions")
    print("=" * 60)
    
    print("\n1️⃣ Go to your admin panel:")
    print("   https://gestion-heuressupp-app.onrender.com/admin/")
    
    print("\n2️⃣ Enter your credentials:")
    print("   - Username: (what you just created)")
    print("   - Password: (what you just entered)")
    
    print("\n3️⃣ If you get CSRF error:")
    print("   → Check the CSRF fix instructions")
    print("   → Make sure CSRF_TRUSTED_ORIGINS is set correctly")
    
    print("\n4️⃣ Alternative login URLs:")
    print("   - Main app: https://gestion-heuressupp-app.onrender.com/")
    print("   - Admin: https://gestion-heuressupp-app.onrender.com/admin/")
    print("   - Login: https://gestion-heuressupp-app.onrender.com/accounts/login/")

def main():
    """Main function"""
    
    print("🔑 Admin User Creation Tool")
    print("=" * 40)
    
    try:
        # Setup Django
        setup_django()
        
        # Create admin user
        success = create_admin_user()
        
        if success:
            # Print login instructions
            print_login_instructions()
        else:
            print("\n❌ Failed to create admin user.")
            print("💡 Try using Render shell instead:")
            print("   → Go to Render Dashboard → Your Service → Shell")
            print("   → Run: python manage.py createsuperuser")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Alternative: Use Render Shell")
        print("1. Go to https://dashboard.render.com")
        print("2. Find your service")
        print("3. Go to 'Shell' tab")
        print("4. Run: python manage.py createsuperuser")

if __name__ == "__main__":
    main() 