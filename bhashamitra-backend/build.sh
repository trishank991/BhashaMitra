#!/usr/bin/env bash
# exit on error
set -o errexit

# Poetry configuration
echo "Configuring poetry..."
poetry config virtualenvs.in-project true

# Install dependencies
echo "Installing dependencies from poetry.lock..."
poetry install --no-root --no-dev

# Collect static files
echo "Collecting static files..."
poetry run python manage.py collectstatic --no-input

echo "Build finished successfully!"
