import pandas as pd
import os

def score_cities(weights=None):
    if weights is None:
        weights = {"Market": 0.25, "Growth": 0.20, "Demand": 0.20, "Competition": 0.15, "Cost": 0.10, "Income": 0.10}
        
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/processed")
    city_metrics = pd.read_csv(os.path.join(data_dir, "city_market_metrics.csv"))
    
    # Normalize metrics (mock logic for demonstration)
    city_metrics['score'] = (city_metrics['population'] / city_metrics['population'].max()) * 100
    city_metrics['final_score'] = city_metrics['score'] * weights["Market"] # Simplified
    
    ranked = city_metrics.sort_values(by='final_score', ascending=False)
    return ranked[['city', 'final_score']]

if __name__ == "__main__":
    print(score_cities())
