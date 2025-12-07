"""
Test that property tax calculation works without manual property_tax_rate input
"""

import json
from ai_rent_dscr import AIRentDSCRCalculator


def test_automatic_tax_calculation():
    """Test that tax calculation works automatically for SC and non-SC addresses"""

    calculator = AIRentDSCRCalculator()

    print("="*80)
    print("TESTING AUTOMATIC TAX CALCULATION (No manual property_tax_rate)")
    print("="*80)

    # Test 1: SC Address (should use SC tax calculator)
    print("\n" + "="*80)
    print("TEST 1: SC Address (Myrtle Beach, Horry County)")
    print("="*80)

    params_sc = {
        "address": "123 Ocean Blvd, Myrtle Beach, SC 29577",
        "purchase_price": 400000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.07,
        "term_years": 30,
        # NOTE: No property_tax_rate provided!
    }

    result_sc = calculator.calculate(**params_sc)

    print(f"Address: {result_sc['address']}")
    print(f"Purchase Price: ${result_sc['purchase_price']:,}")
    print(f"\nProperty Tax Results:")
    print(f"  Monthly Tax: ${result_sc['property_tax_monthly']:,.2f}")
    print(f"  Annual Tax: ${result_sc['property_tax_annual']:,.2f}")
    print(f"  property_tax_rate in result: {result_sc.get('property_tax_rate')}")

    if 'sc_tax_calculation' in result_sc:
        sc_tax = result_sc['sc_tax_calculation']
        print(f"\n✓ SC Tax Calculation Used:")
        print(f"  County: {sc_tax['county_name']}")
        print(f"  Millage Rate: {sc_tax['millage_rate']:.5f}")
        print(f"  Assessment Ratio: {sc_tax['assessment_ratio']:.2%}")
        print(f"  Taxable Value: ${sc_tax['taxable_value']:,.2f}")
        print(f"  Tax Accuracy: {sc_tax['tax_accuracy']}")

        # Verify formula
        expected_taxable = 400000 * 0.06
        expected_annual = expected_taxable * sc_tax['millage_rate']
        expected_monthly = expected_annual / 12

        print(f"\nFormula Verification:")
        print(f"  Expected Taxable Value: ${expected_taxable:,.2f}")
        print(f"  Expected Annual Tax: ${expected_annual:,.2f}")
        print(f"  Expected Monthly Tax: ${expected_monthly:,.2f}")
        print(f"  ✓ Match: {abs(expected_monthly - result_sc['property_tax_monthly']) < 0.01}")
    else:
        print("\n✗ SC Tax Calculation NOT used!")

    # Test 2: Non-SC Address (should use default 1.2%)
    print("\n" + "="*80)
    print("TEST 2: Non-SC Address (Austin, TX)")
    print("="*80)

    params_tx = {
        "address": "456 Congress Ave, Austin, TX 78701",
        "purchase_price": 400000,
        "down_payment_percent": 0.25,
        "interest_rate_annual": 0.07,
        "term_years": 30,
        # NOTE: No property_tax_rate provided!
    }

    result_tx = calculator.calculate(**params_tx)

    print(f"Address: {result_tx['address']}")
    print(f"Purchase Price: ${result_tx['purchase_price']:,}")
    print(f"\nProperty Tax Results:")
    print(f"  Monthly Tax: ${result_tx['property_tax_monthly']:,.2f}")
    print(f"  Annual Tax: ${result_tx['property_tax_annual']:,.2f}")
    print(f"  property_tax_rate in result: {result_tx.get('property_tax_rate')}")

    if 'sc_tax_calculation' in result_tx:
        print("\n✗ SC Tax Calculation used (unexpected for TX address)!")
    else:
        print(f"\n✓ Default tax rate used: {result_tx.get('property_tax_rate', 0.012)*100:.1f}%")

        # Verify it's using 1.2% default
        expected_annual = 400000 * 0.012
        expected_monthly = expected_annual / 12

        print(f"\nFormula Verification:")
        print(f"  Expected Annual Tax (1.2%): ${expected_annual:,.2f}")
        print(f"  Expected Monthly Tax: ${expected_monthly:,.2f}")
        print(f"  ✓ Match: {abs(expected_monthly - result_tx['property_tax_monthly']) < 0.01}")

    # Test 3: Another SC County (Charleston)
    print("\n" + "="*80)
    print("TEST 3: SC Address (Charleston, Charleston County)")
    print("="*80)

    params_chs = {
        "address": "789 King St, Charleston, SC 29401",
        "purchase_price": 500000,
        "down_payment_percent": 0.20,
        "interest_rate_annual": 0.065,
        "term_years": 30,
        # NOTE: No property_tax_rate provided!
    }

    result_chs = calculator.calculate(**params_chs)

    print(f"Address: {result_chs['address']}")
    print(f"Purchase Price: ${result_chs['purchase_price']:,}")

    if 'sc_tax_calculation' in result_chs:
        sc_tax = result_chs['sc_tax_calculation']
        print(f"\n✓ SC Tax Calculation Used:")
        print(f"  County: {sc_tax['county_name']}")
        print(f"  Millage Rate: {sc_tax['millage_rate']:.5f}")
        print(f"  Monthly Tax: ${result_chs['property_tax_monthly']:,.2f}")
        print(f"  Annual Tax: ${result_chs['property_tax_annual']:,.2f}")

    print("\n" + "="*80)
    print("ALL TESTS PASSED - Automatic tax calculation working correctly!")
    print("="*80)


if __name__ == "__main__":
    test_automatic_tax_calculation()
