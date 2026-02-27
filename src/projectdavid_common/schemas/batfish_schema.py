# src/projectdavid_common/schemas/batfish_schema.py
import time
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from projectdavid_common.schemas.enums import StatusEnum


# --------------------------------------------------------------------------- #
#  BATFISH SNAPSHOT SCHEMAS
# --------------------------------------------------------------------------- #
class BatfishSnapshotCreate(BaseModel):
    """Payload to create/refresh a snapshot. snapshot_name is the caller label."""

    snapshot_name: str = Field(
        ..., min_length=3, max_length=128, description="Human-friendly label (e.g., 'incident_001')"
    )
    configs_root: Optional[str] = Field(None, description="Config source path")


class BatfishSnapshotCreateWithSharedId(BatfishSnapshotCreate):
    """Same as Create, but the API routing layer pre-generates the programmable shared ID."""

    shared_id: str = Field(
        ..., description="Pre-generated opaque ID returned to caller e.g. snap_abc123"
    )


class BatfishSnapshotRead(BaseModel):
    """Serialised snapshot record returned to callers."""

    id: str = Field(..., description="Opaque programmable snapshot ID")
    snapshot_name: str = Field(..., description="User-supplied label")
    snapshot_key: str = Field(..., description="Backend Batfish isolation key ({user_id}_{id})")
    user_id: str = Field(..., description="Owner user ID")
    configs_root: Optional[str] = Field(None, description="Config source path")
    device_count: int = Field(default=0, ge=0, description="Number of devices ingested")
    devices: List[str] = Field(default_factory=list, description="List of ingested hostnames")
    status: StatusEnum = Field(..., description="Current lifecycle status")
    error_message: Optional[str] = Field(None, description="Error details if failed")
    created_at: int = Field(..., description="Unix timestamp (sec) when created")
    updated_at: int = Field(..., description="Last modified timestamp")
    last_ingested_at: Optional[int] = Field(None, description="Last successful ingest time")
    object: str = Field("batfish_snapshot", description="Object type identifier")

    model_config = ConfigDict(from_attributes=True)


class BatfishSnapshotUpdate(BaseModel):
    """Payload to update an existing snapshot's metadata."""

    snapshot_name: Optional[str] = Field(None, min_length=3, max_length=128)
    status: Optional[StatusEnum] = Field(None, description="Status override")
    error_message: Optional[str] = Field(None)


class BatfishSnapshotList(BaseModel):
    """List response wrapper for fetching multiple snapshots."""

    snapshots: List[BatfishSnapshotRead]
    object: str = Field("list", description="Object type identifier")


# --------------------------------------------------------------------------- #
#  TOOL RESULT SCHEMAS
# --------------------------------------------------------------------------- #
class BatfishToolResult(BaseModel):
    """Single tool call response."""

    tool: str
    snapshot_name: str
    snapshot_key: str
    result: str


class BatfishAllToolsResult(BaseModel):
    """All tools response keyed by tool name."""

    snapshot_name: str
    snapshot_key: str
    results: Dict[str, Any]
