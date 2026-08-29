"""Unit tests for system health checks and observability endpoints."""

from src.core.config import load_config
from src.core.health import check_system_health, get_pipeline_metrics


def test_check_system_health():
    """Validates that system health check probe returns status and checks."""
    config = load_config()
    health = check_system_health(config)

    assert "status" in health
    assert health["status"] in {"HEALTHY", "DEGRADED"}
    assert "response_time_ms" in health
    assert "checks" in health
    assert "system_info" in health
    assert health["checks"]["benchmarks_dir_writable"] is True


def test_get_pipeline_metrics():
    """Validates retrieval of pipeline observability metrics."""
    metrics = get_pipeline_metrics()
    assert "pipeline_health" in metrics
    assert "response_time_ms" in metrics
    assert "python_runtime" in metrics
