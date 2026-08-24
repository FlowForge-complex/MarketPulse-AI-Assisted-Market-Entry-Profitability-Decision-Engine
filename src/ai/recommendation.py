import os
from metrics_payload import get_bengaluru_payload
from prompts import EXPLANATION_PROMPT

def get_recommendation_explanation():
    payload = get_bengaluru_payload()
    prompt = EXPLANATION_PROMPT.format(metrics_json=payload)
    print("--- Sending to LLM API (Mock) ---")
    print(prompt)
    print("--- Mock LLM Response ---")
    print("Recommendation: Enter Bengaluru first using the Medium Pricing strategy.")
    print("Why: It offers the strongest combination of addressable demand (91) and market size.")
    print("Economics: Expected break-even occurs in Month 18 under the base case.")
    print("Key risk: Competitive intensity (72).")

if __name__ == "__main__":
    get_recommendation_explanation()
