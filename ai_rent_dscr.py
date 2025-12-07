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
        property_tax_rate: Optional[float] = None,  # Annual tax rate (e.g., 0.012 for 1.2%)
        insurance_monthly: Optional[float] = None,  # Monthly insurance cost
        property_type: Optional[str] = None,
        beds: Optional[int] = None,
        baths: Optional[float] = None,
        sqft: Optional[int] = None,
        condition: Optional[str] = None,
        mls_description: Optional[str] = None,  # MLS listing description for fact-checking
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
            condition=condition,
            mls_description=mls_description
        )

        estimated_monthly_rent = rent_estimates['estimated']
        low_estimate_rent = rent_estimates['low']
        high_estimate_rent = rent_estimates['high']
        confidence_score = rent_estimates['confidence']
        assumptions = rent_estimates['assumptions']

        # Step 3: Calculate property taxes
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
        condition: Optional[str],
        mls_description: Optional[str]
    ) -> Dict[str, Any]:
        """
        Estimate monthly market rent using the new multi-step formula:

        STEP 1: Price-based rent estimate
        STEP 2: SqFt-based rent estimate (if available) and calculate BaseRent
        STEP 3: Personalization Adjustments (capped at ±25%)
        STEP 4: LLM Adjustment (general correction, capped at ±15%)
        STEP 5: Combine adjustments with total cap at ±25%
        """

        assumptions_list = []
        personalization_details = []
        confidence = 0.70  # Start with good confidence for formula-based approach

        # ========== CONSTANTS (MANDATORY — NEVER CHANGE) ==========
        YIELD_LOCAL = 0.0085  # 0.85% monthly yield
        RENT_PER_SQFT_LOCAL = 1.40  # $1.40 per square foot
        PERSONALIZATION_CAP = 0.25  # ±25%
        LLM_ADJUSTMENT_CAP = 0.15  # ±15%
        TOTAL_ADJUSTMENT_CAP = 0.25  # ±25%
        LOW_RENT_MULTIPLIER = 0.90  # 90% for low estimate
        HIGH_RENT_MULTIPLIER = 1.10  # 110% for high estimate

        # ========== STEP 1: Price-based rent estimate ==========
        rent_price = purchase_price * YIELD_LOCAL
        assumptions_list.append(f"Price-based estimate: ${rent_price:,.0f} (0.85% monthly yield)")

        # ========== STEP 2: SqFt-based rent estimate and BaseRent ==========
        if sqft is not None and sqft > 0:
            rent_sqft = sqft * RENT_PER_SQFT_LOCAL
            base_rent = (rent_price + rent_sqft) / 2
            assumptions_list.append(f"SqFt-based estimate: ${rent_sqft:,.0f} ({sqft} sqft × ${RENT_PER_SQFT_LOCAL}/sqft)")
            assumptions_list.append(f"Base rent: ${base_rent:,.0f} (average of both methods)")
        else:
            base_rent = rent_price
            assumptions_list.append("Square footage not provided - using price-based estimate only")
            confidence *= 0.95

        # ========== STEP 3: Personalization Adjustments ==========
        # Fact-check property features from MLS description
        fact_checked = self._fact_check_property(address, mls_description, beds, baths, condition)

        total_personalization_percent = 0.0

        # 3.1 Condition adjustment
        condition_to_use = fact_checked.get('condition') or condition
        if condition_to_use:
            condition_lower = condition_to_use.lower()
            if 'premium' in condition_lower or 'renovated' in condition_lower or 'updated' in condition_lower:
                adjustment = 0.15  # +15% (mid-range of 12-18%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Premium/renovated condition: +{adjustment*100:.0f}%")
            elif 'excellent' in condition_lower or 'above average' in condition_lower:
                adjustment = 0.08  # +8% (mid-range of 6-10%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Above average condition: +{adjustment*100:.0f}%")
            elif 'good' in condition_lower or 'average' in condition_lower:
                personalization_details.append("Average condition: 0%")
            elif 'below average' in condition_lower or 'fair' in condition_lower:
                adjustment = -0.09  # -9% (mid-range of -6 to -12%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Below average condition: {adjustment*100:.0f}%")
            elif 'poor' in condition_lower or 'fixer' in condition_lower or 'needs work' in condition_lower:
                adjustment = -0.18  # -18% (mid-range of -12 to -25%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Needs work: {adjustment*100:.0f}%")
                confidence *= 0.85
        else:
            assumptions_list.append("Condition not specified - assuming average (0%)")
            confidence *= 0.95

        # 3.2 School district quality
        if fact_checked.get('school_quality'):
            school_quality = fact_checked['school_quality']
            if school_quality == 'excellent':
                adjustment = 0.075  # +7.5% (mid-range of 5-10%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Excellent school district: +{adjustment*100:.1f}%")
            elif school_quality == 'good':
                adjustment = 0.04  # +4% (mid-range of 3-5%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Good school district: +{adjustment*100:.0f}%")
            elif school_quality == 'poor':
                adjustment = -0.075  # -7.5% (mid-range of -5 to -10%)
                total_personalization_percent += adjustment
                personalization_details.append(f"Poor school district: {adjustment*100:.1f}%")

        # 3.3 Location desirability
        if fact_checked.get('near_beach'):
            adjustment = 0.12  # +12% (mid-range of 8-15%)
            total_personalization_percent += adjustment
            personalization_details.append(f"Near beach/coast: +{adjustment*100:.0f}%")
        if fact_checked.get('near_major_employer'):
            adjustment = 0.10  # +10% (mid-range of 8-15%)
            total_personalization_percent += adjustment
            personalization_details.append(f"Near major employer: +{adjustment*100:.0f}%")
        if fact_checked.get('rural_low_demand'):
            adjustment = -0.075  # -7.5% (mid-range of -5 to -10%)
            total_personalization_percent += adjustment
            personalization_details.append(f"Rural/low demand area: {adjustment*100:.1f}%")

        # 3.4 Amenities
        if fact_checked.get('has_pool') or fact_checked.get('has_gym') or fact_checked.get('gated_community'):
            amenities = []
            if fact_checked.get('has_pool'):
                amenities.append('pool')
            if fact_checked.get('has_gym'):
                amenities.append('gym')
            if fact_checked.get('gated_community'):
                amenities.append('gated community')
            adjustment = 0.055  # +5.5% (mid-range of 3-8%)
            total_personalization_percent += adjustment
            personalization_details.append(f"Premium amenities ({', '.join(amenities)}): +{adjustment*100:.1f}%")

        # 3.5 Bedrooms/bathrooms
        if beds is not None:
            if beds >= 4:
                adjustment = 0.125  # +12.5% (mid-range of 10-15%)
                total_personalization_percent += adjustment
                personalization_details.append(f"4+ bedrooms: +{adjustment*100:.1f}%")
            elif beds == 1:
                # Note: This is separate from the 4BR premium
                pass  # No specific adjustment mentioned in new formulas
            else:
                assumptions_list.append(f"{beds} bedrooms (typical size)")
        else:
            assumptions_list.append("Bedrooms not specified - assuming 3 bedrooms")
            confidence *= 0.92

        if baths is not None and baths >= 2:
            adjustment = 0.075  # +7.5% (mid-range of 5-10%)
            total_personalization_percent += adjustment
            personalization_details.append(f"2+ bathrooms: +{adjustment*100:.1f}%")
        elif baths is not None:
            assumptions_list.append(f"{baths} bathrooms")
        else:
            assumptions_list.append("Bathrooms not specified")
            confidence *= 0.95

        # 3.6 Yard/lot
        if fact_checked.get('has_fenced_yard') or fact_checked.get('large_yard'):
            adjustment = 0.05  # +5%
            total_personalization_percent += adjustment
            personalization_details.append("Fenced/large yard: +5%")
        elif fact_checked.get('no_yard'):
            adjustment = -0.05  # -5%
            total_personalization_percent += adjustment
            personalization_details.append("Small/no yard: -5%")

        # 3.7 Parking
        if fact_checked.get('two_car_garage'):
            adjustment = 0.07  # +7%
            total_personalization_percent += adjustment
            personalization_details.append("Two-car garage: +7%")
        elif fact_checked.get('garage'):
            adjustment = 0.05  # +5%
            total_personalization_percent += adjustment
            personalization_details.append("Garage: +5%")
        elif fact_checked.get('no_parking'):
            adjustment = -0.08  # -8%
            total_personalization_percent += adjustment
            personalization_details.append("No parking: -8%")

        # Clamp total personalization to ±25%
        total_personalization_percent = max(-PERSONALIZATION_CAP, min(PERSONALIZATION_CAP, total_personalization_percent))
        personalization_factor = 1 + total_personalization_percent

        if personalization_details:
            assumptions_list.append(f"Personalization adjustments: {'; '.join(personalization_details)}")
            assumptions_list.append(f"Total personalization: {total_personalization_percent*100:+.1f}% (capped at ±25%)")

        # ========== STEP 4: LLM Adjustment ==========
        # General intuition-based correction (you would use LLM analysis here)
        # For now, we'll use a simple heuristic based on overall property profile
        llm_adjustment_factor = 1.0
        llm_adjustment_reasons = []

        # Example LLM-style adjustments (in practice, this would be AI-driven)
        if property_type:
            if property_type.upper() in ['CONDO', 'TOWNHOUSE']:
                llm_adjustment_factor *= 0.98  # -2% general adjustment
                llm_adjustment_reasons.append(f"{property_type} market adjustment: -2%")
            elif property_type.upper() in ['MULTI-FAMILY', 'DUPLEX', 'TRIPLEX']:
                llm_adjustment_reasons.append(f"{property_type} (per unit estimate)")
                confidence *= 0.90

        # Clamp LLM adjustment to ±15%
        llm_adjustment_factor = max(1 - LLM_ADJUSTMENT_CAP, min(1 + LLM_ADJUSTMENT_CAP, llm_adjustment_factor))

        if llm_adjustment_reasons:
            assumptions_list.append(f"LLM adjustments: {'; '.join(llm_adjustment_reasons)}")
            assumptions_list.append(f"LLM adjustment factor: {llm_adjustment_factor:.3f}x (capped at ±15%)")

        # ========== STEP 5: Combine adjustments with total cap ==========
        combined_factor = personalization_factor * llm_adjustment_factor
        # Clamp combined factor to ±25% total cap (0.75 to 1.25)
        combined_factor = max(1 - TOTAL_ADJUSTMENT_CAP, min(1 + TOTAL_ADJUSTMENT_CAP, combined_factor))

        estimated_rent = base_rent * combined_factor

        assumptions_list.append(f"Combined adjustment factor: {combined_factor:.3f}x (capped at ±25%)")
        assumptions_list.append(f"Final estimated rent: ${estimated_rent:,.0f}")

        # Create range using multipliers
        low_estimate = estimated_rent * LOW_RENT_MULTIPLIER
        high_estimate = estimated_rent * HIGH_RENT_MULTIPLIER

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

    def _fact_check_property(
        self,
        address: str,
        mls_description: Optional[str],
        beds: Optional[int],
        baths: Optional[float],
        condition: Optional[str]
    ) -> Dict[str, Any]:
        """
        Fact-check property features from address and MLS description.

        Returns a dictionary with detected features:
        - school_quality: 'excellent', 'good', 'average', 'poor', or None
        - near_beach: bool
        - near_major_employer: bool
        - rural_low_demand: bool
        - has_pool: bool
        - has_gym: bool
        - gated_community: bool
        - has_fenced_yard: bool
        - large_yard: bool
        - no_yard: bool
        - garage: bool
        - two_car_garage: bool
        - no_parking: bool
        - condition: str (extracted from MLS if available)
        """

        result = {}

        # Combine address and MLS description for analysis
        full_text = (address or '').upper()
        if mls_description:
            full_text += ' ' + mls_description.upper()

        # Check for coastal/beach proximity
        beach_keywords = ['BEACH', 'OCEAN', 'COAST', 'WATERFRONT', 'SEASIDE', 'OCEANVIEW', 'OCEAN VIEW']
        result['near_beach'] = any(keyword in full_text for keyword in beach_keywords)

        # Check for major employers/areas (examples - expand as needed)
        employer_keywords = [
            'DOWNTOWN', 'TECH PARK', 'BUSINESS DISTRICT', 'FINANCIAL DISTRICT',
            'SILICON VALLEY', 'GOOGLE', 'APPLE', 'MICROSOFT', 'AMAZON',
            'HOSPITAL', 'UNIVERSITY', 'CAMPUS'
        ]
        result['near_major_employer'] = any(keyword in full_text for keyword in employer_keywords)

        # Check for rural/low demand indicators
        rural_keywords = ['RURAL', 'REMOTE', 'COUNTRY', 'FARMLAND', 'ACRES']
        result['rural_low_demand'] = any(keyword in full_text for keyword in rural_keywords)

        # Check for amenities
        result['has_pool'] = 'POOL' in full_text
        result['has_gym'] = any(keyword in full_text for keyword in ['GYM', 'FITNESS', 'WORKOUT'])
        result['gated_community'] = any(keyword in full_text for keyword in ['GATED', 'GATE', 'SECURED COMMUNITY'])

        # Check for yard features
        result['has_fenced_yard'] = any(keyword in full_text for keyword in ['FENCED YARD', 'FENCED', 'FENCE'])
        result['large_yard'] = any(keyword in full_text for keyword in ['LARGE YARD', 'SPACIOUS YARD', 'BIG YARD'])
        result['no_yard'] = any(keyword in full_text for keyword in ['NO YARD', 'NO OUTDOOR', 'CONDO'])

        # Check for parking
        result['two_car_garage'] = any(keyword in full_text for keyword in ['2 CAR GARAGE', 'TWO CAR GARAGE', '2-CAR GARAGE'])
        result['garage'] = 'GARAGE' in full_text and not result['two_car_garage']
        result['no_parking'] = any(keyword in full_text for keyword in ['NO PARKING', 'STREET PARKING ONLY'])

        # Check for school district quality (basic heuristic - would ideally use school rating APIs)
        excellent_school_keywords = [
            'EXCELLENT SCHOOLS', 'TOP RATED SCHOOLS', 'A+ SCHOOLS', 'AWARD WINNING SCHOOLS',
            'BLUE RIBBON', 'HIGHLY RATED SCHOOLS'
        ]
        good_school_keywords = ['GOOD SCHOOLS', 'GREAT SCHOOLS', 'RATED SCHOOLS']
        poor_school_keywords = ['NEEDS IMPROVEMENT', 'LOW RATED']

        if any(keyword in full_text for keyword in excellent_school_keywords):
            result['school_quality'] = 'excellent'
        elif any(keyword in full_text for keyword in good_school_keywords):
            result['school_quality'] = 'good'
        elif any(keyword in full_text for keyword in poor_school_keywords):
            result['school_quality'] = 'poor'
        else:
            result['school_quality'] = None

        # Extract condition from MLS description if available
        if mls_description:
            condition_keywords = {
                'PREMIUM': ['PREMIUM', 'LUXURY', 'HIGH-END', 'UPSCALE'],
                'RENOVATED': ['RENOVATED', 'REMODELED', 'UPDATED', 'MODERN'],
                'EXCELLENT': ['EXCELLENT', 'PRISTINE', 'IMMACULATE'],
                'GOOD': ['GOOD CONDITION', 'WELL MAINTAINED', 'MOVE-IN READY'],
                'NEEDS WORK': ['FIXER', 'NEEDS WORK', 'AS-IS', 'HANDYMAN', 'TLC', 'INVESTORS SPECIAL'],
                'FAIR': ['AVERAGE', 'FAIR']
            }

            for condition_type, keywords in condition_keywords.items():
                if any(keyword in full_text for keyword in keywords):
                    result['condition'] = condition_type
                    break

        return result

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
