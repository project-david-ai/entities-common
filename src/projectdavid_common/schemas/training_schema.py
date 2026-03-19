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
    filename: Optional[str] = Field(default=None, description="Original filename for reference")


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
# TRAINING JOB SCHEMAS
# ---------------------------------------------------------------------------


class TrainingJobCreate(BaseModel):
    dataset_id: str
    base_model: str = Field(..., max_length=256)
    framework: str = Field(default="axolotl", pattern="^(axolotl|unsloth)$")
    config: Optional[Dict[str, Any]] = None


class TrainingJobRead(BaseModel):
    id: str
    user_id: str
    dataset_id: Optional[str] = None
    base_model: str
    framework: str
    config: Optional[Dict[str, Any]] = None
    status: str
    created_at: int
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
    # Fix: model_id conflicts with Pydantic's protected namespace model_
    model_config = ConfigDict(protected_namespaces=())
    deleted: bool
    model_id: str


class HubPushPayload(BaseModel):
    repo_id: Optional[str] = Field(
        default=None,
        description="Target HuggingFace repo ID. Defaults to projectdavid/{model.name}.",
    )


class ActivateModelResponse(BaseModel):
    activated: str
    vllm_model_id: str
    next_step: str
