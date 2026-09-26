"""Shared contracts for Project David MCP registration and attachment."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class McpServerRegistrationCreate(BaseModel):
    """Register one unauthenticated remote Streamable HTTP MCP server."""

    name: str = Field(..., min_length=1, max_length=128)
    url: HttpUrl
    transport: Literal["streamable_http"] = "streamable_http"
    timeout_seconds: float = Field(30.0, gt=0, le=300)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("MCP server name must not be blank")
        return value


class McpServerRegistrationUpdate(BaseModel):
    """Explicitly update mutable registration settings."""

    name: str | None = Field(None, min_length=1, max_length=128)
    timeout_seconds: float | None = Field(None, gt=0, le=300)
    enabled: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("MCP server name must not be blank")
        return value


class McpServerRegistrationRead(BaseModel):
    id: str
    owner_id: str
    name: str
    url: HttpUrl
    transport: Literal["streamable_http"]
    timeout_seconds: float
    enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


def _validate_remote_tool_names(values: list[str]) -> list[str]:
    normalized: list[str] = []

    for value in values:
        name = value.strip()
        if not name:
            raise ValueError("MCP remote tool names must not be blank")
        normalized.append(name)

    if not normalized:
        raise ValueError("At least one MCP remote tool is required")

    if len(normalized) != len(set(normalized)):
        raise ValueError("Duplicate MCP remote tool names are not allowed")

    return normalized


class AssistantMcpToolsAttach(BaseModel):
    """Attach selected discovered tools from a server to one assistant."""

    server_id: str = Field(..., min_length=1)
    tools: list[str] = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, values: list[str]) -> list[str]:
        return _validate_remote_tool_names(values)


class AssistantMcpToolsDetach(BaseModel):
    """Detach selected MCP tools from one assistant."""

    server_id: str = Field(..., min_length=1)
    tools: list[str] = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, values: list[str]) -> list[str]:
        return _validate_remote_tool_names(values)


class AssistantMcpToolRead(BaseModel):
    id: str
    assistant_id: str
    registration_id: str
    remote_name: str
    canonical_id: str
    provider_name: str
    enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "AssistantMcpToolRead",
    "AssistantMcpToolsAttach",
    "AssistantMcpToolsDetach",
    "McpServerRegistrationCreate",
    "McpServerRegistrationRead",
    "McpServerRegistrationUpdate",
]
