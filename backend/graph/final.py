from ..tools.budget import calculate_budget


def final_node(state):
    total = calculate_budget(state.activities)

    return {
        "activities": state.activities,
        "total_cost": total,
        "weather_summary": state.weather_summary
    }
