from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RepairEstimateModel(Base):
    __tablename__ = 'repair_estimates'
    
    id = Column(Integer, primary_key=True, index=True)
    issue = Column(String, index=True)
    complexity = Column(String)
    location = Column(String)
    device = Column(String)
    price_estimate = Column(Float)
