#!/usr/bin/env python3
"""Verify the preserved ZIP's embedded manifest without extracting any files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def safe_name(name: str) -> None:
    path = PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and ".." not in path.parts
            and "\\" not in name, "Unsafe archive/manifest path: " + name)


def stream_digest(stream) -> str:
    result = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        result.update(chunk)
    return result.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    archive = root / "archive" / "original-package.zip"
    sidecar = root / "archive" / "original-manifest.json"
    prefix = "foregger_1978_reproducibility/"
    with zipfile.ZipFile(archive) as package:
        entries = package.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)), "Duplicate ZIP entry")
        for entry in entries:
            safe_name(entry.filename)
            require(not stat.S_ISLNK(entry.external_attr >> 16),
                    "Symbolic link in ZIP: " + entry.filename)
        embedded = package.read(prefix + "manifest.json")
        require(embedded == sidecar.read_bytes(),
                "Embedded manifest differs from preserved sidecar")
        manifest = json.loads(embedded)
        require(manifest.get("algorithm") == "sha256"
                and isinstance(manifest.get("files"), dict),
                "Unsupported original manifest")
        files = manifest["files"]
        require(len(files) == 25, "Unexpected original manifest file count")
        expected_names = {prefix + "manifest.json"}
        for name, expected in files.items():
            safe_name(name)
            require(isinstance(expected, str)
                    and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                    "Malformed digest: " + name)
            member = prefix + name
            expected_names.add(member)
            with package.open(member) as stream:
                require(stream_digest(stream) == expected,
                        "Original file digest mismatch: " + name)
        actual_names = {entry.filename for entry in entries if not entry.is_dir()}
        require(actual_names == expected_names,
                "Unexpected or missing files in original archive")
    with archive.open("rb") as stream:
        archive_digest = stream_digest(stream)
    print(json.dumps({
        "original_manifest_files_verified": len(files),
        "embedded_manifest_matches_sidecar": True,
        "archive_sha256": archive_digest,
        "scope": "integrity only; not a signature or mathematical proof",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
