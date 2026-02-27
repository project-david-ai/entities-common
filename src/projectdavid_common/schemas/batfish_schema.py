# src/projectdavid_common/schemas/batfish_schema.py
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BatfishSnapshotCreate(BaseModel):
    """Payload to create/refresh a snapshot. snapshot_name is the caller label."""

    snapshot_name: str
    configs_root: Optional[str] = None


class BatfishSnapshotRead(BaseModel):
    """Serialised snapshot record returned to callers."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    snapshot_name: str
    snapshot_key: str
    user_id: str
    configs_root: Optional[str]
    device_count: int
    devices: List[str]
    status: str
    error_message: Optional[str]
    created_at: int
    updated_at: int
    last_ingested_at: Optional[int]


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
    results: dict
