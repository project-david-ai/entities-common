#! src/projectdavid_common/schemas/messages_schema.py
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator


class MessageRole(str, Enum):
    PLATFORM = "platform"
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    TOOL = "tool"


# ---------------------------------------------------------------------------
# ContentType
#
# Plain text:
#   content = "What is in this image?"
#
# Multimodal (produced by MessagesClient.build_image_message — never by hand):
#   content = [
#       {"type": "text",      "text": "What is in this image?"},
#       {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
#   ]
# ---------------------------------------------------------------------------
ContentType = Union[str, List[Dict[str, Any]]]


class MessageCreate(BaseModel):
    content: ContentType  # ← was: str
    thread_id: str
    sender_id: Optional[str] = None
    assistant_id: str
    role: str
    tool_id: Optional[str] = None
    tool_call_id: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_last_chunk: bool = False

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v):
        valid_roles = {"platform", "assistant", "user", "system", "tool"}
        if isinstance(v, str):
            v = v.lower()
            if v in valid_roles:
                return v
        raise ValueError(f"Invalid role: {v}. Must be one of {list(valid_roles)}")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": "Hello, this is a test message.",
                "thread_id": "example_thread_id",
                "assistant_id": "example_assistant_id",
                "meta_data": {"key": "value"},
                "role": "user",
            }
        }
    )


class ToolMessageCreate(BaseModel):
    content: str  # tool output is always plain text / JSON string
    tool_call_id: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": "This is the content of the tool message.",
                "tool_call_id": "call_abc123",
            }
        }
    )


class MessageRead(BaseModel):
    id: str
    assistant_id: Optional[str]
    attachments: List[Any]
    completed_at: Optional[int]
    content: ContentType  # ← was: str
    created_at: int
    incomplete_at: Optional[int]
    incomplete_details: Optional[Dict[str, Any]]
    meta_data: Dict[str, Any]
    object: str
    role: str
    run_id: Optional[str]
    tool_id: Optional[str] = None
    tool_call_id: Optional[str] = None
    status: Optional[str]
    thread_id: str
    sender_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MessageUpdate(BaseModel):
    content: Optional[ContentType] = None  # ← was: Optional[str]
    meta_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    role: Optional[str] = None
    tool_call_id: Optional[str] = None

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return v
        valid_roles = {"platform", "assistant", "user", "system", "tool"}
        v = v.lower()
        if v in valid_roles:
            return v
        raise ValueError(f"Invalid role: {v}. Must be one of {list(valid_roles)}")

    model_config = ConfigDict(from_attributes=True)


class MessagesList(BaseModel):
    object: str = "list"
    data: List[MessageRead]
    first_id: str | None = None
    last_id: str | None = None
    has_more: bool = False

    def to_list(self):
        return [m.dict() for m in self.data]

    model_config = ConfigDict(from_attributes=True)


class MessageDeleted(BaseModel):
    id: str
    object: str = "thread.message.deleted"
    deleted: bool = True

    model_config = ConfigDict(from_attributes=True)
