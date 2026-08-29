"""AI Explanation Layer generating executive recommendations from deterministic metrics."""

from typing import Any, Dict, Optional

from src.ai.metrics_payload import (
    build_recommendation_payload,
    get_serialized_payload,
)
from src.ai.prompts import EXPLANATION_USER_PROMPT_TEMPLATE
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger
from src.core.types import RecommendationPayload

logger = get_logger(__name__)


def generate_structured_explanation(
    payload: RecommendationPayload,
) -> str:
    """Generates an executive consulting recommendation narrative from deterministic metrics.

    Args:
        payload: Validated RecommendationPayload dataclass.

    Returns:
        Formatted multi-paragraph strategic recommendation text.
    """
    logger.info(
        "Synthesizing strategic recommendation for %s...",
        payload.recommended_city,
    )

    explanation = f"""================================================================================
EXECUTIVE STRATEGIC RECOMMENDATION
================================================================================

1. PRIMARY DIRECTIVE:
   Initiate phase-1 market entry in {payload.recommended_city.upper()} utilizing the {payload.recommended_pricing_tier} strategy.
   • Composite Attractiveness Score: {payload.composite_score:.2f}/100.0 (Rank #{payload.rank})
   • Estimated City TAM: INR {payload.estimated_tam_inr_crores:.2f} Crores (~INR {payload.estimated_tam_inr_crores / 100:.2f}B)

2. STRATEGIC RATIONALE:
   • {payload.key_drivers[0]} provides immediate high-velocity addressable volume.
   • {payload.key_drivers[1]} allows sustainable market penetration without destructive price wars.
   • {payload.key_drivers[2]}.

3. UNIT ECONOMICS & FINANCIAL PATHWAY:
   • Target Break-Even Horizon: Month {payload.break_even_month} under Base Case operations.
   • Customer Acquisition Cap: Target CAC must remain capped at <= INR {payload.target_cac_cap_inr} per acquired user.
   • Key Profit Driver: Focus retention campaigns on the '{payload.top_customer_segment}' customer segment.

4. KEY RISKS & MANAGEMENT TRIGGERS:
   • {payload.risk_factors[0]}.
   • {payload.risk_factors[1]}.
   • TRIGGER: If blended CAC exceeds INR {payload.target_cac_cap_inr} or 3-month retention falls below 35%, pause expansion and optimize dark-store route density.
================================================================================"""
    return explanation


def run_recommendation_layer(
    config: Optional[AppConfig] = None,
) -> Dict[str, Any]:
    """Orchestrates payload assembly and recommendation generation."""
    cfg = config or load_config()
    payload = build_recommendation_payload(cfg)
    explanation = generate_structured_explanation(payload)

    return {
        "payload": payload.to_dict(),
        "prompt_template": EXPLANATION_USER_PROMPT_TEMPLATE.format(
            payload_json=get_serialized_payload(cfg)
        ),
        "explanation": explanation,
    }


if __name__ == "__main__":
    result = run_recommendation_layer()
    print(result["explanation"])
