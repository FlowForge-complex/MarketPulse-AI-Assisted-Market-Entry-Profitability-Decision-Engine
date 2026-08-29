"""Unit tests for dashboard data loading and metric calculations."""

import os

import pandas as pd


def test_dashboard_data_loading():
    """Validates that underlying CSV datasets required for the dashboard exist and load cleanly."""
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src/dashboard")
    )
    cities_path = os.path.join(base_dir, "../../data/processed/city_market_metrics.csv")
    orders_path = os.path.join(base_dir, "../../data/synthetic/orders.csv")
    customers_path = os.path.join(base_dir, "../../data/synthetic/customers.csv")

    assert os.path.exists(cities_path)
    assert os.path.exists(orders_path)
    assert os.path.exists(customers_path)

    cities_df = pd.read_csv(cities_path)
    orders_df = pd.read_csv(orders_path)
    customers_df = pd.read_csv(customers_path)

    assert not cities_df.empty
    assert not orders_df.empty
    assert not customers_df.empty

    # Verify required visualization columns exist
    assert "population" in cities_df.columns
    assert "ecommerce_adoption" in cities_df.columns
    assert "customer_segment" in customers_df.columns
    assert "delivery_fee" in orders_df.columns
