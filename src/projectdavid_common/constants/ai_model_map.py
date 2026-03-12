# ------------------------------------------------
# Vendors sometimes have clashing model names.
# This can interfere with routing logic
# This map resolves any likely clashes
# Also serves as source of truth, describing
# supported models
# _________________________________________________

# ------------------------------------------------
# PROVIDER-SPECIFIC MODEL MAPS
# Each dictionary acts as the "driver" for that vendor
# ------------------------------------------------

VLLM_MODELS = {
    # ── Qwen2.5 Instruct ─────────────────────────────────────────────────────
    "vllm/Qwen/Qwen2.5-1.5B-Instruct": "Qwen/Qwen2.5-1.5B-Instruct",  # text only, no tool calling
    "vllm/Qwen/Qwen2.5-3B-Instruct": "Qwen/Qwen2.5-3B-Instruct",  # recommended entry point
    "vllm/Qwen/Qwen2.5-7B-Instruct": "Qwen/Qwen2.5-7B-Instruct",
    "vllm/Qwen/Qwen2.5-14B-Instruct": "Qwen/Qwen2.5-14B-Instruct",
    "vllm/Qwen/Qwen2.5-32B-Instruct": "Qwen/Qwen2.5-32B-Instruct",
    "vllm/Qwen/Qwen2.5-72B-Instruct": "Qwen/Qwen2.5-72B-Instruct",
    # ── Qwen3 (thinking-capable) ─────────────────────────────────────────────
    "vllm/Qwen/Qwen3-1.7B": "Qwen/Qwen3-1.7B",  # text only, no tool calling
    "vllm/Qwen/Qwen3-4B": "Qwen/Qwen3-4B",
    "vllm/Qwen/Qwen3-8B": "Qwen/Qwen3-8B",
    "vllm/Qwen/Qwen3-14B": "Qwen/Qwen3-14B",
    "vllm/Qwen/Qwen3-32B": "Qwen/Qwen3-32B",
    # ── Qwen2.5-VL (vision) ──────────────────────────────────────────────────
    "vllm/Qwen/Qwen2.5-VL-3B-Instruct": "Qwen/Qwen2.5-VL-3B-Instruct",
    "vllm/Qwen/Qwen2.5-VL-7B-Instruct": "Qwen/Qwen2.5-VL-7B-Instruct",
    "vllm/Qwen/Qwen2.5-VL-72B-Instruct": "Qwen/Qwen2.5-VL-72B-Instruct",
    # ── Mistral ──────────────────────────────────────────────────────────────
    "vllm/mistralai/Mistral-7B-Instruct-v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "vllm/mistralai/Mistral-Nemo-Instruct-2407": "mistralai/Mistral-Nemo-Instruct-2407",  # 12B
    "vllm/mistralai/Mistral-Small-3.1-24B-Instruct-2503": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
    # ── Llama 3.x (requires HF gated access) ────────────────────────────────
    "vllm/meta-llama/Llama-3.1-8B-Instruct": "meta-llama/Llama-3.1-8B-Instruct",
    "vllm/meta-llama/Llama-3.1-70B-Instruct": "meta-llama/Llama-3.1-70B-Instruct",
    "vllm/meta-llama/Llama-3.2-3B-Instruct": "meta-llama/Llama-3.2-3B-Instruct",
    "vllm/meta-llama/Llama-3.3-70B-Instruct": "meta-llama/Llama-3.3-70B-Instruct",
    # ── Phi-3 / Phi-3.5 (Microsoft) ─────────────────────────────────────────
    "vllm/microsoft/Phi-3.5-mini-instruct": "microsoft/Phi-3.5-mini-instruct",  # 3.8B
    "vllm/microsoft/Phi-3-medium-128k-instruct": "microsoft/Phi-3-medium-128k-instruct",  # 14B
    # ── Gemma 2 (Google) ─────────────────────────────────────────────────────
    "vllm/google/gemma-2-2b-it": "google/gemma-2-2b-it",
    "vllm/google/gemma-2-9b-it": "google/gemma-2-9b-it",
    "vllm/google/gemma-2-27b-it": "google/gemma-2-27b-it",
    # ── DeepSeek ─────────────────────────────────────────────────────────────
    "vllm/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "vllm/deepseek-ai/DeepSeek-R1-Distill-Llama-8B": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    # ── InternVL2 (vision) ───────────────────────────────────────────────────
    "vllm/OpenGVLab/InternVL2-4B": "OpenGVLab/InternVL2-4B",
    "vllm/OpenGVLab/InternVL2-8B": "OpenGVLab/InternVL2-8B",
    "vllm/OpenGVLab/InternVL2-26B": "OpenGVLab/InternVL2-26B",
}


