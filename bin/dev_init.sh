#!/bin/bash
set -e

export DOCKER_BUILDKIT=1
{
    docker compose up --detach
    docker compose run --rm django python manage.py makemigrations
    docker compose run --rm django python manage.py migrate    
    docker compose run --rm django python manage.py loaddata groups_with_permissions.json
    docker compose run --rm django python manage.py createsuperuser --no-input
    docker compose run --rm django python manage.py loaddata users.json users_cars.json camping_plots.json reservations.json
} || {
    docker-compose up --detach
    docker-compose run --rm django python manage.py makemigrations
    docker-compose run --rm django python manage.py migrate
    docker-compose run --rm django python manage.py loaddata groups_with_permissions.json
    docker-compose run --rm django python manage.py createsuperuser --no-input
    docker-compose run --rm django python manage.py loaddata users.json users_cars.json camping_plots.json reservations.json
}