import Mathlib.LinearAlgebra.Matrix.Permanent
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace ForeggerTwo

noncomputable section

abbrev Mat := Matrix (Fin 2) (Fin 2) ℝ

/-- The entrywise definition of a real doubly stochastic matrix. -/
def DoublyStochastic (M : Mat) : Prop :=
  (∀ i j, 0 ≤ M i j) ∧ (∀ i, ∑ j, M i j = 1) ∧ (∀ j, ∑ i, M i j = 1)

def family (t : ℝ) : Mat :=
  fun i j => if i = j then (1+t)/2 else (1-t)/2

theorem permanent_two (M : Mat) :
    M.permanent = M 0 0 * M 1 1 + M 1 0 * M 0 1 := by
  have hu : (Finset.univ : Finset (Equiv.Perm (Fin 2))) =
      {1, Equiv.swap 0 1} := by decide
  have hne : (1 : Equiv.Perm (Fin 2)) ≠ Equiv.swap 0 1 := by decide
  simp [Matrix.permanent, hu, hne, Fin.prod_univ_two]

theorem family_permanent (t : ℝ) : (family t).permanent = (1+t^2)/2 := by
  rw [permanent_two]
  simp [family]
  ring

theorem family_one : family 1 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [family, Matrix.one_apply]

theorem family_mul (s t : ℝ) : family s * family t = family (s*t) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [family, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem family_pow (t : ℝ) (k : ℕ) : (family t)^k = family (t^k) := by
  induction k with
  | zero => simp [family_one]
  | succ k ih => rw [pow_succ, ih, family_mul, pow_succ]

theorem representation (M : Mat) (hM : DoublyStochastic M) :
    ∃ t : ℝ, -1 ≤ t ∧ t ≤ 1 ∧ M = family t := by
  obtain ⟨hn, hr, hc⟩ := hM
  have hr0 := hr 0
  have hr1 := hr 1
  have hc0 := hc 0
  simp only [Fin.sum_univ_two] at hr0 hr1 hc0
  refine ⟨2*M 0 0-1, ?_, ?_, ?_⟩
  · linarith [hn 0 0]
  · linarith [hn 0 1]
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [family] <;> linarith

theorem scalar_power_bound (t : ℝ) (hlo : -1 ≤ t) (hhi : t ≤ 1)
    (k : ℕ) (hk : 1 ≤ k) : (t^k)^2 ≤ t^2 := by
  have hsq : t^2 ≤ 1 := by nlinarith
  have h := pow_le_pow_of_le_one (sq_nonneg t) hsq hk
  simpa [← pow_mul, Nat.mul_comm] using h

/-- The ordinary-matrix-power conjecture in dimension two, for every k >= 1. -/
theorem permanent_pow_le (M : Mat) (hM : DoublyStochastic M)
    (k : ℕ) (hk : 1 ≤ k) : (M^k).permanent ≤ M.permanent := by
  obtain ⟨t, hlo, hhi, rfl⟩ := representation M hM
  rw [family_pow, family_permanent, family_permanent]
  have h := scalar_power_bound t hlo hhi k hk
  linarith

theorem family_stochastic (t : ℝ) (hlo : -1 ≤ t) (hhi : t ≤ 1) :
    DoublyStochastic (family t) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j
    fin_cases i <;> fin_cases j <;> simp [family] <;> linarith
  · intro i
    fin_cases i <;> simp [family, Fin.sum_univ_two] <;> ring
  · intro j
    fin_cases j <;> simp [family, Fin.sum_univ_two] <;> ring

/-- Squared Frobenius distance, defined explicitly by the sum of squared entries. -/
def frobeniusSq (M N : Mat) : ℝ := ∑ i, ∑ j, (M i j - N i j)^2

/-- Squared distance to the three exceptional matrices in dimension two. -/
def exceptionalDistanceSq (M : Mat) : ℝ :=
  min (frobeniusSq M (family 0))
    (min (frobeniusSq M (family 1)) (frobeniusSq M (family (-1))))

theorem family_frobeniusSq (t s : ℝ) :
    frobeniusSq (family t) (family s) = (t-s)^2 := by
  simp [frobeniusSq, family, Fin.sum_univ_two]
  ring

theorem family_distance (t : ℝ) :
    exceptionalDistanceSq (family t) = min (t^2) ((1-|t|)^2) := by
  simp only [exceptionalDistanceSq, family_frobeniusSq, sub_zero]
  by_cases ht : 0 ≤ t
  · rw [abs_of_nonneg ht, min_eq_left (by nlinarith : (t-1)^2 ≤ (t- -1)^2)]
    congr 1
    ring
  · have ht' : t ≤ 0 := le_of_not_ge ht
    rw [abs_of_nonpos ht', min_eq_right (by nlinarith : (t- -1)^2 ≤ (t-1)^2)]
    congr 1
    ring

theorem scalar_stability (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    (3/8 : ℝ) * min (s^2) ((1-s)^2) ≤ (s^2-s^4)/2 := by
  by_cases hs : s ≤ 1/2
  · rw [min_eq_left (by nlinarith : s^2 ≤ (1-s)^2)]
    have h := mul_nonneg (mul_nonneg (sq_nonneg s)
      (by linarith : 0 ≤ 1-2*s)) (by linarith : 0 ≤ 1+2*s)
    nlinarith
  · rw [min_eq_right (by nlinarith : (1-s)^2 ≤ s^2)]
    have h := mul_nonneg (mul_nonneg (by linarith : 0 ≤ 1-s)
      (by linarith : 0 ≤ 2*s-1)) (by nlinarith : 0 ≤ 2*s^2+3*s+3)
    nlinarith

/-- A sharp quadratic stability bound for every real doubly stochastic 2x2 matrix. -/
theorem sharp_stability (M : Mat) (hM : DoublyStochastic M)
    (k : ℕ) (hk : 2 ≤ k) :
    (3/8 : ℝ) * exceptionalDistanceSq M ≤ M.permanent - (M^k).permanent := by
  obtain ⟨t, hlo, hhi, rfl⟩ := representation M hM
  rw [family_pow, family_permanent, family_permanent, family_distance]
  have habs : |t| ≤ 1 := abs_le.mpr ⟨hlo, hhi⟩
  have hsq : t^2 ≤ 1 := by nlinarith
  have hp := pow_le_pow_of_le_one (sq_nonneg t) hsq hk
  have hp' : (t^k)^2 ≤ t^4 := by
    simpa only [← pow_mul, Nat.mul_comm] using hp
  have hs := scalar_stability |t| (abs_nonneg t) habs
  have heven2 : |t|^2 = t^2 := sq_abs t
  have heven4 : |t|^4 = t^4 := by nlinarith [sq_nonneg (t^2)]
  rw [heven2, heven4] at hs
  linarith

/-- The coefficient 3/8 cannot be increased when all k>=2 are included. -/
theorem stability_constant_optimal (c : ℝ)
    (hc : ∀ (M : Mat), DoublyStochastic M → ∀ k : ℕ, 2 ≤ k →
      c * exceptionalDistanceSq M ≤ M.permanent - (M^k).permanent) :
    c ≤ 3/8 := by
  have h := hc (family (1/2)) (family_stochastic (1/2) (by norm_num) (by norm_num))
    2 (by norm_num)
  rw [family_pow, family_permanent, family_permanent, family_distance] at h
  norm_num at h
  linarith

/-- For every k >= 2, equality holds precisely for the two permutation matrices
and the matrix with all entries equal to 1/2. -/
theorem permanent_pow_eq_iff (M : Mat) (hM : DoublyStochastic M)
    (k : ℕ) (hk : 2 ≤ k) :
    (M^k).permanent = M.permanent ↔
      M = family (-1) ∨ M = family 0 ∨ M = family 1 := by
  constructor
  · intro heq
    have hs := sharp_stability M hM k hk
    rw [heq, sub_self] at hs
    obtain ⟨t, hlo, hhi, rfl⟩ := representation M hM
    rw [family_distance] at hs
    by_cases ht : t^2 ≤ (1-|t|)^2
    · rw [min_eq_left ht] at hs
      have hz : t = 0 := by nlinarith [sq_nonneg t]
      exact Or.inr (Or.inl (congrArg family hz))
    · rw [min_eq_right (le_of_not_ge ht)] at hs
      have ha : |t| = 1 := by nlinarith [sq_nonneg (1-|t|)]
      by_cases hpos : 0 ≤ t
      · rw [abs_of_nonneg hpos] at ha
        exact Or.inr (Or.inr (congrArg family ha))
      · rw [abs_of_nonpos (le_of_not_ge hpos)] at ha
        exact Or.inl (congrArg family (by linarith : t = -1))
  · rintro (rfl | rfl | rfl)
    · rw [family_pow, family_permanent, family_permanent]
      have hneg : ((-1 : ℝ)^k)^2 = 1 := by
        rw [← pow_mul, Nat.mul_comm, pow_mul]
        norm_num
      norm_num [hneg]
    · have hk0 : k ≠ 0 := by omega
      simp [family_pow, family_permanent, hk0]
    · simp [family_pow, family_permanent]

end
end ForeggerTwo

#print axioms ForeggerTwo.permanent_pow_le
#print axioms ForeggerTwo.sharp_stability
#print axioms ForeggerTwo.stability_constant_optimal
#print axioms ForeggerTwo.permanent_pow_eq_iff
