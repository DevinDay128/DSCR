export interface CalculatorInputs {
  address: string;
  purchase_price: number;
  hoa_monthly: number;
  down_payment_percent: number;
  interest_rate_annual: number;
  term_years: number;

  // Optional
  sqft?: number;
  beds?: number;
  baths?: number;
  property_type?: string;

  // Rent
  manual_rent?: number;
  use_manual_rent: boolean;

  // Taxes
  manual_taxes?: number;
  use_manual_taxes: boolean;
}

export interface CalculationResult {
  DSCR: number;
  risk_label: string;
  monthly_cashflow: number;
  estimated_monthly_rent: number;
  property_tax_annual: number;
  property_tax_monthly: number;
  insurance_monthly: number;
  monthly_debt_service: number;
  sc_tax_calculation?: {
    county_name: string;
    millage_rate: number;
    annual_taxes: number;
    tax_accuracy: string;
  };
}
