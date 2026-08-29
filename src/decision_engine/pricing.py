"""Pricing strategy and demand elasticity optimization engine."""

from typing import Any, Dict, List, Optional

import pandas as pd

from src.core.logging_config import get_logger
from src.core.types import PricingTier, ValidationError

logger = get_logger(__name__)


def get_standard_pricing_tiers() -> Dict[str, PricingTier]:
    """Returns standardized market-entry pricing strategies and elasticity assumptions."""
    return {
        "Low (Penetration)": PricingTier(
            tier_name="Low (Penetration)",
            price_multiplier=0.90,  # 10% discount to market
            demand_multiplier=1.25,  # 25% higher volume
            margin_expansion_bps=-400,
        ),
        "Medium (Competitive Parity)": PricingTier(
            tier_name="Medium (Competitive Parity)",
            price_multiplier=1.00,  # Market benchmark price
            demand_multiplier=1.00,  # Baseline volume
            margin_expansion_bps=0,
        ),
        "Premium (Margin Focus)": PricingTier(
            tier_name="Premium (Margin Focus)",
            price_multiplier=1.15,  # 15% premium
            demand_multiplier=0.80,  # 20% lower volume
            margin_expansion_bps=500,
        ),
    }


def evaluate_pricing_strategy(
    base_orders: int,
    base_aov: float,
    base_cogs_ratio: float = 0.75,
    pricing_tiers: Optional[Dict[str, PricingTier]] = None,
) -> pd.DataFrame:
    """Simulates financial outcomes across penetration, parity, and premium pricing models.

    Args:
        base_orders: Baseline annual/monthly order volume.
        base_aov: Baseline Average Order Value (INR).
        base_cogs_ratio: Cost of goods sold as percentage of revenue.
        pricing_tiers: Optional custom pricing tiers dictionary.

    Returns:
        DataFrame with projected orders, revenue, COGS, gross margin, and margin percentage.
    """
    if base_orders <= 0 or base_aov <= 0:
        raise ValidationError("Base orders and AOV must be positive values.")

    tiers = pricing_tiers or get_standard_pricing_tiers()
    logger.info(
        "Simulating pricing strategies for %d base orders at INR %.2f baseline AOV.",
        base_orders,
        base_aov,
    )

    records: List[Dict[str, Any]] = []

    for name, tier in tiers.items():
        effective_aov = base_aov * tier.price_multiplier
        effective_orders = int(base_orders * tier.demand_multiplier)
        projected_revenue = effective_orders * effective_aov
        unit_cogs = base_aov * base_cogs_ratio
        total_cogs = effective_orders * unit_cogs
        gross_profit = projected_revenue - total_cogs
        gross_margin_pct = (
            (gross_profit / projected_revenue * 100) if projected_revenue > 0 else 0.0
        )

        records.append(
            {
                "Pricing Strategy": name,
                "Price Multiplier": tier.price_multiplier,
                "Effective AOV (INR)": round(effective_aov, 2),
                "Projected Orders": effective_orders,
                "Projected Revenue (INR)": round(projected_revenue, 2),
                "Total COGS (INR)": round(total_cogs, 2),
                "Gross Profit (INR)": round(gross_profit, 2),
                "Gross Margin (%)": round(gross_margin_pct, 2),
            }
        )

    results_df = pd.DataFrame(records)
    logger.info("Pricing evaluation completed.")
    return results_df


if __name__ == "__main__":
    outcomes = evaluate_pricing_strategy(base_orders=100000, base_aov=450.0)
    print("Pricing Scenarios:\n", outcomes.to_string())
