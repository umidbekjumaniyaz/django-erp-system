import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from erp_core.models import Employee

try:
    user = User.objects.get(username='admin')
    if not hasattr(user, 'employee'):
        Employee.objects.create(
            user=user,
            department='Admin',
            position='Super Admin',
            phone='N/A',
            hire_date='2025-05-28'
        )
        print('Employee record created successfully!')
    else:
        print('Employee record already exists.')
except User.DoesNotExist:
    print('Admin user does not exist.')
