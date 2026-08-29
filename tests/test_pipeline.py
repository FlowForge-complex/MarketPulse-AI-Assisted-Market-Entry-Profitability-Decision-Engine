"""Integration tests for full pipeline execution."""

import os
import tempfile

from run_pipeline import run_full_pipeline
from src.core.config import AppConfig


def test_full_pipeline_execution():
    """Validates that the full pipeline executes cleanly and produces summary metrics."""
    with tempfile.TemporaryDirectory():
        cfg = AppConfig()
        cfg.paths.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        res = run_full_pipeline(
            config=cfg,
            export_benchmark=True,
            headless=True,
        )

        assert res.status == "SUCCESS"
        assert res.cities_analyzed == 5
        assert res.top_ranked_city == "Bengaluru"
        assert res.top_city_score > 0
        assert res.execution_time_seconds > 0
        assert res.break_even_month == 18
