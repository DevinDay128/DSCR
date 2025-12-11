# DSCR Calculator - React Frontend

Clean, minimal React + TypeScript UI for the DSCR Calculator.

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

## Development

Run development server with hot reload:
```bash
npm run dev
```

The app will be available at http://localhost:5173

## Build for Production

Build the React app:
```bash
npm run build
```

This builds the app and places the output in `../static/dist/`

## Run with Flask Backend

After building:
```bash
cd ..
python app_react.py
```

Open http://localhost:5000

## Features

- **Clean, minimal UI** - Simple single-page design
- **Mobile-first** - Fully responsive
- **Auto-calculation** - Updates as you type (debounced)
- **Smart toggles** - Auto/Manual rent and tax estimates
- **Collapsible optional inputs** - Keep the UI uncluttered
- **Real-time results** - DSCR, cashflow, and taxes

## Tech Stack

- React 18
- TypeScript
- Vite
- CSS3 (no framework dependencies)
