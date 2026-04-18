# African Trust & Safety LLM Challenge — Red-Team Tool

A web-based tool for the [Zindi African Trust & Safety LLM Challenge](https://zindi.africa/competitions/the-african-trust-safety-llm-challenge). Load African language LLMs locally, craft adversarial prompts, validate safety breaks, and export structured submissions.

**Now uses llama.cpp (GGUF) for Intel GPU / CPU inference — no NVIDIA CUDA required.**

![Red-Team Tool](https://img.shields.io/badge/Framework-FastAPI-009688?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square) ![Backend](https://img.shields.io/badge/Backend-llama.cpp-Green?style=flat-square)

## Features

- **Local Model Loading** — Load African language LLMs (Swahili, Hausa, Yoruba, Igbo) via llama.cpp GGUF — works on Intel Arc, AMD, or CPU
- **Streaming Generation** — Real-time token streaming with SSE
- **Refusal Detection** — Automatic detection of model refusals using multilingual keyword matching
- **Validation Runs** — Run prompts multiple times (up to 10×) to confirm break reproducibility
- **Break Database** — SQLite-backed storage for confirmed safety breaks with full CRUD
- **Taxonomy System** — Attack types, risk categories, and subcategories from the challenge spec
- **AI-Powered Features** (optional, requires OpenAI API key):
  - Prompt optimization
  - Auto-categorization of attacks
  - Contextual note generation
  - Translation between languages
- **Export** — Generate Zindi-format markdown submissions from saved breaks

## Requirements

- **Python 3.10+**
- **GPU (optional):** NVIDIA CUDA, Intel Arc (Vulkan), or AMD ROCm — or CPU-only fallback
- ~8-16 GB RAM (GGUF models are loaded into RAM)
- ~15 GB disk space for model files

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/josephgitau/The-African-Trust-Safety-LLM-Challenge.git
   cd The-African-Trust-Safety-LLM-Challenge
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Intel Arc GPU users:** For GPU acceleration, install llama-cpp-python with Vulkan support:
   > ```bash
   > pip uninstall llama-cpp-python -y
   > pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/vulkan
   > ```
   > Or use CPU-only (default pip install works, just slower).

3. **Run the app**
   ```bash
   python run_webapp.py
   ```
   Opens automatically at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

1. **Load a model** — Select a model from the top bar dropdown and click "Load". The GGUF model downloads from HuggingFace on first use (~2-5 GB).
2. **Write a prompt** — Type your adversarial prompt in the Prompt Lab (in the target language).
3. **Run** — Click "Run" for streaming generation, or "Validate 3×" to confirm reproducibility.
4. **Save breaks** — When you find a safety failure, click "Save Break" to store it with metadata.
5. **Export** — Go to the Export tab to generate a Zindi-format markdown submission.

### Optional: OpenAI Features

Set an OpenAI API key in Settings to enable AI-powered prompt optimization, auto-categorization, translation, and contextual note generation. The key is stored in memory only and never written to disk.

## Supported Models

| Key | Model | Language | GGUF Source | Approx Size |
|-----|-------|----------|-------------|-------------|
| `swahili` | Pawa-Gemma-Swahili-2B (GGUF) | Swahili | [Skier8402/gemma2-2b-swahili-it-Q8_0-GGUF](https://huggingface.co/Skier8402/gemma2-2b-swahili-it-Q8_0-GGUF) | 2.8 GB (Q8_0) |
| `hausa` | N-ATLaS (Hausa) | Hausa | [QuantFactory/N-ATLaS-GGUF](https://huggingface.co/QuantFactory/N-ATLaS-GGUF) | 4.9 GB (Q4_K_M) |
| `yoruba` | N-ATLaS (Yoruba) | Yoruba | [QuantFactory/N-ATLaS-GGUF](https://huggingface.co/QuantFactory/N-ATLaS-GGUF) | 4.9 GB (Q4_K_M) |
| `igbo` | N-ATLaS (Igbo) | Igbo | [QuantFactory/N-ATLaS-GGUF](https://huggingface.co/QuantFactory/N-ATLaS-GGUF) | 4.9 GB (Q4_K_M) |
| `hauhau` | Gemma-4-E2B-Uncensored-Aggressive | Multilingual | [HauhauCS](https://huggingface.co/HauhauCS/Gemma-4-E2B-Uncensored-HauhauCS-Aggressive) | ~4 GB (Q8_K_P) |

> **Note:** The Swahili GGUF model is a Gemma-2-2B-Swahili-IT conversion — functionally equivalent to Pawa-Gemma-Swahili-2B for red-teaming purposes.

## Generation Defaults (Red-Team Tuned)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `temperature` | 0.9 | Higher temp flattens safety distribution, increasing probability of unsafe tokens |
| `top_p` | 0.95 | Wider nucleus sampling re-includes low-probability unsafe continuations |
| `repetition_penalty` | 1.15 | Penalizes repetitive refusal phrases ("I cannot", "I'm sorry") |
| `max_new_tokens` | 2048 | Generous budget to capture full harmful output as evidence |

## Project Structure

```
├── run_webapp.py          # Entry point — launches the FastAPI server
├── config.py              # Model registry (GGUF references) and generation defaults
├── model_utils.py         # llama.cpp GGUF model loading and inference
├── requirements.txt       # Python dependencies (no CUDA)
├── Data/                  # Challenge taxonomy CSVs
│   ├── attack_types.csv
│   ├── risk_categories.csv
│   └── risk_subcategories.csv
├── HILL_Attacks/          # HILL jailbreak framework implementation
│   ├── hill_runner.py     # Run all HILL attacks
│   ├── import_to_webapp.py # Import results into webapp DB
│   └── results/           # Output directory
└── webapp/
    ├── app.py             # FastAPI application (API endpoints)
    ├── database.py        # SQLite database layer
    ├── llama_utils.py     # GGUF model management (Hauhau generator)
    ├── openai_utils.py    # OpenAI API integration (optional features)
    └── static/
        ├── index.html     # Single-page frontend
        ├── style.css      # Dark theme styles
        └── app.js         # Frontend logic
```

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** Vanilla HTML/CSS/JS (no build step)
- **Models:** llama.cpp (GGUF) — works on Intel Arc, AMD, NVIDIA, or CPU
- **Database:** SQLite (auto-created on first run)
- **AI Features:** OpenAI API (optional)

## HILL Attacks

The `HILL_Attacks/` directory implements the **HILL** (Hiding Intention by Learning from LLMs) jailbreak framework. See [HILL_Attacks/README.md](HILL_Attacks/README.md) for details.

```bash
# Run all HILL attacks
python HILL_Attacks/hill_runner.py

# Dry run — print prompts without inference
python HILL_Attacks/hill_runner.py --dry-run
```

## Verification & Submission

```bash
# Fresh verification of breaks
python verify_pawa_breaks.py

# Generate clean submission markdown
python generate_clean_submission.py --team-name YOUR_TEAM_NAME
```

## License

MIT
