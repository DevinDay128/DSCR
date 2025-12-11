# React UI Guide - DSCR Calculator

## Overview

Brand new **clean, minimal React + TypeScript UI** that connects to your existing Python DSCR calculator backend.

## Quick Start

### 1. Install and Build (First Time Only)

```bash
./setup_react.sh
```

This will:
- Install all Node.js dependencies
- Build the React app
- Place the build in `static/dist/`

### 2. Run the App

```bash
python app_react.py
```

Open your browser to: **http://localhost:5000**

## Features

### ✨ Clean, Minimal Design
- Single-page calculator
- Mobile-first responsive design
- Airy spacing, zero clutter
- Plain white/gray background

### 📝 Smart Input Organization
- **Required inputs** shown first (address, price, HOA, down payment, interest rate, loan term)
- **Optional inputs** collapsed by default (sqft, beds, baths, property type)
- Smooth animations when expanding sections

### 🔄 Auto/Manual Toggles
- **Rent Estimate**: Toggle between auto-calculated and manual input
- **Property Taxes**: Toggle between auto (county millage) and manual
- Clean two-state pill switches

### 📊 Result Cards
- **DSCR** with color-coded risk label (Strong/Borderline/Weak)
- **Monthly Cashflow** (after mortgage, taxes, insurance, HOA)
- **Annual Taxes** with county info

### ⚡ Real-time Calculation
- Debounced auto-calculation (400ms after typing stops)
- No "Calculate" button needed
- Inline loading states

## File Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main calculator component
│   ├── App.css          # Clean, minimal styles
│   ├── main.tsx         # React entry point
│   ├── types.ts         # TypeScript interfaces
│   └── api.ts           # Backend API calls
├── index.html           # HTML template
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
└── vite.config.ts       # Vite build config

app_react.py             # Flask backend that serves React + API
setup_react.sh           # One-command setup script
```

## Development

### Run Dev Server (Hot Reload)

```bash
cd frontend
npm run dev
```

Dev server runs at: http://localhost:5173

The dev server proxies `/api` requests to `http://localhost:5000`, so make sure your Flask backend is running:

```bash
# In another terminal
python app_react.py
```

### Build for Production

```bash
cd frontend
npm run build
```

Output goes to: `static/dist/`

## API Integration

The React frontend calls your Python backend at `/api/calculate`:

**Request:**
```json
{
  "address": "Myrtle Beach, SC",
  "purchase_price": 400000,
  "down_payment_percent": 0.20,
  "interest_rate_annual": 0.07,
  "term_years": 30,
  "sqft": 1800,
  "beds": 3,
  "baths": 2,
  "property_type": "SFR"
}
```

**Response:**
```json
{
  "DSCR": 1.24,
  "risk_label": "Borderline",
  "monthly_cashflow": 412,
  "estimated_monthly_rent": 3400,
  "property_tax_annual": 4680,
  "property_tax_monthly": 390,
  "insurance_monthly": 150,
  "monthly_debt_service": 2131,
  "sc_tax_calculation": {
    "county_name": "Horry",
    "millage_rate": 0.195,
    "annual_taxes": 4680,
    "tax_accuracy": "ok"
  }
}
```

## Design Goals

The UI achieves:
- ✅ Understandable in 5 seconds
- ✅ Mobile-friendly
- ✅ Uncluttered and calm
- ✅ 100% practical, zero gimmicks
- ✅ Required inputs visible, optional inputs hidden
- ✅ Effortless rent/tax toggles
- ✅ Large, bold, easy-to-read outputs

## Tech Stack

- **React 18** - Modern UI framework
- **TypeScript** - Type safety
- **Vite** - Lightning-fast build tool
- **CSS3** - No framework dependencies, pure CSS
- **Flask** - Python backend API

## Deployment Options

### Option 1: Flask (Included)
Run `python app_react.py` - serves both React UI and API

### Option 2: Static Hosting + Separate API
1. Build: `cd frontend && npm run build`
2. Deploy `static/dist/` to any static host (Netlify, Vercel, S3, etc.)
3. Update API endpoint in `src/api.ts` to point to your Flask backend

### Option 3: Replace Streamlit
Build the React app and configure your hosting to serve it instead of Streamlit

## Troubleshooting

**"Cannot find module" errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Build fails:**
Check Node.js version: `node --version` (should be 16+)

**API calls fail:**
Make sure Flask backend is running on port 5000

**Styles not loading:**
Clear browser cache or try incognito mode

## Next Steps

1. ✅ Run `./setup_react.sh` to build
2. ✅ Run `python app_react.py` to start
3. ✅ Open http://localhost:5000
4. Test with a South Carolina address
5. Deploy to your preferred hosting platform

The calculator logic remains 100% intact - same Python backend, new beautiful frontend! 🎉
