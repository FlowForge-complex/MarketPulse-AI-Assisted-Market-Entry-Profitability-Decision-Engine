"""Exploratory Data Analysis (EDA) module for MarketPulse datasets."""

import os
from typing import Any, Dict, Optional, Type

import pandas as pd
from pydantic import BaseModel

from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import (
    CityMetricsSchema,
    CustomerIngestSchema,
    DataLoadError,
    OrderIngestSchema,
    OrderItemIngestSchema,
    validate_dataframe_schema,
)

logger = get_logger(__name__)

# Registry mapping default filename suffixes to their boundary validation schemas
_SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {
    "city_market_metrics.csv": CityMetricsSchema,
    "customers.csv": CustomerIngestSchema,
    "orders.csv": OrderIngestSchema,
    "order_items.csv": OrderItemIngestSchema,
}


def load_dataset(
    file_path: str,
    schema: Optional[Type[BaseModel]] = None,
    validate_schema: bool = True,
) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame with schema validation.

    Args:
        file_path: Absolute or relative path to CSV file.
        schema: Optional Pydantic schema model to enforce. If None, auto-detected from filename.
        validate_schema: Whether to validate rows/columns against target schema.

    Returns:
        Loaded and validated DataFrame.

    Raises:
        DataLoadError: If file does not exist, parsing fails, or schema validation fails.
    """
    if not os.path.exists(file_path):
        logger.error("Dataset not found at path: %s", file_path)
        raise DataLoadError(f"Dataset file not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
        logger.debug("Successfully loaded %d rows from %s", len(df), file_path)
    except Exception as exc:
        logger.exception("Failed to parse dataset at %s: %s", file_path, exc)
        raise DataLoadError(f"Error reading CSV {file_path}: {exc}") from exc

    if validate_schema:
        target_schema = schema
        if target_schema is None:
            base_name = os.path.basename(file_path)
            target_schema = _SCHEMA_REGISTRY.get(base_name)

        if target_schema is not None:
            validate_dataframe_schema(df, target_schema)
            logger.debug(
                "Validated %s against schema %s",
                file_path,
                target_schema.__name__,
            )

    return df


def run_eda(config: Optional[AppConfig] = None) -> Dict[str, Any]:
    """Executes exploratory analysis across transactions, customers, and cities.

    Args:
        config: Optional application configuration.

    Returns:
        Dictionary summarizing key dataset statistics and metrics.
    """
    cfg = config or load_config()
    logger.info("Initiating Exploratory Data Analysis (EDA)...")

    synthetic_dir = cfg.paths.data_synthetic_dir
    processed_dir = cfg.paths.data_processed_dir

    orders_df = load_dataset(os.path.join(synthetic_dir, "orders.csv"))
    items_df = load_dataset(os.path.join(synthetic_dir, "order_items.csv"))
    customers_df = load_dataset(os.path.join(synthetic_dir, "customers.csv"))
    cities_df = load_dataset(os.path.join(processed_dir, "city_market_metrics.csv"))

    # Compute transactional aggregations
    items_df["gross_revenue"] = items_df["quantity"] * items_df["unit_price"]
    items_df["gross_cost"] = items_df["quantity"] * items_df["cost"]
    items_df["gross_margin"] = items_df["gross_revenue"] - items_df["gross_cost"]

    total_orders = len(orders_df)
    total_customers = len(customers_df)
    total_gross_revenue = float(items_df["gross_revenue"].sum())
    total_gross_margin = float(items_df["gross_margin"].sum())
    aov = total_gross_revenue / total_orders if total_orders > 0 else 0.0
    overall_margin_pct = (
        (total_gross_margin / total_gross_revenue * 100)
        if total_gross_revenue > 0
        else 0.0
    )

    summary: Dict[str, Any] = {
        "total_cities": len(cities_df),
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_gross_revenue_inr": round(total_gross_revenue, 2),
        "total_gross_margin_inr": round(total_gross_margin, 2),
        "average_order_value_inr": round(aov, 2),
        "overall_gross_margin_pct": round(overall_margin_pct, 2),
        "customer_segments_count": customers_df["customer_segment"]
        .value_counts()
        .to_dict(),
        "city_distribution": cities_df[
            ["city", "population", "ecommerce_adoption"]
        ].to_dict(orient="records"),
    }

    logger.info(
        "EDA Complete: %d orders analyzed. Total Revenue: INR %.2f, AOV: INR %.2f, Margin: %.2f%%",
        total_orders,
        total_gross_revenue,
        aov,
        overall_margin_pct,
    )
    return summary


if __name__ == "__main__":
    results = run_eda()
    print("EDA Results Summary:", results)
