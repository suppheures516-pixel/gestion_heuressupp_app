#!/usr/bin/env python3
"""
Build script for Gestion Heures Desktop Application.
This script prepares the Django app for desktop deployment with WhiteNoise.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_desktop_app():
    """Build the desktop application with WhiteNoise"""
    
    project_root = Path(__file__).resolve().parent
    
    print("=" * 60)
    print("🖥️  Building Gestion Heures Desktop Application")
    print("=" * 60)
    
    try:
        # Step 1: Install dependencies
        print("\n📦 Installing Python dependencies...")
        install_dependencies(project_root)
        
        # Step 2: Setup Django with desktop settings
        print("\n⚙️  Setting up Django with desktop settings...")
        setup_django_desktop(project_root)
        
        # Step 3: Collect static files with WhiteNoise
        print("\n📁 Collecting static files with WhiteNoise...")
        collect_static_files(project_root)
        
        # Step 4: Create launcher scripts
        print("\n🚀 Creating launcher scripts...")
        create_launcher_scripts(project_root)
        
        # Step 5: Create shortcuts
        print("\n🔗 Creating desktop shortcuts...")
        create_shortcuts(project_root)
        
        print("\n" + "=" * 60)
        print("✅ Desktop application built successfully!")
        print("📱 To run the app: python run_desktop.py")
        print("🔗 Or double-click the desktop shortcut")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error building desktop app: {e}")
        return False
    
    return True

def install_dependencies(project_root):
    """Install Python dependencies"""
    
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
    else:
        print("⚠️  requirements.txt not found, installing basic dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "Django>=5.1.7", "pandas>=2.1.0", "openpyxl>=3.1.2", "whitenoise>=6.6.0"
        ], check=True)

def setup_django_desktop(project_root):
    """Setup Django with desktop settings"""
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings_desktop')
    
    # Add project to Python path
    sys.path.insert(0, str(project_root))
    
    # Import Django and setup
    import django
    django.setup()
    
    # Run migrations
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Create superuser if none exists
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Created admin user: admin/admin123")

def collect_static_files(project_root):
    """Collect static files with WhiteNoise"""
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings_desktop')
    
    # Import Django and setup
    import django
    django.setup()
    
    # Collect static files
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("✅ Static files collected successfully!")

def create_launcher_scripts(project_root):
    """Create launcher scripts for different platforms"""
    
    # Windows batch file
    batch_file = project_root / "launch_desktop.bat"
    batch_content = f'''@echo off
title Gestion Heures Desktop App
echo Starting Gestion Heures Desktop Application...
cd /d "{project_root}"
python run_desktop.py
pause
'''
    batch_file.write_text(batch_content)
    
    # Windows PowerShell script
    ps_file = project_root / "launch_desktop.ps1"
    ps_content = f'''Write-Host "Starting Gestion Heures Desktop Application..." -ForegroundColor Green
Set-Location "{project_root}"
python run_desktop.py
'''
    ps_file.write_text(ps_content)
    
    # Linux/Mac shell script
    shell_file = project_root / "launch_desktop.sh"
    shell_content = f'''#!/bin/bash
echo "Starting Gestion Heures Desktop Application..."
cd "{project_root}"
python3 run_desktop.py
'''
    shell_file.write_text(shell_content)
    
    # Make shell script executable
    os.chmod(shell_file, 0o755)
    
    print("✅ Launcher scripts created successfully!")

def create_shortcuts(project_root):
    """Create desktop shortcuts"""
    
    try:
        # Try to create Windows shortcuts
        import winshell
        from win32com.client import Dispatch
        
        # Desktop shortcut
        desktop_path = Path.home() / "Desktop"
        shortcut_path = desktop_path / "Gestion Heures.lnk"
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{project_root / "run_desktop.py"}"'
        shortcut.WorkingDirectory = str(project_root)
        shortcut.IconLocation = sys.executable
        shortcut.Description = "Gestion Heures - Desktop Application"
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        
    except ImportError:
        print("⚠️  Windows shortcut creation skipped (pywin32 not installed)")
        print("   You can manually create shortcuts or use the launcher scripts")

def main():
    """Main function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Gestion Heures Desktop App Builder

Usage:
    python build_desktop.py          # Build the desktop app
    python build_desktop.py --help   # Show this help

This script will:
1. Install Python dependencies
2. Setup Django with desktop settings
3. Collect static files with WhiteNoise
4. Create launcher scripts
5. Create desktop shortcuts (Windows only)
        """)
        return
    
    success = build_desktop_app()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("🚀 Run 'python run_desktop.py' to start the application")
    else:
        print("\n❌ Build failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 