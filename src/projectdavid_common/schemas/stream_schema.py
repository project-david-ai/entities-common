# src/projectdavid_common/schemas/stream_schema.py

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict

from projectdavid_common.constants.ai_model_map import MODEL_MAP


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

    @property
    def mapped_model(self) -> str:
        """
        Resolve the provider-prefixed model string to the bare model name
        expected by the downstream provider API.

        For models in the static map (together-ai/*, hyperbolic/*, ollama/*,
        vllm/* known models): return the mapped value.

        For dynamic Sovereign Forge deployments (vllm/vllm_dep_*) and any
        HF path passed directly (vllm/org/model-name): strip the vllm/ prefix
        and return the remainder. Routing handles the rest.

        For anything else not in the map: return as-is and let the router
        surface the error naturally.
        """
        if self.model in MODEL_MAP:
            return MODEL_MAP[self.model]

        # Strip vllm/ prefix for dynamic deployments and bare HF paths
        if self.model.startswith("vllm/"):
            return self.model[len("vllm/") :]

        return self.model
