# 0001 — One folder structure for two writing plugins

Status: decided · Date: 2026-10-01

**Chosen.** Merge the two conventions:
- `story-bible.md` (screenwriting `sw-workflow`) = session state, stage,
  decided items, decision log. Conclusions only.
- `kb/` + `work/` (creative-writing-skills) = per-concept wiki and scratch.
- `production/` = CapCut handoff (neither plugin covers it).
- `CLAUDE.md` = shared contract both plugins read.

**Why.** sw-workflow needs one short file to resume across sessions;
creative-writing agents (muse, critic, continuity-checker…) look for `kb/`
and `work/`. Linking the bible to kb pages keeps one source of truth.

**Rejected.** Two parallel structures (would drift); everything in the
bible (exceeds its size limit, breaks kb-based agents).
