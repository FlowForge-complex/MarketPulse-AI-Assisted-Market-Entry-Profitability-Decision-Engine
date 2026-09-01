"""Unit tests for SecretsManager, Vault providers, and log redaction assurance."""

import io
import logging
import os

import pytest

from src.core.logging_config import SecretRedactionFilter
from src.core.secrets_manager import (
    EnvSecretsProvider,
    SecretsManager,
    VaultSecretsProvider,
    get_secrets_manager,
)


def test_env_secrets_provider():
    """Validates retrieval of secrets from environment."""
    os.environ["TEST_SECRET_KEY"] = "super_secret_value_123"
    provider = EnvSecretsProvider()
    assert provider.get_secret("TEST_SECRET_KEY") == "super_secret_value_123"
    assert provider.get_secret("NON_EXISTENT_KEY", "default_val") == "default_val"


def test_vault_secrets_provider():
    """Validates vault in-memory store and secret rotation."""
    vault = VaultSecretsProvider({"API_KEY": "initial_key_abc"})
    assert vault.get_secret("API_KEY") == "initial_key_abc"

    # Test key rotation
    vault.set_secret("API_KEY", "rotated_key_xyz")
    assert vault.get_secret("API_KEY") == "rotated_key_xyz"


def test_secrets_manager_required():
    """Validates get_required raises ValueError when secret is missing."""
    manager = SecretsManager(EnvSecretsProvider())
    with pytest.raises(ValueError, match="Required secret"):
        manager.get_required("DEFINITELY_MISSING_SECRET_XYZ")


def test_global_singleton():
    """Validates global singleton factory returns consistent manager."""
    mgr1 = get_secrets_manager()
    mgr2 = get_secrets_manager()
    assert mgr1 is mgr2


def test_secrets_manager_never_logs_raw_secrets():
    """Validates that log streams masking never output raw token strings."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.addFilter(SecretRedactionFilter())
    handler.setFormatter(logging.Formatter("%(message)s"))

    test_logger = logging.getLogger("test_security_redaction")
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(handler)

    raw_gemini_key = "AIzaSyD_EXAMPLE_SECRET_KEY_123456789"
    raw_openai_key = "sk-proj-EXAMPLE_SECRET_TOKEN_987654321"

    test_logger.info(f"Loaded credentials: {raw_gemini_key} and {raw_openai_key}")
    output = stream.getvalue()

    assert raw_gemini_key not in output
    assert raw_openai_key not in output
    assert "[REDACTED]" in output
