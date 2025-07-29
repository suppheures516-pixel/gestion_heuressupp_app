#!/usr/bin/env python3
"""
Environment setup script for Gestion Heures Django application.
This script helps you create a .env file with the necessary environment variables.
"""

import os
import secrets
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key"""
    return secrets.token_urlsafe(50)

def create_env_file():
    """Create a .env file with default values"""
    
    project_root = Path(__file__).resolve().parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    # Create .env content
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# For development (SQLite):
DATABASE_URL=sqlite:///db.sqlite3

# For production (PostgreSQL):
# DATABASE_URL=postgresql://username:password@host:port/database_name

# For Railway:
# DATABASE_URL=postgresql://postgres:password@containers-us-west-1.railway.app:5432/railway

# For Render:
# DATABASE_URL=postgresql://user:password@host:5432/database

# Security Settings (for production)
SECURE_SSL_REDIRECT=False
CSRF_TRUSTED_ORIGINS=

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
MAX_UPLOAD_SIZE=10485760

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis Settings (optional)
REDIS_URL=redis://localhost:6379/1

# Admin Email
ADMIN_EMAIL=admin@yourdomain.com
"""
    
    # Write .env file
    env_file.write_text(env_content)
    
    print("✅ .env file created successfully!")
    print(f"📁 Location: {env_file}")
    print("\n📋 Next steps:")
    print("1. Edit the .env file to configure your settings")
    print("2. For production, set DEBUG=False")
    print("3. Configure your DATABASE_URL for your database")
    print("4. Set up email settings if needed")
    print("\n🚀 To run the app:")
    print("   python run_desktop.py")

def main():
    """Main function"""
    
    print("=" * 60)
    print("🔧 Gestion Heures Environment Setup")
    print("=" * 60)
    
    try:
        create_env_file()
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 