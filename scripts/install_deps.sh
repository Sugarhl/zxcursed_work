#!/bin/bash

if ! command -v python3 &> /dev/null; then
  echo "Python is not installed. Please install Python 3.10."
  exit 1
fi

if ! command -v pipenv &> /dev/null; then
  echo "Pipenv is not installed. Installing Pipenv..."
  pip install pipenv
fi

echo "Remove old venv dependencies..."
pipenv --rm

echo "Installing dependencies..."
pipenv install

echo "Activating virtual environment..."
pipenv shell

