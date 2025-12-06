"""
Unit tests for AI Rent and DSCR Calculator

Run with: python test_calculations.py
"""

from ai_rent_dscr import AIRentDSCRCalculator


def test_loan_amount_calculation():
    """Test loan amount calculations."""
    print("\n" + "="*80)
    print("TEST: Loan Amount Calculation")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    # Test 1: Down payment as amount
    loan, dp_amt, dp_pct = calculator._calculate_loan_amount(
        purchase_price=400000,
        down_payment_amount=100000,
        down_payment_percent=None
    )
    assert loan == 300000, f"Expected 300000, got {loan}"
    assert dp_amt == 100000, f"Expected 100000, got {dp_amt}"
    assert dp_pct == 0.25, f"Expected 0.25, got {dp_pct}"
    print("✓ Test 1 passed: Down payment as amount")

    # Test 2: Down payment as percent
    loan, dp_amt, dp_pct = calculator._calculate_loan_amount(
        purchase_price=400000,
        down_payment_amount=None,
        down_payment_percent=0.20
    )
    assert loan == 320000, f"Expected 320000, got {loan}"
    assert dp_amt == 80000, f"Expected 80000, got {dp_amt}"
    assert dp_pct == 0.20, f"Expected 0.20, got {dp_pct}"
    print("✓ Test 2 passed: Down payment as percent")

    # Test 3: Default (no down payment specified)
    loan, dp_amt, dp_pct = calculator._calculate_loan_amount(
        purchase_price=400000,
        down_payment_amount=None,
        down_payment_percent=None
    )
    assert loan == 320000, f"Expected 320000, got {loan}"
    assert dp_amt == 80000, f"Expected 80000, got {dp_amt}"
    assert dp_pct == 0.20, f"Expected 0.20, got {dp_pct}"
    print("✓ Test 3 passed: Default 20% down payment")

    print("\n✅ All loan amount calculation tests passed!\n")


def test_debt_service_calculation():
    """Test debt service calculations."""
    print("\n" + "="*80)
    print("TEST: Debt Service Calculation")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    # Test 1: Interest-only loan
    monthly_payment = calculator._calculate_debt_service(
        loan_amount=300000,
        interest_rate_annual=0.06,
        term_years=30,
        interest_only=True
    )
    expected = 300000 * (0.06 / 12)  # = 1500
    assert abs(monthly_payment - expected) < 0.01, \
        f"Expected {expected}, got {monthly_payment}"
    print(f"✓ Test 1 passed: Interest-only loan = ${monthly_payment:.2f}")

    # Test 2: Fully amortized loan
    monthly_payment = calculator._calculate_debt_service(
        loan_amount=300000,
        interest_rate_annual=0.07,
        term_years=30,
        interest_only=False
    )
    # Expected ~1995.91 based on standard amortization
    assert 1990 < monthly_payment < 2000, \
        f"Expected ~1995.91, got {monthly_payment}"
    print(f"✓ Test 2 passed: Fully amortized loan = ${monthly_payment:.2f}")

    # Test 3: Higher interest rate
    monthly_payment = calculator._calculate_debt_service(
        loan_amount=200000,
        interest_rate_annual=0.08,
        term_years=30,
        interest_only=False
    )
    # Expected ~1467.53
    assert 1460 < monthly_payment < 1475, \
        f"Expected ~1467.53, got {monthly_payment}"
    print(f"✓ Test 3 passed: Higher rate loan = ${monthly_payment:.2f}")

    print("\n✅ All debt service calculation tests passed!\n")


def test_risk_labels():
    """Test DSCR risk label assignment."""
    print("\n" + "="*80)
    print("TEST: Risk Label Assignment")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    # Test Strong
    label = calculator._get_risk_label(1.50)
    assert label == "Strong", f"Expected 'Strong', got '{label}'"
    print("✓ Test 1 passed: DSCR 1.50 = Strong")

    # Test Borderline (upper)
    label = calculator._get_risk_label(1.29)
    assert label == "Borderline", f"Expected 'Borderline', got '{label}'"
    print("✓ Test 2 passed: DSCR 1.29 = Borderline")

    # Test Borderline (lower)
    label = calculator._get_risk_label(1.10)
    assert label == "Borderline", f"Expected 'Borderline', got '{label}'"
    print("✓ Test 3 passed: DSCR 1.10 = Borderline")

    # Test Weak
    label = calculator._get_risk_label(1.05)
    assert label == "Weak", f"Expected 'Weak', got '{label}'"
    print("✓ Test 4 passed: DSCR 1.05 = Weak")

    # Test Very Weak
    label = calculator._get_risk_label(0.85)
    assert label == "Weak", f"Expected 'Weak', got '{label}'"
    print("✓ Test 5 passed: DSCR 0.85 = Weak")

    print("\n✅ All risk label tests passed!\n")


