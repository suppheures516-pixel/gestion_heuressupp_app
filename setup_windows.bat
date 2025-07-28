@echo off
echo 🚀 Django Gestion Heures - Windows Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo 📋 Installing required packages...
pip install Django>=5.1.7,<5.2
pip install pandas>=2.1.0
pip install openpyxl>=3.1.2
pip install xlrd>=2.0.1

REM Ask for optional packages
echo.
set /p install_magic="Do you want to install python-magic for enhanced file validation? (y/n): "
if /i "%install_magic%"=="y" (
    echo 📦 Installing python-magic...
    pip install python-magic>=0.4.27
)

set /p install_env="Do you want to install django-environ for environment management? (y/n): "
if /i "%install_env%"=="y" (
    echo 📦 Installing django-environ...
    pip install django-environ>=0.11.2
)

REM Copy environment template
if not exist ".env" (
    echo 📄 Creating .env file from template...
    copy env.example .env
    echo ⚠️ Please edit .env file with your configuration
)

REM Run migrations
echo 🔄 Running database migrations...
python manage.py migrate

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✅ Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your configuration
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Start the server: python manage.py runserver
echo.
pause 