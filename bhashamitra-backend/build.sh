#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install CPU-only torch first (to avoid CUDA dependencies)
echo "Installing PyTorch CPU-only version..."
pip install torch==2.2.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# Install dependencies from requirements/prod.txt
echo "Installing production dependencies..."
pip install -r requirements/prod.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build finished successfully!"
