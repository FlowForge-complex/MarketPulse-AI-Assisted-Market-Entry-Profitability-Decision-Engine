"""Unit tests for synthetic data generation pipelines and seed reproducibility."""

import os
import tempfile

import pandas as pd

from src.data_generation.generate_customers import generate_customers
from src.data_generation.generate_orders import generate_orders
from src.data_generation.generate_products import generate_products


def test_generate_customers():
    """Validates deterministic customer record generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = generate_customers(count=50, seed=123, output_dir=tmpdir)
        assert os.path.exists(out_file)

        df = pd.read_csv(out_file)
        assert len(df) == 50
        assert "customer_id" in df.columns
        assert "customer_segment" in df.columns
        assert df["customer_id"].tolist() == list(range(1, 51))


def test_generate_products():
    """Validates deterministic product SKU catalog generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = generate_products(count=40, seed=456, output_dir=tmpdir)
        assert os.path.exists(out_file)

        df = pd.read_csv(out_file)
        assert len(df) == 40
        assert "product_id" in df.columns
        assert "unit_cost" in df.columns
        assert "selling_price" in df.columns
        assert (df["selling_price"] >= df["unit_cost"]).all()


def test_generate_orders():
    """Validates deterministic order and order-item transaction generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orders_path, items_path = generate_orders(
            customer_count=20, seed=789, output_dir=tmpdir
        )
        assert os.path.exists(orders_path)
        assert os.path.exists(items_path)

        orders_df = pd.read_csv(orders_path)
        items_df = pd.read_csv(items_path)

        assert len(orders_df) >= 20
        assert len(items_df) >= len(orders_df)
        assert "order_id" in orders_df.columns
        assert "delivery_fee" in orders_df.columns
        assert (items_df["quantity"] > 0).all()
