#!/bin/bash

# Crypto Compatibility Engine - Quick Start Script
# This script helps you get started quickly

echo "╔══════════════════════════════════════════════╗"
echo "║  🚀 Crypto Compatibility Engine Setup       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - FARCASTER_API_KEY"
    echo "   - DATABASE_URL"
    echo ""
    echo "Press Enter to continue when ready..."
    read
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed!"
echo ""

# Check PostgreSQL
echo "🔍 Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL is installed"
    
    # Check if database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw crypto_compatibility; then
        echo "✅ Database 'crypto_compatibility' exists"
    else
        echo "⚠️  Database 'crypto_compatibility' not found"
        echo "   Creating database..."
        echo "   You may need to enter your PostgreSQL password"
        
        # Try to create database
        sudo -u postgres psql -c "CREATE DATABASE crypto_compatibility;" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Database created successfully!"
        else
            echo "⚠️  Could not auto-create database"
            echo "   Please create it manually:"
            echo "   sudo -u postgres psql"
            echo "   CREATE DATABASE crypto_compatibility;"
        fi
    fi
else
    echo "⚠️  PostgreSQL not found. Installing..."
    echo "   sudo apt update && sudo apt install postgresql postgresql-contrib"
fi
echo ""

# Check Redis
echo "🔍 Checking Redis..."
if command -v redis-cli &> /dev/null; then
    echo "✅ Redis is installed"
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis is not running. Starting..."
        sudo systemctl start redis
    fi
else
    echo "⚠️  Redis not found (optional, but recommended)"
    echo "   Install with: sudo apt install redis-server"
fi
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/images
mkdir -p data
mkdir -p templates
echo "✅ Directories created!"
echo ""

# Run database migrations (tables will be created on first run)
echo "🗄️  Database tables will be created automatically on first run"
echo ""

echo "╔══════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                          ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the server, run:"
echo ""
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "Or simply:"
echo ""
echo "   ./start.sh"
echo ""
echo "📚 Visit http://localhost:8000/docs for API documentation"
echo "❤️  Visit http://localhost:8000/ for the frame"
echo ""
echo "Happy matching! 💕"
