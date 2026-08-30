"""Unit tests for decision engine export utilities."""

import json
import os
import tempfile

import pandas as pd

from src.decision_engine.export import (
    export_executive_summary_json,
    export_scenario_matrix_csv,
    format_currency_inr,
)


def test_export_executive_summary_json():
    """Validates export of executive summary dictionary to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = os.path.join(tmpdir, "summary.json")
        sample_data = {"recommended_city": "Bengaluru", "score": 77.5}
        res_path = export_executive_summary_json(sample_data, out_file)

        assert os.path.exists(res_path)
        with open(res_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["recommended_city"] == "Bengaluru"


def test_export_scenario_matrix_csv():
    """Validates export of scenario dataframe to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = os.path.join(tmpdir, "scenarios.csv")
        sample_df = pd.DataFrame(
            [
                {"scenario": "Base Case", "top_city": "Bengaluru", "score": 77.5},
                {
                    "scenario": "Scale Aggressive",
                    "top_city": "Delhi NCR",
                    "score": 78.9,
                },
            ]
        )
        res_path = export_scenario_matrix_csv(sample_df, out_file)

        assert os.path.exists(res_path)
        loaded_df = pd.read_csv(res_path)
        assert len(loaded_df) == 2
        assert "scenario" in loaded_df.columns


def test_format_currency_inr():
    """Validates INR currency formatting with and without Crores conversion."""
    assert "INR 1,500.00" == format_currency_inr(1500)
    assert "INR 2.50 Cr" == format_currency_inr(25000000, in_crores=True)
