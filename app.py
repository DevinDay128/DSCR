"""
Flask Web Application for AI Rent and DSCR Calculator

Run with: python app.py
Then open browser to: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from ai_rent_dscr import AIRentDSCRCalculator
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page with input form."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation request and return results."""
    try:
        # Get form data
        data = request.get_json()

        # Build parameters dictionary
        params = {
            'address': data.get('address', ''),
            'purchase_price': float(data.get('purchase_price', 0))
        }

        # Optional down payment
        if data.get('down_payment_type') == 'amount' and data.get('down_payment_amount'):
            params['down_payment_amount'] = float(data['down_payment_amount'])
        elif data.get('down_payment_type') == 'percent' and data.get('down_payment_percent'):
            params['down_payment_percent'] = float(data['down_payment_percent']) / 100

        # Loan terms
        if data.get('interest_rate_annual'):
            params['interest_rate_annual'] = float(data['interest_rate_annual']) / 100
        if data.get('term_years'):
            params['term_years'] = int(data['term_years'])
        if data.get('interest_only'):
            params['interest_only'] = data['interest_only'] == 'true'

        # Property details
        if data.get('property_type'):
            params['property_type'] = data['property_type']
        if data.get('beds'):
            params['beds'] = int(data['beds'])
        if data.get('baths'):
            params['baths'] = float(data['baths'])
        if data.get('sqft'):
            params['sqft'] = int(data['sqft'])
        if data.get('condition'):
            params['condition'] = data['condition']

        # Operating assumptions
        if data.get('operating_expense_ratio'):
            params['operating_expense_ratio'] = float(data['operating_expense_ratio']) / 100

        # Calculate
        calculator = AIRentDSCRCalculator()
        result = calculator.calculate(**params)

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for direct JSON input."""
    try:
        data = request.get_json()
        calculator = AIRentDSCRCalculator()
        result = calculator.calculate(**data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print("\n" + "="*80)
    print("AI RENT AND DSCR CALCULATOR - WEB INTERFACE")
    print("="*80)
    print("\n🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press CTRL+C to stop the server\n")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
