import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ..state import TripState

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

def planner_node(state: TripState):

    
    weather_text = "\n".join(
        [f"{w['date']} → {w['avg_temp']}°C, {w['common_condition']}" for w in state.weather]
    )

    max_cost = round(state.budget * 0.95, 2)

    prompt = f"""
You are an intelligent trip planner AI.

Your tasks:
1. Use the 5-day weather forecast to choose activities appropriate for the conditions.
   - If temperatures are below 10°C: avoid long outdoor events.
   - If raining or overcast: prioritize museums, indoor tours, food experiences.
   - If sunny and warm: allow outdoor parks, walks, beaches.
2. You MUST generate exactly 5 activities.
3. The **total combined cost of all 5 activities MUST NOT exceed {max_cost}**.
4. Return strictly valid JSON — no text outside JSON.

User Inputs:
City: {state.city}
Budget: {state.budget}

Weather Forecast:
{weather_text}

JSON OUTPUT FORMAT:
{{
  "activities": [
    {{"name": "Activity 1", "cost": 20}},
    {{"name": "Activity 2", "cost": 15}},
    {{"name": "Activity 3", "cost": 40}},
    {{"name": "Activity 4", "cost": 25}},
    {{"name": "Activity 5", "cost": 30}}
  ],
  "total_cost": 130
}}

Rules:
- EXACTLY 5 activities.
- Total cost ≤ {max_cost}.
- Activities must match weather.
- Output ONLY JSON.
"""

    raw = llm.invoke(prompt).content.strip()

    
    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()

    try:
        data = json.loads(raw)
    except Exception as e:
        print("LLM OUTPUT ERROR:", raw)
        raise e

    return {
        "activities": data["activities"],
        "total_cost": data.get("total_cost", sum(a["cost"] for a in data["activities"])),
        "weather_summary": state.weather_summary  
    }
