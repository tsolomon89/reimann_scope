/-
RiemannScope.ExtremalCorrelation
Abstract finite extremal-grade correlation lemma and collision deduction.
Reference: MATH_CONTRACT.md §39, TC_EXTREMAL_GRADE_CORRELATION_LEMMA.md
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.List
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace RiemannScope

open scoped Classical

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

/- ========================================================================= -/
/- Full Finite Atomic Measure Formalization: nu_b = 0 implies integer collision -/
/- ========================================================================= -/

/-- Spatial ratio of an atom under scale factor tau > 0:
    atom_loc tau (K, J, n, m) = tau^(K - J) * (n / m). -/
noncomputable def atom_spatial_ratio (tau : ℝ) (K J : ℤ) (n m : ℕ) : ℝ :=
  tau ^ (K - J) * ((n : ℝ) / (m : ℝ))

/-- Signed mass of an atom with coefficients b and station weights a:
    atom_mass a b (K, J, n, m) = b K * b J * a K n * a J m. -/
noncomputable def atom_pair_mass (a : ℤ → ℕ → ℝ) (b : ℤ → ℝ) (K J : ℤ) (n m : ℕ) : ℝ :=
  b K * b J * a K n * a J m

/-- Evaluation of discrete correlation atomic sum at spatial location y:
    Sums masses of all atoms (K, J, n, m) whose spatial ratio equals y. -/
noncomputable def nu_b_mass_at (atoms : List (ℤ × ℤ × ℕ × ℕ)) (a : ℤ → ℕ → ℝ) (b : ℤ → ℝ) (tau : ℝ) (y : ℝ) : ℝ :=
  ((atoms.filter (fun p => decide (atom_spatial_ratio tau p.1 p.2.1 p.2.2.1 p.2.2.2 = y))).map
    (fun p => atom_pair_mass a b p.1 p.2.1 p.2.2.1 p.2.2.2)).sum

/-- Linearity of mapped list sum under constant scalar multiplication -/
lemma list_sum_map_mul_const (c : ℝ) (l : List α) (f : α → ℝ) :
    (l.map (fun x => c * f x)).sum = c * (l.map f).sum := by
  induction l with
  | nil => simp [List.sum_nil]
  | cons hd tl ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [ih]
    ring

/-- Positivity of sum of strictly positive reals over a non-empty list -/
lemma list_sum_pos_of_all_pos (l : List ℝ) (hl : ∀ x ∈ l, 0 < x) (hne : l ≠ []) :
    0 < l.sum := by
  induction l with
  | nil => contradiction
  | cons head tail ih =>
    simp only [List.sum_cons]
    have h_head : 0 < head := hl head (List.Mem.head _)
    cases tail with
    | nil =>
      simp only [List.sum_nil, add_zero]
      exact h_head
    | cons t_hd t_tl =>
      have h_tail_ne : (t_hd :: t_tl) ≠ [] := by simp
      have h_tail_all : ∀ x ∈ (t_hd :: t_tl), 0 < x := fun x hx => hl x (List.Mem.tail _ hx)
      have h_tail_sum : 0 < (t_hd :: t_tl).sum := ih h_tail_all h_tail_ne
      linarith

/-- Full Finite Extremal-Grade Correlation Theorem:
    Let G be a finite set of integer grades with unique maximum K_plus and minimum K_minus (K_minus < K_plus).
    Let b be real coefficients with b K_plus ≠ 0 and b K_minus ≠ 0.
    Let a K n be strictly positive station weights (a K n > 0).
    Let atoms be any finite list of cross-grade atoms (K, J, n, m) with K, J ∈ G, K ≠ J, and positive station indices n, m > 0.
    Suppose atoms contains at least one extremal atom p0 = (K_plus, K_minus, n0, m0).
    If the discrete atomic correlation measure nu_b vanishes identically across all real spatial locations:
        ∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0,
    then:
    1. The extremal atom MUST be cancelled by an atom (K', J', n1, m1) from a strictly distinct grade pair (K', J') ≠ (K_plus, K_minus).
    2. The grade differences are strictly distinct: K' - J' ≠ K_plus - K_minus (in fact K' - J' < K_plus - K_minus).
    3. The station indices yield positive integers M = n0 * m1 > 0 and N = n1 * m0 > 0 such that:
        M * tau ^ (K_plus - K_minus) = N * tau ^ (K' - J'). -/
