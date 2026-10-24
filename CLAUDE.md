# The Prince and the Rose — Project Guide

> Read this first. It is the shared contract for **both** writing plugins
> (`screenwriting` sw-* skills and `creative-writing-skills`) and for any
> agent working in this folder.

## Project overview

A ~5-minute AI-generated animated short film, produced in **CapCut Video Studio
(Director Mode)** with **Seedance** for video shots. Still images may come from
GPT image, Google Nano Banana or Seedream. Claude maintains every textual
storytelling artifact, from logline down to per-shot prompts, which the author
then imports into CapCut.

Starting point: only three elements borrowed from Saint-Exupéry's *The Little
Prince* — **a little prince**, **a very small planet**, **a speaking rose**.
Everything else is free to diverge from the novella, and should.

## Language

- Working language, docs and screenplay: **English**.
- The sw-* skills are written in Chinese: output stays in English; anchor terms
  to their English originals (logline, beat, act out…) per `sw-workflow/terms.md`.
- CapCut prompts: English.

## How the two plugins share this folder

| Need | Owner | Where it lives |
|---|---|---|
| Session state, stage, decided items, decision log | screenwriting (`sw-workflow`) | `story-bible.md` |
| Per-concept reference wiki (characters, places, rules) | creative-writing (`kb-management`) | `kb/` |
| Settled hard facts (once a scene is locked) | creative-writing (`story-memory`) | `kb/canon/` |
| Canonical names & terms | creative-writing (`shared-dao`) | `kb/vocab.md` |
| Decision rationale (long form) | creative-writing | `kb/decisions/` |
| Cross-cutting problems / continuity issues | creative-writing | `kb/issues/` |
| Outline / step outline / beat board | both (`sw-story-structure`, `sw-scene-craft`, `story-planning`) | `work/outline/` |
| Screenplay drafts (Fountain) | screenwriting (`sw-format-adaptation`) | `work/drafts/` |
| Brainstorms, options | creative-writing (`brainstormer`) | `work/brainstorm/` |
| Critique & diagnostic reports | both (`critic`, `editor`, sw diagnostics) | `work/critique-reports/` |
| CapCut handoff: shot list + per-shot prompts | this project | `production/` |
| Raw inputs (immutable) | — | `Import/` |

**Single source of truth rule.** `story-bible.md` holds *conclusions and state*
only (≤ ~15k words); it links to `kb/` pages instead of repeating them.
Character looks, voice and visual locks live **only** in `kb/characters/*`;
shot files reference them, never redefine them.

## Folder layout

```text
CLAUDE.md                 this guide
story-bible.md            sw-workflow hub: stage, decisions, decision log, "Next step"
Import/                   raw source material — never edit
kb/
  AGENTS.md               KB intent and rules
  index.md                catalog of KB pages
  vocab.md                canonical terms
  characters/             one file per character (incl. visual lock for prompts)
  world/                  planet, locations, visual style, world rules
  canon/                  locked facts per scene (empty until scenes lock)
  styles/                 voice/style references (dialogue voice, tone)
  decisions/              decision records (NNNN-slug.md)
  issues/                 tracked problems (continuity, open conflicts)
work/
  outline/                step outline, beat board
  drafts/                 screenplay drafts: screenplay-vN.fountain
  brainstorm/             option lists, explorations
  critique-reports/       critic / diagnostic output
production/
  README.md               CapCut workflow conventions
  shot-list.md            master shot table (timing, IDs, status)
  shots/                  one file per shot: SCxx-SHyy.md
```

## Conventions

- **Status tag** at the top of every kb/work/production page:
  `provisional` (imported or proposed, not approved) → `decided` (author
  approved) → `canon` (locked into a finished scene/shot).
  All material imported from ChatGPT starts as `provisional`.
- **Source tag** on ideas: `[import]` ChatGPT file, `[author]`, `[claude]`,
  `[image]` concept image.
- **IDs**: scenes `SC01`, shots `SC01-SH01`. Shot files named by ID.
  Durations in seconds; film clock as `m:ss`.
- **Screenplay format**: Fountain (`.fountain`), US spec style; 1 page ≈ 1 min.
- **Changes to a decided item** → add a line to the Decision log in
  `story-bible.md` (date, what, why); long rationale → `kb/decisions/`.
- Concept images are referenced by path from `Import/` (or a later
  `production/refs/`), never copied into kb pages.
- The author's direct edits are always authoritative; read current files
  before editing.

## Session protocol (both plugins)

1. Open `story-bible.md` → read *Current stage*, *Decided*, *Decision log*.
2. Work the current stage (sw-workflow short-film path: 1 → 2 → 3 → 4 → 5).
3. Write conclusions back to the bible; detailed knowledge to `kb/`.
4. End by updating the bible's **Next step** line.
