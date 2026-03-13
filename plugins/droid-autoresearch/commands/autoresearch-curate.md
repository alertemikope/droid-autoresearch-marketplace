---
description: Curate autoresearch knowledge by separating validated lessons, failures, and deferred ideas from the experiment log.
disable-model-invocation: true
---

# Autoresearch Curate

Read these files if they exist:

- `autoresearch.jsonl`
- `autoresearch.playbook.md`
- `autoresearch.failures.md`
- `autoresearch.ideas.md`
- `autoresearch.status.json`

Then:

1. identify validated lessons worth keeping in the playbook
2. identify dead ends and anti-patterns for the failures file
3. move speculative but unvalidated ideas into the ideas backlog
4. keep `autoresearch.jsonl` append-only
5. update `autoresearch.status.json` with the current best known result and next candidate direction

If the user provided focus text in `$ARGUMENTS`, use it to constrain curation.
