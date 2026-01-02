"""
Streamlit DSCR Calculator - Clean Minimal UI
Single-page design matching investor requirements
"""

import streamlit as st
from ai_rent_dscr import AIRentDSCRCalculator

# Page configuration
st.set_page_config(
    page_title="DSCR Calculator",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Minimal clean CSS
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f8f9fa;
        padding: 2rem 1rem;
    }

    /* Remove extra padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }

    /* Clean headers */
    h1 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #1a1a1a !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2rem !important;
    }

    /* Clean buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem;
        border: none;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }

    /* Input fields */
    .stNumberInput input, .stTextInput input {
        border-radius: 8px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 0.875rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# Initialize calculator
calculator = AIRentDSCRCalculator()

# Session state
if 'result' not in st.session_state:
    st.session_state.result = None

# Logo at top left
try:
    st.image("images/bwm_logo.png", width=180)
except:
    st.markdown("**BrickWood Mortgage**")  # Fallback if logo not found

# Header
st.title("DSCR Calculator")
st.caption("Powered by BrickWood Mortgage")

# Compact inputs in grid layout
st.markdown("---")

# ROW 1: Main property info
col1, col2, col3 = st.columns(3)
with col1:
    address = st.text_input(
        "Property Address",
        placeholder="123 Ocean Blvd, Myrtle Beach, SC",
        help="SC address for automatic tax calculation"
    )
with col2:
    purchase_price = st.number_input("Purchase Price", min_value=0, value=400000, step=10000, format="%d")
with col3:
    sqft = st.number_input("Square Feet", min_value=0, value=1800, step=100)

# ROW 2: Loan terms
col1, col2, col3 = st.columns(3)
with col1:
    down_payment_percent = st.slider("Down Payment (%)", min_value=0, max_value=40, value=20, step=1)
with col2:
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.1, format="%.1f")
with col3:
    term_years = st.number_input("Loan Term (Years)", min_value=1, max_value=40, value=30, step=1)

# ROW 3: Additional property details
col1, col2, col3 = st.columns(3)
with col1:
    hoa_monthly = st.number_input("Monthly HOA", min_value=0, value=0, step=50, format="%d")
with col2:
    beds = st.number_input("Bedrooms", min_value=0, value=3, step=1, help="Improves rent estimate")
with col3:
    baths = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=0.5, help="Improves rent estimate")

st.markdown("---")

# COMPACT TOGGLES GRID
st.markdown("##### Auto/Manual Settings")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Insurance**")
    insurance_mode = st.radio("", ["Auto ($150)", "Manual"], horizontal=True, label_visibility="collapsed", key="ins")
    if insurance_mode == "Manual":
        insurance_monthly = st.number_input("Amount", min_value=0, value=150, step=10, key="ins_amt")
    else:
        insurance_monthly = 150

with col2:
    st.markdown("**Rent Estimate**")
    rent_mode = st.radio("", ["Auto", "Manual"], horizontal=True, label_visibility="collapsed", key="rent")
    if rent_mode == "Manual":
        manual_rent = st.number_input("Amount", min_value=0, value=2500, step=50, key="rent_amt")
    else:
        manual_rent = None

with col3:
    st.markdown("**Property Taxes**")
    tax_mode = st.radio("", ["Auto", "Manual"], horizontal=True, label_visibility="collapsed", key="tax")
    if tax_mode == "Manual":
        manual_taxes = st.number_input("Annual", min_value=0, value=5000, step=100, key="tax_amt")
    else:
        manual_taxes = None

st.markdown("---")

# CALCULATE BUTTON
calculate_clicked = st.button("Calculate DSCR", type="primary", use_container_width=True)

if calculate_clicked:
    if not address:
        st.error("Please enter a property address")
    else:
        try:
            # Property type not collected in compact UI
            property_type = None

            # Build parameters
            params = {
                'address': address,
                'purchase_price': purchase_price,
                'down_payment_percent': down_payment_percent / 100,
                'interest_rate_annual': interest_rate / 100,
                'term_years': term_years,
                'insurance_monthly': insurance_monthly,
                'hoa_monthly': hoa_monthly
            }

            # Optional parameters
            if sqft > 0:
                params['sqft'] = int(sqft)
            if beds > 0:
                params['beds'] = int(beds)
            if baths > 0:
                params['baths'] = float(baths)
            if property_type:
                params['property_type'] = property_type

            # Calculate
            with st.spinner("Calculating..."):
                result = calculator.calculate(**params)
                st.session_state.result = result

        except Exception as e:
            st.error(f"Error: {str(e)}")

