---
name: flip-week
description: Draft a flipped-class plan and a draft in-person session deck for one FSDS teaching week, from the session page, video transcripts, lecture decks, and the lecturer's annotated readings. Use when the user says "flip week N", "/flip-week N", "plan the in-person session for week N", "make week N's prep count", or "build the session around the readings/videos". Never edits existing course materials; writes one plan file and one new deck (`--plan-only` skips the deck).
argument-hint: "[week number] [optional: readings folder] [optional: --plan-only]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# Flip a Teaching Week

Produce a session plan in which every pre-class item (video, reading) has a named point in the in-person session where it gets **used**. The worked example is `quality_reports/plans/2026-10-13_week2-flipped-session.md`; match its structure and level of detail.

**Do NOT edit** existing session pages, decks, or transcripts. Proposed changes go in the plan. The only new course file is the session deck (step 10), and it must never overwrite an existing file. The one permitted edit to an existing file is adding the deck's render exclusion to `_quarto.yml` (step 10).

**2026/27 scope (Tier A):** the lecturer has about 60–90 min a week. Follow the reduced pattern in `quality_reports/plans/2026-10-13_flipped-rollout-tiers.md`, not the full template: votes are with **fingers (1–4) or hands by reading**; Mentimeter (browser only, never PowerPoint) is used just for the exit ticket. No QR poll decks, short-text polls, or ranking polls. Suggest a surname split only if the readings total more than about 30 pages.

**Participation (from the week 2 post-session note):** never ask for volunteers or cold-call individuals. Questions to the room go to a pair or group ("What did you two decide?"), and which reading they used is asked only after they answer. Each neighbour discussion starts with 1 minute of silent writing. Spare time goes to neighbour discussion, not to more lecturing. Write these into the run sheet and the deck notes.

## Configuration (machine-specific; change these here if they move)

| Input | Location |
|---|---|
| Session page | `sessions/week$N.qmd` |
| Lecture decks | `lectures/$N.*.qmd` (and any extra decks linked from the session page) |
| Video transcripts | `../fsds-private/scripts/$N.*.md` |
| Annotated readings | `~/Library/CloudStorage/Dropbox/FSDS_26-27/Readings/Week $N/` (or the folder passed as the 2nd argument) |
| PDF helper venv | `.venv` in the repo root, with `pymupdf` installed |
| Lecturer's session notes (earlier years) | `~/Library/CloudStorage/Dropbox/FSDS_26-27/Week $N Session.md`. Use the admin items (e.g. group sign-up) and "Intro to the practical" for the closing slides. The readings and study guide in it may be from an older schedule: don't use them. |
| Mentimeter QR | `lectures/img/mentimeter-qr-week-$N.png` (the lecturer makes it) |

Room constraint (from the template): about 110 students, free seating, 120 minutes. Design with neighbour pairs and whole-room votes only.

## Steps

1. **Check inputs.** Confirm `$N` is given. Glob each location above and list what was found or missing. If the readings folder or transcripts are missing, say so and carry on with what exists. Don't guess at content.

2. **Read the session page.** Pull out: learning outcomes, the "Before class" list, readings, study-guide questions, the pre-recorded video table, the in-person table, and the practical focus. Note which decks are **video** and which are **live**.

