import os
import re
from pathlib import Path

print("~" * 50)
msg = """Don't forget to also generate the answer PDFs using:\n    quarto render --profile pracs practicals\nThese are generated to `_answers` using the `prac` profile while the web content is in `_site`."""
print(msg)
print("~" * 50)
print("To publish once you've rendered run: `quarto publish gh-pages --no-render`")

# Quarto's stock website templates emit several <nav> landmarks per page
# (main navbar, secondary/mobile nav, docked sidebar, TOC, page prev/next)
# none of which carry an accessible name. Axe's "landmarks must be unique"
# check flags these as duplicates since they all resolve to the same
# implicit role with no label. Add distinguishing aria-labels post-render
# since these elements come from Quarto's built-in .ejs templates, not
# project source.
# Negative lookahead guards against double-injection on incremental
# re-renders that reuse an already-labeled HTML file.
NAV_LABELS = [
    (re.compile(r'<nav class="navbar navbar-expand-lg[^"]*"(?!\s+aria-label)'), ' aria-label="Main navigation"'),
    (re.compile(r'<nav class="quarto-secondary-nav"(?!\s+aria-label)'), ' aria-label="Secondary navigation"'),
    (re.compile(r'<nav id="quarto-sidebar" class="sidebar[^"]*"(?!\s+aria-label)'), ' aria-label="Section navigation"'),
    (re.compile(r'<nav id="TOC" role="doc-toc"(?!\s+aria-label)'), ' aria-label="Table of contents"'),
    (re.compile(r'<nav class="page-navigation"(?!\s+aria-label)'), ' aria-label="Page navigation"'),
]

# Quarto's sidebaritem.ejs puts role="navigation" on every collapsible
# section's toggle link/button (sidebar-item-text and sidebar-item-toggle).
# These are accordion controls within the already-labeled sidebar nav, not
# distinct navigation regions, and every section repeats the identical
# role="navigation" + aria-label="Toggle section" combination, which axe
# flags as duplicate landmarks.
#
# These elements are <a> tags with no href, so removing role="navigation"
# outright leaves them with the implicit "generic" role, which does not
# support aria-expanded/aria-label — a worse axe violation. The correct
# role for an accordion disclosure toggle is "button" (which does support
# both attributes), and since a hrefless <a> isn't natively focusable,
# tabindex="0" is added alongside it.
ROLE_BUTTON_PATTERNS = [
    re.compile(r'(<a class="sidebar-item-text sidebar-link[^"]*"[^>]*?) role="navigation"'),
    re.compile(r'(<a class="sidebar-item-toggle[^"]*"[^>]*?) role="navigation"'),
    # Same misuse on the mobile "Toggle sidebar navigation" trigger.
    re.compile(r'(<a class="flex-grow-1 no-decor"[^>]*?) role="navigation"'),
]

# Quarto's theme CSS sets `div.sourceCode { overflow: auto; }`, making any
# code block wider than its container horizontally scrollable. That div has
# no tabindex, so a keyboard-only user can't focus it to scroll — WCAG 2.1.1
# ("scrollable region must have keyboard access", axe rule
# scrollable-region-focusable). Whether a given block actually overflows
# depends on rendered width/font, which isn't knowable from the static HTML,
# so tabindex="0" is added to every sourceCode block; this is the standard
# remediation pattern for CSS-scrollable containers and is harmless on
# blocks that never overflow (just one extra, no-op tab stop).
TABINDEX_PATTERNS = [
    re.compile(r'<div class="sourceCode"(?!\s+tabindex)'),
]


def label_nav_landmarks(output_dir: str) -> None:
    site = Path(output_dir)
    if not site.is_dir():
        return
    n_files = 0
    for html_file in site.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        original = text
        for pattern, label_attr in NAV_LABELS:
            text = pattern.sub(lambda m: m.group(0) + label_attr, text)
        for pattern in ROLE_BUTTON_PATTERNS:
            text = pattern.sub(r'\1 role="button" tabindex="0"', text)
        for pattern in TABINDEX_PATTERNS:
            text = pattern.sub(lambda m: m.group(0) + ' tabindex="0"', text)
        if text != original:
            html_file.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"[post.py] Added nav aria-labels/roles to {n_files} HTML file(s) in {site}")


_output_dir = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")
label_nav_landmarks(_output_dir)
