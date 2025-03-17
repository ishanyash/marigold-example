# schemas/customer.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CustomerProfile(BaseModel):
    """
    Schema for customer profile data used in email generation.
    Contains all necessary information about a customer for personalized marketing.
    """
    customer_id: str
    name: str
    tariff_type: str
    energy_usage: int
    potential_savings: int
    recommended_plan: str
    location: Optional[str] = None
    peak_usage_time: Optional[str] = None
    history_summary: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "C1234",
                "name": "John Smith",
                "tariff_type": "Standard Variable",
                "energy_usage": 320,
                "potential_savings": 15,
                "recommended_plan": "GreenFlex",
                "location": "London",
                "peak_usage_time": "Evening",
                "history_summary": "Customer for 3 years, previously inquired about solar panels"
            }
        }


