"""
Taxeen Backend - FastAPI Application
Nigerian Personal Tax Intelligence Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db
from app.api import (
    auth_router,
    bank_accounts_router,
    transactions_router,
    uploads_router,
    tax_reports_router,
    admin_router
)

app = FastAPI(
    title="Taxeen API",
    description="Taxeen - Nigerian Personal Tax Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(bank_accounts_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(uploads_router, prefix="/api")
app.include_router(tax_reports_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ Taxeen Backend Started")


@app.get("/")
def root():
    return {"name": "Taxeen API", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
