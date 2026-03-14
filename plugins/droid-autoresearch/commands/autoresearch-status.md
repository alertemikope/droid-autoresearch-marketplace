---
description: Summarize the current autoresearch session status from autoresearch.md, autoresearch.jsonl, and autoresearch.ideas.md.
disable-model-invocation: true
---

# Autoresearch Status

Inspect the current repository for these files if they exist:

- `autoresearch.md`
- `autoresearch.jsonl`
- `autoresearch.ideas.md`
- `autoresearch.status.json`

Then provide a concise status summary including:

1. objective
2. current baseline or best-known result
3. latest retained improvement
4. pending ideas or next experiments
5. whether the session appears active or inactive
6. whether an autonomous campaign is in progress
7. target runs and completed runs if present
8. whether auto-continue is enabled
9. whether the current campaign appears completed

If `autoresearch.status.json` contains campaign fields such as `target_runs`, `completed_runs_in_campaign`, `campaign_label`, `auto_continue`, or `campaign_completed`, surface them explicitly.

If the session is active, also mention whether Droid should continue improving autonomously and how far along the current campaign appears to be.

If the campaign budget appears reached, mention that the loop should stop cleanly, summarize the final state, and wait for a new user instruction instead of starting a fresh campaign automatically.

If the user provided extra arguments in `$ARGUMENTS`, use them to focus the summary.
