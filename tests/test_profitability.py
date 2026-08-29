"""Unit tests for unit economics and profitability analysis."""

import pandas as pd

from src.analytics.profitability import (
    calculate_category_profitability,
    run_profitability_analysis,
)


def test_category_profitability_calculations():
    """Validates category margin metrics."""
    items = pd.DataFrame(
        [
            {
                "order_id": 1,
                "product_id": 10,
                "quantity": 2,
                "unit_price": 100,
                "cost": 70,
            },
            {
                "order_id": 2,
                "product_id": 20,
                "quantity": 1,
                "unit_price": 200,
                "cost": 120,
            },
        ]
    )
    products = pd.DataFrame(
        [
            {"product_id": 10, "category": "Snacks", "subcategory": "Chips"},
            {"product_id": 20, "category": "Grocery", "subcategory": "Oil"},
        ]
    )
    res = calculate_category_profitability(items, products)
    assert len(res) == 2
    snacks = res[res["category"] == "Snacks"].iloc[0]
    assert snacks["total_revenue"] == 200
    assert snacks["total_cogs"] == 140
    assert snacks["gross_profit"] == 60
    assert snacks["gross_margin_pct"] == 30.0


def test_run_profitability_pipeline():
    """Validates end-to-end profitability pipeline execution."""
    cat_df, city_df = run_profitability_analysis()
    assert not cat_df.empty
    assert not city_df.empty
    assert "contribution_margin" in city_df.columns
    assert "gross_margin_pct" in cat_df.columns