3. **Extract annotations** (cheap; don't read the reading PDFs in full):
   ```bash
   [ -x .venv/bin/python ] || (python3 -m venv .venv && .venv/bin/pip -q install pymupdf)
   .venv/bin/python scripts/extract_annotations.py "<readings folder>" -o .claude/state/annotations/week$N.md
   ```
   Then read the output. Files listed under "No annotations" whose names start with `NN-` are the lecturer's reading summaries: read those with `pdftotext -layout`. Only open a full reading if it has neither annotations nor a summary, and then read just the abstract, introduction and conclusion.

4. **Read the transcripts.** For each video, note: (a) the **first-person stories** (search for "I ", "my ", "true story", "when I", and named people); (b) the "Test Yourself", "pause the video" and "discuss in class" prompts, which are promises the session must keep; (c) out-of-date references (tools, week numbers, versions).

5. **Read the live decks.** Make a slide inventory for each deck (slide title or first line, plus the line number). Note slides that already invite interaction (polls, "ask students", reorder exercises), duplicated speaker notes, unfinished notes, obvious code bugs, and **overlap between decks** (the same argument, quote or example in more than one deck). The inventory feeds the live-talk proposal in step 7. Make the same short inventory for the **video decks** (slide titles and line numbers only), with each slide's narrated length if `../fsds-private/flip.settings/lessons.md` has the cut times.

6. **Find the bridges.** Map each margin note or reading quote onto a live-deck slide that makes the same argument. This connection usually goes unused, and it is the centre of the plan. If an LO names the readings but nothing in class uses them, say so.

7. **Fill in the template** (`templates/flipped-week.md`) in the shape of the worked example:
   - Diagnosis (why preparation would be skipped *this* week, with evidence)
   - The week's question (arguable, and not a technical question)
   - Before-class actions: a draft announcement, "Listen for" hooks (one story per video, naming the story rather than the topic), the reading split if the load check says so, and the materials/poll deck to build
   - A 120-minute run sheet (table: time / block / what happens / draws on). Predict-the-output snippets must come **from the videos' own prompts**, with expected answers.
   - **The week in the round: a proposal for a live talk** (always included, even when the week has no live deck). Look at the whole week (videos, readings, live decks and the practical) and ask: *is there something that should be recapped or taken up in a short standalone live talk this week?* The talk sits in block 3. The worked example is week 2: 2.7 and 2.8 were folded into a much shorter `lectures/2.7-On_Writing.qmd`, and 2.6 became the session deck. Candidate material comes from three sources:
     - **Live decks.** Fold them into one deck with fewer slides.
     - **Pre-recorded videos.** *Pull content out* of a video into the live talk, which shortens the preparation load. Good candidates: segments that depend on discussion or judgement, segments students commonly get stuck on (if the practical or the previous week's exit tickets show it), segments that are out of date, and "we'll discuss in class" promises.
     - **Gaps.** Something the readings or the practical assume but nothing teaches, or an argument that links this week to the next.

     Give:
     1. **Recommendation first:** *no talk needed*, *fold the live decks*, *pull from the videos*, or a combination, with one sentence on why. "No talk" is a valid outcome; say what the block 3 time is used for instead.
     2. **Slide budget.** Block 3 minutes ÷ about 2 min per slide, so roughly 10–14 content slides, and no segment over 10 minutes. State the current total so the change is visible ("31 → 12", or "video 4.2: 15 → 9 min").
     3. **Disposition table**, one row per affected slide: source (deck or video) · slide (title + line) · **Keep / Merge / Cut / Move / Pull to live** · where to (the live talk, the session deck, the practical, a later week, an "Additional resources" slide) · reason in a few words. Typical reasons: duplicated elsewhere; covered by a reading (quote the reading instead); doesn't serve the week's question; works better as discussion; out of date; a story only the lecturer can tell (keep, live or recorded).
     4. **Proposed running order** of the talk as a numbered list, each item tagged with its source (`2.7 L27`, `video 3.2 L88`, `new: Donoho p.4`). Mark where a slide should become a reading quote or margin note.
     5. **Where it lives:** in the session deck (step 10) or a separate live deck, and which file. Reuse the lowest-numbered existing live deck and its filename so links survive. List the session-page rows to add, remove or rename, including the video table, the "Before class" minutes, and the "Listen for" hooks if a video gets shorter.
     6. **Video cost** for each video you propose to change, using `To_Do.md` § "How `flip` handles changes" and the narration script. Removing whole narrated slides means dropping their rows from the cut table in `../fsds-private/flip.settings/lessons.md` and renumbering the later sequences (cheap). Removing slides at the **end** is cheapest. Changing what the narration *says* means re-recording (expensive). If the narration refers to the removed material elsewhere ("as we saw earlier…"), quote those lines.
     7. **Effort estimate** in minutes (live slides plus video rebuilds), and the 3 changes that would free the most student or lecturer time if only those are done.

     This is a proposal only: never edit or delete decks, scripts or video configs.
   - Cut or move (anything not covered by the consolidation proposal, such as demos or the practical: say where it should go)
   - Fixes noticed (not for this session)
   - How to tell whether it worked

8. **Load the previous week's lessons.** If `quality_reports/session_logs/` has a post-session note for week `$N-1` (template Step 6), apply its "what to change" lines and say which ones you applied.

9. **Save** to `quality_reports/plans/YYYY-MM-DD_week$N-flipped-session.md` (today's date) with `**Status:** DRAFT`.

10. **Draft the session deck** (skip with `--plan-only`). Copy the structure, front matter and notes style of the worked example `lectures/2.6-What_We_Do.qmd`:
    0. **Last week, you said…** (2 slides): 3 quotes from the previous week's exit tickets (`data/exit-survey/`, gitignored), as written, chosen to lead into this week's question. The notes give the room's overall verdict and say that the tickets are anonymous and used. Then a visible **"Why these three?"** slide: one short line per quote linking it to today's material, and one line on the learning half. Skip both if there's no export yet, and say so in the report.
    1. **The week's question** (1 slide), with the run sheet timings in the notes.
    2. **Predict the output** (section): 3–4 snippets copied **verbatim** from the week's video decks ("Test Yourself", "what will this print?"). Use 4 numbered options for a finger vote and put the answer in a `. . .` fragment. **Run each snippet** with `.venv/bin/python -I -c` to confirm the answer. The notes name the video and the story to tell (≤ 60 seconds). If the decks have no such prompts, take short snippets from the video decks' code examples and say so in the report.
    3. **The reading verdict** (section): one vote slide (the week's question as 2–3 numbered positions, with the vote-by-reading procedure in the notes), then one slide per reading with 1–2 quotes and the lecturer's margin note in the notes. The notes give the procedure: 1 minute of silent writing, then neighbours, then a plenary that asks pairs, not volunteers.
    4. **A bridge** into the existing live material or the practical: a reading quote that leads into it, plus one question to the room.
    5. **Closing slides**, in this order (model: the end of `lectures/3.5-Session.qmd`):
       - Admin from the lecturer's `Week $N Session.md`, if any (e.g. "A Word About Groups"). Check the dates are this year's.
       - **"Intro to the practical"**: the bullets from `Week $N Session.md`, as written.
       - **"Before You Go..."**: the exit-ticket stem, built from the week's question, and "A selection will open next week's session."
       - **"Input"**: the Mentimeter link and `![Mentimeter QR Code](./img/mentimeter-qr-week-$N.png){height="500px"}`. If the link or image doesn't exist yet, write `[CHECK: menti link]` and list it in the report. The notes say: start at a fixed time (minute 110), give 3 minutes of silence, and repeat that it's anonymous.

    **Notes style.** Keep speaker notes short: what to do and what to say. Leave out where a prompt came from ("From LOLs: the video says…") and editorial asides. Call them "margin notes", not "my margin notes".

    **Quotes must be verbatim.** Take them from the annotation extract or search the PDF text with pymupdf (`.venv/bin/python -I`, PDF path as an argument). Cite as `@Key [p.N]` using the **printed** page number, not the PDF page index (check the running header). Mark omissions with `[...]` and check who is actually being quoted (for example, Donoho quoting Tukey or Claerbout). Use only keys that exist in `ref/Readings.bib`; if one is missing, write `[CHECK: key]` and list it in the report.

    **Filename:** `lectures/$N.M-Session.qmd`, where `M` is the next number not already used by a `lectures/$N.*.qmd` file. Never reuse `$N.0` (for example, `6.0-Feedback.qmd` already exists). Title the deck with the week's question. Don't add it to the session page: list the table row to add in the report.

    **Keep it off the site until after the session.** The deck contains the answers. Add `- "!lectures/$N.M-Session.qmd"` to `project.render` in `_quarto.yml`, under the existing `"*.qmd"` entry and the comment that explains it. A full render wipes `_site`, so a normal `quarto publish gh-pages` leaves the deck out. Committing it is fine (the lecturer wants the backup). Don't use `draft: true`: Quarto 1.10 still renders revealjs drafts in full.

    **Render** with `quarto render <deck>`. While the deck is excluded, this writes a standalone copy *next to the source* (`lectures/$N.M-Session.html` and `_files/`), without the site theme, and nothing to `_site/`. Check that the output was created, then scan the log for warnings or unresolved citations. Delete the standalone `.html` and `_files/`, and confirm that `_site/lectures/` has no copy of the deck.

11. **Report** in fewer than 15 lines: the plan and deck paths, the week's question, the 3 strongest bridges, the live-talk recommendation (none, fold or pull; slides or video minutes before → after; the 3 biggest changes), quotes or snippets the lecturer should check, any missing inputs, and the assumptions to confirm (date, room). Also give the offline steps. **To present:** delete the exclusion line, render the deck and present from `_site/`; don't publish until the session is over, and never use `publish --no-render`. **After the session:** leave the line deleted, add the session-page row, then render and publish.

## Token discipline

- Use the annotation extract, never the full PDFs (step 3).
- Transcripts are usually 5–10k words a week. Read them whole once; don't re-read.
- Don't read practical notebooks unless the user asks. The session page's "Connections" box is enough.
