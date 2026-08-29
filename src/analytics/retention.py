"""Cohort retention and customer lifetime repeat purchase analysis."""

import os
from typing import Optional

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import ModelExecutionError

logger = get_logger(__name__)


def calculate_cohort_retention(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Computes month-over-month cohort retention rates.

    Args:
        orders_df: DataFrame with customer_id and order_date columns.

    Returns:
        DataFrame representing cohort matrix with retention percentages.
    """
    logger.info("Computing customer cohort retention matrix...")
    try:
        df = orders_df.copy()
        df["order_date"] = pd.to_datetime(df["order_date"])
        df["order_month"] = df["order_date"].dt.to_period("M")

        # Determine each customer's first cohort month
        cohort_min = df.groupby("customer_id")["order_month"].min().reset_index()
        cohort_min.columns = ["customer_id", "cohort_month"]

        merged = df.merge(cohort_min, on="customer_id")
        merged["cohort_index"] = (
            merged["order_month"].dt.year - merged["cohort_month"].dt.year
        ) * 12 + (merged["order_month"].dt.month - merged["cohort_month"].dt.month)

        cohort_counts = (
            merged.groupby(["cohort_month", "cohort_index"])["customer_id"]
            .nunique()
            .reset_index()
        )

        cohort_pivot = cohort_counts.pivot(
            index="cohort_month", columns="cohort_index", values="customer_id"
        )

        cohort_size = cohort_pivot.iloc[:, 0]
        retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100

        logger.info(
            "Cohort retention matrix built for %d monthly cohorts.",
            len(retention_matrix),
        )
        return retention_matrix.round(2)

    except Exception as exc:
        logger.exception("Error computing cohort retention: %s", exc)
        raise ModelExecutionError(f"Cohort retention error: {exc}") from exc


def run_retention_analysis(
    config: Optional[AppConfig] = None,
) -> pd.DataFrame:
    """Executes end-to-end retention workflow."""
    cfg = config or load_config()
    orders_path = os.path.join(cfg.paths.data_synthetic_dir, "orders.csv")
    orders = load_dataset(orders_path)
    return calculate_cohort_retention(orders)


if __name__ == "__main__":
    matrix = run_retention_analysis()
    print("Retention Matrix (%):\n", matrix)
