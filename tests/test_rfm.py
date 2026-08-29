"""Unit tests for RFM customer segmentation and margin analysis."""

import pandas as pd
import pytest

from src.analytics.rfm import compute_rfm_scores, run_rfm_analysis


def test_rfm_scoring_and_segmentation():
    """Validates RFM quantile scores and assigned customer segments."""
    rfm_df, summary_df = run_rfm_analysis()

    assert len(rfm_df) == 1000
    assert "recency_days" in rfm_df.columns
    assert "frequency" in rfm_df.columns
    assert "monetary" in rfm_df.columns
    assert "r_score" in rfm_df.columns
    assert "assigned_segment" in rfm_df.columns

    # Verify score ranges
    assert rfm_df["r_score"].min() >= 1 and rfm_df["r_score"].max() <= 5
    assert rfm_df["f_score"].min() >= 1 and rfm_df["f_score"].max() <= 5
    assert rfm_df["m_score"].min() >= 1 and rfm_df["m_score"].max() <= 5

    # Check segment summary
    assert len(summary_df) > 0
    assert "margin_contribution_pct" in summary_df.columns
    assert summary_df["margin_contribution_pct"].sum() == pytest.approx(100.0, abs=1.0)


def test_rfm_monetary_monotonicity():
    """Validates higher spend increases customer contribution margin."""
    orders = pd.DataFrame(
        [
            {"order_id": 1, "customer_id": 101, "order_date": "2026-07-01"},
            {"order_id": 2, "customer_id": 102, "order_date": "2026-07-01"},
        ]
    )
    items = pd.DataFrame(
        [
            {
                "order_id": 1,
                "quantity": 1,
                "unit_price": 500,
                "cost": 300,
            },
            {
                "order_id": 2,
                "quantity": 5,
                "unit_price": 500,
                "cost": 300,
            },
        ]
    )
    scored = compute_rfm_scores(orders, items)
    m1 = scored.loc[scored["customer_id"] == 101, "monetary"].values[0]
    m2 = scored.loc[scored["customer_id"] == 102, "monetary"].values[0]
    assert m2 > m1
