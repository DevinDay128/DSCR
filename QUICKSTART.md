# 🚀 Quick Start Guide

Get your AI Rent & DSCR Calculator running in **under 2 minutes**!

## Choose Your Interface

### Option 1: Streamlit (Easiest! ⚡)

**Perfect for:** Quick demos, local use, sharing with team

```bash
# Install Streamlit
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

**That's it!** Your browser will automatically open to the calculator.

---

### Option 2: Flask (Professional 🎨)

**Perfect for:** Production deployment, custom branding, API access

```bash
# Install Flask
pip install flask

# Run the app
python app.py
```

**Then open:** http://localhost:5000 in your browser

---

## What You'll See

### Beautiful Web Interface
- 🏠 Enter property details (address, price, bedrooms, etc.)
- 💰 Set loan terms (down payment, interest rate, term)
- 📊 Configure operating assumptions
- 🔍 Click "Calculate" to get instant results

### Comprehensive Results
- **Estimated Rent** with confidence score and range
- **DSCR** with risk rating (Strong/Borderline/Weak)
- **Monthly Cashflow** projection
- **Financial breakdown** of all calculations
- **AI assumptions** that were made
- **Investor notes** and warnings

---

## Example Property Analysis

Try this example in the form:

```
Address: 123 Main St, Austin, TX 78701
Purchase Price: $400,000
Down Payment: 25%
Interest Rate: 7%
Term: 30 years
Bedrooms: 3
Bathrooms: 2
Square Feet: 1800
```

**Expected Results:**
- Estimated Rent: ~$3,400/month
- DSCR: ~1.03 (Weak - needs higher rent or lower price)
- Cashflow: ~$64/month (very tight!)

---

## Next Steps

### 1. Run Locally ✅
```bash
streamlit run streamlit_app.py
```

### 2. Try the Examples
```bash
python examples.py
```

### 3. Deploy to the Cloud ☁️
See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for deployment options:
- **Streamlit Cloud** (free, 1-click deploy)
- **Heroku** (free tier available)
- **AWS, Google Cloud, Azure**
- **Vercel, Render, Railway**

### 4. Use the API 🔌
```python
from ai_rent_dscr import AIRentDSCRCalculator

calculator = AIRentDSCRCalculator()
result = calculator.calculate(
    address="123 Main St, Austin, TX",
    purchase_price=400000,
    down_payment_percent=0.25,
    interest_rate_annual=0.07,
    term_years=30
)

print(f"DSCR: {result['DSCR']:.2f}")
print(f"Monthly Rent: ${result['estimated_monthly_rent']:,.0f}")
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask
```

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Port Already in Use
```bash
# For Flask, change the port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead

# For Streamlit, use:
streamlit run streamlit_app.py --server.port 8502
```

### Not Working?
1. Make sure you're in the DSCR directory
2. Check Python version: `python --version` (need 3.7+)
3. Try using `python3` instead of `python`
4. Install all dependencies: `pip install -r requirements.txt`

---

## Screenshots

### Flask Interface
```
┌─────────────────────────────────────────┐
│  🏠 AI Rent & DSCR Calculator          │
│  Estimate rental income and analyze     │
│  investment property performance         │
│                                          │
│  ⚠️ Important: This tool provides rough │
│  AI estimates for screening only         │
├─────────────────────────────────────────┤
│  📍 Property Information                │
│  Property Address: [..................] │
│  Purchase Price:   [..................] │
│                                          │
│  🏡 Property Details                    │
│  Type: [SFR ▼] Beds: [3] Baths: [2]    │
│  ...                                     │
│                                          │
│  💰 Loan Terms                          │
│  Down Payment: ○ Percentage ● Amount    │
│  ...                                     │
│                                          │
│  [      Calculate DSCR      ]           │
└─────────────────────────────────────────┘
```

### Streamlit Interface
```
┌─────────────────────────────────────────┐
│         🏠 AI Rent & DSCR Calculator    │
│  Estimate rental income and analyze...  │
│                                          │
│  [📝 Input] [📊 Results]                │
│                                          │
│  📍 Property Information                │
│  Property Address: ..................   │
│  Purchase Price:   ..................   │
│                                          │
│  🏡 Property Details (Optional)         │
│  Property Type: [Single Family ▼]       │
│  ...                                     │
│                                          │
│  [🔍 Calculate DSCR]                    │
└─────────────────────────────────────────┘
```

---

## Key Features

✨ **Smart Rent Estimation**
- AI-powered based on property value and characteristics
- Adjusts for location, condition, size, property type
- Provides confidence score and range

📊 **Complete DSCR Analysis**
- Proper loan amortization calculations
- NOI computation with operating expenses
- Risk assessment (Strong/Borderline/Weak)
- Monthly cashflow projections

⚠️ **Clear Disclaimers**
- Transparent assumptions
- Investor warnings
- Professional disclosure

🔧 **Flexible & Customizable**
- Supports various loan types
- Adjustable operating expense ratios
- Optional property details for better accuracy

---

## Share With Your Team

1. **Run Locally:** Follow steps above
2. **Share on Network:** Use your IP address (e.g., `http://192.168.1.100:5000`)
3. **Deploy Online:** Free options available (see HOSTING_GUIDE.md)

---

## Getting Help

- 📖 **Full Docs:** See [README.md](README.md)
- 🚀 **Deployment:** See [HOSTING_GUIDE.md](HOSTING_GUIDE.md)
- 🧪 **Examples:** Run `python examples.py`
- ✅ **Tests:** Run `python test_calculations.py`

---

**Ready? Let's go!**

```bash
pip install streamlit && streamlit run streamlit_app.py
```

Your calculator will be running in seconds! 🎉
