"""Profitability and unit economics analysis module."""

import os
from typing import Optional, Tuple

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import ModelExecutionError

logger = get_logger(__name__)


def calculate_category_profitability(
    items_df: pd.DataFrame, products_df: pd.DataFrame
) -> pd.DataFrame:
    """Calculates revenue, COGS, gross profit, and margin % by product category."""
    logger.info("Computing product category profitability...")
    try:
        merged = items_df.merge(
            products_df[["product_id", "category", "subcategory"]],
            on="product_id",
            how="left",
        )
        merged["revenue"] = merged["quantity"] * merged["unit_price"]
        merged["cogs"] = merged["quantity"] * merged["cost"]
        merged["gross_profit"] = merged["revenue"] - merged["cogs"]

        category_summary = (
            merged.groupby("category")
            .agg(
                total_units_sold=("quantity", "sum"),
                total_revenue=("revenue", "sum"),
                total_cogs=("cogs", "sum"),
                gross_profit=("gross_profit", "sum"),
            )
            .reset_index()
        )

        category_summary["gross_margin_pct"] = (
            category_summary["gross_profit"] / category_summary["total_revenue"] * 100
        ).round(2)

        return category_summary.sort_values(by="gross_profit", ascending=False)

    except Exception as exc:
        logger.exception("Error in category profitability calculation: %s", exc)
        raise ModelExecutionError(f"Category profitability error: {exc}") from exc


def calculate_city_contribution_margin(
    orders_df: pd.DataFrame,
    items_df: pd.DataFrame,
    cities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculates contribution margins per city accounting for delivery fees and discounts."""
    logger.info("Computing city contribution margins...")
    try:
        items_df["item_revenue"] = items_df["quantity"] * items_df["unit_price"]
        items_df["item_cogs"] = items_df["quantity"] * items_df["cost"]

        order_rollup = (
            items_df.groupby("order_id")
            .agg(
                order_revenue=("item_revenue", "sum"),
                order_cogs=("item_cogs", "sum"),
            )
            .reset_index()
        )

        merged_orders = orders_df.merge(order_rollup, on="order_id", how="left")
        merged_orders["net_order_revenue"] = (
            merged_orders["order_revenue"]
            + merged_orders["delivery_fee"]
            - merged_orders["discount"]
        )
        merged_orders["order_contribution_margin"] = (
            merged_orders["net_order_revenue"] - merged_orders["order_cogs"]
        )

        city_perf = (
            merged_orders.groupby("city_id")
            .agg(
                total_orders=("order_id", "count"),
                gross_merchandise_value=("order_revenue", "sum"),
                net_revenue=("net_order_revenue", "sum"),
                cogs=("order_cogs", "sum"),
                total_delivery_fees=("delivery_fee", "sum"),
                total_discounts=("discount", "sum"),
                contribution_margin=("order_contribution_margin", "sum"),
            )
            .reset_index()
        )

        city_perf = city_perf.merge(
            cities_df[["city_id", "city"]], on="city_id", how="left"
        )
        city_perf["contribution_margin_pct"] = (
            city_perf["contribution_margin"] / city_perf["net_revenue"] * 100
        ).round(2)

        return city_perf.sort_values(by="contribution_margin", ascending=False)

    except Exception as exc:
        logger.exception("Error in city contribution margin calculation: %s", exc)
        raise ModelExecutionError(f"City margin calculation error: {exc}") from exc


def run_profitability_analysis(
    config: Optional[AppConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Executes full profitability and margin analysis."""
    cfg = config or load_config()
    items = load_dataset(os.path.join(cfg.paths.data_synthetic_dir, "order_items.csv"))
    products = load_dataset(os.path.join(cfg.paths.data_synthetic_dir, "products.csv"))
    orders = load_dataset(os.path.join(cfg.paths.data_synthetic_dir, "orders.csv"))
    cities = load_dataset(
        os.path.join(cfg.paths.data_processed_dir, "city_market_metrics.csv")
    )

    category_df = calculate_category_profitability(items, products)
    city_df = calculate_city_contribution_margin(orders, items, cities)
    return category_df, city_df


if __name__ == "__main__":
    cat_df, city_df = run_profitability_analysis()
    print("Category Margins:\n", cat_df)
    print("City Margins:\n", city_df)
