# 🚀 Neon PostgreSQL Deployment Guide

This guide shows you how to deploy your Gestion Heures Django app with Neon PostgreSQL database.

## 📋 Prerequisites

- Neon PostgreSQL database account
- Your Django app ready for deployment
- Environment variables configured

## 🔧 Step 1: Configure Your .env File

Create a `.env` file in your project root with your Neon database credentials:

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Neon PostgreSQL Database
DATABASE_URL=postgresql://neondb_owner:npg_mnrk0j2MNWOF@ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech:5432/neondb?sslmode=require

# Security Settings
SECURE_SSL_REDIRECT=True
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com

# Other settings...
```

## 🌐 Step 2: Deploy to Render

### Option A: Using Render Dashboard

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service**
3. **Configure the service:**
   - **Name:** `gestion-heures-app`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn gestion_heures.wsgi:application --bind 0.0.0.0:$PORT`

### Option B: Using render.yaml

Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: gestion-heures-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn gestion_heures.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: your-app-name.onrender.com
      - key: DATABASE_URL
        value: postgresql://neondb_owner:npg_mnrk0j2MNWOF@ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech:5432/neondb?sslmode=require
      - key: SECURE_SSL_REDIRECT
        value: True
      - key: CSRF_TRUSTED_ORIGINS
        value: https://your-app-name.onrender.com
```

## 🔒 Step 3: Security Configuration

### Environment Variables in Render

Set these environment variables in your Render dashboard:

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://neondb_owner:npg_mnrk0j2MNWOF@ep-square-block-abfm3ciy-pooler.eu-west-2.aws.neon.tech:5432/neondb?sslmode=require
SECURE_SSL_REDIRECT=True
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

## 🗄️ Step 4: Database Setup

### Run Migrations

After deployment, run migrations to set up your database:

```bash
# In Render shell or locally with production settings
python manage.py migrate --settings=gestion_heures.settings_production
```

### Create Superuser

```bash
python manage.py createsuperuser --settings=gestion_heures.settings_production
```

## 🧪 Step 5: Test Your Deployment

1. **Visit your app URL:** `https://your-app-name.onrender.com`
2. **Test database connection** by uploading an Excel file
3. **Check logs** in Render dashboard for any errors

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Verify your `DATABASE_URL` is correct
   - Ensure `sslmode=require` is included
   - Check if Neon database is active

2. **Migration Errors:**
   - Run `python manage.py migrate --settings=gestion_heures.settings_production`
   - Check if database user has proper permissions

3. **Static Files Not Loading:**
   - Run `python manage.py collectstatic --settings=gestion_heures.settings_production`
   - Verify WhiteNoise is configured correctly

### Useful Commands

```bash
# Check database connection
python manage.py dbshell --settings=gestion_heures.settings_production

# Run migrations
python manage.py migrate --settings=gestion_heures.settings_production

# Collect static files
python manage.py collectstatic --settings=gestion_heures.settings_production

# Create superuser
python manage.py createsuperuser --settings=gestion_heures.settings_production
```

## 📊 Monitoring

- **Render Dashboard:** Monitor app performance and logs
- **Neon Dashboard:** Monitor database performance and connections
- **Django Admin:** Monitor application data and users

## 🔄 Updates and Maintenance

1. **Update your code** and push to GitHub
2. **Render will automatically redeploy** your app
3. **Run migrations** if you have database changes
4. **Monitor logs** for any issues

## 🎯 Benefits of Neon + Render

✅ **Serverless PostgreSQL** - No database management required  
✅ **Automatic Scaling** - Handles traffic spikes  
✅ **Built-in SSL** - Secure connections  
✅ **Free Tier** - Generous free tier available  
✅ **Easy Integration** - Works seamlessly with Django  
✅ **Global CDN** - Fast loading worldwide  

Your Django app is now ready for production with Neon PostgreSQL! 🚀 