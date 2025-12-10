from agent import build_graph
from backend.state import TripState
from dotenv import load_dotenv

load_dotenv()



def main():
    """
    CLI version of the trip planner.
    This will NOT run automatically when the backend starts.
    You can run manually using:  python main.py
    """
    city = input("Enter city: ")
    budget = float(input("Enter your budget: "))

    graph = build_graph()
    state = TripState(city=city, budget=budget)

    result = graph.invoke(state)
    print(result)


if __name__ == "__main__":
    
    main()
