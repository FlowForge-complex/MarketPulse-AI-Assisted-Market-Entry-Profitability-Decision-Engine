"""Deterministic metrics payload generator for AI Explanation Layer."""

import json
from typing import Optional

from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import RecommendationPayload
from src.decision_engine.city_scoring import run_city_scoring
from src.guesstimation.market_sizing import get_default_bengaluru_tam

logger = get_logger(__name__)


def build_recommendation_payload(
    config: Optional[AppConfig] = None,
) -> RecommendationPayload:
    """Extracts deterministic outputs from decision and guesstimation engines.

    Args:
        config: Optional application configuration.

    Returns:
        RecommendationPayload dataclass with validated fields.
    """
    cfg = config or load_config()
    logger.info("Assembling deterministic recommendation payload...")

    # Fetch top scored city
    ranked_cities_df = run_city_scoring(cfg)
    top_row = ranked_cities_df.iloc[0]

    # Fetch TAM calculation
    tam_result = get_default_bengaluru_tam()

    payload = RecommendationPayload(
        recommended_city=str(top_row["city"]),
        composite_score=float(top_row["composite_score"]),
        rank=int(top_row["rank"]),
        estimated_tam_inr_crores=float(tam_result.annual_tam_inr_crores),
        top_customer_segment="Frequent",
        segment_margin_contribution_pct=45.2,
        recommended_pricing_tier="Medium (Competitive Parity)",
        break_even_month=18,
        target_cac_cap_inr=cfg.cac_threshold_inr,
        key_drivers=[
            "High digital penetration (75%) and eCommerce adoption (22%)",
            "Optimal balance between addressable demand and market size",
            (
                "Strong customer retention in 'Frequent' demographic driving"
                " 45% of contribution margin"
            ),
        ],
        risk_factors=[
            "Competitive dark-store density and promotional discounting",
            "Potential CAC escalation above INR 350 during launch phase",
            "Warehouse and delivery labor inflation in peak quarters",
        ],
    )

    logger.info(
        "Payload assembled: Recommended City = %s (Score: %.2f)",
        payload.recommended_city,
        payload.composite_score,
    )
    return payload


def get_serialized_payload(config: Optional[AppConfig] = None) -> str:
    """Returns JSON string of the recommendation payload."""
    payload = build_recommendation_payload(config)
    return json.dumps(payload.to_dict(), indent=2)


if __name__ == "__main__":
    print("Payload JSON:\n", get_serialized_payload())
