from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erp_core.models import Employee
from django.utils import timezone
from django.db import connection


class Command(BaseCommand):
    help = 'Initialize the application with required data'

    def handle(self, *args, **options):
        self.stdout.write('=== Initializing application ===')
        
        # Check if database tables exist
        table_names = connection.introspection.table_names()
        self.stdout.write(f'Available tables: {table_names}')
        
        if 'auth_user' not in table_names:
            self.stdout.write(self.style.ERROR('Database tables not found! Running migrations...'))
            from django.core.management import call_command
            call_command('migrate', verbosity=2)
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            
            # Create employee profile for superuser
            Employee.objects.create(
                user=user,
                department='Administration',
                position='Admin',
                phone='N/A',
                hire_date=timezone.now().date()
            )
            self.stdout.write(self.style.SUCCESS('Employee profile created for superuser!'))
        else:
            self.stdout.write('Superuser already exists.')
            user = User.objects.get(username='admin')
            if not hasattr(user, 'employee'):
                Employee.objects.create(
                    user=user,
                    department='Administration',
                    position='Admin',
                    phone='N/A',
                    hire_date=timezone.now().date()
                )
                self.stdout.write(self.style.SUCCESS('Employee profile created for existing superuser!'))
        
        self.stdout.write(self.style.SUCCESS('=== Application initialization completed! ==='))
