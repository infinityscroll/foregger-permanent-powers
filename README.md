# Foregger's permanent-of-powers conjecture: candidate proof

This repository publishes an **unreviewed candidate proof** of the uniform-exponent conjecture attributed to Foregger in Minc's 1978 catalogue, together with exact diagnostics, reproducibility workflows, and a Lean proof of the complete dimension-two case.

The manuscript claims that for every dimension $n$ there is an integer $N(n)\ge2$ such that

$$
\operatorname{per}(A^k)\le\operatorname{per}(A)
\qquad(A\text{ doubly stochastic},\ k\ge N(n)).
$$

Powers are ordinary matrix powers. Equality is claimed precisely for uniform block-permutation matrices: a common partition of row and column labels, with each row class sent uniformly to a class of the same size. The manuscript also claims a uniform quadratic stability bound. Its global exponent and stability constant are not explicit; the cutoff $16n^2$ is proved only inside stated local neighborhoods.

Start with the [manuscript PDF](proof.pdf) or [LaTeX source](proof.tex). Separate AI agents within the same assistant session reviewed the local and global arguments without identifying a mathematical gap. **There has been no external specialist review, and priority is not certified.** The arbitrary-dimension theorem has not been formalized in Lean. See the [historical review](docs/PRIORITY.md) and [verification scope](docs/VERIFICATION.md).

## What is verified

| Evidence | Scope |
| --- | --- |
| Written mathematical argument | All dimensions, including the local estimate, global compactness argument, equality, and stability; remains a candidate proof |
| Original exact diagnostics | 90 fixtures in dimensions 2–7; Python and C++ reproduce all nine reference files |
| Fresh independent diagnostics | Separate standard-library implementation, including all exceptional matrices through dimension four and additional local/noncommuting cases |
| Lean kernel checks | Every real doubly stochastic $2\times2$ matrix; power inequality, equality characterization, and optimal stability coefficient $3/8$ |

The original comparison covers 1,080 records and 4,500 numeric fields: **2,520 mathematical values plus 1,980 identifiers and exponents**. Finite checks do not prove the arbitrary-dimension theorem.

The Lean result makes the dimension-two constants explicit:

$$
N(2)=2,\qquad
\operatorname{per}(A)-\operatorname{per}(A^k)
\ge\frac38\,\operatorname{dist}_F(A,\mathcal F_2)^2
\quad(k\ge2).
$$

The coefficient $3/8$ is optimal for this range of exponents. Here $\mathcal F_2$ consists of the two permutation matrices and the uniform matrix. No novelty is claimed for these dimension-two calculations. See the [elementary derivation](docs/DIMENSION_TWO.md) and [Lean source and reproduction instructions](lean/README.md).

## Reproduce

The exact suite needs Python 3.10+, a C++17 compiler, and Boost headers. On Ubuntu:

    sudo apt-get update
    sudo apt-get install -y g++ libboost-dev
    python3 scripts/verify_original_archive.py
    bash verify.sh

For retained outputs and the additional tests:

    python3 verify_package.py
    bash reproduce.sh build/reproduced
    python3 tests/hardening_regressions.py --cpp build/reproduced/build/audit_cpp --output build/hardening_regressions.json
    python3 -m unittest discover -s independent -v
    python3 -O -m unittest discover -s independent -v
    python3 independent/verify.py --output build/independent.json
    diff -u independent/reference/diagnostics.json build/independent.json

The reproduction output directory must be absent or empty. Lean has separate pinned dependencies; follow [lean/README.md](lean/README.md). GitHub Actions runs the exact suite on Python 3.10 and 3.13 and runs the dimension-two Lean verification separately.

## Provenance and changes

The [original supplied archive](archive/original-package.zip), its [manifest](archive/original-manifest.json), and the [separately supplied README](archive/supplied-readme.md) are preserved. The original archive verifier checks its 25 manifest entries without extracting it.

The working copies repair malformed-input handling in C++ and require complete, unique local-power records. Both the original and hardened suites reproduced the same nine reference files during this review. The repairs change validation, not the diagnostic arithmetic or mathematical results. See [hardening details](docs/HARDENING.md) and [recorded evidence](docs/evidence/).

Additional review material:

- [Local analytic audit](docs/LOCAL_AUDIT.md) and [global argument audit](docs/GLOBAL_AUDIT.md).
- [Original code audit](docs/ORIGINAL_CODE_AUDIT.md).
- [Historical sources and access limits](docs/PRIORITY.md).
- [Fresh independent diagnostics](independent/README.md).

The supplied PDF and its source remain the original manuscript; the additions and corrections to verification scope are documented here. Hash manifests establish file integrity, not authorship, mathematical truth, peer review, or first discovery.
