# Deployment Instructions for SC Tax Calculator Feature

## Current Status

The South Carolina rental property tax calculator feature has been successfully implemented and is available on the branch:

```
claude/sc-rental-tax-calculator-01N2FFLA4wL1HoW72d57iUFB
```

All code changes have been committed and pushed to this branch.

## Streamlit Cloud Deployment Update

Your Streamlit Cloud app at https://2hy2qfismpueqzwsvpnusa.streamlit.app/ needs to be updated to deploy from the new branch.

### Steps to Update Streamlit Cloud:

1. **Log into Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Sign in with your account

2. **Access App Settings:**
   - Find your deployed app in the dashboard
   - Click on the app or the settings/menu icon (⋮)
   - Select "Settings" or "App settings"

3. **Update Branch:**
   - Look for "Branch" or "Git branch" setting
   - Change from: `claude/add-ai-rent-dscr-mode-01G8bJkzFBGqP4GQQz7zDyy1`
   - Change to: `claude/sc-rental-tax-calculator-01N2FFLA4wL1HoW72d57iUFB`
   - Save the changes

4. **Trigger Redeployment:**
   - Click "Reboot app" or "Redeploy"
   - Wait for the app to redeploy (usually takes 1-2 minutes)

5. **Verify Deployment:**
   - Visit https://2hy2qfismpueqzwsvpnusa.streamlit.app/
   - Enter a South Carolina address (e.g., "123 Ocean Blvd, Myrtle Beach, SC 29577")
   - You should see the blue notice box: "🏛️ South Carolina Property Detected"
   - The property tax rate input field should be hidden
   - After calculating, you should see SC tax details showing county, millage rate, etc.

## Alternative: Quick Test Locally

If you want to test before deploying to Streamlit Cloud:

```bash
# Make sure you're on the correct branch
git checkout claude/sc-rental-tax-calculator-01N2FFLA4wL1HoW72d57iUFB

# Run Streamlit locally
streamlit run streamlit_app.py

# Or run Flask locally
python app.py
```

Then open http://localhost:8501 (Streamlit) or http://localhost:5000 (Flask) in your browser.

## What's New in This Deployment

✅ **SC Tax Calculator Module** (`sc_tax_calculator.py`)
- Deterministic tax calculation using official SC millage rates
- Automatic county detection from address
- 6% assessment ratio applied exactly as per SC law

✅ **SC Millage Database** (`sc_millage.json`)
- All 46 SC counties with official millage rates
- Easy to update when rates change

✅ **Updated UI** (Streamlit & Flask)
- Automatic SC property detection
- Hidden/disabled tax rate input for SC properties
- Display of SC tax details (county, millage, assessment ratio)
- Informative notice about automatic calculation

✅ **Comprehensive Tests** (`test_sc_tax.py`)
- Validates all formulas and calculations
- Tests multiple SC counties
- Verifies integration with main calculator

## Features Working After Deployment

When you enter a South Carolina address:
- ❌ **User CANNOT input custom tax rate** (field is hidden)
- ✅ **Tax automatically calculated** using official SC millage rates
- ✅ **County detected** from city name or ZIP code
- ✅ **Exact formulas applied:**
  - Taxable Value = Purchase Price × 6%
  - Annual Tax = Taxable Value × County Millage Rate
  - Monthly Tax = Annual Tax ÷ 12
- ✅ **Tax details displayed** showing county, millage, assessment ratio

## Support

If the deployment doesn't work:
1. Check that the branch name is correct in Streamlit Cloud settings
2. Verify the app has access to the GitHub repository
3. Check Streamlit Cloud logs for any errors
4. Try a manual reboot of the app

## Testing the Feature

Use these test addresses to verify the SC tax calculator works:

| Address | Expected County | Expected Behavior |
|---------|----------------|-------------------|
| Myrtle Beach, SC 29577 | Horry County | Tax input hidden, millage ~192.3 mills |
| Charleston, SC 29401 | Charleston County | Tax input hidden, millage ~201.2 mills |
| Greenville, SC 29601 | Greenville County | Tax input hidden, millage ~208.9 mills |
| Austin, TX 78701 | N/A | Tax input shown (not SC) |
