"""Unit tests for cohort retention analysis."""

import pandas as pd
import pytest

from src.analytics.retention import calculate_cohort_retention, run_retention_analysis


def test_cohort_retention_structure():
    """Validates structure and calculations of cohort matrix."""
    matrix = run_retention_analysis()

    assert not matrix.empty
    assert 0 in matrix.columns  # Month 0 (acquisition month)
    # Month 0 retention must always be 100%
    for val in matrix[0].dropna():
        assert val == pytest.approx(100.0)


def test_synthetic_cohort_calculation():
    """Validates retention calculation logic on controlled mock data."""
    mock_orders = pd.DataFrame(
        [
            {"customer_id": 1, "order_date": "2026-01-15"},
            {"customer_id": 1, "order_date": "2026-02-10"},
            {"customer_id": 2, "order_date": "2026-01-20"},
        ]
    )
    res = calculate_cohort_retention(mock_orders)
    # Cohort 2026-01 has 2 customers, 1 active in month 1 -> 50%
    assert res.loc[pd.Period("2026-01", "M"), 0] == 100.0
    assert res.loc[pd.Period("2026-01", "M"), 1] == 50.0