theorem full_finite_extremal_grade_correlation_theorem
    (tau : ℝ) (_htau : 0 < tau)
    (G : Finset ℤ)
    (K_plus K_minus : ℤ)
    (_hK_plus : K_plus ∈ G) (_hK_minus : K_minus ∈ G)
    (h_max : ∀ x ∈ G, x ≤ K_plus)
    (h_min : ∀ x ∈ G, K_minus ≤ x)
    (_h_diff_grades : K_minus < K_plus)
    (b : ℤ → ℝ)
    (hb_plus : b K_plus ≠ 0)
    (hb_minus : b K_minus ≠ 0)
    (a : ℤ → ℕ → ℝ)
    (h_a_pos : ∀ K n, 0 < a K n)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (h_atoms_in_G : ∀ p ∈ atoms, p.1 ∈ G ∧ p.2.1 ∈ G)
    (h_atoms_pos : ∀ p ∈ atoms, 0 < p.2.2.1 ∧ 0 < p.2.2.2)
    (n0 m0 : ℕ) (hn0 : 0 < n0) (hm0 : 0 < m0)
    (h_p0_in : (K_plus, K_minus, n0, m0) ∈ atoms)
    (h_nu_zero : ∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0) :
    ∃ (K' J' : ℤ) (n1 m1 : ℕ),
      (K', J', n1, m1) ∈ atoms ∧
      (K' - J' ≠ K_plus - K_minus) ∧
      (∃ (M N : ℕ), 0 < M ∧ 0 < N ∧
        (M : ℝ) * tau ^ (K_plus - K_minus) = (N : ℝ) * tau ^ (K' - J')) := by
  -- 1. Consider the target location of the extremal atom p0
  let y0 := atom_spatial_ratio tau K_plus K_minus n0 m0
  let l0 := atoms.filter (fun p => decide (atom_spatial_ratio tau p.1 p.2.1 p.2.2.1 p.2.2.2 = y0))
  have h_p0_in_l0 : (K_plus, K_minus, n0, m0) ∈ l0 := by
    rw [List.mem_filter]
    refine ⟨h_p0_in, ?_⟩
    simp [y0]
  have h_l0_nonempty : l0 ≠ [] := by
    intro h_nil
    rw [h_nil] at h_p0_in_l0
    exact List.not_mem_nil _ h_p0_in_l0

  -- 2. From h_nu_zero at y0, the sum of masses in l0 is zero
  have h_sum_zero : (l0.map (fun p => atom_pair_mass a b p.1 p.2.1 p.2.2.1 p.2.2.2)).sum = 0 := h_nu_zero y0

  -- 3. Show there must exist p' in l0 with ¬(p'.1 = K_plus ∧ p'.2.1 = K_minus)
  have h_exists_other : ∃ p' ∈ l0, ¬(p'.1 = K_plus ∧ p'.2.1 = K_minus) := by
    by_contra h_none
    push_neg at h_none
    -- If all atoms in l0 have pair (K_plus, K_minus), then mass factors through b K_plus * b K_minus
    let C := b K_plus * b K_minus
    have hC_ne : C ≠ 0 := mul_ne_zero hb_plus hb_minus
    have h_mass_eq : ∀ p ∈ l0,
        atom_pair_mass a b p.1 p.2.1 p.2.2.1 p.2.2.2 =
        C * (a K_plus p.2.2.1 * a K_minus p.2.2.2) := by
      intro p hp
      have ⟨hK, hJ⟩ := h_none p hp
      dsimp [atom_pair_mass, C]
      rw [hK, hJ]
      ring
    -- The mapped list equals a scalar multiple of positive terms
    have h_map_eq :
        l0.map (fun p => atom_pair_mass a b p.1 p.2.1 p.2.2.1 p.2.2.2) =
        l0.map (fun p => C * (a K_plus p.2.2.1 * a K_minus p.2.2.2)) :=
      List.map_congr h_mass_eq
    rw [h_map_eq] at h_sum_zero
    rw [list_sum_map_mul_const C l0 (fun p => a K_plus p.2.2.1 * a K_minus p.2.2.2)] at h_sum_zero
    -- The inner sum is strictly positive
    have h_pos_terms : ∀ x ∈ l0.map (fun p => a K_plus p.2.2.1 * a K_minus p.2.2.2), 0 < x := by
      intro x hx
      rw [List.mem_map] at hx
      rcases hx with ⟨p, _, rfl⟩
      exact mul_pos (h_a_pos K_plus p.2.2.1) (h_a_pos K_minus p.2.2.2)
    have h_map_ne : l0.map (fun p => a K_plus p.2.2.1 * a K_minus p.2.2.2) ≠ [] := by
      intro h_empty
      have : l0 = [] := List.eq_nil_of_map_eq_nil h_empty
      exact h_l0_nonempty this
    have h_inner_pos : 0 < (l0.map (fun p => a K_plus p.2.2.1 * a K_minus p.2.2.2)).sum :=
      list_sum_pos_of_all_pos _ h_pos_terms h_map_ne
    have h_prod_ne : C * (l0.map (fun p => a K_plus p.2.2.1 * a K_minus p.2.2.2)).sum ≠ 0 := by
      apply mul_ne_zero hC_ne (ne_of_gt h_inner_pos)
    exact h_prod_ne h_sum_zero

  -- 4. Extract the cancelling atom p'
  rcases h_exists_other with ⟨p', hp'_in_l0, hp'_not_ext⟩
  rw [List.mem_filter] at hp'_in_l0
  rcases hp'_in_l0 with ⟨hp'_in_atoms, hp'_loc_dec⟩
  have hp'_loc : atom_spatial_ratio tau p'.1 p'.2.1 p'.2.2.1 p'.2.2.2 = y0 := by
    simpa using hp'_loc_dec
  dsimp [y0] at hp'_loc

  -- 5. Establish properties of p'
  have ⟨hp'_K_in_G, hp'_J_in_G⟩ := h_atoms_in_G p' hp'_in_atoms
  have ⟨hp'_n_pos, hp'_m_pos⟩ := h_atoms_pos p' hp'_in_atoms

  -- 6. Apply finite_extremal_grade_correlation_lemma
  have h_lemma := finite_extremal_grade_correlation_lemma
    K_plus K_minus G h_max h_min
    p'.1 p'.2.1 hp'_K_in_G hp'_J_in_G
    hp'_not_ext
    (tau ^ (K_plus - K_minus)) (tau ^ (p'.1 - p'.2.1))
    n0 m0 p'.2.2.1 p'.2.2.2
    hn0 hm0 hp'_n_pos hp'_m_pos
    (by
      dsimp [atom_spatial_ratio] at hp'_loc
      exact hp'_loc.symm)

  rcases h_lemma with ⟨h_diff_ne, M, N, hM_pos, hN_pos, h_cross⟩
  refine ⟨p'.1, p'.2.1, p'.2.2.1, p'.2.2.2, hp'_in_atoms, ?_, M, N, hM_pos, hN_pos, ?_⟩
  · exact h_diff_ne
  · exact h_cross

/-- Lindemann-Weierstrass Transcendence Specialization:
    If tau satisfies the transcendence property that no non-zero integer power of tau is rational:
        ∀ k ≠ 0, ∀ (r : ℚ), tau ^ k ≠ r,
    then the discrete atomic correlation measure nu_b CANNOT vanish identically.
    Derives False directly from nu_b = 0 without additional hypotheses. -/
theorem full_finite_correlation_transcendence_contradiction
    (tau : ℝ) (htau : 0 < tau)
    (h_trans : ∀ (k : ℤ), k ≠ 0 → ∀ (r : ℚ), tau ^ k ≠ (r : ℝ))
    (G : Finset ℤ)
    (K_plus K_minus : ℤ)
    (hK_plus : K_plus ∈ G) (hK_minus : K_minus ∈ G)
    (h_max : ∀ x ∈ G, x ≤ K_plus)
    (h_min : ∀ x ∈ G, K_minus ≤ x)
    (h_diff_grades : K_minus < K_plus)
    (b : ℤ → ℝ)
    (hb_plus : b K_plus ≠ 0)
    (hb_minus : b K_minus ≠ 0)
    (a : ℤ → ℕ → ℝ)
    (h_a_pos : ∀ K n, 0 < a K n)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (h_atoms_in_G : ∀ p ∈ atoms, p.1 ∈ G ∧ p.2.1 ∈ G)
    (h_atoms_pos : ∀ p ∈ atoms, 0 < p.2.2.1 ∧ 0 < p.2.2.2)
    (n0 m0 : ℕ) (hn0 : 0 < n0) (hm0 : 0 < m0)
    (h_p0_in : (K_plus, K_minus, n0, m0) ∈ atoms)
    (h_nu_zero : ∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0) :
    False := by
  have ⟨K', J', _, _, _, h_ne, M, N, hM_pos, _, h_cross⟩ :=
    full_finite_extremal_grade_correlation_theorem
      tau htau G K_plus K_minus hK_plus hK_minus h_max h_min h_diff_grades
      b hb_plus hb_minus a h_a_pos atoms h_atoms_in_G h_atoms_pos
      n0 m0 hn0 hm0 h_p0_in h_nu_zero

  let a_diff := K_plus - K_minus
  let c_diff := K' - J'
  have h_k_ne : a_diff - c_diff ≠ 0 := by
    intro h_eq
    have h_diff_eq : K' - J' = K_plus - K_minus := by
      dsimp [a_diff, c_diff] at h_eq
      linarith
    exact h_ne h_diff_eq

  have hM_real_pos : 0 < (M : ℝ) := Nat.cast_pos.mpr hM_pos
  have hM_real_ne : (M : ℝ) ≠ 0 := ne_of_gt hM_real_pos

  have h_tau_pow_div : tau ^ a_diff / tau ^ c_diff = ((N : ℚ) / (M : ℚ) : ℚ) := by
    push_cast
    have h_div : tau ^ a_diff = ((N : ℝ) / (M : ℝ)) * tau ^ c_diff := by
      calc tau ^ a_diff = ((M : ℝ) * tau ^ a_diff) / (M : ℝ) := by rw [mul_div_cancel_left₀ (tau ^ a_diff) hM_real_ne]
      _ = ((N : ℝ) * tau ^ c_diff) / (M : ℝ) := by rw [h_cross]
      _ = ((N : ℝ) / (M : ℝ)) * tau ^ c_diff := by ring
    have htau_c_pos : 0 < tau ^ c_diff := zpow_pos_of_pos htau c_diff
    have htau_c_ne : tau ^ c_diff ≠ 0 := ne_of_gt htau_c_pos
    rw [h_div, mul_div_cancel_right₀ _ htau_c_ne]

  have h_tau_sub : tau ^ (a_diff - c_diff) = tau ^ a_diff / tau ^ c_diff := by
    rw [zpow_sub₀ (ne_of_gt htau)]

  rw [← h_tau_sub] at h_tau_pow_div
  have h_contra := h_trans (a_diff - c_diff) h_k_ne ((N : ℚ) / (M : ℚ))
  exact h_contra h_tau_pow_div

#print axioms full_finite_extremal_grade_correlation_theorem
#print axioms full_finite_correlation_transcendence_contradiction

end RiemannScope
