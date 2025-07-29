"""
Neon PostgreSQL Configuration Example for Gestion Heures Django App

This file shows how to configure your Django app to use Neon PostgreSQL database.
"""

# Your Neon PostgreSQL configuration converted to DATABASE_URL format:
DATABASE_URL = "postgresql://neondb_owner:npg_mnrk0j2MNWOF@ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech:5432/neondb?sslmode=require"

# Alternative: Traditional Django database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_mnrk0j2MNWOF',
        'HOST': 'ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# How to use with your Django settings:

# Option 1: Using DATABASE_URL (Recommended)
# Add this to your .env file:
# DATABASE_URL=postgresql://neondb_owner:npg_mnrk0j2MNWOF@ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech:5432/neondb?sslmode=require

# Option 2: Using individual environment variables
# Add these to your .env file:
# DB_NAME=neondb
# DB_USER=neondb_owner
# DB_PASSWORD=npg_mnrk0j2MNWOF
# DB_HOST=ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech
# DB_PORT=5432
# DB_SSLMODE=require

# Your Django settings will automatically use the DATABASE_URL
# from the environment variable thanks to dj-database-url configuration. 