#!/usr/bin/env python3
"""Fresh exact finite diagnostics for the candidate Foregger permanent proof.

Python 3.10+, standard library only. These checks are independent additions to
the supplied package, not a formal proof of the all-dimension theorem.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path
import sys
from typing import Any, Iterable


class VerificationError(ValueError):
    """A supplied input or mathematical diagnostic is invalid."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


Matrix = tuple[tuple[Q, ...], ...]
Partition = tuple[tuple[int, ...], ...]


def rational(value: Any) -> Q:
    require(type(value) in (int, str, Q), "entries must be integers or exact rational strings")
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationError(f"invalid rational: {value!r}") from error


def matrix(rows: Iterable[Iterable[Any]], *, allow_empty: bool = False) -> Matrix:
    require(type(rows) in (tuple, list), "matrix must be an array of rows")
    require(all(type(row) in (tuple, list) for row in rows), "matrix rows must be arrays")
    result = tuple(tuple(rational(value) for value in row) for row in rows)
    require(bool(result) or allow_empty, "empty matrix")
    require(all(len(row) == len(result) for row in result), "matrix must be square")
    return result


def stochastic(A: Matrix) -> None:
    n = len(A)
    require(n > 0 and all(len(row) == n for row in A), "matrix must be nonempty and square")
    require(all(type(x) is Q for row in A for x in row), "matrix entries must be Fraction values")
    require(all(x >= 0 for row in A for x in row), "negative entry")
    require(all(sum(row) == 1 for row in A), "row sum differs from one")
    require(all(sum(A[i][j] for i in range(n)) == 1 for j in range(n)),
            "column sum differs from one")


def zero(n: int) -> Matrix:
    return tuple(tuple(Q(0) for _ in range(n)) for _ in range(n))


def identity(n: int) -> Matrix:
    return tuple(tuple(Q(i == j) for j in range(n)) for i in range(n))


def uniform(n: int) -> Matrix:
    return tuple(tuple(Q(1, n) for _ in range(n)) for _ in range(n))


def add(A: Matrix, B: Matrix) -> Matrix:
    require(len(A) == len(B), "matrix dimensions differ")
    return tuple(tuple(x + y for x, y in zip(a, b)) for a, b in zip(A, B))


def scale(c: Q, A: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in A)


def subtract(A: Matrix, B: Matrix) -> Matrix:
    return add(A, scale(Q(-1), B))


