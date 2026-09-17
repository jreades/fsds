# Session Log: axe accessibility diagnosis — navbar issues

**Date:** 2026-09-15
**Branch:** 26-27-dev

## Goal

User running Quarto site locally (localhost:4200) with axe accessibility testing enabled, saw two remaining violations after fixing others:
- Moderate: "Ensure landmarks are unique" — linked to `.navbar`
- Serious: "Ensure links have discernible text" — linked to `.navbar-brand-logo`

## Findings

### Serious: `.navbar-brand-logo` discernible text
Root cause: Quarto's `navbrand.ejs` template renders logo `<img>` tags with
`alt="<%- navbar.logo.light.alt || '' %>"`. `_website.yml` sets `navbar.logo`
but never `navbar.logo-alt`, so both light/dark images render `alt=""` and the
wrapping `<a class="navbar-brand navbar-brand-logo">` has no accessible name.

**Fix (not yet applied):** add `logo-alt: "Foundations of Spatial Data Science home"`
under `navbar:` in `_website.yml`.

### Moderate: `.navbar` landmarks not unique
Root cause: Stock Quarto templates emit multiple `<nav>` elements per page that
all resolve to the same implicit ARIA landmark (`role="navigation"`, no
accessible name):
- `<nav class="navbar">` (main navbar)
- `<nav class="quarto-secondary-nav">` (mobile collapse trigger)
- `<nav id="quarto-sidebar" class="sidebar...">` (docked sidebar)
- `<nav class="page-navigation">` (prev/next footer links)

These come from Quarto's built-in templates, not project source, so cannot be
fixed via `_website.yml`. Project already has a `post-render: scripts/post.py`
hook wired up in `_quarto.yml` — proposed fix is to add a step there that
injects distinguishing `aria-label` attributes into rendered HTML (e.g.
`aria-label="Main"`, `"Section navigation"`, `"Table of contents"`, `"Page
navigation"`).

## Status: Implemented

- Added `logo-alt: "Foundations of Spatial Data Science home"` under `navbar:`
  in `_website.yml`.
- Added a `label_nav_landmarks()` step to `scripts/post.py` that walks
  `$QUARTO_PROJECT_OUTPUT_DIR` (default `_site`) after render and injects
  distinguishing `aria-label` attributes into the five recurring `<nav>`
  patterns (main navbar, secondary/mobile nav, docked sidebar, TOC,
  page-navigation). Regex uses a negative lookahead so re-running on an
  already-labeled file is a no-op (safe for incremental re-renders).
- Verified via `quarto render index.qmd assessments/index.qmd`: post.py
  reported "Added nav aria-labels to 47 HTML file(s)"; grepped rendered
  output on `index.html` and `assessments/index.html` and confirmed both the
  logo alt text and all nav aria-labels are present as expected.

## Follow-up: third violation found (2026-09-15, same session)

User found a further "landmarks are unique" violation on `sessions/index.qmd`,
targeting `.sidebar-item-text`/`.sidebar-item-toggle` elements with
`role="navigation"` and `aria-label="Toggle section"`.

Root cause: Quarto's `sidebaritem.ejs` template applies `role="navigation"`
to every collapsible sidebar section's toggle link/button. These are
accordion controls inside the already-labeled sidebar `<nav>`, not distinct
navigation regions — every section repeats the identical
role="navigation" + aria-label="Toggle section" combo, which axe flags as
duplicate landmarks.

**Fix:** extended `scripts/post.py` with `ROLE_STRIP_PATTERNS` that remove
the redundant `role="navigation"` from `.sidebar-item-text.sidebar-link` and
`.sidebar-item-toggle` anchors (rather than giving each section a unique
label, which would just create landmark spam). Verified via
`quarto render sessions/index.qmd` — grep confirms `role="navigation"` is
gone from all three section toggles on that page, other attributes
(`aria-expanded`, `aria-label="Toggle section"` on the chevron) untouched.

## Correction (2026-09-15, same session): stripping role="navigation" regressed

Stripping `role="navigation"` outright (as originally implemented) left these
`<a>` elements (no `href` attribute) with the implicit "generic" role, which
does not support `aria-expanded`/`aria-label` — this traded the "duplicate
landmarks" violation for two new ones:
- Moderate: "ARIA role supports its ARIA attributes"
- Serious: "ARIA attributes are not prohibited for an element's role"

