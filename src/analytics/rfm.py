"""Recency, Frequency, Monetary (RFM) Customer Segmentation module."""

import os
from typing import Optional, Tuple

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import ModelExecutionError

logger = get_logger(__name__)


def compute_rfm_scores(orders_df: pd.DataFrame, items_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates recency, frequency, monetary metrics and assigns RFM tiers.

    Args:
        orders_df: Orders header dataframe.
        items_df: Order line items dataframe.

    Returns:
        DataFrame containing customer_id, recency_days, frequency, monetary, and segment.
    """
    logger.info("Computing customer RFM matrices...")
    try:
        # Calculate order monetary values
        items_df["item_total"] = items_df["quantity"] * items_df["unit_price"]
        items_df["item_cost"] = items_df["quantity"] * items_df["cost"]
        order_totals = (
            items_df.groupby("order_id")
            .agg(
                order_value=("item_total", "sum"),
                order_cost=("item_cost", "sum"),
            )
            .reset_index()
        )

        orders_merged = orders_df.merge(order_totals, on="order_id", how="left")
        orders_merged["order_date"] = pd.to_datetime(orders_merged["order_date"])

        snapshot_date = orders_merged["order_date"].max() + pd.Timedelta(days=1)

        rfm = (
            orders_merged.groupby("customer_id")
            .agg(
                last_order=("order_date", "max"),
                frequency=("order_id", "count"),
                monetary=("order_value", "sum"),
                total_cost=("order_cost", "sum"),
            )
            .reset_index()
        )

        rfm["recency_days"] = (snapshot_date - rfm["last_order"]).dt.days
        rfm["contribution_margin"] = rfm["monetary"] - rfm["total_cost"]

        # 1-5 Scoring using quantiles with rank fallback for ties
        rfm["r_score"] = pd.qcut(
            rfm["recency_days"].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1]
        ).astype(int)
        rfm["f_score"] = pd.qcut(
            rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]
        ).astype(int)
        rfm["m_score"] = pd.qcut(
            rfm["monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]
        ).astype(int)

        rfm["rfm_composite"] = (
            rfm["r_score"].astype(str)
            + rfm["f_score"].astype(str)
            + rfm["m_score"].astype(str)
        )

        def assign_segment(row: pd.Series) -> str:
            r, f, m = row["r_score"], row["f_score"], row["m_score"]
            if r >= 4 and f >= 4 and m >= 4:
                return "Frequent"
            if m >= 4 and (r >= 3 or f >= 3):
                return "Premium"
            if r <= 2 and (f >= 3 or m >= 3):
                return "At-Risk"
            if f <= 2 and m <= 2:
                return "Budget"
            return "Occasional"

        rfm["assigned_segment"] = rfm.apply(assign_segment, axis=1)
        logger.info("RFM Segmentation completed across %d customers.", len(rfm))
        return rfm

    except Exception as exc:
        logger.exception("Failed executing RFM calculation: %s", exc)
        raise ModelExecutionError(f"RFM processing error: {exc}") from exc


def get_segment_profitability_summary(
    rfm_df: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregates revenue, margin, and contribution percentage by segment."""
    summary = (
        rfm_df.groupby("assigned_segment")
        .agg(
            customer_count=("customer_id", "count"),
            total_revenue=("monetary", "sum"),
            total_margin=("contribution_margin", "sum"),
            avg_aov=("monetary", "mean"),
        )
        .reset_index()
    )
    total_margin_pool = summary["total_margin"].sum()
    summary["margin_contribution_pct"] = (
        (summary["total_margin"] / total_margin_pool * 100).round(2)
        if total_margin_pool > 0
        else 0.0
    )
    return summary.sort_values(by="total_margin", ascending=False)


def run_rfm_analysis(
    config: Optional[AppConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Orchestrates end-to-end RFM analysis pipeline."""
    cfg = config or load_config()
    orders_path = os.path.join(cfg.paths.data_synthetic_dir, "orders.csv")
    items_path = os.path.join(cfg.paths.data_synthetic_dir, "order_items.csv")

    orders = load_dataset(orders_path)
    items = load_dataset(items_path)

    rfm_df = compute_rfm_scores(orders, items)
    summary_df = get_segment_profitability_summary(rfm_df)
    return rfm_df, summary_df


if __name__ == "__main__":
    _, summary = run_rfm_analysis()
    print("Segment Summary:\n", summary)
