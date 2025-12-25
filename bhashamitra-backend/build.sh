#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/render.txt

# Verify google-cloud-texttospeech is installed
echo "Checking Google TTS package..."
pip show google-cloud-texttospeech || echo "WARNING: google-cloud-texttospeech not installed!"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
echo "Note: Migrations will run via pre-deploy command (requires database access)"
