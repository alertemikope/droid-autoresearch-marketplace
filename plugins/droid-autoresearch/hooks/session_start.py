import json
from pathlib import Path


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
