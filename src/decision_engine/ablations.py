"""Ablation studies and baseline comparison engine for decision model evaluation."""

from typing import Any, Dict, List, Optional

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import ScoringWeights
from src.decision_engine.city_scoring import calculate_city_scores

logger = get_logger(__name__)


def run_baseline_comparison(
    cities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compares the standard strategic model against naive and heuristic baselines.

    Baselines:
      1. Strategic Model: Balanced strategic MCDA weights.
      2. Uniform Baseline: Equal weight (1/6 = ~16.67%) across all 6 features.
      3. Size Heuristic: 100% weight on population/market size alone.
      4. Growth Heuristic: 100% weight on GDP economic growth rate.

    Args:
        cities_df: Input city metrics DataFrame.

    Returns:
        Comparison DataFrame with composite scores and rank shifts per city.
    """
    logger.info("Executing baseline comparison analysis...")

    strategic_weights = ScoringWeights(
        economic_growth=0.25,
        competition_inverse=0.25,
        cost_efficiency=0.15,
        demand_index=0.15,
        market_size=0.10,
        income_level=0.10,
    )
    uniform_weights = ScoringWeights(
        economic_growth=1 / 6,
        competition_inverse=1 / 6,
        cost_efficiency=1 / 6,
        demand_index=1 / 6,
        market_size=1 / 6,
        income_level=1 / 6,
    )
    size_weights = ScoringWeights(
        economic_growth=0.0,
        competition_inverse=0.0,
        cost_efficiency=0.0,
        demand_index=0.0,
        market_size=1.0,
        income_level=0.0,
    )

    strat_res = calculate_city_scores(cities_df, weights=strategic_weights)
    uni_res = calculate_city_scores(cities_df, weights=uniform_weights)
    size_res = calculate_city_scores(cities_df, weights=size_weights)

    comparison_records: List[Dict[str, Any]] = []
    for _, row in strat_res.iterrows():
        city = str(row["city"])
        uni_row = uni_res[uni_res["city"] == city].iloc[0]
        size_row = size_res[size_res["city"] == city].iloc[0]

        comparison_records.append(
            {
                "city": city,
                "strategic_score": row["composite_score"],
                "strategic_rank": int(row["rank"]),
                "uniform_score": uni_row["composite_score"],
                "uniform_rank": int(uni_row["rank"]),
                "size_heuristic_score": size_row["composite_score"],
                "size_heuristic_rank": int(size_row["rank"]),
                "rank_delta_vs_uniform": int(uni_row["rank"] - row["rank"]),
            }
        )

    results_df = pd.DataFrame(comparison_records)
    logger.info("Baseline comparison completed across %d cities.", len(results_df))
    return results_df


def run_feature_ablation_study(
    cities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Iteratively removes one scoring dimension to assess model sensitivity and feature importance.

    Args:
        cities_df: Input city metrics DataFrame.

    Returns:
        DataFrame summarizing top-ranked city and score shifts when each feature is ablated.
    """
    logger.info("Executing feature ablation sensitivity study...")

    features = [
        "economic_growth",
        "competition_inverse",
        "cost_efficiency",
        "demand_index",
        "market_size",
        "income_level",
    ]

    base_weights = ScoringWeights(
        economic_growth=0.25,
        competition_inverse=0.25,
        cost_efficiency=0.15,
        demand_index=0.15,
        market_size=0.10,
        income_level=0.10,
    )
    base_res = calculate_city_scores(cities_df, weights=base_weights)
    base_top_city = str(base_res.iloc[0]["city"])
    base_top_score = float(base_res.iloc[0]["composite_score"])

    ablation_records: List[Dict[str, Any]] = []

    for feature in features:
        weights_dict = base_weights.to_dict()
        removed_weight = weights_dict.pop(feature)
        remaining_sum = sum(weights_dict.values())

        # Normalize remaining weights so sum = 1.0
        normalized_weights: Dict[str, float] = {
            k: v / remaining_sum for k, v in weights_dict.items()
        }
        normalized_weights[feature] = 0.0

        ablated_weights = ScoringWeights(**normalized_weights)
        ablated_res = calculate_city_scores(cities_df, weights=ablated_weights)
        ablated_top_row = ablated_res.iloc[0]

        ablation_records.append(
            {
                "ablated_feature": feature,
                "removed_weight": removed_weight,
                "top_ranked_city": str(ablated_top_row["city"]),
                "top_score": float(ablated_top_row["composite_score"]),
                "score_delta": round(
                    float(ablated_top_row["composite_score"]) - base_top_score, 2
                ),
                "top_rank_preserved": str(ablated_top_row["city"]) == base_top_city,
            }
        )

    results_df = pd.DataFrame(ablation_records)
    logger.info("Feature ablation study completed.")
    return results_df


def run_ablation_pipeline(
    config: Optional[AppConfig] = None,
) -> Dict[str, pd.DataFrame]:
    """Orchestrates baseline comparison and feature ablation evaluation."""
    cfg = config or load_config()
    cities = load_dataset(f"{cfg.paths.data_processed_dir}/city_market_metrics.csv")
    return {
        "baseline_comparison": run_baseline_comparison(cities),
        "ablation_study": run_feature_ablation_study(cities),
    }


if __name__ == "__main__":
    res = run_ablation_pipeline()
    print("Baseline Comparison:\n", res["baseline_comparison"].to_string())
    print("\nFeature Ablations:\n", res["ablation_study"].to_string())
