#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"${PYTHON:-python3}" "$BASE/verify_package.py"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/foregger-verify.XXXXXXXX")"
trap 'rm -rf -- "$OUT"' EXIT
bash "$BASE/reproduce.sh" "$OUT"
printf 'Integrity and exact diagnostic reproduction passed.\n'
