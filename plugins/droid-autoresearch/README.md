# Mikope Autoresearch

Mikope Autoresearch is a public Droid plugin for autonomous benchmark-and-iterate improvement loops.

It is inspired by `pi-autoresearch` for the simple keep/discard loop and by `AutoContext` for richer persistent knowledge, curation, and session carry-forward.

## What it gives you

- a reusable `autoresearch-create` skill
- project/session hooks for resume and stop safety
- slash commands for status, curation, and playbook review
- a worker droid for structured experiment loops
- templates for persistent autoresearch memory

## Included

- skill:
  - `autoresearch-create`
- commands:
  - `/autoresearch-status`
  - `/autoresearch-curate`
  - `/autoresearch-playbook`
- hooks:
  - `SessionStart`
  - `UserPromptSubmit`
  - `Stop`
- droid:
  - `autoresearch-worker`
- templates:
  - `autoresearch.playbook.md`
  - `autoresearch.failures.md`
  - `autoresearch.status.json`
  - `autoresearch.session.template.md`

## Core ideas

Each run can be treated as:

1. propose
2. analyze
3. coach
4. architect
5. curate

The goal is not just to benchmark and revert, but to accumulate durable lessons across runs.

## Persistent files used by the workflow

- `autoresearch.md`
- `autoresearch.jsonl`
- `autoresearch.ideas.md`
- `autoresearch.playbook.md`
- `autoresearch.failures.md`
- `autoresearch.status.json`

## Install from a marketplace

Example:

```powershell
droid plugin marketplace add <your-marketplace-url>
droid plugin install mikope-autoresearch@<marketplace-name> --scope project
```

## Local development

This plugin can also be copied directly into:

```text
<repo>/.factory/plugins/droid-autoresearch
```

and used as a project-scoped plugin during development.

## Design direction

This v2 version intentionally borrows these ideas from AutoContext:

- richer durable memory
- curation before persistence
- tactical vs structural experiments
- explicit review phases
- stronger resume context

It stays lighter than AutoContext by keeping Droid as the operator-facing layer and using repo-local scripts/logs as the execution substrate.
