"""City Attractiveness Decision Engine with Multi-Criteria Decision Analysis (MCDA)."""

import os
from typing import List, Optional

import pandas as pd

from src.analytics.eda import load_dataset
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import CityScoreResult, ModelExecutionError, ScoringWeights

logger = get_logger(__name__)


def min_max_normalize(series: pd.Series, invert: bool = False) -> pd.Series:
    """Applies Min-Max scaling to map values into a 0-100 score range.

    Args:
        series: Pandas series with numerical data.
        invert: If True, lower original values receive higher scores (e.g. costs).

    Returns:
        Series normalized to [0, 100].
    """
    s_min = series.min()
    s_max = series.max()
    if s_max == s_min:
        return pd.Series(50.0, index=series.index)

    if invert:
        scaled = (s_max - series) / (s_max - s_min) * 100.0
    else:
        scaled = (series - s_min) / (s_max - s_min) * 100.0
    return scaled


def calculate_city_scores(
    city_metrics_df: pd.DataFrame,
    weights: Optional[ScoringWeights] = None,
) -> pd.DataFrame:
    """Evaluates candidate cities using weighted multi-criteria normalization.

    Args:
        city_metrics_df: Raw demographic and economic metrics per city.
        weights: Configured criteria weights summing to 1.0.

    Returns:
        DataFrame containing normalized factor scores, composite score, and rank.
    """
    scoring_weights = weights or ScoringWeights()
    logger.info(
        "Evaluating city attractiveness using weights: %s",
        scoring_weights.to_dict(),
    )

    try:
        df = city_metrics_df.copy()

        # Normalize 6 Core Dimensions to [0, 100]
        df["market_size_score"] = min_max_normalize(df["population"])
        df["economic_growth_score"] = min_max_normalize(df["economic_growth"])
        df["demand_score"] = min_max_normalize(
            df["ecommerce_adoption"] * df["internet_penetration"]
        )
        # Higher density / competition proxy -> lower score if competition is negative
        df["competition_score"] = min_max_normalize(
            df["population_density"], invert=True
        )
        # Lower MPCE/rent index -> higher cost efficiency score
        df["cost_score"] = min_max_normalize(df["mpce"], invert=True)
        df["income_score"] = min_max_normalize(df["income_proxy"])

        # Compute Composite Weighted Score
        df["composite_score"] = (
            df["market_size_score"] * scoring_weights.market_size
            + df["economic_growth_score"] * scoring_weights.economic_growth
            + df["demand_score"] * scoring_weights.demand_index
            + df["competition_score"] * scoring_weights.competition_inverse
            + df["cost_score"] * scoring_weights.cost_efficiency
            + df["income_score"] * scoring_weights.income_level
        ).round(2)

        df["rank"] = (
            df["composite_score"].rank(ascending=False, method="min").astype(int)
        )
        df_ranked = df.sort_values(by="composite_score", ascending=False).reset_index(
            drop=True
        )

        logger.info(
            "City scoring completed. Top ranked city: %s (Score: %.2f)",
            df_ranked.iloc[0]["city"],
            df_ranked.iloc[0]["composite_score"],
        )
        return df_ranked

    except Exception as exc:
        logger.exception("Error executing city scoring: %s", exc)
        raise ModelExecutionError(f"City scoring calculation error: {exc}") from exc


def get_city_score_objects(
    df_ranked: pd.DataFrame,
) -> List[CityScoreResult]:
    """Converts ranked scoring dataframe to typed dataclass objects."""
    results: List[CityScoreResult] = []
    for _, row in df_ranked.iterrows():
        results.append(
            CityScoreResult(
                city_id=int(row["city_id"]),
                city_name=str(row["city"]),
                market_size_score=float(row["market_size_score"]),
                economic_growth_score=float(row["economic_growth_score"]),
                demand_score=float(row["demand_score"]),
                competition_score=float(row["competition_score"]),
                cost_score=float(row["cost_score"]),
                income_score=float(row["income_score"]),
                composite_score=float(row["composite_score"]),
                rank=int(row["rank"]),
            )
        )
    return results


def run_city_scoring(
    config: Optional[AppConfig] = None,
    weights: Optional[ScoringWeights] = None,
) -> pd.DataFrame:
    """Executes city scoring pipeline."""
    cfg = config or load_config()
    file_path = os.path.join(cfg.paths.data_processed_dir, "city_market_metrics.csv")
    cities_df = load_dataset(file_path)
    return calculate_city_scores(cities_df, weights=weights)


if __name__ == "__main__":
    ranked = run_city_scoring()
    print(
        "Ranked Cities:\n",
        ranked[["rank", "city", "composite_score", "demand_score", "cost_score"]],
    )
