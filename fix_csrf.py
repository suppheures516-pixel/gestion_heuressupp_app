#!/usr/bin/env python3
"""
CSRF Fix Script for Gestion Heures Django App
This script helps fix CSRF verification issues in production.
"""

import os
import sys
from pathlib import Path

def print_csrf_fix_instructions():
    """Print instructions to fix CSRF issues"""
    
    print("=" * 60)
    print("🔧 CSRF Fix Instructions for Your Deployed App")
    print("=" * 60)
    
    print("\n📍 Your app URL: gestion-heuressupp-app.onrender.com")
    
    print("\n🚨 CSRF Error Fix Steps:")
    print("\n1️⃣ Go to Render Dashboard:")
    print("   https://dashboard.render.com")
    print("   → Find your 'gestion-heuressupp-app' service")
    
    print("\n2️⃣ Go to Environment Variables:")
    print("   → Click on your service")
    print("   → Go to 'Environment' tab")
    print("   → Click 'Edit' or 'Add Environment Variable'")
    
    print("\n3️⃣ Update/Add these variables:")
    print("\n   🔑 CSRF_TRUSTED_ORIGINS")
    print("   Value: https://gestion-heuressupp-app.onrender.com")
    
    print("\n   🔑 ALLOWED_HOSTS") 
    print("   Value: gestion-heuressupp-app.onrender.com")
    
    print("\n   🔑 DEBUG (temporarily)")
    print("   Value: True")
    print("   ⚠️  Remember to set back to False after fixing!")
    
    print("\n4️⃣ Save and redeploy:")
    print("   → Click 'Save Changes'")
    print("   → Your app will automatically redeploy")
    print("   → Wait 2-3 minutes for deployment")
    
    print("\n5️⃣ Test the fix:")
    print("   → Go to: https://gestion-heuressupp-app.onrender.com/admin/")
    print("   → Try logging in")
    
    print("\n6️⃣ If it works, secure it:")
    print("   → Set DEBUG back to False")
    print("   → Redeploy again")
    
    print("\n🔍 Alternative: Check your actual URL")
    print("If your URL is different, replace 'gestion-heuressupp-app.onrender.com'")
    print("with your actual domain in the CSRF_TRUSTED_ORIGINS setting.")

def check_current_settings():
    """Check current settings configuration"""
    
    print("\n📋 Current Configuration Check:")
    
    # Check if settings_production.py exists
    settings_file = Path("gestion_heures/settings_production.py")
    if settings_file.exists():
        print("✅ Production settings file exists")
        
        # Read CSRF settings
        with open(settings_file, 'r') as f:
            content = f.read()
            
        if 'CSRF_TRUSTED_ORIGINS' in content:
            print("✅ CSRF_TRUSTED_ORIGINS is configured")
        else:
            print("❌ CSRF_TRUSTED_ORIGINS not found in settings")
            
    else:
        print("❌ Production settings file not found")

def main():
    """Main function"""
    
    print("🔍 CSRF Fix Tool for Gestion Heures")
    print("=" * 40)
    
    # Check current settings
    check_current_settings()
    
    # Print fix instructions
    print_csrf_fix_instructions()
    
    print("\n" + "=" * 60)
    print("💡 Need more help? Check the logs in Render dashboard")
    print("   → Go to your service → Logs tab")
    print("   → Look for CSRF-related error messages")
    print("=" * 60)

if __name__ == "__main__":
    main() 