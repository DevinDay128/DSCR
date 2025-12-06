"""
AI Rent and DSCR Calculator for Real Estate Investment Analysis

This module provides AI-powered estimation of rental income and
Debt Service Coverage Ratio (DSCR) for investment properties.
"""

import json
import math
from typing import Dict, Optional, Any


class AIRentDSCRCalculator:
    """
    Calculates estimated rent and DSCR for investment properties.

    This calculator provides rough estimates based on general market patterns
    and is NOT a substitute for professional underwriting or appraisal.
    """

    def __init__(self):
        self.mode = "ai_rent_and_dscr"

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
        operating_expense_ratio: Optional[float] = None,
        property_type: Optional[str] = None,
        beds: Optional[int] = None,
        baths: Optional[float] = None,
        sqft: Optional[int] = None,
        condition: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate estimated rent and DSCR for a property.

        Args:
            address: Property address
            purchase_price: Purchase price in USD
            down_payment_amount: Down payment in USD (optional)
            down_payment_percent: Down payment as decimal (e.g., 0.20 for 20%)
            interest_rate_annual: Annual interest rate as decimal (e.g., 0.07 for 7%)
            term_years: Loan term in years
            interest_only: Whether loan is interest-only
            vacancy_rate: Vacancy rate as decimal (default 0.0)
            operating_expense_ratio: Operating expense ratio as decimal
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

        # Step 3: Calculate operating expense ratio
        if operating_expense_ratio is None:
            operating_expense_ratio = 0.35  # Default 35%

        # Step 4: Calculate effective gross income (with vacancy)
        effective_gross_income_monthly = estimated_monthly_rent * (1 - vacancy_rate)

        # Step 5: Calculate operating expenses
        # Per requirements: estimate insurance at $150/month
        insurance_monthly = 150
        base_operating_expenses = effective_gross_income_monthly * operating_expense_ratio
        operating_expenses_monthly = base_operating_expenses + insurance_monthly

        # Step 6: Calculate NOI
        NOI_monthly = effective_gross_income_monthly - operating_expenses_monthly
        NOI_annual = NOI_monthly * 12

        # Step 7: Calculate debt service
        monthly_debt_service = self._calculate_debt_service(
            loan_amount=loan_amount,
            interest_rate_annual=interest_rate_annual,
            term_years=term_years,
            interest_only=interest_only
        )
        annual_debt_service = monthly_debt_service * 12

        # Step 8: Calculate DSCR
        if annual_debt_service > 0:
            DSCR = NOI_annual / annual_debt_service
        else:
            DSCR = 0

        # Step 9: Determine risk label
        risk_label = self._get_risk_label(DSCR)

        # Step 10: Calculate monthly cashflow
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
        return {
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
            "operating_expense_ratio": operating_expense_ratio,

            "effective_gross_income_monthly": effective_gross_income_monthly,
            "operating_expenses_monthly": operating_expenses_monthly,
            "NOI_annual": NOI_annual,

            "monthly_debt_service": monthly_debt_service,
            "annual_debt_service": annual_debt_service,
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
        Estimate monthly market rent for the property.

        This uses general patterns based on purchase price and property characteristics.
        NOT based on live MLS, Zillow, or any paid data source.
        """

        assumptions_list = []
        confidence = 0.6  # Start with moderate confidence

        # Base estimate using 1% rule as starting point, then adjust
        # The 1% rule suggests monthly rent = 1% of purchase price
        base_estimate = purchase_price * 0.01

        # Adjust based on price tier (lower priced properties often exceed 1%, higher priced are below)
        if purchase_price < 100000:
            rent_multiplier = 0.012  # 1.2%
            confidence = 0.5
            assumptions_list.append("Low purchase price - using higher rent multiplier")
        elif purchase_price < 250000:
            rent_multiplier = 0.01  # 1.0%
            confidence = 0.65
        elif purchase_price < 500000:
            rent_multiplier = 0.0085  # 0.85%
            confidence = 0.7
        elif purchase_price < 1000000:
            rent_multiplier = 0.007  # 0.7%
            confidence = 0.6
        else:
            rent_multiplier = 0.006  # 0.6%
            confidence = 0.5
            assumptions_list.append("High purchase price - using lower rent multiplier")

        estimated_rent = purchase_price * rent_multiplier

        # Adjust based on property type if provided
        if property_type:
            if property_type.upper() in ['CONDO', 'TOWNHOUSE']:
                estimated_rent *= 0.95
                assumptions_list.append(f"Adjusted for {property_type} (typically -5%)")
            elif property_type.upper() in ['MULTI-FAMILY', 'DUPLEX', 'TRIPLEX']:
                assumptions_list.append(f"Multi-family property - estimate is per unit average")
                confidence *= 0.9
        else:
            assumptions_list.append("Property type not specified - assuming single-family residence")
            confidence *= 0.95

        # Adjust based on bedrooms if provided
        if beds is not None:
            if beds == 1:
                assumptions_list.append("1 bedroom property")
                confidence *= 0.9
            elif beds >= 5:
                assumptions_list.append(f"{beds} bedrooms - larger property")
                confidence *= 0.85
        else:
            assumptions_list.append("Number of bedrooms not specified - assuming 3 bedrooms")
            confidence *= 0.9

        # Note baths if provided
        if baths is not None:
            assumptions_list.append(f"Property has {baths} bathrooms")
        else:
            assumptions_list.append("Number of bathrooms not specified - assuming 2 bathrooms")
            confidence *= 0.9

        # Note square footage if provided
        if sqft is not None:
            assumptions_list.append(f"Property is {sqft} square feet")
            # Sanity check on price per sqft
            price_per_sqft = purchase_price / sqft
            if price_per_sqft < 50:
                assumptions_list.append("Low price per sqft - may be in low-cost area or needs work")
                confidence *= 0.8
            elif price_per_sqft > 500:
                assumptions_list.append("High price per sqft - may be in premium area")
                confidence *= 0.85
        else:
            assumptions_list.append("Square footage not specified")
            confidence *= 0.9

        # Adjust based on condition if provided
        if condition:
            condition_lower = condition.lower()
            if 'excellent' in condition_lower or 'updated' in condition_lower or 'renovated' in condition_lower:
                estimated_rent *= 1.1
                assumptions_list.append("Good condition - increased rent estimate by 10%")
            elif 'poor' in condition_lower or 'fixer' in condition_lower or 'needs work' in condition_lower:
                estimated_rent *= 0.85
                assumptions_list.append("Poor condition - decreased rent estimate by 15%")
                confidence *= 0.8
        else:
            assumptions_list.append("Property condition not specified - assuming average condition")
            confidence *= 0.95

        # Parse location from address for regional adjustments
        address_upper = address.upper()

        # High-cost metros (rough heuristic)
        high_cost_cities = ['SAN FRANCISCO', 'NEW YORK', 'BOSTON', 'SEATTLE', 'LOS ANGELES',
                           'SAN JOSE', 'WASHINGTON DC', 'OAKLAND', 'MANHATTAN']
        if any(city in address_upper for city in high_cost_cities):
            assumptions_list.append("High-cost metro area detected")
            confidence *= 0.85  # Lower confidence due to high variability

        # Create range (±15%)
        low_estimate = estimated_rent * 0.85
        high_estimate = estimated_rent * 1.15

        # Cap confidence at 0.75 (never claim high confidence for AI estimates)
        confidence = min(confidence, 0.75)

        assumptions_text = "; ".join(assumptions_list) if assumptions_list else "Using general market patterns only"

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
        notes.append("Operating expense ratio of 35% is an estimate - verify actual costs for this property.")
        notes.append("Insurance estimate of $150/month is generic - get actual quote for this property.")

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
