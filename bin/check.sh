#!/bin/bash

set -o nounset

pyclean() {
    find . | grep -E 'pytest_cache|\.py[cod]$)' | xargs rm -rf
}

run_check () {
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

# Run check process
run_check

# Clean everything up
trap pyclean EXIT INT TERM