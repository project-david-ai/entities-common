from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from projectdavid_common.schemas.users_schema import UserBase


class ThreadCreate(BaseModel):
    participant_ids: Optional[List[str]] = Field(
        default=None,
        description=(
            "Additional participant IDs to attach at creation time. "
            "The authenticated user (owner) is always included automatically."
        ),
    )
    meta_data: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional metadata for the thread"
    )


class ThreadRead(BaseModel):
    id: str
    created_at: int
    meta_data: Dict[str, Any]
    object: str
    tool_resources: Dict[str, Any]

    # ── Ownership (read-only, set server-side) ───────────────────────────────
    # Nullable during the back-fill window; will be non-null on all threads
    # created after the owner_id migration is applied.
    owner_id: Optional[str] = Field(
        default=None,
        description="Canonical owner of this thread. Read-only — set at creation time.",
    )

    model_config = ConfigDict(from_attributes=True)


class ThreadUpdate(BaseModel):
    # owner_id is deliberately absent — ownership is not transferable via update.
    participant_ids: Optional[List[str]] = Field(
        default=None, description="Updated list of participant IDs"
    )
    meta_data: Optional[Dict[str, Any]] = Field(
        default=None, description="Updated metadata"
    )
    tool_resources: Optional[Dict[str, Any]] = Field(
        default=None, description="Updated tool resources for the thread"
    )

    model_config = ConfigDict(from_attributes=True)


class ThreadParticipant(UserBase):
    pass


class ThreadReadDetailed(ThreadRead):
    # owner_id is inherited from ThreadRead.
    participants: List[UserBase]

    model_config = ConfigDict(from_attributes=True)


class ThreadIds(BaseModel):
    thread_ids: List[str]

    model_config = ConfigDict(from_attributes=True)


class ThreadDeleted(BaseModel):
    id: str
    object: str = "thread.deleted"
    deleted: bool = True
