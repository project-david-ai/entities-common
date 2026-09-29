"""Shared contracts for the Project David Scratchpad resource."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ScratchpadCreate(BaseModel):
    """Create the single Scratchpad associated with an owned Thread."""

    thread_id: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class ScratchpadRead(BaseModel):
    """Read representation of one tenant-owned Scratchpad resource."""

    id: str
    owner_id: str
    thread_id: str
    created_at: datetime
    updated_at: datetime
    meta_data: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class ScratchpadUpdate(BaseModel):
    """Update mutable SQL-backed Scratchpad metadata."""

    meta_data: dict[str, Any] | None = None

    model_config = ConfigDict(extra="forbid")


class ScratchpadList(BaseModel):
    """Typed list response for Scratchpad resources."""

    object: str = "list"
    data: list[ScratchpadRead]

    model_config = ConfigDict(from_attributes=True)


class ScratchpadDeleted(BaseModel):
    """Deletion confirmation for one Scratchpad resource."""

    id: str
    object: str = "scratchpad.deleted"
    deleted: bool = True

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "ScratchpadCreate",
    "ScratchpadDeleted",
    "ScratchpadList",
    "ScratchpadRead",
    "ScratchpadUpdate",
]


class ScratchpadContentUpdate(BaseModel):
    """Replace the mutable working body for a Scratchpad."""

    content: str

    model_config = ConfigDict(extra="forbid")


class ScratchpadContentRead(BaseModel):
    """Current mutable working body for a Scratchpad."""

    scratchpad_id: str
    content: str
    updated_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class ScratchpadEntryCreate(BaseModel):
    """Append one immutable entry to a Scratchpad ledger."""

    content: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class ScratchpadEntryRead(BaseModel):
    """One ordered Scratchpad ledger entry."""

    scratchpad_id: str
    content: str
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class ScratchpadEntryList(BaseModel):
    """Ordered Scratchpad append ledger."""

    object: str = "list"
    data: list[ScratchpadEntryRead]

    model_config = ConfigDict(extra="forbid")


class ScratchpadStateCleared(BaseModel):
    """Typed acknowledgement for clearing mutable Scratchpad state."""

    id: str
    object: str = "scratchpad.state.cleared"
    scope: Literal["content", "entries", "all"]
    cleared: bool = True

    model_config = ConfigDict(extra="forbid")