def multiply(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    require(n == len(B), "matrix dimensions differ")
    return tuple(tuple(sum((A[i][h] * B[h][j] for h in range(n)), Q(0))
                       for j in range(n)) for i in range(n))


def transpose(A: Matrix) -> Matrix:
    return tuple(zip(*A))


def power(A: Matrix, k: int) -> Matrix:
    require(type(k) is int and k >= 0, "power must be a nonnegative integer")
    result, base = identity(len(A)), A
    while k:
        if k & 1:
            result = multiply(result, base)
        k //= 2
        if k:
            base = multiply(base, base)
    return result


def inner(A: Matrix, B: Matrix) -> Q:
    return sum((x * y for a, b in zip(A, B) for x, y in zip(a, b)), Q(0))


def norm_squared(A: Matrix) -> Q:
    return inner(A, A)


def l1(A: Matrix) -> Q:
    return sum((abs(x) for row in A for x in row), Q(0))


def permanent_dp(A: Matrix) -> Q:
    """Subset dynamic programming, assigning rows in order."""
    n = len(A)
    dp = [Q(0)] * (1 << n)
    dp[0] = Q(1)
    for mask in range(1 << n):
        i = mask.bit_count()
        if i == n:
            continue
        for j in range(n):
            if not (mask >> j) & 1:
                dp[mask | (1 << j)] += dp[mask] * A[i][j]
    return dp[-1]


def permanent_permutations(A: Matrix) -> Q:
    result = Q(0)
    for sigma in permutations(range(len(A))):
        term = Q(1)
        for i, j in enumerate(sigma):
            term *= A[i][j]
        result += term
    return result


def permanent_ryser(A: Matrix) -> Q:
    """Ryser inclusion-exclusion with direct row sums, no subset-DP dependency."""
    n = len(A)
    result = Q(0)
    for mask in range(1 << n):
        term = Q((-1) ** (n - mask.bit_count()))
        for row in A:
            term *= sum((row[j] for j in range(n) if (mask >> j) & 1), Q(0))
        result += term
    return result


def checked_permanent(A: Matrix) -> Q:
    values = (permanent_dp(A), permanent_permutations(A), permanent_ryser(A))
    require(len(set(values)) == 1, "permanent algorithms disagree")
    return values[0]


def minor(A: Matrix, omitted_rows: set[int], omitted_columns: set[int]) -> Matrix:
    return tuple(tuple(value for j, value in enumerate(row) if j not in omitted_columns)
                 for i, row in enumerate(A) if i not in omitted_rows)


def permanent_derivative(A: Matrix, X: Matrix) -> Q:
    return sum((X[i][j] * permanent_ryser(minor(A, {i}, {j}))
                for i in range(len(A)) for j in range(len(A))), Q(0))


def permanent_hessian(A: Matrix, Y: Matrix) -> Q:
    n = len(A)
    return sum((2 * Y[i][a] * Y[j][b] * permanent_ryser(minor(A, {i, j}, {a, b}))
                for i, j in combinations(range(n), 2)
                for a in range(n) for b in range(n) if a != b), Q(0))


def permanent_coefficients(A: Matrix, Y: Matrix) -> tuple[Q, Q, Q]:
    """Coefficients through t² from explicit expansion of permutation products."""
    totals = [Q(0), Q(0), Q(0)]
    for sigma in permutations(range(len(A))):
        coefficients = [Q(1), Q(0), Q(0)]
        for i, j in enumerate(sigma):
            c0, c1, c2 = coefficients
            coefficients = [c0 * A[i][j], c1 * A[i][j] + c0 * Y[i][j],
                            c2 * A[i][j] + c1 * Y[i][j]]
        totals = [x + y for x, y in zip(totals, coefficients)]
    return tuple(totals)


def power_derivative_binary(A: Matrix, X: Matrix, k: int) -> tuple[Matrix, Matrix]:
    require(type(k) is int and k >= 0, "power must be a nonnegative integer")
    def dual_mul(left, right):
        B, D = left
        C, H = right
        return multiply(B, C), add(multiply(D, C), multiply(B, H))
    result = (identity(len(A)), zero(len(A)))
    base = (A, X)
    while k:
        if k & 1:
            result = dual_mul(result, base)
        k //= 2
        if k:
            base = dual_mul(base, base)
    return result


def power_derivative_sequential(A: Matrix, X: Matrix, k: int) -> tuple[Matrix, Matrix]:
    require(type(k) is int and k >= 0, "power must be a nonnegative integer")
    P, D = identity(len(A)), zero(len(A))
    for _ in range(k):
        D = add(multiply(D, A), multiply(P, X))
        P = multiply(P, A)
    return P, D


def validate_partition(n: int, classes: Partition, pi: tuple[int, ...]) -> None:
    require(type(n) is int and n >= 1, "dimension must be positive")
    require(type(classes) in (list, tuple) and bool(classes), "partition must be nonempty")
    require(all(type(C) in (list, tuple) and C for C in classes), "partition has an empty or invalid class")
    flattened = [i for C in classes for i in C]
    require(all(type(i) is int for i in flattened), "partition labels must be integers")
    require(sorted(flattened) == list(range(n)), "classes must partition the common state labels")
    require(type(pi) in (list, tuple) and all(type(i) is int for i in pi),
            "class permutation must be an integer array")
    require(sorted(pi) == list(range(len(classes))), "invalid class permutation")
    require(all(len(classes[a]) == len(classes[pi[a]]) for a in range(len(classes))),
            "class permutation must preserve sizes")


def exceptional(n: int, classes: Partition, pi: tuple[int, ...]) -> tuple[Matrix, Matrix, Q]:
    validate_partition(n, classes, pi)
    F, E = [list(row) for row in zero(n)], [list(row) for row in zero(n)]
    p = Q(1)
    for a, C in enumerate(classes):
        m = len(C)
        p *= Q(factorial(m), m ** m)
        for i in C:
            for j in C:
                E[i][j] = Q(1, m)
            for j in classes[pi[a]]:
                F[i][j] = Q(1, m)
    return matrix(F), matrix(E), p


def partitions(n: int) -> Iterable[Partition]:
    """Each set partition once, in canonical smallest-label order."""
    if n == 0:
        yield ()
        return
    for part in partitions(n - 1):
        for index in range(len(part)):
            yield part[:index] + (part[index] + (n - 1,),) + part[index + 1:]
        yield part + ((n - 1,),)


def exceptional_parameters(n: int) -> Iterable[tuple[Partition, tuple[int, ...]]]:
    for classes in partitions(n):
        for pi in permutations(range(len(classes))):
            if all(len(classes[a]) == len(classes[pi[a]]) for a in range(len(classes))):
                yield classes, pi


def tangent_projection(X: Matrix, classes: Partition, pi: tuple[int, ...]) -> Matrix:
    n = len(X)
    validate_partition(n, classes, pi)
    Y = [list(row) for row in zero(n)]
    for a, C in enumerate(classes):
        D, m = classes[pi[a]], len(C)
        rows = {i: sum(X[i][j] for j in D) for i in C}
        columns = {j: sum(X[i][j] for i in C) for j in D}
        total = sum(rows.values())
        for i in C:
            for j in D:
                Y[i][j] = X[i][j] - rows[i] / m - columns[j] / m + total / (m * m)
    return matrix(Y)


def tangent_projection_products(X: Matrix, F: Matrix, E: Matrix) -> Matrix:
    supported = tuple(tuple(x if f else Q(0) for x, f in zip(row, allowed))
                      for row, allowed in zip(X, F))
    Qproj = subtract(identity(len(X)), E)
    return multiply(multiply(Qproj, supported), Qproj)


def class_sums(M: Matrix, classes: Partition) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(sum((M[i][j] for i in C), Q(0)) for j in range(len(M))) for C in classes)


