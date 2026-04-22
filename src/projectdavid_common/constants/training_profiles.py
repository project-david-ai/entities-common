"""
Canonical training configuration constants.

Single source of truth for BASE_DEFAULTS and PROFILES used by the training
config resolver (projectdavid-core server-side) and the trainer's safety-net
fallbacks (unsloth_train.py inside the training worker).

Historically these dicts were duplicated across two files in projectdavid-core,
which made drift a real risk — a change to a profile value in one location
would silently diverge from the other. Hoisting them into projectdavid_common
makes drift impossible: both consumers import the same objects.

Schemas for these constants (TrainingConfig, TrainingProfile enum, bounds,
literals) live alongside them in projectdavid_common.schemas.training_schema.
"""

from typing import Any, Dict

# ─── BASE DEFAULTS ────────────────────────────────────────────────────────────
# The fall-through values when no profile is selected and no user override is
# provided. Represents the behaviour of an empty config on a "standard" shaped
# run — equivalent to selecting profile="standard" for the profile-scoped
# fields, plus SFTConfig and PEFT defaults that aren't profile-overridable.
BASE_DEFAULTS: Dict[str, Any] = {
    # Profile-scoped (overridable by profile preset):
    "max_seq_length": 2048,
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "max_steps": 60,
    "optim": "adamw_8bit",
    # SFTConfig-scoped:
    "learning_rate": 2e-4,
    "warmup_steps": 2,
    "weight_decay": 0.01,
    "lr_scheduler_type": "linear",
    "seed": 3407,
    "logging_steps": 50,
    "num_train_epochs": 3,
    # PEFT-scoped:
    "lora_r": 32,
    "lora_alpha": 32,
    "lora_dropout": 0.0,
    "bias": "none",
}


# ─── PROFILES ─────────────────────────────────────────────────────────────────
# Profile presets that override BASE_DEFAULTS when the user selects a profile.
# Only profile-scoped fields (the top block of BASE_DEFAULTS) appear here;
# SFTConfig/PEFT defaults are not per-profile concerns.
#
# laptop:   VRAM-frugal (e.g. RTX 4060 Laptop 8GB), long-horizon runs
# standard: Desktop/small-cloud GPU (e.g. RTX 4090 24GB), default shape
PROFILES: Dict[str, Dict[str, Any]] = {
    "laptop": {
        "max_seq_length": 1024,
        "per_device_train_batch_size": 1,
        "gradient_accumulation_steps": 8,
        "max_steps": 12500,
        "optim": "adamw_8bit",
    },
    "standard": {
        "max_seq_length": 2048,
        "per_device_train_batch_size": 2,
        "gradient_accumulation_steps": 4,
        "max_steps": 60,
        "optim": "adamw_8bit",
    },
}


__all__ = ["BASE_DEFAULTS", "PROFILES"]
