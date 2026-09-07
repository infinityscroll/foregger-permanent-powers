# Additional exact diagnostics

This Python 3.10+ standard-library implementation was written during review,
separately from the supplied Python/C++ package. It uses `Fraction` arithmetic
throughout. It tests finite rational examples and identities; it is not a formal
proof of the universal Foregger theorem or evidence of publication priority.

From this directory:

```sh
python3 -m unittest discover -v
python3 -O -m unittest discover -v
python3 verify.py --output build/diagnostics.json
diff -u reference/diagnostics.json build/diagnostics.json
```

Both normal and optimized Python passed all **35 unittest tests**. The exact
diagnostics passed for the following deterministic coverage:

| Check | Count |
|---|---:|
| Exceptional matrices, dimension 2 | 3 |
| Exceptional matrices, dimension 3 | 10 |
| Exceptional matrices, dimension 4 | 47 |
| General perturbation fixtures | 60 |
| Fixed-power mixing derivatives | 240 |
| Tangent Hessians | 60 |
| Occupancy identities | 300 |
| Ordinary-power records | 300 |
| Fixtures not commuting with the averaging projection | 23 |
| Fixtures inside the explicit local radius | 8 |
| Additional derivatives at the local cutoff | 8 |
| Late-power local gap checks | 16 |
| Two-dimensional stability samples | 36 |

The 60 exceptional matrices exhaust this family in dimensions 2, 3 and 4, by
enumerating every common set partition and every size-preserving permutation of
its classes. Their perturbations do **not** exhaust doubly stochastic matrices.
Each general fixture is `(3/4)F + (1/4)B`, where
`B = (1/2)I + (1/3)P + (1/6)J` and `P` shifts the state labels cyclically.

Seven local fixtures use the same target with mixing weight `rho_F/(2n)`.
The eighth is a period-two 4×4 exceptional matrix with noncommuting leakage
and different tangent perturbations in its two allowed blocks, with coefficients
`2^-20`. Local checks use both `k=16n²` and `k=16n²+1`; all hypotheses, including
the squared Frobenius-radius bound, are checked exactly. The reported cutoff is
the manuscript's **local** cutoff. These tests do not establish a global cutoff.

## Distinct algorithms

Permanents are compared by subset dynamic programming, explicit permutation
summation, and Ryser inclusion-exclusion. The tangent projection is computed
both by subtracting row and column means and by matrix multiplication with the
orthogonal block projections. The matrix-power derivative uses both dual-number
binary exponentiation and a sequential recurrence. The tangent Hessian uses both
explicit coefficient expansion and cofactor sums. Occupancy probabilities use
both count-state dynamic programming and direct categorical-assignment enumeration.
These implementations share basic exact matrix operations, so they are not
completely independent software systems or external replication.

The ordinary-power tests also check the noncommuting recurrence for the part
outside the averaging projection, the vanishing first derivative at a row-averaged
matrix, the Hessian error bound, and monotonicity of the mixing defect.

The tests compare all three permanent algorithms on every one of the 512 binary
3×3 matrices. Other tests reject malformed matrices, floats, booleans, signed
matrices, incorrect row/column sums, malformed partitions, invalid permutations,
wrong occupancy normalization, and a fixture outside the claimed local radius.
They also explicitly distinguish a period-two exceptional matrix from an
idempotent matrix, and reject the commutative shortcut for a noncommuting
matrix-power derivative.

## Attributed calibration and two-dimensional addition

Joseph Van Name's [8 May 2022 MathOverflow answer](https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix)
supplies the previously known 4×4 matrix with permanent `1/8` and square permanent
`9/64`. The actual matrix in that answer was inspected and is recomputed by all
three formulas here. This is a scope calibration, not a newly found counterexample.

The separate two-dimensional theorem is sampled at nine rational values of `t`
and four exponents for `A_t = ((1+t)/2,(1-t)/2; (1-t)/2,(1+t)/2)`. The script
checks the exact power formula, distance to `{I,swap,J}`, and stability constant
`3/8`. The choice `t=1/2, k=2` attains that positive constant, establishing its
sharpness once the universal two-dimensional inequality is proved. The 36 samples
alone are not that universal proof.

## Reproducibility details

The review machine used Python 3.12.14. The 35 tests took about 0.1 seconds;
the complete additional diagnostic report takes several seconds. All output
fractions are canonical rational strings; some late-power values have thousands
of digits. Serialization temporarily lifts Python's decimal integer conversion
limit for these locally generated values, then restores the process setting.
The saved report is approximately 377 KB and is deterministic.

The original package's 90 fixtures, 4500 compared numeric fields, 42 local gap
checks and 17 guards are separately reproduced by its own two routes. They are
not counts from this additional implementation.
