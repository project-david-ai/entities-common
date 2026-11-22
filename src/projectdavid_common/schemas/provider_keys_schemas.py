"""Shared contracts for user-owned inference provider keys."""

from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

_PROVIDER_PATTERN = re.compile(r"[a-z][a-z0-9_-]{0,63}")
_MAX_SECRET_BYTES = 16384


class ProviderKeyCreate(BaseModel):
    """Register an inference provider credential.

    The provider secret is write-only. Ownership is established
    from authenticated identity, never from request data.
    """

    provider: str = Field(..., min_length=1, max_length=64)
    api_key: SecretStr = Field(..., exclude=True, repr=False)
    name: str | None = Field(None, max_length=128)

    model_config = ConfigDict(extra="forbid")

    @field_validator("provider")
    @classmethod
    def normalize_provider(cls, value: str) -> str:
        normalized = value.strip().lower()

        if not _PROVIDER_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid inference provider identifier")

        return normalized

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, value: SecretStr) -> SecretStr:
        raw = value.get_secret_value()

        if not raw or not raw.strip():
            raise ValueError("Provider API key must not be blank")

        if len(raw.encode("utf-8")) > _MAX_SECRET_BYTES:
            raise ValueError("Provider API key exceeds size limit")

        return value

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()

        if not normalized:
            raise ValueError("Provider key name must not be blank")

        return normalized


class ProviderKeyUpdate(BaseModel):
    """Rename an existing provider key.

    Credential replacement is deliberately unsupported.
    """

    name: str = Field(..., min_length=1, max_length=128)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("Provider key name must not be blank")

        return normalized


class ProviderKeyRead(BaseModel):
    """Non-secret representation of a provider key."""

    id: str
    owner_id: str
    provider: str
    name: str | None
    created_at: datetime
    revoked_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


__all__ = [
    "ProviderKeyCreate",
    "ProviderKeyUpdate",
    "ProviderKeyRead",
]