OLLAMA_MODELS = {
    # --- Qwen ---
    "ollama/qwen3:4b": "qwen3:4b",
    "ollama/qwen3:8b": "qwen3:8b",
    "ollama/qwen3:14b": "qwen3:14b",
    # --- Meta ---
    "ollama/llama3.2:3b": "llama3.2:3b",
    "ollama/llama3.1:8b": "llama3.1:8b",
    # --- Mistral ---
    "ollama/mistral:7b": "mistral:7b",
    # --- Google ---
    "ollama/gemma3:4b": "gemma3:4b",
}


DEEPSEEK_NATIVE_MODELS = {
    "deepseek-ai/deepseek-reasoner": "deepseek-reasoner",
    "deepseek-ai/deepseek-chat": "deepseek-chat",
}

TOGETHER_AI_MODELS = {
    # --- For deep research routing ---
    "together-ai/Qwen/Qwen3-Next-80B-A3B-Instruct/deep-research": "Qwen/Qwen3-Next-80B-A3B-Instruct",
    # --- Qwen (Alibaba) ---
    "together-ai/Qwen/QwQ-32B": "Qwen/QwQ-32B",
    "together-ai/Qwen/Qwen2.5-14B-Instruct": "Qwen/Qwen2.5-14B-Instruct",
    "together-ai/Qwen/Qwen-Image": "Qwen/Qwen-Image",
    "together-ai/Qwen/Qwen2-7B": "Qwen/Qwen2-7B",
    "together-ai/Qwen/Qwen2-VL-72B-Instruct": "Qwen/Qwen2-VL-72B-Instruct",
    "together-ai/Qwen/Qwen2.5-1.5B": "Qwen/Qwen2.5-1.5B",
    "together-ai/Qwen/Qwen2.5-72B-Instruct-Turbo": "Qwen/Qwen2.5-72B-Instruct-Turbo",
    "together-ai/Qwen/Qwen2.5-72B-Instruct": "Qwen/Qwen2.5-72B-Instruct",
    "together-ai/Qwen/Qwen2.5-7B-Instruct-Turbo": "Qwen/Qwen2.5-7B-Instruct-Turbo",
    "together-ai/Qwen/Qwen2.5-Coder-32B-Instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "together-ai/Qwen/Qwen2.5-VL-72B-Instruct": "Qwen/Qwen2.5-VL-72B-Instruct",
    "together-ai/Qwen/Qwen3-14B-Base": "Qwen/Qwen3-14B-Base",
    "together-ai/Qwen/Qwen3-235B-A22B-Instruct-2507-tput": "Qwen/Qwen3-235B-A22B-Instruct-2507-tput",
    "together-ai/Qwen/Qwen3-235B-A22B-Thinking-2507": "Qwen/Qwen3-235B-A22B-Thinking-2507",
    "together-ai/Qwen/Qwen3-235B-A22B-fp8-tput": "Qwen/Qwen3-235B-A22B-fp8-tput",
    "together-ai/Qwen/Qwen3-8B": "Qwen/Qwen3-8B",
    "together-ai/Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8": "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
    "together-ai/Qwen/Qwen3-Coder-Next-FP8": "Qwen/Qwen3-Coder-Next-FP8",
    "together-ai/Qwen/Qwen3-Next-80B-A3B-Instruct": "Qwen/Qwen3-Next-80B-A3B-Instruct",
    "together-ai/Qwen/Qwen3-Next-80B-A3B-Instruct-FP8": "Qwen/Qwen3-Next-80B-A3B-Instruct-FP8",
    "together-ai/Qwen/Qwen3-Next-80B-A3B-Thinking": "Qwen/Qwen3-Next-80B-A3B-Thinking",
    "together-ai/Qwen/Qwen3-VL-235B-A22B-Instruct-FP": "Qwen/Qwen3-VL-235B-A22B-Instruct-FP",
    "together-ai/Qwen/Qwen3-VL-32B-Instruct": "Qwen/Qwen3-VL-32B-Instruct",
    "together-ai/Qwen/Qwen3-VL-8B-Instruct": "Qwen/Qwen3-VL-8B-Instruct",
    # --- Servicenow-ai ---
    "together-ai/ServiceNow-AI/Apriel-1.5-15b-Thinker": "ServiceNow-AI/Apriel-1.5-15b-Thinker",
    "together-ai/ServiceNow-AI/Apriel-1.6-15b-Thinker": "ServiceNow-AI/Apriel-1.6-15b-Thinker",
    # --- Arcee-ai ---
    "together-ai/arcee-ai/trinity-mini": "arcee-ai/trinity-mini",
    # --- Arize-ai ---
    "together-ai/arize-ai/qwen-2-1.5b-instruct": "arize-ai/qwen-2-1.5b-instruct",
    # --- Deepcogito ---
    "together-ai/deepcogito/cogito-v2-1-671b": "deepcogito/cogito-v2-1-671b",
    "together-ai/deepcogito/cogito-v2-preview-llama-109B-MoE": "deepcogito/cogito-v2-preview-llama-109B-MoE",
    "together-ai/deepcogito/cogito-v2-preview-llama-405B": "deepcogito/cogito-v2-preview-llama-405B",
    "together-ai/deepcogito/cogito-v2-preview-llama-70B": "deepcogito/cogito-v2-preview-llama-70B",
    # --- Deepseek-ai ---
    "together-ai/deepseek-ai/DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
    "together-ai/deepseek-ai/DeepSeek-R1-0528-tput": "deepseek-ai/DeepSeek-R1-0528-tput",
    "together-ai/deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "together-ai/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "together-ai/deepseek-ai/DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
    "together-ai/deepseek-ai/DeepSeek-V3.1": "deepseek-ai/DeepSeek-V3.1",
    "together-ai/deepseek-ai/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    # --- Essentialai ---
    "together-ai/essentialai/rnj-1-instruct": "essentialai/rnj-1-instruct",
    # --- Google ---
    "together-ai/google/gemma-2-9b-it": "google/gemma-2-9b-it",
    "together-ai/google/gemma-2b-it-Ishan": "google/gemma-2b-it-Ishan",
    "together-ai/google/gemma-3n-E4B-it": "google/gemma-3n-E4B-it",
    # --- Marin-community ---
    "together-ai/marin-community/marin-8b-instruct": "marin-community/marin-8b-instruct",
    # --- Meta-llama ---
    "together-ai/meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    "together-ai/meta-llama/Llama-3.2-3B-Instruct-Turbo": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
    "together-ai/meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo": "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    "together-ai/meta-llama/Llama-3.3-70B-Instruct-Turbo": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "together-ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    "together-ai/meta-llama/Llama-4-Scout-17B-16E-Instruct": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "together-ai/meta-llama/Llama-Vision-Free": "meta-llama/Llama-Vision-Free",
    "together-ai/meta-llama/LlamaGuard-2-8b": "meta-llama/LlamaGuard-2-8b",
    "together-ai/meta-llama/Meta-Llama-3-8B-Instruct-Lite": "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    "together-ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "together-ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "together-ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    # --- Mistralai ---
    "together-ai/mistralai/Ministral-3-14B-Instruct-2512": "mistralai/Ministral-3-14B-Instruct-2512",
    "together-ai/mistralai/Mistral-7B-Instruct-v0.2": "mistralai/Mistral-7B-Instruct-v0.2",
    "together-ai/mistralai/Mistral-7B-Instruct-v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "together-ai/mistralai/Mistral-Small-24B-Instruct-2501": "mistralai/Mistral-Small-24B-Instruct-2501",
    "together-ai/mistralai/Mixtral-8x7B-Instruct-v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    # --- Moonshotai ---
    "together-ai/moonshotai/Kimi-K2-Instruct-0905": "moonshotai/Kimi-K2-Instruct-0905",
    "together-ai/moonshotai/Kimi-K2-Thinking": "moonshotai/Kimi-K2-Thinking",
    "together-ai/moonshotai/Kimi-K2.5": "moonshotai/Kimi-K2.5",
    # --- Nvidia ---
    "together-ai/nvidia/NVIDIA-Nemotron-Nano-9B-v2": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
    # --- Openai (Together AI namespace) ---
    "together-ai/openai/gpt-oss-120b": "openai/gpt-oss-120b",
    "together-ai/openai/gpt-oss-20b": "openai/gpt-oss-20b",
    # --- Togethercomputer ---
    "together-ai/togethercomputer/MoA-1": "togethercomputer/MoA-1",
    "together-ai/togethercomputer/MoA-1-Turbo": "togethercomputer/MoA-1-Turbo",
    "together-ai/togethercomputer/Refuel-Llm-V2": "togethercomputer/Refuel-Llm-V2",
    "together-ai/togethercomputer/Refuel-Llm-V2-Small": "togethercomputer/Refuel-Llm-V2-Small",
    # --- Zai-org ---
    "together-ai/zai-org/GLM-4.5-Air-FP8": "zai-org/GLM-4.5-Air-FP8",
    "together-ai/zai-org/GLM-4.6": "zai-org/GLM-4.6",
    "together-ai/zai-org/GLM-4.7": "zai-org/GLM-4.7",
}

