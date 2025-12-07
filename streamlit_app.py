"""
Streamlit Web Application for AI Rent and DSCR Calculator

This is a simpler alternative to the Flask app.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
from ai_rent_dscr import AIRentDSCRCalculator

# Page configuration
st.set_page_config(
    page_title="AI Rent & DSCR Calculator",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 30px;
    }
    .metric-card {
        background: #f9fafb;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }
    .risk-strong {
        background-color: #d1fae5;
        color: #065f46;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    .risk-borderline {
        background-color: #fed7aa;
        color: #92400e;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    .risk-weak {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏠 AI Rent & DSCR Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estimate rental income and analyze investment property performance</div>', unsafe_allow_html=True)

# Warning banner
st.warning("⚠️ **Important:** This tool provides rough AI estimates for screening purposes only. Always verify with professional appraisals and local market research.")

# Initialize calculator
calculator = AIRentDSCRCalculator()

# Create tabs for input and results
tab1, tab2 = st.tabs(["📝 Input", "📊 Results"])

with tab1:
    # Property Information
    st.header("📍 Property Information")
    col1, col2 = st.columns(2)
    with col1:
        address = st.text_input("Property Address *", placeholder="123 Main St, Austin, TX 78701")
    with col2:
        purchase_price = st.number_input("Purchase Price *", min_value=0, value=400000, step=10000)

    # Property Details
    st.header("🏡 Property Details (Optional)")
    col1, col2, col3 = st.columns(3)
    with col1:
        property_type = st.selectbox("Property Type", ["", "SFR", "Condo", "Townhouse", "Duplex", "Multi-family"])
        beds = st.number_input("Bedrooms", min_value=0, value=3, step=1)
    with col2:
        baths = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=0.5)
        sqft = st.number_input("Square Feet", min_value=0, value=1800, step=100)
    with col3:
        condition = st.selectbox("Condition", ["", "Excellent", "Good", "Average", "Fair", "Poor", "Fixer"])

    # Loan Terms
    st.header("💰 Loan Terms")
    col1, col2 = st.columns(2)
    with col1:
        down_payment_type = st.radio("Down Payment Type", ["Percentage", "Dollar Amount"])
        if down_payment_type == "Percentage":
            down_payment_percent = st.number_input("Down Payment %", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
            down_payment_amount = None
        else:
            down_payment_amount = st.number_input("Down Payment $", min_value=0, value=80000, step=1000)
            down_payment_percent = None

    with col2:
        interest_rate_annual = st.number_input("Interest Rate %", min_value=0.0, max_value=20.0, value=7.0, step=0.01)
        term_years = st.number_input("Loan Term (years)", min_value=1, max_value=40, value=30, step=1)
        interest_only = st.checkbox("Interest-Only Loan")

    # Expense Assumptions
    st.header("📊 Expense Assumptions")
    st.info("💡 **Expenses calculated: P&I (Principal & Interest), Property Taxes, and Insurance only**")

    col1, col2 = st.columns(2)
    with col1:
        property_tax_rate = st.number_input(
            "Property Tax Rate % (default 1.2%)",
            min_value=0.0,
            max_value=10.0,
            value=1.2,
            step=0.1,
            help="Annual property tax rate. US average is ~1.2% but varies greatly by location."
        )
    with col2:
        insurance_monthly = st.number_input(
            "Insurance ($/month, default $150)",
            min_value=0,
            value=150,
            step=10,
            help="Monthly homeowners insurance cost. Get actual quote for accuracy."
        )

    st.warning("⚠️ Note: This calculator does NOT include maintenance, property management, HOA, utilities, or other operating expenses. Actual cashflow will be lower.")

    # Calculate button
    if st.button("🔍 Calculate DSCR", type="primary", use_container_width=True):
        if not address:
            st.error("Please enter a property address")
        else:
            # Build parameters
            params = {
                'address': address,
                'purchase_price': purchase_price,
                'interest_rate_annual': interest_rate_annual / 100,
                'term_years': term_years,
                'interest_only': interest_only,
                'property_tax_rate': property_tax_rate / 100,
                'insurance_monthly': insurance_monthly
            }

            if down_payment_percent is not None:
                params['down_payment_percent'] = down_payment_percent / 100
            if down_payment_amount is not None:
                params['down_payment_amount'] = down_payment_amount
            if property_type:
                params['property_type'] = property_type
            if beds > 0:
                params['beds'] = beds
            if baths > 0:
                params['baths'] = baths
            if sqft > 0:
                params['sqft'] = sqft
            if condition:
                params['condition'] = condition

            # Calculate
            try:
                result = calculator.calculate(**params)
                st.session_state.result = result
                st.success("✅ Calculation complete! Check the Results tab.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Results Tab
with tab2:
    if 'result' in st.session_state:
        result = st.session_state.result

        # Header with address and risk badge
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(f"🏠 {result['address']}")
        with col2:
            risk_class = f"risk-{result['risk_label'].lower()}"
            st.markdown(f'<div class="{risk_class}">{result["risk_label"].upper()}</div>', unsafe_allow_html=True)

        st.divider()

        # Key Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Estimated Monthly Rent",
                f"${result['estimated_monthly_rent']:,.0f}",
                f"Range: ${result['low_estimate_rent']:,.0f} - ${result['high_estimate_rent']:,.0f}"
            )
            st.caption(f"Confidence: {result['confidence_score']*100:.0f}%")

        with col2:
            st.metric(
                "DSCR",
                f"{result['DSCR']:.2f}",
                delta=None
            )

        with col3:
            cashflow = result['monthly_cashflow']
            st.metric(
                "Monthly Cashflow",
                f"${abs(cashflow):,.2f}",
                delta=f"{'Positive' if cashflow >= 0 else 'Negative'}"
            )

        st.divider()

        # Financial Details
        st.subheader("💰 Financial Details")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Purchase & Financing:**")
            st.write(f"- Purchase Price: ${result['purchase_price']:,.0f}")
            st.write(f"- Down Payment: ${result['down_payment_amount']:,.0f} ({result['down_payment_percent']*100:.0f}%)")
            st.write(f"- Loan Amount: ${result['loan_amount']:,.0f}")
            st.write(f"- Interest Rate: {result['interest_rate_annual']*100:.2f}%")
            st.write(f"- Term: {result['term_years']} years")
            st.write(f"- Loan Type: {'Interest-Only' if result['interest_only'] else 'Fully Amortized'}")

        with col2:
            st.markdown("**Monthly Expenses (PITI):**")
            st.write(f"- Property Taxes: ${result['property_tax_monthly']:,.2f}")
            st.write(f"- Insurance: ${result['insurance_monthly']:,.2f}")
            st.write(f"- P&I (Debt Service): ${result['monthly_debt_service']:,.2f}")
            total_monthly = result['property_tax_monthly'] + result['insurance_monthly'] + result['monthly_debt_service']
            st.write(f"- **Total Monthly PITI: ${total_monthly:,.2f}**")
            st.write("")
            st.markdown("**DSCR Calculation:**")
            st.write(f"- Annual NOI: ${result['NOI_annual']:,.2f}")
            st.write(f"- Annual Debt Service: ${result['annual_debt_service']:,.2f}")
            st.write(f"- **DSCR Ratio: {result['DSCR']:.2f}**")

        # SC Tax Calculation Details (if applicable)
        if result.get('sc_tax_calculation') and result['sc_tax_calculation']['tax_accuracy'] == 'ok':
            st.divider()
            st.success("🏛️ **South Carolina Tax Calculation (Automatic)**")
            sc_tax = result['sc_tax_calculation']
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**County:** {sc_tax['county_name']}")
                st.write(f"**Assessment Ratio:** {sc_tax['assessment_ratio']*100:.1f}% (Rental Property)")
                st.write(f"**Millage Rate:** {sc_tax['millage_rate']:.3f}")
            with col2:
                st.write(f"**Taxable Value:** ${sc_tax['taxable_value']:,.2f}")
                st.write(f"**Annual Taxes:** ${sc_tax['annual_taxes']:,.2f}")
                st.write(f"**Monthly Taxes:** ${sc_tax['monthly_taxes']:,.2f}")
            st.caption("✓ Taxes calculated automatically using official 2024 SC county millage rates.")

        st.divider()

        # Summary
        st.subheader("📝 Summary")
        st.info(result['human_summary'])

        # Assumptions
        with st.expander("🔍 Assumptions Made"):
            st.write(result['assumptions'])

        # Investor Notes
        with st.expander("💡 Notes for Investor"):
            st.warning(result['notes_for_investor'])

        # Disclaimer
        with st.expander("⚠️ Disclaimer"):
            st.error(result['disclaimer'])

        # Download JSON
        st.divider()
        import json
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json_str,
            file_name=f"dscr_analysis_{address.replace(' ', '_')}.json",
            mime="application/json"
        )

    else:
        st.info("👈 Fill out the form in the Input tab and click 'Calculate DSCR' to see results here.")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This calculator uses AI to estimate rental income and calculate DSCR for investment properties.

    **DSCR Risk Levels:**
    - 🟢 **Strong** (≥1.30): Healthy margin
    - 🟡 **Borderline** (1.10-1.30): Verify carefully
    - 🔴 **Weak** (<1.10): May have negative cashflow

    **Expenses Calculated:**
    - **P** = Principal (part of loan payment)
    - **I** = Interest (part of loan payment)
    - **T** = Property Taxes (default 1.2% annually)
    - **I** = Insurance (default $150/month)

    **Note:** Does NOT include maintenance, HOA, property management, or other operating expenses.
    """)

    st.divider()

    st.header("📚 Resources")
    st.write("""
    - Run examples: `python examples.py`
    - Run tests: `python test_calculations.py`
    - API docs: See README.md
    """)
