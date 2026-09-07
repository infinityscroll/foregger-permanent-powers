# Semantic audit of the dimension-two formalization

Reviewed 8 September 2026 against the complete Lean source, followed by a
successful compilation and axiom-log check in this standalone Lake project.

- **Matrices and coefficients:** `Mat` is exactly
  `Matrix (Fin 2) (Fin 2) ℝ`, so the theorems quantify over all real entries,
  not just rational examples or a sampled family.
- **Hypotheses:** `DoublyStochastic` requires every entry nonnegative and
  separately requires every row sum and every column sum to equal one.
  `representation` derives the one-parameter form from these hypotheses.
- **Permanent:** `permanent_two` expands mathlib's actual
  `Matrix.permanent`, using the two permutations of `Fin 2`. It is not a
  replacement function merely named permanent.
- **Powers:** `M^k` is the power operation from the ordinary matrix ring.
  `family_mul` proves the matrix multiplication identity explicitly;
  `family_pow` then follows by induction on the natural exponent.
- **Distance:** `frobeniusSq` sums squared entry differences.
  `exceptionalDistanceSq` takes the minimum over exactly the three stated
  exceptional matrices. Thus the stated coefficient multiplies the square
  of the usual Frobenius distance, without dimension-dependent rescaling.
- **Quantifiers:** the inequality holds for every `k ≥ 1`; stability and
  equality classification hold for every `k ≥ 2`. Optimality quantifies
  over any coefficient valid for every doubly stochastic matrix and every
  `k ≥ 2`, and specializes to a valid matrix with parameter `1/2` and `k=2`.
- **Equality:** `permanent_pow_eq_iff` is an equivalence, proving both
  necessity and sufficiency. The right side is exactly the identity,
  transposition, and uniform averaging matrix via `family 1`, `family (-1)`,
  and `family 0`.
- **Foundations:** all four main theorem reports contain only `propext`,
  `Classical.choice`, and `Quot.sound`; no `sorry`, custom axiom, or
  `native_decide` appears in the source. Auxiliary lemmas are fully proved.

No semantic mismatch was found between these four dimension-two claims and
their Lean statements. The all-dimensions candidate theorem and its local and
global analytic arguments are outside this formalization's scope.
