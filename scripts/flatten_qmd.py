#!/usr/bin/env python3
"""
flatten_qmd.py — inline Quarto {{< include >}} shortcodes into a new .qmd.

Usage:
    python flatten_qmd.py input.qmd [output.qmd | output_dir/]

If output is omitted, writes <input>-flat.qmd next to the input. If output
is an existing directory, writes <output_dir>/<input name>.

During `quarto render` this runs automatically (from scripts/post.py) for
any rendered file whose front matter contains `flatten-qmd: true`: the
flattened copy is written next to its HTML/PDF in the output dir.

Behaviour (mirrors Quarto's own rules):
  * Relative include paths resolve from the directory of the MAIN file,
    even inside nested includes (Quarto treats included content as if it
    had been typed into the main document).
  * Paths starting with "/" resolve from the project root (the nearest
    directory upward containing _quarto.yml/_quarto.yaml; falls back to
    the main file's directory).
  * Nested includes are expanded recursively; include cycles raise an error.
  * Escaped shortcodes ({{{< include ... >}}}) are left untouched.
  * Shortcodes inside fenced code blocks (``` or ~~~) are left untouched.
  * YAML front matter in included files is dropped (Quarto ignores it too),
    except in the main file.
  * The `flatten-qmd` flag is removed from the main file's front matter.
  * Code chunks are NOT executed — the output is still a renderable .qmd.
"""
import re
import sys
from pathlib import Path

FLAG = "flatten-qmd"

INCLUDE_RE = re.compile(
    r'(?<!\{)\{\{<\s*include\s+(?P<path>"[^"]+"|\'[^\']+\'|\S+)\s*>\}\}(?!\})'
)
FENCE_RE = re.compile(r'^(\s*)(`{3,}|~{3,})')
FRONT_MATTER_RE = re.compile(r'^---\s*\n.*?\n(---|\.\.\.)\s*\n', re.S)
FLAG_LINE_RE = re.compile(rf'^{FLAG}\s*:.*\n', re.M)


def find_project_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / "_quarto.yml").exists() or (d / "_quarto.yaml").exists():
            return d
    return start


def strip_front_matter(text: str) -> str:
    m = FRONT_MATTER_RE.match(text)
    return text[m.end():] if m else text


def is_flagged(path: Path) -> bool:
    """True if the file's front matter has a top-level `flatten-qmd: true`."""
    try:
        m = FRONT_MATTER_RE.match(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return False
    return bool(m and re.search(rf'^{FLAG}\s*:\s*true\s*(#.*)?$', m.group(0), re.M))


def drop_flag(text: str) -> str:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return text
    return FLAG_LINE_RE.sub("", m.group(0)) + text[m.end():]


def expand(text, main_dir, root, stack):
    out, fence = [], None  # fence = (char, length) when inside a code block
    for line in text.splitlines(keepends=True):
        m = FENCE_RE.match(line)
        if m:
            tok = m.group(2)
            if fence is None:
                fence = (tok[0], len(tok))
            elif tok[0] == fence[0] and len(tok) >= fence[1] and line.strip() == tok:
                fence = None
            out.append(line)
            continue
        if fence is not None:
            out.append(line)
            continue

        def repl(match):
            raw = match.group("path").strip("\"'")
            p = (root / raw.lstrip("/")) if raw.startswith("/") else (main_dir / raw)
            p = p.resolve()
            if p in stack:
                chain = " -> ".join(str(s) for s in [*stack, p])
                raise RuntimeError(f"Include cycle: {chain}")
            if not p.is_file():
                raise FileNotFoundError(f"Included file not found: {raw} (looked for {p})")
            body = strip_front_matter(p.read_text(encoding="utf-8"))
            body = expand(body, main_dir, root, [*stack, p])
            return body.rstrip("\n")

        out.append(INCLUDE_RE.sub(repl, line))
    return "".join(out)


def flatten(src: Path) -> str:
    src = Path(src).resolve()
    main_dir = src.parent
    root = find_project_root(main_dir)
    return drop_flag(expand(src.read_text(encoding="utf-8"), main_dir, root, [src]))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    if len(sys.argv) > 2:
        dst = Path(sys.argv[2])
        if dst.is_dir():
            dst = dst / src.name
    else:
        dst = src.with_name(src.stem + "-flat.qmd")
    if dst.resolve() == src:
        sys.exit("Refusing to overwrite the input file.")
    dst.write_text(flatten(src), encoding="utf-8")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
