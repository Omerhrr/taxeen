# Taxeen --- Nigerian Personal Tax SaaS

## Full Technical & Product Plan (2026)

## 1. Overview

Taxeen is a SaaS platform that helps Nigerians calculate their personal
income tax using their real financial transactions.

Users upload bank statements, the system extracts transactions,
classifies income/expenses, detects internal transfers, and calculates
tax based on Nigerian Personal Income Tax rules effective 2026.

Target Users: - Freelancers - Consultants - Remote workers - Small
business owners - Crypto traders - Anyone earning income outside PAYE

Annual subscription: ₦5000

------------------------------------------------------------------------

# 2. Core Features

1.  Secure account registration using:

    -   Name
    -   Email
    -   Username
    -   Password
    -   NIN

2.  Bank account management

3.  Bank statement upload

4.  Automatic transaction extraction

5.  Internal transfer detection

6.  Transaction classification

7.  Tax calculation engine

8.  Tax report generator

9.  Admin control panel

------------------------------------------------------------------------

# 3. System Architecture

Project structure:

taxeen/ backend/ frontend1/ frontend2/ website1/ website2/ infra/

Backend: FastAPI + SQLAlchemy

Database: PostgreSQL

Task Queue: Redis + Celery

------------------------------------------------------------------------

# 4. Tech Stack

Backend: - FastAPI - SQLAlchemy - PostgreSQL - Redis - Celery

Parsing: - pdfplumber - pytesseract - opencv

Frontend 1: - Flask - Jinja - HTMX - AlpineJS - TailwindCSS - Flowbite -
ECharts

Frontend 2: - VueJS - Pinia - Axios - TailwindCSS

------------------------------------------------------------------------

# 5. Registration Flow

User registers with:

name email username password nin

Account created with:

subscription_status = inactive

User redirected to payment page.

Login middleware checks:

if subscription inactive: redirect to payment page

------------------------------------------------------------------------

# 6. Database Schema

## users

id name email username password_hash nin_encrypted subscription_status
subscription_expiry created_at

## bank_accounts

id user_id bank_name account_number created_at

## statement_uploads

id user_id bank_account_id date_from date_to json_path md_path
created_at

## transactions

id user_id bank_account_id date description amount direction balance
category is_internal_transfer is_income is_expense taxable notes

------------------------------------------------------------------------

# 7. Bank Statement Processing

Pipeline:

upload statement ↓ store temporary file ↓ extract text ↓ parse
transactions ↓ convert to JSON ↓ generate markdown copy ↓ delete
original file

------------------------------------------------------------------------

# 8. Transaction JSON Example

\[ { "date": "2026-01-02", "description": "Transfer from John",
"amount": 50000, "direction": "credit", "balance": 150000 }\]

------------------------------------------------------------------------

# 9. Transaction Aggregation

Transactions from all banks are merged and sorted by date.

Example:

1 Jan 2026 --- Bank A 1 Jan 2026 --- Bank B 2 Jan 2026 --- Bank A

------------------------------------------------------------------------

# 10. Internal Transfer Detection

Algorithm checks:

-   Same user
-   Same amount
-   Opposite direction
-   Close timestamps
-   Different banks

Example:

Bank A debit 50,000\
Bank B credit 50,000

Result:

is_internal_transfer = true\
taxable = false

------------------------------------------------------------------------

# 11. Transaction Classification

Categories:

Income Expense Internal Transfer Loan Refund Gift Investment Tax Exempt

Users can manually classify transactions.

------------------------------------------------------------------------

# 12. Nigerian Personal Income Tax (2026)

Tax bands:

0 -- 800,000 → 0% 800,001 -- 3,000,000 → 15% 3,000,001 -- 12,000,000 →
18% 12,000,001 -- 25,000,000 → 21% 25,000,001 -- 50,000,000 → 23% Above
50,000,000 → 25%

First ₦800,000 is tax free.

------------------------------------------------------------------------

# 13. Rent Relief Allowance

CRA removed.

Rent relief:

min( 20% of annual rent, 500,000 )

------------------------------------------------------------------------

# 14. Allowable Deductions

Pension contributions\
NHF contributions\
NHIS contributions\
Life insurance premiums\
Mortgage interest\
Charitable donations\
Rent relief

------------------------------------------------------------------------

# 15. Tax Calculation Algorithm

gross_income ↓ subtract deductions ↓ chargeable_income ↓ apply tax bands
↓ final tax amount

------------------------------------------------------------------------

# 16. Dashboard Layout

Sidebar:

Dashboard

Banks GTBank Access Bank UBA

Transactions Uploads Income Expenses Internal Transfers Tax Exempt
Reports Settings

------------------------------------------------------------------------

# 17. Tax Reports

User selects date range.

System generates:

Total Income Total Expenses Deductions Chargeable Income Tax Payable

Export formats:

PDF CSV JSON

------------------------------------------------------------------------

# 18. Security

NIN encrypted (AES)

Passwords hashed using Argon2

JWT authentication

Uploaded statements deleted after parsing

Audit logs for sensitive actions

------------------------------------------------------------------------

# 19. Admin Panel

Admin can:

View users Update pricing Edit landing page View subscriptions Disable
accounts View system logs

------------------------------------------------------------------------

# 20. Development Phases

Phase 1: Authentication Subscription logic Bank accounts Statement
upload

Phase 2: Transaction extraction Internal transfer detection
Classification

Phase 3: Tax engine Report generation

Phase 4: AI classification Bank API integration

------------------------------------------------------------------------

# 21. Revenue Projection

20,000 users × ₦5000

= ₦100,000,000 yearly revenue

------------------------------------------------------------------------

# 22. Vision

Taxeen aims to become the Nigerian equivalent of TurboTax, giving
individuals the ability to understand and calculate their tax
obligations using real financial data.
