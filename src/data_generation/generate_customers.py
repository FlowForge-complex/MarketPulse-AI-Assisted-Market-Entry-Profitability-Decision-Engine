"""Synthetic customer demographics generator with reproducible random seed."""

import csv
import os
import random
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.core.logging_config import get_logger

logger = get_logger(__name__)


def generate_customers(
    count: int = 1000,
    seed: int = 42,
    output_dir: Optional[str] = None,
) -> str:
    """Generates synthetic customer demographic profiles.

    Args:
        count: Number of customer profiles to generate.
        seed: Random seed for reproducibility.
        output_dir: Destination directory for the CSV file.

    Returns:
        Absolute path to generated CSV file.
    """
    random.seed(seed)
    logger.info(
        "Generating %d synthetic customer profiles with seed=%d...", count, seed
    )

    cities = {
        1: "Bengaluru",
        2: "Mumbai",
        3: "Delhi NCR",
        4: "Hyderabad",
        5: "Pune",
    }
    segments = ["Premium", "Frequent", "Budget", "Occasional", "At-Risk"]
    age_groups = ["18-25", "26-35", "36-45", "46-60"]

    now = datetime(2026, 8, 1, tzinfo=timezone.utc)
    customers = []

    for i in range(1, count + 1):
        city_id = random.choice(list(cities.keys()))
        signup_date = now - timedelta(days=random.randint(10, 365))
        age_group = random.choice(age_groups)
        segment = random.choice(segments)

        customers.append(
            {
                "customer_id": i,
                "city_id": city_id,
                "signup_date": signup_date.strftime("%Y-%m-%d"),
                "age_group": age_group,
                "customer_segment": segment,
            }
        )

    out_path = output_dir or os.path.join(
        os.path.dirname(__file__), "../../data/synthetic"
    )
    os.makedirs(out_path, exist_ok=True)
    file_path = os.path.join(out_path, "customers.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
        writer.writeheader()
        writer.writerows(customers)

    logger.info("Customers dataset successfully written to %s", file_path)
    return file_path


if __name__ == "__main__":
    generate_customers()
