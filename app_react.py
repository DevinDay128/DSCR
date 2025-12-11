"""
Flask API + React Frontend for AI Rent and DSCR Calculator

Run with: python app_react.py
Then open browser to: http://localhost:5000
"""

from flask import Flask, send_from_directory, jsonify, request
from ai_rent_dscr import AIRentDSCRCalculator
import os

app = Flask(__name__, static_folder='static/dist', static_url_path='')

@app.route('/')
def serve_react():
    """Serve the React app."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for DSCR calculation."""
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
    print("AI RENT AND DSCR CALCULATOR - REACT UI")
    print("="*80)
    print("\n🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press CTRL+C to stop the server\n")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
