# src/projectdavid_common/schemas/training_schema.py

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

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

    All fields are optional. Resolution order at job-create time:
        BASE_DEFAULTS → PROFILES[profile] (if profile set) → user field overrides

    The fully-resolved dict is written to TrainingJob.config and is the sole
    source of truth for the worker and trainer. No late resolution anywhere.

    The four knobs most commonly tuned in practice are:
        max_steps, learning_rate, lora_r, lora_alpha.
    The rest are exposed for power users.

    lora_alpha convention: if lora_r is set and lora_alpha is not, the service
    sets lora_alpha = lora_r automatically (standard PEFT convention).
    """

    model_config = ConfigDict(extra="forbid")

    # ── Profile preset ────────────────────────────────────────────────────
    profile: Optional[TrainingProfile] = Field(
        default=None,
        description="Hardware preset. 'laptop' = consumer GPU (8GB). "
        "'standard' = datacenter GPU. Omit to use BASE_DEFAULTS "
        "(equivalent to 'standard' for profile-scoped fields).",
    )

    # ── LoRA adapter dials ────────────────────────────────────────────────
    lora_r: Optional[int] = Field(
        default=None,
        ge=1,
        le=128,
        description="LoRA rank. Higher = more expressive adapter, larger file. "
        "Typical: 8, 16, 32, 64.",
    )
    lora_alpha: Optional[int] = Field(
        default=None,
        ge=1,
        le=256,
        description="LoRA alpha scaling. Defaults to lora_r if unset "
        "(standard PEFT convention).",
    )
    lora_dropout: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=0.5,
        description="Dropout applied to LoRA layers during training.",
    )
    bias: Optional[Literal["none", "all", "lora_only"]] = Field(
        default=None,
        description="Which biases to train. 'none' is standard for LoRA fine-tuning.",
    )

    # ── Training dynamics ─────────────────────────────────────────────────
    learning_rate: Optional[float] = Field(
        default=None,
        gt=0.0,
        le=1e-2,
        description="Optimizer learning rate. Values above 1e-2 usually diverge "
        "(safety ceiling).",
    )
    num_train_epochs: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Full passes over the dataset. Ignored if max_steps is set.",
    )
    max_steps: Optional[int] = Field(
        default=None,
        ge=1,
        le=1_000_000,
        description="Hard ceiling on training steps. Overrides num_train_epochs.",
    )
    warmup_steps: Optional[int] = Field(
        default=None,
        ge=0,
        le=10_000,
        description="Linear LR warmup steps at the start of training.",
    )
    weight_decay: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="L2 regularization strength.",
    )
    lr_scheduler_type: Optional[
        Literal["linear", "cosine", "constant", "constant_with_warmup"]
    ] = Field(
        default=None,
        description="Learning rate scheduler shape.",
    )
    optim: Optional[Literal["adamw_8bit", "adamw_torch", "sgd"]] = Field(
        default=None,
        description="Optimizer. 'adamw_8bit' is default for memory efficiency.",
    )
    seed: Optional[int] = Field(
        default=None,
        ge=0,
        le=2**31 - 1,
        description="RNG seed. Used by both SFTConfig and PEFT model init for "
        "full determinism.",
    )
    logging_steps: Optional[int] = Field(
        default=None,
        ge=1,
        le=10_000,
        description="How often to emit progress metrics. Lower = more DB writes.",
    )

    # ── Hardware scaling ──────────────────────────────────────────────────
    max_seq_length: Optional[int] = Field(
        default=None,
        ge=128,
        le=32_768,
        description="Max sequence length in tokens. Larger = more VRAM per sample.",
    )
    per_device_train_batch_size: Optional[int] = Field(
        default=None,
        ge=1,
        le=64,
        description="Samples per GPU per forward pass. Higher needs more VRAM.",
    )
    gradient_accumulation_steps: Optional[int] = Field(
        default=None,
        ge=1,
        le=256,
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
# QUEUE DIAGNOSTIC SCHEMAS
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
    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_id: str
    node: str
    tensor_parallel_size: int = Field(default=1, ge=1)
    next_step: str


class TrainingJobCancelResponse(BaseModel):
    job_id: str
    status: str
    cancelled_at: Optional[int] = None
    message: str
