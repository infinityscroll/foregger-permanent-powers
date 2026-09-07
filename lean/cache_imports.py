"""Download mathlib's compiled cache for exactly the file's direct imports.

Run after fetching the pinned Lake dependencies. The cache command also fetches
each imported module's transitive prerequisites.
"""

from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
modules = []
for line in (root / "ForeggerTwo.lean").read_text(encoding="utf-8").splitlines():
    if line.startswith("import "):
        modules.extend(line.removeprefix("import ").split())
if not modules:
    raise SystemExit("No Lean imports found")
subprocess.run(["lake", "exe", "cache", "get", *modules], cwd=root, check=True)
