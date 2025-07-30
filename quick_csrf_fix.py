#!/usr/bin/env python3
"""
Quick CSRF Fix - Simplified Version
"""

import os
import sys
from pathlib import Path

def print_quick_fix():
    """Print quick fix instructions"""
    
    print("=" * 60)
    print("🔧 Quick CSRF Fix - Simplified")
    print("=" * 60)
    
    print("\n✅ Changes made:")
    print("   - Simplified CSRF_TRUSTED_ORIGINS (no complex logic)")
    print("   - Added temporary CSRF settings for debugging")
    print("   - Disabled secure cookies temporarily")
    
    print("\n🚀 Deploy now:")
    print("   git add gestion_heures/settings_production.py")
    print("   git commit -m 'Simplify CSRF configuration'")
    print("   git push")
    
    print("\n⏱️ Wait 3-5 minutes for deployment")
    print("\n🧪 Test login:")
    print("   URL: https://gestion-heuressupp-app.onrender.com/")
    print("   Username: admin")
    print("   Password: Admin123!@#")
    
    print("\n💡 If it works, we can secure it later")
    print("   For now, the goal is to get you logged in!")

def main():
    """Main function"""
    
    print("🔧 Quick CSRF Fix")
    print("=" * 40)
    print_quick_fix()
    
    print("\n" + "=" * 60)
    print("🎯 This should work!")
    print("=" * 60)

if __name__ == "__main__":
    main() 