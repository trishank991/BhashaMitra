#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/render.txt

# Verify google-cloud-texttospeech is installed
echo "Checking Google Cloud packages..."
pip show google-cloud-texttospeech || echo "WARNING: google-cloud-texttospeech not installed!"
pip show google-cloud-speech || echo "WARNING: google-cloud-speech not installed!"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Build completed successfully!"
