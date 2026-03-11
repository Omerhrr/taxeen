"""
Tax Reports API Routes
Generate Nigerian personal income tax reports
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import io
import json
import csv

from app.database import get_db
from app.models import User, BankAccount, Transaction
from app.auth import get_current_user
from app.tax_engine.calculator import NigerianTaxEngine
from app.config import settings
from app.schemas.tax_report import (
    TaxReportRequest,
    TaxReportResponse,
    TaxReportSummary,
    TaxReportExport,
    TaxCalculationPreview,
    DeductionItem,
    TaxBandBreakdown,
    AnnualTaxSummary,
)
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/tax-reports", tags=["Tax Reports"])


@router.post("/generate", response_model=TaxReportResponse)
async def generate_tax_report(
    request: TaxReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a comprehensive tax report for a period
    
    - Calculates gross income from transactions
    - Applies allowable deductions
    - Computes tax using Nigerian 2026 tax bands
    """
    # Determine date range
    if request.date_from and request.date_to:
        date_from = request.date_from
        date_to = request.date_to
    else:
        # Use full tax year
        date_from = datetime(request.tax_year, 1, 1)
        date_to = datetime(request.tax_year, 12, 31)
    
    # Get all transactions for the period
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date <= date_to,
        Transaction.is_internal_transfer == False,
    ).all()
    
    # Calculate income
    gross_income = sum(
        tx.amount for tx in transactions
        if tx.is_income and tx.is_taxable
    )
    
    total_credits = sum(
        tx.amount for tx in transactions
        if tx.is_income
    )
    
    total_debits = sum(
        tx.amount for tx in transactions
        if tx.is_expense
    )
    
    # Calculate deductions from categorized transactions
    pension_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "pension" and tx.is_deductible
    )
    
    nhf_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "nhf" and tx.is_deductible
    )
    
    nhis_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "nhis" and tx.is_deductible
    )
    
    life_insurance_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "insurance" and tx.is_deductible
    )
    
    mortgage_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "mortgage_interest" and tx.is_deductible
    )
    
    donations_from_tx = sum(
        tx.amount for tx in transactions
        if tx.category == "charitable_donation" and tx.is_deductible
    )
    
    # Use provided values or transaction values
    pension = request.pension_amount or pension_from_tx if request.include_pension else 0
    nhf = request.nhf_amount or nhf_from_tx if request.include_nhf else 0
    nhis = request.nhis_amount or nhis_from_tx if request.include_nhis else 0
    life_insurance = request.life_insurance or life_insurance_from_tx
    mortgage_interest = request.mortgage_interest or mortgage_from_tx
    charitable_donations = request.charitable_donations or donations_from_tx
    
    # Add other deductions
    other_deductions_total = sum(d.amount for d in request.other_deductions)
    
    # Calculate rent relief
    rent_relief = 0
    if request.include_rent_relief and request.annual_rent:
        rent_relief = min(
            request.annual_rent * settings.RENT_RELIEF_PERCENTAGE,
            settings.RENT_RELIEF_MAX
        )
    
    # Calculate tax
    engine = NigerianTaxEngine()
    
    # Total deductions
    total_deductions = pension + nhf + nhis + life_insurance + mortgage_interest + charitable_donations + rent_relief + other_deductions_total
    
    # Taxable income
    taxable_income = max(0, gross_income - total_deductions)
    
    # Calculate tax
    tax_result = engine.calculate_tax(taxable_income)
    
    # Get statistics
    internal_transfers = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date <= date_to,
        Transaction.is_internal_transfer == True,
    ).count()
    
    internal_transfers_amount = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date <= date_to,
        Transaction.is_internal_transfer == True,
    ).scalar() or 0
    
    categorized = sum(1 for tx in transactions if tx.category != "uncategorized")
    uncategorized = len(transactions) - categorized
    
    # Build response
    response = TaxReportResponse(
        id=None,
        user_id=current_user.id,
        tax_year=request.tax_year,
        date_from=date_from,
        date_to=date_to,
        generated_at=datetime.utcnow(),
        gross_income=gross_income,
        total_credits=total_credits,
        total_debits=total_debits,
        net_income=total_credits - total_debits,
        pension_contribution=pension,
        nhf_contribution=nhf,
        nhis_contribution=nhis,
        life_insurance=life_insurance,
        mortgage_interest=mortgage_interest,
        charitable_donations=charitable_donations,
        rent_relief=rent_relief,
        total_deductions=total_deductions,
        taxable_income=taxable_income,
        tax_free_allowance=tax_result.get("tax_free_allowance", settings.TAX_FREE_THRESHOLD),
        tax_band_breakdown=[
            TaxBandBreakdown(**band) for band in tax_result.get("breakdown", [])
        ],
        total_tax_payable=tax_result.get("total_tax", 0),
        effective_tax_rate=tax_result.get("effective_rate", 0),
        monthly_tax=tax_result.get("monthly_tax", 0),
        internal_transfers_detected=internal_transfers,
        internal_transfers_amount=internal_transfers_amount,
        categorized_transactions=categorized,
        uncategorized_transactions=uncategorized,
        is_finalized=False,
    )
    
    return response


