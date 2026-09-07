# Verification scope

This repository contains three different forms of evidence: a written proof, finite exact computations, and a Lean formalization in dimension two. Their scopes should be kept explicit.

## Written argument

The candidate manuscript claims the eventual permanent inequality for every dimension, with equality exactly at uniform block-permutation matrices and a quadratic stability consequence. The local and global arguments were reviewed by separate AI agents within the same assistant session. No mathematical gap was identified in those reviews. This is not external specialist review or a proof-assistant check of the complete argument.

The analytic audit checks the tangent/leakage split, permanent derivatives, the fixed-power mixing-defect derivative, the ordered noncommuting recurrence, every radius constraint, and boundary cases. The global audit checks the cyclic decomposition and the varying-matrix limit used in the compactness argument. The closest historical results and limits of the priority search are recorded in PRIORITY.md.

## Original exact diagnostics

The supplied package has 90 deterministic fixtures in dimensions two through seven. It compares:

- Subset-DP permanents with C++ Ryser inclusion–exclusion.
- Dual-number binary power derivatives with a sequential differential recurrence.
- Mean-subtraction tangent projections with blockwise matrix projections.
- Truncated permanent-polynomial coefficients with explicit complementary cofactors.
- Categorical count dynamic programming with recursive assignments.

The comparison comprises 1,080 records and 4,500 numeric fields. Of those fields, 2,520 are mathematical output values; 1,080 are record identifiers and 900 are exponents. This is not 4,500 independent mathematical tests.

The recorded checks include 450 power derivatives, 90 tangent Hessians, 90 occupancy identities, and 450 specified powers. The 21 radius-controlled fixtures supply 42 quantitative local-gap checks. Their radius tests use exact squared Frobenius norms and rational comparisons, without floating-point square roots. The remaining 69 fixtures are finite diagnostics and need not lie inside the conservative local radius.

Both the unchanged supplied package and the hardened working copies regenerated two fixture files and seven result files byte for byte. The original 17-guard report remains unchanged; 15 additional hardening regressions exercise the repaired validation separately.

## Fresh independent diagnostics

The independent directory was developed separately from the supplied implementation. It has 35 unit tests, checked under ordinary Python and Python optimization. Its deterministic report covers:

- All exceptional matrices in dimensions two, three, and four: 3, 10, and 47 respectively.
- 240 fixed-power derivatives, 60 tangent Hessians, and 300 occupancy/power records.
- Eight additional local fixtures, eight local derivatives, and 16 quantitative local-gap tests.
- 23 fixtures in which the averaging projection and perturbed matrix do not commute.
- 36 exact rational samples of the sharp dimension-two stability inequality.

Its rational report is compared with independent/reference/diagnostics.json. These computations probe the argument and detect implementation mistakes; they do not establish the infinite quantifiers in the manuscript.

## Lean

The standalone project pins Lean, mathlib, and transitive package revisions. It proves statements about every real matrix of type Matrix (Fin 2) (Fin 2) ℝ satisfying entrywise nonnegativity and both stochasticity conditions. Matrix powers use ordinary multiplication and the permanent is mathlib's Matrix.permanent.

The checked statements are:

1. The permanent of every positive integer power is at most the original permanent.
2. For every exponent at least two, the gap is at least $3/8$ times squared Frobenius distance to the three exceptional matrices.
3. No larger stability coefficient works for all such matrices and exponents at least two.
4. For each exponent at least two, equality holds exactly at the three exceptional matrices.

The source contains no sorry placeholders, custom axioms, or native_decide. The four main declarations depend on the standard Lean foundations propext, Classical.choice, and Quot.sound. The verifier recompiles the source and checks its axiom reports; the committed log is supporting evidence rather than a substitute for rerunning Lean.

The general occupancy argument, arbitrary-dimensional local estimate, Markov decomposition, compactness step, and full conjecture are not Lean-verified.

## Reproducibility and limits

The exact workflow runs on Ubuntu 24.04 with Python 3.10 and 3.13, GCC, and Boost. It checks integrity, reproduces the supplied finite suite with hardened sources, runs added regressions, and compares the independent report. The Lean workflow uses the pinned project and checks its dependency manifest after fetching dependencies. Both upload logs and reports.

The original archive's embedded 25-file manifest is verified directly in the ZIP. The working manifest is regenerated only after intended repository changes using scripts/update_manifest.py. These are integrity checks, not signatures or evidence of research priority.
