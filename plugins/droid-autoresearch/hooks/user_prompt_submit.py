import json
import re
from pathlib import Path


EXPLICIT_CONTINUE_PATTERNS = (
    r"\bcontinue\b",
    r"\bcontinuer\b",
    r"\bpoursuis\b",
    r"\bpoursuivre\b",
    r"\breprends\b",
    r"\breprendre\b",
    r"\blance\b",
    r"\blancer\b",
    r"\bfais\b.*\bruns?\b",
    r"\bruns?\b",
)

QUESTION_ONLY_HINTS = (
    "explique",
    "résume",
    "resume",
    "pourquoi",
    "comment",
    "tu as mis a jour",
    "tu as mis à jour",
    "c'est quoi",
    "cest quoi",
    "qu'est-ce",
    "quest ce",
)


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

    explicit_continue = any(re.search(pattern, lowered) for pattern in EXPLICIT_CONTINUE_PATTERNS)
    question_only = any(hint in lowered for hint in QUESTION_ONLY_HINTS) and not explicit_continue

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

    if question_only:
        context = (
            "Autoresearch context exists in this repository, but this user message looks like a request for explanation or clarification, "
            "not an instruction to resume experiments. Answer the question plainly without launching a new run unless the user explicitly asks to continue."
        )
    else:
        context = (
            "Autoresearch mode may be active in this repository. "
            "Before changing direction, read autoresearch.md, autoresearch.playbook.md, autoresearch.failures.md, and autoresearch.status.json, "
            "then preserve the append-only experiment history and durable lessons. "
            "The purpose is continuous improvement, so once the benchmark and checks are trustworthy, do not hesitate to test many focused experiments."
        )

    if run_count or autonomous or explicit_continue:
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
