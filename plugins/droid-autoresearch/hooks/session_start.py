import json
from pathlib import Path


def _campaign_hint(status_path: Path) -> str:
    try:
        state = json.loads(status_path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    if state.get("mode") != "active":
        return ""

    parts: list[str] = []
    label = str(state.get("campaign_label") or "").strip()
    if label:
        parts.append(f"campaign '{label}'")
    target_runs = state.get("target_runs")
    completed_runs = state.get("completed_runs_in_campaign")
    if target_runs is not None:
        parts.append(f"progress {completed_runs if completed_runs is not None else 0}/{target_runs}")
    if state.get("auto_continue"):
        parts.append("auto-continue enabled")
    if not parts:
        return ""
    return "Active autoresearch campaign detected: " + ", ".join(parts) + "."


def main() -> None:
    try:
        payload = json.load(__import__("sys").stdin)
    except Exception:
        return

    cwd = Path(payload.get("cwd", "."))
    md = cwd / "autoresearch.md"
    log = cwd / "autoresearch.jsonl"
    ideas = cwd / "autoresearch.ideas.md"
    playbook = cwd / "autoresearch.playbook.md"
    failures = cwd / "autoresearch.failures.md"
    status = cwd / "autoresearch.status.json"

    if not md.exists():
        return

    parts = [
        "Autoresearch session detected.",
        f"Read {md} before planning further experiments.",
    ]

    if log.exists():
        parts.append(f"Review recent entries in {log} before resuming.")
    if ideas.exists():
        parts.append(f"Consider pending ideas from {ideas}.")
    if playbook.exists():
        parts.append(f"Reuse only validated lessons from {playbook}.")
    if failures.exists():
        parts.append(f"Avoid repeating known-bad ideas from {failures}.")
    if status.exists():
        parts.append(f"Check current session state in {status} before choosing the next experiment.")
        hint = _campaign_hint(status)
        if hint:
            parts.append(hint)

    parts.append(
        "The purpose of autoresearch is continuous improvement: once the benchmark and guardrails are valid, do not hesitate "
        "to test many focused experiments instead of stopping after the first win."
    )

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": " ".join(parts),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