def defect(M: Matrix, classes: Partition) -> Q:
    return len(M) - sum((x * x for row in class_sums(M, classes) for x in row), Q(0))


def occupancy_dp(M: Matrix, classes: Partition) -> dict[tuple[int, ...], Q]:
    y = class_sums(M, classes)
    distribution = {tuple(0 for _ in classes): Q(1)}
    for j in range(len(M)):
        next_distribution = defaultdict(Q)
        for counts, probability in distribution.items():
            for a in range(len(classes)):
                updated = list(counts)
                updated[a] += 1
                next_distribution[tuple(updated)] += probability * y[a][j]
        distribution = dict(next_distribution)
    return {counts: probability for counts, probability in distribution.items() if probability}


def occupancy_assignments(M: Matrix, classes: Partition) -> dict[tuple[int, ...], Q]:
    y = class_sums(M, classes)
    distribution = defaultdict(Q)
    for assignment in product(range(len(classes)), repeat=len(M)):
        counts = [0] * len(classes)
        probability = Q(1)
        for j, a in enumerate(assignment):
            counts[a] += 1
            probability *= y[a][j]
        distribution[tuple(counts)] += probability
    return {counts: probability for counts, probability in distribution.items() if probability}


def validate_occupancy(M: Matrix, E: Matrix, classes: Partition, p: Q) -> dict[str, Q]:
    stochastic(M)
    require(multiply(E, M) == M, "occupancy matrix is not row-averaged")
    dp, direct = occupancy_dp(M, classes), occupancy_assignments(M, classes)
    require(dp == direct, "occupancy algorithms disagree")
    require(sum(dp.values()) == 1, "occupancy probabilities do not sum to one")
    target = tuple(map(len, classes))
    balanced_probability = dp.get(target, Q(0))
    variance = sum((probability * sum((c - m) ** 2 for c, m in zip(counts, target))
                    for counts, probability in dp.items()), Q(0))
    value, V = checked_permanent(M), defect(M, classes)
    require(value == p * balanced_probability, "occupancy permanent identity failed")
    require(V == variance, "occupancy defect variance identity failed")
    require(value <= p * (1 - V / (2 * len(M) ** 2)) <= p,
            "categorical occupancy bound failed")
    return {"permanent": value, "balanced_probability": balanced_probability, "defect": V}


