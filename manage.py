#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


if __name__ == "__main__":
    # Set the Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_heures.settings_production")
    
    # Automatically clear all sessions before starting the server
    if 'runserver' in sys.argv:
        try:
            import django
            django.setup()
            from django.contrib.sessions.models import Session
            Session.objects.all().delete()  # Delete ALL sessions
            print("[INFO] All sessions cleared. All users will be logged out.")
        except Exception as e:
            print(f"[INFO] Could not clear sessions automatically: {e}")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
