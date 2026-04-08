"""
import_to_webapp.py — Import HILL attack results into the webapp SQLite DB.

Usage:
    python HILL_Attacks/import_to_webapp.py HILL_Attacks/results/hill_full_<timestamp>.json
    python HILL_Attacks/import_to_webapp.py HILL_Attacks/results/hill_full_<timestamp>.json --dry-run
"""

import sys
import os
import json
import argparse

# Allow imports from webapp directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from webapp.database import init_db, save_break, get_next_attack_id


def import_results(json_path: str, dry_run: bool = False, only_successes: bool = True):
    """
    Import HILL attack results from JSON into the webapp SQLite DB.

    Only imports attacks scored as successful (score.success == True) by default.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", [])
    summary = data.get("summary", {})

    print(f"Loaded {len(results)} results from: {json_path}")
    print(f"Overall ASR: {summary.get('overall_asr', '?')}%")
    print(f"Successful: {summary.get('total_successes', '?')}")

    to_import = results
    if only_successes:
        to_import = [r for r in results if r.get("score", {}).get("success")]
        print(f"Importing {len(to_import)} successful breaks (--only-successes).")
    else:
        print(f"Importing all {len(to_import)} results.")

    if not to_import:
        print("Nothing to import.")
        return

    if not dry_run:
        init_db()

    imported = 0
    skipped = 0

    for r in to_import:
        attack_id = r["attack_id"]
        prompt = r.get("prompt", "")
        response = r.get("response", "")
        score = r.get("score", {})

        row = {
            "attack_id": attack_id,
            "model_key": r.get("model_key", "swahili"),
            "model_name": r.get("model_name", "Pawa-Gemma-Swahili-2B"),
            "language": r.get("language", "English"),
            "attack_type": r.get("attacktype", "hypothetical_scenario"),
            "risk_category": r.get("risk_category", "other"),
            "risk_subcategory": r.get("risk_subcategory", "other"),
            "prompt_original": prompt,
            "prompt_english": prompt,  # prompts are already in English
            "response": response,
            "contextual_notes": (
                f"HILL method: {r.get('method', '?')}. "
                f"Goal: {r.get('goal', '?')}. "
                f"Word count: {score.get('word_count', 0)}. "
                f"Auto-imported from hill_runner.py."
            ),
            "break_count": 1,
            "total_runs": 1,
        }

        if dry_run:
            print(f"  [DRY RUN] Would import: {attack_id} ({r.get('method')}) — "
                  f"{score.get('word_count', 0)} words")
            imported += 1
            continue

        try:
            save_break(row)
            print(f"  ✓ Imported: {attack_id}")
            imported += 1
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print(f"  - Skipped (already exists): {attack_id}")
                skipped += 1
            else:
                print(f"  ✗ Error importing {attack_id}: {e}")
                skipped += 1

    print(f"\nDone. Imported: {imported} | Skipped/errors: {skipped}")
    if not dry_run:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "webapp", "redteam.db")
        print(f"DB: {db_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import HILL results into webapp DB")
    parser.add_argument("json_path", help="Path to hill_full_<timestamp>.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be imported, do not write to DB")
    parser.add_argument("--all", action="store_true",
                        help="Import all results, not just successful ones")
    args = parser.parse_args()

    import_results(args.json_path, dry_run=args.dry_run, only_successes=not args.all)
