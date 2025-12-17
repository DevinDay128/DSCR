"""
SC Rental Rate Configuration
Hard-coded rates based on real SC market data by city/area

Structure: Each location has tiered $/sqft rates by property size
Target: 1800 sqft properties used as calibration benchmark
"""

# ==================================================================================
# SC RENTAL MARKET RATES BY LOCATION
# ==================================================================================
#
# Format:
# "City/Area Name": {
#     "target_1800_sqft": <monthly rent for 1800 sqft>,
#     "tier_multipliers": {size_tier: multiplier vs 1800 sqft}
# }
#
# Tier multipliers adjust from the 1800 sqft baseline:
# - small (<1000): Higher $/sqft (studios/1-beds)
# - medium (1000-1500): Slightly higher $/sqft (2-beds)
# - standard (1500-2000): Baseline - this is where 1800 sqft sits
# - large (2000-2500): Lower $/sqft (4-beds)
# - very_large (>2500): Lowest $/sqft (5+ beds)
# ==================================================================================

SC_RENTAL_RATES = {
    # =============================================================================
    # COASTAL TIER 1: Ultra-Luxury Islands
    # =============================================================================
    "Hilton Head": {
        "target_1800_sqft": 3600,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Kiawah": {
        "target_1800_sqft": 3600,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Isle of Palms": {
        "target_1800_sqft": 3600,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Seabrook": {
        "target_1800_sqft": 3600,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Sullivans Island": {
        "target_1800_sqft": 3500,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Fripp Island": {
        "target_1800_sqft": 3200,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # CHARLESTON METRO: Differentiated by neighborhood
    # =============================================================================
    "Daniel Island": {
        "target_1800_sqft": 3400,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Charleston Downtown": {
        "target_1800_sqft": 3400,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Charleston": {
        "target_1800_sqft": 2800,  # General Charleston (not downtown/premium)
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Mount Pleasant": {
        "target_1800_sqft": 2700,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "James Island": {
        "target_1800_sqft": 2500,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "West Ashley": {
        "target_1800_sqft": 2300,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Summerville": {
        "target_1800_sqft": 2200,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "North Charleston": {
        "target_1800_sqft": 2000,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # MYRTLE BEACH AREA: Beach/Tourist Markets
    # =============================================================================
    "Myrtle Beach": {
        "target_1800_sqft": 2200,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "North Myrtle Beach": {
        "target_1800_sqft": 2250,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Little River": {
        "target_1800_sqft": 2100,  # Lower than Myrtle Beach proper
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Surfside Beach": {
        "target_1800_sqft": 2100,  # Similar to Little River
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Surfside": {  # Alias for Surfside Beach
        "target_1800_sqft": 2100,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Murrells Inlet": {
        "target_1800_sqft": 2150,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Pawleys Island": {
        "target_1800_sqft": 2400,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Garden City": {
        "target_1800_sqft": 2000,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # OTHER COASTAL AREAS
    # =============================================================================
    "Beaufort": {
        "target_1800_sqft": 2300,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Edisto": {
        "target_1800_sqft": 2200,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Folly Beach": {
        "target_1800_sqft": 2800,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Georgetown": {
        "target_1800_sqft": 2000,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # COLUMBIA METRO
    # =============================================================================
    "Columbia": {
        "target_1800_sqft": 1950,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Lexington": {
        "target_1800_sqft": 1900,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Irmo": {
        "target_1800_sqft": 1850,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Forest Acres": {
        "target_1800_sqft": 2000,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # UPSTATE METROS
    # =============================================================================
    "Greenville": {
        "target_1800_sqft": 1900,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Spartanburg": {
        "target_1800_sqft": 1750,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Anderson": {
        "target_1800_sqft": 1700,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Clemson": {
        "target_1800_sqft": 1950,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Simpsonville": {
        "target_1800_sqft": 1850,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },
    "Greer": {
        "target_1800_sqft": 1800,
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    },

    # =============================================================================
    # FALLBACK: Base SC Market
    # =============================================================================
    "Default SC": {
        "target_1800_sqft": 2000,  # Conservative baseline for unlisted areas
        "tier_multipliers": {"small": 1.19, "medium": 1.09, "standard": 1.0, "large": 0.89, "very_large": 0.78}
    }
}


def get_rental_rate_for_location(address: str, sqft: int) -> dict:
    """
    Get rental rate information for a specific location and property size.

    Args:
        address: Property address (should include city/area)
        sqft: Square footage of property

    Returns:
        dict with 'location', 'rate_per_sqft', 'estimated_rent', 'tier'
    """
    address_upper = address.upper()

    # Determine size tier
    if sqft < 1000:
        size_tier = "small"
    elif sqft < 1500:
        size_tier = "medium"
    elif sqft < 2000:
        size_tier = "standard"
    elif sqft < 2500:
        size_tier = "large"
    else:
        size_tier = "very_large"

    # Match location (order matters - check specific areas before general ones)
    location_data = None
    matched_location = None

    # Check for specific matches first
    location_checks = [
        # Ultra-luxury coastal
        ("HILTON HEAD", "Hilton Head"),
        ("KIAWAH", "Kiawah"),
        ("ISLE OF PALMS", "Isle of Palms"),
        ("SEABROOK", "Seabrook"),
        ("SULLIVANS ISLAND", "Sullivans Island"),
        ("FRIPP ISLAND", "Fripp Island"),

        # Charleston - specific to general
        ("DANIEL ISLAND", "Daniel Island"),
        ("FOLLY BEACH", "Folly Beach"),
        ("JAMES ISLAND", "James Island"),
        ("WEST ASHLEY", "West Ashley"),
        ("MOUNT PLEASANT", "Mount Pleasant"),
        ("SUMMERVILLE", "Summerville"),
        ("NORTH CHARLESTON", "North Charleston"),
        # Check for downtown keywords
        (["DOWNTOWN", "PENINSULA", "BATTERY", "WATERFRONT"], "Charleston Downtown"),
        ("CHARLESTON", "Charleston"),  # General Charleston last

        # Myrtle Beach area
        ("NORTH MYRTLE", "North Myrtle Beach"),
        ("LITTLE RIVER", "Little River"),
        ("SURFSIDE", "Surfside"),
        ("MURRELLS INLET", "Murrells Inlet"),
        ("PAWLEYS ISLAND", "Pawleys Island"),
        ("GARDEN CITY", "Garden City"),
        ("MYRTLE BEACH", "Myrtle Beach"),

        # Other coastal
        ("BEAUFORT", "Beaufort"),
        ("EDISTO", "Edisto"),
        ("GEORGETOWN", "Georgetown"),

        # Columbia
        ("FOREST ACRES", "Forest Acres"),
        ("LEXINGTON", "Lexington"),
        ("IRMO", "Irmo"),
        ("COLUMBIA", "Columbia"),

        # Upstate
        ("SIMPSONVILLE", "Simpsonville"),
        ("GREER", "Greer"),
        ("CLEMSON", "Clemson"),
        ("SPARTANBURG", "Spartanburg"),
        ("ANDERSON", "Anderson"),
        ("GREENVILLE", "Greenville"),
    ]

    for check, location_name in location_checks:
        if isinstance(check, list):
            # Multiple keywords (for Charleston Downtown)
            if any(keyword in address_upper for keyword in check):
                location_data = SC_RENTAL_RATES[location_name]
                matched_location = location_name
                break
        else:
            # Single keyword
            if check in address_upper:
                location_data = SC_RENTAL_RATES[location_name]
                matched_location = location_name
                break

    # Fallback to default
    if not location_data:
        location_data = SC_RENTAL_RATES["Default SC"]
        matched_location = "Default SC"

    # Calculate rate
    baseline_rent_1800 = location_data["target_1800_sqft"]
    tier_multiplier = location_data["tier_multipliers"][size_tier]

    # Calculate $/sqft for this tier
    # Start with 1800 sqft baseline rate, then adjust for size tier
    baseline_rate_per_sqft = baseline_rent_1800 / 1800
    adjusted_rate_per_sqft = baseline_rate_per_sqft * tier_multiplier

    # Calculate estimated rent
    estimated_rent = sqft * adjusted_rate_per_sqft

    return {
        "location": matched_location,
        "rate_per_sqft": round(adjusted_rate_per_sqft, 2),
        "estimated_rent": round(estimated_rent, 2),
        "size_tier": size_tier,
        "baseline_1800_sqft": baseline_rent_1800
    }
