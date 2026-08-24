import pandas as pd
import os

def retention_analysis():
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    first_orders = orders.groupby('customer_id')['order_date'].min().reset_index()
    first_orders.columns = ['customer_id', 'first_order_date']
    
    orders = orders.merge(first_orders, on='customer_id')
    orders['cohort_month'] = orders['first_order_date'].dt.to_period('M')
    orders['order_month'] = orders['order_date'].dt.to_period('M')
    
    print("Retention analysis complete. Grouped by cohort_month.")

if __name__ == "__main__":
    retention_analysis()
