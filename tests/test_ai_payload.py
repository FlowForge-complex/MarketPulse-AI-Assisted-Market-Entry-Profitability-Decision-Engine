"""Unit tests for AI Explanation Layer payload assembly and narrative synthesis."""

import json
import os

from src.ai.metrics_payload import (
    build_recommendation_payload,
    get_serialized_payload,
)
from src.ai.recommendation import (
    generate_structured_explanation,
    run_recommendation_layer,
)
from src.core.types import RecommendationPayload


def test_build_recommendation_payload():
    """Validates deterministic recommendation payload assembly."""
    payload = build_recommendation_payload()
    assert isinstance(payload, RecommendationPayload)
    assert payload.recommended_city == "Bengaluru"
    assert payload.rank == 1
    assert payload.break_even_month == 18
    assert len(payload.key_drivers) >= 3
    assert len(payload.risk_factors) >= 3


def test_serialized_payload_valid_json():
    """Validates serialized payload is valid JSON."""
    raw_json = get_serialized_payload()
    parsed = json.loads(raw_json)
    assert parsed["recommended_city"] == "Bengaluru"
    assert parsed["break_even_month"] == 18


def test_generate_structured_explanation():
    """Validates that explanation narrative contains key decision metrics."""
    payload = build_recommendation_payload()
    narrative = generate_structured_explanation(payload)
    assert "PRIMARY DIRECTIVE" in narrative
    assert "BENGALURU" in narrative
    assert "Month 18" in narrative
    assert "INR 350" in narrative


def test_run_recommendation_layer():
    """Validates full execution of recommendation layer."""
    res = run_recommendation_layer()
    assert "payload" in res
    assert "explanation" in res
    assert "prompt_template" in res


def test_offline_keyless_execution():
    """Validates keyless offline execution when all API keys are unset."""
    original_gemini = os.environ.pop("GEMINI_API_KEY", None)
    original_openai = os.environ.pop("OPENAI_API_KEY", None)

    try:
        res = run_recommendation_layer()
        assert "explanation" in res
        assert "PRIMARY DIRECTIVE" in res["explanation"]
        assert "BENGALURU" in res["explanation"]
    finally:
        if original_gemini:
            os.environ["GEMINI_API_KEY"] = original_gemini
        if original_openai:
            os.environ["OPENAI_API_KEY"] = original_openai
