"""
registry_schemas.py

Pydantic request and response models for the Base Model Registry API.

Covers:
  - Registration (create)
  - Retrieval (single + list)
  - Deletion confirmation
  - Deployment lifecycle responses (activate, deactivate)
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------
class BaseModelRegisterRequest(BaseModel):
    """
    Payload for registering a new base model in the catalog.
    """

    hf_model_id: str = Field(
        ...,
        description="HuggingFace model path, e.g. 'unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit'.",
        examples=["unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit"],
    )
    name: str = Field(
        ...,
        description="Human-readable display name.",
        examples=["Qwen2.5 1.5B Instruct (Unsloth 4bit)"],
    )
    family: Optional[str] = Field(
        default=None,
        description="Model family, e.g. 'qwen', 'llama', 'mistral'.",
        examples=["qwen"],
    )
    parameter_count: Optional[str] = Field(
        default=None,
        description="Parameter count as a human-readable string.",
        examples=["1.5B"],
    )
    is_multimodal: bool = Field(
        default=False,
        description="True if the model accepts image inputs alongside text.",
    )


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------
class BaseModelRead(BaseModel):
    """
    Full representation of a registered base model.
    Returned on registration, retrieval, and list endpoints.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description="Prefixed catalog ID, e.g. 'bm_abc123...'.",
    )
    name: str = Field(
        ...,
        description="Human-readable display name.",
    )
    family: Optional[str] = Field(
        default=None,
        description="Model family.",
    )
    parameter_count: Optional[str] = Field(
        default=None,
        description="Parameter count string.",
    )
    is_multimodal: bool = Field(
        default=False,
        description="Whether the model accepts image inputs.",
    )
    endpoint: Optional[str] = Field(
        default=None,
        description="HuggingFace model path or custom inference endpoint identifier.",
    )
    created_at: int = Field(
        ...,
        description="Unix timestamp of registration.",
    )


class BaseModelList(BaseModel):
    """
    Paginated list of registered base models.
    """

    model_config = ConfigDict(from_attributes=True)

    items: List[BaseModelRead] = Field(
        default_factory=list,
        description="Page of base model records.",
    )
    total: int = Field(
        ...,
        description="Total number of registered base models.",
    )
    limit: int = Field(
        ...,
        description="Page size used for this response.",
    )
    offset: int = Field(
        ...,
        description="Offset used for this response.",
    )


class BaseModelDeleted(BaseModel):
    """
    Confirmation payload returned after deregistering a base model.
    """

    status: str = Field(
        default="deleted",
        description="Always 'deleted' on success.",
    )
    model_id: str = Field(
        ...,
        description="The bm_... ID of the deregistered model.",
    )


# ---------------------------------------------------------------------------
# Deployment Lifecycle Response Schemas
# ---------------------------------------------------------------------------
class DeactivateModelResponse(BaseModel):
    """
    Returned by surgical deactivation of a fine-tuned or base model.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(
        ...,
        description="Outcome of the deactivation request.",
        examples=["success"],
    )
    message: Optional[str] = Field(
        default=None,
        description="Human-readable summary of the operation.",
        examples=["Cluster resources released."],
    )


class DeployBaseModelResponse(BaseModel):
    """
    Returned when a base backbone model is dispatched to the cluster.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(
        ...,
        description="Deployment status.",
        examples=["deploying_standard"],
    )
    model_id: str = Field(
        ...,
        description="The bm_... ID of the model being deployed.",
    )
    node: str = Field(
        ...,
        description="Ray node ID selected for this deployment.",
    )
    tensor_parallel_size: int = Field(
        ...,
        description="Number of GPUs the model is sharded across.",
        examples=[1],
    )
    next_step: str = Field(
        ...,
        description="Human-readable description of the next pipeline stage.",
        examples=["Standard backbone is being provisioned."],
    )
