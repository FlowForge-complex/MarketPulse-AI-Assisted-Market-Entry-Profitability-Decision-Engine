"""Type definitions, validation schemas, and dataclasses for MarketPulse."""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Type

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field


class MarketPulseError(Exception):
    """Base exception class for all MarketPulse errors."""

    pass


class ValidationError(MarketPulseError):
    """Raised when an input parameter or schema fails validation constraints."""

    pass


class DataLoadError(MarketPulseError):
    """Raised when raw or processed dataset files cannot be loaded or parsed."""

    pass


class ModelExecutionError(MarketPulseError):
    """Raised when an analytics model or decision engine encounters calculation errors."""

    pass


# ==============================================================================
# Pydantic Schemas for Ingestion Boundary Validation
# ==============================================================================


class CityMetricsSchema(BaseModel):
    """Pydantic schema for validating city demographic and economic market data."""

    model_config = ConfigDict(extra="ignore")

    city_id: int = Field(gt=0, description="Unique city identifier")
    city: str = Field(min_length=1, description="City name")
    state: str = Field(min_length=1, description="Indian State")
    population: int = Field(gt=0, description="Metropolitan population")
    households: int = Field(gt=0, description="Total households")
    population_density: int = Field(gt=0, description="People per sq km")
    urbanization: float = Field(ge=0.0, le=100.0, description="Urbanization %")
    mpce: int = Field(gt=0, description="Monthly per-capita expenditure")
    internet_penetration: float = Field(ge=0.0, le=100.0, description="Internet %")
    economic_growth: float = Field(ge=-50.0, le=100.0, description="GDP Growth %")
    income_proxy: int = Field(gt=0, description="Per capita income proxy")
    ecommerce_adoption: float = Field(ge=0.0, le=100.0, description="eCommerce %")


class CustomerIngestSchema(BaseModel):
    """Pydantic schema for customer record ingestion validation."""

    model_config = ConfigDict(extra="ignore")

    customer_id: int = Field(gt=0)
    city_id: int = Field(gt=0)
    signup_date: str = Field(min_length=8)
    age_group: str = Field(min_length=2)
    customer_segment: str = Field(min_length=2)


class ProductIngestSchema(BaseModel):
    """Pydantic schema for SKU product catalog validation."""

    model_config = ConfigDict(extra="ignore")

    product_id: int = Field(gt=0)
    category: str = Field(min_length=1)
    subcategory: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    unit_cost: int = Field(ge=0)
    selling_price: int = Field(ge=0)


class OrderIngestSchema(BaseModel):
    """Pydantic schema for customer order header validation."""

    model_config = ConfigDict(extra="ignore")

    order_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    city_id: int = Field(gt=0)
    order_date: str = Field(min_length=8)
    order_status: str = Field(min_length=2)
    delivery_time: int = Field(ge=0)
    discount: int = Field(ge=0)
    delivery_fee: int = Field(ge=0)


class OrderItemIngestSchema(BaseModel):
    """Pydantic schema for order line-item SKU validation."""

    model_config = ConfigDict(extra="ignore")

    order_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: int = Field(ge=0)
    cost: int = Field(ge=0)


def validate_dataframe_schema(
    df: pd.DataFrame,
    schema_cls: Type[BaseModel],
    sample_size: Optional[int] = 50,
) -> bool:
    """Validates DataFrame columns and sampled rows against a Pydantic schema model.

    Args:
        df: Input pandas DataFrame to validate.
        schema_cls: Target Pydantic schema class.
        sample_size: Number of sample rows to test (None for full scan).

    Returns:
        True if all rows pass validation.

    Raises:
        DataLoadError: If schema constraints or required fields are violated.
    """
    if df.empty:
        raise DataLoadError("Cannot validate schema: DataFrame is empty.")

    # Check required fields exist in columns
    schema_fields = schema_cls.model_fields.keys()
    missing_cols = set(schema_fields) - set(df.columns)
    if missing_cols:
        raise DataLoadError(
            f"Schema validation failed: Missing required columns: {sorted(missing_cols)}"
        )

    # Validate rows against Pydantic model
    sample_df = df if sample_size is None else df.head(sample_size)
    records = sample_df.to_dict(orient="records")

    for idx, row in enumerate(records):
        try:
            schema_cls(**row)
        except Exception as exc:
            raise DataLoadError(
                f"Schema row validation failed at record index {idx}: {exc}"
            ) from exc

    return True


# ==============================================================================
# Domain Dataclasses
# ==============================================================================


@dataclass
class CityMetrics:
    """Represents public and economic metrics for a target city."""

    city_id: int
    city: str
    state: str
    population: int
    households: int
    population_density: int
    urbanization: float
    mpce: int
    internet_penetration: float
    economic_growth: float
    income_proxy: int
    ecommerce_adoption: float

    def __post_init__(self) -> None:
        if self.population <= 0:
            raise ValidationError(f"Population must be positive, got {self.population}")
        if not 0.0 <= self.internet_penetration <= 100.0:
            raise ValidationError(
                f"Internet penetration must be in [0, 100], got {self.internet_penetration}"
            )
        if not 0.0 <= self.ecommerce_adoption <= 100.0:
            raise ValidationError(
                f"eCommerce adoption must be in [0, 100], got {self.ecommerce_adoption}"
            )


