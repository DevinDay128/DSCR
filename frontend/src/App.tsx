import { useState, useEffect } from 'react';
import './App.css';
import type { CalculatorInputs, CalculationResult } from './types';
import { calculateDSCR } from './api';

function App() {
  const [inputs, setInputs] = useState<CalculatorInputs>({
    address: '',
    purchase_price: 400000,
    hoa_monthly: 0,
    down_payment_percent: 20,
    interest_rate_annual: 7.0,
    term_years: 30,
    use_manual_rent: false,
    use_manual_taxes: false,
  });

  const [result, setResult] = useState<CalculationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showOptional, setShowOptional] = useState(false);

  // Debounced calculation
  useEffect(() => {
    if (!inputs.address || inputs.purchase_price <= 0) {
      return;
    }

    const timeout = setTimeout(() => {
      performCalculation();
    }, 400);

    return () => clearTimeout(timeout);
  }, [inputs]);

  const performCalculation = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await calculateDSCR(inputs);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Calculation failed');
    } finally {
      setLoading(false);
    }
  };

  const updateInput = (field: keyof CalculatorInputs, value: any) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="app">
      <div className="calculator-card">
        <h1 className="calculator-title">DSCR Calculator</h1>
        <p className="calculator-subtitle">
          Analyze investment property performance in seconds
        </p>

        {/* Required Inputs */}
        <div className="section">
          <div className="section-title">Required Inputs</div>
          <div className="input-grid">
            <div className="input-group">
              <label className="input-label">Property Address</label>
              <input
                type="text"
                className="input-field"
                placeholder="123 Main St, City, SC"
                value={inputs.address}
                onChange={(e) => updateInput('address', e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Purchase Price</label>
              <input
                type="number"
                className="input-field"
                placeholder="400000"
                value={inputs.purchase_price}
                onChange={(e) => updateInput('purchase_price', parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Monthly HOA</label>
              <input
                type="number"
                className="input-field"
                placeholder="0"
                value={inputs.hoa_monthly}
                onChange={(e) => updateInput('hoa_monthly', parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Down Payment (%)</label>
              <div className="slider-container">
                <input
                  type="range"
                  className="slider"
                  min="0"
                  max="40"
                  step="1"
                  value={inputs.down_payment_percent}
                  onChange={(e) => updateInput('down_payment_percent', parseFloat(e.target.value))}
                />
                <span className="slider-value">{inputs.down_payment_percent}%</span>
              </div>
            </div>

            <div className="input-group">
              <label className="input-label">Interest Rate (%)</label>
              <input
                type="number"
                className="input-field"
                placeholder="7.0"
                step="0.1"
                value={inputs.interest_rate_annual}
                onChange={(e) => updateInput('interest_rate_annual', parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Loan Term (Years)</label>
              <input
                type="number"
                className="input-field"
                placeholder="30"
                value={inputs.term_years}
                onChange={(e) => updateInput('term_years', parseInt(e.target.value) || 30)}
              />
            </div>
          </div>
        </div>

        {/* Optional Inputs */}
        <div className="optional-section">
          <div className="optional-header" onClick={() => setShowOptional(!showOptional)}>
            <span className="optional-title">Optional inputs (improve accuracy)</span>
            <span className="optional-toggle">{showOptional ? '▲ Hide' : '▼ Show'}</span>
          </div>

          {showOptional && (
            <div className="optional-content">
              <div className="input-grid">
                <div className="input-group">
                  <label className="input-label">Square Feet</label>
                  <input
                    type="number"
                    className="input-field"
                    placeholder="1800"
                    value={inputs.sqft || ''}
                    onChange={(e) => updateInput('sqft', parseInt(e.target.value) || undefined)}
                  />
                  <span className="input-hint">Helps estimate rent more accurately</span>
                </div>

                <div className="input-group">
                  <label className="input-label">Bedrooms</label>
                  <input
                    type="number"
                    className="input-field"
                    placeholder="3"
                    value={inputs.beds || ''}
                    onChange={(e) => updateInput('beds', parseInt(e.target.value) || undefined)}
                  />
                  <span className="input-hint">Optional — improves rent estimate</span>
                </div>

                <div className="input-group">
                  <label className="input-label">Bathrooms</label>
                  <input
                    type="number"
                    className="input-field"
                    placeholder="2"
                    step="0.5"
                    value={inputs.baths || ''}
                    onChange={(e) => updateInput('baths', parseFloat(e.target.value) || undefined)}
                  />
                  <span className="input-hint">Optional — improves rent estimate</span>
                </div>

                <div className="input-group">
                  <label className="input-label">Property Type</label>
                  <select
                    className="input-field"
                    value={inputs.property_type || ''}
                    onChange={(e) => updateInput('property_type', e.target.value || undefined)}
                  >
                    <option value="">Select...</option>
                    <option value="SFR">Single Family</option>
                    <option value="Condo">Condo</option>
                    <option value="Townhouse">Townhome</option>
                    <option value="Multi-family">Multi-Family</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Rent Section */}
        <div className="toggle-section">
          <div className="toggle-header">
            <span className="toggle-title">Rent Estimate</span>
            <div className="toggle-switch">
              <div
                className={`toggle-option ${!inputs.use_manual_rent ? 'active' : ''}`}
                onClick={() => updateInput('use_manual_rent', false)}
              >
                Auto Estimate
              </div>
              <div
                className={`toggle-option ${inputs.use_manual_rent ? 'active' : ''}`}
                onClick={() => updateInput('use_manual_rent', true)}
              >
                Manual Rent
              </div>
            </div>
          </div>

          <div className="toggle-input-group">
            <input
              type="number"
              className="toggle-input"
              placeholder="Monthly rent"
              value={inputs.use_manual_rent ? (inputs.manual_rent || '') : (result?.estimated_monthly_rent || '')}
              onChange={(e) => updateInput('manual_rent', parseFloat(e.target.value) || undefined)}
              disabled={!inputs.use_manual_rent}
            />
            <span className="input-hint">
              {inputs.use_manual_rent
                ? "You're overriding the automatic estimate"
                : 'Automatically estimated. Toggle to enter your own rent'}
            </span>
          </div>
        </div>

        {/* Taxes Section */}
        <div className="toggle-section">
          <div className="toggle-header">
            <span className="toggle-title">Property Taxes</span>
            <div className="toggle-switch">
              <div
                className={`toggle-option ${!inputs.use_manual_taxes ? 'active' : ''}`}
                onClick={() => updateInput('use_manual_taxes', false)}
              >
                Auto Estimate
              </div>
              <div
                className={`toggle-option ${inputs.use_manual_taxes ? 'active' : ''}`}
                onClick={() => updateInput('use_manual_taxes', true)}
              >
                Manual
              </div>
            </div>
          </div>

          <div className="toggle-input-group">
            <input
              type="number"
              className="toggle-input"
              placeholder="Annual taxes"
              value={inputs.use_manual_taxes ? (inputs.manual_taxes || '') : (result?.property_tax_annual || '')}
              onChange={(e) => updateInput('manual_taxes', parseFloat(e.target.value) || undefined)}
              disabled={!inputs.use_manual_taxes}
            />
            <span className="input-hint">
              {inputs.use_manual_taxes
                ? `Suggested: $${result?.property_tax_annual?.toFixed(0) || '—'}`
                : 'Calculated automatically from county data'}
            </span>
          </div>
        </div>

        {loading && <div className="loading">Calculating...</div>}
        {error && <div className="error">{error}</div>}
      </div>

      {/* Results */}
      {result && !loading && (
        <>
          <div className="result-cards">
            <div className="result-card">
              <div className="result-label">DSCR</div>
              <div className="result-value">{result.DSCR.toFixed(2)}</div>
              <div className={`risk-badge risk-${result.risk_label.toLowerCase()}`}>
                {result.risk_label}
              </div>
            </div>

            <div className="result-card">
              <div className="result-label">Monthly Cashflow</div>
              <div className="result-value">
                ${Math.abs(result.monthly_cashflow).toFixed(0)}
              </div>
              <div className="result-subtext">
                After mortgage, taxes, insurance, and HOA
              </div>
            </div>

            <div className="result-card">
              <div className="result-label">Annual Taxes</div>
              <div className="result-value">
                ${result.property_tax_annual.toFixed(0)}
              </div>
              <div className="result-subtext">
                {result.sc_tax_calculation?.tax_accuracy === 'ok'
                  ? `${result.sc_tax_calculation.county_name} County`
                  : 'Based on your settings'}
              </div>
            </div>
          </div>

          <div className="summary">
            At your inputs, this property shows a DSCR of {result.DSCR.toFixed(2)} and approximately
            ${Math.abs(result.monthly_cashflow).toFixed(0)}/month {result.monthly_cashflow >= 0 ? 'positive' : 'negative'} cashflow.
          </div>
        </>
      )}
    </div>
  );
}

export default App;
