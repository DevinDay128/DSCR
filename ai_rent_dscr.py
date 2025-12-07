"""
AI Rent and DSCR Calculator for Real Estate Investment Analysis

This module provides AI-powered estimation of rental income and
Debt Service Coverage Ratio (DSCR) for investment properties.
"""

import json
import math
from typing import Dict, Optional, Any
from sc_tax_calculator import SCTaxCalculator


class AIRentDSCRCalculator:
    """
    Calculates estimated rent and DSCR for investment properties.

    This calculator provides rough estimates based on general market patterns
    and is NOT a substitute for professional underwriting or appraisal.
    """

    def __init__(self):
        self.mode = "ai_rent_and_dscr"
        self.sc_tax_calculator = SCTaxCalculator()

    def calculate(
        self,
        address: str,
        purchase_price: float,
        down_payment_amount: Optional[float] = None,
        down_payment_percent: Optional[float] = None,
        interest_rate_annual: float = 0.07,
        term_years: int = 30,
        interest_only: bool = False,
        vacancy_rate: float = 0.0,  # Per requirements: 0% vacancy
        property_tax_rate: Optional[float] = None,  # Annual tax rate (e.g., 0.012 for 1.2%)
        insurance_monthly: Optional[float] = None,  # Monthly insurance cost
        property_type: Optional[str] = None,
        beds: Optional[int] = None,
        baths: Optional[float] = None,
        sqft: Optional[int] = None,
        condition: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate estimated rent and DSCR for a property.

        Expenses calculated: Principal & Interest (P&I), Property Taxes, Insurance only.

        Args:
            address: Property address
            purchase_price: Purchase price in USD
            down_payment_amount: Down payment in USD (optional)
            down_payment_percent: Down payment as decimal (e.g., 0.20 for 20%)
            interest_rate_annual: Annual interest rate as decimal (e.g., 0.07 for 7%)
            term_years: Loan term in years
            interest_only: Whether loan is interest-only
            vacancy_rate: Vacancy rate as decimal (default 0.0)
            property_tax_rate: Annual property tax rate as decimal (default 0.012 for 1.2%)
            insurance_monthly: Monthly insurance cost in USD (default 150)
            property_type: Type of property (SFR, condo, etc.)
            beds: Number of bedrooms
            baths: Number of bathrooms
            sqft: Square footage
            condition: Property condition

        Returns:
            Dictionary with all calculated values and estimates
        """

        # Step 1: Calculate loan amount
        loan_amount, down_payment_amount_final, down_payment_percent_final = \
            self._calculate_loan_amount(
                purchase_price,
                down_payment_amount,
                down_payment_percent
            )

        # Step 2: Estimate rent
        rent_estimates = self._estimate_rent(
            address=address,
            purchase_price=purchase_price,
            property_type=property_type,
            beds=beds,
            baths=baths,
            sqft=sqft,
            condition=condition
        )

        estimated_monthly_rent = rent_estimates['estimated']
        low_estimate_rent = rent_estimates['low']
        high_estimate_rent = rent_estimates['high']
        confidence_score = rent_estimates['confidence']
        assumptions = rent_estimates['assumptions']

        # Step 2.5: Check if this is a South Carolina property and use deterministic tax calculation
        sc_tax_result = self.sc_tax_calculator.calculate_sc_rental_tax(
            address=address,
            property_value=purchase_price
        )

        # Store SC tax information
        is_sc_property = sc_tax_result['tax_accuracy'] == 'ok'
        sc_tax_info = sc_tax_result if is_sc_property else None

        # Step 3: Calculate property taxes
        if is_sc_property:
            # Use SC deterministic tax calculation
            property_tax_rate = None  # Not applicable for SC (uses millage instead)
            property_tax_annual = sc_tax_result['annual_taxes']
            property_tax_monthly = sc_tax_result['monthly_taxes']
        else:
            # Use standard tax calculation for non-SC properties
            if property_tax_rate is None:
                property_tax_rate = 0.012  # Default 1.2% annually (US average)

            property_tax_annual = purchase_price * property_tax_rate
            property_tax_monthly = property_tax_annual / 12

        # Step 4: Set insurance
        if insurance_monthly is None:
            insurance_monthly = 150  # Default $150/month

        # Step 5: Calculate effective gross income (with vacancy)
        effective_gross_income_monthly = estimated_monthly_rent * (1 - vacancy_rate)

        # Step 6: Calculate total monthly expenses (Taxes + Insurance only)
        # Note: P&I (debt service) is calculated separately and NOT included in operating expenses
        monthly_operating_expenses = property_tax_monthly + insurance_monthly

        # Step 7: Calculate NOI (Net Operating Income)
        # NOI = Income - Operating Expenses (does NOT subtract debt service)
        NOI_monthly = effective_gross_income_monthly - monthly_operating_expenses
        NOI_annual = NOI_monthly * 12

        # Step 8: Calculate debt service (P&I)
        monthly_debt_service = self._calculate_debt_service(
            loan_amount=loan_amount,
            interest_rate_annual=interest_rate_annual,
            term_years=term_years,
            interest_only=interest_only
        )
        annual_debt_service = monthly_debt_service * 12

        # Step 9: Calculate DSCR
        # DSCR = NOI / Annual Debt Service
        if annual_debt_service > 0:
            DSCR = NOI_annual / annual_debt_service
        else:
            DSCR = 0

        # Step 10: Determine risk label
        risk_label = self._get_risk_label(DSCR)

        # Step 11: Calculate monthly cashflow
        # Cashflow = Rent - Taxes - Insurance - P&I
        monthly_cashflow = NOI_monthly - monthly_debt_service

        # Step 11: Generate summaries
        inputs_summary = self._generate_inputs_summary(
            address=address,
            purchase_price=purchase_price,
            down_payment_percent=down_payment_percent_final,
            interest_rate_annual=interest_rate_annual,
            term_years=term_years
        )

        human_summary = self._generate_human_summary(
            address=address,
            estimated_monthly_rent=estimated_monthly_rent,
            DSCR=DSCR,
            monthly_cashflow=monthly_cashflow,
            risk_label=risk_label
        )

        notes_for_investor = self._generate_investor_notes(
            DSCR=DSCR,
            monthly_cashflow=monthly_cashflow,
            confidence_score=confidence_score
        )

        disclaimer = (
            "IMPORTANT: This is a rough AI-powered estimate based on general market "
            "patterns and assumptions. It is NOT a substitute for professional property "
            "appraisal, rental market analysis, or underwriting. Actual rental income may "
            "vary significantly based on specific property features, local market conditions, "
            "property management, and numerous other factors. Do NOT make investment decisions "
            "based solely on this estimate. Always conduct thorough due diligence including "
            "professional inspections, appraisals, and market research."
        )

        # Return complete result
        result = {
            "mode": self.mode,

            "address": address,
            "purchase_price": purchase_price,
            "down_payment_amount": down_payment_amount_final,
            "down_payment_percent": down_payment_percent_final,
            "loan_amount": loan_amount,
            "interest_rate_annual": interest_rate_annual,
            "term_years": term_years,
            "interest_only": interest_only,

            "estimated_monthly_rent": estimated_monthly_rent,
            "low_estimate_rent": low_estimate_rent,
            "high_estimate_rent": high_estimate_rent,
            "vacancy_rate": vacancy_rate,

            # Expense breakdown
            "property_tax_rate": property_tax_rate,
            "property_tax_monthly": property_tax_monthly,
            "property_tax_annual": property_tax_annual,
            "insurance_monthly": insurance_monthly,
            "insurance_annual": insurance_monthly * 12,

            "effective_gross_income_monthly": effective_gross_income_monthly,
            "monthly_operating_expenses": monthly_operating_expenses,
            "NOI_monthly": NOI_monthly,
            "NOI_annual": NOI_annual,

            # Debt service (P&I)
            "monthly_debt_service": monthly_debt_service,
            "annual_debt_service": annual_debt_service,

            # Results
            "DSCR": DSCR,
            "risk_label": risk_label,
            "monthly_cashflow": monthly_cashflow,

            "inputs_summary": inputs_summary,
            "human_summary": human_summary,

            "confidence_score": confidence_score,
            "assumptions": assumptions,
            "notes_for_investor": notes_for_investor,
            "disclaimer": disclaimer
        }

        # Add SC tax information if this is a SC property
        if is_sc_property:
            result["sc_tax_info"] = sc_tax_info

        return result

    def _calculate_loan_amount(
        self,
        purchase_price: float,
        down_payment_amount: Optional[float],
        down_payment_percent: Optional[float]
    ) -> tuple:
        """Calculate loan amount from purchase price and down payment."""

        if down_payment_amount is not None and down_payment_amount > 0:
            loan_amount = purchase_price - down_payment_amount
            down_payment_percent_final = down_payment_amount / purchase_price
            down_payment_amount_final = down_payment_amount
        elif down_payment_percent is not None and down_payment_percent > 0:
            down_payment_amount_final = purchase_price * down_payment_percent
            loan_amount = purchase_price - down_payment_amount_final
            down_payment_percent_final = down_payment_percent
        else:
            # Default to 20% down
            down_payment_percent_final = 0.20
            down_payment_amount_final = purchase_price * 0.20
            loan_amount = purchase_price - down_payment_amount_final

        return loan_amount, down_payment_amount_final, down_payment_percent_final

    def _calculate_debt_service(
        self,
        loan_amount: float,
        interest_rate_annual: float,
        term_years: int,
        interest_only: bool
    ) -> float:
        """Calculate monthly debt service."""

        if loan_amount <= 0:
            return 0

        if interest_only:
            # Interest-only payment
            monthly_debt_service = loan_amount * (interest_rate_annual / 12)
        else:
            # Fully amortized loan
            r = interest_rate_annual / 12
            n = term_years * 12

            if r == 0:
                # No interest case (unrealistic but handle it)
                monthly_debt_service = loan_amount / n
            else:
                # Standard amortization formula
                monthly_debt_service = loan_amount * (r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)

        return monthly_debt_service

    def _estimate_rent(
        self,
        address: str,
        purchase_price: float,
        property_type: Optional[str],
        beds: Optional[int],
        baths: Optional[float],
        sqft: Optional[int],
        condition: Optional[str]
    ) -> Dict[str, Any]:
        """
        Estimate monthly market rent for the property using yield-based formula.

        Formula:
        1. Price-based: Rent_price = PurchasePrice × 0.0085 (0.85% monthly yield)
        2. SqFt-based: Rent_sqft = SqFt × $1.40/sqft (if available)
        3. BaseRent = average of both, or just price-based if no sqft
        4. Apply adjustment factor (0.85 to 1.15) based on property characteristics
        5. Range = ±10% of estimated rent
        """

        assumptions_list = []
        confidence = 0.70  # Start with good confidence for formula-based approach

        # Constants
        YIELD_LOCAL = 0.0085  # 0.85% monthly yield
        RENT_PER_SQFT_LOCAL = 1.40  # $1.40 per square foot

        # Step 1: Price-based estimate
        rent_price = purchase_price * YIELD_LOCAL
        assumptions_list.append(f"Price-based estimate: ${rent_price:,.0f} (0.85% monthly yield)")

        # Step 2: SqFt-based estimate (if available)
        if sqft is not None and sqft > 0:
            rent_sqft = sqft * RENT_PER_SQFT_LOCAL
            base_rent = (rent_price + rent_sqft) / 2
            assumptions_list.append(f"SqFt-based estimate: ${rent_sqft:,.0f} ({sqft} sqft × ${RENT_PER_SQFT_LOCAL}/sqft)")
            assumptions_list.append(f"Base rent: ${base_rent:,.0f} (average of both methods)")
        else:
            base_rent = rent_price
            assumptions_list.append("Square footage not provided - using price-based estimate only")
            confidence *= 0.95

        # Step 3: Calculate adjustment factor (bounded to ±15%)
        adjustment_factor = 1.0  # Start at neutral
        adjustment_reasons = []

        # Adjust for property type
        if property_type:
            if property_type.upper() in ['CONDO', 'TOWNHOUSE']:
                adjustment_factor *= 0.97  # -3%
                adjustment_reasons.append(f"{property_type} (-3%)")
            elif property_type.upper() in ['MULTI-FAMILY', 'DUPLEX', 'TRIPLEX']:
                adjustment_reasons.append(f"{property_type} (per unit estimate)")
                confidence *= 0.90
        else:
            assumptions_list.append("Property type not specified - assuming single-family")
            confidence *= 0.95

        # Adjust for condition
        if condition:
            condition_lower = condition.lower()
            if 'excellent' in condition_lower or 'updated' in condition_lower or 'renovated' in condition_lower:
                adjustment_factor *= 1.08  # +8%
                adjustment_reasons.append("Excellent condition (+8%)")
            elif 'good' in condition_lower:
                adjustment_factor *= 1.03  # +3%
                adjustment_reasons.append("Good condition (+3%)")
            elif 'poor' in condition_lower or 'fixer' in condition_lower or 'needs work' in condition_lower:
                adjustment_factor *= 0.90  # -10%
                adjustment_reasons.append("Poor condition (-10%)")
                confidence *= 0.85
            elif 'fair' in condition_lower or 'average' in condition_lower:
                # No adjustment for average condition
                adjustment_reasons.append("Average condition (no adjustment)")
        else:
            assumptions_list.append("Condition not specified - assuming average")
            confidence *= 0.95

        # Adjust for location (high-cost metros)
        address_upper = address.upper()
        high_cost_cities = ['SAN FRANCISCO', 'NEW YORK', 'BOSTON', 'SEATTLE', 'LOS ANGELES',
                           'SAN JOSE', 'WASHINGTON DC', 'OAKLAND', 'MANHATTAN', 'MIAMI']
        if any(city in address_upper for city in high_cost_cities):
            adjustment_factor *= 1.05  # +5% for high-cost metros
            adjustment_reasons.append("High-cost metro area (+5%)")
            confidence *= 0.90  # Lower confidence due to variability

        # Adjust for bedrooms (if unusual size)
        if beds is not None:
            if beds == 1:
                adjustment_factor *= 0.95  # -5% for studio/1-bed
                adjustment_reasons.append("1 bedroom (-5%)")
            elif beds >= 5:
                adjustment_factor *= 1.03  # +3% for large properties
                adjustment_reasons.append(f"{beds} bedrooms (+3%)")
            else:
                assumptions_list.append(f"{beds} bedrooms (typical size)")
        else:
            assumptions_list.append("Bedrooms not specified - assuming 3 bedrooms")
            confidence *= 0.92

        # Note bathrooms
        if baths is not None:
            assumptions_list.append(f"{baths} bathrooms")
        else:
            assumptions_list.append("Bathrooms not specified")
            confidence *= 0.95

        # Sanity check: bound adjustment factor to ±15% (0.85 to 1.15)
        adjustment_factor = max(0.85, min(1.15, adjustment_factor))

        # Step 4: Apply adjustment factor
        estimated_rent = base_rent * adjustment_factor

        if adjustment_reasons:
            assumptions_list.append(f"Adjustments applied: {', '.join(adjustment_reasons)}")
            assumptions_list.append(f"Final adjustment factor: {adjustment_factor:.2f}x")

        # Step 5: Create range (±10%)
        low_estimate = estimated_rent * 0.90
        high_estimate = estimated_rent * 1.10

        # Cap confidence at 0.75 (never claim high confidence for AI estimates)
        confidence = min(confidence, 0.75)

        assumptions_text = "; ".join(assumptions_list) if assumptions_list else "Using formula-based estimation"

        return {
            'estimated': round(estimated_rent, 2),
            'low': round(low_estimate, 2),
            'high': round(high_estimate, 2),
            'confidence': round(confidence, 2),
            'assumptions': assumptions_text
        }

    def _get_risk_label(self, DSCR: float) -> str:
        """Determine risk label based on DSCR."""
        if DSCR >= 1.30:
            return "Strong"
        elif DSCR >= 1.10:
            return "Borderline"
        else:
            return "Weak"

    def _generate_inputs_summary(
        self,
        address: str,
        purchase_price: float,
        down_payment_percent: float,
        interest_rate_annual: float,
        term_years: int
    ) -> str:
        """Generate human-readable inputs summary."""
        return (
            f"{address} | ${purchase_price:,.0f} purchase | "
            f"{down_payment_percent*100:.0f}% down | "
            f"{interest_rate_annual*100:.2f}% rate | {term_years}yr term"
        )

    def _generate_human_summary(
        self,
        address: str,
        estimated_monthly_rent: float,
        DSCR: float,
        monthly_cashflow: float,
        risk_label: str
    ) -> str:
        """Generate human-readable summary for investor."""
        cashflow_text = f"${abs(monthly_cashflow):,.0f}/month {'positive' if monthly_cashflow >= 0 else 'negative'} cashflow"

        summary = (
            f"For {address}, estimated market rent is ${estimated_monthly_rent:,.0f}/month. "
            f"With the given loan terms and operating assumptions, the property shows a DSCR of {DSCR:.2f} "
            f"({risk_label} rating) with {cashflow_text}. "
        )

        if DSCR >= 1.30:
            summary += "This indicates strong debt coverage with healthy margin for unexpected expenses."
        elif DSCR >= 1.10:
            summary += "This indicates borderline debt coverage - carefully verify rent estimates and expenses."
        else:
            summary += "This indicates weak debt coverage - property may have negative cashflow or tight margins."

        return summary

    def _generate_investor_notes(
        self,
        DSCR: float,
        monthly_cashflow: float,
        confidence_score: float
    ) -> str:
        """Generate notes and warnings for investor."""
        notes = []

        if confidence_score < 0.6:
            notes.append("LOW CONFIDENCE in rent estimate due to limited property information.")

        if DSCR < 1.10:
            notes.append("CAUTION: DSCR below 1.10 indicates property may not generate sufficient income to cover debt.")

        if monthly_cashflow < 0:
            notes.append("WARNING: Projected negative monthly cashflow. Property would require ongoing capital contributions.")
        elif monthly_cashflow < 200:
            notes.append("Tight cashflow margins - ensure reserve funds for repairs and vacancies.")

        notes.append("Verify actual rents with local property managers or recent comparable leases.")
        notes.append("Consider getting professional appraisal and rent study before proceeding.")
        notes.append("Property tax estimate is based on purchase price - verify actual tax rate for this location.")
        notes.append("Insurance estimate may vary - get actual quote for this specific property.")
        notes.append("This calculation includes only P&I, Taxes, and Insurance. Additional expenses (maintenance, HOA, property management, etc.) will reduce actual cashflow.")

        return " ".join(notes)


def calculate_ai_rent_dscr(params: Dict[str, Any]) -> str:
    """
    Main entry point for AI Rent and DSCR calculation.

    Args:
        params: Dictionary of input parameters

    Returns:
        JSON string with calculation results
    """
    calculator = AIRentDSCRCalculator()
    result = calculator.calculate(**params)
    return json.dumps(result, indent=2)


def calculate_ai_rent_dscr_dict(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for AI Rent and DSCR calculation (returns dict).

    Args:
        params: Dictionary of input parameters

    Returns:
        Dictionary with calculation results
    """
    calculator = AIRentDSCRCalculator()
    return calculator.calculate(**params)


if __name__ == "__main__":
    # Example usage
    example_params = {
        "address": "123 Main St, Austin, TX 78701",
        "purchase_price": 400000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.07,
        "term_years": 30,
        "interest_only": False,
        "property_type": "SFR",
        "beds": 3,
        "baths": 2,
        "sqft": 1800,
        "condition": "Good"
    }

    result = calculate_ai_rent_dscr(example_params)
    print(result)
