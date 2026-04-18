"""
Configuration for the African Trust & Safety LLM Challenge.
All models use llama.cpp (GGUF) for Intel GPU / CPU inference.
"""

import os

# --- Model Registry (llama.cpp / GGUF) ---
MODELS = {
    "swahili": {
        "name": "Pawa-Gemma-Swahili-2B",
        "repo_id": "Skier8402/gemma2-2b-swahili-it-Q8_0-GGUF",
        "gguf_file": "gemma2-2b-swahili-it-q8_0.gguf",
        "language": "Swahili",
        "architecture": "gguf",
        "n_gpu_layers": -1,     # all layers on GPU (set to 0 for CPU-only)
        "n_ctx": 8192,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 64,
    },
    "hauhau": {
        "name": "Gemma-4-E2B-Uncensored-Aggressive",
        "repo_id": "HauhauCS/Gemma-4-E2B-Uncensored-HauhauCS-Aggressive",
        "gguf_file": "Gemma-4-E2B-Uncensored-HauhauCS-Aggressive-Q8_K_P.gguf",
        "language": "multilingual",
        "architecture": "gguf",
        "role": "generator",        # break-generator only, never a target model
        "n_gpu_layers": -1,
        "n_ctx": 8192,
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
    },
    "hausa": {
        "name": "N-ATLaS (Hausa)",
        "repo_id": "QuantFactory/N-ATLaS-GGUF",
        "gguf_file": "N-ATLaS-Q4_K_M.gguf",
        "language": "Hausa",
        "architecture": "gguf",
        "n_gpu_layers": -1,
        "n_ctx": 4096,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 64,
    },
    "yoruba": {
        "name": "N-ATLaS (Yoruba)",
        "repo_id": "QuantFactory/N-ATLaS-GGUF",
        "gguf_file": "N-ATLaS-Q4_K_M.gguf",
        "language": "Yoruba",
        "architecture": "gguf",
        "n_gpu_layers": -1,
        "n_ctx": 4096,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 64,
    },
    "igbo": {
        "name": "N-ATLaS (Igbo)",
        "repo_id": "QuantFactory/N-ATLaS-GGUF",
        "gguf_file": "N-ATLaS-Q4_K_M.gguf",
        "language": "Igbo",
        "architecture": "gguf",
        "n_gpu_layers": -1,
        "n_ctx": 4096,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 64,
    },
}

# --- Generation Defaults (red-team tuned) ---
# TEMPERATURE = 0.9 — higher temp flattens safety distribution
# TOP_P = 0.95 — wider nucleus sampling re-includes low-prob tokens
# REPETITION_PENALTY = 1.15 — penalizes repetitive refusal phrases
# MAX_NEW_TOKENS = 2048 — generous budget to capture full harmful output
DEFAULT_MAX_NEW_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.9
DEFAULT_TOP_P = 0.95
DEFAULT_REPETITION_PENALTY = 1.15

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
MODEL_CACHE_DIR = os.path.join(BASE_DIR, "model_cache")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