@router.get("/preview", response_model=TaxCalculationPreview)
async def preview_tax_calculation(
    gross_income: float,
    pension: float = 0,
    nhf: float = 0,
    nhis: float = 0,
    life_insurance: float = 0,
    mortgage_interest: float = 0,
    charitable_donations: float = 0,
    annual_rent: float = 0,
    current_user: User = Depends(get_current_user),
):
    """
    Preview tax calculation with given parameters
    """
    # Calculate rent relief
    rent_relief = 0
    if annual_rent > 0:
        rent_relief = min(
            annual_rent * settings.RENT_RELIEF_PERCENTAGE,
            settings.RENT_RELIEF_MAX
        )
    
    # Total deductions
    total_deductions = pension + nhf + nhis + life_insurance + mortgage_interest + charitable_donations + rent_relief
    
    # Taxable income
    taxable_income = max(0, gross_income - total_deductions)
    
    # Calculate tax
    engine = NigerianTaxEngine()
    tax_result = engine.calculate_tax(taxable_income)
    
    return TaxCalculationPreview(
        gross_income=gross_income,
        deductions={
            "pension": pension,
            "nhf": nhf,
            "nhis": nhis,
            "life_insurance": life_insurance,
            "mortgage_interest": mortgage_interest,
            "charitable_donations": charitable_donations,
            "rent_relief": rent_relief,
            "total": total_deductions,
        },
        taxable_income=taxable_income,
        tax_breakdown=[TaxBandBreakdown(**band) for band in tax_result.get("breakdown", [])],
        total_tax=tax_result.get("total_tax", 0),
        monthly_tax=tax_result.get("monthly_tax", 0),
        effective_rate=tax_result.get("effective_rate", 0),
    )


@router.get("/annual-summary", response_model=AnnualTaxSummary)
async def get_annual_summary(
    tax_year: int = Query(..., ge=2020, le=2030),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get annual tax summary with monthly breakdown
    """
    # Get monthly income and tax
    monthly_data = []
    monthly_income = []
    monthly_tax = []
    
    engine = NigerianTaxEngine()
    
    for month in range(1, 13):
        start_date = datetime(tax_year, month, 1)
        if month == 12:
            end_date = datetime(tax_year + 1, 1, 1) - relativedelta(days=1)
        else:
            end_date = datetime(tax_year, month + 1, 1) - relativedelta(days=1)
        
        # Get income for month
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.is_income == True,
            Transaction.is_internal_transfer == False,
            Transaction.is_taxable == True,
        ).scalar() or 0
        
        monthly_income.append(income)
        
        # Calculate estimated monthly tax
        annual_equivalent = income * 12
        tax_result = engine.calculate_tax(annual_equivalent)
        monthly_tax.append(tax_result.get("monthly_tax", 0))
    
    # Calculate totals
    total_income = sum(monthly_income)
    total_tax = sum(monthly_tax)
    
    return AnnualTaxSummary(
        tax_year=tax_year,
        monthly_income=monthly_income,
        monthly_tax=monthly_tax,
        total_income=total_income,
        total_tax=total_tax,
        average_monthly_tax=total_tax / 12 if total_tax > 0 else 0,
    )


@router.get("/tax-bands")
async def get_tax_bands():
    """
    Get current Nigerian tax bands
    """
    return {
        "year": 2026,
        "tax_free_threshold": settings.TAX_FREE_THRESHOLD,
        "bands": [
            {
                "name": "Band 1",
                "range": "₦0 - ₦800,000",
                "rate": "0%",
                "lower": 0,
                "upper": 800000,
            },
            {
                "name": "Band 2",
                "range": "₦800,001 - ₦3,000,000",
                "rate": "15%",
                "lower": 800001,
                "upper": 3000000,
            },
            {
                "name": "Band 3",
                "range": "₦3,000,001 - ₦12,000,000",
                "rate": "18%",
                "lower": 3000001,
                "upper": 12000000,
            },
            {
                "name": "Band 4",
                "range": "₦12,000,001 - ₦25,000,000",
                "rate": "21%",
                "lower": 12000001,
                "upper": 25000000,
            },
            {
                "name": "Band 5",
                "range": "₦25,000,001 - ₦50,000,000",
                "rate": "23%",
                "lower": 25000001,
                "upper": 50000000,
            },
            {
                "name": "Band 6",
                "range": "Above ₦50,000,000",
                "rate": "25%",
                "lower": 50000001,
                "upper": None,
            },
        ],
        "allowable_deductions": [
            {"name": "Pension Contribution", "description": "Contributions to approved pension schemes"},
            {"name": "NHF", "description": "National Housing Fund contributions"},
            {"name": "NHIS", "description": "National Health Insurance Scheme contributions"},
            {"name": "Life Insurance", "description": "Life insurance premiums"},
            {"name": "Mortgage Interest", "description": "Interest on mortgage for owner-occupied property"},
            {"name": "Charitable Donations", "description": "Donations to approved charitable organizations"},
            {"name": "Rent Relief", "description": f"Min(20% of annual rent, ₦{settings.RENT_RELIEF_MAX:,.0f})"},
        ],
    }


@router.get("/deductions/summary")
async def get_deductions_summary(
    tax_year: int = Query(..., ge=2020, le=2030),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get summary of potential deductions from categorized transactions
    """
    date_from = datetime(tax_year, 1, 1)
    date_to = datetime(tax_year, 12, 31)
    
    # Get deductible transactions by category
    deductions = {}
    
    deductible_categories = [
        ("pension", "Pension Contribution"),
        ("nhf", "National Housing Fund"),
        ("nhis", "National Health Insurance"),
        ("insurance", "Life Insurance"),
        ("mortgage_interest", "Mortgage Interest"),
        ("charitable_donation", "Charitable Donations"),
    ]
    
    for cat_code, cat_name in deductible_categories:
        total = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date <= date_to,
            Transaction.category == cat_code,
            Transaction.is_deductible == True,
        ).scalar() or 0
        
        if total > 0:
            deductions[cat_code] = {
                "name": cat_name,
                "amount": total,
                "transaction_count": db.query(Transaction).filter(
                    Transaction.user_id == current_user.id,
                    Transaction.transaction_date >= date_from,
                    Transaction.transaction_date <= date_to,
                    Transaction.category == cat_code,
                    Transaction.is_deductible == True,
                ).count()
            }
    
    return {
        "tax_year": tax_year,
        "deductions": deductions,
        "total_deductions": sum(d["amount"] for d in deductions.values()),
    }


