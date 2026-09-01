"""Unit tests for SecretsManager and Vault providers."""

import os

import pytest

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
