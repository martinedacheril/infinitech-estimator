from typing import Optional
from sqlalchemy.orm import Session
from .models import RepairEstimateModel

# Example price data for different issues, complexity levels, and device types
issue_prices = {
    "cracked screen": {
        "low": {"phone": 100, "laptop": 150, "desktop": 180},
        "medium": {"phone": 200, "laptop": 250, "desktop": 300},
        "high": {"phone": 300, "laptop": 350, "desktop": 400},
    },
    "battery replacement": {
        "low": {"phone": 80, "laptop": 120, "desktop": 150},
        "medium": {"phone": 150, "laptop": 200, "desktop": 250},
        "high": {"phone": 220, "laptop": 270, "desktop": 320},
    },
    "overheating": {
        "low": {"phone": 50, "laptop": 100, "desktop": 120},
        "medium": {"phone": 120, "laptop": 150, "desktop": 180},
        "high": {"phone": 180, "laptop": 220, "desktop": 250},
    },
}

# Location-based pricing
location_multiplier = {
    "new_york": 1.2,  # 20% higher for New York
    "san_francisco": 1.15,  # 15% higher for SF
    "los_angeles": 1.1,  # 10% higher for LA
    "default": 1.0  # Standard price for other areas
}

async def get_price_estimate(issue: str, complexity: str = "medium", location: str = "default", device: str = "phone") -> float:
    """
    Returns the price estimate based on the issue, complexity, location, and device type.
    
    Parameters:
    - issue: The issue the user is facing (e.g., 'cracked screen')
    - complexity: The complexity of the repair (e.g., 'low', 'medium', 'high')
    - location: The location of the customer (e.g., 'new_york', 'san_francisco')
    - device: The device type (e.g., 'phone', 'laptop', 'desktop')
    
    Returns:
    - Estimated price or 0 if not found.
    """
    issue_info = issue_prices.get(issue.lower())
    if issue_info:
        base_price = issue_info.get(complexity.lower(), {}).get(device.lower(), 0)
        if base_price == 0:
            return 0
        # Apply location multiplier
        location_factor = location_multiplier.get(location.lower(), location_multiplier["default"])
        return base_price * location_factor
    return 0

async def save_estimate(db: Session, issue: str, complexity: str, location: str, device: str, price_estimate: float):
    """
    Saves the repair estimate to the database.
    """
    estimate = RepairEstimateModel(
        issue=issue,
        complexity=complexity,
        location=location,
        device=device,
        price_estimate=price_estimate
    )
    db.add(estimate)
    db.commit()
    db.refresh(estimate)
    return estimate