@dataclass
class CustomerRecord:
    """Represents a customer profile and demographic segment."""

    customer_id: int
    city_id: int
    signup_date: str
    age_group: str
    customer_segment: str

    def __post_init__(self) -> None:
        valid_segments = {
            "Budget",
            "Occasional",
            "Frequent",
            "Premium",
            "At-Risk",
        }
        if self.customer_segment not in valid_segments:
            raise ValidationError(
                f"Invalid customer segment: '{self.customer_segment}'. Allowed: {valid_segments}"
            )


@dataclass
class ProductRecord:
    """Represents a SKU in the retail catalog with unit economics."""

    product_id: int
    category: str
    subcategory: str
    product_name: str
    unit_cost: int
    selling_price: int

    def __post_init__(self) -> None:
        if self.selling_price < 0 or self.unit_cost < 0:
            raise ValidationError("Prices and unit costs cannot be negative.")


@dataclass
class OrderRecord:
    """Represents a customer transaction header."""

    order_id: int
    customer_id: int
    city_id: int
    order_date: str
    order_status: str
    delivery_time: int
    discount: int
    delivery_fee: int


@dataclass
class OrderItemRecord:
    """Represents an individual SKU item within an order."""

    order_id: int
    product_id: int
    quantity: int
    unit_price: int
    cost: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValidationError(f"Order quantity must be >= 1, got {self.quantity}")


@dataclass
class ScoringWeights:
    """Weights configuration for multi-criteria city attractiveness scoring."""

    economic_growth: float = 0.25
    competition_inverse: float = 0.25
    cost_efficiency: float = 0.15
    demand_index: float = 0.15
    market_size: float = 0.10
    income_level: float = 0.10

    def __post_init__(self) -> None:
        total = sum(
            [
                self.economic_growth,
                self.competition_inverse,
                self.cost_efficiency,
                self.demand_index,
                self.market_size,
                self.income_level,
            ]
        )
        if abs(total - 1.0) > 1e-4:
            raise ValidationError(
                f"Scoring weights must sum to exactly 1.0 (100%). Current sum: {total:.4f}"
            )

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class CityScoreResult:
    """Evaluated score and rank for a single candidate city."""

    city_id: int
    city_name: str
    market_size_score: float
    economic_growth_score: float
    demand_score: float
    competition_score: float
    cost_score: float
    income_score: float
    composite_score: float
    rank: int


@dataclass
class SensitivityScenario:
    """Defines a strategic management scenario with weighted priorities."""

    scenario_name: str
    description: str
    weights: ScoringWeights


@dataclass
class PricingTier:
    """Represents pricing scenario parameters and demand elasticity multipliers."""

    tier_name: str
    price_multiplier: float
    demand_multiplier: float
    margin_expansion_bps: int


@dataclass
class TAMParameters:
    """Inputs for bottom-up Total Addressable Market (TAM) guesstimation."""

    target_city: str
    population: int
    household_size: float
    internet_penetration_rate: float
    ecommerce_adoption_rate: float
    target_category_share: float
    orders_per_month_per_hh: float
    average_order_value: float

    def __post_init__(self) -> None:
        if self.population <= 0 or self.household_size <= 0:
            raise ValidationError("Population and household size must be positive.")
        if not 0.0 <= self.internet_penetration_rate <= 1.0:
            raise ValidationError("internet_penetration_rate must be in range [0, 1].")
        if not 0.0 <= self.ecommerce_adoption_rate <= 1.0:
            raise ValidationError("ecommerce_adoption_rate must be in range [0, 1].")
        if self.average_order_value <= 0:
            raise ValidationError("AOV must be positive.")


@dataclass
class TAMResult:
    """Output metrics from market sizing calculation."""

    city: str
    total_households: int
    connected_households: int
    active_ecommerce_households: int
    target_customers: int
    annual_order_volume: int
    annual_tam_inr: float
    annual_tam_inr_crores: float
    sanity_check_passed: bool
    benchmark_variance_pct: float


@dataclass
class RFMScoreRecord:
    """Customer-level RFM metrics and segment assignment."""

    customer_id: int
    recency_days: int
    frequency: int
    monetary: float
    r_score: int
    f_score: int
    m_score: int
    rfm_score: str
    segment: str


@dataclass
class RecommendationPayload:
    """Structured deterministic payload ingested by the AI explanation layer."""

    recommended_city: str
    composite_score: float
    rank: int
    estimated_tam_inr_crores: float
    top_customer_segment: str
    segment_margin_contribution_pct: float
    recommended_pricing_tier: str
    break_even_month: int
    target_cac_cap_inr: int
    key_drivers: List[str]
    risk_factors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineExecutionResult:
    """Summarizes end-to-end execution of the analytics and decision pipeline."""

    status: str
    execution_time_seconds: float
    cities_analyzed: int
    total_customers: int
    total_orders: int
    top_ranked_city: str
    top_city_score: float
    tam_estimate_cr: float
    break_even_month: int
    artifacts_generated: List[str] = field(default_factory=list)
