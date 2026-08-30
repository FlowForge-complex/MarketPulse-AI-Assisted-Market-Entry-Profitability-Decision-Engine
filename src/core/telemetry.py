"""Performance profiling and pipeline telemetry instrumentation module."""

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional

from src.core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class StepTelemetry:
    """Records timing and metadata for an individual pipeline execution step."""

    step_name: str
    duration_ms: float
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class BenchmarkProfiler:
    """Lightweight in-memory telemetry profiler for tracking pipeline execution efficiency."""

    def __init__(self, pipeline_name: str = "marketpulse_pipeline") -> None:
        self.pipeline_name = pipeline_name
        self.start_time: float = time.perf_counter()
        self.steps: List[StepTelemetry] = []

    @contextmanager
    def track_step(
        self, step_name: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Generator[None, None, None]:
        """Context manager to measure latency of an operational stage."""
        step_start = time.perf_counter()
        status = "SUCCESS"
        step_meta = metadata or {}
        try:
            yield
        except Exception as exc:
            status = "FAILED"
            step_meta["error"] = str(exc)
            raise
        finally:
            duration_ms = round((time.perf_counter() - step_start) * 1000, 2)
            telemetry = StepTelemetry(
                step_name=step_name,
                duration_ms=duration_ms,
                status=status,
                metadata=step_meta,
            )
            self.steps.append(telemetry)
            logger.debug(
                "Telemetry [%s]: Completed in %.2fms (status: %s)",
                step_name,
                duration_ms,
                status,
            )

    def get_summary(self) -> Dict[str, Any]:
        """Returns structured dictionary summarizing all measured steps."""
        total_duration_ms = round((time.perf_counter() - self.start_time) * 1000, 2)
        return {
            "pipeline": self.pipeline_name,
            "total_duration_ms": total_duration_ms,
            "step_count": len(self.steps),
            "steps": [
                {
                    "step": s.step_name,
                    "duration_ms": s.duration_ms,
                    "status": s.status,
                    "metadata": s.metadata,
                }
                for s in self.steps
            ],
        }
