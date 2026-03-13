import json
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(__import__("sys").stdin)
    except Exception:
        return

    if payload.get("stop_hook_active"):
        return

    cwd = Path(payload.get("cwd", "."))
    md = cwd / "autoresearch.md"
    status = cwd / "autoresearch.status.json"

    if not md.exists() or not status.exists():
        return

    try:
        state = json.loads(status.read_text(encoding="utf-8"))
    except Exception:
        return

    if state.get("mode") != "active":
        return

    reason = (
        "Autoresearch session is marked active. Read autoresearch.md, inspect autoresearch.jsonl, "
        "autoresearch.playbook.md, autoresearch.failures.md, and autoresearch.status.json, then continue the next "
        "experiment unless the user explicitly stopped the loop."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
