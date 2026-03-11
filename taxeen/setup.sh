#!/bin/bash
# Taxeen Local Development Setup Script

echo "🚀 Setting up Taxeen for local development..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend setup
echo -e "${YELLOW}Setting up Backend...${NC}"
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads/statements uploads/exports

# Initialize database
echo "Initializing SQLite database..."
python -c "from app.database import init_db; init_db()"

echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""
echo "To run the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

# Frontend1 setup
echo -e "${YELLOW}Setting up Frontend1 (Flask)...${NC}"
cd ../frontend1

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✅ Frontend1 setup complete!${NC}"
echo ""
echo "To run Frontend1:"
echo "  cd frontend1"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Frontend will be available at: http://localhost:5000"
echo ""

# Frontend2 setup (optional)
echo -e "${YELLOW}Setting up Frontend2 (Vue.js)...${NC}"
cd ../frontend2

if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    npm install
    echo -e "${GREEN}✅ Frontend2 setup complete!${NC}"
    echo ""
    echo "To run Frontend2:"
    echo "  cd frontend2"
    echo "  npm run dev"
    echo ""
    echo "Vue app will be available at: http://localhost:3001"
else
    echo "Node.js not found. Skipping Frontend2 setup."
fi

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Quick Start:"
echo "  1. Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  2. Terminal 2: cd frontend1 && source venv/bin/activate && python app.py"
echo "  3. Open: http://localhost:5000"
