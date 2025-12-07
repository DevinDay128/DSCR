"""
Test script to verify SC tax calculation integration with DSCR calculator
"""

import json
from ai_rent_dscr import AIRentDSCRCalculator


def test_sc_integration():
    """Test SC tax calculation integration with various SC addresses"""

    calculator = AIRentDSCRCalculator()

    test_cases = [
        {
            "name": "Myrtle Beach, SC (Horry County)",
            "params": {
                "address": "123 Ocean Blvd, Myrtle Beach, SC 29577",
                "purchase_price": 400000,
                "down_payment_percent": 0.25,
                "interest_rate_annual": 0.07,
                "term_years": 30,
                "property_type": "SFR",
                "beds": 3,
                "baths": 2,
                "sqft": 1800,
            }
        },
        {
            "name": "Charleston, SC (Charleston County)",
            "params": {
                "address": "456 Meeting St, Charleston, SC 29401",
                "purchase_price": 500000,
                "down_payment_percent": 0.20,
                "interest_rate_annual": 0.065,
                "term_years": 30,
                "property_type": "Townhouse",
                "beds": 3,
                "baths": 2.5,
                "sqft": 2000,
            }
        },
        {
            "name": "Little River, SC (Horry County)",
            "params": {
                "address": "789 Palm Blvd, Little River, SC 29566",
                "purchase_price": 350000,
                "down_payment_percent": 0.25,
                "interest_rate_annual": 0.07,
                "term_years": 30,
                "beds": 4,
                "baths": 3,
                "sqft": 2200,
            }
        },
        {
            "name": "Columbia, SC (Richland County)",
            "params": {
                "address": "321 Main St, Columbia, SC 29201",
                "purchase_price": 300000,
                "down_payment_percent": 0.20,
                "interest_rate_annual": 0.07,
                "term_years": 30,
                "beds": 3,
                "baths": 2,
                "sqft": 1600,
            }
        },
        {
            "name": "Non-SC Address (Austin, TX)",
            "params": {
                "address": "999 Sixth St, Austin, TX 78701",
                "purchase_price": 400000,
                "down_payment_percent": 0.25,
                "interest_rate_annual": 0.07,
                "term_years": 30,
                "property_tax_rate": 0.02,  # Specify TX rate
            }
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")

        result = calculator.calculate(**test['params'])

        print(f"\n📍 Address: {result['address']}")
        print(f"💰 Purchase Price: ${result['purchase_price']:,.0f}")
        print(f"\n💵 ESTIMATED RENT: ${result['estimated_monthly_rent']:,.0f}/month")
        print(f"   Range: ${result['low_estimate_rent']:,.0f} - ${result['high_estimate_rent']:,.0f}")
        print(f"   Confidence: {result['confidence_score']*100:.0f}%")

        print(f"\n📊 MONTHLY EXPENSES:")
        print(f"   Property Taxes: ${result['property_tax_monthly']:,.2f}")

        # Show SC tax details if available
        if 'sc_tax_calculation' in result and result['sc_tax_calculation'] is not None:
            sc_tax = result['sc_tax_calculation']
            print(f"   ✓ SC Tax Calculation Used:")
            print(f"     - County: {sc_tax['county_name']}")
            print(f"     - Millage Rate: {sc_tax['millage_rate']:.5f}")
            print(f"     - Assessment Ratio: {sc_tax['assessment_ratio']:.2%}")
            print(f"     - Taxable Value: ${sc_tax['taxable_value']:,.2f}")
            print(f"     - Annual Taxes: ${sc_tax['annual_taxes']:,.2f}")
            print(f"     - Tax Accuracy: {sc_tax['tax_accuracy']}")
        else:
            if result.get('property_tax_rate'):
                print(f"     (Using generic rate: {result['property_tax_rate']*100:.2f}%)")

        print(f"   Insurance: ${result['insurance_monthly']:,.2f}")
        print(f"   P&I (Debt Service): ${result['monthly_debt_service']:,.2f}")
        total_expenses = result['property_tax_monthly'] + result['insurance_monthly'] + result['monthly_debt_service']
        print(f"   TOTAL MONTHLY EXPENSES: ${total_expenses:,.2f}")

        print(f"\n📈 DSCR ANALYSIS:")
        print(f"   DSCR: {result['DSCR']:.2f} ({result['risk_label']})")
        print(f"   Monthly Cashflow: ${result['monthly_cashflow']:,.2f}")
        print(f"   Annual NOI: ${result['NOI_annual']:,.2f}")

        print(f"\n📝 Summary:")
        print(f"   {result['human_summary']}")

    print(f"\n{'='*80}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    test_sc_integration()
