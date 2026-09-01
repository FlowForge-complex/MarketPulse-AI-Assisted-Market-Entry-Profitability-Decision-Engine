"""Unit tests for Directed Acyclic Graph (DAG) task engine and runner."""

import pytest

from src.pipeline.dag import DAGRunner, PipelineDAG, TaskStatus


def test_dag_topological_execution_order():
    """Validates tasks execute strictly according to their declared dependency order."""
    dag = PipelineDAG(name="test_order_dag")
    execution_trail = []

    def task_a(ctx):
        execution_trail.append("A")
        return "result_a"

    def task_b(ctx):
        execution_trail.append("B")
        return "result_b"

    def task_c(ctx):
        execution_trail.append("C")
        return "result_c"

    # Declare out of order: C depends on B, B depends on A
    dag.add_task("task_c", task_c, dependencies=["task_b"])
    dag.add_task("task_a", task_a, dependencies=[])
    dag.add_task("task_b", task_b, dependencies=["task_a"])

    runner = DAGRunner(dag)
    results = runner.run()

    assert execution_trail == ["A", "B", "C"]
    assert results["task_a"] == "result_a"
    assert results["task_b"] == "result_b"
    assert results["task_c"] == "result_c"


def test_dag_cycle_detection():
    """Validates that circular dependencies raise ValueError."""
    dag = PipelineDAG(name="cycle_dag")
    dag.add_task("task_1", lambda ctx: None, dependencies=["task_2"])
    dag.add_task("task_2", lambda ctx: None, dependencies=["task_1"])

    with pytest.raises(ValueError, match="Cycle detected"):
        dag.get_execution_order()


def test_dag_retry_policy():
    """Validates task retry succeeds on transient error."""
    dag = PipelineDAG(name="retry_dag")
    attempts = 0

    def flaky_task(ctx):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionError("Temporary network hiccup")
        return "recovered"

    dag.add_task("flaky", flaky_task, retries=2)
    runner = DAGRunner(dag)
    res = runner.run()

    assert res["flaky"] == "recovered"
    assert attempts == 2
    assert dag.tasks["flaky"].status == TaskStatus.SUCCESS
