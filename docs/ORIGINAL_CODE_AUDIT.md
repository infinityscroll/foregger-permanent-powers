# Audit of the original reproducibility code

Scope: original src/audit_local.py, src/audit_cpp.cpp, and the directly relevant Python generator, comparison, and hostile-test code. The original package was read without editing its source. This audit does not claim absence of every implementation defect.

## Summary

The core arithmetic diagnostics are mathematically sound on correctly generated fixtures. I found no circular computation of the permanent, the power derivative, the tangent quadratic coefficient, or the occupancy probability. The local-radius and local-gap comparisons use exact rational arithmetic without a square root.

I found two concrete guard defects, plus a closely related truncated-input issue. They concern robustness and coverage accounting; they do not invalidate the analytical proof or the mathematical results computed on the supplied valid fixtures. The published working copies are now hardened; see [repairs and regression results](HARDENING.md). The original archive remains preserved.

## Local-radius and local-gap arithmetic

The function norm2 is the sum of squared matrix entries. Thus the local audit's comparison

    eps2 <= rho * rho

is exactly equivalent to the Frobenius-radius condition, since rho is positive. All operands are Fraction values. It then computes the claimed lower bound directly as

    4*p*delta + p*eps2/8

and compares this with pa-pk using exact rational arithmetic. It also checks vk >= r*delta and the correct strictness/equality distinction according to whether eps2 is positive.

The constants routine encodes the manuscript's smallness assumptions correctly, including the mixing-remainder constraint 16*n*r*r*rho <= r. Its 446 constant checks are finite diagnostics: integer partitions through dimension 12 and two selected permanent values for each dimension 13–100. The all-dimension implication comes from the analytical proof, not this finite sample.

The local audit consumes the already generated permanent/power outputs; it is not a third independently implemented permanent calculator. In the reproduction pipeline, Python and C++ are compared before those outputs are passed to the local checker. This is a valid division of responsibility when described accurately.

## Independent mathematical calculations in C++

- The permanent uses Ryser inclusion–exclusion, whereas the main Python route uses subset dynamic programming. Empty complementary minors correctly have permanent one.
- The tangent projection uses blockwise multiplication by I-J on both sides, whereas Python subtracts row and column means.
- The tangent quadratic coefficient is computed by explicit complementary cofactors over unordered row pairs and ordered distinct columns, giving the correct factor of one half relative to the fully ordered Hessian sum.
- The power differential uses D_r=D_{r-1}F+F^{r-1}X, retaining the correct noncommutative order. Python uses dual-number binary exponentiation.
- The categorical occupancy probability uses recursive assignments subject to class capacities. The recursion's terminal value one is valid: after n assignments, nonnegative counts bounded by capacities whose total is n must equal every capacity. Python uses count-state dynamic programming.
- Late powers are computed by exact integer matrix multiplication and a common denominator. Unreduced rational outputs are normalized exactly by the comparator. The mixing defect uses class row sums, which equal those of EA^k without explicitly multiplying by E.

The basic derivative/projection tests use X=B-F, where B is the fixture's permutation mixture. The late-power tests instead use the interpolated matrix A. This is mathematically legitimate, because the derivative identities apply to every feasible direction B-F. It does mean that changing only the interpolation parameters does not produce a new derivative direction. Counts of fixtures are counts of test records, not a claim that every invariant input is distinct.

## Defect 1: duplicate rows can conceal missing local coverage

The original local audit only requires

    len(rows) == 2 * len(selected)

after accepting late-power records. It does not reject repeated (fixture ID, exponent) keys or require coverage of each selected fixture.

Concrete reproduction: take the original valid record for case 69 and exponent 64, repeat it 42 times, and pass that file with the original fixture file to audit_local.run. The function succeeds and reports 21 radius-controlled fixtures and 42 local-gap checks even though only the key (69,64) occurs. This behavior was reproduced during review. The published hardening regressions now reject that duplicate-row case.

Recommended fix: validate unique selected fixture IDs, reject duplicate accepted keys, and require exactly the intended key set

    {(id, 16*n*n), (id, 16*n*n+1) for each selected fixture}.

Add regressions for a repeated valid row replacing another row, a missing fixture, a missing exponent, and an unexpected late exponent. The supplied reference outputs contain the expected records; this defect is not evidence that the original valid run skipped them.

## Defect 2: unsafe class-permutation indexing

The original C++ loop validates the sorted permutation one entry at a time, then immediately indexes sz[pi[h]]. For sizes=[1,2] and pi=[100,0], at h=0 the sorted entry is zero and passes the first check, but the next expression reads sz[100] before the invalid permutation is rejected.

A minimal reproduction copying this validation order produced a heap-buffer-overflow under AddressSanitizer during review. The published regression suite exercises malformed class permutations against the repaired full parser, including under sanitizers.

Recommended fix: complete the range and permutation checks for every class image before any indexing by pi; only then check preservation of class sizes. The regression should require a controlled diagnostic exit, not merely an arbitrary nonzero exit.

Closely related: the original declarations int total and int id,n,s are not initialized, and failed header extraction is not checked immediately. Empty or truncated input can therefore cause indeterminate integers to be read before the later stream-state check. Initialize header variables and check extraction before using dimensions or allocating dependent vectors.

The original hostile suite treats any nonzero C++ return code as rejection. Consequently a crash can be recorded as a passing guard test. A stronger guard regression should distinguish normal validation failure from a signal or sanitizer failure.

## Counting the compared fields accurately

The original comparator counts every numeric field, including identifiers and exponents, as a rational field. Its reported 4,500 fields across 1,080 records consist of:

| Category | Count |
| --- | ---: |
| Mathematical output values | 2,520 |
| Fixture identifiers | 1,080 |
| Derivative or power exponents | 900 |
| Total numeric fields | 4,500 |

Thus “4,500 numeric fields, including identifiers and exponents” is accurate. “4,500 independent mathematical checks” would overstate the evidence. The 2,520 output-value count is 90 times (6 basic values + 5 derivative values + 2 occupancy values + 15 power values).

## Source consistency

The packaged proof.pdf is byte-identical to the separately supplied Foregger PDF. Both have SHA-256:

    5e5ef1a982a72e5319e1ed73d15b53e0acfbcd52d04aa6fca4bdd993a2f6daed

The inspected proof.tex local statements agree with the extracted manuscript. The scope distinction in its diagnostics section is correct: 69 default fixtures need not satisfy the local radius, while only the 21 designated radius-controlled fixtures are used for the explicit quantitative local-gap audit.
