"""
South Carolina Rental Property Tax Calculator

This module provides DETERMINISTIC tax calculations for South Carolina rental properties.
It uses ONLY the millage rates found in sc_millage.json and applies the SC rental property
tax formulas EXACTLY as specified.

IMPORTANT: This module NEVER invents, estimates, assumes, or replaces any millage rate.
"""

import json
import os
import re
from typing import Dict, Any, Optional


class SCTaxCalculator:
    """
    Deterministic tax calculator for South Carolina rental properties.

    This calculator:
    - Detects SC county from address
    - Looks up exact millage rate from sc_millage.json
    - Applies SC rental property tax formulas exactly
    - Returns null if county is not found
    - NEVER invents or estimates tax rates
    """

    # SC rental property assessment ratio (6%)
    ASSESSMENT_RATIO = 0.06

    def __init__(self, millage_file_path: Optional[str] = None):
        """
        Initialize the SC tax calculator.

        Args:
            millage_file_path: Path to sc_millage.json file (optional)
        """
        if millage_file_path is None:
            # Default to sc_millage.json in same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            millage_file_path = os.path.join(current_dir, 'sc_millage.json')

        self.millage_file_path = millage_file_path
        self.millage_data = self._load_millage_data()

    def _load_millage_data(self) -> Dict[str, Any]:
        """Load millage data from JSON file."""
        try:
            with open(self.millage_file_path, 'r') as f:
                data = json.load(f)
                return data.get('counties', {})
        except FileNotFoundError:
            print(f"WARNING: Millage file not found at {self.millage_file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"WARNING: Invalid JSON in millage file {self.millage_file_path}")
            return {}

    def _detect_county_from_address(self, address: str) -> Optional[str]:
        """
        Detect South Carolina county name from address.

        Args:
            address: Property address string

        Returns:
            County name (e.g., "Horry County") or None if not detected
        """
        if not address:
            return None

        # Normalize address to uppercase for matching
        address_upper = address.upper()

        # Check if address contains "SC" or "SOUTH CAROLINA"
        if 'SC' not in address_upper and 'SOUTH CAROLINA' not in address_upper:
            return None

        # SC ZIP code patterns (29000-29999)
        zip_match = re.search(r'\b29\d{3}\b', address)

        # Common SC city to county mappings
        city_to_county = {
            'CHARLESTON': 'Charleston County',
            'COLUMBIA': 'Richland County',
            'GREENVILLE': 'Greenville County',
            'MYRTLE BEACH': 'Horry County',
            'LITTLE RIVER': 'Horry County',
            'NORTH MYRTLE BEACH': 'Horry County',
            'SURFSIDE BEACH': 'Horry County',
            'GARDEN CITY': 'Horry County',
            'PAWLEYS ISLAND': 'Georgetown County',
            'HILTON HEAD': 'Beaufort County',
            'HILTON HEAD ISLAND': 'Beaufort County',
            'ROCK HILL': 'York County',
            'MOUNT PLEASANT': 'Charleston County',
            'SUMMERVILLE': 'Dorchester County',
            'NORTH CHARLESTON': 'Charleston County',
            'SPARTANBURG': 'Spartanburg County',
            'FLORENCE': 'Florence County',
            'ANDERSON': 'Anderson County',
            'AIKEN': 'Aiken County',
            'SUMTER': 'Sumter County',
            'GOOSE CREEK': 'Berkeley County',
            'LEXINGTON': 'Lexington County',
            'CLEMSON': 'Pickens County',
            'BEAUFORT': 'Beaufort County',
            'CONWAY': 'Horry County',
            'GREER': 'Greenville County',
            'EASLEY': 'Pickens County',
            'SIMPSONVILLE': 'Greenville County',
            'HANAHAN': 'Berkeley County',
            'MAULDIN': 'Greenville County',
            'BLUFFTON': 'Beaufort County',
            'WEST COLUMBIA': 'Lexington County',
            'CAYCE': 'Lexington County',
            'IRMO': 'Lexington County',
            'FOLLY BEACH': 'Charleston County',
            'ISLE OF PALMS': 'Charleston County',
            'SULLIVAN\'S ISLAND': 'Charleston County',
            'JOHNS ISLAND': 'Charleston County',
            'JAMES ISLAND': 'Charleston County',
            'DANIEL ISLAND': 'Charleston County',
            'KIAWAH ISLAND': 'Charleston County',
            'SEABROOK ISLAND': 'Charleston County',
        }

        # Check for city matches
        for city, county in city_to_county.items():
            if city in address_upper:
                return county

        # Check if county name is explicitly mentioned
        for county_name in self.millage_data.keys():
            # Remove "County" suffix for matching
            county_base = county_name.replace(' County', '').upper()
            # Look for county name in address
            if county_base in address_upper:
                return county_name

        # If we have a SC ZIP but couldn't determine county, return None
        # (Do NOT guess or estimate)
        return None

    def calculate_sc_rental_tax(
        self,
        address: str,
        property_value: float
    ) -> Dict[str, Any]:
        """
        Calculate South Carolina rental property taxes using ONLY millage from JSON.

        This method follows the EXACT formula:
        1. TAXABLE_VALUE = VALUE × ASSESSMENT_RATIO (0.06)
        2. ANNUAL_TAXES = TAXABLE_VALUE × MILLAGE_RATE
        3. MONTHLY_TAXES = ANNUAL_TAXES / 12

        Args:
            address: Property address
            property_value: Market value or purchase price

        Returns:
            Dictionary with tax calculation results in the EXACT required format:
            {
                "county_name": str | null,
                "millage_rate": float | null,
                "assessment_ratio": float | null,
                "taxable_value": float | null,
                "annual_taxes": float | null,
                "monthly_taxes": float | null,
                "tax_accuracy": "ok" | "county_not_found" | "missing_value"
            }
        """
        # Validate inputs
        if not property_value or property_value <= 0:
            return {
                "county_name": None,
                "millage_rate": None,
                "assessment_ratio": None,
                "taxable_value": None,
                "annual_taxes": None,
                "monthly_taxes": None,
                "tax_accuracy": "missing_value"
            }

        # Detect county from address
        county_name = self._detect_county_from_address(address)

        if not county_name:
            return {
                "county_name": None,
                "millage_rate": None,
                "assessment_ratio": None,
                "taxable_value": None,
                "annual_taxes": None,
                "monthly_taxes": None,
                "tax_accuracy": "county_not_found"
            }

        # Look up millage rate from JSON
        county_data = self.millage_data.get(county_name)

        if not county_data or 'millage_rate' not in county_data:
            return {
                "county_name": county_name,
                "millage_rate": None,
                "assessment_ratio": None,
                "taxable_value": None,
                "annual_taxes": None,
                "monthly_taxes": None,
                "tax_accuracy": "county_not_found"
            }

        millage_rate = county_data['millage_rate']

        # Apply SC rental property tax formulas EXACTLY
        # Formula 1: TAXABLE_VALUE = VALUE × ASSESSMENT_RATIO
        taxable_value = property_value * self.ASSESSMENT_RATIO

        # Formula 2: ANNUAL_TAXES = TAXABLE_VALUE × MILLAGE_RATE
        annual_taxes = taxable_value * millage_rate

        # Formula 3: MONTHLY_TAXES = ANNUAL_TAXES / 12
        monthly_taxes = annual_taxes / 12

        # Return EXACT format required
        return {
            "county_name": county_name,
            "millage_rate": millage_rate,
            "assessment_ratio": self.ASSESSMENT_RATIO,
            "taxable_value": taxable_value,
            "annual_taxes": annual_taxes,
            "monthly_taxes": monthly_taxes,
            "tax_accuracy": "ok"
        }


def calculate_sc_tax(address: str, property_value: float) -> Dict[str, Any]:
    """
    Convenience function to calculate SC rental property tax.

    Args:
        address: Property address
        property_value: Market value or purchase price

    Returns:
        Tax calculation result dictionary
    """
    calculator = SCTaxCalculator()
    return calculator.calculate_sc_rental_tax(address, property_value)


if __name__ == "__main__":
    # Example usage and testing
    calculator = SCTaxCalculator()

    # Test 1: Horry County (Myrtle Beach area)
    print("Test 1: Myrtle Beach, SC")
    result = calculator.calculate_sc_rental_tax(
        address="123 Ocean Blvd, Myrtle Beach, SC 29577",
        property_value=400000
    )
    print(json.dumps(result, indent=2))
    print()

    # Test 2: Charleston County
    print("Test 2: Charleston, SC")
    result = calculator.calculate_sc_rental_tax(
        address="456 King St, Charleston, SC 29401",
        property_value=500000
    )
    print(json.dumps(result, indent=2))
    print()

    # Test 3: County not found
    print("Test 3: Non-SC address")
    result = calculator.calculate_sc_rental_tax(
        address="789 Main St, Austin, TX 78701",
        property_value=400000
    )
    print(json.dumps(result, indent=2))
    print()

    # Test 4: Missing value
    print("Test 4: Missing value")
    result = calculator.calculate_sc_rental_tax(
        address="123 Ocean Blvd, Myrtle Beach, SC 29577",
        property_value=0
    )
    print(json.dumps(result, indent=2))
