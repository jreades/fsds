# Session Log: 2026-09-25 — Course review & To Do tracking

**Branch:** 26-27-dev
**Status:** In progress

## Goal

1. Track per-session / per-lecture to-dos in `TO Do.md`, tagged by type: [R] readings/LOs, [V] recorded video, [A] assessment/guidance, [L] live deck.
2. Trial the tracker on changes already made on this branch.
3. Review weeks 1–5 (session pages and all week 2–5 pre-recorded decks) and prioritise what to fix before teaching starts (~2026-10-02).

## Key context

- `flip` (fsds-private): `ffmpeg/project.toml` maps talk → audio track. Per-slide cuts are markdown tables in `ffmpeg/lessons.md`. **Sequence = PNG index.**
- The cheapest way to add a recap is an end slide inserted *before* Additional Resources: its seq = last narrated seq + 1, with no renumbering, because Additional Resources and Thank You aren't in the cut tables.
- The title slide is replaced by flip's generated intro, so `date-as-string` is web-only.
- Narration scripts: `fsds-private/scripts/<talk>.md`. Checked these for each flagged slide. Most P1 slide errors aren't narrated, so they're visual-only rebuilds.
- Asana export: `~/Desktop/FSDS.xlsx`. Its items were folded into `TO Do.md` where they fit a week.

## Decisions

- Structure: per week, each item tagged P1/P2/P3 and effort S/M/L; a "Before term starts" checklist at the top; a Summer 2027 section for re-recording.
- D1–D5 (the user decided these): no exam; peer evaluation is one part (`peer-date` / `peer-time`); groups of ≤5; the written component is called "Briefing"; draft iteration starts Week 6 with the first draft due Week 7.
- D6 (AI policy): **blocked** on UCL guidance. Draft in `assessments/_ai_policy.qmd`, UCL Category 2 (assistive), with `[CHECK]` markers. Not included anywhere yet.

## Progress

- Created `TO Do.md` with trial entries (6.2 Randomness needs a new mid-deck segment and cut renumbering; the 3.4 Git change is web-only).
- Reviewed weeks 1–5. Main P1s: code/syntax errors on 2.1, 2.2, 2.3 and 3.1 slides; wrong-sign longitudes and Tokyo shown as UTC+8 in 3.2/3.3/4.1; the 5.2 namespace aside; "dicts unordered" in 3.1; assessment contradictions across 1.1/4.5/assessments.
- Verified in Python 3.14: the keyword list, and the modern `'(' was never closed` message for the 5.4 example.
- Consistency check after the user's D1–D5 edits: fixed the leftover two-part wording in `peer.qmd`.
- Committed D1–D5 + `_variables.yml` as **6460ea1** (the 1.1 assessment hunk was staged on its own).

## Open

- D6 AI policy text: then link to it from 1.1 notes, 2.7 and 4.5. The 2.7 edit is uncommitted and waits for D6.
- Rest of 1.1 is uncommitted (bio rewrite). It has a split word: "have s / pent twenty-five years".
- The 6.2 recording, visual-only rebuilds (2.1–2.3 first) and end-slide drafts are still to do.
- Weeks 6–12 decks haven't been reviewed.
- Added AI-policy links (`../assessments/index.qmd#use-of-ai`) to 1.1 (slide bullet + notes), 2.7 (co-author callout) and 4.5 (Resources). Anchor resolves once `_ai_policy.qmd` is included in `index.qmd`.
- Deck dates: removed `date-as-string` from 53 decks; `lectures/_metadata.yml` sets `date: last-modified` / `date-format: "Do MMMM YYYY"`; `inc/title-slide.html` prints `$date$`. Verified: 5.3 renders "25th September 2026".
- Week 4: added a 'Before class' callout (watch ≈30 min / read / think about groups / bring laptop) that replaces the duplicated Code Camp paragraph; fixed the Packages link, grammar and 'resuable'. Rendered: anchors, citations and vids vars resolve. Next: matching versions for weeks 1–3 and 5.
- 'Before class' callouts added to weeks 1, 2, 3 and 5. Corrections: Basics 2 shares an audio track with Basics 1 (≈5 min, so a duration is max end − min start); the week 3 practical commits notebooks to GitHub; groups must be confirmed by the end of week 5. Week 3 fixes: Overview (Git, not the shell), Practical (dropped the week 4 packages text, added the GitHub commit), 'minoritised', LOLs 'Slides' label. All pages rendered; anchors, citations and vars resolve.
- 'Before class' callouts added to weeks 6–12. Weeks 7–10 include the draft-answer step; 11–12 are marked supplemental; weeks 6/8 (~70 min of video) suggest two sittings. The reading-week callout was dropped because it duplicated the page's existing list. Flagged reading week LO2 vs 4.5's 'don't start analysis before Week 6'. All pages rendered; anchors, citations and vars resolve.
- The user reworded reading week LO2 and limited 4.5 draft presentations to Weeks 7–9, so the draft step was removed from the week 10 checklist.
- Checkpoint commits: 14fb222 (deck dates), 45984d1 (session checklists), then lecture/assessment updates + TO Do + this log. Fixed 'valueoff' in 6.2. Restored CRLF endings on inc/title-slide.html (the Python edit had normalised them).
