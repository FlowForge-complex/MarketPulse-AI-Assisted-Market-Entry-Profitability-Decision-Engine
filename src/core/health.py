"""System health check and pipeline observability monitoring module."""

import json
import os
import sys
import time
from typing import Any, Dict, Optional

from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger

logger = get_logger(__name__)


def health_check(config: Optional[AppConfig] = None) -> Dict[str, Any]:
    """Evaluates readiness of dataset files, file permissions, and environment.

    Args:
        config: Optional application configuration.

    Returns:
        Dictionary containing overall health status, checks breakdown, and system info.
    """
    cfg = config or load_config()
    start_time = time.perf_counter()

    synthetic_dir = cfg.paths.data_synthetic_dir
    processed_dir = cfg.paths.data_processed_dir

    required_files = [
        os.path.join(processed_dir, "city_market_metrics.csv"),
        os.path.join(synthetic_dir, "customers.csv"),
        os.path.join(synthetic_dir, "orders.csv"),
        os.path.join(synthetic_dir, "order_items.csv"),
        os.path.join(synthetic_dir, "products.csv"),
    ]

    files_status: Dict[str, bool] = {}
    for fpath in required_files:
        files_status[os.path.basename(fpath)] = os.path.isfile(fpath)

    all_files_present = all(files_status.values())

    # Check benchmark output directory writability
    benchmarks_dir = cfg.paths.benchmarks_dir
    can_write_benchmarks = False
    try:
        os.makedirs(benchmarks_dir, exist_ok=True)
        test_file = os.path.join(benchmarks_dir, ".health_check_probe")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("probe")
        if os.path.exists(test_file):
            os.remove(test_file)
        can_write_benchmarks = True
    except Exception as exc:
        logger.warning("Benchmark directory write probe failed: %s", exc)

    is_healthy = all_files_present and can_write_benchmarks

    health_report: Dict[str, Any] = {
        "status": "HEALTHY" if is_healthy else "DEGRADED",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "response_time_ms": round((time.perf_counter() - start_time) * 1000, 2),
        "checks": {
            "dataset_files": files_status,
            "benchmarks_dir_writable": can_write_benchmarks,
        },
        "system_info": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "random_seed": cfg.random_seed,
        },
    }

    logger.debug("System health evaluation completed: %s", health_report["status"])
    return health_report


# Backward compatibility alias
check_system_health = health_check


def get_pipeline_metrics(config: Optional[AppConfig] = None) -> Dict[str, Any]:
    """Retrieves operational metrics and dataset dimensions.

    Args:
        config: Optional application configuration.

    Returns:
        Summary metric dictionary.
    """
    health = health_check(config)
    return {
        "pipeline_health": health["status"],
        "response_time_ms": health["response_time_ms"],
        "python_runtime": health["system_info"]["python_version"],
    }


if __name__ == "__main__":
    report = health_check()
    print(json.dumps(report, indent=2))
    if report["status"] != "HEALTHY":
        sys.exit(1)
    sys.exit(0)
