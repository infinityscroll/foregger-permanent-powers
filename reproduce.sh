#!/usr/bin/env bash
# Rebuild and regenerate without overwriting the supplied reference files.
set -euo pipefail
BASE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -ne 1 ]]; then
    printf 'Usage: bash reproduce.sh /path/to/fresh-output\n' >&2
    exit 2
fi
PYTHON="${PYTHON:-python3}"
CXX="${CXX:-g++}"
export PYTHONDONTWRITEBYTECODE=1
"$PYTHON" -c 'import sys; sys.version_info >= (3,10) or sys.exit("Python 3.10+ is required")'
mkdir -p -- "$1"
OUT="$(cd -- "$1" && pwd)"
if [[ -n "$(find "$OUT" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    printf 'Refusing to overwrite nonempty directory: %s\n' "$OUT" >&2
    exit 2
fi
mkdir -p -- "$OUT/src" "$OUT/build" "$OUT/outputs"
printf '[1/6] Regenerating fixtures and running exact Python diagnostics.\n'
"$PYTHON" "$BASE/src/audit_python.py" --generate \
    --fixtures "$OUT/src/fixtures.json" --output "$OUT/outputs/python_exact.tsv" \
    > "$OUT/build/python.log" 2>&1 || { tail -30 "$OUT/build/python.log" >&2; exit 1; }
printf '[2/6] Compiling and running the independent C++ diagnostics.\n'
"$CXX" -O2 -std=c++17 -Wall -Wextra -Werror "$BASE/src/audit_cpp.cpp" \
    -o "$OUT/build/audit_cpp"
"$OUT/build/audit_cpp" "$OUT/src/fixtures.txt" "$OUT/outputs/cpp_exact.tsv" \
    > "$OUT/build/cpp.log" 2>&1 || { tail -30 "$OUT/build/cpp.log" >&2; exit 1; }
printf '[3/6] Comparing every exact rational field.\n'
"$PYTHON" "$BASE/src/compare_outputs.py" "$OUT/outputs/python_exact.tsv" \
    "$OUT/outputs/cpp_exact.tsv" --output "$OUT/outputs/independent_comparison.json"
printf '[4/6] Checking the explicit local gap and malformed-input guards.\n'
"$PYTHON" "$BASE/src/audit_local.py" --fixtures "$OUT/src/fixtures.json" \
    --values "$OUT/outputs/python_exact.tsv" --output "$OUT/outputs/local_gap_audit.json"
"$PYTHON" "$BASE/src/hostile_tests.py" --fixtures "$OUT/src/fixtures.json" \
    --cpp "$OUT/build/audit_cpp" --output "$OUT/outputs/hostile_tests.json"
printf '[5/6] Recomputing the attributed k=2 counterexample.\n'
"$PYTHON" "$BASE/src/calibration.py" --output "$OUT/outputs/known_k2_calibration.json"
printf '[6/6] Comparing regenerated files with the supplied references.\n'
"$PYTHON" - "$BASE" "$OUT" <<'PY'
import hashlib, json, sys
from pathlib import Path
base, out = map(Path, sys.argv[1:])
names = ['src/fixtures.json', 'src/fixtures.txt',
         'outputs/python_exact.tsv', 'outputs/cpp_exact.tsv',
         'outputs/python_exact.summary.json', 'outputs/independent_comparison.json',
         'outputs/local_gap_audit.json', 'outputs/hostile_tests.json',
         'outputs/known_k2_calibration.json']
records = []
for name in names:
    expected, actual = (base / name).read_bytes(), (out / name).read_bytes()
    if expected != actual:
        raise SystemExit('Reference mismatch: ' + name)
    records.append({'path': name, 'sha256': hashlib.sha256(actual).hexdigest(),
                    'bytes': len(actual), 'byte_identical': True})
report = {'files_compared': len(records), 'all_byte_identical': True,
          'finite_diagnostics_not_formal_proof': True, 'files': records}
(out / 'reproduction_comparison.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k != 'files'}, sort_keys=True))
PY
printf 'Reproduction passed. Retained outputs: %s\n' "$OUT"
