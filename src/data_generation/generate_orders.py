"""Synthetic orders and order-items transaction generator."""

import csv
import os
import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from src.core.logging_config import get_logger

logger = get_logger(__name__)


def generate_orders(
    customer_count: int = 1000,
    seed: int = 42,
    output_dir: Optional[str] = None,
) -> Tuple[str, str]:
    """Generates synthetic order transactions and order items.

    Args:
        customer_count: Number of customers placing orders.
        seed: Random seed for reproducibility.
        output_dir: Output folder.

    Returns:
        Tuple of (orders_csv_path, order_items_csv_path).
    """
    random.seed(seed)
    logger.info(
        "Generating synthetic transactions for %d customers (seed=%d)...",
        customer_count,
        seed,
    )

    orders = []
    order_items = []
    order_id = 1
    now = datetime(2026, 8, 1, tzinfo=timezone.utc)

    for customer_id in range(1, customer_count + 1):
        num_orders = random.randint(1, 10)
        city_id = random.randint(1, 5)

        for _ in range(num_orders):
            order_date = now - timedelta(days=random.randint(1, 180))
            delivery_time = random.randint(10, 30)
            discount = random.randint(0, 40)
            delivery_fee = random.choice([0, 15, 30])

            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "city_id": city_id,
                    "order_date": order_date.strftime("%Y-%m-%d"),
                    "order_status": "Delivered",
                    "delivery_time": delivery_time,
                    "discount": discount,
                    "delivery_fee": delivery_fee,
                }
            )

            num_items = random.randint(1, 5)
            for _ in range(num_items):
                product_id = random.randint(1, 100)
                quantity = random.randint(1, 3)
                price = random.randint(50, 450)
                cost = int(price * 0.72)

                order_items.append(
                    {
                        "order_id": order_id,
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price": price,
                        "cost": cost,
                    }
                )

            order_id += 1

    out_path = output_dir or os.path.join(
        os.path.dirname(__file__), "../../data/synthetic"
    )
    os.makedirs(out_path, exist_ok=True)

    orders_file = os.path.join(out_path, "orders.csv")
    items_file = os.path.join(out_path, "order_items.csv")

    with open(orders_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(orders[0].keys()))
        writer.writeheader()
        writer.writerows(orders)

    with open(items_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(order_items[0].keys()))
        writer.writeheader()
        writer.writerows(order_items)

    logger.info(
        "Generated %d orders and %d order items.", len(orders), len(order_items)
    )
    return orders_file, items_file


if __name__ == "__main__":
    generate_orders()
