"""Unit tests for structured logging configuration."""

import json
import logging

from src.core.logging_config import (
    JSONFormatter,
    SecretRedactionFilter,
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


def test_secret_redaction_filter():
    """Validates that sensitive API keys and tokens are masked with [REDACTED]."""
    filter_obj = SecretRedactionFilter()

    # Test Google / Gemini API key redaction
    rec = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Connecting with key AIzaSyD98734ndskfjhsdf98342jklsdhf98",
        args=(),
        exc_info=None,
    )
    filter_obj.filter(rec)
    assert "AIzaSy" not in str(rec.msg)
    assert "[REDACTED]" in str(rec.msg)

    # Test OpenAI API key redaction
    rec2 = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Using secret token sk-1234567890abcdef1234567890abcdef12345",
        args=(),
        exc_info=None,
    )
    filter_obj.filter(rec2)
    assert "sk-" not in str(rec2.msg)
    assert "[REDACTED]" in str(rec2.msg)
