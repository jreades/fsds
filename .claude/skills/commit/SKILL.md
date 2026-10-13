---
name: commit
description: Stage and commit changes (and optionally push / open a PR). Use ONLY on explicit commit intent — user says "commit", "ship it", "push this", "open a PR", "let's commit this", or prefixes with `/commit`. Do NOT auto-invoke on vague end-of-task phrases ("we're done", "wrap up"). Never force-pushes or skips hooks.
argument-hint: "[optional: commit message]"
allowed-tools: ["Bash", "Read", "Glob"]
---

# Commit

Default: commit to the **current branch** (usually `master` or `26-27-dev`). Push only if asked. Open a PR only if asked.

## Steps

1. **Check state**
   ```bash
   git status --short
   git diff --stat
   git log --oneline -5
   ```

2. **Verify changed `.qmd` files**: render each one (`quarto render <file>`) and check for errors, as in `.claude/rules/verification-protocol.md`. If a render fails, stop and report. The user can say "commit anyway".

3. **Stage specific files.** Never use `git add -A`. Never stage: `.claude/settings*.json`, `.claude/state/`, `quality_reports/`, data files, or stray downloads in the repo root. If unsure whether an untracked file belongs, ask.

4. **Commit.** Use `$ARGUMENTS` exactly if given. Otherwise write a message that explains *why*, not just *what*.
   ```bash
   git commit -m "$(cat <<'EOF'
   <message>
   EOF
   )"
   ```

5. **Push / PR (only if asked)**
   ```bash
   git push -u origin <branch>
   gh pr create --base master --title "<title>" --body "<summary + test plan>"
   ```

6. **Report** the commit hash, the files committed, and anything left unstaged.
