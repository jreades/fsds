"""Pre-render hook: keep the data-download includes in step with _variables.yml.

The code-block includes (practicals/_data_definition*.qmd) can't use
{{< var >}}, so this writes them from `data:` in _variables.yml. It runs
before every render, including single-file renders.

`freeze: auto` only re-executes a document when its *own* source changes, not
an included file. So when the date changes, this also deletes the frozen
results of every document that includes one of these files, forcing them to
re-run. The last date written is kept in _freeze/.data-ymd (gitignored).

Standard library only: the Python that Quarto runs this with may not have
PyYAML.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARS = ROOT / "_variables.yml"
PRACS = ROOT / "practicals"
FREEZE = ROOT / "_freeze"
STAMP = FREEZE / ".data-ymd"
CITY = "London"

# file name -> (label, extension, extra lines)
INCLUDES = {
    "_data_definition_csv.qmd": ("file-location-csv", "csv.gz", []),
    "_data_definition_sp.qmd": ("file-location-geoparquet", "geoparquet", []),
    "_data_definition.qmd": (
        "file-location-parquet",
        "parquet",
        ["file = f'{ymd}-{city}-listings.parquet'"],
    ),
}


def read_data_vars(path: Path) -> dict:
    """Return the scalar keys under the top-level `data:` block."""
    out, inside = {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\S", line):  # a new top-level key
            inside = line.startswith("data:")
            continue
        m = re.match(r'^\s+([\w-]+):\s*"?([^"#]*?)"?\s*(#.*)?$', line)
        if inside and m:
            out[m.group(1)] = m.group(2)
    return out


def include_text(ymd: str, host: str, label: str, ext: str, extra: list) -> str:
    lines = [
        "```{python}",
        f"#| label: {label}",
        f"ymd  = '{ymd}'",
        f"city = '{CITY}'",
        f"host = '{host}'",
        f"url  = f'{{host}}/~jreades/data/{{ymd}}-{{city}}-listings.{ext}'",
        *extra,
        "```",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    data = read_data_vars(VARS)
    ymd = data.get("ymd", "")
    if not re.fullmatch(r"\d{8}", ymd):
        raise SystemExit(f"[pre.py] data.ymd in {VARS.name} isn't YYYYMMDD: {ymd!r}")
    m = re.match(r"(https?://[^/]+)", data.get("url", ""))
    host = m.group(1) if m else "https://orca.casa.ucl.ac.uk"

    for name, (label, ext, extra) in INCLUDES.items():
        p = PRACS / name
        text = include_text(ymd, host, label, ext, extra)
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            p.write_text(text, encoding="utf-8")
            print(f"[pre.py] wrote {p.relative_to(ROOT)} ({ymd})")

    last = STAMP.read_text().strip() if STAMP.exists() else None
    if last == ymd:
        return

    # The date changed (or this is the first run): drop frozen results for
    # every document that includes one of the generated files.
    pattern = re.compile(r"\{\{<\s*include\s+\S*_data_definition")
    for qmd in ROOT.glob("**/*.qmd"):
        if any(part.startswith(("_", ".")) for part in qmd.relative_to(ROOT).parts[:-1]):
            continue  # skip _site, _freeze, _answers, .quarto, ...
        if not pattern.search(qmd.read_text(encoding="utf-8")):
            continue
        frozen = FREEZE / qmd.relative_to(ROOT).with_suffix("")
        if frozen.exists():
            shutil.rmtree(frozen)
            print(f"[pre.py] cleared frozen results: {frozen.relative_to(ROOT)}")

    FREEZE.mkdir(exist_ok=True)
    STAMP.write_text(ymd + "\n")
    print(f"[pre.py] data date {last or '(none)'} -> {ymd}")


if __name__ == "__main__":
    main()
