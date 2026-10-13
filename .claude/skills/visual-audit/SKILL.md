---
name: visual-audit
description: Adversarial visual-layout audit of a Quarto revealjs `.qmd` deck. Flags overflow, font inconsistency, box fatigue, spacing, and alignment issues. Use when user says "visual audit", "check the layout", "does this overflow?", "look for visual issues", "audit the slides", or after reworking a deck's appearance. Does NOT check writing or pedagogy — pair with `/proofread` or `/pedagogy-review`.
argument-hint: "[QMD filename in lectures/]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Visual Audit of Slide Deck

Perform a thorough visual layout audit of a slide deck.

## Steps

1. **Read the slide file** specified in `$ARGUMENTS`

2. **Render** with `quarto render lectures/$ARGUMENTS` (bare names resolve to `lectures/`). Don't start servers or take screenshots. Audit the source and the rendered HTML in `_site/lectures/`, and list the slides the user should eyeball.

3. **Audit every slide for:**

   **OVERFLOW:** Content exceeding slide boundaries
   **FONT CONSISTENCY:** Inline font-size overrides, inconsistent sizes
   **BOX FATIGUE:** 2+ colored boxes on one slide, wrong box types
   **SPACING:** Missing negative margins, missing fig-align
   **LAYOUT:** Missing transitions, missing framing sentences, semantic colors

4. **Produce a report** organized by slide with severity and recommendations

5. **Follow the spacing-first principle:**
   1. Reduce vertical spacing with negative margins
   2. Consolidate lists
   3. Move displayed equations inline
   4. Reduce image/SVG size
   5. Last resort: font size reduction (never below 0.85em)
