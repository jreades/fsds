# CLAUDE.md: Foundations of Spatial Data Science (FSDS)

UCL CASA MSc module, taught as a **flipped** class: about 110 students watch pre-recorded videos and read before a 2-hour in-person session (free seating), then attend a practical. Quarto website, published to GitHub Pages.

Writing: British spelling, Oxford comma, plain English.

## Where things are

`fsds` and `../fsds-private` are **one source** with two levels of exposure. `fsds` is public (students and the web); `fsds-private` holds narration scripts, the video build and anything not for release. Read across both freely, but don't copy private material into `fsds`, and treat the `fsds-private` copy as the only version (no mirrors in `fsds`).

| What | Where |
|---|---|
| Week pages (LOs, "Before class", readings, study guide, video/live tables) | `sessions/weekN.qmd` |
| Slide decks (revealjs), named `N.M-Title.qmd` | `lectures/` |
| Practicals (notebooks) | `practicals/` |
| Assessments + AI policy | `assessments/` |
| Bibliography | `ref/Readings.bib` (CSL: `ref/chicago-author-date.csl`) |
| Render hooks | `scripts/pre.py`, `scripts/post.py` (post-render a11y fixes) |
| Task tracker | `To_Do.md` |
| Lessons learned (`[LEARN:category]`) | `MEMORY.md` |
| Plans, session logs, reports (gitignored) | `quality_reports/` |
| Video narration scripts | `../fsds-private/scripts/N.M-Title.md` |
| Video build tool (`flip`) + config | `../fsds-private/flip/`, with cut tables in `../fsds-private/flip.settings/lessons.md` (see `To_Do.md` § "How `flip` handles changes") |
| Annotated readings + summaries (`NN-Author.pdf`) | `~/Library/CloudStorage/Dropbox/FSDS_26-27/Readings/Week N/` |

**Recorded vs live decks:** decks listed under "Pre-Recorded Lectures" on a week page have narrated videos. Changing their text may need a video rebuild or re-recording (check the narration script first). Decks under "In-Person Lectures" (e.g. 1.x, 2.6–2.8, 3.5–3.7, 5.5, 6.0, 10.2) are live-only and can be edited freely.

## Commands

```bash
quarto render                    # whole site → _site/
quarto render lectures/2.7-On_Writing.qmd   # one file
quarto render --profile content --no-clean  # sessions, lectures, assessments only (keeps rest of _site)
quarto render --profile pracs    # practicals only → _answers/
quarto preview                   # NB: doesn't run post-render scripts

scripts/publish-content.sh       # content render + checks + publish --no-render (see To_Do.md § "Rendering and publishing")

# Annotations from readings (needs .venv with pymupdf)
.venv/bin/python scripts/extract_annotations.py "<Week N folder>" -o out.md
```

`project.render` in `_quarto.yml` holds only `!` exclusions: profiles *append* to that list, so the files to render live in `_quarto-site.yml` (default), `_quarto-content.yml` and `_quarto-pracs.yml`. Any render of the whole project (profiles included) empties `_site` unless you pass `--no-clean`; `quarto publish gh-pages` replaces the branch with `_site`.

## Skills worth using here

| Skill | Use |
|---|---|
| `/flip-week N` | Flipped-session plan from the week page, transcripts, decks and annotated readings (template: `templates/flipped-week.md`) |
| `/proofread`, `/visual-audit`, `/pedagogy-review` | Read-only reviews of a deck |
| `/devils-advocate`, `/slide-excellence` | Challenge, or full review of a deck (visual + pedagogy + proofread + spatial-DS substance via `domain-reviewer`) |
| `/curriculum-reviewer` | Broader review of curriculum materials (note: may offer to apply fixes) |
| `/validate-bib` | Citations vs `ref/Readings.bib` |
| `/commit` | Commit / PR (only on explicit request) |

## Working conventions

- For multi-file or multi-step work, save a short plan to `quality_reports/plans/YYYY-MM-DD_description.md` first.
- After editing a `.qmd`, render it and check the output timestamp changed.
- Don't start local servers for visual checks: the user checks layout by eye.
- When corrected, add a `[LEARN:category] wrong → right` line to `MEMORY.md`.
