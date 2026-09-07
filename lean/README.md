# Lean verification in dimension two

`ForeggerTwo.lean` proves four statements for **every real doubly stochastic
2-by-2 matrix**. This is a symbolic proof, not a finite enumeration. The matrix
type is `Matrix (Fin 2) (Fin 2) ℝ`; double stochasticity means entrywise
nonnegativity, every row sum one, and every column sum one. Powers use ordinary
matrix multiplication, and the permanent is mathlib's `Matrix.permanent`.

Let `F₂` consist of the identity matrix, the transposition matrix, and the matrix
whose four entries equal one half. Let `d(M,F₂)²` be the minimum squared
Frobenius distance to these three matrices. The checked theorems are:

1. `permanent_pow_le`: `per(M^k) ≤ per(M)` for every natural number `k ≥ 1`.
2. `sharp_stability`: `per(M) - per(M^k) ≥ (3/8) d(M,F₂)²` for every `k ≥ 2`.
3. `stability_constant_optimal`: any coefficient valid for all such matrices
   and every `k ≥ 2` is at most `3/8`.
4. `permanent_pow_eq_iff`: for each `k ≥ 2`, equality holds precisely when
   `M ∈ F₂`.

The proof first derives the representation
`M = [[(1+t)/2, (1-t)/2], [(1-t)/2, (1+t)/2]]`, where `-1 ≤ t ≤ 1`.
It proves the family multiplication law and permanent formula, then reduces
the assertions to polynomial and power inequalities. Squared Frobenius
distance is explicitly defined as the sum of the four squared entry
differences. The optimality witness has `t = 1/2` and `k = 2`.

## Exact scope

This is **partial formal verification** of the supplied Foregger project.
It proves the complete dimension-two statements above. It does not formalize
arbitrary matrix dimensions, the occupancy bound, the local quantitative gap
near general block-permutation matrices, the periodic Markov decomposition,
the compactness argument, or the claimed uniform eventual theorem for every
dimension. The candidate proof of the old conjecture therefore remains a
written argument requiring independent review. No novelty claim for the
dimension-two formalization or its mathematical ingredients is made here.

The file contains no `sorry`, custom axiom declarations, or `native_decide`.
All four main theorem dependency reports contain exactly Lean's standard
`propext`, `Classical.choice`, and `Quot.sound`. The proofs are checked by
Lean's kernel using these standard foundations; they are not axiom-free.

## Reproduce

The project pins Lean `v4.33.0-rc2`, mathlib commit
`51e6992efd06126df61a496bebf8f49482a4e129`, and the transitive dependency
revisions in `lake-manifest.json`. With `elan`, Git, and Python 3.9 or newer,
run from this directory:

```sh
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update
python3 cache_imports.py
bash verify.sh
```

The cache helper reads the direct imports from `ForeggerTwo.lean` and fetches
their compiled dependencies. `verify.sh` recompiles the complete file,
regenerates `lean-check.log`, fails on compilation errors, and checks all four
axiom reports. A committed log alone is not a substitute for running Lean.
The source and standalone project were checked on 8 September 2026 against
the pinned toolchain using existing local dependency checkouts and caches.
