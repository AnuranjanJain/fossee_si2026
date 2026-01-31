"""
Create initial admin user for deployment.
Run with: python manage.py shell < create_admin.py
"""
from django.contrib.auth.models import User
import os

username = os.environ.get('ADMIN_USERNAME', 'admin')
password = os.environ.get('ADMIN_PASSWORD', 'admin123')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created admin user: {username}")
else:
    print(f"Admin user already exists: {username}")
