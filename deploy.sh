#!/bin/bash

# Production Deployment Script for Django Gestion Heures
# Make sure to run this as a user with appropriate permissions

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy env.example to .env and configure your environment variables."
    exit 1
fi

# Load environment variables
source .env

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Set up PostgreSQL
echo "🗄️ Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

# Run Django migrations
echo "🔄 Running database migrations..."
export DJANGO_SETTINGS_MODULE=gestion_heures.settings_production
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo "👤 Creating superuser..."
python manage.py createsuperuser --noinput || echo "Superuser creation skipped (may already exist)"

# Set up Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/gestion_heures << EOF
server {
    listen 80;
    server_name $DJANGO_ALLOWED_HOSTS;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DJANGO_ALLOWED_HOSTS;
    
    # SSL Configuration (you'll need to add your certificates)
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/gestion_heures /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service for Gunicorn
echo "⚙️ Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gestion_heures.service << EOF
[Unit]
Description=Gestion Heures Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=gestion_heures.settings_production"
ExecStart=/path/to/your/project/venv/bin/gunicorn --config gunicorn.conf.py gestion_heures.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Start and enable services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable gestion_heures
sudo systemctl start gestion_heures
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Set up firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Set up log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/gestion_heures << EOF
/path/to/your/project/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload gestion_heures
    endscript
}
EOF

# Set proper permissions
echo "🔐 Setting file permissions..."
sudo chown -R www-data:www-data /path/to/your/project
sudo chmod -R 755 /path/to/your/project
sudo chmod 600 /path/to/your/project/.env

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update the Nginx configuration with your actual domain and SSL certificates"
echo "2. Update the systemd service file with your actual project path"
echo "3. Configure SSL certificates (Let's Encrypt recommended)"
echo "4. Set up regular backups"
echo "5. Monitor the application logs"
echo ""
echo "🔍 Useful commands:"
echo "  Check status: sudo systemctl status gestion_heures"
echo "  View logs: sudo journalctl -u gestion_heures -f"
echo "  Restart app: sudo systemctl restart gestion_heures"
echo "  Check Nginx: sudo nginx -t && sudo systemctl status nginx" 