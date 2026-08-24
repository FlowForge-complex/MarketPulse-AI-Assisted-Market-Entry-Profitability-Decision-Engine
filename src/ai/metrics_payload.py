import json

def get_bengaluru_payload():
    return json.dumps({
        "city": "Bengaluru",
        "score": 8.42,
        "market_size": 12000000000,
        "expected_revenue": 450000000,
        "expected_profit": 52000000,
        "break_even_month": 18,
        "competition_score": 72,
        "demand_score": 91
    }, indent=2)
