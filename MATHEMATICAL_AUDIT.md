# Adversarial audit of the proposed proof

Date: 7 September 2026. This is a same-session audit, not an external referee report.

## Quantifiers and target

The theorem covers **all real nonnegative doubly stochastic n by n matrices**, with a common threshold depending only on n and valid for every later integer exponent. It is not a statement with a threshold chosen separately for each A. Ordinary powers, not entrywise powers, are used. The explicit local exponent 16 n^2 is **not asserted to be a global threshold**. The proof does not imply monotonicity between successive powers.

## Points checked for possible proof failure

1. **Nonuniform Markov convergence.** No uniform convergence over A is used. For a convergent sequence A_j -> A_* and diverging k_j, a fixed-time contraction estimate is used first; the fixed time tends to infinity only after the j-limit. This order is crucial.

2. **Periodicity.** The limiting projection averages the cyclic classes, not entire periodic irreducible components. No divisibility of k_j by the component periods is required. The local argument uses F^r, not an incorrect assumption that F^r=E. Fixtures include nontrivial class cycles and late exponents r+1.

3. **Relabelling.** The exceptional set uses a common partition of row and column indices and a size-preserving permutation of that partition. Arbitrary separate row and column relabellings are not substituted into a matrix-power assertion.

4. **Commutation.** E commutes with F, but it need not commute with the perturbed matrix A. The fast-part recurrence keeps the noncommuting terms explicitly: D_k = R A^(k-1) + T D_(k-1).

5. **Boundary perturbations.** The residual Z has norm at most 4 delta, not merely O(epsilon). This distinction makes the errors proportional to epsilon*delta. A bound of O(epsilon^2) alone would not suffice when leakage is much smaller than internal perturbation.

6. **Uniformity for arbitrarily large k.** Only a fixed power r is Taylor-expanded. Its mixing defect grows by at least r delta. Euclidean contraction then makes that defect nondecreasing for every later power. There is no unjustified k*epsilon-small assumption.

7. **Starting permanent.** The exact first derivative is -p delta; the tangent quadratic coefficient is p*m/[2(m-1)] times the squared block norm. Both sign and factor were independently checked. Blocks of size one have no tangent directions.

8. **Row averaging.** The occupancy identity is derived with the factor product(m! / m^m). The categorical trials are independent across columns; their expected count vector is m because row sums also equal one. Reversing the variance probability bound would invalidate the proof; the direction used is V <= 2n^2 P(failure).

9. **Taylor constants and domain.** The chosen radius guarantees F+Y is nonnegative, hence all interpolation segments lie in the doubly stochastic polytope. Hessian and power-derivative bounds are then uniform on those segments. The explicit radius meets every displayed auxiliary inequality.

10. **Global equality case.** Equality of the limiting lower bound forces every square cyclic transition block to be uniform, using the unique-equality part of the classical van der Waerden theorem. Merely using the lower bound without its equality characterization would leave a gap.

11. **Global quadratic stability.** Its compactness contradiction uses a vanishing ratio to squared distance, not an unjustified minimum over infinitely many powers. Distances are bounded on the compact polytope. The local estimate then supplies a fixed positive ratio.

12. **Independent calculations versus proof.** Two exact programs agree on 4,500 rational fields for 90 fixtures. These finite checks do not verify the universal theorem or produce a numerical global N(n). The analytic proof is the certificate for the infinite statement.

## Software audit correction

The initial output comparator used zip and a subsequent read to check file length. That could miss one extra trailing row in one ordering. It was replaced by zip_longest, and explicit one-extra-row and one-missing-row mutations are rejected in both input orders. Compiler misleading-indentation warnings were eliminated; the C++ program compiles with -Wall -Wextra -Werror.

The hostile test suite rejects 17 distinct deliberately malformed inputs/output mutations, including invalid class permutations, an interchange of unequal class sizes, invalid convex parameters, non-bijective point maps, coefficient changes, bad field counts, zero denominators, and truncated files. This is not a proof of absence of all implementation bugs.

## Finite coverage

The base family contains 69 fixtures from integer partitions in dimensions 2 through 7 with specified class permutations and deterministic convex mixtures of point permutations. It is not an exhaustive matrix census. Another 21 fixtures are placed inside the explicit local radius, in pure-tangent, pure-leakage, and combined modes; their two tested late powers give 42 exact local-gap checks. Constants are additionally checked at 446 parameter settings. See src/fixtures.json and outputs/ for exact scope.

## Verdict and unresolved review items

No mathematical gap was found in the checks above. The manuscript proves the stated theorem provided its deductions and classical imports are correct; it is not based on a numerical conjecture. Independent specialist review, proof-assistant formalization, an explicit global threshold, and comprehensive publication-priority certification remain undone. None is claimed to have occurred.

## Attributed negative calibration of a stronger statement

The package separately recomputes Joseph Van Name's 8 May 2022 example with per(A)=1/8 and per(A^2)=9/64, using direct permutation summation and Ryser inclusion–exclusion. The example is credited and is not presented as new. This demonstrates why neither a universal exponent two nor monotonicity at every consecutive time may be substituted for the actual theorem.
