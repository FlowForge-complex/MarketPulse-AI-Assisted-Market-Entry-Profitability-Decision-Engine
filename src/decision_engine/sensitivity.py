"""Sensitivity and Scenario Analysis engine for strategic decision testing."""

import os
from typing import Any, Dict, List, Optional

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import ScoringWeights, SensitivityScenario
from src.decision_engine.city_scoring import calculate_city_scores

logger = get_logger(__name__)


def get_standard_scenarios() -> List[SensitivityScenario]:
    """Returns predefined strategic management scenarios for sensitivity analysis."""
    return [
        SensitivityScenario(
            scenario_name="Balanced (Base Case)",
            description="Equalized trade-off between growth velocity and unit profitability.",
            weights=ScoringWeights(
                economic_growth=0.25,
                competition_inverse=0.25,
                cost_efficiency=0.15,
                demand_index=0.15,
                market_size=0.10,
                income_level=0.10,
            ),
        ),
        SensitivityScenario(
            scenario_name="Growth Aggressive",
            description="Prioritizes total addressable demand and GDP growth trajectory.",
            weights=ScoringWeights(
                economic_growth=0.30,
                competition_inverse=0.05,
                cost_efficiency=0.05,
                demand_index=0.20,
                market_size=0.35,
                income_level=0.05,
            ),
        ),
        SensitivityScenario(
            scenario_name="Profitability & Margin Focused",
            description="Prioritizes operating cost containment and high household purchasing power.",
            weights=ScoringWeights(
                economic_growth=0.10,
                competition_inverse=0.15,
                cost_efficiency=0.25,
                demand_index=0.15,
                market_size=0.15,
                income_level=0.20,
            ),
        ),
        SensitivityScenario(
            scenario_name="Low Competitive Intensity",
            description="Avoids entrenched competitors to protect acquisition CAC.",
            weights=ScoringWeights(
                economic_growth=0.15,
                competition_inverse=0.35,
                cost_efficiency=0.10,
                demand_index=0.20,
                market_size=0.15,
                income_level=0.05,
            ),
        ),
    ]


def run_multi_scenario_sensitivity(
    cities_df: pd.DataFrame,
    scenarios: Optional[List[SensitivityScenario]] = None,
) -> pd.DataFrame:
    """Executes city scoring across multiple strategic scenarios and builds a comparison table.

    Args:
        cities_df: Demographic and economic metrics DataFrame.
        scenarios: List of scenarios to evaluate.

    Returns:
        DataFrame showing composite scores and ranks per city across all scenarios.
    """
    scenario_list = scenarios or get_standard_scenarios()
    logger.info(
        "Executing sensitivity analysis across %d scenarios.", len(scenario_list)
    )

    comparison_records: Dict[str, Dict[str, Any]] = {}

    for scenario in scenario_list:
        scored = calculate_city_scores(cities_df, weights=scenario.weights)
        for _, row in scored.iterrows():
            city = str(row["city"])
            if city not in comparison_records:
                comparison_records[city] = {"City": city}
            comparison_records[city][f"{scenario.scenario_name} Score"] = row[
                "composite_score"
            ]
            comparison_records[city][f"{scenario.scenario_name} Rank"] = int(
                row["rank"]
            )

    results_df = pd.DataFrame(list(comparison_records.values()))
    logger.info("Sensitivity analysis successfully computed.")
    return results_df


def run_sensitivity_pipeline(
    config: Optional[AppConfig] = None,
) -> pd.DataFrame:
    """Orchestrates sensitivity pipeline execution."""
    cfg = config or load_config()
    cities_path = os.path.join(cfg.paths.data_processed_dir, "city_market_metrics.csv")
    cities = load_dataset(cities_path)
    return run_multi_scenario_sensitivity(cities)


if __name__ == "__main__":
    sensitivity_table = run_sensitivity_pipeline()
    print("Scenario Comparison Matrix:\n", sensitivity_table.to_string())
