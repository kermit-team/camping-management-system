#!/bin/bash

set -o nounset

pyclean() {
    find . | grep -E '__pycache__|\.py[cod]$)' | xargs rm -rf
}

run_check () {
    cd backend || exit

    echo "Running flake8..."
    flake8 .
    echo ""

    echo ""
    echo "Running migrations check..."
    python manage.py makemigrations --dry-run --check
    echo ""

    echo ""
    echo "Running tests check..."
    pytest
}

# Remove any cache files
pyclean

# Clean everything up
trap pyclean EXIT INT TERM

# Run check process
run_check