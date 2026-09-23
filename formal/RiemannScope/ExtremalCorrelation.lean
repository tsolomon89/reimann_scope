/-
RiemannScope.ExtremalCorrelation
Abstract finite extremal-grade correlation lemma and collision deduction.
Reference: MATH_CONTRACT.md §39, TC_EXTREMAL_GRADE_CORRELATION_LEMMA.md
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace RiemannScope

/-- Maximal Grade Difference Uniqueness:
    In any finite set of integer grades G with maximum K_plus and minimum K_minus,
    the ordered pair (K_plus, K_minus) is the unique pair in G × G achieving
    the difference K_plus - K_minus. -/
theorem maximal_grade_difference_unique (K_plus K_minus : ℤ) (G : Finset ℤ)
    (h_max : ∀ x ∈ G, x ≤ K_plus)
    (h_min : ∀ x ∈ G, K_minus ≤ x)
    (K J : ℤ) (hK : K ∈ G) (hJ : J ∈ G)
    (h_diff : K - J = K_plus - K_minus) :
    K = K_plus ∧ J = K_minus := by
  have hK_le : K ≤ K_plus := h_max K hK
  have hJ_ge : K_minus ≤ J := h_min J hJ
  have hK_eq : K = K_plus := by linarith
  have hJ_eq : J = K_minus := by linarith
  exact ⟨hK_eq, hJ_eq⟩

/-- Strict Dominance of Extremal Difference:
    Every non-extremal pair (K, J) ≠ (K_plus, K_minus) has a strictly smaller
    grade difference: K - J < K_plus - K_minus. -/
theorem other_grade_difference_strictly_smaller (K_plus K_minus : ℤ) (G : Finset ℤ)
    (h_max : ∀ x ∈ G, x ≤ K_plus)
    (h_min : ∀ x ∈ G, K_minus ≤ x)
    (K J : ℤ) (hK : K ∈ G) (hJ : J ∈ G)
    (h_not_extremal : ¬(K = K_plus ∧ J = K_minus)) :
    K - J < K_plus - K_minus := by
  have hK_le : K ≤ K_plus := h_max K hK
  have hJ_ge : K_minus ≤ J := h_min J hJ
  have h_diff_le : K - J ≤ K_plus - K_minus := by linarith
  by_contra h_contra
  push_neg at h_contra
  have h_eq : K - J = K_plus - K_minus := le_antisymm h_diff_le h_contra
  have ⟨h1, h2⟩ := maximal_grade_difference_unique K_plus K_minus G h_max h_min K J hK hJ h_eq
  exact h_not_extremal ⟨h1, h2⟩

/-- Atomic Spatial Location Equality Cross-Multiplication:
    If tau_a * (n0 / m0) = tau_c * (n1 / m1) with m0, m1 ≠ 0,
    then (n0 * m1) * tau_a = (n1 * m0) * tau_c in ℝ. -/
theorem atomic_location_equality_cross_mul (tau_a tau_c n0 m0 n1 m1 : ℝ)
    (hm0 : m0 ≠ 0) (hm1 : m1 ≠ 0)
    (h_loc : tau_a * (n0 / m0) = tau_c * (n1 / m1)) :
    (n0 * m1) * tau_a = (n1 * m0) * tau_c := by
  calc (n0 * m1) * tau_a
    _ = (tau_a * (n0 / m0)) * (m0 * m1) := by
        calc (n0 * m1) * tau_a
          _ = tau_a * (n0 * m1) := by ring
          _ = tau_a * ((n0 / m0) * m0 * m1) := by rw [div_mul_cancel₀ n0 hm0]
          _ = (tau_a * (n0 / m0)) * (m0 * m1) := by ring
    _ = (tau_c * (n1 / m1)) * (m0 * m1) := by rw [h_loc]
    _ = tau_c * ((n1 / m1) * m1 * m0) := by ring
    _ = tau_c * (n1 * m0) := by rw [div_mul_cancel₀ n1 hm1]
    _ = (n1 * m0) * tau_c := by ring

