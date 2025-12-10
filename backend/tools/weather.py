import os
import requests
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

API_KEY = os.getenv("OPENWEATHER_API_KEY")



def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url).json()

    if response.get("cod") != "200":
        return []

    daily = {}
    for entry in response["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        cond = entry["weather"][0]["description"]

        if date not in daily:
            daily[date] = {"temps": [], "conds": []}

        daily[date]["temps"].append(temp)
        daily[date]["conds"].append(cond)

    forecast = []
    for d, info in daily.items():
        forecast.append({
            "date": d,
            "avg_temp": sum(info["temps"]) / len(info["temps"]),
            "common_condition": max(set(info["conds"]), key=info["conds"].count)
        })

    return forecast[:5]


def summarize_weather(forecast):
    if not forecast:
        return "Weather data unavailable."

    temps = [day["avg_temp"] for day in forecast]
    conds = [day["common_condition"] for day in forecast]

    avg = sum(temps) / len(temps)
    unique_conditions = ", ".join(set(conds))

    return (
        f"The weather will average around {avg:.1f}°C "
        f"with typical conditions including {unique_conditions}."
    )
