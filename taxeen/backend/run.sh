#!/bin/bash
# Quick start script for Taxeen Backend

echo "🚀 Starting Taxeen Backend..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/lib/python3.*/site-packages/fastapi" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Create uploads directory
mkdir -p uploads/statements uploads/exports

# Run the server
echo "✅ Starting server on http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000
