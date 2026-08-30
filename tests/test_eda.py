"""Unit tests for Exploratory Data Analysis (EDA) module."""

import os
import tempfile

import pytest

from src.analytics.eda import load_dataset, run_eda
from src.core.types import DataLoadError, OrderIngestSchema


def test_run_eda_execution():
    """Validates full EDA execution and key statistical outputs."""
    summary = run_eda()
    assert summary["total_cities"] == 5
    assert summary["total_customers"] == 1000
    assert summary["total_orders"] > 0
    assert summary["total_gross_revenue_inr"] > 0
    assert summary["average_order_value_inr"] > 0
    assert summary["overall_gross_margin_pct"] > 0
    assert "Frequent" in summary["customer_segments_count"]


def test_load_dataset_missing_file():
    """Validates DataLoadError is raised when file does not exist."""
    with pytest.raises(DataLoadError):
        load_dataset("non_existent_directory/missing_file.csv")


def test_load_dataset_schema_violation():
    """Validates DataLoadError is raised when CSV content violates schema constraints."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("order_id,customer_id\n1,100\n")  # Missing required schema columns
        temp_path = f.name

    try:
        with pytest.raises(DataLoadError):
            load_dataset(temp_path, schema=OrderIngestSchema)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
