"""Unit tests for strategic scenario sensitivity engine."""

import pytest

from src.decision_engine.sensitivity import (
    get_standard_scenarios,
    run_sensitivity_pipeline,
)


def test_standard_scenarios_weights():
    """Validates that all predefined scenarios have valid weights summing to 1.0."""
    scenarios = get_standard_scenarios()
    assert len(scenarios) >= 3
    for sc in scenarios:
        total = sum(sc.weights.to_dict().values())
        assert total == pytest.approx(1.0, abs=1e-4)


def test_sensitivity_pipeline_matrix():
    """Validates output comparison matrix across all scenarios."""
    matrix = run_sensitivity_pipeline()
    assert not matrix.empty
    assert "City" in matrix.columns
    assert any("Rank" in col for col in matrix.columns)
    assert any("Score" in col for col in matrix.columns)
