#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/render.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "=== DEBUG: Checking environment ==="
echo "DJANGO_ENV: $DJANGO_ENV"
echo "DATABASE_URL set: $(if [ -n "$DATABASE_URL" ]; then echo 'YES'; else echo 'NO'; fi)"
echo "DATABASE_URL length: ${#DATABASE_URL}"
echo "==================================="

echo "Running migrations..."
python manage.py migrate

echo "Seeding initial data..."
python manage.py seed_badges || echo "Badge seeding skipped or already done"

echo "Build completed successfully!"
