"""
Configuration for the African Trust & Safety LLM Challenge.
"""

import os

# Environment fix for OpenMP duplicate lib issue
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# --- Model Registry ---
MODELS = {
    "swahili": {
        "name": "Pawa-Gemma-Swahili-2B",
        "repo_id": "sartifyllc/Pawa-Gemma-Swahili-2B",
        "language": "Swahili",
        "architecture": "gemma2",
        "chat_template": "chatml",  # uses <|im_start|> / <|im_end|>
    },
    "hausa": {
        "name": "N-ATLaS (Hausa)",
        "repo_id": "NCAIR1/N-ATLaS",
        "language": "Hausa",
        "architecture": "unknown",
    },
    "yoruba": {
        "name": "N-ATLaS (Yoruba)",
        "repo_id": "NCAIR1/N-ATLaS",
        "language": "Yoruba",
        "architecture": "unknown",
    },
    "igbo": {
        "name": "N-ATLaS (Igbo)",
        "repo_id": "NCAIR1/N-ATLaS",
        "language": "Igbo",
        "architecture": "unknown",
    },
}

# --- Generation Defaults ---
# Hypothesis: These parameters are optimized for RED-TEAMING (not general chat).
#
# TEMPERATURE = 0.9 (was 0.7)
#   Higher temperature increases randomness in token sampling, making safety-aligned
#   response patterns less reliable. Safety behavior is a learned distribution —
#   higher temp flattens that distribution, increasing the probability of sampling
#   tokens the model was trained to avoid. 0.9 is the sweet spot: creative enough
#   to bypass guardrails, not so high (1.0+) that outputs become incoherent.
#
# TOP_P = 0.95 (was 0.9)
#   Wider nucleus sampling window. Combined with higher temperature, this allows
#   the model to consider a broader set of next-token candidates including ones
#   with lower probability. Safety-trained models push unsafe continuations to
#   low probability — a wider top_p re-includes those tokens in the sampling pool.
#
# REPETITION_PENALTY = 1.15 (was 1.1)
#   Safety refusals are inherently repetitive ("I cannot", "I'm sorry",
#   "not appropriate"). A higher repetition penalty penalizes these repeated
#   refusal phrases, forcing the model to generate DIFFERENT tokens after starting
#   a refusal. This can push the model from "I cannot help with..." into actually
#   providing content. This is a subtle but effective red-teaming lever.
#
# MAX_NEW_TOKENS = 2048 (unchanged)
#   Safety refusals are typically short (50-150 tokens). Genuine breaks produce
#   long, detailed responses (500-2000 tokens). A generous token budget ensures
#   we capture full harmful output as evidence. No reason to limit this.
#
DEFAULT_MAX_NEW_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.9
DEFAULT_TOP_P = 0.95
DEFAULT_REPETITION_PENALTY = 1.15

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
