#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/render.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
echo "Note: Migrations will run via pre-deploy command (requires database access)"
