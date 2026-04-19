# src/projectdavid_common/schemas/training_schema.py

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DatasetFormat(str, Enum):
    chatml = "chatml"
    alpaca = "alpaca"
    sharegpt = "sharegpt"
    jsonl = "jsonl"


# ---------------------------------------------------------------------------
# DATASET SCHEMAS
# ---------------------------------------------------------------------------


class DatasetCreate(BaseModel):
    name: str = Field(..., max_length=128)
    description: Optional[str] = None
    format: DatasetFormat
    file_id: str = Field(..., description="file_id returned by POST /v1/uploads")
    filename: Optional[str] = Field(
        default=None, description="Original filename for reference"
    )


class DatasetRead(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    format: str
    file_id: str
    storage_path: Optional[str] = None
    train_samples: Optional[int] = None
    eval_samples: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    status: str
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class DatasetList(BaseModel):
    data: List[DatasetRead]
    total: int


class DatasetDeleted(BaseModel):
    deleted: bool
    dataset_id: str


# ---------------------------------------------------------------------------
# TRAINING CONFIG SCHEMA
# ---------------------------------------------------------------------------


class TrainingProfile(str, Enum):
    laptop = "laptop"
    standard = "standard"


class TrainingConfig(BaseModel):
    """
    Tunable parameters for a training job.

    All fields are optional — omitted values fall back to framework defaults
    (for unsloth, that's the values baked into PROFILES in unsloth_train.py).

    Users who want a quick smoke test override `max_steps=20`. Users who
    want an aggressive fine-tune override `lora_r=32` + `num_train_epochs=2`.
    """

    model_config = ConfigDict(extra="forbid")

    # ── Profile preset ────────────────────────────────────────────────────
    profile: Optional[TrainingProfile] = Field(
        default=None,
        description="Hardware preset. 'laptop' = consumer GPU (8GB). 'standard' = datacenter GPU.",
    )

    # ── LoRA adapter dials ────────────────────────────────────────────────
    lora_r: Optional[int] = Field(
        default=None,
        description="LoRA rank. Higher = more expressive adapter, larger file. Typical: 8, 16, 32, 64.",
    )
    lora_alpha: Optional[int] = Field(
        default=None,
        description="LoRA alpha scaling. Conventionally set equal to lora_r.",
    )
    lora_dropout: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=0.5,
        description="Dropout applied to LoRA layers during training.",
    )

    # ── Training dynamics ─────────────────────────────────────────────────
    learning_rate: Optional[float] = Field(
        default=None,
        gt=0.0,
        le=1e-2,
        description="Optimizer learning rate. Above 1e-2 usually diverges.",
    )
    num_train_epochs: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Full passes over the dataset. Overridden by max_steps if both set.",
    )
    max_steps: Optional[int] = Field(
        default=None,
        ge=1,
        le=100000,
        description="Hard ceiling on training steps. Overrides num_train_epochs.",
    )
    logging_steps: Optional[int] = Field(
        default=None,
        ge=1,
        description="How often to emit progress metrics. Lower = more DB writes.",
    )

    # ── Hardware scaling ──────────────────────────────────────────────────
    per_device_train_batch_size: Optional[int] = Field(
        default=None,
        ge=1,
        description="Samples per GPU per forward pass. Higher needs more VRAM.",
    )
    gradient_accumulation_steps: Optional[int] = Field(
        default=None,
        ge=1,
        description="Steps to accumulate gradients before weight update. "
        "Effective batch = per_device_train_batch_size × gradient_accumulation_steps.",
    )


# ---------------------------------------------------------------------------
# TRAINING JOB SCHEMAS
# ---------------------------------------------------------------------------


class TrainingJobCreate(BaseModel):
    dataset_id: str
    base_model: str = Field(..., max_length=256)
    framework: str = Field(default="axolotl", pattern="^(axolotl|unsloth)$")
    config: Optional[TrainingConfig] = None


class TrainingJobRead(BaseModel):
    id: str
    user_id: str
    dataset_id: Optional[str] = None
    base_model: str
    framework: str
    config: Optional[Dict[str, Any]] = None
    status: str
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    started_at: Optional[int] = None
    completed_at: Optional[int] = None
    failed_at: Optional[int] = None
    last_error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    output_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TrainingJobList(BaseModel):
    data: List[TrainingJobRead]
    total: int


# ---------------------------------------------------------------------------
# QUEUE DIAGNOSTIC SCHEMAS (Multi-tenant secure peek)
# ---------------------------------------------------------------------------


class TrainingQueueItem(BaseModel):
    job_id: str
    user_id: str


class TrainingQueueList(BaseModel):
    total_in_queue: int
    data: List[TrainingQueueItem]


# ---------------------------------------------------------------------------
# FINE-TUNED MODEL SCHEMAS
# ---------------------------------------------------------------------------


class FineTunedModelCreate(BaseModel):
    name: str = Field(..., max_length=128)
    description: Optional[str] = None
    base_model: str = Field(..., max_length=256)
    training_job_id: Optional[str] = None
    hf_repo: Optional[str] = None
    storage_path: Optional[str] = None


class FineTunedModelRead(BaseModel):
    id: str
    user_id: str
    training_job_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    base_model: str
    hf_repo: Optional[str] = None
    storage_path: Optional[str] = None
    is_active: bool
    vllm_model_id: Optional[str] = None
    status: str
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class FineTunedModelList(BaseModel):
    data: List[FineTunedModelRead]
    total: int


class FineTunedModelDeleted(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    deleted: bool
    model_id: str


class HubPushPayload(BaseModel):
    repo_id: Optional[str] = Field(
        default=None,
        description="Target HuggingFace repo ID. Defaults to projectdavid/{model.name}.",
    )


class ActivateModelResponse(BaseModel):
    """
    Returned by both activate_model() and activate_base_model().

    Fields:
        status:               'deploying' or 'deploying_standard'
        model_id:             The model being deployed
        node:                 Ray node ID (hex) the deployment is scheduled on
        tensor_parallel_size: Number of GPUs the model is sharded across
        next_step:            Human-readable description of what happens next
    """

    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_id: str
    node: str
    tensor_parallel_size: int = Field(
        default=1,
        ge=1,
        description="Number of GPUs this deployment is sharded across.",
    )
    next_step: str


class TrainingJobCancelResponse(BaseModel):
    """
    Returned by POST /v1/training-jobs/{job_id}/cancel.

    Idempotent — calling cancel on a job already in a terminal state
    returns the current status without error.
    """

    job_id: str
    status: str = Field(
        ...,
        description="Current job status after cancel request. "
        "One of: cancelling, cancelled, completed, failed.",
    )
    cancelled_at: Optional[int] = Field(
        default=None,
        description="Unix timestamp when cancellation was initiated. "
        "None if the job had already finished before cancel was called.",
    )
    message: str = Field(
        ...,
        description="Human-readable description of the cancel outcome.",
    )
