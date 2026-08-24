import pandas as pd
import os

def run_eda():
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    print("Total Orders:", len(orders))
    
    # Revenue analysis
    items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))
    items['gross_revenue'] = items['quantity'] * items['unit_price']
    print("Total Gross Revenue:", items['gross_revenue'].sum())
    
    print("EDA Complete.")

if __name__ == "__main__":
    run_eda()
