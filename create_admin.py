#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysystem.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USERNAME')
password = os.environ.get('ADMIN_PASSWORD')

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, '', password)
    print(f"Superuser '{username}' created.")