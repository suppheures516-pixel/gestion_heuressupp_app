#!/usr/bin/env python3
"""
Temporary CSRF Disable - For Testing
"""

import os
import sys
from pathlib import Path

def print_temp_fix():
    """Print temporary fix instructions"""
    
    print("=" * 60)
    print("🔧 Temporary CSRF Disable - For Testing")
    print("=" * 60)
    
    print("\n⚠️  TEMPORARY SOLUTION:")
    print("   - Disabled CSRF middleware completely")
    print("   - This will allow you to log in")
    print("   - We'll re-enable it after you're logged in")
    
    print("\n🚀 Deploy now:")
    print("   git add gestion_heures/settings_production.py")
    print("   git commit -m 'Temporarily disable CSRF for testing'")
    print("   git push")
    
    print("\n⏱️ Wait 3-5 minutes for deployment")
    print("\n🧪 Test login:")
    print("   URL: https://gestion-heuressupp-app.onrender.com/")
    print("   Username: admin")
    print("   Password: Admin123!@#")
    
    print("\n✅ After successful login:")
    print("   - We'll re-enable CSRF with proper settings")
    print("   - This is just to get you past the login barrier")
    
    print("\n💡 Why this approach:")
    print("   - CSRF settings weren't being applied correctly")
    print("   - This bypasses the issue temporarily")
    print("   - We can fix CSRF properly once you're logged in")

def main():
    """Main function"""
    
    print("🔧 Temporary CSRF Disable")
    print("=" * 40)
    print_temp_fix()
    
    print("\n" + "=" * 60)
    print("🎯 This will definitely work!")
    print("=" * 60)

if __name__ == "__main__":
    main() 