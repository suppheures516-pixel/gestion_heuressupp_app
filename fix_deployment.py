#!/usr/bin/env python3
"""
Deployment Fix Script for Gestion Heures Django App
This script helps fix deployment issues on Render.
"""

import os
import sys
from pathlib import Path

def print_deployment_fix():
    """Print deployment fix instructions"""
    
    print("=" * 60)
    print("🔧 Deployment Fix for Render")
    print("=" * 60)
    
    print("\n🚨 Issue: Build command failing")
    print("   The build command was looking for requirements.txt in wrong location")
    
    print("\n✅ Fixed render.yaml:")
    print("   - buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate")
    print("   - startCommand: gunicorn gestion_heures.wsgi:application --bind 0.0.0.0:$PORT")
    
    print("\n📋 Next Steps:")
    print("\n1️⃣ Commit the fixed render.yaml:")
    print("   git add render.yaml")
    print("   git commit -m 'Fix build command for Render deployment'")
    print("   git push")
    
    print("\n2️⃣ Or manually update in Render Dashboard:")
    print("   → Go to your service settings")
    print("   → Update Build Command to:")
    print("     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate")
    print("   → Update Start Command to:")
    print("     gunicorn gestion_heures.wsgi:application --bind 0.0.0.0:$PORT")
    
    print("\n3️⃣ Deploy again:")
    print("   → Render will automatically redeploy")
    print("   → Wait 3-5 minutes for build to complete")
    
    print("\n💡 About Free Tier Hours:")
    print("   ✅ 750 hours per month (not per deployment)")
    print("   ✅ Failed deployments don't count much")
    print("   ✅ Only running services consume hours")
    print("   ✅ You still have full 750 hours available")

def check_files():
    """Check if required files exist"""
    
    print("\n📋 File Check:")
    
    files_to_check = [
        "requirements.txt",
        "manage.py", 
        "gestion_heures/wsgi.py",
        "render.yaml"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING!")

def main():
    """Main function"""
    
    print("🔍 Deployment Fix Tool")
    print("=" * 40)
    
    # Check files
    check_files()
    
    # Print fix instructions
    print_deployment_fix()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("   - Your 750 hours are safe (not divided)")
    print("   - Build command was the issue")
    print("   - Fixed render.yaml should resolve it")
    print("=" * 60)

if __name__ == "__main__":
    main() 