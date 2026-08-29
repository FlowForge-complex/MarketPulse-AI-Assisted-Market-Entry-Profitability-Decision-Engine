"""Unit tests for Pydantic schema validation at data boundaries."""

import os
import tempfile

import pandas as pd
import pytest

from src.analytics.eda import load_dataset
from src.core.types import (
    CityMetricsSchema,
    CustomerIngestSchema,
    DataLoadError,
    OrderIngestSchema,
    validate_dataframe_schema,
)


def test_valid_city_metrics_schema():
    """Validates that well-formed city dataframe passes schema validation."""
    valid_data = pd.DataFrame(
        [
            {
                "city_id": 1,
                "city": "Bengaluru",
                "state": "Karnataka",
                "population": 12500000,
                "households": 3125000,
                "population_density": 4381,
                "urbanization": 100.0,
                "mpce": 6500,
                "internet_penetration": 75.0,
                "economic_growth": 8.5,
                "income_proxy": 850000,
                "ecommerce_adoption": 22.0,
            }
        ]
    )
    assert validate_dataframe_schema(valid_data, CityMetricsSchema) is True


def test_schema_missing_required_columns():
    """Validates that DataLoadError is raised when required columns are absent."""
    invalid_data = pd.DataFrame(
        [
            {
                "city_id": 1,
                "city": "Bengaluru",
                # missing state, population, etc.
            }
        ]
    )
    with pytest.raises(DataLoadError, match="Missing required columns"):
        validate_dataframe_schema(invalid_data, CityMetricsSchema)


def test_schema_row_constraint_violation():
    """Validates that DataLoadError is raised when data violates bounds."""
    invalid_row = pd.DataFrame(
        [
            {
                "customer_id": -5,  # Invalid negative id
                "city_id": 1,
                "signup_date": "2026-01-01",
                "age_group": "25-34",
                "customer_segment": "Frequent",
            }
        ]
    )
    with pytest.raises(DataLoadError, match="Schema row validation failed"):
        validate_dataframe_schema(invalid_row, CustomerIngestSchema)


def test_load_dataset_schema_violation_raises_error():
    """Validates that load_dataset raises DataLoadError on corrupted CSV."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("order_id,customer_id\n1,100\n")  # Missing required order fields
        temp_path = f.name

    try:
        with pytest.raises(DataLoadError):
            load_dataset(temp_path, schema=OrderIngestSchema)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