/-- Integer Cross-Multiplication for Nat Indices:
    For positive natural numbers n0, m0, n1, m1, the cross-multiplied weights
    M = n0 * m1 and N = n1 * m0 are strictly positive natural numbers. -/
theorem nat_indices_product_pos (n0 m0 n1 m1 : ℕ)
    (hn0 : 0 < n0) (hm0 : 0 < m0) (hn1 : 0 < n1) (hm1 : 0 < m1) :
    0 < n0 * m1 ∧ 0 < n1 * m0 := by
  constructor
  · exact Nat.mul_pos hn0 hm1
  · exact Nat.mul_pos hn1 hm0

/-- Abstract Finite Extremal-Grade Correlation Lemma:
    Suppose an atom at location tau_a * (n0 / m0) from the unique extremal pair
    (K_plus, K_minus) with difference a = K_plus - K_minus is cancelled by an atom
    from another active pair (K', J') with difference c = K' - J' at location
    tau_c * (n1 / m1).
    Then:
    1. The grade differences are strictly distinct: a ≠ c (in fact c < a).
    2. The station indices yield positive integers M = n0 * m1 and N = n1 * m0
       such that M * tau_a = N * tau_c. -/
theorem finite_extremal_grade_correlation_lemma
    (K_plus K_minus : ℤ) (G : Finset ℤ)
    (h_max : ∀ x ∈ G, x ≤ K_plus)
    (h_min : ∀ x ∈ G, K_minus ≤ x)
    (K' J' : ℤ) (hK' : K' ∈ G) (hJ' : J' ∈ G)
    (h_not_ext : ¬(K' = K_plus ∧ J' = K_minus))
    (tau_a tau_c : ℝ)
    (n0 m0 n1 m1 : ℕ)
    (hn0 : 0 < n0) (hm0 : 0 < m0) (hn1 : 0 < n1) (hm1 : 0 < m1)
    (h_loc : tau_a * ((n0 : ℝ) / (m0 : ℝ)) = tau_c * ((n1 : ℝ) / (m1 : ℝ))) :
    (K' - J' ≠ K_plus - K_minus) ∧
    (∃ (M N : ℕ), 0 < M ∧ 0 < N ∧ (M : ℝ) * tau_a = (N : ℝ) * tau_c) := by
  have h_lt : K' - J' < K_plus - K_minus :=
    other_grade_difference_strictly_smaller K_plus K_minus G h_max h_min K' J' hK' hJ' h_not_ext
  have h_ne : K' - J' ≠ K_plus - K_minus := ne_of_lt h_lt
  have hm0_real : (m0 : ℝ) ≠ 0 := by
    have : 0 < (m0 : ℝ) := Nat.cast_pos.mpr hm0
    linarith
  have hm1_real : (m1 : ℝ) ≠ 0 := by
    have : 0 < (m1 : ℝ) := Nat.cast_pos.mpr hm1
    linarith
  have h_cross : ((n0 : ℝ) * (m1 : ℝ)) * tau_a = ((n1 : ℝ) * (m0 : ℝ)) * tau_c :=
    atomic_location_equality_cross_mul tau_a tau_c (n0 : ℝ) (m0 : ℝ) (n1 : ℝ) (m1 : ℝ) hm0_real hm1_real h_loc
  have hM_cast : ((n0 * m1 : ℕ) : ℝ) = (n0 : ℝ) * (m1 : ℝ) := by push_cast; rfl
  have hN_cast : ((n1 * m0 : ℕ) : ℝ) = (n1 : ℝ) * (m0 : ℝ) := by push_cast; rfl
  rw [← hM_cast, ← hN_cast] at h_cross
  have ⟨hM_pos, hN_pos⟩ := nat_indices_product_pos n0 m0 n1 m1 hn0 hm0 hn1 hm1
  constructor
  · exact h_ne
  · exact ⟨n0 * m1, n1 * m0, hM_pos, hN_pos, h_cross⟩

end RiemannScope
