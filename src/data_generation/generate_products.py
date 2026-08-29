"""Synthetic SKU product catalog generator with realistic cost-price margins."""

import csv
import os
import random
from typing import Optional

from src.core.logging_config import get_logger

logger = get_logger(__name__)


def generate_products(
    count: int = 100,
    seed: int = 42,
    output_dir: Optional[str] = None,
) -> str:
    """Generates synthetic SKU catalog with category mappings and unit economics.

    Args:
        count: Number of products to generate.
        seed: Random seed for reproducibility.
        output_dir: Target directory.

    Returns:
        Path to generated CSV file.
    """
    random.seed(seed)
    logger.info("Generating %d synthetic products with seed=%d...", count, seed)

    categories = {
        "Grocery": (50, 200),
        "Snacks": (20, 100),
        "Beverages": (30, 150),
        "Personal Care": (100, 500),
        "Electronics": (500, 2000),
    }

    products = []
    cat_keys = list(categories.keys())

    for i in range(1, count + 1):
        cat = random.choice(cat_keys)
        cost_range = categories[cat]
        cost = random.randint(cost_range[0], cost_range[1])
        margin_mult = random.uniform(1.15, 1.45)
        price = int(cost * margin_mult)

        products.append(
            {
                "product_id": i,
                "category": cat,
                "subcategory": f"{cat} Essentials",
                "product_name": f"{cat} Premium Item {i}",
                "unit_cost": cost,
                "selling_price": price,
            }
        )

    out_path = output_dir or os.path.join(
        os.path.dirname(__file__), "../../data/synthetic"
    )
    os.makedirs(out_path, exist_ok=True)
    file_path = os.path.join(out_path, "products.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
        writer.writeheader()
        writer.writerows(products)

    logger.info("Products dataset successfully written to %s", file_path)
    return file_path


if __name__ == "__main__":
    generate_products()
