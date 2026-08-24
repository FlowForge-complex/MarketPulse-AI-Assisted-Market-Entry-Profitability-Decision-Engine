import pandas as pd
import os

def calculate_rfm():
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))
    
    # Simple monetary
    order_values = items.groupby('order_id').apply(lambda x: (x['quantity'] * x['unit_price']).sum()).reset_index(name='order_value')
    orders_val = orders.merge(order_values, on='order_id')
    
    rfm = orders_val.groupby('customer_id').agg({
        'order_date': 'max',
        'order_id': 'count',
        'order_value': 'sum'
    }).reset_index()
    
    rfm.columns = ['customer_id', 'last_order_date', 'frequency', 'monetary']
    print("RFM Calculated. Sample:")
    print(rfm.head())

if __name__ == "__main__":
    calculate_rfm()
