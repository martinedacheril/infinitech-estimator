# app/services.py

# Sample predefined prices (you can update or expand this)
PRICE_GUIDE = {
    'cracked_screen': {
        'low': 100.0,
        'medium': 150.0,
        'high': 200.0,
    },
    'battery_replacement': {
        'low': 50.0,
        'medium': 80.0,
        'high': 120.0,
    },
    'virus_removal': {
        'low': 40.0,
        'medium': 70.0,
        'high': 100.0,
    },
}

async def get_price_estimate(issue: str, complexity: str) -> float:
    """
    Function to get the price estimate based on the issue and complexity level.
    """
    issue_data = PRICE_GUIDE.get(issue.lower())
    if issue_data:
        price = issue_data.get(complexity.lower())
        if price:
            return price
    return 0.0  # Return 0 if no match is found
