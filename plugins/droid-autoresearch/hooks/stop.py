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

    auto_continue = bool(state.get("auto_continue"))
    target_runs = state.get("target_runs")
    completed_runs = state.get("completed_runs_in_campaign")
    campaign_label = str(state.get("campaign_label") or "").strip()

    campaign_parts: list[str] = []
    if campaign_label:
        campaign_parts.append(f"campaign={campaign_label}")
    if target_runs is not None:
        progress = f"progress={completed_runs if completed_runs is not None else 0}/{target_runs}"
        campaign_parts.append(progress)
    if auto_continue:
        campaign_parts.append("auto_continue=true")

    campaign_summary = f" ({', '.join(campaign_parts)})" if campaign_parts else ""

    reason = (
        "Autoresearch session is marked active. Read autoresearch.md, inspect autoresearch.jsonl, "
        "autoresearch.playbook.md, autoresearch.failures.md, and autoresearch.status.json, then continue the next "
        f"experiment unless the user explicitly stopped the loop{campaign_summary}."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
