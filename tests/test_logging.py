"""Unit tests for structured logging configuration."""

import json
import logging

from src.core.logging_config import (
    JSONFormatter,
    TextFormatter,
    get_logger,
    setup_logging,
)


def test_text_formatter():
    """Validates human-readable text log formatter."""
    formatter = TextFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Sample log message",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    assert "[INFO    ]" in output
    assert "Sample log message" in output
    assert "test_logger" in output


def test_json_formatter():
    """Validates structured JSON log formatter output."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_json_logger",
        level=logging.ERROR,
        pathname=__file__,
        lineno=25,
        msg="Error encountered in calculation",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    parsed = json.loads(output)
    assert parsed["level"] == "ERROR"
    assert parsed["logger"] == "test_json_logger"
    assert parsed["message"] == "Error encountered in calculation"
    assert "timestamp" in parsed


def test_get_logger_singleton():
    """Validates logger factory retrieves valid logger instances."""
    setup_logging(level="DEBUG")
    logger = get_logger("unit_test_component")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "unit_test_component"
