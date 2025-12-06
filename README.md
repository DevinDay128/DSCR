# AI Rent and DSCR Calculator

An AI-powered tool for estimating rental income and calculating Debt Service Coverage Ratio (DSCR) for real estate investment properties in the United States.

## Overview

This tool helps real estate investors quickly evaluate rental properties by:
1. **Estimating realistic monthly market rent** based on property characteristics and general market patterns
2. **Calculating DSCR** (Debt Service Coverage Ratio) to assess the property's ability to cover debt payments

## 🚀 Quick Start - Web Interface

**Get started in under 2 minutes!**

### Option 1: Streamlit (Easiest)
```bash
pip install streamlit
streamlit run streamlit_app.py
```

### Option 2: Flask (Professional)
```bash
pip install flask
python app.py
# Open http://localhost:5000
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions and [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for deployment options.

## Important Disclaimers

⚠️ **This is NOT professional underwriting** - This tool provides rough AI-powered estimates based on general patterns. It does NOT access live MLS data, Zillow, AirDNA, or any paid databases.

⚠️ **Always conduct proper due diligence** - Get professional appraisals, rental market studies, and verify all assumptions before making investment decisions.

⚠️ **Estimates may vary significantly** - Actual rental income depends on specific property features, local market conditions, property management, tenant quality, and many other factors.

## Features

### Rent Estimation
- Estimates monthly market rent using property characteristics
- Provides low, middle, and high rent estimates
- Assumes long-term (12+ month) rentals, NOT short-term vacation rentals
- Confidence score to indicate estimation reliability
- Detailed assumptions and notes

### DSCR Calculation
- Calculates monthly and annual debt service
- Computes Net Operating Income (NOI)
- Determines DSCR ratio with risk label (Strong/Borderline/Weak)
- Projects monthly cashflow
- Accounts for vacancy, operating expenses, and insurance

### Risk Assessment
- **Strong** (DSCR ≥ 1.30): Healthy margin for unexpected expenses
- **Borderline** (1.10 ≤ DSCR < 1.30): Verify estimates carefully
- **Weak** (DSCR < 1.10): May have negative cashflow or tight margins

## Installation

No special installation required. Just Python 3.7+ with standard library.

```bash
# Clone or download the repository
git clone <repository-url>
cd DSCR

# Run directly
python ai_rent_dscr.py
```

## Usage

### Python API

```python
from ai_rent_dscr import AIRentDSCRCalculator

calculator = AIRentDSCRCalculator()

result = calculator.calculate(
    address="123 Main St, Austin, TX 78701",
    purchase_price=400000,
    down_payment_percent=0.25,
    interest_rate_annual=0.07,
    term_years=30,
    interest_only=False,
    property_type="SFR",
    beds=3,
    baths=2,
    sqft=1800,
    condition="Good"
)

print(f"Estimated Rent: ${result['estimated_monthly_rent']}")
print(f"DSCR: {result['DSCR']:.2f}")
print(f"Risk: {result['risk_label']}")
print(f"Monthly Cashflow: ${result['monthly_cashflow']:.2f}")
```

### JSON API

```python
from ai_rent_dscr import calculate_ai_rent_dscr
import json

params = {
    "address": "456 Oak Ave, Denver, CO 80202",
    "purchase_price": 550000,
    "down_payment_amount": 110000,
    "interest_rate_annual": 0.065,
    "term_years": 30,
    "interest_only": False
}

json_result = calculate_ai_rent_dscr(params)
print(json_result)
```

## Input Parameters

### Required
- `address` (str): Property address
- `purchase_price` (float): Purchase price in USD

### Loan Terms
- `down_payment_amount` (float): Down payment in USD (optional)
- `down_payment_percent` (float): Down payment as decimal, e.g., 0.20 for 20% (optional)
  - If neither provided, defaults to 20%
- `interest_rate_annual` (float): Annual interest rate as decimal, e.g., 0.07 for 7% (default: 0.07)
- `term_years` (int): Loan term in years (default: 30)
- `interest_only` (bool): Whether loan is interest-only (default: False)

### Property Details (Optional but Recommended)
- `property_type` (str): "SFR", "Condo", "Townhouse", "Multi-family", etc.
- `beds` (int): Number of bedrooms
- `baths` (float): Number of bathrooms
- `sqft` (int): Square footage
- `condition` (str): Property condition ("Excellent", "Good", "Average", "Poor", "Fixer")

### Operating Assumptions
- `vacancy_rate` (float): Vacancy rate as decimal (default: 0.0 per requirements)
- `operating_expense_ratio` (float): Operating expense ratio as decimal (default: 0.35)

## Output Format

The calculator returns a comprehensive JSON object with all inputs, calculations, and estimates:

```json
{
  "mode": "ai_rent_and_dscr",

  "address": "...",
  "purchase_price": 400000,
  "loan_amount": 300000,
  "down_payment_amount": 100000,
  "down_payment_percent": 0.25,

  "estimated_monthly_rent": 3400,
  "low_estimate_rent": 2890,
  "high_estimate_rent": 3910,
  "confidence_score": 0.70,

  "DSCR": 1.45,
  "risk_label": "Strong",
  "monthly_cashflow": 450,

  "NOI_annual": 19800,
  "annual_debt_service": 13680,

  "inputs_summary": "...",
  "human_summary": "...",
  "assumptions": "...",
  "notes_for_investor": "...",
  "disclaimer": "..."
}
```

## Calculation Methodology

### 1. Loan Amount
```
If down_payment_amount provided:
    loan_amount = purchase_price - down_payment_amount
