# Taxeen — Nigerian Personal Tax SaaS

A SaaS platform that helps Nigerians calculate their personal income tax using real financial transactions from bank statements.

## Target Users

- Freelancers
- Consultants
- Remote workers
- Small business owners
- Crypto traders
- Anyone earning income outside PAYE

**Subscription:** ₦5,000/year

## Features

- **Secure Registration** - NIN verification with AES-256 encryption
- **Bank Account Management** - Link multiple Nigerian bank accounts
- **Statement Upload** - Parse PDF bank statements automatically
- **Transaction Classification** - Categorize income, expenses, transfers
- **Internal Transfer Detection** - Auto-detect transfers between your accounts
- **Nigerian Tax Engine** - 2026 Personal Income Tax calculation
- **Tax Reports** - Export in PDF, CSV, JSON formats
- **Admin Panel** - User management, system settings, logs

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- Redis + Celery
- PyJWT, Argon2, PyCryptodome

### Frontend 1
- Flask + Jinja2
- HTMX + Alpine.js
- TailwindCSS + Flowbite
- ECharts

### Frontend 2
- Vue.js 3 + Pinia
- TailwindCSS

### Parsing
- pdfplumber
- pytesseract
- OpenCV

## Nigerian Tax Bands (2026)

| Income Band | Tax Rate |
|-------------|----------|
| ₦0 - ₦800,000 | 0% |
| ₦800,001 - ₦3,000,000 | 15% |
| ₦3,000,001 - ₦12,000,000 | 18% |
| ₦12,000,001 - ₦25,000,000 | 21% |
| ₦25,000,001 - ₦50,000,000 | 23% |
| Above ₦50,000,000 | 25% |

**First ₦800,000 is tax-free**

### Allowable Deductions
- Pension contributions
- NHF contributions
- NHIS contributions
- Life insurance premiums
- Mortgage interest
- Charitable donations
- Rent relief: min(20% of annual rent, ₦500,000)

## Project Structure

```
taxeen/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── auth/     # Security & encryption
│   │   ├── models/   # SQLAlchemy models
│   │   └── tax_engine/ # Nigerian tax calculator
│   └── requirements.txt
├── frontend1/        # Flask dashboard
├── frontend2/        # Vue.js dashboard
├── website1/         # Flask marketing site
├── website2/         # Vue marketing site
└── infra/            # Docker & Nginx configs
```

## Running the Project

### Backend

```bash
cd taxeen/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd taxeen/frontend1
pip install flask requests
python app.py
```

## Security

- **NIN Encryption** - AES-256
- **Password Hashing** - Argon2
- **Authentication** - JWT
- **File Safety** - Statements auto-deleted after parsing

## Development Phases

- [x] Phase 1: Authentication, Subscription logic, Bank accounts, Statement upload
- [x] Phase 2: Transaction extraction, Internal transfer detection, Classification
- [x] Phase 3: Tax engine, Report generation
- [ ] Phase 4: AI classification, Bank API integration

## License

MIT License

---

Built with ❤️ for Nigerians
