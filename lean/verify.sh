#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
lake env lean ForeggerTwo.lean 2>&1 | tee lean-check.log
python3 audit_log.py
