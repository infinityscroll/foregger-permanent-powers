"""Validate the compiler's reported axiom dependencies of the four main results."""

from pathlib import Path
import re

THEOREMS = (
    "permanent_pow_le",
    "sharp_stability",
    "stability_constant_optimal",
    "permanent_pow_eq_iff",
)
EXPECTED = {"propext", "Classical.choice", "Quot.sound"}
root = Path(__file__).resolve().parent
text = (root / "lean-check.log").read_text(encoding="utf-8")
for theorem in THEOREMS:
    name = f"ForeggerTwo.{theorem}"
    matches = re.findall(
        rf"'{re.escape(name)}' depends on axioms: \[([^\]]*)\]", text
    )
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one axiom report for {name}")
    found = {item.strip() for item in matches[0].split(",") if item.strip()}
    if found != EXPECTED:
        raise SystemExit(f"Unexpected axiom dependencies for {name}: {sorted(found)}")
if "error:" in text or "sorryAx" in text:
    raise SystemExit("Compiler errors or an unproved placeholder appeared in the log")
print("PASS: all four theorems use only propext, Classical.choice, and Quot.sound")
