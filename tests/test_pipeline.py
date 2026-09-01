"""Integration tests for full DAG pipeline execution and idempotency."""

import json
import os
import tempfile

from run_pipeline import build_pipeline_dag, run_full_pipeline
from src.core.config import AppConfig
from src.pipeline.dag import PipelineDAG


def test_full_pipeline_execution():
    """Validates that the full pipeline executes cleanly and produces summary metrics."""
    cfg = AppConfig()
    cfg.paths.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    res = run_full_pipeline(
        config=cfg,
        export_benchmark=True,
        headless=True,
    )

    assert res.status == "SUCCESS"
    assert res.cities_analyzed == 5
    assert res.top_ranked_city == "Bengaluru"
    assert res.top_city_score > 0
    assert res.execution_time_seconds > 0
    assert res.break_even_month == 18


def test_build_pipeline_dag():
    """Validates DAG structure and dependency registration."""
    cfg = AppConfig()
    dag = build_pipeline_dag(cfg)

    assert isinstance(dag, PipelineDAG)
    assert len(dag.tasks) >= 9
    assert "eda" in dag.tasks
    assert "scoring" in dag.tasks
    assert "pricing" in dag.tasks
    assert "recommendation" in dag.tasks

    order = dag.get_execution_order()
    order_ids = [t.task_id for t in order]
    # EDA must execute before scoring and rfm
    assert order_ids.index("eda") < order_ids.index("scoring")
    assert order_ids.index("eda") < order_ids.index("rfm")


def test_pipeline_idempotency():
    """Validates that two consecutive pipeline runs with the same seed generate identical evaluation metrics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = AppConfig()
        cfg.paths.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        cfg.paths.benchmarks_dir = tmpdir
        cfg.random_seed = 42

        # Run 1
        res1 = run_full_pipeline(
            config=cfg,
            export_benchmark=True,
            headless=True,
        )
        bench1_path = os.path.join(tmpdir, "benchmark_results.json")
        with open(bench1_path, "r", encoding="utf-8") as f:
            data1 = json.load(f)

        # Run 2
        res2 = run_full_pipeline(
            config=cfg,
            export_benchmark=True,
            headless=True,
        )
        with open(bench1_path, "r", encoding="utf-8") as f:
            data2 = json.load(f)

        assert res1.top_ranked_city == res2.top_ranked_city
        assert res1.top_city_score == res2.top_city_score
        assert (
            data1["metadata"]["metrics_checksum"]
            == data2["metadata"]["metrics_checksum"]
        )
        assert data1["evaluation_metrics"] == data2["evaluation_metrics"]
