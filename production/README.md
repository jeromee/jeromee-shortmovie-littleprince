# Production — CapCut handoff

Everything here is meant to be pasted or imported into CapCut Video Studio
(Director Mode / Seedance) or an image model.

- `shot-list.md` — master table: order, ID, duration, characters, status.
- `shots/SCxx-SHyy.md` — one file per shot: purpose, action, dialogue,
  camera, the prompt, and which reference images to attach.

## Rules
- The CapCut video-prompt field accepts timestamps: write every video prompt
  as a timeline (`[0s] … [3s] … [6s] …`) ending with a `Style:` line. No
  separate single-paragraph version.
- Prompts reuse the **visual lock** paragraphs from `kb/characters/*` and
  `kb/world/*` verbatim — edit the lock there, then refresh prompts.
- One shot = one Seedance generation. Keep dialogue sayable within the
  duration (~2.5 words/s).
- Status per shot: `provisional` → `decided` → `generated` → `approved`.
- Imported prompts are kept verbatim under "Imported prompt (v0)" for
  reference; the "Current prompt" section is the one to use.
