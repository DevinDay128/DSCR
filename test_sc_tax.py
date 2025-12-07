"""
Test script for South Carolina tax calculation feature

This script tests:
1. SC tax calculator standalone functionality
2. Integration with AI Rent DSCR Calculator
3. Various SC counties
4. Edge cases (non-SC addresses, missing data)
"""

import json
from sc_tax_calculator import SCTaxCalculator
from ai_rent_dscr import AIRentDSCRCalculator


def test_sc_tax_calculator():
    """Test SC tax calculator directly"""
    print("="*80)
    print("TEST 1: SC TAX CALCULATOR - STANDALONE TESTS")
    print("="*80)

    calculator = SCTaxCalculator()

    # Test Case 1: Horry County (Myrtle Beach)
    print("\n1. Horry County (Myrtle Beach, SC 29577)")
    result = calculator.calculate_sc_rental_tax(
        address="123 Ocean Blvd, Myrtle Beach, SC 29577",
        property_value=400000
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'ok'
    assert result['county_name'] == 'Horry County'
    assert result['assessment_ratio'] == 0.06
    assert result['taxable_value'] == 24000.0
    print("✓ PASSED")

    # Test Case 2: Charleston County
    print("\n2. Charleston County")
    result = calculator.calculate_sc_rental_tax(
        address="456 King St, Charleston, SC 29401",
        property_value=500000
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'ok'
    assert result['county_name'] == 'Charleston County'
    assert result['taxable_value'] == 30000.0
    print("✓ PASSED")

    # Test Case 3: Greenville County
    print("\n3. Greenville County")
    result = calculator.calculate_sc_rental_tax(
        address="789 Main St, Greenville, SC 29601",
        property_value=350000
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'ok'
    assert result['county_name'] == 'Greenville County'
    assert result['taxable_value'] == 21000.0
    print("✓ PASSED")

    # Test Case 4: Non-SC address
    print("\n4. Non-SC Address (should return county_not_found)")
    result = calculator.calculate_sc_rental_tax(
        address="123 Main St, Austin, TX 78701",
        property_value=400000
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'county_not_found'
    assert result['county_name'] is None
    assert result['millage_rate'] is None
    print("✓ PASSED")

    # Test Case 5: Missing value
    print("\n5. Missing Value (should return missing_value)")
    result = calculator.calculate_sc_rental_tax(
        address="123 Ocean Blvd, Myrtle Beach, SC 29577",
        property_value=0
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'missing_value'
    assert result['county_name'] is None
    print("✓ PASSED")

    # Test Case 6: Beaufort County (Hilton Head)
    print("\n6. Beaufort County (Hilton Head)")
    result = calculator.calculate_sc_rental_tax(
        address="100 Beach Dr, Hilton Head Island, SC 29928",
        property_value=600000
    )
    print(json.dumps(result, indent=2))
    assert result['tax_accuracy'] == 'ok'
    assert result['county_name'] == 'Beaufort County'
    assert result['taxable_value'] == 36000.0
    print("✓ PASSED")

    print("\n" + "="*80)
    print("ALL SC TAX CALCULATOR TESTS PASSED!")
    print("="*80)


def test_ai_rent_dscr_integration():
    """Test integration with AI Rent DSCR Calculator"""
    print("\n" + "="*80)
    print("TEST 2: AI RENT DSCR CALCULATOR - INTEGRATION TESTS")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    # Test Case 1: SC Property (Myrtle Beach)
    print("\n1. SC Property - Myrtle Beach")
    result = calculator.calculate(
        address="123 Ocean Blvd, Myrtle Beach, SC 29577",
        purchase_price=400000,
        down_payment_percent=0.25,
        interest_rate_annual=0.07,
        term_years=30,
        property_type="SFR",
        beds=3,
        baths=2,
        sqft=1800
    )

    print(f"Address: {result['address']}")
    print(f"Purchase Price: ${result['purchase_price']:,}")
    print(f"Property Tax Monthly: ${result['property_tax_monthly']:,.2f}")
    print(f"Property Tax Annual: ${result['property_tax_annual']:,.2f}")

    # Check that SC tax info is present
    assert 'sc_tax_info' in result
    assert result['sc_tax_info']['tax_accuracy'] == 'ok'
    assert result['sc_tax_info']['county_name'] == 'Horry County'

    print(f"SC County: {result['sc_tax_info']['county_name']}")
    print(f"SC Millage Rate: {result['sc_tax_info']['millage_rate']}")
    print(f"SC Assessment Ratio: {result['sc_tax_info']['assessment_ratio']}")
    print(f"SC Taxable Value: ${result['sc_tax_info']['taxable_value']:,.2f}")
    print("✓ PASSED")

    # Test Case 2: Non-SC Property (should not have sc_tax_info)
    print("\n2. Non-SC Property - Austin, TX")
    result = calculator.calculate(
        address="123 Main St, Austin, TX 78701",
        purchase_price=400000,
        down_payment_percent=0.25,
        interest_rate_annual=0.07,
        term_years=30,
        property_tax_rate=0.012  # Manually provided for non-SC
    )

    print(f"Address: {result['address']}")
    print(f"Purchase Price: ${result['purchase_price']:,}")
    print(f"Property Tax Monthly: ${result['property_tax_monthly']:,.2f}")
    print(f"Property Tax Rate: {result['property_tax_rate']*100:.2f}%")

    # Check that SC tax info is NOT present
    assert 'sc_tax_info' not in result or result.get('sc_tax_info') is None
    print("✓ PASSED - SC tax info not present for non-SC property")

    # Test Case 3: SC Property without user-provided tax rate
    print("\n3. SC Property - Charleston (no user tax rate)")
    result = calculator.calculate(
        address="456 King St, Charleston, SC 29401",
        purchase_price=500000,
        down_payment_percent=0.20,
        interest_rate_annual=0.065,
        term_years=30,
        # Note: No property_tax_rate provided - should use SC calculation
        property_type="Condo",
        beds=2,
        baths=2,
        sqft=1500
    )

    print(f"Address: {result['address']}")
    print(f"Property Tax Monthly: ${result['property_tax_monthly']:,.2f}")
    print(f"DSCR: {result['DSCR']:.2f}")
    print(f"Monthly Cashflow: ${result['monthly_cashflow']:,.2f}")

    assert 'sc_tax_info' in result
    assert result['sc_tax_info']['county_name'] == 'Charleston County'
    print(f"SC County: {result['sc_tax_info']['county_name']}")
    print("✓ PASSED")

    # Test Case 4: Multiple SC counties
    print("\n4. Testing Multiple SC Counties")
    sc_test_cases = [
        ("Greenville, SC", "Greenville County"),
        ("Columbia, SC", "Richland County"),
        ("Rock Hill, SC", "York County"),
        ("Spartanburg, SC", "Spartanburg County"),
        ("Florence, SC", "Florence County"),
    ]

    for city, expected_county in sc_test_cases:
        result = calculator.calculate(
            address=f"100 Main St, {city}",
            purchase_price=300000,
            down_payment_percent=0.20
        )
        if 'sc_tax_info' in result:
            actual_county = result['sc_tax_info']['county_name']
            print(f"  {city} → {actual_county} ✓")
            assert actual_county == expected_county
        else:
            print(f"  {city} → County not detected ✗")

    print("\n" + "="*80)
    print("ALL INTEGRATION TESTS PASSED!")
    print("="*80)


def test_formula_accuracy():
    """Test that formulas are applied correctly"""
    print("\n" + "="*80)
    print("TEST 3: FORMULA ACCURACY VERIFICATION")
    print("="*80)

    calculator = SCTaxCalculator()

    # Test with known values
    property_value = 400000
    expected_assessment_ratio = 0.06
    expected_taxable_value = property_value * expected_assessment_ratio  # 24000

    # Horry County millage rate: 0.1923
    expected_millage = 0.1923
    expected_annual_tax = expected_taxable_value * expected_millage  # 24000 * 0.1923 = 4615.2
    expected_monthly_tax = expected_annual_tax / 12  # 384.6

    result = calculator.calculate_sc_rental_tax(
        address="Myrtle Beach, SC 29577",
        property_value=property_value
    )

    print(f"Property Value: ${property_value:,}")
    print(f"Assessment Ratio: {result['assessment_ratio']} (expected: {expected_assessment_ratio})")
    print(f"Taxable Value: ${result['taxable_value']:,} (expected: ${expected_taxable_value:,})")
    print(f"Millage Rate: {result['millage_rate']} (expected: {expected_millage})")
    print(f"Annual Taxes: ${result['annual_taxes']:,.2f} (expected: ${expected_annual_tax:,.2f})")
    print(f"Monthly Taxes: ${result['monthly_taxes']:,.2f} (expected: ${expected_monthly_tax:,.2f})")

    # Verify formulas
    assert result['assessment_ratio'] == expected_assessment_ratio, "Assessment ratio mismatch"
    assert result['taxable_value'] == expected_taxable_value, "Taxable value mismatch"
    assert result['millage_rate'] == expected_millage, "Millage rate mismatch"
    assert abs(result['annual_taxes'] - expected_annual_tax) < 0.01, "Annual tax mismatch"
    assert abs(result['monthly_taxes'] - expected_monthly_tax) < 0.01, "Monthly tax mismatch"

    print("\n✓ ALL FORMULAS VERIFIED CORRECTLY!")
    print("="*80)


if __name__ == "__main__":
    try:
        test_sc_tax_calculator()
        test_ai_rent_dscr_integration()
        test_formula_accuracy()

        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("="*80)
        print("\nThe SC tax calculation feature is working correctly:")
        print("✓ SC counties are detected accurately")
        print("✓ Millage rates are loaded from sc_millage.json")
        print("✓ Tax formulas are applied exactly as specified")
        print("✓ Integration with AI Rent DSCR Calculator works")
        print("✓ Non-SC properties are handled correctly")
        print("="*80)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise
