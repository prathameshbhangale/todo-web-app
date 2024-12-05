#!/bin/bash

# Exit on error
set -e

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run collectstatic to gather static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Any other build steps can be added here
echo "Build process completed."
