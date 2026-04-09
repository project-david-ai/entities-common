# src/projectdavid_common/schemas/deployment_schemas.py
"""
deployment_schemas.py

Pydantic request and response models for the Deployment API.

Covers:
  - Activation requests (base model, fine-tuned model)
  - Activation responses
  - Deactivation responses (single, all)
  - Deployment listing

Note:
  Registry schemas (BaseModelRead, BaseModelList, etc.) remain in
  registry_schemas.py. This file covers deployment lifecycle only.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------


class ActivateBaseModelRequest(BaseModel):
    """
    Payload for activating a base model (no LoRA adapter) for inference.
    """

    base_model_id: str = Field(
        ...,
        description=(
            "Either a `bm_...` prefixed catalog ID or a raw HuggingFace model path. "
            "Examples: 'bm_abc123' or 'unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit'."
        ),
        examples=[
            "bm_KZcYp7GJaD4M58gBSlTlsj",
            "unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit",
        ],
    )
    target_node_id: Optional[str] = Field(
        default=None,
        description=(
            "Pin deployment to a specific Ray node ID. "
            "If omitted, the DeploymentService selects the most resource-rich available node."
        ),
    )
    tensor_parallel_size: int = Field(
        default=1,
        ge=1,
        description="Number of GPUs to shard the model across.",
        examples=[1],
    )


class ActivateFineTunedModelRequest(BaseModel):
    """
    Payload for activating a fine-tuned model (base + LoRA adapter) for inference.
    """

    model_id: str = Field(
        ...,
        description="The `ftm_...` prefixed ID of the fine-tuned model to deploy.",
        examples=["ftm_G05BERHAEvSRr2KTyUqWIJ"],
    )
    target_node_id: Optional[str] = Field(
        default=None,
        description=(
            "Pin deployment to a specific Ray node ID. "
            "If omitted, the DeploymentService selects the most resource-rich available node."
        ),
    )
    tensor_parallel_size: int = Field(
        default=1,
        ge=1,
        description="Number of GPUs to shard the model across.",
        examples=[1],
    )


# ---------------------------------------------------------------------------
# Activation Response Schemas
# ---------------------------------------------------------------------------


class DeploymentActivationResponse(BaseModel):
    """
    Returned when a model is successfully scheduled for deployment.

    The deployment is not yet live — the InferenceReconciler picks up the
    pending InferenceDeployment record on its next poll cycle and deploys
    the corresponding Ray Serve application.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(
        ...,
        description="Deployment status. Always 'deploying' on success.",
        examples=["deploying"],
    )
    model_id: str = Field(
        ...,
        description="The catalog ID of the model being deployed (bm_... or ftm_...).",
    )
    hf_path: Optional[str] = Field(
        default=None,
        description="The resolved HuggingFace model path.",
        examples=["unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit"],
    )
    base_model_id: Optional[str] = Field(
        default=None,
        description="For fine-tuned model deployments — the bm_... ID of the base model.",
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
    serve_route: str = Field(
        ...,
        description="Internal Ray Serve HTTP route for this deployment.",
        examples=["http://inference_worker:8000/vllm_dep_abc123"],
    )
    next_step: str = Field(
        ...,
        description="Human-readable description of the next pipeline stage.",
        examples=["InferenceReconciler will deploy via Ray Serve on next poll."],
    )


# ---------------------------------------------------------------------------
# Deactivation Response Schemas
# ---------------------------------------------------------------------------


class DeploymentDeactivationResponse(BaseModel):
    """
    Returned by surgical deactivation of a single deployment.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(
        ...,
        description="Always 'deactivated' on success.",
        examples=["deactivated"],
    )
    model_id: Optional[str] = Field(
        default=None,
        description="The ftm_... ID of the deactivated fine-tuned model, if applicable.",
    )
    base_model_id: Optional[str] = Field(
        default=None,
        description="The bm_... ID of the deactivated base model, if applicable.",
    )


class DeactivateAllResponse(BaseModel):
    """
    Returned after a full cluster clean slate deactivation.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(
        ...,
        description="Always 'success' on success.",
        examples=["success"],
    )
    message: str = Field(
        ...,
        description="Human-readable summary of the operation.",
        examples=[
            "All deployments cleared. InferenceReconciler will release GPU resources on next poll."
        ],
    )


# ---------------------------------------------------------------------------
# Deployment List Response Schema
# ---------------------------------------------------------------------------


class DeploymentRecord(BaseModel):
    """
    Single InferenceDeployment record as returned by the list endpoint.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Deployment ID (dep_...).")
    base_model_id: str = Field(..., description="bm_... ID of the base model.")
    fine_tuned_model_id: Optional[str] = Field(
        default=None,
        description="ftm_... ID of the LoRA adapter, if applicable.",
    )
    node_id: str = Field(..., description="Ray node ID this deployment is pinned to.")
    status: str = Field(..., description="Current deployment status.")
    tensor_parallel_size: int = Field(..., description="GPU shard count.")
    internal_hostname: Optional[str] = Field(
        default=None,
        description="Internal Ray Serve HTTP route.",
    )
    last_seen: int = Field(..., description="Unix timestamp of last reconciler check.")


class DeploymentListResponse(BaseModel):
    """
    Paginated list of active InferenceDeployment records.
    """

    model_config = ConfigDict(from_attributes=True)

    items: List[DeploymentRecord] = Field(
        default_factory=list,
        description="Active deployment records.",
    )
    total: int = Field(
        ...,
        description="Total number of active deployments.",
    )