def derivative_of_defect(F: Matrix, X: Matrix, classes: Partition, r: int) -> Q:
    P, D = power_derivative_binary(F, X, r)
    require((P, D) == power_derivative_sequential(F, X, r),
            "matrix-power derivative algorithms disagree")
    U_P, U_D = class_sums(P, classes), class_sums(D, classes)
    return -2 * sum((x * y for a, b in zip(U_P, U_D) for x, y in zip(a, b)), Q(0))


def fixture_target(n: int) -> Matrix:
    shift = tuple(tuple(Q(j == (i + 1) % n) for j in range(n)) for i in range(n))
    return add(add(scale(Q(1, 2), identity(n)), scale(Q(1, 3), shift)), scale(Q(1, 6), uniform(n)))


def audit_fixture(n: int, classes: Partition, pi: tuple[int, ...], eta: Q = Q(1, 4)) -> dict:
    require(Q(0) < eta <= 1, "fixture mixing weight outside (0,1]")
    F, E, p = exceptional(n, classes, pi)
    stochastic(F)
    require(multiply(E, E) == E == transpose(E), "averaging projection identity failed")
    require(multiply(E, F) == F == multiply(F, E), "exceptional map/projection identity failed")
    require(checked_permanent(F) == p == checked_permanent(E), "exceptional permanent formula failed")
    A = add(scale(1 - eta, F), scale(eta, fixture_target(n)))
    stochastic(A)
    X = subtract(A, F)
    Y = tangent_projection(X, classes, pi)
    Z = subtract(X, Y)
    require(Y == tangent_projection_products(X, F, E), "tangent projection algorithms disagree")
    require(multiply(E, Y) == zero(n) == multiply(Y, E), "tangent averaging does not vanish")
    require(inner(Y, Z) == 0, "tangent and leakage components not orthogonal")
    eps2, tangent2, remainder2 = norm_squared(X), norm_squared(Y), norm_squared(Z)
    delta = sum((A[i][j] for i in range(n) for j in range(n) if not F[i][j]), Q(0))
    require(eps2 == tangent2 + remainder2, "Pythagorean projection identity failed")
    require(0 <= delta and delta * delta <= n * n * eps2, "leakage Cauchy bound failed")
    require(remainder2 <= l1(Z) ** 2 and l1(Z) <= 4 * delta, "leakage remainder bound failed")
    require(permanent_derivative(F, X) == -p * delta, "permanent leakage derivative failed")
    require(permanent_derivative(F, Y) == 0, "tangent permanent derivative failed")
    coefficients = permanent_coefficients(F, Y)
    predicted_quadratic = p * sum((Q(len(C), 2 * (len(C) - 1)) *
                                  sum((Y[i][j] ** 2 for i in C for j in classes[pi[a]]), Q(0))
                                  for a, C in enumerate(classes) if len(C) > 1), Q(0))
    require(coefficients == (p, Q(0), predicted_quadratic), "tangent Taylor coefficient failed")
    require(permanent_hessian(F, Y) == 2 * predicted_quadratic, "cofactor tangent Hessian failed")
    derivative_checks = []
    for r in (1, 2, 3, 5):
        value = derivative_of_defect(F, X, classes, r)
        require(value == 2 * r * delta, "fixed-power defect derivative failed")
        require(defect(power(add(F, Y), r), classes) == 0, "pure tangent defect did not vanish")
        derivative_checks.append({"r": r, "derivative": value})
    powers, previous_defect = [], Q(0)
    Cbound = Q(n * n * factorial(n - 2), 2)
    Qproj = subtract(identity(n), E)
    for k in (1, 2, 3, 4, 5):
        Fk = power(F, k)
        pik = tuple(range(len(classes)))
        for _ in range(k):
            pik = tuple(pi[a] for a in pik)
        expected_Fk, _, _ = exceptional(n, classes, pik)
        require(Fk == expected_Fk and checked_permanent(Fk) == p, "exceptional power identity failed")
        Ak = power(A, k)
        M = multiply(E, Ak)
        occupancy = validate_occupancy(M, E, classes, p)
        V = occupancy["defect"]
        require(V >= previous_defect, "mixing defect decreased")
        previous_defect = V
        D = multiply(Qproj, Ak)
        require(permanent_derivative(M, D) == 0, "row-averaged first derivative does not vanish")
        value = checked_permanent(Ak)
        require(value <= occupancy["permanent"] + Cbound * norm_squared(D),
                "row-averaged permanent Hessian bound failed")
        if k >= 2:
            R = multiply(multiply(Qproj, A), E)
            T = multiply(multiply(Qproj, A), Qproj)
            recurrence = add(multiply(R, power(A, k - 1)), multiply(T, multiply(Qproj, power(A, k - 1))))
            require(D == recurrence, "noncommuting recurrence failed")
        powers.append({"k": k, "permanent": value, **{f"occupancy_{key}": val for key, val in occupancy.items()}})
    return {"n": n, "classes": classes, "pi": pi, "eta": eta, "p": p,
            "epsilon_squared": eps2, "delta": delta, "tangent_squared": tangent2,
            "leakage_component_squared": remainder2, "tangent_quadratic_coefficient": predicted_quadratic,
            "noncommutes_with_E": multiply(E, A) != multiply(A, E),
            "derivative_checks": derivative_checks, "powers": powers}


