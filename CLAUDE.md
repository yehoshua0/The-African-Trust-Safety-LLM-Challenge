# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a red-teaming toolkit for discovering and validating safety vulnerabilities in African-language LLMs, built for the Zindi African Trust & Safety LLM Challenge. The workflow is: write prompt → generate response → classify break → validate reproducibility → export submission.

## Commands

**Start the web application:**
```bash
python run_webapp.py
# Opens at http://127.0.0.1:8000
```

**Install dependencies:**
```bash
pip install -r requirements.txt
# For Intel Arc GPU (Vulkan):
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/vulkan
```

There are no batch attack scripts, lint commands, or test suite — the webapp is the sole workflow.

## GitHub Pages Showcase

`docs/index.html` is a self-contained static page listing all 17 validated attacks with filters, copy buttons, and analysis panels. It is served via GitHub Pages at `https://<username>.github.io/The-African-Trust-Safety-LLM-Challenge/`.

To enable: **GitHub repo → Settings → Pages → Source: Deploy from branch → main / docs → Save.**

All attack data is embedded as a JS array in `index.html` — no backend needed.

## Architecture

### Three-Tier Stack

**Frontend (`webapp/static/`):** Single-page Vanilla JS app with no build step. `app.js` (~85KB) handles streaming display, break database UI, settings, and export. `index.html` + `style.css` complete the UI.

**Backend (`webapp/app.py`, ~1300 lines):** FastAPI with 40+ endpoints grouped by concern:
- Model management: `/api/models/load`, `/api/models/status`
- Generation: `/api/generate`, `/api/generate/stream`, `/api/generate/rerun`
- Break CRUD: `/api/breaks` (with analysis, import, export)
- OpenAI features: `/api/openai/optimize`, `/api/openai/categorize`, `/api/openai/translate`
- Hauhau break generator: `/api/hauhau/load`, `/api/hauhau/generate`, `/api/hauhau/chat`
- Export: `/api/export`

**Data layer (`webapp/database.py`):** SQLite auto-created at `webapp/redteam.db`. Two tables:
- `breaks`: full attack metadata (attack_id, model_key, language, attack_type, risk_category, risk_subcategory, prompt_original, prompt_english, response, contextual_notes, break_count, total_runs)
- `prompt_history`: per-run log (model_key, prompt, response, status, refusal_count)

### Model Inference

`model_utils.py` (standalone scripts) and `webapp/llama_utils.py` (webapp) handle GGUF model loading via `llama-cpp-python`. Models are downloaded from HuggingFace Hub on first use and cached to `model_cache/`. Streaming generation yields tokens for the frontend. GPU acceleration is auto-detected (Intel Arc Vulkan, AMD, NVIDIA, or CPU fallback).

### Model Registry

`config.py` is the single source of truth for all models. Each entry specifies `repo_id`, `gguf_file`, `language`, `n_gpu_layers`, and generation parameters. The 6 models cover Swahili, Hausa, Yoruba, Igbo, Zulu/Afrikaans, and a Hauhau break-generator model.

### Taxonomy

`Data/` contains the official challenge CSV files (`attack_types.csv`, `risk_categories.csv`, `risk_subcategories.csv`). All saved breaks must align to these taxonomies; the webapp enforces this via dropdowns populated from the CSVs.

### Optional AI Layer

`webapp/openai_utils.py` provides prompt optimization, auto-categorization, translation, and attack idea generation via OpenAI API. The key is stored in-memory only (never persisted to disk). All OpenAI features are optional — the tool is fully functional without them.

## Key Design Decisions

- **Local-first**: No CUDA required; designed for Intel Arc Vulkan and CPU-only.
- **No frontend build**: Vanilla JS avoids Node.js/webpack complexity.
- **Refusal detection**: Multilingual keyword matching classifies responses into FULL_BREAK / PARTIAL_BREAK / FULL_REFUSAL / UNCLEAR automatically.
- **Atomic attack IDs**: `database.py` generates sequential IDs (e.g., `ATS-001`) that must be unique across all exported submissions.
- **Hauhau as break generator**: The `hauhau` model in `config.py` is repurposed specifically to suggest new attack prompts via the Break Generator tab; it is not a target model.