@router.post("/export")
async def export_tax_report(
    report_data: TaxReportResponse,
    format: str = Query("csv", pattern="^(csv|json)$"),
    current_user: User = Depends(get_current_user),
):
    """
    Export tax report in various formats
    """
    if format == "json":
        # Return as JSON
        return report_data.model_dump()
    
    elif format == "csv":
        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["Taxeen Tax Report", f"Tax Year {report_data.tax_year}"])
        writer.writerow([])
        
        # Income section
        writer.writerow(["INCOME"])
        writer.writerow(["Gross Income", f"₦{report_data.gross_income:,.2f}"])
        writer.writerow(["Total Credits", f"₦{report_data.total_credits:,.2f}"])
        writer.writerow(["Total Debits", f"₦{report_data.total_debits:,.2f}"])
        writer.writerow([])
        
        # Deductions section
        writer.writerow(["DEDUCTIONS"])
        writer.writerow(["Pension Contribution", f"₦{report_data.pension_contribution:,.2f}"])
        writer.writerow(["NHF Contribution", f"₦{report_data.nhf_contribution:,.2f}"])
        writer.writerow(["NHIS Contribution", f"₦{report_data.nhis_contribution:,.2f}"])
        writer.writerow(["Life Insurance", f"₦{report_data.life_insurance:,.2f}"])
        writer.writerow(["Mortgage Interest", f"₦{report_data.mortgage_interest:,.2f}"])
        writer.writerow(["Charitable Donations", f"₦{report_data.charitable_donations:,.2f}"])
        writer.writerow(["Rent Relief", f"₦{report_data.rent_relief:,.2f}"])
        writer.writerow(["Total Deductions", f"₦{report_data.total_deductions:,.2f}"])
        writer.writerow([])
        
        # Tax calculation
        writer.writerow(["TAX CALCULATION"])
        writer.writerow(["Taxable Income", f"₦{report_data.taxable_income:,.2f}"])
        writer.writerow(["Tax-Free Allowance", f"₦{report_data.tax_free_allowance:,.2f}"])
        writer.writerow([])
        
        # Tax bands
        writer.writerow(["TAX BAND BREAKDOWN"])
        writer.writerow(["Band", "Taxable Amount", "Rate", "Tax"])
        for band in report_data.tax_band_breakdown:
            writer.writerow([
                band.band_name,
                f"₦{band.taxable_amount:,.2f}",
                f"{band.rate * 100:.0f}%",
                f"₦{band.tax_amount:,.2f}"
            ])
        writer.writerow([])
        
        # Totals
        writer.writerow(["TOTALS"])
        writer.writerow(["Total Tax Payable", f"₦{report_data.total_tax_payable:,.2f}"])
        writer.writerow(["Monthly Tax", f"₦{report_data.monthly_tax:,.2f}"])
        writer.writerow(["Effective Tax Rate", f"{report_data.effective_tax_rate * 100:.2f}%"])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=tax_report_{report_data.tax_year}.csv"
            }
        )
