#!/usr/bin/env python3
"""
Extract highlights and margin notes from annotated PDFs as Markdown.

Usage:
    python scripts/extract_annotations.py PATH [PATH ...] [-o OUT.md]

PATH can be a PDF or a directory (all PDFs in it are processed, not
recursively). PDFs without annotations are listed so that you can see
what was skipped.

Requires PyMuPDF (`pip install pymupdf`). It is not part of the SDS
container's default stack, so a local venv is the easiest option:

    python3 -m venv .venv && .venv/bin/pip install pymupdf
    .venv/bin/python scripts/extract_annotations.py "path/to/Week 2"
"""
import argparse
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    sys.exit("PyMuPDF is not installed: run `pip install pymupdf` (see the docstring for a venv recipe).")

# Annotation types that mark up existing text (so we can recover what was marked)
MARKUP = {"Highlight", "Underline", "StrikeOut", "Squiggly"}
# Annotation types that carry only a note
NOTES = {"Text", "FreeText"}


def marked_text(page, annot):
    """Return the words covered by a markup annotation, in reading order."""
    verts = annot.vertices or []
    rects = [pymupdf.Quad(verts[i:i + 4]).rect for i in range(0, len(verts), 4)]
    words = page.get_text("words")  # (x0, y0, x1, y1, word, block, line, word_no)
    hits = []
    for w in words:
        # Use the word's centre point so that neighbouring lines aren't picked up
        cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
        if any(r.contains(pymupdf.Point(cx, cy)) for r in rects):
            hits.append(w)
    hits.sort(key=lambda w: (w[5], w[6], w[7]))
    text = ""
    for i, w in enumerate(hits):
        text += w[4]
        # Rejoin words hyphenated at a line break ("intel- lectual" -> "intellectual")
        line_break = i + 1 < len(hits) and hits[i + 1][5:7] != w[5:7]
        if not (w[4].endswith("-") and line_break):
            text += " "
        else:
            text = text[:-1]
    return text.strip()


def indent(note):
    """Keep multi-line notes inside their Markdown list item."""
    return note.replace("\n", "\n      ")


def extract(pdf):
    """Return a list of Markdown lines for one PDF (empty if no annotations)."""
    lines = []
    with pymupdf.open(pdf) as doc:
        for page in doc:
            for annot in page.annots() or []:
                kind = annot.type[1]
                note = (annot.info.get("content") or "").strip()
                if kind in MARKUP:
                    text = marked_text(page, annot)
                    if text:
                        lines.append(f"- **p{page.number + 1}** > {text}")
                        if note:
                            lines.append(f"    - *Note:* {indent(note)}")
                    elif note:
                        lines.append(f"- **p{page.number + 1}** *Note:* {indent(note)}")
                elif kind in NOTES and note:
                    lines.append(f"- **p{page.number + 1}** *Note:* {indent(note)}")
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("-o", "--out", type=Path, help="write Markdown here instead of stdout")
    args = parser.parse_args()

    pdfs = []
    for p in args.paths:
        pdfs.extend(sorted(p.glob("*.pdf")) if p.is_dir() else [p])

    out, empty = [], []
    for pdf in pdfs:
        lines = extract(pdf)
        if lines:
            out += [f"## {pdf.stem}", ""] + lines + [""]
        else:
            empty.append(pdf.name)
    if empty:
        out += ["## No annotations", ""] + [f"- {e}" for e in empty] + [""]

    text = "\n".join(out)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
