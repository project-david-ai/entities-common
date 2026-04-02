# src/projectdavid_common/schemas/stream_schema.py

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from projectdavid_common.constants.ai_model_map import MODEL_MAP

# ---------------------------------------------------------------------------
# Sovereign Forge deployment prefix
#
# Active vLLM deployments are reachable via Ray Serve at routes that follow
# this pattern. These IDs are dynamic — generated at activation time — so
# they cannot be enumerated in the static MODEL_MAP.
#
# The validator accepts any string matching this prefix without a map lookup.
# The mapped_model property strips the provider prefix (vllm/) so the value
# passed to the vLLM API is the bare deployment name, which Ray Serve uses
# to route to the correct replica.
#
# Example:
#   model:        "vllm/vllm_dep_cDBDmVAvwc9fjaZF0FIgfx"
#   mapped_model: "vllm_dep_cDBDmVAvwc9fjaZF0FIgfx"
# ---------------------------------------------------------------------------
_SOVEREIGN_FORGE_PREFIX = "vllm/vllm_dep_"


class StreamRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str
    api_key: Optional[str] = None  # LLM provider key (Hyperbolic, OpenAI, etc.)
    thread_id: str
    message_id: str
    run_id: str
    assistant_id: str
    content: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

    # When True (default) the endpoint returns a text/event-stream SSE response.
    # When False the endpoint buffers the full response server-side and returns
    # a single JSON object. All side effects (tool calls, file generation, status
    # events) execute identically in both modes — only the response shape differs.
    stream: bool = True

    @field_validator("model")
    @classmethod
    def validate_model_key(cls, v: str) -> str:
        # Sovereign Forge deployments: accept any vllm/vllm_dep_* string
        # without a static map lookup — these IDs are minted at activation time.
        if v.startswith(_SOVEREIGN_FORGE_PREFIX):
            return v

        if v not in MODEL_MAP:
            raise ValueError(
                f"Invalid model '{v}'. Must be one of: {', '.join(MODEL_MAP.keys())}"
            )
        return v

    @property
    def mapped_model(self) -> str:
        # Sovereign Forge deployments: strip the provider prefix.
        # The vLLM handler routes to VLLM_BASE_URL — Ray Serve uses the
        # bare deployment name to select the correct replica.
        if self.model.startswith(_SOVEREIGN_FORGE_PREFIX):
            return self.model[len("vllm/") :]

        return MODEL_MAP[self.model]
