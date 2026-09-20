# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT-MAP.md`** at the repo root: it points at one `CONTEXT.md` per context (one per course unit). Read each one relevant to the topic.
- **`docs/adr/`**: read ADRs that touch the area you're about to work in. Also check `<unit>/docs/adr/` for unit-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill creates them lazily when terms or decisions actually get resolved.

## File structure

This is a multi-context repo. Each course unit (`weekNN/`, `home_workNN/`) is its own context and owns its glossary:

```text
/
├── CONTEXT-MAP.md                     ← points at each unit's CONTEXT.md
├── docs/adr/                          ← cross-unit decisions
├── week02/
│   ├── CONTEXT.md
│   └── docs/adr/                      ← unit-specific decisions (create only when needed)
└── home_work_01/
```

A unit only gets a `CONTEXT.md` when it actually has domain vocabulary worth pinning down. Units without one are read directly from their files.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in that unit's `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Stay inside the unit

Per the repo's `CLAUDE.md`, work on a unit reads and modifies that unit's directory. Earlier units may be read for reference, but a shared concept is not a reason to edit a past week's work.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