Else if down_payment_percent provided:
    loan_amount = purchase_price * (1 - down_payment_percent)
Else:
    loan_amount = purchase_price * 0.80  (default 20% down)
```

### 2. Rent Estimation
- Uses purchase price-to-rent ratios adjusted by price tier
- Lower-priced properties typically achieve higher ratios (>1%)
- Higher-priced properties typically achieve lower ratios (<1%)
- Adjusts for property type, condition, and other factors
- NOT based on live market data

### 3. Operating Expenses
- Base: `effective_gross_income * operating_expense_ratio`
- Plus: Insurance at $150/month (per requirements)
- Default operating expense ratio: 35%

### 4. NOI (Net Operating Income)
```
effective_gross_income = monthly_rent * (1 - vacancy_rate)
operating_expenses = (effective_gross_income * op_ratio) + insurance
NOI_monthly = effective_gross_income - operating_expenses
NOI_annual = NOI_monthly * 12
```

### 5. Debt Service
**Interest-Only:**
```
monthly_payment = loan_amount * (annual_rate / 12)
```

**Fully Amortized:**
```
r = annual_rate / 12
n = term_years * 12
monthly_payment = loan_amount * [r * (1 + r)^n] / [(1 + r)^n - 1]
```

### 6. DSCR
```
DSCR = NOI_annual / annual_debt_service
```

**Risk Labels:**
- DSCR ≥ 1.30: Strong
- 1.10 ≤ DSCR < 1.30: Borderline
- DSCR < 1.10: Weak

### 7. Cashflow
```
monthly_cashflow = NOI_monthly - monthly_debt_service
```

## Examples

### Example 1: Single Family Home in Mid-Tier Market

```python
params = {
    "address": "789 Elm St, Raleigh, NC 27601",
    "purchase_price": 350000,
    "down_payment_percent": 0.20,
    "interest_rate_annual": 0.07,
    "term_years": 30,
    "interest_only": False,
    "property_type": "SFR",
    "beds": 4,
    "baths": 2.5,
    "sqft": 2200
}
```

### Example 2: Condo with Interest-Only Loan

```python
params = {
    "address": "100 Harbor View, Miami, FL 33131",
    "purchase_price": 425000,
    "down_payment_amount": 127500,
    "interest_rate_annual": 0.065,
    "term_years": 10,
    "interest_only": True,
    "property_type": "Condo",
    "beds": 2,
    "baths": 2
}
```

### Example 3: Fixer-Upper Investment

```python
params = {
    "address": "456 Maple Dr, Cleveland, OH 44101",
    "purchase_price": 125000,
    "down_payment_percent": 0.25,
    "interest_rate_annual": 0.08,
    "term_years": 30,
    "property_type": "SFR",
    "beds": 3,
    "baths": 1,
    "condition": "Fixer - needs work"
}
```

## Key Assumptions

1. **Vacancy Rate**: 0% (per requirements) - You should adjust based on local market
2. **Insurance**: $150/month (generic estimate) - Get actual quote
3. **Operating Expense Ratio**: 35% default - Verify for your market
4. **Rent Estimates**: Based on general patterns, NOT live data
5. **Long-Term Rentals**: Assumes 12+ month leases, not short-term

## Limitations

- Does not access live MLS, Zillow, or rental listing data
- Cannot account for specific property features (view, lot size, amenities)
- Does not consider local rent control or regulations
- Generic insurance and expense estimates
- Cannot predict future market changes
- Not suitable as sole basis for investment decisions

## Integration with Existing DSCR Calculator

This mode (`ai_rent_and_dscr`) is designed to work alongside existing manual DSCR calculation modes. Key differences:

- **Manual mode**: User provides exact rent and expenses → precise DSCR
- **AI mode**: AI estimates rent → approximate DSCR for quick screening

Use AI mode for initial property screening, then use manual mode with verified numbers for final underwriting.

## Best Practices

1. **Use as screening tool**: Quickly evaluate multiple properties
2. **Verify estimates**: Always confirm rents with local market data
3. **Get professional help**: Use appraisers and property managers
4. **Adjust assumptions**: Customize vacancy, expenses, and insurance
5. **Build in margins**: Don't rely on optimistic scenarios
6. **Local research**: Study the specific neighborhood and comparable rentals

## License

[Specify your license here]

## Contributing

[Specify contribution guidelines here]

## Support

For issues or questions, please [specify contact method].
