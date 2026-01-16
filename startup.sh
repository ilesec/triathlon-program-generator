#!/bin/bash

# Startup script for Azure App Services
echo "Starting Triathlon Program Generator..."

# Create database if it doesn't exist
python -c "from app.database import init_db; init_db()"

# Get PORT from Azure environment variable (defaults to 8000)
PORT="${PORT:-8000}"

# Start the application with gunicorn
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile -
