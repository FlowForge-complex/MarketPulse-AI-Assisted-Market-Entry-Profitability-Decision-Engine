"""Unit tests for pricing strategy and elasticity simulations."""

import pytest

from src.core.types import ValidationError
from src.decision_engine.pricing import evaluate_pricing_strategy


def test_pricing_strategy_evaluation():
    """Validates pricing scenario simulations and margin outputs."""
    res = evaluate_pricing_strategy(
        base_orders=10000, base_aov=500.0, base_cogs_ratio=0.70
    )
    assert len(res) == 3
    assert "Pricing Strategy" in res.columns
    assert "Projected Revenue (INR)" in res.columns
    assert "Gross Margin (%)" in res.columns

    # Verify Premium tier has highest margin %
    premium = res[res["Pricing Strategy"].str.contains("Premium")].iloc[0]
    low = res[res["Pricing Strategy"].str.contains("Low")].iloc[0]
    assert premium["Gross Margin (%)"] > low["Gross Margin (%)"]


def test_pricing_invalid_inputs():
    """Validates exception when zero or negative orders/AOV are passed."""
    with pytest.raises(ValidationError):
        evaluate_pricing_strategy(base_orders=-10, base_aov=500.0)

    with pytest.raises(ValidationError):
        evaluate_pricing_strategy(base_orders=100, base_aov=0.0)
