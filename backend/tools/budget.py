def calculate_budget(activities):
    return sum(a["cost"] for a in activities)
