#!/usr/bin/env python3
"""Check an attributed 2022 counterexample to the stronger, false k=2 claim.

This example is Joseph Van Name's, not a discovery of this package.
Two elementary exact formulas are implemented locally without importing
any routines from the main audits.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path


def multiply(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Q(0))
             for j in range(n)] for i in range(n)]


def permutation_sum(a: list[list[Q]]) -> Q:
    total = Q(0)
    for permutation in itertools.permutations(range(len(a))):
        term = Q(1)
        for i, j in enumerate(permutation):
            term *= a[i][j]
        total += term
    return total


def ryser(a: list[list[Q]]) -> Q:
    n = len(a)
    total = Q(0)
    for bits in range(1 << n):
        selected = [j for j in range(n) if (bits >> j) & 1]
        term = Q((-1) ** (n - len(selected)))
        for row in a:
            term *= sum((row[j] for j in selected), Q(0))
        total += term
    return total


def check_ds(a: list[list[Q]]) -> None:
    n = len(a)
    if any(len(row) != n for row in a) or any(x < 0 for row in a for x in row):
        raise ValueError('not a nonnegative square matrix')
    if any(sum(row) != 1 for row in a):
        raise ValueError('row sums')
    if any(sum(a[i][j] for i in range(n)) != 1 for j in range(n)):
        raise ValueError('column sums')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    zero_one = [[1, 0, 1, 0], [0, 0, 1, 1], [1, 1, 0, 0], [0, 1, 0, 1]]
    a = [[Q(x, 2) for x in row] for row in zero_one]
    a2 = multiply(a, a)
    check_ds(a)
    check_ds(a2)
    values = [permutation_sum(m) for m in (a, a2)]
    if values != [ryser(m) for m in (a, a2)] or values != [Q(1, 8), Q(9, 64)]:
        raise RuntimeError('the attributed k=2 calibration failed')
    report = {
        'attribution': 'Joseph Van Name, MathOverflow answer, 8 May 2022',
        'source_question': 'https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix',
        'novelty': 'Previously public example; not a discovery in this package.',
        'matrix': [[str(x) for x in row] for row in a],
        'matrix_squared': [[str(x) for x in row] for row in a2],
        'permanent': str(values[0]),
        'permanent_of_square': str(values[1]),
        'increase': str(values[1] - values[0]),
        'routes': ['direct sum over all permutations', 'Ryser inclusion-exclusion'],
        'scope': 'Rules out a universal k=2 and stepwise monotonicity, not the eventual-exponent theorem.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('Attributed k=2 counterexample verified exactly by both formulas.')


if __name__ == '__main__':
    main()
