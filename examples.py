"""
Example usage of AI Rent and DSCR Calculator

This file demonstrates various scenarios and use cases.
"""

from ai_rent_dscr import AIRentDSCRCalculator, calculate_ai_rent_dscr_dict
import json


def print_result_summary(result):
    """Print a formatted summary of the calculation result."""
    print("\n" + "="*80)
    print(f"PROPERTY: {result['address']}")
    print("="*80)

    print(f"\n📍 INPUTS")
    print(f"   Purchase Price: ${result['purchase_price']:,.0f}")
    print(f"   Down Payment: ${result['down_payment_amount']:,.0f} ({result['down_payment_percent']*100:.1f}%)")
    print(f"   Loan Amount: ${result['loan_amount']:,.0f}")
    print(f"   Interest Rate: {result['interest_rate_annual']*100:.2f}%")
    print(f"   Term: {result['term_years']} years")
    print(f"   Loan Type: {'Interest-Only' if result['interest_only'] else 'Fully Amortized'}")

    print(f"\n💰 RENT ESTIMATE")
    print(f"   Estimated Monthly Rent: ${result['estimated_monthly_rent']:,.0f}")
    print(f"   Range: ${result['low_estimate_rent']:,.0f} - ${result['high_estimate_rent']:,.0f}")
    print(f"   Confidence Score: {result['confidence_score']:.0%}")

    print(f"\n📊 FINANCIAL METRICS")
    print(f"   Monthly Debt Service: ${result['monthly_debt_service']:,.2f}")
    print(f"   Annual NOI: ${result['NOI_annual']:,.2f}")
    print(f"   Annual Debt Service: ${result['annual_debt_service']:,.2f}")
    print(f"   DSCR: {result['DSCR']:.2f} ({result['risk_label']})")
    print(f"   Monthly Cashflow: ${result['monthly_cashflow']:,.2f}")

    print(f"\n📝 SUMMARY")
    print(f"   {result['human_summary']}")

    print(f"\n⚠️  ASSUMPTIONS")
    print(f"   {result['assumptions']}")

    print(f"\n💡 NOTES FOR INVESTOR")
    print(f"   {result['notes_for_investor']}")

    print("\n" + "="*80 + "\n")


def example_1_standard_sfr():
    """Example 1: Standard single-family rental in mid-tier market."""
    print("\n" + "#"*80)
    print("# EXAMPLE 1: Standard Single-Family Rental")
    print("#"*80)

    params = {
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

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_2_condo_interest_only():
    """Example 2: Condo with interest-only loan."""
    print("\n" + "#"*80)
    print("# EXAMPLE 2: Condo with Interest-Only Loan")
    print("#"*80)

    params = {
        "address": "100 Harbor View, Miami, FL 33131",
        "purchase_price": 425000,
        "down_payment_amount": 127500,  # 30% down
        "interest_rate_annual": 0.065,
        "term_years": 10,
        "interest_only": True,
        "property_type": "Condo",
        "beds": 2,
        "baths": 2,
        "sqft": 1200
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_3_fixer_upper():
    """Example 3: Fixer-upper in lower-cost market."""
    print("\n" + "#"*80)
    print("# EXAMPLE 3: Fixer-Upper Investment")
    print("#"*80)

    params = {
        "address": "456 Maple Dr, Cleveland, OH 44101",
        "purchase_price": 125000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.08,
        "term_years": 30,
        "interest_only": False,
        "property_type": "SFR",
        "beds": 3,
        "baths": 1,
        "condition": "Fixer - needs work"
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_4_high_end_property():
    """Example 4: High-end property in expensive market."""
    print("\n" + "#"*80)
    print("# EXAMPLE 4: High-End Property")
    print("#"*80)

    params = {
        "address": "789 Ocean Blvd, San Francisco, CA 94102",
        "purchase_price": 1500000,
        "down_payment_percent": 0.30,
        "interest_rate_annual": 0.06,
        "term_years": 30,
        "interest_only": False,
        "property_type": "SFR",
        "beds": 4,
        "baths": 3.5,
        "sqft": 2800,
        "condition": "Excellent"
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_5_minimal_inputs():
    """Example 5: Minimal inputs - let AI fill in assumptions."""
    print("\n" + "#"*80)
    print("# EXAMPLE 5: Minimal Inputs (Maximum AI Estimation)")
    print("#"*80)

    params = {
        "address": "321 Pine St, Denver, CO 80202",
        "purchase_price": 550000,
        "interest_rate_annual": 0.07,
        "term_years": 30
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_6_low_dscr_scenario():
    """Example 6: Scenario likely to produce low DSCR."""
    print("\n" + "#"*80)
    print("# EXAMPLE 6: Low DSCR Scenario (Weak Deal)")
    print("#"*80)

    params = {
        "address": "555 Suburban Ln, Expensive City, CA 90210",
        "purchase_price": 900000,
        "down_payment_percent": 0.20,  # Minimum down
        "interest_rate_annual": 0.08,  # Higher rate
        "term_years": 30,
        "interest_only": False,
        "property_type": "SFR",
        "beds": 3,
        "baths": 2,
        "condition": "Average"
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_7_custom_operating_expenses():
    """Example 7: Custom operating expense ratio."""
    print("\n" + "#"*80)
    print("# EXAMPLE 7: Custom Operating Expense Ratio")
    print("#"*80)

    params = {
        "address": "222 Efficiency St, Phoenix, AZ 85001",
        "purchase_price": 300000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.065,
        "term_years": 30,
        "interest_only": False,
        "property_type": "SFR",
        "beds": 3,
        "baths": 2,
        "operating_expense_ratio": 0.25  # Lower expenses (25% instead of default 35%)
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_8_multi_family():
    """Example 8: Multi-family property."""
    print("\n" + "#"*80)
    print("# EXAMPLE 8: Multi-Family Property (Duplex)")
    print("#"*80)

    params = {
        "address": "888 Duplex Ave, Portland, OR 97201",
        "purchase_price": 650000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.07,
        "term_years": 30,
        "interest_only": False,
        "property_type": "Duplex",
        "beds": 6,  # 3 per unit
        "baths": 4,  # 2 per unit
        "sqft": 3200
    }

    result = calculate_ai_rent_dscr_dict(params)
    print_result_summary(result)


def example_json_output():
    """Example: Getting full JSON output."""
    print("\n" + "#"*80)
    print("# EXAMPLE: Full JSON Output")
    print("#"*80)

    params = {
        "address": "999 JSON St, Seattle, WA 98101",
        "purchase_price": 475000,
        "down_payment_percent": 0.20,
        "interest_rate_annual": 0.068,
        "term_years": 30,
        "beds": 3,
        "baths": 2.5
    }

    calculator = AIRentDSCRCalculator()
    result = calculator.calculate(**params)

    print("\nComplete JSON Output:")
    print(json.dumps(result, indent=2))


def run_all_examples():
    """Run all examples."""
    example_1_standard_sfr()
    example_2_condo_interest_only()
    example_3_fixer_upper()
    example_4_high_end_property()
    example_5_minimal_inputs()
    example_6_low_dscr_scenario()
    example_7_custom_operating_expenses()
    example_8_multi_family()
    example_json_output()


if __name__ == "__main__":
    print("\n")
    print("*"*80)
    print("*" + " "*78 + "*")
    print("*" + "  AI RENT AND DSCR CALCULATOR - EXAMPLES".center(78) + "*")
    print("*" + " "*78 + "*")
    print("*"*80)

    run_all_examples()

    print("\n" + "*"*80)
    print("All examples completed!")
    print("*"*80 + "\n")
