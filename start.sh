#!/bin/bash

# Simple start script for Crypto Compatibility Engine

echo "🚀 Starting Crypto Compatibility Engine..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Run ./setup.sh first!"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Run ./setup.sh first!"
    exit 1
fi

# Start the application
echo "🌐 Starting server on http://localhost:8000"
echo ""
python app.py
