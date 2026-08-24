import os, csv, random
from datetime import datetime, timedelta

def generate():
    orders = []
    order_items = []
    order_id = 1
    
    for customer_id in range(1, 1001):
        num_orders = random.randint(1, 10)
        city_id = random.randint(1, 5) # simplified
        for _ in range(num_orders):
            order_date = datetime.now() - timedelta(days=random.randint(1, 180))
            delivery_time = random.randint(10, 30)
            discount = random.randint(0, 50)
            delivery_fee = random.choice([0, 15, 30])
            
            orders.append({
                "order_id": order_id, "customer_id": customer_id, "city_id": city_id,
                "order_date": order_date.strftime("%Y-%m-%d"), "order_status": "Delivered",
                "delivery_time": delivery_time, "discount": discount, "delivery_fee": delivery_fee
            })
            
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                product_id = random.randint(1, 100)
                quantity = random.randint(1, 3)
                price = random.randint(50, 500) # simplified
                cost = int(price * 0.7)
                order_items.append({
                    "order_id": order_id, "product_id": product_id, "quantity": quantity,
                    "unit_price": price, "cost": cost
                })
            order_id += 1
            
    out_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    with open(os.path.join(out_dir, "orders.csv"), "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
        
    with open(os.path.join(out_dir, "order_items.csv"), "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=order_items[0].keys())
        writer.writeheader()
        writer.writerows(order_items)
    print("Orders and items generated.")

if __name__ == "__main__":
    generate()
