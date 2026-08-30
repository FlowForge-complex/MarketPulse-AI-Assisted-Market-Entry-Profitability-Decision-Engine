"""Unit tests for BenchmarkProfiler and pipeline telemetry instrumentation."""

import time

import pytest

from src.core.telemetry import BenchmarkProfiler


def test_profiler_track_step():
    """Validates latency measurement and step tracking."""
    profiler = BenchmarkProfiler(pipeline_name="test_pipeline")

    with profiler.track_step("step_1", metadata={"batch_size": 100}):
        time.sleep(0.01)

    summary = profiler.get_summary()
    assert summary["pipeline"] == "test_pipeline"
    assert summary["step_count"] == 1
    assert summary["steps"][0]["step"] == "step_1"
    assert summary["steps"][0]["status"] == "SUCCESS"
    assert summary["steps"][0]["duration_ms"] > 0
    assert summary["steps"][0]["metadata"]["batch_size"] == 100


def test_profiler_error_handling():
    """Validates profiler captures failed step telemetry on exception."""
    profiler = BenchmarkProfiler(pipeline_name="failing_pipeline")

    with pytest.raises(ValueError, match="Synthetic failure"):
        with profiler.track_step("faulty_step"):
            raise ValueError("Synthetic failure")

    summary = profiler.get_summary()
    assert summary["step_count"] == 1
    assert summary["steps"][0]["status"] == "FAILED"
    assert "Synthetic failure" in summary["steps"][0]["metadata"]["error"]
