import os, csv, random

def generate():
    categories = {"Grocery": (50, 200), "Snacks": (20, 100), "Beverages": (30, 150), "Personal Care": (100, 500), "Electronics": (500, 2000)}
    products = []
    for i in range(1, 101):
        cat = random.choice(list(categories.keys()))
        cost = random.randint(categories[cat][0], categories[cat][1])
        price = int(cost * random.uniform(1.1, 1.5))
        products.append({
            "product_id": i, "category": cat, "subcategory": cat + " Item",
            "product_name": f"{cat} Product {i}", "unit_cost": cost, "selling_price": price
        })
        
    out_dir = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
    with open(os.path.join(out_dir, "products.csv"), "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print("Products generated.")

if __name__ == "__main__":
    generate()
