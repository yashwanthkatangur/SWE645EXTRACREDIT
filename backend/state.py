from pydantic import BaseModel
from typing import List, Optional

class TripState(BaseModel):
    city: str
    budget: float
    weather: List = []
    weather_summary: Optional[str] = None
    activities: List = []
    total_cost: Optional[float] = None
