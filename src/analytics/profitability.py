import pandas as pd
import os

def profitability_analysis():
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))
    products = pd.read_csv(os.path.join(data_dir, "products.csv"))
    
    merged = items.merge(products, on='product_id')
    merged['gross_profit'] = (merged['unit_price'] - merged['cost']) * merged['quantity']
    
    category_profit = merged.groupby('category')['gross_profit'].sum().sort_values(ascending=False)
    print("Profitability by category:")
    print(category_profit)

if __name__ == "__main__":
    profitability_analysis()
