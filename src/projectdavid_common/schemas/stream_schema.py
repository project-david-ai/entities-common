from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from projectdavid_common.constants.ai_model_map import MODEL_MAP


class StreamRequest(BaseModel):
    # 1. FIX: Tell Pydantic to allow fields starting with "model_"
    model_config = ConfigDict(protected_namespaces=())

    # provider: str  <-- REMOVED
    model: str
    api_key: Optional[str] = None
    thread_id: str
    message_id: str
    run_id: str
    assistant_id: str
    content: Optional[str] = None

    @field_validator("model")
    @classmethod
    def validate_model_key(cls, v: str) -> str:
        if v not in MODEL_MAP:
            raise ValueError(f"Invalid model '{v}'. Must be one of: {', '.join(MODEL_MAP.keys())}")
        return v

    @property
    def mapped_model(self) -> str:
        return MODEL_MAP[self.model]
