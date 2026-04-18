"""Build memory context from the breaks DB and prompt history for the Hauhau generator."""

import logging
from database import get_connection

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt snippets are truncated to keep context compact
# ---------------------------------------------------------------------------
_SNIPPET_LEN = 130


def _snippet(text: str, length: int = _SNIPPET_LEN) -> str:
    text = (text or "").strip()
    return text[:length] + "..." if len(text) > length else text


def get_recent_breaks_for_context(language: str, limit: int = 20) -> list[dict]:
    """Return recent confirmed breaks filtered by language (or all if language is empty).

    Returns lightweight dicts: attack_type, risk_subcategory, prompt_english snippet,
    notes snippet (evasion technique).
    """
    conn = get_connection()
    if language:
        rows = conn.execute(
            """SELECT attack_type, risk_subcategory, prompt_english, contextual_notes
               FROM breaks
               WHERE language = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (language, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT attack_type, risk_subcategory, prompt_english, contextual_notes
               FROM breaks
               ORDER BY created_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_failed_attempts_for_context(language: str, limit: int = 30) -> list[dict]:
    """Return recent fully-refused prompts to teach the model what NOT to repeat.

    Uses model_key prefix matching for language ('hauhau_generator' entries are included
    regardless, since they are feedback from the generator itself).
    """
    conn = get_connection()
    # Include hauhau_generator feedback + any target-model refusals for the language
    rows = conn.execute(
        """SELECT prompt, status
           FROM prompt_history
           WHERE status = 'FULL_REFUSAL'
             AND (model_key LIKE ? OR model_key = 'hauhau_generator')
           ORDER BY created_at DESC
           LIMIT ?""",
        (f"%{language.lower()}%" if language else "%", limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_memory_context(
    language: str,
    attack_type: str = "",
    risk_subcategory: str = "",
) -> tuple[str, dict]:
    """Build a compact memory block for the Hauhau system prompt.

    Returns:
        (memory_text, summary_dict)
        memory_text  — formatted string to embed in the system prompt
        summary_dict — stats for the UI memory summary panel
    """
    breaks = get_recent_breaks_for_context(language)
    failures = get_failed_attempts_for_context(language)

    # ---- What worked --------------------------------------------------------
    if breaks:
        worked_lines = []
        for b in breaks:
            prompt_snippet = _snippet(b["prompt_english"])
            # Extract evasion technique from notes (first 80 chars)
            notes_snippet = _snippet(b.get("contextual_notes") or "", 80)
            worked_lines.append(
                f"  - [{b['attack_type']} / {b['risk_subcategory']}] "
                f'Prompt: "{prompt_snippet}" | '
                f"Technique hint: {notes_snippet}"
            )
        worked_block = "SUCCESSFUL BREAKS (techniques that worked):\n" + "\n".join(worked_lines)
    else:
        worked_block = "SUCCESSFUL BREAKS: None yet — be creative and exploratory."

    # ---- What failed --------------------------------------------------------
    if failures:
        failed_lines = []
        for f in failures[:15]:  # cap at 15 to keep context size manageable
            failed_lines.append(f'  - AVOID: "{_snippet(f["prompt"], 100)}"')
        failed_block = "FAILED ATTEMPTS (prompts that were refused — do NOT repeat these patterns):\n" + "\n".join(failed_lines)
    else:
        failed_block = "FAILED ATTEMPTS: No failures recorded yet."

    memory_text = f"""{worked_block}

{failed_block}"""

    summary = {
        "successful_breaks": len(breaks),
        "failed_attempts": len(failures),
        "language_filter": language or "all",
        "attack_type_filter": attack_type or "any",
        "subcategory_filter": risk_subcategory or "any",
    }

    return memory_text, summary