def audit_local(n: int, classes: Partition, pi: tuple[int, ...], *, eta: Q | None = None,
                explicit_matrix: Matrix | None = None) -> dict:
    F, E, p = exceptional(n, classes, pi)
    r, Cbound = 16 * n * n, Q(n * n * factorial(n - 2), 2)
    rho = min(Q(1, 16 * n * r), p / (128 * Cbound * n))
    if explicit_matrix is None:
        if eta is None:
            eta = rho / (2 * n)
        require(Q(0) < eta <= 1, "invalid local fixture mixing weight")
        A = add(scale(1 - eta, F), scale(eta, fixture_target(n)))
    else:
        require(eta is None, "do not combine an explicit local matrix with a mixing weight")
        A = explicit_matrix
    stochastic(A)
    X = subtract(A, F)
    eps2 = norm_squared(X)
    require(eps2 <= rho * rho, "fixture is outside the explicit local radius")
    delta = sum((A[i][j] for i in range(n) for j in range(n) if not F[i][j]), Q(0))
    Y = tangent_projection(X, classes, pi)
    Z = subtract(X, Y)
    require(l1(Z) <= 4 * delta, "local leakage bound failed")
    require(derivative_of_defect(F, X, classes, r) == 2 * r * delta, "local fixed-time derivative failed")
    value = checked_permanent(A)
    require(value >= p - 3 * p * delta + p * eps2 / 4, "starting-matrix lower bound failed")
    lower_gap = 4 * p * delta + p * eps2 / 8
    records = []
    previous_V = Q(0)
    for k in (r, r + 1):
        Ak = power(A, k)
        M = multiply(E, Ak)
        D = subtract(Ak, M)
        V = defect(M, classes)
        require(V >= r * delta and V >= previous_V, "late-power mixing lower bound failed")
        previous_V = V
        value_k = checked_permanent(Ak)
        averaged = checked_permanent(M)
        require(averaged <= p * (1 - V / (2 * n * n)), "late occupancy bound failed")
        require(permanent_derivative(M, D) == 0, "late averaged derivative does not vanish")
        require(value_k <= averaged + Cbound * norm_squared(D), "late Hessian error bound failed")
        # Exact relaxation of (8 delta + epsilon^k)^2 using 2(a²+b²).
        require(norm_squared(D) <= 128 * delta * delta + 2 * eps2 ** k,
                "squared non-averaged-row suppression bound failed")
        gap = value - value_k
        require(gap >= lower_gap, "explicit local permanent gap failed")
        records.append({"k": k, "gap": gap, "lower_gap": lower_gap,
                        "defect": V, "nonaveraged_norm_squared": norm_squared(D)})
    return {"n": n, "classes": classes, "pi": pi, "radius": rho, "eta": eta,
            "explicit_matrix": A if explicit_matrix is not None else None,
            "epsilon_squared": eps2, "delta": delta, "p": p, "late_powers": records}


