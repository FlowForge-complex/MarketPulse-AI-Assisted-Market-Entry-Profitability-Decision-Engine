from city_scoring import score_cities

def run_sensitivity():
    print("Scenario A: Growth Focused")
    wA = {"Market": 0.25, "Growth": 0.30, "Demand": 0.20, "Competition": 0.10, "Cost": 0.10, "Income": 0.05}
    print(score_cities(wA))

    print("\nScenario B: Profitability Focused")
    wB = {"Market": 0.20, "Growth": 0.10, "Demand": 0.15, "Competition": 0.20, "Cost": 0.25, "Income": 0.10}
    print(score_cities(wB))

if __name__ == "__main__":
    run_sensitivity()
