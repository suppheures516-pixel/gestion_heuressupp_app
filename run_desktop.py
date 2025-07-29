#!/usr/bin/env python3
"""
Desktop launcher for Gestion Heures Django application.
This script starts the Django server with desktop-optimized settings.
"""

import os
import sys
import django
import threading
import webbrowser
import time
from pathlib import Path

def setup_django():
    """Setup Django for desktop environment with WhiteNoise"""
    
    # Add the project directory to Python path
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    
    # Load environment variables from .env file
    from decouple import config
    from pathlib import Path
    
    # Set Django settings to desktop settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_heures.settings_desktop')
    
    # Setup Django
    django.setup()
    
    # Run migrations
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files with WhiteNoise
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Create superuser if none exists
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Created superuser: admin/admin123")
    
    print("✅ Django setup completed successfully!")

def run_django_server():
    """Run Django development server with desktop settings"""
    from django.core.management import execute_from_command_line
    print("🚀 Starting Django server with WhiteNoise...")
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)  # Wait for server to start
    print("🌐 Opening browser...")
    webbrowser.open('http://127.0.0.1:8000')

def create_directories():
    """Create necessary directories"""
    project_dir = Path(__file__).resolve().parent
    
    # Create uploads directory
    uploads_dir = project_dir / 'uploads'
    uploads_dir.mkdir(exist_ok=True)
    
    # Create logs directory
    logs_dir = project_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Create staticfiles directory
    staticfiles_dir = project_dir / 'staticfiles'
    staticfiles_dir.mkdir(exist_ok=True)
    
    print("✅ Directories created successfully!")

def main():
    """Main function to launch the desktop app"""
    
    print("=" * 50)
    print("🖥️  Gestion Heures Desktop Application")
    print("=" * 50)
    
    try:
        # Create necessary directories
        create_directories()
        
        # Setup Django
        setup_django()
        
        # Start Django server in a thread
        server_thread = threading.Thread(target=run_django_server, daemon=True)
        server_thread.start()
        
        # Open browser
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("\n" + "=" * 50)
        print("✅ Application started successfully!")
        print("📱 Access your app at: http://127.0.0.1:8000")
        print("🔑 Admin login: admin/admin123")
        print("⏹️  Press Ctrl+C to stop the application")
        print("=" * 50)
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Gestion Heures Desktop App...")
            print("👋 Goodbye!")
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Please check your installation and try again.")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main() 