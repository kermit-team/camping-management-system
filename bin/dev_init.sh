#!/bin/bash
set -e

export DOCKER_BUILDKIT=1
{
    docker compose up --detach
    docker compose run --rm django python manage.py makemigrations
    docker compose run --rm django python manage.py migrate    
    #docker compose run --rm django python manage.py loaddata groups_and_permissions.json
    docker compose run --rm django python manage.py createsuperuser --no-input
} || {
    docker-compose up --detach
    docker-compose run --rm django python manage.py makemigrations
    docker-compose run --rm django python manage.py migrate
    #docker-compose run --rm django python manage.py loaddata groups_and_permissions.json
    docker-compose run --rm django python manage.py createsuperuser --no-input
}