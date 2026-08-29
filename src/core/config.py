"""Centralized configuration management for MarketPulse."""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class PathConfig:
    """Standard workspace filesystem paths."""

    base_dir: str = field(
        default_factory=lambda: os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
    )

    @property
    def data_processed_dir(self) -> str:
        return os.path.join(self.base_dir, "data", "processed")

    @property
    def data_synthetic_dir(self) -> str:
        return os.path.join(self.base_dir, "data", "synthetic")

    @property
    def data_raw_dir(self) -> str:
        return os.path.join(self.base_dir, "data", "raw")

    @property
    def benchmarks_dir(self) -> str:
        return os.path.join(self.base_dir, "data", "benchmarks")

    @property
    def financial_model_dir(self) -> str:
        return os.path.join(self.base_dir, "financial_model")

    @property
    def presentation_dir(self) -> str:
        return os.path.join(self.base_dir, "presentation")


@dataclass
class AppConfig:
    """Master application configuration."""

    random_seed: int = 42
    log_level: str = "INFO"
    log_format: str = "text"
    log_file: Optional[str] = None
    default_scenario: str = "balanced"
    paths: PathConfig = field(default_factory=PathConfig)
    cac_threshold_inr: int = 350
    target_margin_threshold_pct: float = 0.12


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Loads configuration from YAML file or returns default settings.

    Args:
        config_path: Optional path to a YAML configuration file.

    Returns:
        AppConfig instance populated with settings.
    """
    config = AppConfig()
    if config_path and os.path.exists(config_path) and HAS_YAML:
        with open(config_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}
            if "random_seed" in data:
                config.random_seed = int(data["random_seed"])
            if "log_level" in data:
                config.log_level = str(data["log_level"])
            if "default_scenario" in data:
                config.default_scenario = str(data["default_scenario"])
            if "cac_threshold_inr" in data:
                config.cac_threshold_inr = int(data["cac_threshold_inr"])
    return config
