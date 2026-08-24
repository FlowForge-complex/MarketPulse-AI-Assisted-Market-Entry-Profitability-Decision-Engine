def calculate_pricing_scenario(base_price, strategy):
    if strategy == "Low":
        return base_price * 0.9, 1.2 # Lower price, high demand
    elif strategy == "Premium":
        return base_price * 1.2, 0.7 # High price, lower demand
    return base_price, 1.0 # Medium

if __name__ == "__main__":
    print("Medium Strategy:", calculate_pricing_scenario(100, "Medium"))
