import type { CalculatorInputs, CalculationResult } from './types';

export async function calculateDSCR(inputs: CalculatorInputs): Promise<CalculationResult> {
  const payload = {
    address: inputs.address,
    purchase_price: inputs.purchase_price,
    down_payment_percent: inputs.down_payment_percent / 100,
    interest_rate_annual: inputs.interest_rate_annual / 100,
    term_years: inputs.term_years,
    ...(inputs.sqft && { sqft: inputs.sqft }),
    ...(inputs.beds && { beds: inputs.beds }),
    ...(inputs.baths && { baths: inputs.baths }),
    ...(inputs.property_type && { property_type: inputs.property_type }),
  };

  const response = await fetch('/api/calculate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Calculation failed');
  }

  return response.json();
}
