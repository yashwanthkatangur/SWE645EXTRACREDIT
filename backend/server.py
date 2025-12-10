from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import build_graph
from .state import TripState

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

class TripRequest(BaseModel):
    city: str
    budget: float

@app.post("/plan-trip")
def plan_trip(req: TripRequest):
    state = TripState(city=req.city, budget=req.budget)

    result = graph.invoke(state)   

    return {
        "weather_summary": result.get("weather_summary"),
        "activities": result.get("activities"),
        "total_cost": result.get("total_cost")
    }

@app.get("/")
def root():
    return {"message": "Trip Planner API is running!"}
