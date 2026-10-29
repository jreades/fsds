# MEMORY

General lessons from working sessions, as `[LEARN:category]` entries. Machine- and user-specific notes go in `.claude/state/personal-memory.md` (gitignored). Keep this file under 200 lines.

## Quarto

- [LEARN:quarto] Shortcodes are processed even inside HTML comments. Never leave `{{< include file >}}` in a `<!-- -->` note inside the file being included: it includes itself.
- [LEARN:quarto] For a per-file date on revealjs title slides, set `date: last-modified` and `date-format: "Do MMMM YYYY"` (gives "25th September 2026") in the folder's `_metadata.yml`, and print `$date$` in the title-slide partial. It's the file's modification time at render, so it resets on a fresh clone.
- [LEARN:quarto] Code-cell figure files are named `cell-N-output-M.png`, with N one higher than the chunk's position because of a hidden setup cell. `_freeze/` can hold orphaned figures from old chunk versions, so treat the rendered HTML as authoritative.
- [LEARN:quarto] `fig-alt` is ignored for `{mermaid}` cells in revealjs output (the source is passed through as `<pre class="mermaid">`). Use Mermaid's own `accTitle:` / `accDescr:` lines instead.
- [LEARN:quarto] `quarto preview` doesn't run `post-render` scripts. Run `quarto render` before checking post-render fixes.
- [LEARN:quarto] One `quarto render --quiet` run silently left the output unchanged. When verifying, check the output file's timestamp.

## Accessibility

- [LEARN:accessibility] Quarto's revealjs template produces axe issues in every deck: a viewport meta with `maximum-scale=1.0, user-scalable=no`, footnotes in a bare `<aside>` (unnamed landmark), and a slide logo `<img>` with no `alt`. Fix them in a post-render step, not per deck.
- [LEARN:accessibility] When patching ARIA via post-render regex, changing or removing a `role` can flip an element to the implicit "generic" role, which forbids attributes like `aria-expanded`. Re-run axe after any role change.
- [LEARN:accessibility] Alt text isn't visible, so adding it to a pre-recorded deck needs neither a video rebuild nor re-recording.
- [LEARN:accessibility] Captions make a good default for `fig-alt`, but few slide images have them. Draft alt text from the slide title, surrounding text and file name, flag low-confidence ones, and have the author review before applying.

## Pre-recorded (flipped) lectures

- [LEARN:workflow] To add a recap to a recorded deck cheaply, insert one slide just after the last narrated slide and before any un-narrated "Additional Resources" slide. It then takes the next sequence number and nothing else needs renumbering. A mid-deck insertion shifts every later sequence number.
- [LEARN:workflow] Before calling a slide fix "visual-only", check the narration script doesn't read out the changed text.
- [LEARN:workflow] Rebuilding videos exports slides from whatever server the flip config names. Point it at the local preview when the fixes aren't published yet.

## Editing and verification

- [LEARN:workflow] Rules without a `paths:` scope load into every session, and scoped rules load on any matching file (a TikZ rule scoped to `scripts/**/*.py` loaded when a Python script was written). When moving a skill to `~/.claude/`, put the rules it depends on inside the skill's folder, not `~/.claude/rules/`, or they'll load in every project.

- [LEARN:workflow] Python's text-mode read/write converts CRLF to LF, turning a two-line edit into a whole-file diff. Use `open(p, newline='')` when rewriting files that may have Windows line endings.
- [LEARN:workflow] After a scripted bulk edit, verify every changed line mechanically: strip the inserted text from the new line and compare it with the original. This caught a bug that silently truncated text after the edit point.
- [LEARN:workflow] When recommending an external resource for a purpose ("close to our length"), check that property, not just that the link works. Some sites (e.g. parliament.uk) block scripted requests with 403, so confirm those via search.
- [LEARN:workflow] Keep consistency checks aligned with the author's deliberate choices: record intentional oddities (e.g. a deadline order chosen for timetabling reasons) so they aren't flagged again.

## Course design

- [LEARN:design] Weekly learning outcomes are easier to write, and easier to check for coverage, when each is tagged with the module outcome it supports. A coverage table (module outcome × weeks × assessment) shows thin spots straight away.
- [LEARN:design] A "Before class" checklist at the top of each week page (watch with durations, read, week-specific actions) answers the common student request to know "what to do" before the reading material.
- [LEARN:quarto] `draft: true` → still renders revealjs decks in full (Quarto 1.10.18) → exclude with `!file` in `project.render`; a full render wipes `_site`.
- [LEARN:pedagogy] Cold-calling and asking for volunteers → ask a pair or group while walking the room ("What did you two decide?"); add a minute of silent writing first. Week 2: the same 10% volunteered, but group answers worked.
- [LEARN:workflow] Editing a deck the lecturer also has open → their next save can silently undo it (week 3 lost the 100k Chicago change). Say which file you're editing; after the lecturer saves, diff against the last render.
- [LEARN:style] Speaker notes with provenance ("From LOLs: the video says…") and editorial asides → the lecturer trims them. Keep notes to what to do and say; reasons for slide choices go on a visible slide if they matter to students.
- [LEARN:workflow] The /flip-week report held items (assumptions, [CHECK]s, render warnings, offline steps) that weren't in the plan → the plan ends with an "Open items" section that mirrors the report.
- [LEARN:quarto] "A profile render leaves `_site` alone" → wrong: `clean` defaults to true, so any whole-project render (profiles included) empties `_site`; partial renders need `--no-clean`. `quarto publish gh-pages` runs `git rm -r .` on the branch, so the live site becomes an exact copy of `_site`.
- [LEARN:quarto] `#| label:` with spaces/brackets → invalid cell div ID, shows as "unbalanced div fence" → use hyphenated labels (e.g. `file-location-csv`)
- [LEARN:duckdb] Timing `db.sql(query)` without `.df()` → measures query construction, not execution (DuckDB is lazy) → always materialise (`.df()`) when benchmarking, and read a local file, not a URL.
- [LEARN:paths] Practical 9 saved to `data/clean`, Practical 10 read `data/geo` → spatial outputs go in `data/geo`, non-spatial in `data/clean`; when one practical hands files to the next, check writer and reader paths agree and have the reader fail with "run Practical N first".
- [LEARN:geopandas] Loading every column of the 85k-row listings geoparquet killed the kernel in a 3.6 GB container → pass `columns=[...]` to `gpd.read_parquet` for large files.
