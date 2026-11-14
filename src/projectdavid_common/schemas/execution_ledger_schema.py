# src/projectdavid_common/schemas/execution_ledger_schema.py

"""
Public Pydantic response contracts for Project David's execution ledger.

These schemas describe durable execution lineage exposed by Core.

They cover:
    - Execution epochs
    - Supervisor and worker identity snapshots
    - Parent/child Run delegation relationships
    - Structured forensic execution events
    - Paginated API responses

Raw tool outputs, reasoning contents, credentials and evidence
storage locators are not part of these public response contracts.
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ExecutionActorRead(BaseModel):
    """Durable identity snapshot for an execution actor."""

    id: str
    epoch_id: str
    slot: str
    execution_role: str

    assistant_id_snapshot: Optional[str] = None
    model_snapshot: Optional[str] = None

    ephemeral: bool
    state: str

    reserved_at: int
    activated_at: Optional[int] = None
    retired_at: Optional[int] = None
    last_seen_at: Optional[int] = None


class ExecutionEpochRead(BaseModel):
    """One execution attempt associated with a logical Run."""

    id: str
    run_id: str
    root_run_id: str

    epoch_number: int
    state: str

    created_at: int
    started_at: Optional[int] = None
    last_seen_at: Optional[int] = None
    ended_at: Optional[int] = None

    terminal_status: Optional[str] = None

    actors: list[ExecutionActorRead] = Field(default_factory=list)


class ExecutionPage(BaseModel):
    """Paginated execution epochs belonging to a root Run."""

    object: Literal["list"] = "list"

    root_run_id: str
    data: list[ExecutionEpochRead] = Field(default_factory=list)

    has_more: bool
    next_cursor: Optional[str] = None


class DelegationRead(BaseModel):
    """Durable parent Action to child Run relationship."""

    id: str
    root_run_id: str

    parent_epoch_id: str
    parent_run_id: str
    parent_action_id: str

    child_epoch_id: str
    child_run_id: str

    initiating_actor_id: Optional[str] = None

    created_at: int


class DelegationPage(BaseModel):
    """Paginated delegation relationships for a root Run."""

    object: Literal["list"] = "list"

    root_run_id: str
    data: list[DelegationRead] = Field(default_factory=list)

    has_more: bool
    next_cursor: Optional[str] = None


class ExecutionEventRead(BaseModel):
    """
    Structured forensic event.

    Events are recorded against a specific execution epoch.
    Their origin_run_id identifies the Run that generated them.

    Evidence references remain internal to Core and are not
    included in this public API model.
    """

    id: int
    epoch_id: str

    actor_id: Optional[str] = None
    origin_run_id: str

    event_type: str
    schema_version: int
    evidence_class: str

    occurred_at_us: int
    recorded_at_us: int

    evidence_expires_at: Optional[int] = None

    action_id_snapshot: Optional[str] = None
    tool_call_id_snapshot: Optional[str] = None

    details: dict[str, Any] = Field(default_factory=dict)

    evidence_sha256: Optional[str] = None
    previous_digest: Optional[str] = None
    record_digest: Optional[str] = None


class ExecutionEventPage(BaseModel):
    """Paginated forensic events across a root Run's graph."""

    object: Literal["list"] = "list"

    root_run_id: str
    data: list[ExecutionEventRead] = Field(default_factory=list)

    has_more: bool
    next_cursor: Optional[int] = None
