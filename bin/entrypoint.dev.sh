#!/bin/bash
set -e

while ! nc -z db 5432; do sleep 1; done;
python manage.py runserver 0.0.0.0:8000