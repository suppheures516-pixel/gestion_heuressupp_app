#!/usr/bin/env python3
"""
Dependency Installation Script for Django Gestion Heures
This script helps install required and optional dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_package(package, description, optional=False):
    """Install a Python package"""
    if optional:
        print(f"🔧 Installing optional package: {package}")
        response = input(f"Do you want to install {package}? (y/n): ").lower().strip()
        if response != 'y':
            print(f"⏭️ Skipping {package}")
            return True
    
    return run_command(f"{sys.executable} -m pip install {package}", f"Installing {description}")

def main():
    print("🚀 Django Gestion Heures - Dependency Installation")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️ Warning: You're not in a virtual environment!")
        response = input("Do you want to continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("Please activate a virtual environment first.")
            return
    
    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Required packages
    required_packages = [
        ("Django>=5.1.7,<5.2", "Django"),
        ("pandas>=2.1.0", "Pandas"),
        ("openpyxl>=3.1.2", "OpenPyXL"),
        ("xlrd>=2.0.1", "xlrd"),
    ]
    
    print("\n📋 Installing required packages...")
    for package, description in required_packages:
        if not install_package(package, description):
            print(f"❌ Failed to install {description}. Please check your internet connection.")
            return
    
    # Optional packages
    optional_packages = [
        ("python-magic>=0.4.27", "python-magic (enhanced file validation)", True),
        ("django-environ>=0.11.2", "django-environ (environment management)", True),
        ("django-cors-headers>=4.3.1", "django-cors-headers (CORS support)", True),
    ]
    
    print("\n🔧 Installing optional packages...")
    for package, description, optional in optional_packages:
        install_package(package, description, optional)
    
    # Development packages (optional)
    dev_packages = [
        ("django-debug-toolbar>=4.2.0", "django-debug-toolbar (development)", True),
        ("django-extensions>=3.2.3", "django-extensions (development tools)", True),
    ]
    
    print("\n🛠️ Installing development packages...")
    for package, description, optional in dev_packages:
        install_package(package, description, optional)
    
    print("\n✅ Dependency installation completed!")
    print("\n📋 Next steps:")
    print("1. Copy env.example to .env and configure your settings")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py collectstatic")
    print("4. Run: python manage.py createsuperuser")
    print("5. Test the application: python manage.py runserver")
    
    # Test if the application can start
    print("\n🧪 Testing application startup...")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings')
        django.setup()
        print("✅ Django application can start successfully!")
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        print("Please check your configuration.")

if __name__ == '__main__':
    main() 