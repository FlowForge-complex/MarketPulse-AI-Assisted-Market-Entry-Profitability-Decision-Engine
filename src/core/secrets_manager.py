"""Provider-agnostic secrets management and vault integration module."""

import os
from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.core.logging_config import get_logger

logger = get_logger(__name__)


class SecretsProvider(ABC):
    """Abstract base class for secrets retrieval providers."""

    @abstractmethod
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves a secret by key name."""
        pass


class EnvSecretsProvider(SecretsProvider):
    """Retrieves secrets strictly from environment variables."""

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, default)


class VaultSecretsProvider(SecretsProvider):
    """In-memory and HashiCorp Vault compatible secrets provider with rotation support."""

    def __init__(self, initial_secrets: Optional[Dict[str, str]] = None) -> None:
        self._vault_store: Dict[str, str] = initial_secrets or {}

    def set_secret(self, key: str, value: str) -> None:
        """Stores or rotates a secret inside the secure vault store."""
        self._vault_store[key] = value
        logger.debug("Rotated secret key [%s] in vault store", key)

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves secret from vault, falling back to environment if not found."""
        if key in self._vault_store:
            return self._vault_store[key]
        return os.environ.get(key, default)


class SecretsManager:
    """Centralized secrets manager dispatching to configured provider."""

    def __init__(self, provider: Optional[SecretsProvider] = None) -> None:
        self.provider = provider or EnvSecretsProvider()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves secret value using active provider."""
        val = self.provider.get_secret(key, default)
        return val

    def get_required(self, key: str) -> str:
        """Retrieves secret or raises ValueError if absent."""
        val = self.get(key)
        if val is None or val.strip() == "":
            raise ValueError(
                f"Required secret [{key}] is missing from active provider."
            )
        return val

    def set_provider(self, provider: SecretsProvider) -> None:
        """Updates the active secrets provider."""
        self.provider = provider
        logger.info(
            "Updated active secrets provider to %s", provider.__class__.__name__
        )


# Global singleton instance
_GLOBAL_SECRETS_MANAGER: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """Returns the global SecretsManager instance."""
    global _GLOBAL_SECRETS_MANAGER
    if _GLOBAL_SECRETS_MANAGER is None:
        _GLOBAL_SECRETS_MANAGER = SecretsManager()
    return _GLOBAL_SECRETS_MANAGER