# RESULTS
if st.session_state.result:
    result = st.session_state.result

    st.markdown("---")

    # FOUR RESULT CARDS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="DSCR",
            value=f"{result['DSCR']:.2f}"
        )
        risk = result['risk_label']
        if risk == "Excellent":
            st.success(f"✓ {risk}")
        elif risk == "Good":
            st.success(f"✓ {risk}")
        else:  # Borderline
            st.warning(f"⚠ {risk}")

    with col2:
        st.metric(
            label="Est. Monthly Rent",
            value=f"${result['estimated_monthly_rent']:,.0f}"
        )
        st.caption(f"Range: ${result['low_estimate_rent']:,.0f}-${result['high_estimate_rent']:,.0f}")

    with col3:
        cashflow = result['monthly_cashflow']
        st.metric(
            label="Monthly Cashflow",
            value=f"${abs(cashflow):,.0f}",
            delta="Positive" if cashflow >= 0 else "Negative"
        )
        st.caption("After mortgage, taxes, insurance, and HOA")

    with col4:
        st.metric(
            label="Annual Taxes",
            value=f"${result['property_tax_annual']:,.0f}"
        )
        if result.get('sc_tax_calculation', {}).get('tax_accuracy') == 'ok':
            county = result['sc_tax_calculation']['county_name']
            st.caption(f"{county} County")
        else:
            st.caption("Based on your settings")

    # SUMMARY SENTENCE
    st.markdown("---")
    st.info(
        f"At your inputs, this property shows a DSCR of {result['DSCR']:.2f} and approximately "
        f"${abs(result['monthly_cashflow']):,.0f}/month "
        f"{'positive' if result['monthly_cashflow'] >= 0 else 'negative'} cashflow."
    )

    # PHONE BUTTON
    st.markdown(
        '<div style="text-align: center; margin: 2rem 0;">'
        '<a href="tel:8433144104" style="'
        'display: inline-block; '
        'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
        'color: white; '
        'padding: 1rem 2rem; '
        'border-radius: 8px; '
        'text-decoration: none; '
        'font-weight: 600; '
        'font-size: 1.1rem;">'
        '📞 Click here to get a quote from BrickWood Mortgage'
        '</a>'
        '</div>',
        unsafe_allow_html=True
    )

    # NOI CALCULATOR (Toggle)
    st.markdown("---")

    # Make button more prominent
    if 'show_noi' not in st.session_state:
        st.session_state.show_noi = False

    if st.button("📊 Calculate Additional Investment Metrics", type="primary", use_container_width=True):
        st.session_state.show_noi = not st.session_state.show_noi

    if st.session_state.show_noi:
        # NOI Explanation
        st.info("**What is NOI?** This metric analyzes the cashflow of a property itself as if it had no mortgage.")

        st.markdown("### Investment Metrics Settings")
        st.caption("Adjust assumptions to calculate Net Operating Income (NOI)")

        # Input columns
        col1, col2 = st.columns(2)

        with col1:
            vacancy_rate = st.number_input(
                "Vacancy Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=5.0,
                step=0.5,
                help="Expected vacancy rate as percentage"
            )

            maintenance_rate = st.number_input(
                "Maintenance Reserve (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.5,
                help="Annual maintenance reserve as percentage of rent"
            )

        with col2:
            utilities_mode = st.radio(
                "Who pays utilities?",
                ["Tenant pays utilities", "Owner pays utilities"],
                horizontal=False,
                key="utilities_toggle"
            )

            if utilities_mode == "Owner pays utilities":
                manual_utilities = st.number_input(
                    "Monthly Utilities (optional)",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                    help="Leave at 0 to use automatic estimate"
                )
            else:
                manual_utilities = 0.0

        # Calculate extended NOI
        noi_result = calculator.calculate_extended_noi(
            monthly_rent=result['estimated_monthly_rent'],
            monthly_taxes=result['property_tax_monthly'],
            monthly_insurance=result['insurance_monthly'],
            monthly_hoa=hoa_monthly,
            sqft=int(sqft) if sqft > 0 else None,
            vacancy_rate=vacancy_rate / 100,
            maintenance_rate=maintenance_rate / 100,
            tenant_pays_utilities=(utilities_mode == "Tenant pays utilities"),
            manual_utilities_monthly=manual_utilities
        )

        # Display NOI Results
        st.markdown("---")
        st.markdown("### 📈 Net Operating Income (NOI)")

        # Key Metrics in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Monthly NOI",
                value=f"${noi_result['noi_monthly']:,.0f}"
            )

        with col2:
            st.metric(
                label="Annual NOI",
                value=f"${noi_result['noi_annual']:,.0f}"
            )

        with col3:
            st.metric(
                label="Operating Expenses",
                value=f"${noi_result['operating_expenses_monthly']:,.0f}/mo"
            )

        # Detailed Breakdown
        st.markdown("---")
        st.markdown("#### 📋 Operating Expense Breakdown")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Monthly Operating Expenses:**")
            st.write(f"• Property Taxes: ${noi_result['monthly_taxes']:,.0f}")
            st.write(f"• Insurance: ${noi_result['monthly_insurance']:,.0f}")
            st.write(f"• HOA Fees: ${noi_result['monthly_hoa']:,.0f}")
            st.write(f"• Maintenance Reserve ({maintenance_rate:.1f}%): ${noi_result['maintenance_monthly']:,.0f}")
            st.write(f"• Utilities: ${noi_result['utilities_monthly']:,.0f}")
            st.write(f"**Total: ${noi_result['operating_expenses_monthly']:,.0f}**")

        with col2:
            st.write("**Assumptions Used:**")
            st.write(f"• Monthly Rent: ${noi_result['monthly_rent']:,.0f}")
            st.write(f"• Vacancy Rate: {noi_result['vacancy_rate']*100:.1f}%")
            st.write(f"• Maintenance Reserve: {noi_result['maintenance_rate']*100:.1f}%")
            st.write(f"• {noi_result['utilities_note']}")

        # Info box with NOI context
        st.info(
            f"💡 **What is NOI?** Net Operating Income (NOI) is the total income from the property minus all operating expenses. "
            f"Your property generates **${noi_result['noi_monthly']:,.0f}/month** or **${noi_result['noi_annual']:,.0f}/year** "
            f"in NOI before debt service (mortgage payments). This is a key metric for evaluating investment performance."
        )

    # SC TAX DETAILS (Optional expander)
    if result.get('sc_tax_calculation', {}).get('tax_accuracy') == 'ok':
        with st.expander("🏛️ South Carolina Tax Details"):
            sc_tax = result['sc_tax_calculation']
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**County:** {sc_tax['county_name']}")
                st.write(f"**Millage Rate:** {sc_tax['millage_rate']:.3f}")
                st.write(f"**Assessment Ratio:** {sc_tax['assessment_ratio']*100:.1f}%")
            with col2:
                st.write(f"**Taxable Value:** ${sc_tax['taxable_value']:,.2f}")
                st.write(f"**Monthly Taxes:** ${sc_tax['monthly_taxes']:,.2f}")
                st.write(f"**Annual Taxes:** ${sc_tax['annual_taxes']:,.2f}")

# DISCLAIMER (always visible at bottom)
st.markdown("---")
st.markdown(
    '<p style="color: #9ca3af; font-size: 0.75rem; text-align: center; line-height: 1.4;">'
    '<strong>Disclaimer:</strong> All calculations and figures shown on this site are estimates only and are provided for informational purposes. '
    'DSCR, rent projections, tax amounts, and cashflow outputs may vary by lender, property type, county assessment data, and actual underwriting guidelines. '
    'Nothing on this page constitutes a loan approval, financial advice, or a binding offer of credit. '
    'Please verify all numbers with a licensed mortgage professional.'
    '</p>',
    unsafe_allow_html=True
)
