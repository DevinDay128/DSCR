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
    initial_sidebar_state="collapsed"
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

# Header with Logo
col1, col2 = st.columns([1, 3])
with col1:
    # Logo will be displayed if bwm_logo.png exists in images/ folder
    try:
        st.image("images/bwm_logo.png", width=120)
    except:
        st.markdown("**BWM**")  # Fallback if logo not found
with col2:
    st.title("DSCR Calculator")
    st.caption("Powered by BrickWood Mortgage")

st.divider()

# REQUIRED INPUTS
st.markdown("### Required Inputs")

col1, col2 = st.columns(2)

with col1:
    address = st.text_input(
        "Property Address",
        placeholder="Myrtle Beach, SC",
        help="Address must include South Carolina city/county for automatic tax calculation",
        label_visibility="visible"
    )

    purchase_price = st.number_input(
        "Purchase Price",
        min_value=0,
        value=400000,
        step=10000,
        format="%d"
    )

    hoa_monthly = st.number_input(
        "Monthly HOA",
        min_value=0,
        value=0,
        step=50,
        format="%d"
    )

with col2:
    down_payment_percent = st.slider(
        "Down Payment (%)",
        min_value=0,
        max_value=40,
        value=20,
        step=1
    )
    st.caption(f"{down_payment_percent}%")

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=7.0,
        step=0.1,
        format="%.1f"
    )

    term_years = st.number_input(
        "Loan Term (Years)",
        min_value=1,
        max_value=40,
        value=30,
        step=1
    )

st.divider()

# OPTIONAL INPUTS (Collapsed)
with st.expander("📝 Optional inputs (improve accuracy)"):
    col1, col2 = st.columns(2)

    with col1:
        sqft = st.number_input(
            "Square Feet (optional)",
            min_value=0,
            value=0,
            step=100
        )
        st.caption("Helps estimate rent more accurately")

        beds = st.number_input(
            "Bedrooms (optional)",
            min_value=0,
            value=0,
            step=1
        )
        st.caption("Optional — improves rent estimate")

    with col2:
        baths = st.number_input(
            "Bathrooms (optional)",
            min_value=0.0,
            value=0.0,
            step=0.5
        )
        st.caption("Optional — improves rent estimate")

        property_type = st.selectbox(
            "Property Type (optional)",
            ["", "Single Family", "Condo", "Townhome", "Multi-Family"]
        )

st.divider()

# INSURANCE SECTION
st.markdown("### Insurance")

insurance_mode = st.radio(
    "",
    ["Default ($150/month)", "Custom Amount"],
    horizontal=True,
    label_visibility="collapsed",
    key="insurance_toggle"
)

if insurance_mode == "Custom Amount":
    insurance_monthly = st.number_input(
        "Monthly Insurance",
        min_value=0,
        value=150,
        step=10
    )
    st.caption("Enter your custom insurance amount")
else:
    insurance_monthly = 150
    st.caption("Default: $150/month")

st.divider()

# RENT SECTION
st.markdown("### Rent Estimate *")

rent_mode = st.radio(
    "",
    ["Auto Estimate", "Manual Rent"],
    horizontal=True,
    label_visibility="collapsed"
)

if rent_mode == "Manual Rent":
    manual_rent = st.number_input(
        "Monthly Rent",
        min_value=0,
        value=3000,
        step=50
    )
    st.caption("You're overriding the automatic estimate")
else:
    manual_rent = None
    if st.session_state.result:
        est_rent = st.session_state.result.get('estimated_monthly_rent', 0)
        st.number_input(
            "Estimated Rent",
            value=float(est_rent),
            disabled=True
        )
    st.caption("Automatically estimated. Toggle to enter your own rent")

st.divider()

# TAXES SECTION
st.markdown("### Property Taxes *")

tax_mode = st.radio(
    "",
    ["Auto Estimate", "Manual"],
    horizontal=True,
    label_visibility="collapsed",
    key="tax_toggle"
)

if tax_mode == "Manual":
    manual_taxes = st.number_input(
        "Annual Taxes",
        min_value=0,
        value=5000,
        step=100
    )
    if st.session_state.result:
        suggested = st.session_state.result.get('property_tax_annual', 0)
        st.caption(f"Suggested: ${suggested:,.0f}")
else:
    manual_taxes = None
    if st.session_state.result:
        auto_tax = st.session_state.result.get('property_tax_annual', 0)
        st.number_input(
            "Annual Taxes",
            value=float(auto_tax),
            disabled=True
        )
    st.caption("Calculated automatically from county data")

st.divider()

# CALCULATE BUTTON
calculate_clicked = st.button("Calculate DSCR", type="primary", use_container_width=True)

if calculate_clicked:
    if not address:
        st.error("Please enter a property address")
    else:
        try:
            # Build parameters
            params = {
                'address': address,
                'purchase_price': purchase_price,
                'down_payment_percent': down_payment_percent / 100,
                'interest_rate_annual': interest_rate / 100,
                'term_years': term_years,
                'insurance_monthly': insurance_monthly
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
        if risk == "Golden":
            st.success(f"🏆 {risk}")
        elif risk == "Excellent":
            st.success(f"✓ {risk}")
        elif risk == "Good":
            st.info(f"✓ {risk}")
        else:  # Bad
            st.error(f"✗ {risk}")

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
        '📞 Click here to see real lender terms for this scenario'
        '</a>'
        '</div>',
        unsafe_allow_html=True
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
