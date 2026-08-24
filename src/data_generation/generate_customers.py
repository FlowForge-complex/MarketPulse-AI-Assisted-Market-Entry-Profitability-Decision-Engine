import os, csv, random
from datetime import datetime, timedelta

def generate():
    cities = {1: "Bengaluru", 2: "Mumbai", 3: "Delhi NCR", 4: "Hyderabad", 5: "Pune"}
    segments = ["Premium", "Frequent", "Budget", "Occasional", "At-Risk"]
    
    customers = []
    for i in range(1, 1001):
        city_id = random.choice(list(cities.keys()))
        signup_date = datetime.now() - timedelta(days=random.randint(10, 365))
        age_group = random.choice(["18-25", "26-35", "36-45", "46-60"])
        segment = random.choice(segments)
        
        customers.append({
            "customer_id": i, "city_id": city_id, "signup_date": signup_date.strftime("%Y-%m-%d"),
            "age_group": age_group, "customer_segment": segment
        })
    
    out_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    with open(os.path.join(out_dir, "customers.csv"), "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    print("Customers generated.")

if __name__ == "__main__":
    generate()
