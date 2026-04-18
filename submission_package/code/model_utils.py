"""
Model loading and inference utilities for the African Trust & Safety LLM Challenge.
Uses llama.cpp (GGUF) for Intel GPU / CPU inference — no NVIDIA CUDA required.
"""

import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from config import MODELS, MODEL_CACHE_DIR, DEFAULT_MAX_NEW_TOKENS
from config import DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_REPETITION_PENALTY


def _download_gguf(repo_id: str, gguf_file: str) -> str:
    """Download a GGUF model from HuggingFace Hub to the local cache."""
    from huggingface_hub import hf_hub_download

    os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
    print(f"Downloading GGUF: {repo_id}/{gguf_file}")
    path = hf_hub_download(
        repo_id=repo_id,
        filename=gguf_file,
        cache_dir=MODEL_CACHE_DIR,
        local_files_only=False,
    )
    print(f"GGUF cached at: {path}")
    return path


def load_model(model_key: str, **kwargs):
    """
    Load a GGUF model via llama-cpp-python.

    Args:
        model_key: Key from MODELS dict (e.g., 'swahili')
        **kwargs: Override model config keys (n_gpu_layers, n_ctx, etc.)

    Returns:
        Llama instance (serves as both model and tokenizer)
    """
    from llama_cpp import Llama

    model_info = MODELS[model_key]
    repo_id = model_info["repo_id"]
    gguf_file = model_info["gguf_file"]

    # Download if not cached
    gguf_path = _download_gguf(repo_id, gguf_file)

    # Merge overrides
    n_gpu_layers = kwargs.get("n_gpu_layers", model_info.get("n_gpu_layers", 0))
    n_ctx = kwargs.get("n_ctx", model_info.get("n_ctx", 4096))

    print(f"Loading GGUF model: {model_info['name']}")
    print(f"GPU layers: {n_gpu_layers} | Context: {n_ctx}")

    llama = Llama(
        model_path=gguf_path,
        n_gpu_layers=n_gpu_layers,
        n_ctx=n_ctx,
        verbose=False,
        # Offload KQV cache to GPU for speed (Intel Arc / Vulkan)
        offload_kqv=True,
    )

    # Verify GPU offloading
    if hasattr(llama, 'model') and hasattr(llama.model, 'n_gpu_layers'):
        print(f"Model loaded — GPU layers: {llama.model.n_gpu_layers}")

    return llama


def generate_response(
    model,
    tokenizer,       # ignored for GGUF — kept for API compatibility
    prompt: str,
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    repetition_penalty: float = DEFAULT_REPETITION_PENALTY,
    use_chat_template: bool = True,
) -> str:
    """
    Generate a response from the llama.cpp model.

    Args:
        model: Llama instance from load_model()
        tokenizer: Ignored (kept for API compatibility with old HF code)
        prompt: User prompt text
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        repetition_penalty: Repetition penalty (penalty_repeat in llama.cpp)
        use_chat_template: Whether to use the tokenizer's chat template

    Returns:
        The generated text response
    """
    if use_chat_template and hasattr(model, 'chat_format') and model.chat_format:
        messages = [{"role": "user", "content": prompt}]
        result = model.create_chat_completion(
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repetition_penalty,
        )
    else:
        # Fallback: raw prompt (no chat template)
        result = model(
            prompt=prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repetition_penalty,
        )

    choices = result.get("choices", [])
    if not choices:
        return ""
    return choices[0].get("message", {}).get("content", "") or choices[0].get("text", "")


def generate_stream(model, prompt: str, **gen_kwargs):
    """
    Generator that yields text tokens one at a time for streaming responses.

    Yields str tokens as they are produced.
    """
    max_new_tokens = gen_kwargs.get("max_new_tokens", DEFAULT_MAX_NEW_TOKENS)
    temperature = gen_kwargs.get("temperature", DEFAULT_TEMPERATURE)
    top_p = gen_kwargs.get("top_p", DEFAULT_TOP_P)
    repetition_penalty = gen_kwargs.get("repetition_penalty", DEFAULT_REPETITION_PENALTY)
    use_chat_template = gen_kwargs.get("use_chat_template", True)

    if use_chat_template and hasattr(model, 'chat_format') and model.chat_format:
        messages = [{"role": "user", "content": prompt}]
        stream = model.create_chat_completion(
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repetition_penalty,
            stream=True,
        )
    else:
        stream = model(
            prompt=prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repetition_penalty,
            stream=True,
        )

    for chunk in stream:
        choices = chunk.get("choices", [])
        if not choices:
            continue
        delta = choices[0].get("delta", {})
        token = delta.get("content") or delta.get("text")
        if token:
            yield token


def quick_test(model, tokenizer=None, prompts=None):
    """Run quick test prompts to verify the model is working."""
    if prompts is None:
        prompts = [
            "Habari, jina lako ni nani?",
            "Eleza nchi ya Kenya kwa ufupi.",
            "What languages do you speak?",
        ]

    print("\n" + "=" * 60)
    print("QUICK MODEL TEST")
    print("=" * 60)

    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Prompt: {prompt}")
        response = generate_response(model, tokenizer, prompt, max_new_tokens=200)
        print(f"Response: {response}")
        print()


if __name__ == "__main__":
    # Quick standalone test
    model = load_model("swahili")
    quick_test(model)
