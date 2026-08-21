# projectdavid_common/constants/ai_model_map.py

from __future__ import annotations

# ---------------------------------------------------------------------------
# Project David internal provider namespaces
# ---------------------------------------------------------------------------
#
# These prefixes exist for Project David routing only.
#
# Once routing is complete, the prefix is removed and the remaining model
# identifier is passed directly to the selected provider.
#
# Example:
#
#   together-ai/moonshotai/Kimi-K3
#       -> moonshotai/Kimi-K3
#
#   hyperbolic/openai/gpt-oss-120b
#       -> openai/gpt-oss-120b
#
# This intentionally does NOT act as a model allowlist.
# Providers themselves remain the source of truth for whether a model exists.
#

MODEL_PROVIDER_PREFIXES = (
    "together-ai/",
    "hyperbolic/",
    "deepseek-ai/",
    "ollama/",
    "vllm/",
)


# ---------------------------------------------------------------------------
# Exceptional aliases
# ---------------------------------------------------------------------------
#
# Keep this deliberately small.
#
# These are internal routing identifiers whose provider-facing model name
# cannot be obtained simply by stripping the Project David provider prefix.
#
# Add entries here only when Project David introduces a genuine synthetic
# route or a provider has an unavoidable naming mismatch.
#

MODEL_ALIASES = {
    # Synthetic Project David deep-research route.
    "together-ai/Qwen/Qwen3-Next-80B-A3B-Instruct/deep-research": "Qwen/Qwen3-Next-80B-A3B-Instruct",
}


def translate_model_id(model: str) -> str:
    """
    Translate a Project David internal model identifier into the model
    identifier expected by the selected inference provider.

    This function performs translation only.

    It intentionally does NOT validate whether the model currently exists,
    is supported, has been deprecated, or is available to the user's
    provider account.

    Those concerns belong to provider discovery / provider error handling,
    not the routing namespace.
    """

    if not isinstance(model, str):
        return model

    model = model.strip()

    if not model:
        return model

    # Explicit synthetic routes / unavoidable naming exceptions win first.
    alias = MODEL_ALIASES.get(model)

    if alias is not None:
        return alias

    # Normal case: remove exactly one Project David routing namespace.
    for prefix in MODEL_PROVIDER_PREFIXES:
        if model.startswith(prefix):
            return model[len(prefix) :]

    # Already provider-native, or not a Project David namespaced model.
    return model


# ---------------------------------------------------------------------------
# Backwards compatibility
# ---------------------------------------------------------------------------
#
# Existing imports of MODEL_MAP should ideally be migrated to
# translate_model_id().
#
# Keep this only temporarily if old code still imports MODEL_MAP directly.
#

MODEL_MAP = MODEL_ALIASES
