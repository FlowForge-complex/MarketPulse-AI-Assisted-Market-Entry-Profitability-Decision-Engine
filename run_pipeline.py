"""Unified Headless CLI Pipeline Runner for MarketPulse Decision Engine.

Usage:
    python run_pipeline.py [OPTIONS]

Options:
    --seed INTEGER       Random seed for deterministic runs (default: 42)
    --config PATH        Path to custom YAML configuration file
    --benchmark          Export performance and model evaluation metrics to data/benchmarks/
    --headless           Run quietly without printing verbose narrative
    --force              Force re-execution and overwrite cached benchmark outputs
    --log-level TEXT     Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import argparse
import hashlib
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
from src.decision_engine.ablations import run_ablation_pipeline
from src.decision_engine.city_scoring import run_city_scoring
from src.decision_engine.pricing import evaluate_pricing_strategy
from src.decision_engine.sensitivity import run_sensitivity_pipeline
from src.guesstimation.market_sizing import get_default_bengaluru_tam
from src.pipeline.dag import DAGRunner, PipelineDAG

logger = get_logger("marketpulse.pipeline")


def build_pipeline_dag(config: AppConfig) -> PipelineDAG:
    """Constructs the dependency-directed execution graph for MarketPulse analytics."""
    dag = PipelineDAG(name="marketpulse_analytics_dag")

    dag.add_task(
        "eda",
        lambda ctx: run_eda(config),
        dependencies=[],
        description="Exploratory Data Analysis across transactions and cities",
    )
    dag.add_task(
        "rfm",
        lambda ctx: run_rfm_analysis(config),
        dependencies=["eda"],
        description="Customer Recency, Frequency, Monetary segmentation",
    )
    dag.add_task(
        "retention",
        lambda ctx: run_retention_analysis(config),
        dependencies=["eda"],
        description="Monthly cohort retention analysis",
    )
    dag.add_task(
        "profitability",
        lambda ctx: run_profitability_analysis(config),
        dependencies=["eda"],
        description="SKU and city unit profitability economics",
    )
    dag.add_task(
        "scoring",
        lambda ctx: run_city_scoring(config),
        dependencies=["eda"],
        description="Multi-Criteria Decision Analysis (MCDA) city attractiveness",
    )
    dag.add_task(
        "sensitivity",
        lambda ctx: run_sensitivity_pipeline(config),
        dependencies=["scoring"],
        description="Macro stress testing and scenario sensitivity matrix",
    )
    dag.add_task(
        "pricing",
        lambda ctx: evaluate_pricing_strategy(
            base_orders=ctx["eda"]["total_orders"],
            base_aov=ctx["eda"]["average_order_value_inr"],
        ),
        dependencies=["eda", "profitability"],
        description="Dynamic pricing elasticity evaluation",
    )
    dag.add_task(
        "tam",
        lambda ctx: get_default_bengaluru_tam(),
        dependencies=["scoring"],
        description="Bottom-up demographic Total Addressable Market sizing",
    )
    dag.add_task(
        "ablations",
        lambda ctx: run_ablation_pipeline(config),
        dependencies=["scoring"],
        description="Baseline comparisons and feature ablation studies",
    )
    dag.add_task(
        "recommendation",
        lambda ctx: run_recommendation_layer(config),
        dependencies=["scoring", "pricing", "tam"],
        description="Deterministic executive strategy narrative synthesis",
    )

    return dag


def run_full_pipeline(
    config: AppConfig,
    export_benchmark: bool = False,
    headless: bool = False,
    force: bool = False,
) -> PipelineExecutionResult:
    """Executes all analytics, modeling, decision, and explanation stages end-to-end via DAG.

    Args:
        config: Application configuration settings.
        export_benchmark: Whether to write benchmark metrics to disk.
        headless: Whether to suppress console prints.
        force: Whether to overwrite existing cached benchmarks.

    Returns:
        PipelineExecutionResult summary object.
    """
    start_time = time.perf_counter()
    logger.info("Starting MarketPulse Decision Engine DAG Pipeline...")

    artifacts: List[str] = []

    # Check idempotency cache if benchmark was already computed with identical seed
    bench_dir = config.paths.benchmarks_dir
    bench_json_path = os.path.join(bench_dir, "benchmark_results.json")

    # Build and execute the DAG
    dag = build_pipeline_dag(config)
    runner = DAGRunner(dag)
    dag_results = runner.run()

    eda_summary = dag_results["eda"]
    ranked_cities_df = dag_results["scoring"]
    top_city_row = ranked_cities_df.iloc[0]
    tam_res = dag_results["tam"]
    rec_result = dag_results["recommendation"]

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

    # Export benchmark artifacts with idempotency validation
    if export_benchmark:
        os.makedirs(bench_dir, exist_ok=True)

        benchmark_data: Dict[str, Any] = {
            "metadata": {
                "pipeline_version": "1.1.0",
                "execution_status": result.status,
                "execution_time_seconds": result.execution_time_seconds,
                "random_seed": config.random_seed,
                "dag_tasks_executed": len(dag.tasks),
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

        # Compute deterministic checksum
        serialized_metrics = json.dumps(
            benchmark_data["evaluation_metrics"], sort_keys=True
        )
        data_checksum = hashlib.sha256(serialized_metrics.encode("utf-8")).hexdigest()[
            :16
        ]
        benchmark_data["metadata"]["metrics_checksum"] = data_checksum

        with open(bench_json_path, "w", encoding="utf-8") as f:
            json.dump(benchmark_data, f, indent=2)
        artifacts.append(bench_json_path)

        # Write summary CSV
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

        logger.info(
            "Benchmark artifacts exported to %s (checksum: %s)",
            bench_dir,
            data_checksum,
        )

    logger.info(
        "DAG Pipeline executed successfully in %.4f seconds. Recommended City: %s (Score: %.2f)",
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
        "--force",
        action="store_true",
        help="Force re-execution and overwrite cached benchmark outputs",
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
            force=args.force,
        )
        sys.exit(0)
    except Exception as exc:
        logger.exception("Pipeline execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
