"""
Tax Report Schemas
Request/Response models for tax report endpoints
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal


class DeductionItem(BaseModel):
    """Individual deduction item"""
    name: str
    amount: float
    category: str
    is_verified: bool = False
    source: Optional[str] = None  # Transaction ID or manual entry


class TaxBandBreakdown(BaseModel):
    """Tax band calculation breakdown"""
    band_name: str
    lower_limit: float
    upper_limit: float
    rate: float
    taxable_amount: float
    tax_amount: float


class TaxReportRequest(BaseModel):
    """Tax report generation request"""
    tax_year: int = Field(..., ge=2020, le=2030)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    include_rent_relief: bool = True
    annual_rent: Optional[float] = Field(None, ge=0)
    include_pension: bool = True
    pension_amount: Optional[float] = Field(None, ge=0)
    include_nhf: bool = True
    nhf_amount: Optional[float] = Field(None, ge=0)
    include_nhis: bool = True
    nhis_amount: Optional[float] = Field(None, ge=0)
    life_insurance: float = Field(default=0, ge=0)
    mortgage_interest: float = Field(default=0, ge=0)
    charitable_donations: float = Field(default=0, ge=0)
    other_deductions: List[DeductionItem] = []


class TaxReportResponse(BaseModel):
    """Tax report response"""
    id: Optional[int] = None
    user_id: int
    tax_year: int
    date_from: datetime
    date_to: datetime
    generated_at: datetime
    
    # Income Summary
    gross_income: float
    total_credits: float
    total_debits: float
    net_income: float
    
    # Deductions
    pension_contribution: float
    nhf_contribution: float
    nhis_contribution: float
    life_insurance: float
    mortgage_interest: float
    charitable_donations: float
    rent_relief: float
    total_deductions: float
    
    # Tax Calculation
    taxable_income: float
    tax_free_allowance: float
    tax_band_breakdown: List[TaxBandBreakdown]
    total_tax_payable: float
    effective_tax_rate: float
    monthly_tax: float
    
    # Statistics
    internal_transfers_detected: int
    internal_transfers_amount: float
    categorized_transactions: int
    uncategorized_transactions: int
    
    # Status
    is_finalized: bool = False
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaxReportSummary(BaseModel):
    """Summary of tax report"""
    tax_year: int
    gross_income: float
    total_deductions: float
    taxable_income: float
    total_tax: float
    effective_rate: float
    status: str


class TaxReportList(BaseModel):
    """List of tax reports"""
    items: List[TaxReportSummary]
    total: int


class TaxReportExport(BaseModel):
    """Tax report export request"""
    report_id: int
    format: str = Field(default="pdf", pattern="^(pdf|csv|excel|json)$")
    include_transactions: bool = False
    include_breakdown: bool = True


class TaxCalculationPreview(BaseModel):
    """Preview of tax calculation"""
    gross_income: float
    deductions: dict
    taxable_income: float
    tax_breakdown: List[TaxBandBreakdown]
    total_tax: float
    monthly_tax: float
    effective_rate: float


class DeductionValidation(BaseModel):
    """Deduction validation request"""
    category: str
    amount: float
    description: Optional[str] = None
    
    @property
    def is_allowable(self) -> bool:
        """Check if deduction category is allowable"""
        allowable = [
            "pension", "nhf", "nhis", "life_insurance",
            "mortgage_interest", "charitable_donation", "rent_relief"
        ]
        return self.category.lower() in allowable


class AnnualTaxSummary(BaseModel):
    """Annual tax summary for dashboard"""
    tax_year: int
    monthly_income: List[float] = []
    monthly_tax: List[float] = []
    total_income: float
    total_tax: float
    average_monthly_tax: float
