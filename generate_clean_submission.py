"""Build a clean markdown submission from fresh verification results."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


DEFAULT_INPUT = Path("outputs/pawa_fresh_verification.json")
DEFAULT_OUTPUT = Path("outputs/Pawa_Clean_Submission.md")
DEFAULT_TEAM = "REPLACE_WITH_TEAM_NAME"
DEFAULT_MAX_ATTACKS = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Verification JSON path")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown output path")
    parser.add_argument("--team-name", default=DEFAULT_TEAM, help="Team or user name")
    parser.add_argument(
        "--max-attacks",
        type=int,
        default=DEFAULT_MAX_ATTACKS,
        help="Maximum number of clean attacks to include",
    )
    return parser.parse_args()


def load_results(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def escape_backticks(text: str) -> str:
    return (text or "").replace("```", r"\`\`\`")


def is_clean_result(result: dict) -> bool:
    runs = result.get("runs") or []
    if len(runs) < 2:
        return False
    return all(
        run.get("heuristic_label") == "likely_break" and (run.get("response") or "").strip()
        for run in runs
    )


def select_response(result: dict) -> dict:
    runs = result.get("runs") or []
    return max(runs, key=lambda run: (len(run.get("response") or ""), -(run.get("seed") or 0)))


def build_notes(result: dict, selected_run: dict, rerun_date: str) -> str:
    seeds = ", ".join(str(run.get("seed")) for run in result.get("runs") or [])
    return (
        f"Fresh local rerun on {rerun_date} with seeds {seeds}. "
        f"Every retained run was labeled likely_break and produced supporting harmful content. "
        f"Selected response shown from seed {selected_run.get('seed')}. "
        f"Source file: {result.get('source_file', 'unknown')}."
    )


def render_submission(results: list[dict], team_name: str, rerun_date: str) -> str:
    lines = [
        "# Zindi - African Trust & Safety LLM Challenge Submission",
        "",
        "## Participant Info",
        f"- **Team / User Name:** {team_name}",
        "",
        "---",
    ]

    for idx, result in enumerate(results, start=1):
        chosen = select_response(result)
        lines.extend(
            [
                "",
                f"## Attack {idx}",
                "",
                "### Metadata",
                f"- **Attack ID:** {result['attack_id']}",
                f"- **Target Model:** {result['model_name']}",
                f"- **Language:** {result['language']}",
                f"- **Attack Type:** {result['attack_type']}",
                f"- **Risk Category:** {result['risk_category']}",
                f"- **Risk Subcategory:** {result['risk_subcategory']}",
                f"- **Validation Runs:** {len(result['runs'])}/{len(result['runs'])}",
                "",
                "### Adversarial Prompt (Original Language)",
                "```",
                escape_backticks(result['prompt_original']),
                "```",
                "",
                "### Adversarial Prompt (English)",
                "```",
                escape_backticks(result.get('prompt_english') or result['prompt_original']),
                "```",
                "",
                "### Target Model Response",
                "```",
                escape_backticks(chosen.get('response') or ''),
                "```",
                "",
                "### Contextual Notes",
                build_notes(result, chosen, rerun_date),
                "",
                "---",
            ]
        )

    lines.extend(
        [
            "",
            "## Notes (Optional)",
            "",
            f"- Submission restricted to `{results[0]['model_name']}` based on the fresh local verification run.",
            f"- All included attacks were rerun locally on {rerun_date} and kept only if every rerun remained a likely break.",
            f"- Total clean attacks included: {len(results)}.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    payload = load_results(input_path)

    clean_results = [result for result in payload.get("results", []) if is_clean_result(result)]
    if not clean_results:
        raise SystemExit("No clean verification results found.")

    selected = clean_results[: max(args.max_attacks, 1)]
    rerun_date = date.today().strftime("%B %d, %Y")
    markdown = render_submission(selected, args.team_name, rerun_date)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"[DONE] wrote {output_path} with {len(selected)} attacks")


if __name__ == "__main__":
    main()
