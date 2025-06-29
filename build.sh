#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "=== Running Django management commands ==="

echo "Making migrations..."
python manage.py makemigrations --verbosity=2

echo "Running database migrations..."
python manage.py migrate --verbosity=2

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear --verbosity=2

echo "=== Creating superuser and employee profile ==="
python manage.py init_app

echo "=== Checking database status ==="
python manage.py showmigrations --verbosity=2

echo "=== Build completed successfully! ==="
