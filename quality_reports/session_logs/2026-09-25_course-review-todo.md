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
- 2026-09-28 axe on revealjs (1.3): the warnings came from Quarto's revealjs template, not the source. Added REVEAL_PATTERNS to scripts/post.py: remove `maximum-scale=1.0, user-scalable=no` from the viewport meta (meta-viewport); give footnote `<aside>` role="note" + aria-label="Footnotes" (unnamed complementary landmarks); add alt="" to the decorative `.slide-logo` img. Verified on 1.3; patched 53 decks in _site; idempotent. Not yet re-checked in the browser's axe report.
- Alt text: 142 uncaptioned images collected with context-based proposals (35 [?]) in quality_reports/2026-09-28_lecture-alt-text.md; fig-alt copied from captions for 1.1 ACC QR and 10.1 Seaborn. Remote 404s: hackernoon (8.1:22), sklearn ml_map (12.3:185). The two missing 1.4 SVGs are on slides commented out with <!-- -->. Next: the user edits the table, then apply fig-alt/alt= at every use.
- Applied the user-edited alt text: 142 uses (fig-alt, or alt= on 10 <img> in 7.1/7.4), plus the 2 caption-derived ones; replaced the dead URLs with the user's corrections (hackernoon.imgix, sklearn 1.3 ml_map). The first apply script truncated text after images that already had attributes (hit one linked logo in 9.3); restored from git, fixed, re-applied and verified all 144 changed lines mechanically. Rendered 7.1, 8.1, 9.3: every <img> has alt.
- Code-generated figures: 20 Python figures + the 6.2 mermaid diagram lack fig-alt. Cell-N output files are offset +1 from chunk position (hidden setup cell). Proposals, with _site thumbnails, in quality_reports/2026-09-28_code-figure-alt-text.md; checked 4 figures visually. Awaiting user edits.
- Code-figure alt text: the user added fig-alt to all 21 chunks directly (my review table was redundant). Rendered 10.1, 6.2, 7.2, 7.3, 7.5, 9.2: all 20 Python figure <img>s have alt, and no image in these decks lacks one. Quarto drops fig-alt for mermaid (it passes the source through as <pre class="mermaid">), so added accTitle/accDescr to the 6.2 flowchart (bundled Mermaid 11.12 supports them); not yet checked in a browser.
