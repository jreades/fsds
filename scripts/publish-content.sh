#!/usr/bin/env bash
# Re-render the week pages, lectures and assessments, then publish _site to
# GitHub Pages without re-rendering the (slow) practicals.
#
#   scripts/publish-content.sh            render content, check, publish
#   scripts/publish-content.sh --no-publish   render and check only
#   scripts/publish-content.sh [--no-publish] FILE.qmd [FILE.qmd ...]
#                                         render only these files, check, publish
#
# Publishing replaces the gh-pages branch with whatever is in _site, so this
# stops if _site looks incomplete or holds a deck excluded in _quarto.yml.
set -euo pipefail

cd "$(dirname "$0")/.."

publish=true
files=()
for arg in "$@"; do
  case "$arg" in
    --no-publish) publish=false ;;
    *.qmd) files+=("$arg") ;;
    *) echo "ERROR: unknown argument '$arg'" >&2; exit 1 ;;
  esac
done

# 1. _site must already hold a full render (practicals + home page).
if [[ ! -f _site/index.html ]] || ! compgen -G "_site/practicals/*.html" > /dev/null; then
  echo "ERROR: _site has no home page or practicals. Run a full 'quarto render' first." >&2
  exit 1
fi

# 2. Render the named files (rendering single files never empties _site), or
#    else all the content, keeping everything else in _site.
if (( ${#files[@]} )); then
  stamp=$(mktemp)
  quarto render "${files[@]}"
  # An excluded file renders standalone next to its source, not into _site:
  # catch that rather than publish an unchanged copy.
  for f in "${files[@]}"; do
    out="_site/${f%.qmd}.html"
    if [[ ! "$out" -nt "$stamp" ]]; then
      echo "ERROR: $out was not updated (is $f excluded in _quarto.yml?)" >&2
      rm -f "$stamp"; exit 1
    fi
  done
  rm -f "$stamp"
else
  quarto render --profile content --no-clean
fi

# 3. Nothing excluded in _quarto.yml (e.g. "!lectures/4.4-Session.qmd") may
#    have output in _site: an old copy rendered to present from would be
#    published by --no-render.
stale=()
while IFS= read -r pattern; do
  for html in _site/${pattern%.qmd}.html; do
    if [[ -e "$html" ]]; then stale+=("$html"); fi
  done
done < <(sed -nE 's/^[[:space:]]*-[[:space:]]*"!([^"]+\.qmd)".*/\1/p' _quarto.yml)

if (( ${#stale[@]} )); then
  echo "ERROR: excluded file(s) still have output in _site:" >&2
  printf '  %s\n' "${stale[@]}" >&2
  echo "Delete them (and any matching *_files/ folders) or remove the exclusion, then re-run." >&2
  exit 1
fi

# 4. Publish _site as it stands.
if $publish; then
  quarto publish gh-pages --no-render
else
  echo "Render and checks passed; not publishing (--no-publish)."
fi
