#!/bin/bash
rm -rf .env
echo "Setting environment variables from .env file..."
cp .env.prod .env

echo "Starting FastAPI application using Uvicorn..."
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

