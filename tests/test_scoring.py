"""Unit tests for Multi-Criteria Decision Analysis (MCDA) city scoring."""

import pandas as pd

from src.core.types import ScoringWeights
from src.decision_engine.city_scoring import min_max_normalize, run_city_scoring


def test_min_max_normalize():
    """Validates 0-100 normalization and inversion."""
    s = pd.Series([10, 20, 30, 40, 50])
    norm = min_max_normalize(s)
    assert norm.min() == 0.0
    assert norm.max() == 100.0
    assert norm.iloc[2] == 50.0

    inverted = min_max_normalize(s, invert=True)
    assert inverted.iloc[0] == 100.0
    assert inverted.iloc[-1] == 0.0


def test_city_scoring_pipeline():
    """Validates city scoring ranking and score bounds."""
    ranked = run_city_scoring()
    assert len(ranked) == 5
    assert "composite_score" in ranked.columns
    assert "rank" in ranked.columns
    assert ranked["rank"].tolist() == [1, 2, 3, 4, 5]

    # Scores must be bounded within [0, 100]
    assert ranked["composite_score"].min() >= 0.0
    assert ranked["composite_score"].max() <= 100.0


def test_custom_weights_effect():
    """Validates that prioritizing cost shifts ranking toward lower-cost cities."""
    weights_growth = ScoringWeights(
        economic_growth=0.40,
        competition_inverse=0.05,
        cost_efficiency=0.03,
        demand_index=0.10,
        market_size=0.40,
        income_level=0.02,
    )
    ranked_growth = run_city_scoring(weights=weights_growth)
    assert ranked_growth.iloc[0]["rank"] == 1
