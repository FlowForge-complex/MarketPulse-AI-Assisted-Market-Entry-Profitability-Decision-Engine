"""Directed Acyclic Graph (DAG) task orchestration engine for MarketPulse."""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from src.core.logging_config import get_logger

logger = get_logger(__name__)


class TaskStatus(str, Enum):
    """Execution status states for a DAG task."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class Task:
    """Represents an atomic, dependency-aware stage in the analytics pipeline."""

    task_id: str
    func: Callable[..., Any]
    dependencies: List[str] = field(default_factory=list)
    retries: int = 1
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    duration_ms: float = 0.0
    error: Optional[str] = None


class PipelineDAG:
    """Directed Acyclic Graph managing task registration, validation, and topological sorting."""

    def __init__(self, name: str = "marketpulse_dag") -> None:
        self.name = name
        self.tasks: Dict[str, Task] = {}

    def add_task(
        self,
        task_id: str,
        func: Callable[..., Any],
        dependencies: Optional[List[str]] = None,
        retries: int = 1,
        description: str = "",
    ) -> "PipelineDAG":
        """Registers a new task node in the graph."""
        if task_id in self.tasks:
            raise ValueError(f"Duplicate task identifier: '{task_id}'")

        task = Task(
            task_id=task_id,
            func=func,
            dependencies=dependencies or [],
            retries=retries,
            description=description,
        )
        self.tasks[task_id] = task
        return self

    def get_execution_order(self) -> List[Task]:
        """Performs topological sort (Kahn's algorithm) to determine valid task execution sequence."""
        in_degree: Dict[str, int] = {t_id: 0 for t_id in self.tasks}
        adj_list: Dict[str, List[str]] = {t_id: [] for t_id in self.tasks}

        for task_id, task in self.tasks.items():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    raise ValueError(
                        f"Task '{task_id}' depends on unregistered task '{dep}'"
                    )
                adj_list[dep].append(task_id)
                in_degree[task_id] += 1

        queue: List[str] = [t_id for t_id, deg in in_degree.items() if deg == 0]
        order: List[Task] = []

        while queue:
            current_id = queue.pop(0)
            order.append(self.tasks[current_id])

            for neighbor_id in adj_list[current_id]:
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in PipelineDAG! Execution cannot proceed.")

        return order


class DAGRunner:
    """Executes a PipelineDAG in topological order with retry policies and execution telemetry."""

    def __init__(self, dag: PipelineDAG) -> None:
        self.dag = dag

    def run(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes all DAG tasks in dependency order."""
        logger.info("Executing PipelineDAG: %s", self.dag.name)
        exec_order = self.dag.get_execution_order()
        pipeline_context = context.copy() if context else {}
        results: Dict[str, Any] = {}

        for task in exec_order:
            task.status = TaskStatus.RUNNING
            start_t = time.perf_counter()
            attempts = 0
            success = False

            logger.info("Executing DAG Task [%s]...", task.task_id)
            while attempts <= task.retries and not success:
                attempts += 1
                try:
                    res = task.func(pipeline_context)
                    task.result = res
                    results[task.task_id] = res
                    pipeline_context[task.task_id] = res
                    task.status = TaskStatus.SUCCESS
                    success = True
                except Exception as exc:
                    task.error = str(exc)
                    if attempts > task.retries:
                        task.status = TaskStatus.FAILED
                        task.duration_ms = round(
                            (time.perf_counter() - start_t) * 1000, 2
                        )
                        logger.error(
                            "Task [%s] failed after %d attempts: %s",
                            task.task_id,
                            attempts,
                            exc,
                        )
                        raise RuntimeError(
                            f"DAG Task [{task.task_id}] failed: {exc}"
                        ) from exc
                    logger.warning(
                        "Task [%s] attempt %d failed: %s. Retrying...",
                        task.task_id,
                        attempts,
                        exc,
                    )

            task.duration_ms = round((time.perf_counter() - start_t) * 1000, 2)

        logger.info("PipelineDAG [%s] completed successfully.", self.dag.name)
        return results
