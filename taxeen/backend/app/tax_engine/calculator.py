"""
Nigerian Personal Income Tax Calculator (2026)
Implements the latest Nigerian tax bands and relief allowances
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from enum import Enum


class TaxBand(Enum):
    """Nigerian tax bands for 2026"""
    BAND_1 = (0, 800_000, 0.00)          # 0 - 800,000: 0%
    BAND_2 = (800_000, 3_000_000, 0.15)  # 800,001 - 3,000,000: 15%
    BAND_3 = (3_000_000, 12_000_000, 0.18)  # 3,000,001 - 12,000,000: 18%
    BAND_4 = (12_000_000, 25_000_000, 0.21)  # 12,000,001 - 25,000,000: 21%
    BAND_5 = (25_000_000, 50_000_000, 0.23)  # 25,000,001 - 50,000,000: 23%
    BAND_6 = (50_000_000, float('inf'), 0.25)  # Above 50,000,000: 25%


@dataclass
class Deduction:
    """Represents a tax deduction"""
    name: str
    amount: Decimal
    is_percentage: bool = False
    percentage_of: Optional[str] = None  # e.g., "gross_income"
    cap: Optional[Decimal] = None


@dataclass
class TaxResult:
    """Result of tax calculation"""
    gross_income: Decimal
    total_deductions: Decimal
    chargeable_income: Decimal
    tax_payable: Decimal
    effective_rate: Decimal
    tax_bands: List[Dict]
    deductions_breakdown: List[Dict]
    rent_relief: Decimal


class NigerianTaxEngine:
    """
    Nigerian Personal Income Tax Calculator
    
    Implements the 2026 Nigerian tax rules:
    - Progressive tax bands
    - Rent relief allowance
    - Allowable deductions
    """
    
    TAX_BANDS = [
        {"min": 0, "max": 800_000, "rate": 0.00},
        {"min": 800_000, "max": 3_000_000, "rate": 0.15},
        {"min": 3_000_000, "max": 12_000_000, "rate": 0.18},
        {"min": 12_000_000, "max": 25_000_000, "rate": 0.21},
        {"min": 25_000_000, "max": 50_000_000, "rate": 0.23},
        {"min": 50_000_000, "max": float('inf'), "rate": 0.25},
    ]
    
    RENT_RELIEF_CAP = Decimal("500000")
    RENT_RELIEF_PERCENTAGE = Decimal("0.20")
    
    def __init__(self):
        self.deductions: List[Deduction] = []
    
    def add_deduction(
        self,
        name: str,
        amount: float,
        is_percentage: bool = False,
        percentage_of: Optional[str] = None,
        cap: Optional[float] = None
    ) -> None:
        """Add a deduction to the calculation"""
        self.deductions.append(Deduction(
            name=name,
            amount=Decimal(str(amount)),
            is_percentage=is_percentage,
            percentage_of=percentage_of,
            cap=Decimal(str(cap)) if cap else None
        ))
    
    def calculate_rent_relief(self, annual_rent: Decimal) -> Decimal:
        """
        Calculate rent relief allowance
        
        Rent relief = min(20% of annual rent, ₦500,000)
        """
        relief = annual_rent * self.RENT_RELIEF_PERCENTAGE
        return min(relief, self.RENT_RELIEF_CAP)
    
    def calculate_total_deductions(
        self,
        gross_income: Decimal,
        annual_rent: Decimal = Decimal("0"),
        pension_contribution: Decimal = Decimal("0"),
        nhf_contribution: Decimal = Decimal("0"),
        nhis_contribution: Decimal = Decimal("0"),
        life_insurance: Decimal = Decimal("0"),
        mortgage_interest: Decimal = Decimal("0"),
        charitable_donations: Decimal = Decimal("0")
    ) -> Tuple[Decimal, List[Dict]]:
        """
        Calculate total allowable deductions
        
        Returns:
            Tuple of (total_deductions, breakdown_list)
        """
        breakdown = []
        total = Decimal("0")
        
        # Rent relief
        rent_relief = self.calculate_rent_relief(annual_rent)
        if rent_relief > 0:
            breakdown.append({
                "name": "Rent Relief",
                "amount": float(rent_relief),
                "description": f"min(20% of ₦{annual_rent:,.2f}, ₦500,000)"
            })
            total += rent_relief
        
        # Pension contribution
        if pension_contribution > 0:
            breakdown.append({
                "name": "Pension Contribution",
                "amount": float(pension_contribution),
                "description": "Mandatory pension contribution"
            })
            total += pension_contribution
        
        # NHF contribution
        if nhf_contribution > 0:
            breakdown.append({
                "name": "NHF Contribution",
                "amount": float(nhf_contribution),
                "description": "National Housing Fund contribution"
            })
            total += nhf_contribution
        
        # NHIS contribution
        if nhis_contribution > 0:
            breakdown.append({
                "name": "NHIS Contribution",
                "amount": float(nhis_contribution),
                "description": "National Health Insurance Scheme"
            })
            total += nhis_contribution
        
        # Life insurance
        if life_insurance > 0:
            breakdown.append({
                "name": "Life Insurance Premium",
                "amount": float(life_insurance),
                "description": "Life insurance premium paid"
            })
            total += life_insurance
        
        # Mortgage interest
        if mortgage_interest > 0:
            breakdown.append({
                "name": "Mortgage Interest",
                "amount": float(mortgage_interest),
                "description": "Interest on mortgage for owner-occupied property"
            })
            total += mortgage_interest
        
        # Charitable donations
        if charitable_donations > 0:
            breakdown.append({
                "name": "Charitable Donations",
                "amount": float(charitable_donations),
                "description": "Donations to approved charitable organizations"
            })
            total += charitable_donations
        
        return total, breakdown
    
    def calculate_tax_for_band(self, taxable_income: Decimal) -> List[Dict]:
        """
        Calculate tax for each band based on taxable income
        
        Returns a list of dictionaries showing tax per band
        """
        bands_result = []
        remaining_income = taxable_income
        
        for i, band in enumerate(self.TAX_BANDS):
            band_min = Decimal(str(band["min"]))
            band_max = Decimal(str(band["max"]))
            rate = Decimal(str(band["rate"]))
            
            if remaining_income <= 0:
                break
            
            # Calculate the width of this band
            band_width = band_max - band_min
            
            # Calculate taxable amount in this band
            if remaining_income <= band_width:
                taxable_in_band = remaining_income
            else:
                taxable_in_band = band_width
            
            # Calculate tax for this band
            tax_in_band = taxable_in_band * rate
            
            if tax_in_band > 0 or taxable_in_band > 0:
                bands_result.append({
                    "band": f"₦{band_min:,.0f} - ₦{band_max:,.0f}" if band_max != float('inf') else f"Above ₦{band_min:,.0f}",
                    "rate": f"{float(rate) * 100:.0f}%",
                    "taxable_amount": float(taxable_in_band),
                    "tax": float(tax_in_band)
                })
            
            remaining_income -= taxable_in_band
        
        return bands_result
    
    def calculate(
        self,
        gross_income: float,
        annual_rent: float = 0,
        pension_contribution: float = 0,
        nhf_contribution: float = 0,
        nhis_contribution: float = 0,
        life_insurance: float = 0,
        mortgage_interest: float = 0,
        charitable_donations: float = 0
    ) -> TaxResult:
        """
        Calculate Nigerian Personal Income Tax
        
        Args:
            gross_income: Total annual income
            annual_rent: Annual rent paid
            pension_contribution: Pension contribution amount
            nhf_contribution: National Housing Fund contribution
            nhis_contribution: National Health Insurance Scheme contribution
            life_insurance: Life insurance premium
            mortgage_interest: Mortgage interest paid
            charitable_donations: Charitable donations made
            
        Returns:
            TaxResult with complete tax breakdown
        """
        gross = Decimal(str(gross_income))
        rent = Decimal(str(annual_rent))
        pension = Decimal(str(pension_contribution))
        nhf = Decimal(str(nhf_contribution))
        nhis = Decimal(str(nhis_contribution))
        insurance = Decimal(str(life_insurance))
        mortgage = Decimal(str(mortgage_interest))
        donations = Decimal(str(charitable_donations))
        
        # Calculate deductions
        total_deductions, deductions_breakdown = self.calculate_total_deductions(
            gross_income=gross,
            annual_rent=rent,
            pension_contribution=pension,
            nhf_contribution=nhf,
            nhis_contribution=nhis,
            life_insurance=insurance,
            mortgage_interest=mortgage,
            charitable_donations=donations
        )
        
        # Calculate chargeable income
        chargeable_income = max(Decimal("0"), gross - total_deductions)
        
        # Calculate tax per band
        tax_bands = self.calculate_tax_for_band(chargeable_income)
        
        # Total tax payable
        tax_payable = sum(Decimal(str(band["tax"])) for band in tax_bands)
        
        # Effective tax rate
        effective_rate = Decimal("0")
        if gross > 0:
            effective_rate = (tax_payable / gross) * 100
        
        # Rent relief amount
        rent_relief = self.calculate_rent_relief(rent)
        
        return TaxResult(
            gross_income=gross,
            total_deductions=total_deductions,
            chargeable_income=chargeable_income,
            tax_payable=tax_payable,
            effective_rate=effective_rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            tax_bands=tax_bands,
            deductions_breakdown=deductions_breakdown,
            rent_relief=rent_relief
        )


def calculate_nigerian_tax(
    gross_income: float,
    annual_rent: float = 0,
    pension_contribution: float = 0,
    nhf_contribution: float = 0,
    nhis_contribution: float = 0,
    life_insurance: float = 0,
    mortgage_interest: float = 0,
    charitable_donations: float = 0
) -> Dict:
    """
    Convenience function to calculate Nigerian tax
    
    Returns a dictionary with all tax calculation details
    """
    engine = NigerianTaxEngine()
    result = engine.calculate(
        gross_income=gross_income,
        annual_rent=annual_rent,
        pension_contribution=pension_contribution,
        nhf_contribution=nhf_contribution,
        nhis_contribution=nhis_contribution,
        life_insurance=life_insurance,
        mortgage_interest=mortgage_interest,
        charitable_donations=charitable_donations
    )
    
    return {
        "gross_income": float(result.gross_income),
        "total_deductions": float(result.total_deductions),
        "chargeable_income": float(result.chargeable_income),
        "tax_payable": float(result.tax_payable),
        "effective_rate": float(result.effective_rate),
        "tax_bands": result.tax_bands,
        "deductions_breakdown": result.deductions_breakdown,
        "rent_relief": float(result.rent_relief)
    }


# Example usage
if __name__ == "__main__":
    # Example: Annual income of 8,500,000 with deductions
    result = calculate_nigerian_tax(
        gross_income=8_500_000,
        annual_rent=1_200_000,  # 1.2M annual rent
        pension_contribution=680_000,  # 8% of gross
        nhf_contribution=85_000,  # 1% of gross
        nhis_contribution=42_500,  # 0.5% of gross
    )
    
    print(f"Gross Income: ₦{result['gross_income']:,.2f}")
    print(f"Total Deductions: ₦{result['total_deductions']:,.2f}")
    print(f"Chargeable Income: ₦{result['chargeable_income']:,.2f}")
    print(f"Tax Payable: ₦{result['tax_payable']:,.2f}")
    print(f"Effective Rate: {result['effective_rate']:.2f}%")
    print("\nTax Bands:")
    for band in result['tax_bands']:
        print(f"  {band['band']}: {band['rate']} = ₦{band['tax']:,.2f}")
