"""
South Carolina Rental Property Tax Calculator

This module provides deterministic tax calculation for South Carolina rental properties
using exact millage rates from sc_millage.json.

IMPORTANT: This module ONLY uses millage rates from sc_millage.json.
It does NOT estimate, guess, or invent any tax rates.
"""

import json
import os
import re
from typing import Dict, Optional, Any


class SCTaxCalculator:
    """
    Calculates property taxes for South Carolina rental properties using
    exact millage rates from sc_millage.json.
    """

    # SC rental property assessment ratio (6%)
    ASSESSMENT_RATIO = 0.06

    def __init__(self, millage_json_path: str = "sc_millage.json"):
        """
        Initialize the tax calculator.

        Args:
            millage_json_path: Path to the sc_millage.json file
        """
        self.millage_data = self._load_millage_data(millage_json_path)

    def _load_millage_data(self, json_path: str) -> Dict[str, float]:
        """Load millage rates from JSON file."""
        if not os.path.exists(json_path):
            # Try absolute path
            json_path = os.path.join(os.path.dirname(__file__), json_path)

        if not os.path.exists(json_path):
            raise FileNotFoundError(
                f"sc_millage.json not found. Please ensure the file exists at {json_path}"
            )

        with open(json_path, 'r') as f:
            data = json.load(f)

        return data

    def detect_county(self, address: str) -> Optional[str]:
        """
        Detect South Carolina county from address string.

        Args:
            address: Full address string

        Returns:
            County name (e.g., "Horry County") or None if not detected
        """
        if not address:
            return None

        # Normalize address
        address_upper = address.upper()

        # Check if this is a South Carolina address
        if 'SC' not in address_upper and 'SOUTH CAROLINA' not in address_upper:
            # Also check common SC zip codes (29xxx)
            if not re.search(r'\b29\d{3}\b', address):
                return None

        # List of all SC counties (without "County" suffix for matching)
        sc_counties = [
            "ABBEVILLE", "AIKEN", "ALLENDALE", "ANDERSON", "BAMBERG",
            "BARNWELL", "BEAUFORT", "BERKELEY", "CALHOUN", "CHARLESTON",
            "CHEROKEE", "CHESTER", "CHESTERFIELD", "CLARENDON", "COLLETON",
            "DARLINGTON", "DILLON", "DORCHESTER", "EDGEFIELD", "FAIRFIELD",
            "FLORENCE", "GEORGETOWN", "GREENVILLE", "GREENWOOD", "HAMPTON",
            "HORRY", "JASPER", "KERSHAW", "LANCASTER", "LAURENS",
            "LEE", "LEXINGTON", "MARION", "MARLBORO", "MCCORMICK",
            "NEWBERRY", "OCONEE", "ORANGEBURG", "PICKENS", "RICHLAND",
            "SALUDA", "SPARTANBURG", "SUMTER", "UNION", "WILLIAMSBURG", "YORK"
        ]

        # Common SC cities and their counties
        city_to_county = {
            # Major cities
            "MYRTLE BEACH": "HORRY",
            "NORTH MYRTLE BEACH": "HORRY",
            "LITTLE RIVER": "HORRY",
            "SURFSIDE BEACH": "HORRY",
            "GARDEN CITY": "HORRY",
            "PAWLEYS ISLAND": "GEORGETOWN",
            "CHARLESTON": "CHARLESTON",
            "NORTH CHARLESTON": "CHARLESTON",
            "MOUNT PLEASANT": "CHARLESTON",
            "SUMMERVILLE": "DORCHESTER",
            "COLUMBIA": "RICHLAND",
            "GREENVILLE": "GREENVILLE",
            "SPARTANBURG": "SPARTANBURG",
            "ROCK HILL": "YORK",
            "HILTON HEAD": "BEAUFORT",
            "FLORENCE": "FLORENCE",
            "AIKEN": "AIKEN",
            "ANDERSON": "ANDERSON",
            "CLEMSON": "PICKENS",
            "SIMPSONVILLE": "GREENVILLE",
            "GOOSE CREEK": "BERKELEY",
            "MAULDIN": "GREENVILLE",
            "GREER": "GREENVILLE",
            "CONWAY": "HORRY",
            # Additional Horry County cities/areas
            "SOCASTEE": "HORRY",
            "CAROLINA FOREST": "HORRY",
            "LORIS": "HORRY",
            "AYNOR": "HORRY",
            # Additional Charleston area
            "JAMES ISLAND": "CHARLESTON",
            "WEST ASHLEY": "CHARLESTON",
            "JOHNS ISLAND": "CHARLESTON",
            "FOLLY BEACH": "CHARLESTON",
            "ISLE OF PALMS": "CHARLESTON",
            "SULLIVANS ISLAND": "CHARLESTON",
            # Other cities
            "BEAUFORT": "BEAUFORT",
            "BLUFFTON": "BEAUFORT",
            "LEXINGTON": "LEXINGTON",
            "IRMO": "LEXINGTON",
            "CAYCE": "LEXINGTON",
            "WEST COLUMBIA": "LEXINGTON",
            "FORT MILL": "YORK",
            "YORK": "YORK",
            "CLOVER": "YORK",
            "GREENWOOD": "GREENWOOD",
            "SUMTER": "SUMTER",
            "ORANGEBURG": "ORANGEBURG",
            "GAFFNEY": "CHEROKEE",
            "EASLEY": "PICKENS",
            "SENECA": "OCONEE",
        }

        # First, try to match city name
        for city, county in city_to_county.items():
            if city in address_upper:
                return f"{county.title()} County"

        # Then, try to match county name directly
        for county in sc_counties:
            # Look for county name with or without "County" suffix
            if f"{county} COUNTY" in address_upper or f"{county}," in address_upper:
                return f"{county.title()} County"

        # Try to extract from common address formats
        # Format: "City, County, SC"
        county_match = re.search(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+County\s*,?\s*SC', address, re.IGNORECASE)
        if county_match:
            county_name = county_match.group(1).upper()
            if county_name in sc_counties:
                return f"{county_name.title()} County"

        return None

    def calculate_tax(
        self,
        address: str,
        value: Optional[float] = None,
        county_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate property taxes for a South Carolina rental property.

        FORMULAS (MANDATORY):
        - ASSESSMENT_RATIO = 0.06 (for rental/investment properties)
        - TAXABLE_VALUE = VALUE × ASSESSMENT_RATIO
        - ANNUAL_TAXES = TAXABLE_VALUE × MILLAGE_RATE
        - MONTHLY_TAXES = ANNUAL_TAXES / 12

        Args:
            address: Property address (used to detect county if county_name not provided)
            value: Market value or purchase price
            county_name: County name (optional, will be detected from address if not provided)

        Returns:
            Dictionary with exact structure:
            {
                "county_name": string | null,
                "millage_rate": number | null,
                "assessment_ratio": number | null,
                "taxable_value": number | null,
                "annual_taxes": number | null,
                "monthly_taxes": number | null,
                "tax_accuracy": "ok" | "county_not_found" | "missing_value"
            }
        """

        # Step 1: Detect county if not provided
        if county_name is None:
            county_name = self.detect_county(address)

        # Step 2: Check if value is valid
        if value is None or value <= 0:
            return {
                "county_name": county_name,
                "millage_rate": None,
                "assessment_ratio": None,
                "taxable_value": None,
                "annual_taxes": None,
                "monthly_taxes": None,
                "tax_accuracy": "missing_value"
            }

        # Step 3: Look up millage rate
        if county_name is None or county_name not in self.millage_data:
            return {
                "county_name": county_name,
                "millage_rate": None,
                "assessment_ratio": None,
                "taxable_value": None,
                "annual_taxes": None,
                "monthly_taxes": None,
                "tax_accuracy": "county_not_found"
            }

        millage_rate = self.millage_data[county_name]

        # Step 4: Apply formulas EXACTLY as specified
        assessment_ratio = self.ASSESSMENT_RATIO
        taxable_value = value * assessment_ratio
        annual_taxes = taxable_value * millage_rate
        monthly_taxes = annual_taxes / 12

        # Step 5: Return result in EXACT format
        return {
            "county_name": county_name,
            "millage_rate": millage_rate,
            "assessment_ratio": assessment_ratio,
            "taxable_value": taxable_value,
            "annual_taxes": annual_taxes,
            "monthly_taxes": monthly_taxes,
            "tax_accuracy": "ok"
        }


def calculate_sc_tax(address: str, value: float, county_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate South Carolina rental property tax.

    Args:
        address: Property address
        value: Market value or purchase price
        county_name: Optional county name (will be detected if not provided)

    Returns:
        Tax calculation result dictionary
    """
    calculator = SCTaxCalculator()
    return calculator.calculate_tax(address, value, county_name)


if __name__ == "__main__":
    # Test examples
    test_cases = [
        {
            "address": "123 Ocean Blvd, Myrtle Beach, SC 29577",
            "value": 400000,
            "description": "Myrtle Beach (Horry County)"
        },
        {
            "address": "456 Meeting St, Charleston, SC 29401",
            "value": 500000,
            "description": "Charleston (Charleston County)"
        },
        {
            "address": "789 Main St, Columbia, SC 29201",
            "value": 300000,
            "description": "Columbia (Richland County)"
        },
        {
            "address": "321 Palm Blvd, Little River, SC 29566",
            "value": 350000,
            "description": "Little River (Horry County)"
        },
        {
            "address": "999 Unknown St, Atlanta, GA 30301",
            "value": 400000,
            "description": "Non-SC address (should fail)"
        },
        {
            "address": "555 Beach Dr, Myrtle Beach, SC 29577",
            "value": None,
            "description": "Missing value (should fail)"
        }
    ]

    calculator = SCTaxCalculator()

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['description']}")
        print(f"Address: {test['address']}")
        print(f"Value: ${test['value']:,}" if test['value'] else "Value: None")
        print(f"{'='*60}")

        result = calculator.calculate_tax(test['address'], test['value'])

        print(json.dumps(result, indent=2))

        # Verify formulas if successful
        if result['tax_accuracy'] == 'ok':
            print(f"\nVerification:")
            print(f"  Taxable Value = ${test['value']:,} × 0.06 = ${result['taxable_value']:,.2f}")
            print(f"  Annual Taxes = ${result['taxable_value']:,.2f} × {result['millage_rate']} = ${result['annual_taxes']:,.2f}")
            print(f"  Monthly Taxes = ${result['annual_taxes']:,.2f} / 12 = ${result['monthly_taxes']:,.2f}")
