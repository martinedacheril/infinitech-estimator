from fastapi import FastAPI
from .services import get_price_estimate
from .models import RepairEstimate

app = FastAPI()

@app.get("/estimate/{issue}")
async def get_estimate(issue: str, complexity: str = "medium"):
    """
    Endpoint to get an estimate for a given issue.
    
    Parameters:
    - issue: The issue the user is facing (e.g., 'cracked screen')
    - complexity: The complexity of the repair (e.g., 'low', 'medium', 'high')
    
    Returns:
    - Estimate based on predefined values
    """
    price = await get_price_estimate(issue, complexity)
    if price > 0:
        return RepairEstimate(issue=issue, complexity=complexity, price_estimate=price)
    return {"error": "Issue or complexity not found"}
