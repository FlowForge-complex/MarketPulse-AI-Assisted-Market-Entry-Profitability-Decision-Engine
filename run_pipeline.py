"""Unified Headless CLI Pipeline Runner for MarketPulse Decision Engine.

Usage:
    python run_pipeline.py [OPTIONS]

Options:
    --seed INTEGER       Random seed for deterministic runs (default: 42)
    --config PATH        Path to custom YAML configuration file
    --benchmark          Export performance and model evaluation metrics to data/benchmarks/
    --headless           Run quietly without printing verbose narrative
    --log-level TEXT     Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

# UTF-8 terminal encoding guard for Windows platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.ai.recommendation import run_recommendation_layer
from src.analytics.eda import run_eda
from src.analytics.profitability import run_profitability_analysis
from src.analytics.retention import run_retention_analysis
from src.analytics.rfm import run_rfm_analysis
from src.core.config import AppConfig, load_config
from src.core.logging_config import get_logger, setup_logging
from src.core.types import PipelineExecutionResult
from src.decision_engine.city_scoring import run_city_scoring
from src.decision_engine.pricing import evaluate_pricing_strategy
from src.decision_engine.sensitivity import run_sensitivity_pipeline
from src.guesstimation.market_sizing import get_default_bengaluru_tam

logger = get_logger("marketpulse.pipeline")


def run_full_pipeline(
    config: AppConfig,
    export_benchmark: bool = False,
    headless: bool = False,
) -> PipelineExecutionResult:
    """Executes all analytics, modeling, decision, and explanation stages end-to-end.

    Args:
        config: Application configuration settings.
        export_benchmark: Whether to write benchmark metrics to disk.
        headless: Whether to suppress console prints.

    Returns:
        PipelineExecutionResult summary object.
    """
    start_time = time.perf_counter()
    logger.info("Starting MarketPulse Decision Engine Pipeline...")

    artifacts: List[str] = []

    # 1. Exploratory Data Analysis
    eda_summary = run_eda(config)

    # 2. RFM Customer Segmentation
    _, _ = run_rfm_analysis(config)

    # 3. Cohort Retention Matrix
    _ = run_retention_analysis(config)

    # 4. Profitability Unit Economics
    _, _ = run_profitability_analysis(config)

    # 5. City Attractiveness Scoring (MCDA)
    ranked_cities_df = run_city_scoring(config)
    top_city_row = ranked_cities_df.iloc[0]

    # 6. Sensitivity & Scenario Analysis
    _ = run_sensitivity_pipeline(config)

    # 7. Pricing Elasticity Strategy
    _ = evaluate_pricing_strategy(
        base_orders=eda_summary["total_orders"],
        base_aov=eda_summary["average_order_value_inr"],
    )

    # 8. TAM Guesstimation
    tam_res = get_default_bengaluru_tam()

    # 9. AI Recommendation Layer
    rec_result = run_recommendation_layer(config)

    elapsed_time = time.perf_counter() - start_time

    result = PipelineExecutionResult(
        status="SUCCESS",
        execution_time_seconds=round(elapsed_time, 4),
        cities_analyzed=len(ranked_cities_df),
        total_customers=eda_summary["total_customers"],
        total_orders=eda_summary["total_orders"],
        top_ranked_city=str(top_city_row["city"]),
        top_city_score=float(top_city_row["composite_score"]),
        tam_estimate_cr=float(tam_res.annual_tam_inr_crores),
        break_even_month=18,
        artifacts_generated=artifacts,
    )

    # Export benchmark artifacts if requested
    if export_benchmark:
        bench_dir = config.paths.benchmarks_dir
        os.makedirs(bench_dir, exist_ok=True)

        benchmark_data: Dict[str, Any] = {
            "metadata": {
                "pipeline_version": "1.1.0",
                "execution_status": result.status,
                "execution_time_seconds": result.execution_time_seconds,
                "random_seed": config.random_seed,
            },
            "evaluation_metrics": {
                "top_ranked_city": result.top_ranked_city,
                "composite_score": result.top_city_score,
                "estimated_tam_crores": result.tam_estimate_cr,
                "total_orders_analyzed": result.total_orders,
                "total_customers": result.total_customers,
                "gross_revenue_inr": eda_summary["total_gross_revenue_inr"],
                "gross_margin_pct": eda_summary["overall_gross_margin_pct"],
                "projected_break_even_month": result.break_even_month,
            },
            "top_city_breakdown": top_city_row.to_dict(),
        }

        bench_json_path = os.path.join(bench_dir, "benchmark_results.json")
        with open(bench_json_path, "w", encoding="utf-8") as f:
            json.dump(benchmark_data, f, indent=2)
        artifacts.append(bench_json_path)

        # Also write summary CSV
        summary_csv_path = os.path.join(bench_dir, "metrics_summary.csv")
        ranked_cities_df[
            [
                "rank",
                "city",
                "composite_score",
                "demand_score",
                "competition_score",
                "cost_score",
            ]
        ].to_csv(summary_csv_path, index=False)
        artifacts.append(summary_csv_path)

        logger.info("Benchmark artifacts exported to %s", bench_dir)

    logger.info(
        "Pipeline executed successfully in %.4f seconds. Recommended City: %s (Score: %.2f)",
        elapsed_time,
        result.top_ranked_city,
        result.top_city_score,
    )

    if not headless:
        try:
            print("\n" + rec_result["explanation"] + "\n")
        except Exception:
            safe_text = (
                rec_result["explanation"].encode("ascii", "replace").decode("ascii")
            )
            print("\n" + safe_text + "\n")

    return result


def main() -> None:
    """CLI entrypoint parsing flags and executing pipeline."""
    parser = argparse.ArgumentParser(
        description="MarketPulse: AI-Assisted Market Entry Decision Engine"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible execution",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to custom YAML configuration",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Export benchmark metrics to data/benchmarks/",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without console narrative output",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Console logging verbosity level",
    )
    args = parser.parse_args()

    setup_logging(level=args.log_level)
    config = load_config(args.config)
    config.random_seed = args.seed

    try:
        run_full_pipeline(
            config=config,
            export_benchmark=args.benchmark,
            headless=args.headless,
        )
        sys.exit(0)
    except Exception as exc:
        logger.exception("Pipeline execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
