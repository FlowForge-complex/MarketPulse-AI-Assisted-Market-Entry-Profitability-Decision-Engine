"""Core module initialization."""

from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger, setup_logging
from src.core.types import (
    CityMetrics,
    CityScoreResult,
    CustomerRecord,
    DataLoadError,
    ModelExecutionError,
    OrderItemRecord,
    OrderRecord,
    PipelineExecutionResult,
    PricingTier,
    ProductRecord,
    RecommendationPayload,
    RFMScoreRecord,
    ScoringWeights,
    SensitivityScenario,
    TAMParameters,
    TAMResult,
    ValidationError,
)

__all__ = [
    "setup_logging",
    "get_logger",
    "AppConfig",
    "load_config",
    "CityMetrics",
    "CustomerRecord",
    "ProductRecord",
    "OrderRecord",
    "OrderItemRecord",
    "ScoringWeights",
    "CityScoreResult",
    "SensitivityScenario",
    "PricingTier",
    "TAMParameters",
    "TAMResult",
    "RecommendationPayload",
    "PipelineExecutionResult",
    "RFMScoreRecord",
    "ValidationError",
    "DataLoadError",
    "ModelExecutionError",
]
