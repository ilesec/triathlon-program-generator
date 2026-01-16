#!/bin/bash

# Startup script for Azure App Services
echo "Starting Triathlon Program Generator..."

# Create database if it doesn't exist
python -c "from app.database import init_db; init_db()"

# Start the application with gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
