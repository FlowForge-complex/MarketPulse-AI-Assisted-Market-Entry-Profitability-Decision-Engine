"""Unit tests for system health checks and observability endpoints."""

from src.core.config import AppConfig, load_config
from src.core.health import check_system_health, get_pipeline_metrics, health_check


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


def test_health_check_alias():
    """Validates health_check standard function returns healthy status."""
    config = load_config()
    health = health_check(config)
    assert health["status"] == "HEALTHY"
    assert health["checks"]["benchmarks_dir_writable"] is True


def test_health_check_degraded_on_missing_dir():
    """Validates health_check returns DEGRADED when dataset paths are invalid."""
    cfg = AppConfig()
    cfg.paths.base_dir = "/non_existent_path_xyz_123"
    health = health_check(cfg)
    assert health["status"] == "DEGRADED"


def test_get_pipeline_metrics():
    """Validates retrieval of pipeline observability metrics."""
    metrics = get_pipeline_metrics()
    assert "pipeline_health" in metrics
    assert "response_time_ms" in metrics
    assert "python_runtime" in metrics
