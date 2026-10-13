---
name: slide-excellence
description: Multi-agent comprehensive review of one lecture deck (visual + pedagogy + proofreading + spatial-data-science substance). Use when user says "full review", "excellence pass", "comprehensive check", "review everything", "pre-release review", "slide excellence", or before teaching a deck. Fan-out wrapper — for a single lens, use `/visual-audit`, `/pedagogy-review`, or `/proofread` directly.
argument-hint: "[QMD filename in lectures/] [--fast] [--skip-substance]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Task"]
context: fork
---

# Slide Excellence Review

## Step 1: Resolve inputs

- Deck: `$ARGUMENTS` (bare names resolve to `lectures/`).
- Narration script, if it's a recorded deck: `lectures/scripts/<same name>.md`, else `../fsds-private/scripts/<same name>.md`. Missing means a live deck.
- Detect: number of Python code cells, and whether the deck makes spatial/statistical claims (maps, CRS, regression, clustering, sampling).

## Step 2: Confirm the cost

Print the plan, then wait for "go":

```
Deck:        lectures/7.2-Geopandas.qmd   (recorded; script found)
Agents:      slide-auditor, pedagogy-reviewer, proofreader, domain-reviewer
Est. cost:   ~40–60k tokens  (--fast: ~10k, single pass)
```

If the user already ran `/proofread`, `/visual-audit` or `/pedagogy-review` on this deck this session, reuse those reports by default.

## Step 3: Run agents in parallel

| Agent | Lens | Report |
|---|---|---|
| `slide-auditor` | Overflow, font, box fatigue, spacing, images/alt text | `quality_reports/[FILE]_visual_audit.md` |
| `pedagogy-reviewer` | Narrative, pacing, prerequisites, examples, plus how deck and script fit together | `quality_reports/[FILE]_pedagogy_report.md` |
| `proofreader` | British spelling, Oxford comma, grammar, consistency, citations | `quality_reports/[FILE]_proofread_report.md` |
| `domain-reviewer` (skip with `--skip-substance`) | Spatial data science correctness and code ↔ claim consistency | `quality_reports/[FILE]_substance_review.md` |

`--fast`: no subagents. Read the deck once and cover all four lenses in one report.

For **recorded** decks, every proposed text change must be tagged **visual-only** or **needs re-record** (check the narration script before choosing).

## Step 4: Synthesise

```markdown
# Slide Excellence Review: [file]

**Deck type:** recorded / live · **Agents run:** …

| Dimension | Critical | Medium | Low |
|---|---|---|---|
| Visual | | | |
| Pedagogy | | | |
| Proofreading | | | |
| Substance | | | |

### Critical (fix before teaching)
### Medium (next revision)
### Re-record needed? (recorded decks only)
```

Overall: **Ready** (0–2 critical) · **Minor fixes** (3–5) · **Needs work** (6+).

Read-only. Don't edit the deck.
