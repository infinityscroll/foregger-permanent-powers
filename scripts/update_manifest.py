#!/usr/bin/env python3
"""Regenerate the working repository's SHA-256 integrity list.

Run after intended source or deliverable changes. This does not certify
mathematical correctness, authorship, or priority.
"""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path


EXCLUDED_DIRECTORIES = {".git", ".lake", "build", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-date", default=date.today().isoformat())
    args = parser.parse_args()
    date.fromisoformat(args.record_date)
    root = Path(__file__).resolve().parents[1]
    files = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRECTORIES for part in rel.parts):
            continue
        if rel.as_posix() == "manifest.json" or path.name in EXCLUDED_NAMES:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise SystemExit("Refusing to hash a symbolic link: " + rel.as_posix())
        if path.is_file():
            files[rel.as_posix()] = digest(path)
    manifest = {
        "algorithm": "sha256",
        "record_date": args.record_date,
        "files": files,
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"manifest_files": len(files), "algorithm": "sha256"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
