#!/bin/sh

echo "Works well"

python manage.py migrate

echo "
import os
from django.contrib.auth.models import User

User.objects.create_superuser(
    os.getenv('ADMIN_USERNAME'),
    os.getenv('ADMIN_EMAIL'),
    os.getenv('ADMIN_PASSWORD')
)" | python manage.py shell

python manage.py runserver 0.0.0.0:8000

$@