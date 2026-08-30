"""Unit tests for synthetic orders and order items generation."""

import os
import tempfile

import pandas as pd

from src.data_generation.generate_orders import generate_orders


def test_generate_orders_schema_and_counts():
    """Validates generate_orders produces valid orders.csv and order_items.csv with expected row counts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orders_path, items_path = generate_orders(
            customer_count=10, seed=1, output_dir=tmpdir
        )
        assert os.path.exists(orders_path)
        assert os.path.exists(items_path)

        orders_df = pd.read_csv(orders_path)
        items_df = pd.read_csv(items_path)

        # Assert minimum bounds and structural integrity
        assert len(orders_df) >= 10
        assert len(items_df) >= len(orders_df)

        expected_order_cols = {
            "order_id",
            "customer_id",
            "city_id",
            "order_date",
            "order_status",
            "delivery_time",
            "discount",
            "delivery_fee",
        }
        expected_item_cols = {
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "cost",
        }

        assert expected_order_cols.issubset(set(orders_df.columns))
        assert expected_item_cols.issubset(set(items_df.columns))
        assert (items_df["quantity"] >= 1).all()
        assert (items_df["unit_price"] >= items_df["cost"]).all()
