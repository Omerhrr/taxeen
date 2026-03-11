#!/bin/bash
# Quick start script for Taxeen Frontend1 (Flask Dashboard)

echo "🚀 Starting Taxeen Frontend..."

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
pip install -r requirements.txt -q

# Run the Flask app
echo "✅ Starting frontend on http://localhost:5000"
echo ""
python app.py
