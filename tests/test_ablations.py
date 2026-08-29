"""Unit tests for baseline comparison and feature ablation studies."""

import pandas as pd

from src.decision_engine.ablations import (
    run_ablation_pipeline,
    run_baseline_comparison,
    run_feature_ablation_study,
)


def _get_mock_cities_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "city_id": 1,
                "city": "Bengaluru",
                "state": "Karnataka",
                "population": 12500000,
                "households": 3125000,
                "population_density": 4381,
                "urbanization": 100.0,
                "mpce": 6500,
                "internet_penetration": 75.0,
                "economic_growth": 8.5,
                "income_proxy": 850000,
                "ecommerce_adoption": 22.0,
            },
            {
                "city_id": 2,
                "city": "Delhi NCR",
                "state": "Delhi",
                "population": 28514000,
                "households": 7128500,
                "population_density": 11320,
                "urbanization": 97.5,
                "mpce": 5800,
                "internet_penetration": 68.0,
                "economic_growth": 7.8,
                "income_proxy": 720000,
                "ecommerce_adoption": 18.5,
            },
        ]
    )


def test_run_baseline_comparison():
    """Validates baseline comparison matrix generation."""
    cities = _get_mock_cities_df()
    res = run_baseline_comparison(cities)
    assert not res.empty
    assert "strategic_rank" in res.columns
    assert "uniform_rank" in res.columns
    assert "size_heuristic_rank" in res.columns


def test_run_feature_ablation_study():
    """Validates feature ablation metrics across all dimensions."""
    cities = _get_mock_cities_df()
    res = run_feature_ablation_study(cities)
    assert len(res) == 6
    assert "ablated_feature" in res.columns
    assert "top_ranked_city" in res.columns
    assert "top_rank_preserved" in res.columns


def test_run_ablation_pipeline():
    """Validates end-to-end ablation pipeline."""
    res = run_ablation_pipeline()
    assert "baseline_comparison" in res
    assert "ablation_study" in res
    assert not res["baseline_comparison"].empty
