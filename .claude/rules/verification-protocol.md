---
paths:
  - "lectures/**/*.qmd"
  - "sessions/**/*.qmd"
  - "practicals/**/*.qmd"
  - "assessments/**/*.qmd"
---

# Verification after editing Quarto files

At the end of a task that changed a `.qmd`, render and check it. Don't start servers or take screenshots: the user checks layout by eye.

1. `quarto render <file>`. Not `quarto preview`, which skips the post-render `scripts/post.py`.
2. Confirm the output in `_site/` has a **new timestamp** (a quiet render has silently left output unchanged before).
3. Scan the render log for errors, warnings, and unresolved citations (`[@key]` / "citation not found").
4. For recorded decks (the "Pre-Recorded Lectures" table on the week page), check whether the narration script in `../fsds-private/scripts/` reads out the changed text. If it does, the video needs re-recording, not just re-exporting (see `To_Do.md`).
5. Report: the file rendered, output path, any warnings, and which slides the user should eyeball.
