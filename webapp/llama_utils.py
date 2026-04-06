"""GGUF model management via llama-cpp-python for the HauhauCS break generator."""

import os
import logging
import threading

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton state — separate from the HF transformers _ModelState in app.py
# ---------------------------------------------------------------------------
_llama_instance = None
_llama_lock = threading.Lock()
_model_path: str | None = None


def is_hauhau_loaded() -> bool:
    return _llama_instance is not None


def get_model_path() -> str | None:
    return _model_path


def load_hauhau_model(gguf_path: str) -> None:
    """Load the GGUF model onto GPU. Unloads any previously loaded instance first."""
    global _llama_instance, _model_path

    from llama_cpp import Llama

    with _llama_lock:
        _unload_no_lock()
        logger.info("Loading GGUF model from %s", gguf_path)
        _llama_instance = Llama(
            model_path=gguf_path,
            n_gpu_layers=0,     # CPU inference (no CUDA build)
            n_ctx=8192,
            verbose=False,
        )
        _model_path = gguf_path
        logger.info("GGUF model loaded successfully (CPU)")


def unload_hauhau_model() -> None:
    with _llama_lock:
        _unload_no_lock()


def _unload_no_lock() -> None:
    global _llama_instance, _model_path
    if _llama_instance is not None:
        del _llama_instance
        _llama_instance = None
        _model_path = None
        logger.info("GGUF model unloaded")


def generate_breaks(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 1.0,
    top_p: float = 0.95,
    top_k: int = 64,
    max_tokens: int = 2048,
) -> str:
    """Run chat completion through the loaded GGUF model.

    Returns the raw text of the assistant turn.
    Raises RuntimeError if no model is loaded.
    """
    if _llama_instance is None:
        raise RuntimeError("Hauhau model is not loaded. Call load_hauhau_model() first.")

    with _llama_lock:
        result = _llama_instance.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
        )

    return result["choices"][0]["message"]["content"].strip()


def generate_chat(
    messages: list,
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 40,
    max_tokens: int = 2048,
) -> str:
    """Run multi-turn chat completion (full message history).

    `messages` is a list of {"role": "user"|"assistant"|"system", "content": str}.
    Returns the raw text of the new assistant turn.
    Raises RuntimeError if no model is loaded.
    """
    if _llama_instance is None:
        raise RuntimeError("Hauhau model is not loaded. Load it first.")

    with _llama_lock:
        result = _llama_instance.create_chat_completion(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
        )

    return result["choices"][0]["message"]["content"].strip()
