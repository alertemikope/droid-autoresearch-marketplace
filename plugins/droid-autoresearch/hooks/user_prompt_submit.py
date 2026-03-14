import json
import re
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(__import__("sys").stdin)
    except Exception:
        return

    cwd = Path(payload.get("cwd", "."))
    md = cwd / "autoresearch.md"
    if not md.exists():
        return

    prompt = payload.get("prompt", "")
    if not prompt:
        return

    lowered = str(prompt).lower()
    run_count = None
    match = re.search(r"\b(?:fais|faire|lance|lancer|run|runs)\s+(\d{1,4})\s*runs?\b", lowered)
    if match:
        run_count = match.group(1)

    autonomous = any(
        phrase in lowered
        for phrase in (
            "avance tout seul",
            "ne me demande pas",
            "continue tout seul",
            "autonome",
            "sans me demander",
        )
    )

    context = (
        "Autoresearch mode may be active in this repository. "
        "Before changing direction, read autoresearch.md, autoresearch.playbook.md, autoresearch.failures.md, and autoresearch.status.json, "
        "then preserve the append-only experiment history and durable lessons. "
        "The purpose is continuous improvement, so once the benchmark and checks are trustworthy, do not hesitate to test many focused experiments."
    )

    if run_count or autonomous:
        campaign_parts: list[str] = []
        if run_count:
            campaign_parts.append(f"target_runs={run_count}")
        if autonomous:
            campaign_parts.append("auto_continue=true")
        context += " Treat this as an explicit autonomous campaign request"
        if campaign_parts:
            context += f" ({', '.join(campaign_parts)})"
        context += ". Update autoresearch.status.json accordingly before or during the loop."

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
