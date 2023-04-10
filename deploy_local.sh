#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Python is not installed. Please install Python 3.6 or higher."
  exit 1
fi

# Check if Pipenv is installed
if ! command -v pipenv &> /dev/null; then
  echo "Pipenv is not installed. Installing Pipenv..."
  pip install pipenv
fi

# Install dependencies
echo "Installing dependencies..."
pipenv install

# Activate virtual environment
echo "Activating virtual environment..."
pipenv shell

# Set environment variables from .env file
echo "Setting environment variables from .env file..."
export $(grep -v ^# .env | xargs)

# Run FastAPI application using Uvicorn
echo "Starting FastAPI application using Uvicorn..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

