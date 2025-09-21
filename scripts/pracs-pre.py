import shutil
from pathlib import Path
rootdir = Path("_answers").resolve()
print(f"Removing {rootdir}")
shutil.rmtree(rootdir)
print("~" * 50)
msg = """Rendering the practicals..."""
# > quarto render --profile pracs practicals
print(msg)
print("~" * 50)
exit()