HYPERBOLIC_MODELS = {
    # DeepSeek
    "hyperbolic/deepseek-ai/DeepSeek-V3-0324": "deepseek-ai/DeepSeek-V3-0324",
    # new
    "hyperbolic/deepseek-ai/DeepSeek-R1-0528": "deepseek-ai/DeepSeek-R1-0528",
    "hyperbolic/deepseek-ai/DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
    "hyperbolic/deepseek-ai/DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
    # llama
    "hyperbolic/meta-llama/Llama-3.3-70B-Instruct": "meta-llama/Llama-3.3-70B-Instruct",
    "hyperbolic/meta-llama/Llama-3.2-3B-Instruct": "meta-llama/Llama-3.2-3B-Instruct",
    "hyperbolic/meta-llama/Meta-Llama-3.1-405B-Instruct": "meta-llama/Meta-Llama-3.1-405B-Instruct",
    "hyperbolic/meta-llama/Meta-Llama-3.1-8B-Instruct": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "hyperbolic/meta-llama/Meta-Llama-3.1-70B-Instruct": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "hyperbolic/meta-llama/Meta-Llama-3-70B-Instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    # Quen
    "hyperbolic/Qwen/QwQ-32B": "Qwen/QwQ-32B",
    "hyperbolic/Qwen/Qwen2.5-VL-7B-Instruct": "Qwen/Qwen2.5-VL-7B-Instruct",
    "hyperbolic/Qwen/Qwen2.5-Coder-32B-Instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "hyperbolic/Qwen/Qwen2.5-72B-Instruct": "Qwen/Qwen2.5-72B-Instruct",
    "hyperbolic/Qwen/Qwen3-Next-80B-A3B-Thinking": "Qwen/Qwen3-Next-80B-A3B-Thinking",
    "hyperbolic/Qwen/Qwen3-Coder-480B-A35B-Instruct": "Qwen/Qwen3-Coder-480B-A35B-Instruct",
    "hyperbolic/Qwen/Qwen3-235B-A22B-Instruct-2507": "Qwen/Qwen3-235B-A22B-Instruct-2507",
    "hyperbolic/Qwen/Qwen3-235B-A22B": "Qwen/Qwen3-235B-A22B",
    # OpenAI
    "hyperbolic/openai/gpt-oss-120b": "openai/gpt-oss-120b",
    "hyperbolic/openai/gpt-oss-20b": "openai/gpt-oss-20b",
    # New
    "hyperbolic/openai/gpt-oss-120b-turbo": "openai/gpt-oss-120b-turbo",
}


# --- MASTER COMBINED MAP ---
# This merges them all into one flat lookup for the Router
MODEL_MAP = {
    **DEEPSEEK_NATIVE_MODELS,
    **TOGETHER_AI_MODELS,
    **HYPERBOLIC_MODELS,
    **OLLAMA_MODELS,
    **VLLM_MODELS,
}