def stress_matrix() -> Matrix:
    """A period-two exception with noncommuting leakage and unequal tangent blocks."""
    F, E, _ = exceptional(4, ((0, 1), (2, 3)), (1, 0))
    P = matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    tangent = matrix([[0, 0, 1, -1], [0, 0, -1, 1],
                      [2, -2, 0, 0], [-2, 2, 0, 0]])
    weight = Q(1, 2 ** 20)
    A = add(add(scale(1 - weight, F), scale(weight, P)), scale(weight, tangent))
    stochastic(A)
    require(multiply(E, A) != multiply(A, E), "stress fixture unexpectedly commutes with E")
    require(multiply(F, A) != multiply(A, F), "stress fixture unexpectedly commutes with F")
    return A


def dimension_two_stability() -> dict:
    # For A_t = ((1+t)/2,(1-t)/2;...), dist(A_t,{I,swap,J})²
    # equals min(t²,(1-|t|)²). Test the written sharp constant independently.
    records = []
    for t in (Q(-1), Q(-3, 4), Q(-1, 2), Q(-1, 4), Q(0),
              Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
        A = matrix([[(1 + t) / 2, (1 - t) / 2], [(1 - t) / 2, (1 + t) / 2]])
        exceptional_matrices = [exceptional(2, classes, pi)[0]
                                for classes, pi in exceptional_parameters(2)]
        distance_squared = min(norm_squared(subtract(A, F)) for F in exceptional_matrices)
        require(distance_squared == min(t * t, (1 - abs(t)) ** 2), "two-dimensional distance formula failed")
        for k in (2, 3, 5, 8):
            Ak = power(A, k)
            predicted = matrix([[(1 + t ** k) / 2, (1 - t ** k) / 2],
                                [(1 - t ** k) / 2, (1 + t ** k) / 2]])
            require(Ak == predicted, "two-dimensional exact power formula failed")
            gap = checked_permanent(A) - checked_permanent(Ak)
            require(gap == (t * t - t ** (2 * k)) / 2, "two-dimensional permanent gap formula failed")
            require(gap >= Q(3, 8) * distance_squared, "two-dimensional quadratic stability check failed")
            records.append({"t": t, "k": k, "gap": gap, "distance_squared": distance_squared})
    sharp = [record for record in records if record["t"] == Q(1, 2) and record["k"] == 2][0]
    require(sharp["gap"] == Q(3, 8) * sharp["distance_squared"] > 0,
            "two-dimensional sharpness calibration failed")
    return {"scope": "Finite exact calibrations of the separate two-dimensional theorem; these samples are not its proof.",
            "stability_constant": Q(3, 8), "sharpness_t": Q(1, 2), "sharpness_k": 2, "records": records}


COUNTEREXAMPLE_SOURCE = "https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix"


def known_counterexample() -> dict:
    # Joseph Van Name, answer dated 8 May 2022 to MathOverflow question 422029.
    # The matrix and values were checked against the original answer.
    A = scale(Q(1, 2), matrix([[1, 0, 1, 0], [0, 0, 1, 1], [1, 1, 0, 0], [0, 1, 0, 1]]))
    stochastic(A)
    before, after = checked_permanent(A), checked_permanent(power(A, 2))
    require((before, after) == (Q(1, 8), Q(9, 64)), "attributed k=2 calibration failed")
    return {"attribution": "Joseph Van Name, MathOverflow answer, 8 May 2022",
            "source": COUNTEREXAMPLE_SOURCE, "matrix": A,
            "permanent": before, "permanent_of_square": after, "increase": after - before}


def all_diagnostics() -> dict:
    fixtures = []
    counts = {}
    for n in (2, 3, 4):
        parameters = list(exceptional_parameters(n))
        matrices = {exceptional(n, classes, pi)[0] for classes, pi in parameters}
        require(len(matrices) == len(parameters), "exceptional family enumeration contains duplicates")
        counts[str(n)] = len(parameters)
        fixtures.extend(audit_fixture(n, classes, pi) for classes, pi in parameters)
    local_parameters = [
        (2, ((0,), (1,)), (1, 0)),
        (2, ((0, 1),), (0,)),
        (3, ((0, 1), (2,)), (0, 1)),
        (3, ((0, 1, 2),), (0,)),
        (4, ((0, 1), (2, 3)), (1, 0)),
        (4, ((0, 1), (2,), (3,)), (0, 2, 1)),
        (4, ((0, 1, 2, 3),), (0,)),
    ]
    local = [audit_local(*parameters) for parameters in local_parameters]
    local.append(audit_local(4, ((0, 1), (2, 3)), (1, 0), explicit_matrix=stress_matrix()))
    return {
        "scope": "Fresh finite rational diagnostics; not a universal formal proof or recovery of the original package.",
        "summary": {"dimensions": [2, 3, 4], "exceptional_matrices_by_dimension": counts,
                    "general_fixtures": len(fixtures), "power_derivatives": 4 * len(fixtures),
                    "tangent_hessians": len(fixtures), "occupancy_identities": 5 * len(fixtures),
                    "ordinary_power_records": 5 * len(fixtures),
                    "noncommuting_projection_fixtures": sum(f["noncommutes_with_E"] for f in fixtures),
                    "radius_controlled_fixtures": len(local), "local_fixed_power_derivatives": len(local),
                    "late_power_gap_checks": 2 * len(local), "dimension_two_stability_samples": 36},
        "known_k2_counterexample": known_counterexample(), "fixtures": fixtures, "local_fixtures": local,
        "dimension_two_stability": dimension_two_stability(),
    }


def jsonable(value: Any) -> Any:
    if type(value) is Q:
        return f"{value.numerator}/{value.denominator}"
    if type(value) is dict:
        return {key: jsonable(item) for key, item in value.items()}
    if type(value) in (tuple, list):
        return [jsonable(item) for item in value]
    return value


def serialize_report(report: dict) -> str:
    # Only locally generated exact values are serialized. Late-power fractions
    # exceed Python 3.11+'s default decimal conversion limit; restore that limit
    # immediately after this serialization operation.
    old_limit = sys.get_int_max_str_digits() if hasattr(sys, "get_int_max_str_digits") else None
    try:
        if old_limit is not None:
            sys.set_int_max_str_digits(0)
        return json.dumps(jsonable(report), indent=2, sort_keys=True) + "\n"
    finally:
        if old_limit is not None:
            sys.set_int_max_str_digits(old_limit)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = all_diagnostics()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialize_report(report), encoding="utf-8")
        print(json.dumps(report["summary"], indent=2, sort_keys=True))
        print(f"Exact report written to {args.output}")
        return 0
    except (VerificationError, OSError) as error:
        parser.exit(1, f"verification failed: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
