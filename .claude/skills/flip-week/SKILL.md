---
name: flip-week
description: Draft a flipped-class plan for one FSDS teaching week by filling in `templates/flipped-week.md` from the session page, video transcripts, lecture decks, and the lecturer's annotated readings. Use when the user says "flip week N", "/flip-week N", "plan the in-person session for week N", "make week N's prep count", or "build the session around the readings/videos". Read-only on course materials; writes one plan file.
argument-hint: "[week number] [optional: readings folder]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# Flip a Teaching Week

Produce a session plan in which every pre-class item (video, reading) has a named point in the in-person session where it gets **used**. The worked example is `quality_reports/plans/2026-10-13_week2-flipped-session.md`; match its structure and level of detail.

**Do NOT edit** session pages, decks, or transcripts. Proposed changes go in the plan.

## Configuration (machine-specific; change these here if they move)

| Input | Location |
|---|---|
| Session page | `sessions/week$N.qmd` |
| Lecture decks | `lectures/$N.*.qmd` (and any extra decks linked from the session page) |
| Video transcripts | `../fsds-private/scripts/$N.*.md` |
| Annotated readings | `~/Library/CloudStorage/Dropbox/FSDS_26-27/Readings/Week $N/` (or the folder passed as the 2nd argument) |
| PDF helper venv | `.venv` in the repo root, with `pymupdf` installed |

Room constraint (from the template): about 110 students, free seating, 120 minutes. Design with neighbour pairs and whole-room polls only.

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

5. **Read the live decks.** Note slides that already invite interaction (polls, "ask students", reorder exercises), duplicated speaker notes, unfinished notes, and obvious code bugs.

6. **Find the bridges.** Map each margin note or reading quote onto a live-deck slide that makes the same argument. This connection usually goes unused, and it is the centre of the plan. If an LO names the readings but nothing in class uses them, say so.

7. **Fill in the template** (`templates/flipped-week.md`) in the shape of the worked example:
   - Diagnosis (why preparation would be skipped *this* week, with evidence)
   - The week's question (arguable, and not a technical question)
   - Before-class actions: a draft announcement, "Listen for" hooks (one story per video, naming the story rather than the topic), the reading split if the load check says so, and the materials/poll deck to build
   - A 120-minute run sheet (table: time / block / what happens / draws on). Predict-the-output snippets must come **from the videos' own prompts**, with expected answers.
   - Cut or move (what doesn't fit in block 3: say where it should go)
   - Fixes noticed (not for this session)
   - How to tell whether it worked

8. **Load the previous week's lessons.** If `quality_reports/session_logs/` has a post-session note for week `$N-1` (template Step 6), apply its "what to change" lines and say which ones you applied.

9. **Save** to `quality_reports/plans/YYYY-MM-DD_week$N-flipped-session.md` (today's date) with `**Status:** DRAFT`.

10. **Report** in fewer than 15 lines: the file path, the week's question, the 3 strongest bridges, what you'd cut, any missing inputs, and any assumptions the user should confirm (date, room, poll tool).

## Token discipline

- Use the annotation extract, never the full PDFs (step 3).
- Transcripts are usually 5–10k words a week. Read them whole once; don't re-read.
- Don't read practical notebooks unless the user asks. The session page's "Connections" box is enough.
