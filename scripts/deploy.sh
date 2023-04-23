#!/bin/bash

if ! command -v python3 &> /dev/null; then
  echo "Python is not installed. Please install Python 3.6 or higher."
  exit 1
fi

if ! command -v pipenv &> /dev/null; then
  echo "Pipenv is not installed. Installing Pipenv..."
  pip install pipenv
fi

if [[ $1 == "--create-shell" ]]; then
echo "Installing dependencies..."
pipenv install

echo "Activating virtual environment..."
pipenv shell
fi

echo "Setting environment variables from .env file..."
cp .env.prod .env

echo "Starting FastAPI application using Uvicorn..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

