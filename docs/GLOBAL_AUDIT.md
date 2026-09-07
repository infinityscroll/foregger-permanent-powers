# Global argument audit

Reviewed 8 September 2026 against the supplied version 1.0 manuscript dated 7 September 2026. This separate AI-assisted audit checks Sections 1.1, 5 and 6. It takes the row-averaging bound in Lemma 2.1 and the uniform local gap in Theorem 4.3 as provisional inputs. It is not external peer review or formal verification.

**Verdict:** no mathematical flaw was found in the periodic decomposition, varying-matrix limit argument, compactness contradiction, equality classification, or stability deduction, conditional on those inputs.

## Exceptional family

There are finitely many partitions of the common label set `[n]`, and finitely many permutations of each partition's classes. Hence the exceptional set `F_n` is finite. It is nonempty because it contains all permutation matrices. Its definition correctly requires a common partition of row and column labels: arbitrary independent relabelling is inappropriate for a theorem about ordinary powers.

For a class `C_a` of size `m_a`, a uniform transition to the equal-sized class `C_pi(a)` composes with another such transition to give the same uniform distribution on `C_pi^2(a)`. Thus every positive power is again a uniform block-permutation matrix for the same partition. The permanent is always

`p(F) = product_a m_a! / m_a^(m_a) > 0`.

No idempotence of `F` is required. Cycles of classes, including cycles of singleton classes, are correctly included.

## Lemma 5.1(i): the fixed-matrix comparison

For a doubly stochastic matrix, a sink strongly connected component has no outgoing mass. Its rows therefore send total mass equal to its number of vertices to its own columns. Since those columns have exactly that same total capacity, there is no incoming mass either. Removing this component leaves another doubly stochastic matrix. Iteration gives a simultaneous block-diagonal decomposition into irreducible matrices; there are no transient states.

Within an irreducible component, the standard cyclic decomposition has transitions from each class only to its successor. Every such transition block has row sums one and column sums one. Summing its entries in the two ways proves that consecutive classes have equal sizes. Therefore all transition blocks are square doubly stochastic matrices.

The `d`-step restrictions to the cyclic classes are irreducible and aperiodic. Their stationary distributions are uniform. Taking `L` to be a common multiple of the component periods yields `A_*^(Lt) -> E`, where `E` averages within every cyclic class. This is an orthogonal projection.

The support forces every nonzero permanent term to match each row class with its unique succeeding column class. The permanent therefore factors over the transition blocks, even when the component is periodic. Applying the classical van der Waerden bound to each block gives `per(A_*) >= per(E)`. Equality in a product of these positive lower bounds requires equality in every block, hence every transition block is uniform. This gives exactly `A_* in F_n`; conversely matrices in that family do attain equality.

The bound and its unique equality case are existing ingredients, stated together in [Gurvits, Introduction](https://arxiv.org/html/0711.3496v2), which credits Falikman and Egorychev. Neither is a new result of the candidate.

## Lemma 5.1(ii): varying matrices and unbounded powers

Let `A_j -> A_*`, `k_j -> infinity`, and `A_j^k_j -> B`. Fix a positive integer `t`. Eventually `k_j >= Lt`, so

`(I-E) A_j^k_j = ((I-E) A_j^(Lt)) A_j^(k_j-Lt)`.

Every doubly stochastic matrix is a Euclidean contraction, and so is every power. Submultiplicativity gives

`||(I-E) A_j^k_j||_2 <= ||(I-E) A_j^(Lt)||_2`.

At this point `t` is fixed. Ordinary polynomial continuity of the fixed power gives, after taking `j -> infinity`,

`||(I-E) B||_2 <= ||(I-E) A_*^(Lt)||_2`.

Now take `t -> infinity`. The right-hand side tends to zero, so `EB=B`. Closure of the Birkhoff polytope ensures that `B` is doubly stochastic. Lemma 2.1 then gives `per(B) <= per(E)`.

This order of limits is valid. The argument does not require a spectral gap uniform in `j`, stable supports, stable periods, divisibility of `k_j` by `L`, or uniform convergence of `A_j^k`. These are precisely the assumptions that would have made a naive compactness argument invalid.

## Global threshold and equality

Failure of an eventual threshold with strict inequality outside `F_n` supplies arbitrarily large integers `k_j` and matrices `A_j notin F_n` satisfying `per(A_j^k_j) >= per(A_j)`. Compactness applies to pairs `(A_j,A_j^k_j)` because both matrices belong to the same finite-dimensional compact Birkhoff polytope. Passing to a convergent subsequence and using the previous lemma gives

`per(A_*) <= per(B) <= per(E) <= per(A_*)`.

Consequently `A_*=F` is exceptional. The local theorem is applicable eventually since its radius at this fixed `F` is positive and `k_j -> infinity`. Its gap is strictly positive for `A_j != F`, contradicting the chosen sequence. The hypothesis `A_j notin F_n` guarantees `A_j != F`.

This proves an exponent threshold depending only on the fixed dimension, and proves that every exponent beyond that threshold has precisely the claimed equality family. It does **not** calculate the threshold. The explicit `16n^2` remains a local threshold only.

## Quadratic stability

Negating the joint existence of `c_n>0` and `N_n` correctly permits choosing `c=1/j`, `k_j >= max(j,2)` and `A_j` with

`per(A_j)-per(A_j^k_j) < dist(A_j,F_n)^2/j`.

Exceptional matrices cannot satisfy this strict inequality because both sides would be zero. Distances are uniformly bounded on the Birkhoff polytope, so any compact limiting permanent gap is nonpositive. Lemma 5.1 forces the limiting matrix to be some `F in F_n`. The local estimate gives

`per(A_j)-per(A_j^k_j) >= (p(F)/8)||A_j-F||_F^2 >= (p(F)/8)dist(A_j,F_n)^2`.

For sufficiently large `j`, this contradicts `1/j < p(F)/8`; the distance is positive because `F_n` is finite and `A_j` is not exceptional. The case `n=1` is trivial. Both global constants remain nonexplicit.

## Suggested presentation refinements

- In the stability proof, write `k_j >= max(j,2)` and explicitly mention that the distance is positive for a nonexceptional matrix. These clarify rather than repair the argument.
- Explain the fixed-`t`, then `j`, then `t -> infinity` order of limits prominently. It is the decisive global uniformity step.
- Keep the local theorem's verification separate: this audit does not certify its derivative identities or numerical constants.
- Do not describe finite fixtures or this reasoning audit as a proof-assistant verification of the universal theorem.
