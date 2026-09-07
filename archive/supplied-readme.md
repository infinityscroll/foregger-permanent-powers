# Foregger's 1978 permanent-of-powers conjecture

**Version:** 1.0, 7 September 2026.  
**Review status:** unreviewed proof; no external peer review or certified publication priority.

## Mathematical result

For every positive integer `n`, there exists an integer `N(n) >= 2` such that

    per(A^k) <= per(A)

for **every** real nonnegative doubly stochastic `n x n` matrix `A` and **every** integer `k >= N(n)`. Powers are ordinary matrix powers. The threshold depends only on the dimension, not on the entries or on a lower bound for nonzero entries.

The manuscript proves the stronger eventual statement, classifies every eventual equality case, and proves a uniform quadratic lower bound on the permanent gap in terms of distance from the exceptional family. The exceptional matrices uniformly map each class of a common row/column partition onto a size-preservingly permuted class. The exact definition and all estimates are in **`proof.pdf`**, with editable LaTeX in **`proof.tex`**.

The global threshold and the global quadratic constant are **nonexplicit**. The explicit cutoff `16*n*n` is local to the displayed neighborhoods; it is **not** claimed to work globally. The assertion does not imply monotonicity at every consecutive time. An attributed, previously public counterexample to the stronger `k=2` assertion is recomputed separately.

## Proof rather than extrapolation

The universal theorem has an analytic proof. Its central estimate is uniform even when the power is arbitrarily large and the initial matrix is arbitrarily close to a reducible or periodic matrix. Finite computations are diagnostics of the proof's identities and scope, not a substitute for that argument.

Two separately written exact implementations use different permanent, derivative, projection, and occupancy algorithms. On 90 fixtures in dimensions 2 through 7, their outputs agree on 4,500 rational fields across 1,080 records. The fixtures include 21 cases inside the explicit local radius. Their 42 late-power checks satisfy the quantitative local inequality. A separate guard suite rejects 17 deliberately corrupted cases. No floating-point calculation is a premise of the proof.

Implementation independence here means separate code paths and algorithms within this session. It does not mean independent institutional replication, proof-assistant verification, or external mathematical review.

## Reproduce

Requirements: Python 3.10 or later (standard library only), a GCC-compatible C++17 compiler, Boost's header-only `rational` and `multiprecision` components, and a POSIX shell. No network access, SageMath, package installation, or external Python modules are required by the checks. The reference platform and versions are recorded in `environment.json`.

From this directory:

```bash
# Check the supplied files against their SHA-256 manifest.
python3 verify_package.py

# Rebuild, rerun, and compare all results in a temporary directory.
bash verify.sh

# Or retain regenerated outputs in a fresh directory of your choosing.
bash reproduce.sh /path/to/fresh-output
```

`reproduce.sh` refuses to overwrite a nonempty output directory. `PYTHON` and `CXX` may be set to suitable executables. Seven mathematical output files and both fixture encodings are compared byte-for-byte with the references. The two main implementations are additionally compared as exact rational numbers, accepting equivalent unreduced fractions. Large integer conversion limits are disabled only in the relevant scripts.

The manifest checks file integrity, **not** authorship, priority, or mathematical correctness. `verify.sh` executes the mathematical diagnostics as well, but is still not a formal proof checker for the universal theorem.

Optional PDF rebuild, requiring a LaTeX installation with the packages listed in `proof.tex`:

```bash
mkdir -p latex-build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=latex-build proof.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=latex-build proof.tex
```

## Contents

- `proof.pdf`, `proof.tex`: full theorem, explicit local estimate, global proof, equality cases, stability, and bibliography.
- `MATHEMATICAL_AUDIT.md`: checks of uniformity, periodicity, noncommutation, boundary perturbations, derivative signs, and implementation scope.
- `sources/prior_art.md`, `sources/query_log.txt`: dated prior-art review, known ingredients, excluded similarly named results, and access limitations.
- `src/`: two principal exact implementations, fixture encodings, comparison, local-gap checks, hostile tests, and the attributed negative calibration.
- `outputs/`: exact reference data and diagnostic reports.
- `reproduce.sh`, `verify.sh`, `verify_package.py`, `manifest.json`, `environment.json`: reproduction and integrity tools.

## Attribution and priority

Foregger's conjecture is attributed through the 1978 Minc catalogue and inspected later primary sources. The closest inspected prior theorem is Melnykova's 2012 result under a fixed positive lower bound on nonzero entries. The van der Waerden–Falikman–Egorychev theorem, its equality characterization, standard Markov-chain convergence, and the other classical ingredients are credited and are not claimed as new.

The dated search found no earlier publication of this uniform theorem or proof. Search coverage is incomplete, some original papers were accessible only through later primary accounts, and private or unindexed concurrent work was not searched. "Apparently unpublished" is therefore qualified, not a guarantee of worldwide novelty. See the source audit for exact limitations.
