import runpy
import shutil
from pathlib import Path

# Same data-include + freeze check as the site render (safe to run twice).
runpy.run_path(str(Path(__file__).resolve().parent / "pre.py"), run_name="__main__")
rootdir = Path("_answers").resolve()
#print(f"Removing {rootdir}")
#shutil.rmtree(rootdir)
print("~" * 50)
msg = """Rendering the practicals..."""
# > quarto render --profile pracs --to ipynb,pdf
print(msg)
print("~" * 50)
exit()
