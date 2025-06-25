#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from erp_core.models import Employee
from django.utils import timezone

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('Superuser created successfully!')
    
    # Create employee profile for superuser
    if not hasattr(user, 'employee'):
        Employee.objects.create(
            user=user,
            department='Administration',
            position='Admin',
            phone='N/A',
            hire_date=timezone.now().date()
        )
        print('Employee profile created for superuser!')
else:
    print('Superuser already exists.')
    user = User.objects.get(username='admin')
    if not hasattr(user, 'employee'):
        Employee.objects.create(
            user=user,
            department='Administration',
            position='Admin',
            phone='N/A',
            hire_date=timezone.now().date()
        )
        print('Employee profile created for existing superuser!')
"

echo "Build completed successfully!"
