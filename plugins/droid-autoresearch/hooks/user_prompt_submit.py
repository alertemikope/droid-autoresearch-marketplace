import json
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

    context = (
        "Autoresearch mode may be active in this repository. "
        "Before changing direction, read autoresearch.md, autoresearch.playbook.md, autoresearch.failures.md, and autoresearch.status.json, "
        "then preserve the append-only experiment history and durable lessons."
    )

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
