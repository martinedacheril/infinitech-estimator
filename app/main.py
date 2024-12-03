from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .services import get_price_estimate, save_estimate
from .database import get_db

app = FastAPI()

# Pydantic model to represent the input data from the user
class RepairEstimateRequest(BaseModel):
    issue: str
    complexity: str = "medium"  # default value
    location: str = "default"  # default value
    device: str = "phone"  # default value

# Pydantic model for the response
class RepairEstimate(BaseModel):
    issue: str
    complexity: str
    location: str
    device: str
    price_estimate: float

@app.post("/estimate/")
async def create_estimate(request: RepairEstimateRequest, db: Session = Depends(get_db)):
    """
    Endpoint to get an estimate for a repair job and save the estimate to the database.
    
    Parameters:
    - request: The body of the request containing issue, complexity, location, and device
    
    Returns:
    - Repair estimate based on the data
    """
    price = await get_price_estimate(request.issue, request.complexity, request.location, request.device)
    if price > 0:
        # Save the estimate to the database
        saved_estimate = await save_estimate(db, request.issue, request.complexity, request.location, request.device, price)
        return RepairEstimate(
            issue=saved_estimate.issue,
            complexity=saved_estimate.complexity,
            location=saved_estimate.location,
            device=saved_estimate.device,
            price_estimate=saved_estimate.price_estimate
        )
    raise HTTPException(status_code=400, detail="Invalid issue, complexity, or device.")
