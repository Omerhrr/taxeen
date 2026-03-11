# Taxeen Local Testing Guide

## Prerequisites
- Python 3.10+
- Node.js (optional, for Vue frontend)

## Quick Start

### Step 1: Backend Setup

```bash
# Navigate to backend
cd /home/z/my-project/taxeen/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Backend

```bash
# Make sure you're in the backend directory with venv activated
cd /home/z/my-project/taxeen/backend
source venv/bin/activate

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

### Step 3: Frontend1 Setup (Flask Dashboard)

Open a new terminal:

```bash
# Navigate to frontend1
cd /home/z/my-project/taxeen/frontend1

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run Frontend1

```bash
# Make sure you're in frontend1 directory with venv activated
cd /home/z/my-project/taxeen/frontend1
source venv/bin/activate

# Run Flask app
python app.py
```

Frontend1 will be available at: http://localhost:5000

---

## Alternative: Run Only Backend (for API testing)

If you just want to test the API:

```bash
cd /home/z/my-project/taxeen/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/docs for interactive API testing.

---

## Database

SQLite database file will be created automatically at:
- `/home/z/my-project/taxeen/backend/taxeen.db`

To reset the database:
```bash
rm /home/z/my-project/taxeen/backend/taxeen.db
# Restart the server - it will create a fresh database
```

---

## Default Test Credentials

After registering a user, you can use:
- Email: demo@taxeen.ng
- Password: demo123

---

## Testing the API

1. **Register a new user:**
   - POST `/api/auth/register`
   - Body: `{"email": "test@example.com", "password": "password123", "first_name": "Test", "last_name": "User"}`

2. **Login:**
   - POST `/api/auth/login`
   - Body: `{"email": "test@example.com", "password": "password123"}`
   - Returns: JWT token

3. **Add Bank Account:**
   - POST `/api/bank-accounts`
   - Headers: `Authorization: Bearer <token>`
   - Body: `{"bank_name": "GTBank", "account_number": "0123456789", "account_name": "TEST USER"}`

---

## Troubleshooting

### Port already in use:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Module not found:
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database errors:
```bash
# Delete and recreate database
rm taxeen.db
uvicorn app.main:app --reload
```
