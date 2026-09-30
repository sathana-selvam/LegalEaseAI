#!/bin/bash

# Exit script immediately if a command exits with a non-zero status
set -e

# Make sure virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment 'venv' not found. Please create it using: python3 -m venv venv"
    exit 1
fi

# Install dependencies if needed
pip install -r requirements.txt --quiet

# Start FastAPI backend in the background
echo "Starting LegalEase API Backend..."
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait briefly for backend server startup
sleep 2

# Start Streamlit frontend
echo "Starting LegalEase Streamlit App..."
streamlit run frontend/app.py

# Kill backend process when Streamlit closes
kill $BACKEND_PID