# src/projectdavid_common/schemas/deployment_schemas.py
"""
deployment_schemas.py

Pydantic request and response models for the Deployment API.

Covers:
  - Activation requests (base model, fine-tuned model)
  - Activation responses
  - Deactivation responses (single, all)
  - Deployment listing

Hyperparam fields on activation requests:
  All vLLM engine hyperparams are optional on both activation schemas.
  None (default) means the InferenceReconciler falls back to the node-level
  VLLM_DEFAULT_* env vars or its own built-in safe defaults.
  Set explicitly to override on a per-deployment basis without touching
  compose files or rebuilding images.

Note:
  Registry schemas (BaseModelRead, BaseModelList, etc.) remain in
  registry_schemas.py. This file covers deployment lifecycle only.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------


class ActivateBaseModelRequest(BaseModel):
    """
    Payload for activating a base model (no LoRA adapter) for inference.

    All vLLM hyperparam fields are optional. Omit them to use node-level
    env var defaults. Set them to tune a specific deployment without any
    compose or image changes.
    """

    base_model_id: str = Field(
        ...,
        description=(
            "Either a `bm_...` prefixed catalog ID or a raw HuggingFace model path. "
            "Examples: 'bm_abc123' or 'OpenGVLab/InternVL2-4B'."
        ),
        examples=[
            "bm_KZcYp7GJaD4M58gBSlTlsj",
            "OpenGVLab/InternVL2-4B",
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

    # --- vLLM engine hyperparam overrides ---
    # All optional. None = fall back to VLLM_DEFAULT_* env vars or built-in defaults.

    gpu_memory_utilization: Optional[float] = Field(
        default=None,
        ge=0.10,
        le=0.95,
        description=(
            "Fraction of GPU VRAM vLLM may allocate for weights + KV cache. "
            "Overrides VLLM_DEFAULT_GPU_MEM_UTIL on this deployment only. "
            "Safe range: 0.10–0.95."
        ),
        examples=[0.90, 0.95],
    )
    max_model_len: Optional[int] = Field(
        default=None,
        ge=512,
        description=(
            "Maximum sequence length in tokens (prompt + completion). "
            "Larger values consume more KV cache VRAM. "
            "Overrides VLLM_DEFAULT_MAX_MODEL_LEN on this deployment only."
        ),
        examples=[4096, 8192],
    )
    max_num_seqs: Optional[int] = Field(
        default=None,
        ge=1,
        description=(
            "Maximum number of concurrent sequences vLLM will process. "
            "Critical for vision models — each image consumes multiple sequence slots. "
            "None = vLLM chooses based on available memory."
        ),
        examples=[4, 8],
    )
    quantization: Optional[str] = Field(
        default=None,
        description=(
            "Quantization scheme to apply. "
            "Options: 'awq', 'awq_marlin', 'gptq', 'bitsandbytes'. "
            "None = full precision (model weights loaded as-is)."
        ),
        examples=["awq_marlin", "gptq"],
    )
    dtype: Optional[str] = Field(
        default=None,
        description=(
            "Compute dtype for model weights and activations. "
            "Options: 'float16', 'bfloat16', 'auto'. "
            "None defaults to float16 in the reconciler."
        ),
        examples=["float16", "bfloat16"],
    )
    enforce_eager: Optional[bool] = Field(
        default=None,
        description=(
            "Disable CUDA graph capture. Slower at inference time but avoids "
            "OOM during graph capture on memory-constrained GPUs. "
            "Useful for debugging. None defaults to False."
        ),
        examples=[False, True],
    )
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(
        default=None,
        description=(
            "Per-modality token cap per request. Prevents runaway token counts "
            "from high-resolution images on small GPUs. "
            "Example: {'image': 2, 'video': 0}. None = vLLM default (unlimited)."
        ),
        examples=[{"image": 2}, {"image": 1, "video": 0}],
    )


class ActivateFineTunedModelRequest(BaseModel):
    """
    Payload for activating a fine-tuned model (base + LoRA adapter) for inference.

    All vLLM hyperparam fields are optional. Omit them to use node-level
    env var defaults. Set them to tune a specific deployment without any
    compose or image changes.
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

    # --- vLLM engine hyperparam overrides ---
    # All optional. None = fall back to VLLM_DEFAULT_* env vars or built-in defaults.

    gpu_memory_utilization: Optional[float] = Field(
        default=None,
        ge=0.10,
        le=0.95,
        description=(
            "Fraction of GPU VRAM vLLM may allocate for weights + KV cache. "
            "Overrides VLLM_DEFAULT_GPU_MEM_UTIL on this deployment only."
        ),
        examples=[0.90],
    )
    max_model_len: Optional[int] = Field(
        default=None,
        ge=512,
        description=(
            "Maximum sequence length in tokens (prompt + completion). "
            "Overrides VLLM_DEFAULT_MAX_MODEL_LEN on this deployment only."
        ),
        examples=[4096],
    )
    max_num_seqs: Optional[int] = Field(
        default=None,
        ge=1,
        description=(
            "Maximum number of concurrent sequences. "
            "None = vLLM chooses based on available memory."
        ),
        examples=[8],
    )
    quantization: Optional[str] = Field(
        default=None,
        description=(
            "Quantization scheme: 'awq', 'awq_marlin', 'gptq', 'bitsandbytes', or None."
        ),
        examples=["awq_marlin"],
    )
    dtype: Optional[str] = Field(
        default=None,
        description="Compute dtype: 'float16', 'bfloat16', 'auto', or None.",
        examples=["float16"],
    )
    enforce_eager: Optional[bool] = Field(
        default=None,
        description="Disable CUDA graphs. None defaults to False.",
        examples=[False],
    )
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(
        default=None,
        description=(
            "Per-modality token cap per request. "
            "Example: {'image': 2, 'video': 0}. None = vLLM default."
        ),
        examples=[{"image": 2}],
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
        examples=["OpenGVLab/InternVL2-4B"],
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
    gpu_memory_utilization: Optional[float] = Field(
        default=None,
        description="GPU VRAM fraction written to the deployment record. None = env default.",
    )
    max_model_len: Optional[int] = Field(
        default=None,
        description="Max sequence length written to the deployment record. None = env default.",
    )
    quantization: Optional[str] = Field(
        default=None,
        description="Quantization scheme written to the deployment record. None = full precision.",
    )
    dtype: Optional[str] = Field(
        default=None,
        description="Compute dtype written to the deployment record. None = float16.",
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
    gpu_memory_utilization: Optional[float] = Field(
        default=None,
        description="GPU VRAM fraction for this deployment.",
    )
    max_model_len: Optional[int] = Field(
        default=None,
        description="Max sequence length for this deployment.",
    )
    quantization: Optional[str] = Field(
        default=None,
        description="Quantization scheme for this deployment.",
    )
    dtype: Optional[str] = Field(
        default=None,
        description="Compute dtype for this deployment.",
    )
    enforce_eager: Optional[bool] = Field(
        default=None,
        description="Whether CUDA graphs are disabled for this deployment.",
    )
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(
        default=None,
        description="Per-modality token cap for this deployment.",
    )
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


class DeploymentUpdateRequest(BaseModel):
    """
    Patch a live InferenceDeployment record.

    Only fields explicitly provided are updated — omitted fields retain
    their current DB values. Changes take effect on the next reconciler
    poll cycle (the reconciler redeploys if it detects drift).
    """

    gpu_memory_utilization: Optional[float] = Field(default=None, ge=0.10, le=0.95)
    max_model_len: Optional[int] = Field(default=None, ge=512)
    max_num_seqs: Optional[int] = Field(default=None, ge=1)
    quantization: Optional[str] = Field(default=None)
    dtype: Optional[str] = Field(default=None)
    enforce_eager: Optional[bool] = Field(default=None)
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(default=None)
    tensor_parallel_size: Optional[int] = Field(default=None, ge=1)