def test_full_calculation():
    """Test full calculation end-to-end."""
    print("\n" + "="*80)
    print("TEST: Full Calculation End-to-End")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    result = calculator.calculate(
        address="Test Property, Test City, TX 12345",
        purchase_price=400000,
        down_payment_percent=0.25,
        interest_rate_annual=0.07,
        term_years=30,
        interest_only=False,
        beds=3,
        baths=2,
        sqft=1800
    )

    # Verify all required fields are present
    required_fields = [
        'mode', 'address', 'purchase_price', 'loan_amount',
        'estimated_monthly_rent', 'DSCR', 'risk_label',
        'monthly_cashflow', 'NOI_annual', 'human_summary',
        'disclaimer'
    ]

    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
        print(f"✓ Field '{field}' present")

    # Verify calculations make sense
    assert result['loan_amount'] == 300000, "Loan amount incorrect"
    assert result['estimated_monthly_rent'] > 0, "Rent should be positive"
    assert result['DSCR'] > 0, "DSCR should be positive"
    assert result['mode'] == 'ai_rent_and_dscr', "Mode should be 'ai_rent_and_dscr'"

    print("\n✅ Full calculation test passed!\n")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n" + "="*80)
    print("TEST: Edge Cases")
    print("="*80)

    calculator = AIRentDSCRCalculator()

    # Test 1: Very low purchase price
    result = calculator.calculate(
        address="123 Budget St, Affordable City, OH 44101",
        purchase_price=50000,
        down_payment_percent=0.25,
        interest_rate_annual=0.08,
        term_years=30
    )
    assert result['estimated_monthly_rent'] > 0, "Rent should be positive for low price"
    print("✓ Test 1 passed: Very low purchase price handled")

    # Test 2: Very high purchase price
    result = calculator.calculate(
        address="789 Luxury Ln, San Francisco, CA 94102",
        purchase_price=3000000,
        down_payment_percent=0.30,
        interest_rate_annual=0.06,
        term_years=30
    )
    assert result['estimated_monthly_rent'] > 0, "Rent should be positive for high price"
    assert result['DSCR'] >= 0, "DSCR should be calculated"
    print("✓ Test 2 passed: Very high purchase price handled")

    # Test 3: 100% down payment (no loan)
    result = calculator.calculate(
        address="456 Cash Buy Ave, Denver, CO 80202",
        purchase_price=400000,
        down_payment_amount=400000,
        interest_rate_annual=0.07,
        term_years=30
    )
    assert result['loan_amount'] == 0, "Loan amount should be zero"
    assert result['monthly_debt_service'] == 0, "Debt service should be zero"
    print("✓ Test 3 passed: 100% down payment (cash purchase) handled")

    # Test 4: 0% vacancy rate (per requirements)
    result = calculator.calculate(
        address="111 Full Occupancy St, Austin, TX 78701",
        purchase_price=300000,
        vacancy_rate=0.0
    )
    assert result['vacancy_rate'] == 0.0, "Vacancy should be 0%"
    assert result['effective_gross_income_monthly'] == result['estimated_monthly_rent'], \
        "EGI should equal rent when vacancy is 0%"
    print("✓ Test 4 passed: 0% vacancy rate handled correctly")

    print("\n✅ All edge case tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "*"*80)
    print("*" + " "*78 + "*")
    print("*" + "RUNNING UNIT TESTS FOR AI RENT AND DSCR CALCULATOR".center(78) + "*")
    print("*" + " "*78 + "*")
    print("*"*80)

    try:
        test_loan_amount_calculation()
        test_debt_service_calculation()
        test_risk_labels()
        test_full_calculation()
        test_edge_cases()

        print("\n" + "*"*80)
        print("*" + " "*78 + "*")
        print("*" + "🎉 ALL TESTS PASSED! 🎉".center(78) + "*")
        print("*" + " "*78 + "*")
        print("*"*80 + "\n")

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
