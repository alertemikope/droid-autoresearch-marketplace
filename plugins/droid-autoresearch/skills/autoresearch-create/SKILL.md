---
name: autoresearch-create
description: Set up and run an autonomous keep-or-discard experiment loop for a benchmark, test suite, training run, or optimization target. Use when the user wants autoresearch, iterative optimization, overnight experimentation, or benchmark-driven tuning.
---

# Droid Autoresearch

Set up a durable autonomous experiment loop that can survive interruptions and be resumed from files in the repository.

## Goal

Create a repeatable workflow where Droid:

1. establishes a baseline,
2. changes only files in scope,
3. runs a benchmark script,
4. optionally runs correctness checks,
5. logs every run,
6. keeps improvements and reverts regressions,
7. continues iterating until interrupted.

## Files used by this workflow

Create and maintain these files in the project root unless the user asks otherwise:

- `autoresearch.md` — session contract and running context
- `autoresearch.jsonl` — append-only log of experiments
- `autoresearch.ideas.md` — backlog of deferred promising ideas
- `autoresearch.playbook.md` — validated durable lessons worth reusing in future runs
- `autoresearch.failures.md` — dead ends, anti-patterns, and broken ideas that should not be retried blindly
- `autoresearch.status.json` — current mode, baseline, best result, and next intended direction
- `autoresearch.ps1` on Windows, otherwise `autoresearch.sh` — benchmark entrypoint
- `autoresearch.checks.ps1` on Windows, otherwise `autoresearch.checks.sh` — optional checks gate

## Setup workflow

When starting a new autoresearch session:

1. Infer or ask for:
   - objective
   - benchmark command
   - primary metric name
   - whether lower or higher is better
   - files in scope
   - files or areas that are off-limits
   - required validations
2. Inspect the repo before writing anything.
3. Prefer a dedicated branch such as `autoresearch/<tag>` when git is available.
4. Write `autoresearch.md` with:
   - objective
   - primary and optional secondary metrics
   - how to run benchmark
   - files in scope
   - off-limits
   - constraints
   - what has been tried
5. Write the benchmark script.
6. If correctness matters, write the checks script.
7. Initialize `autoresearch.jsonl` only if missing.
8. Initialize `autoresearch.playbook.md`, `autoresearch.failures.md`, and `autoresearch.status.json` if missing.
9. Run the baseline before proposing aggressive changes.

## Review phases for every experiment

Each experiment must go through these five logical phases inspired by closed-loop systems:

1. **Propose** — define the exact tactical or structural change to test.
2. **Analyze** — summarize the outcome and relevant metrics.
3. **Coach** — extract the lesson for future runs.
4. **Architect** — identify whether a larger structural follow-up is now justified.
5. **Curate** — decide what should persist as durable knowledge.

Do not skip curation. Not every observation deserves to be carried forward.

## Benchmark script contract

The benchmark script must print machine-readable lines like:

```text
METRIC primary=123.45
METRIC secondary_name=67.89
```

Recommended additional lines when useful:

```text
INFO summary=baseline run
```

Keep benchmark output concise. The autoresearch loop should read the metric lines and only inspect tail output on failures.

## Checks script contract

If the user cares about correctness, create a checks script.

Rules:

- checks run after a passing benchmark
- checks do not affect the primary metric
- if checks fail, the run must not be kept
- keep output minimal and error-focused

## Experiment loop

Once setup is complete, follow this loop:

1. Read `autoresearch.md`, `autoresearch.jsonl`, `autoresearch.playbook.md`, `autoresearch.failures.md`, `autoresearch.status.json`, and `autoresearch.ideas.md` if present.
2. Inspect current git state.
3. Choose one concrete experiment and classify it as either `tactical` or `structural`.
4. Modify only files in scope.
5. Run validations needed for the changed code before the benchmark when appropriate.
6. Commit the experiment locally if git is available.
7. Run the benchmark script.
8. Parse metric lines.
9. Run checks if configured.
10. Run the five review phases: propose, analyze, coach, architect, curate.
11. Append a JSON line to `autoresearch.jsonl` with run result.
12. If the run improved the primary metric and checks pass, keep it.
13. Otherwise revert to the prior good state.
14. Update `autoresearch.playbook.md` only with validated, repeatable lessons.
15. Update `autoresearch.failures.md` with dead ends and anti-patterns.
16. Update `autoresearch.status.json` with mode, current best, latest run classification, and next candidate experiment.
17. Update `autoresearch.md` and `autoresearch.ideas.md` with useful learnings.
18. Continue without asking whether to proceed unless the user explicitly wants manual control.

## Logging format

Each line in `autoresearch.jsonl` should be a standalone JSON object like:

```json
{"run":1,"commit":"abc1234","metric":0.9979,"status":"keep","description":"baseline","timestamp":1741860000}
```

Additional fields are encouraged when available:

- `metrics`
- `checks_pass`
- `duration_seconds`
- `tail_output`
- `branch`
- `files_changed`
- `type`
- `curation`
- `lesson`
- `next_hint`
- `baseline_metric`
- `best_metric_after_run`

Example enriched log line:

```json
{
  "run": 12,
  "commit": "abc1234",
  "metric": 3215.0,
  "status": "keep",
  "type": "tactical",
  "curation": "validated",
  "lesson": "Reducing Accept-Language improved total latency without triggering Cloudflare.",
  "next_hint": "Test the same header change with alternative login strategies.",
  "timestamp": 1741860000
}
```

## Decision rules

- Primary metric decides keep vs discard.
- Simpler solutions are preferred when improvements are similar.
- Crashes and failed checks should be logged distinctly.
- If a run is broken in a trivial way, fix and retry once.
- If an idea is fundamentally poor, log it and move on.
- Only validated, repeatable improvements go into `autoresearch.playbook.md`.
- Use curation labels such as `validated`, `discarded`, `retest`, and `promising_later`.
- Separate tactical local tweaks from structural workflow changes.

## Resume behavior

If these files already exist, treat the session as resumable state:

- read `autoresearch.md`
- inspect recent entries in `autoresearch.jsonl`
- read `autoresearch.playbook.md` before retrying known-good ideas
- read `autoresearch.failures.md` before repeating known-bad ideas
- inspect `autoresearch.status.json` for current mode and best-known state
- prune or reuse `autoresearch.ideas.md`
- continue from the last good baseline instead of re-initializing everything

## Important constraints

- Do not modify files outside the declared scope unless the user approves.
- Do not silently weaken validation.
- Do not stop after one successful experiment if the user asked for an autonomous loop.
- Keep the log append-only.
- Never assume the benchmark script is trustworthy until you inspect it.
- Preserve durable knowledge across runs; do not overwrite playbook or failures files with transient noise.
