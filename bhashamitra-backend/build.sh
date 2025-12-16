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
python -c "import os; print(f'Python sees DATABASE_URL: {bool(os.getenv(\"DATABASE_URL\"))}')"
python -c "import os; env=os.getenv('DJANGO_ENV','dev'); db=os.getenv('DATABASE_URL'); print(f'Will load: prod' if env=='prod' or db else 'Will load: dev')"
echo "==================================="

echo "Running migrations..."
python manage.py migrate

echo "Seeding initial data..."
python manage.py seed_badges || echo "Badge seeding skipped or already done"

echo "Build completed successfully!"