**Corrected fix:** `ROLE_STRIP_PATTERNS` replaced with `ROLE_BUTTON_PATTERNS`
in `scripts/post.py` — instead of removing the role, these toggle elements
now get `role="button" tabindex="0"` (button is the semantically correct
role for an accordion disclosure toggle, supports both `aria-expanded` and
`aria-label`, and `tabindex="0"` restores keyboard focusability lost by
having no `href`). Applied to three anchor patterns sharing this Quarto
template defect:
- `.sidebar-item-text.sidebar-link` (section heading toggle)
- `.sidebar-item-toggle` (chevron toggle)
- `.flex-grow-1.no-decor` (mobile "Toggle sidebar navigation" trigger —
  found proactively since it shares the identical root-cause pattern; not
  yet reported by axe but would very likely surface next)

Verified via `quarto render sessions/index.qmd`: all three anchor types now
render `role="button" tabindex="0"` in place of `role="navigation"`.

## Open questions

- None outstanding for this fix. User should reload localhost:4200 and
  re-run axe to confirm all violations are cleared in the live preview
  (preview may need a restart since it does incremental rendering and
  post-render scripts run on full `quarto render`, not per-file preview
  updates).
- Worth a full-site re-render + fresh axe pass across all pages once these
  fixes are confirmed, since post.py fixes only apply to files quarto
  actually re-renders.
- [LEARN:accessibility] When patching ARIA misuse via post-render regex,
  changing/removing a role can flip an element to the "generic" implicit
  role, which is stricter about permitted attributes than many explicit
  roles — always re-check with axe after a role change, not just after
  adding labels.

## Follow-up: heading order violation on sessions/week11.qmd (2026-09-16)

axe flagged a heading-order issue on `sessions/week11.html`. Root cause: the
`::: {.callout-alert}` block containing `### Supplemental` appeared before
the page's first `## Overview` section, producing h1 → h3 → h2 in the
rendered DOM (skips h2). This is a content authoring issue in the `.qmd`
source, not a Quarto template defect.

**Fix:** changed `### Supplemental` to `## Supplemental` in
`sessions/week11.qmd` so it sits as a sibling section (h1 → h2 → h2 → ...),
matching the rest of the document's structure.

Checked `sessions/week12.qmd` for the same copy-pasted pattern — it has
`## Overview` *before* its callout-alert block, so `### Supplemental` there
is correctly nested (h1 → h2 → h3, no skip) and needed no change. Its render
did throw an unrelated `pandoc: ... withBinaryFile: does not exist` error
(likely a missing referenced image/notebook file) — flagged to user,
not investigated further as out of scope for this accessibility session.

Verified via `quarto render sessions/week11.qmd`: heading sequence in
rendered HTML confirmed h1 → h2 → h2 → h2 → h2 → h2 (References/Footnotes),
no skips.

- [LEARN:accessibility] axe's heading-order check is sensitive to callout/
  admonition blocks placed before a document's first top-level section —
  check `.qmd` source structure directly (grep for `#`/`##`/`###` before
  the first `##` heading) rather than assuming template-generated markup is
  the cause, since this class of issue is a genuine authoring error.

## Follow-up: axe crashes RevealJS theme compilation (2026-09-16)

User enabled `axe: output: document` under `format.revealjs` in `_quarto.yml`
(mirroring the working `html` format config) and got a SASS compile error:
`Error: Undefined variable.` at `border: 1px solid $body-color;`.

Traced to a temp SCSS bundle
(`.quarto/quarto-session-temp*/*.scss`, ~90-line file, `body div.quarto-axe-report { ... border: 1px solid $body-color; }`)
— Quarto's own built-in axe-report stylesheet (injected whenever `axe:` is
set for an `$html-files`-tagged format, per
`schema/document-a11y.yml`), which references `$body-color`/`$link-color`.
Confirmed these ARE defined in the project's `css/casa-slides.scss` theme
(line 13), but the generated bundle's "user-defined SCSS" annotation
sections were all empty — this axe-report CSS compiles as an isolated
"extras" SASS bundle (`resolveExtras` → `resolveSassBundles` in the stack
trace) that never inherits the deck theme's variables. Works for the `html`
website format only because Bootstrap's own SCSS defaults `$body-color`
regardless of theme; RevealJS has no such Bootstrap variable layer.

Tested all three `axe.output` values (`document`, `console`) — same crash
regardless of output mode, since the report stylesheet is attached
unconditionally whenever the `axe:` key exists under `revealjs`, not
gated by output mode. This rules out an output-mode workaround.

