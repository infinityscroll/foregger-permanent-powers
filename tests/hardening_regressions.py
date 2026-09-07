#!/usr/bin/env python3
"""Regression checks for parser bounds and exact local-power record coverage.

The original 17-guard report remains unchanged; these additional regressions have
their own output. A C++ crash does not count as a successfully rejected input.
"""
from copy import deepcopy
import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from audit_local import run as audit_local
from hostile_tests import fixture_text


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(cpp, fixtures, values):
    cases = json.loads(fixtures.read_text(encoding="utf-8"))
    base = deepcopy(next(c for c in cases if c["sizes"] == [1, 2]))
    outcomes = []
    with TemporaryDirectory(prefix="foregger-hardening-") as temp:
        directory = Path(temp)
        cpp_cases = []
        for name, pi in [("positive out-of-range class image", [100, 0]),
                         ("negative class image", [-1, 0])]:
            case = deepcopy(base)
            case["pi"] = pi
            cpp_cases.append((name, fixture_text(case)))
        cpp_cases.extend([
            ("empty fixture file", ""),
            ("nonnumeric count header", "invalid\n"),
            ("truncated fixture header", "1\n3 4"),
            ("truncated partition", "1\n0 3 2\n1"),
            ("truncated class permutation", "1\n0 3 2\n1 2\n0"),
            ("truncated rational parameters", "1\n0 3 2\n1 2\n0 1\n1 2"),
            ("truncated mixture length", "1\n0 3 2\n1 2\n0 1\n1 2 1 2\n"),
            ("truncated point permutation", "1\n0 3 2\n1 2\n0 1\n1 2 1 2\n1\n1 0"),
            ("oversized partition entry", "1\n0 3 2\n2147483647 2147483647\n0 1\n"),
        ])
        for name, text in cpp_cases:
            input_path, output_path = directory / "fixture.txt", directory / "output.tsv"
            input_path.write_text(text, encoding="utf-8")
            process = subprocess.run([str(cpp), str(input_path), str(output_path)],
                                     capture_output=True, text=True, timeout=10)
            require(process.returncode == 1, f"{name}: expected normal failure exit 1, got {process.returncode}")
            require(process.stderr.startswith("AUDIT FAILED:"), f"{name}: missing validation diagnostic")
            require("Sanitizer" not in process.stderr, f"{name}: sanitizer detected memory misuse")
            outcomes.append({"test": name, "normal_validation_exit": 1})

        lines = values.read_text(encoding="utf-8").splitlines(keepends=True)
        selected = {c["id"]: c for c in cases if c.get("local_radius_case")}
        late_indices = [index for index, line in enumerate(lines)
                        if (fields := line.rstrip("\n").split("\t"))[1] == "power"
                        and int(fields[0]) in selected
                        and int(fields[2]) >= 16 * selected[int(fields[0])]["n"] ** 2]
        first_index = late_indices[0]
        first = lines[first_index]
        duplicate = first * len(late_indices)
        missing = "".join(lines[:first_index] + lines[first_index + 1:])
        wrong_exponent_fields = first.rstrip("\n").split("\t")
        wrong_exponent_fields[2] = str(int(wrong_exponent_fields[2]) + 2)
        unexpected = "".join(lines[:first_index] + ["\t".join(wrong_exponent_fields) + "\n"] + lines[first_index + 1:])
        for name, text in [("duplicated records replacing all required local powers", duplicate),
                           ("missing local power", missing),
                           ("unexpected local exponent", unexpected)]:
            invalid_values = directory / "invalid-values.tsv"
            invalid_values.write_text(text, encoding="utf-8")
            try:
                audit_local(fixtures, invalid_values)
            except (AssertionError, ValueError):
                outcomes.append({"test": name, "local_audit": "rejected"})
            else:
                raise RuntimeError(f"local audit accepted {name}")

        invalid_fixtures = directory / "invalid-fixtures.json"
        invalid_fixtures.write_text(json.dumps(cases + [cases[-1]]), encoding="utf-8")
        try:
            audit_local(invalid_fixtures, values)
        except (AssertionError, ValueError):
            outcomes.append({"test": "duplicate fixture ID", "local_audit": "rejected"})
        else:
            raise RuntimeError("local audit accepted duplicate fixture IDs")

    valid = audit_local(fixtures, values)
    require(valid["radius_controlled_fixtures"] == 21 and valid["local_gap_checks"] == 42,
            "valid local fixture coverage changed")
    return {"additional_regressions_passed": len(outcomes),
            "valid_local_fixtures": 21, "valid_local_gap_checks": 42,
            "cpp_crashes_do_not_count_as_rejection": True, "tests": outcomes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpp", type=Path, required=True)
    parser.add_argument("--fixtures", type=Path, default=ROOT / "src" / "fixtures.json")
    parser.add_argument("--values", type=Path, default=ROOT / "outputs" / "python_exact.tsv")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.cpp.resolve(), args.fixtures, args.values)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "tests"}, sort_keys=True))


if __name__ == "__main__":
    main()
