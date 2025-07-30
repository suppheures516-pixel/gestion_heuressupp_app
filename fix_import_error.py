#!/usr/bin/env python3
"""
Fix Import Error - Missing config import
"""

import os
import sys
from pathlib import Path

def print_import_fix():
    """Print import fix instructions"""
    
    print("=" * 60)
    print("🔧 FIX IMPORT ERROR - Missing config import")
    print("=" * 60)
    
    print("\n🎯 FOUND THE BUILD ERROR!")
    print("   - 'config' function was not imported")
    print("   - Import was at the bottom of the file")
    print("   - But used at the top of the file")
    print("   - This caused a NameError during build")
    
    print("\n✅ What I fixed:")
    print("   - Moved 'from decouple import config' to the top")
    print("   - Removed duplicate import at the bottom")
    print("   - Now config() function is available everywhere")
    
    print("\n🚀 Deploy now:")
    print("   git add gestion_heures/gestion_heures/settings_production.py")
    print("   git commit -m 'Fix import error - move config import to top'")
    print("   git push")
    
    print("\n⏱️ Wait 3-5 minutes for deployment")
    print("\n🧪 Test after successful build:")
    print("   URL: https://gestion-heuressupp-app.onrender.com/")
    print("   Username: admin")
    print("   Password: Admin123!@#")
    
    print("\n💡 This will fix the build error:")
    print("   - No more NameError: name 'config' is not defined")
    print("   - Build should complete successfully")
    print("   - Then we can test the CSRF fix")

def main():
    """Main function"""
    
    print("🔧 Fix Import Error")
    print("=" * 40)
    print_import_fix()
    
    print("\n" + "=" * 60)
    print("🎯 Build error will be fixed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 