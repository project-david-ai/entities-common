# src/projectdavid_common/schemas/deployment_schemas.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivateBaseModelRequest(BaseModel):
    base_model_id: str = Field(
        ..., examples=["bm_KZcYp7GJaD4M58gBSlTlsj", "OpenGVLab/InternVL2-4B"]
    )
    target_node_id: Optional[str] = Field(default=None)
    tensor_parallel_size: int = Field(default=1, ge=1)
    gpu_memory_utilization: Optional[float] = Field(default=None, ge=0.10, le=0.95)
    max_model_len: Optional[int] = Field(default=None, ge=512)
    max_num_seqs: Optional[int] = Field(default=None, ge=1)
    quantization: Optional[str] = Field(default=None)
    dtype: Optional[str] = Field(default=None)
    enforce_eager: Optional[bool] = Field(default=None)
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(
        default=None, examples=[{"image": 2}]
    )
    mm_processor_kwargs: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Processor-level kwargs passed to the vision processor at engine init. "
            "Overrides the family registry default for this deployment only. "
            "Example: {'min_pixels': 784, 'max_pixels': 50176} for Qwen2.5-VL. "
            "Example: {'num_crops': 4} for Phi-3.5-Vision. "
            "None = family registry default applied by InferenceReconciler."
        ),
        examples=[{"min_pixels": 784, "max_pixels": 50176}, {"num_crops": 4}],
    )


class ActivateFineTunedModelRequest(BaseModel):
    model_id: str = Field(..., examples=["ftm_G05BERHAEvSRr2KTyUqWIJ"])
    target_node_id: Optional[str] = Field(default=None)
    tensor_parallel_size: int = Field(default=1, ge=1)
    gpu_memory_utilization: Optional[float] = Field(default=None, ge=0.10, le=0.95)
    max_model_len: Optional[int] = Field(default=None, ge=512)
    max_num_seqs: Optional[int] = Field(default=None, ge=1)
    quantization: Optional[str] = Field(default=None)
    dtype: Optional[str] = Field(default=None)
    enforce_eager: Optional[bool] = Field(default=None)
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(default=None)
    mm_processor_kwargs: Optional[Dict[str, Any]] = Field(default=None)


class DeploymentActivationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    model_id: str
    hf_path: Optional[str] = None
    base_model_id: Optional[str] = None
    node: str
    tensor_parallel_size: int
    gpu_memory_utilization: Optional[float] = None
    max_model_len: Optional[int] = None
    quantization: Optional[str] = None
    dtype: Optional[str] = None
    serve_route: str
    next_step: str


class DeploymentDeactivationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    model_id: Optional[str] = None
    base_model_id: Optional[str] = None


class DeactivateAllResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str


class DeploymentRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    base_model_id: str
    fine_tuned_model_id: Optional[str] = None
    node_id: str
    status: str
    tensor_parallel_size: int
    gpu_memory_utilization: Optional[float] = None
    max_model_len: Optional[int] = None
    quantization: Optional[str] = None
    dtype: Optional[str] = None
    enforce_eager: Optional[bool] = None
    limit_mm_per_prompt: Optional[Dict[str, int]] = None
    mm_processor_kwargs: Optional[Dict[str, Any]] = None
    internal_hostname: Optional[str] = None
    last_seen: int


class DeploymentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: List[DeploymentRecord] = Field(default_factory=list)
    total: int


class DeploymentUpdateRequest(BaseModel):
    gpu_memory_utilization: Optional[float] = Field(default=None, ge=0.10, le=0.95)
    max_model_len: Optional[int] = Field(default=None, ge=512)
    max_num_seqs: Optional[int] = Field(default=None, ge=1)
    quantization: Optional[str] = Field(default=None)
    dtype: Optional[str] = Field(default=None)
    enforce_eager: Optional[bool] = Field(default=None)
    limit_mm_per_prompt: Optional[Dict[str, int]] = Field(default=None)
    mm_processor_kwargs: Optional[Dict[str, Any]] = Field(default=None)
    tensor_parallel_size: Optional[int] = Field(default=None, ge=1)
