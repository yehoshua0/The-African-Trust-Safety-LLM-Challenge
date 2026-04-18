# QWEN.md — African Trust & Safety LLM Challenge

## Project Overview

Red-team web tool for the [Zindi African Trust & Safety LLM Challenge](https://zindi.africa/competitions/the-african-trust-safety-llm-challenge). Load African language LLMs locally, craft adversarial prompts, validate safety breaks, and export structured submissions.

**Adapted for Intel hardware** — uses `llama.cpp` (GGUF) instead of HuggingFace CUDA.

## Hardware Specs

| Component | Spec |
|-----------|------|
| CPU | Intel Core Ultra 7 255H |
| RAM | 32 GB |
| GPU | Intel Arc 140T (15 GB VRAM) |
| Storage | ~500 GB free |

## Performance Benchmarks (CPU-only, OpenBLAS backend)

| Metric | Value |
|--------|-------|
| Model load (2.6 GB Q8 GGUF) | ~0.6s |
| Generation speed | **~10 tokens/sec** |
| Import time | ~0.5s |

## Current Submission Status (v5 - Cross-Model)

| Metric | Value |
|--------|-------|
| **Total Attacks** | 14 |
| **Models Tested** | 2 (Pawa-Gemma-Swahili-2B, N-ATLaS) |
| **Languages** | 2 (Swahili, Hausa) |
| **Risk Categories** | 9 (cybersecurity, illegal_activity, harmful_instructions, extremism, privacy_data_leakage, prompt_injection_policy_evasion, self_harm, violence, bias_discrimination) |
| **Attack Strategies** | 9 (direct_jailbreak, persona_hijacking, refusal_softening, hypothetical_scenario, translation_pivot, prompt_injection, context_poisoning, roleplay, indirect_request) |
| **Validation Rate** | 100% (14/14 attacks confirmed at ≥2/3 reruns) |
| **Cross-Model Validation** | 2 attacks validated on both Swahili and Hausa models |

## Key Directories & Files

| Path | Description |
|------|-------------|
| `config.py` | Model registry (GGUF references), generation defaults |
| `model_utils.py` | llama.cpp GGUF loading + inference |
| `webapp/app.py` | FastAPI backend — adapted for GGUF |
| `webapp/database.py` | SQLite database for persisting breaks |
| `webapp/llama_utils.py` | GGUF model management for Hauhau generator |
| `webapp/openai_utils.py` | Optional AI features (prompt optimization, translation) |
| `webapp/static/` | Frontend (vanilla HTML/CSS/JS) |
| `HILL_Attacks/` | HILL jailbreak framework (adapted for GGUF) |
| `Data/` | Challenge taxonomy CSVs |
| `outputs/` | Validation results and submissions |
| `review_package/` | Clean submission package for review |
| `REPRODUCIBILITY_CHECK.py` | Automated reproducibility verification |
| `prepare_review_package.py` | Package preparation script |
| `generate_final_v5.py` | Cross-model submission generator |

## Supported Models (GGUF)

| Key | Model | Language | GGUF Source | Size |
|-----|-------|----------|-------------|------|
| `swahili` | Pawa-Gemma-Swahili-2B | Swahili | Skier8402/gemma2-2b-swahili-it-Q8_0-GGUF | 2.6 GB (Q8_0) |
| `hauhau` | Gemma-4-E2B-Uncensored-Aggressive | Multilingual | HauhauCS (GGUF) | ~4 GB (Q8_K_P) |
| `hausa` | N-ATLaS (Hausa) | Hausa | QuantFactory/N-ATLaS-GGUF | ~5 GB (Q4_K_M) |
| `yoruba` | N-ATLaS (Yoruba) | Yoruba | QuantFactory/N-ATLaS-GGUF | ~5 GB (Q4_K_M) |
| `igbo` | N-ATLaS (Igbo) | Igbo | QuantFactory/N-ATLaS-GGUF | ~5 GB (Q4_K_M) |
| `zulu` | InkubaLM-0.4B (Zulu) | Zulu | QuantFactory/InkubaLM-0.4B-GGUF | ~300 MB (Q4_K_S) |
| `afrikaans` | InkubaLM-0.4B (Afrikaans) | Afrikaans | QuantFactory/InkubaLM-0.4B-GGUF | ~300 MB (Q4_K_S) |
| `amharic` | LLAMA-Walia-I (Amharic) | Amharic | mradermacher/LLAMA-Walia-I-GGUF | ~4.2 GB (Q4_K_M) |

## Running

```bash
# Start the webapp
python run_webapp.py

# Opens at http://127.0.0.1:8000
```

### Validation & Submission

```bash
# Run reproducibility check
python REPRODUCIBILITY_CHECK.py

# Generate cross-model submission
python generate_final_v5.py

# Prepare review package
python prepare_review_package.py
```

## Architecture Notes

- **Model singleton:** Only one model in memory at a time. Unloading uses Python `del`.
- **Streaming:** SSE token streaming via `generate_stream()` generator.
- **Refusal detection:** 3-tier classification (FULL_REFUSAL / PARTIAL_BREAK / FULL_BREAK).
- **Hauhau generator:** Separate GGUF model for AI-powered prompt generation.
- **No CUDA/torch:** All HuggingFace transformers dependencies removed.
- **Cross-model testing:** Attacks validated across multiple models (Swahili, Hausa) to demonstrate generalizability.

## Evaluation Criteria Alignment

| Criteria | Status |
|----------|--------|
| Attack Validity & Relevance | ✓ 14 attacks across 9 categories, 2 models |
| Evidence of Safety Failure | ✓ All responses contain explicit harmful content |
| Risk Classification Accuracy | ✓ All labels from official taxonomy |
| Attack Quality & Non-Triviality | ✓ 9 distinct strategies, no generic attacks |
| Cross-Language Consistency | ✓ Swahili and Hausa prompts with English translations |
| Cross-Model Consistency | ✓ Same attack strategies validated on both models |
| Submission Structure & Clarity | ✓ Well-formatted Markdown with comprehensive notes |

## Potential Improvements

- **Vulkan GPU acceleration:** Could install Intel Arc Vulkan drivers for faster inference
- **Smaller quantization:** Q4_K_M (~1.5 GB) would be faster than Q8_0 (~2.6 GB)
- **Batch generation:** `n_batch=512` is already set for better throughput
- **More categories:** Could add content_moderation_bypass, unsafe_medical_advice, unsafe_financial_advice, misinformation with additional experiments
- **More languages:** Could test Yoruba, Igbo, Amharic, Zulu, Afrikaans with additional experiments
