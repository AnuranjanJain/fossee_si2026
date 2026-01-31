"""
Management command to create initial admin user.
Runs automatically during deployment.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates the initial admin user if not exists'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Admin user already exists: {username}')
            )
