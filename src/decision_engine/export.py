"""Export utilities for serializing decision engine findings and scenario matrices."""

import json
import os
from typing import Any, Dict

import pandas as pd

from src.core.logging_config import get_logger

logger = get_logger(__name__)


def export_executive_summary_json(
    summary_data: Dict[str, Any],
    output_path: str,
) -> str:
    """Exports structured executive summary dictionary to a JSON artifact.

    Args:
        summary_data: Dictionary of computed analytics and decision metrics.
        output_path: Destination JSON file path.

    Returns:
        Absolute path to exported JSON file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    logger.info("Executive summary JSON successfully exported to %s", output_path)
    return os.path.abspath(output_path)


def export_scenario_matrix_csv(
    scenario_df: pd.DataFrame,
    output_path: str,
) -> str:
    """Exports sensitivity scenario matrix to CSV.

    Args:
        scenario_df: Pandas DataFrame containing sensitivity analysis ranks and scores.
        output_path: Destination CSV file path.

    Returns:
        Absolute path to exported CSV file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    scenario_df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info("Scenario matrix CSV successfully exported to %s", output_path)
    return os.path.abspath(output_path)


def format_currency_inr(amount: float, in_crores: bool = False) -> str:
    """Formats numeric amounts into standard Indian currency representation.

    Args:
        amount: Raw numerical currency value in INR.
        in_crores: Whether to format as Crores (Cr).

    Returns:
        Formatted string representation.
    """
    if in_crores:
        crores = amount / 1e7
        return f"INR {crores:,.2f} Cr"
    return f"INR {amount:,.2f}"
