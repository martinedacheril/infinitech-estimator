from pydantic import BaseModel

class RepairEstimate(BaseModel):
    issue: str
    complexity: str
    price_estimate: float
