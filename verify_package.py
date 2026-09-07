#!/usr/bin/env python3
"""Verify packaged SHA-256 hashes, not mathematical truth or authorship."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath


def main() -> None:
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / 'manifest.json').read_text())
    if manifest.get('algorithm') != 'sha256' or not isinstance(manifest.get('files'), dict):
        raise SystemExit('Unsupported or malformed manifest')
    for name, expected in manifest['files'].items():
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise SystemExit('Unsafe manifest path: ' + name)
        path = base.joinpath(*rel.parts)
        if not path.is_file() or path.is_symlink():
            raise SystemExit('Missing or nonregular file: ' + name)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            raise SystemExit('SHA-256 mismatch: ' + name)
    print(json.dumps({'manifest_files_verified': len(manifest['files']),
                      'all_hashes_match': True,
                      'scope': 'integrity only; not a signature or mathematical proof'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
