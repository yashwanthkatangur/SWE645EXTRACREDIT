from langgraph.graph import StateGraph

from .state import TripState
from .tools.weather import get_weather
from .tools.budget import calculate_budget
from .graph.planner import planner_node
from .graph.final import final_node


def summarize_weather(weather):
    if isinstance(weather, list) and len(weather) > 0:
        temps = [d["avg_temp"] for d in weather]
        conds = [d["common_condition"] for d in weather]

        avg = sum(temps) / len(temps)
        common = max(set(conds), key=conds.count)

        return f"Expect average temperature around {avg:.1f}°C with mostly {common} conditions."

    return "Weather data unavailable."


def build_graph():
    graph = StateGraph(TripState)

    
    def weather_node(state):
        w = get_weather(state.city)
        summary = summarize_weather(w)
        return {"weather": w, "weather_summary": summary}

    graph.add_node("get_weather", weather_node)

    
    graph.add_node("planner", planner_node)

    
    graph.add_node("final", final_node)

    
    graph.set_entry_point("get_weather")
    graph.add_edge("get_weather", "planner")
    graph.add_edge("planner", "final")

    return graph.compile()