**Resolution:** reverted `_quarto.yml` — `axe:` stays commented out under
`format.revealjs`, with a comment explaining the Quarto 1.8.27 limitation.
Verified clean render of `lectures/1.2-Computers_in_Urban_Studies.qmd`
(exit 0) with `axe:` removed. Recommended the user keep using the axe
browser DevTools extension directly against rendered/previewed slide HTML
for RevealJS decks (works fine, operates on live DOM, no Quarto SCSS
involvement) — `axe: output: document` remains fine and unaffected for the
`html` website format.

- [LEARN:accessibility] Quarto 1.8.27's `axe:` YAML option is broken for
  `format.revealjs` (all `output` modes) due to an isolated SASS "extras"
  bundle referencing undefined Bootstrap variables — do not re-enable it
  under `revealjs:` without first checking Quarto's release notes/changelog
  for a fix in a newer version.

## Resolution: fixed upstream by Quarto 1.10.18 (2026-09-16)

User updated Quarto from 1.8.27 to 1.10.18. Re-tested and the crash is gone.

Confirmed via `quarto.js` source diff between versions: the axe format
handler (`axeFormatDependencies`) now detects `isRevealjsOutput(...)` and
sets `sassDependency = isRevealjs ? "reveal-theme" : "bootstrap"` (was
hardcoded to `"bootstrap"` in 1.8.27, which doesn't exist for revealjs —
this was the exact root cause diagnosed earlier). It also replaced the raw
`$body-color`/`$link-color` SCSS variables in the report rules with CSS
custom properties (`var(--r-main-color, #222)`, `var(--r-background-color,
#fff)`), which need no SCSS variable resolution at all — a second
independent fix for the same failure mode.

Tested both `output: console` and `output: document` under
`format.revealjs` in `_quarto.yml` — both render cleanly now (was crashing
on all three modes before). Re-enabled `axe: output: document` under
`revealjs:` (matches the richer visual-report mode already used for
`html`), with a comment noting the fix and Quarto version. Reverted an
incidental `output: document` → `output: console` edit I'd made on the
`html` format block during testing — that was the user's own prior
deliberate setting, unrelated to this bug, restored to what it was
(`console`).

- [LEARN:accessibility] Quarto's axe support for revealjs was broken through
  at least 1.8.27 and fixed by 1.10.18 — if this resurfaces on a future
  Quarto downgrade or in a different project, check the installed version
  first before re-diagnosing from scratch.

## Follow-up: 404 for fonts/source-sans-pro/source-sans-pro.css (2026-09-16)

User saw a `/lectures/fonts/source-sans-pro/source-sans-pro.css (404)` in the
Quarto preview console on multiple lecture pages, right after enabling axe
on revealjs. Traced via source inspection (no live browser tool was
available in-session to confirm the Network-tab initiator directly):

- Reveal.js's base `quarto.scss` unconditionally imports a fallback font:
  `@import url(./fonts/source-sans-pro/source-sans-pro.css);` — never
  actually used since the project's `css/casa-slides.scss` overrides all
  font-family variables (Cousine/Hanken Grotesk via Google Fonts).
- Confirmed via curl against a locally-run preview (port 4321, killed after)
  that the correct path
  (`/site_libs/revealjs/dist/theme/fonts/source-sans-pro/source-sans-pro.css`)
  returns 200, while the exact reported path returns 404 — both on-disk and
  through the dev server, ruling out a stale/missing file or a preview-server
  proxy quirk.
- `axe.min.js` creates a synthetic `<style>@import "<stylesheet-url>"</style>`
  element per page stylesheet to work around CORS-restricted `cssRules`
  access (needed for its color-contrast checks). A *nested* `@import` inside
  a stylesheet loaded this way (rather than via a normal `<link>`) can lose
  its correct base-URL context in some browser engines, resolving relative
  to the page URL instead of the fetched stylesheet's URL — matching the
  `/lectures/fonts/...` pattern exactly.
- Conclusion: harmless axe-core side effect hitting an unused legacy font
  import baked into Quarto's shipped revealjs theme. Not fixable from
  project `_quarto.yml`/theme SCSS (the `@import` lives in Quarto's own
  `revealjs/quarto.scss`) and does not affect actual page rendering or the
  validity of axe's other findings.

**Process note:** started a competing `quarto preview` (port 4321) to test
this, which triggered Quarto's "Terminating existing preview server"
behavior and likely killed the user's own preview on port 4200 — flagged
immediately, user was fine with it and explicitly authorized running a
second instance for debugging. Killed the test instance when done.

- [LEARN:workflow] Never start a second `quarto preview` process without
  checking whether one is already running for the project first — Quarto
  enforces a single-preview-per-project lock and will silently terminate an
  existing instance. Ask before spawning one, even for debugging.
