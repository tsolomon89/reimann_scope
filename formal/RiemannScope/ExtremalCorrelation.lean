import Mathlib.Analysis.SpecialFunctions.Log.Basic
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

/-- Logarithmic lag of an atom under scale factor tau > 0:
    atom_log_lag tau (K, J, n, m) = log (tau^(K - J) * (n / m)). -/
noncomputable def atom_log_lag (tau : ℝ) (K J : ℤ) (n m : ℕ) : ℝ :=
  Real.log (atom_spatial_ratio tau K J n m)

/-- Strict positivity of atom spatial ratio:
    For tau > 0 and positive natural indices n, m > 0,
    the spatial ratio tau^(K - J) * (n / m) is strictly positive. -/
theorem atom_spatial_ratio_pos (tau : ℝ) (htau : 0 < tau) (K J : ℤ) (n m : ℕ)
    (hn : 0 < n) (hm : 0 < m) :
    0 < atom_spatial_ratio tau K J n m := by
  dsimp [atom_spatial_ratio]
  have h_pow : 0 < tau ^ (K - J) := zpow_pos_of_pos htau (K - J)
  have hn_real : 0 < (n : ℝ) := Nat.cast_pos.mpr hn
  have hm_real : 0 < (m : ℝ) := Nat.cast_pos.mpr hm
  have h_div : 0 < (n : ℝ) / (m : ℝ) := div_pos hn_real hm_real
  exact mul_pos h_pow h_div

/-- Equivalence between spatial ratio equality and logarithmic lag equality:
    By injectivity of Real.log on (0, ∞), two atoms have equal spatial ratios
    if and only if their logarithmic lags are equal.
    This connects the spatial ratio representation of the formal theorem to
    the intended signed correlation at logarithmic lags:
        u - v = log(x / y) = log(tau^(K-J) * n / m). -/
theorem atom_spatial_ratio_eq_iff_log_lag_eq
    (tau : ℝ) (htau : 0 < tau)
    (K1 J1 K2 J2 : ℤ) (n1 m1 n2 m2 : ℕ)
    (hn1 : 0 < n1) (hm1 : 0 < m1)
    (hn2 : 0 < n2) (hm2 : 0 < m2) :
    atom_spatial_ratio tau K1 J1 n1 m1 = atom_spatial_ratio tau K2 J2 n2 m2 ↔
    atom_log_lag tau K1 J1 n1 m1 = atom_log_lag tau K2 J2 n2 m2 := by
  have h1 : 0 < atom_spatial_ratio tau K1 J1 n1 m1 := atom_spatial_ratio_pos tau htau K1 J1 n1 m1 hn1 hm1
  have h2 : 0 < atom_spatial_ratio tau K2 J2 n2 m2 := atom_spatial_ratio_pos tau htau K2 J2 n2 m2 hn2 hm2
  dsimp [atom_log_lag]
  constructor
  · intro h
    rw [h]
  · intro h
    have h_inj : Set.InjOn Real.log (Set.Ioi (0 : ℝ)) := Real.log_injOn_pos
    have h1_mem : atom_spatial_ratio tau K1 J1 n1 m1 ∈ Set.Ioi (0 : ℝ) := h1
    have h2_mem : atom_spatial_ratio tau K2 J2 n2 m2 ∈ Set.Ioi (0 : ℝ) := h2
    exact h_inj h1_mem h2_mem h

/-- Canonical strictly positive extension of authentic station weights:
    Given authentic TC weights a K n that are strictly positive on the finite active stations
    actually occurring in atoms, positive_weight_extension extends them to all of ℤ × ℕ
    by setting unobserved or inactive stations to 1. -/
noncomputable def positive_weight_extension
    (a : ℤ → ℕ → ℝ)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (K : ℤ) (n : ℕ) : ℝ :=
  if (∃ p ∈ atoms, (p.1 = K ∧ p.2.2.1 = n) ∨ (p.2.1 = K ∧ p.2.2.2 = n)) then a K n else 1

/-- Agreement on active stations: on all pairs appearing in atoms,
    the positive weight extension identically matches the original weights a. -/
theorem positive_weight_extension_eq_on_atoms
    (a : ℤ → ℕ → ℝ)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (p : ℤ × ℤ × ℕ × ℕ) (hp : p ∈ atoms) :
    positive_weight_extension a atoms p.1 p.2.2.1 = a p.1 p.2.2.1 ∧
    positive_weight_extension a atoms p.2.1 p.2.2.2 = a p.2.1 p.2.2.2 := by
  dsimp [positive_weight_extension]
  have h1 : ∃ q ∈ atoms, (q.1 = p.1 ∧ q.2.2.1 = p.2.2.1) ∨ (q.2.1 = p.1 ∧ q.2.2.2 = p.2.2.1) := by
    refine ⟨p, hp, Or.inl ⟨rfl, rfl⟩⟩
  have h2 : ∃ q ∈ atoms, (q.1 = p.2.1 ∧ q.2.2.1 = p.2.2.2) ∨ (q.2.1 = p.2.1 ∧ q.2.2.2 = p.2.2.2) := by
    refine ⟨p, hp, Or.inr ⟨rfl, rfl⟩⟩
  simp [h1, h2]

/-- Strict positivity everywhere: if the authentic weights a are strictly positive
    on the active stations occurring in atoms, the extension is strictly positive everywhere. -/
theorem positive_weight_extension_pos
    (a : ℤ → ℕ → ℝ)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (h_supp : ∀ (p : ℤ × ℤ × ℕ × ℕ), p ∈ atoms → 0 < a p.1 p.2.2.1 ∧ 0 < a p.2.1 p.2.2.2) :
    ∀ K n, 0 < positive_weight_extension a atoms K n := by
  intro K n
  dsimp [positive_weight_extension]
  split_ifs with h_mem
  · rcases h_mem with ⟨p, hp, h_or⟩
    have ⟨ha1, ha2⟩ := h_supp p hp
    rcases h_or with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact ha1
    · exact ha2
  · exact zero_lt_one

/-- Invariance of atom pair mass under positive weight extension:
    For any atom p in atoms, atom_pair_mass using the extension equals
    atom_pair_mass using the original authentic weights. -/
theorem atom_pair_mass_extension_eq
    (a : ℤ → ℕ → ℝ)
    (b : ℤ → ℝ)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (p : ℤ × ℤ × ℕ × ℕ) (hp : p ∈ atoms) :
    atom_pair_mass (positive_weight_extension a atoms) b p.1 p.2.1 p.2.2.1 p.2.2.2 =
    atom_pair_mass a b p.1 p.2.1 p.2.2.1 p.2.2.2 := by
  have ⟨h1, h2⟩ := positive_weight_extension_eq_on_atoms a atoms p hp
  dsimp [atom_pair_mass]
  rw [h1, h2]

/-- Invariance of nu_b discrete measure under positive weight extension -/
theorem nu_b_mass_at_extension_eq
    (a : ℤ → ℕ → ℝ)
    (b : ℤ → ℝ)
    (tau : ℝ)
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (y : ℝ) :
    nu_b_mass_at atoms (positive_weight_extension a atoms) b tau y =
    nu_b_mass_at atoms a b tau y := by
  dsimp [nu_b_mass_at]
  congr 1
  apply List.map_congr
  intro p hp
  have hp_atoms : p ∈ atoms := List.mem_filter.mp hp |>.1
  exact atom_pair_mass_extension_eq a b atoms p hp_atoms

/-- Construct the finite list of cross-grade atoms from authentic active station lists for each grade:
    For distinct grades K ≠ J in G, and active stations n ∈ N_stations K, m ∈ N_stations J,
    the atom (K, J, n, m) is included in the list. -/
def make_cross_grade_atoms (G : List ℤ) (N_stations : ℤ → List ℕ) : List (ℤ × ℤ × ℕ × ℕ) :=
  G.bind (fun K =>
    (G.filter (fun J => decide (J ≠ K))).bind (fun J =>
      (N_stations K).bind (fun n =>
        (N_stations J).map (fun m => (K, J, n, m)))))

/-- Membership of the extremal atom in the authentic cross-grade atom list:
    Given active station lists with n0 ∈ N_stations K_plus and m0 ∈ N_stations K_minus,
    with distinct extremal grades K_plus ≠ K_minus in G,
    the extremal atom (K_plus, K_minus, n0, m0) belongs to make_cross_grade_atoms. -/
theorem extremal_atom_mem_make_cross_grade_atoms
    (G : List ℤ) (N_stations : ℤ → List ℕ)
    (K_plus K_minus : ℤ) (n0 m0 : ℕ)
    (h_Kp : K_plus ∈ G)
    (h_Km : K_minus ∈ G)
    (h_ne : K_minus ≠ K_plus)
    (hn0 : n0 ∈ N_stations K_plus) (hm0 : m0 ∈ N_stations K_minus) :
    (K_plus, K_minus, n0, m0) ∈ make_cross_grade_atoms G N_stations := by
  dsimp [make_cross_grade_atoms]
  rw [List.mem_bind]
  refine ⟨K_plus, h_Kp, ?_⟩
  rw [List.mem_bind]
  have h_filter : K_minus ∈ G.filter (fun J => decide (J ≠ K_plus)) := by
    rw [List.mem_filter]
    exact ⟨h_Km, by simpa using h_ne⟩
  refine ⟨K_minus, h_filter, ?_⟩
  rw [List.mem_bind]
  refine ⟨n0, hn0, ?_⟩
  rw [List.mem_map]
  refine ⟨m0, hm0, rfl⟩

/-- Full Finite Extremal-Grade Correlation Theorem (Support-Restricted Formulation):
    Discharges the global-positivity requirement by applying the canonical extension.
    Requires strictly positive weights ONLY on the active stations occurring in atoms. -/
theorem full_finite_extremal_grade_correlation_theorem_support
    (tau : ℝ) (htau : 0 < tau)
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
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (h_a_supp : ∀ (p : ℤ × ℤ × ℕ × ℕ), p ∈ atoms → 0 < a p.1 p.2.2.1 ∧ 0 < a p.2.1 p.2.2.2)
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
  let a_ext := positive_weight_extension a atoms
  have h_a_ext_pos : ∀ K n, 0 < a_ext K n := positive_weight_extension_pos a atoms h_a_supp
  have h_nu_ext_zero : ∀ y : ℝ, nu_b_mass_at atoms a_ext b tau y = 0 := by
    intro y
    rw [nu_b_mass_at_extension_eq]
    exact h_nu_zero y
  exact full_finite_extremal_grade_correlation_theorem
    tau htau G K_plus K_minus hK_plus hK_minus h_max h_min h_diff_grades
    b hb_plus hb_minus a_ext h_a_ext_pos atoms h_atoms_in_G h_atoms_pos
    n0 m0 hn0 hm0 h_p0_in h_nu_ext_zero

/-- Transcendence hypothesis: no non-zero integer power of tau is rational.
    For tau = 2*pi, this is a consequence of the Lindemann-Weierstrass theorem. -/
def tau_transcendence (tau : ℝ) : Prop :=
  ∀ (k : ℤ), k ≠ 0 → ∀ (r : ℚ), tau ^ k ≠ (r : ℝ)

/-- TC Specialized Extremal Correlation Non-Vanishing Corollary:
    For any scale factor tau > 0 satisfying tau_transcendence tau (specifically tau = 2*pi),
    and any finite set of integer grades G with at least two effective active grades
    (achieving extremal grades K_minus < K_plus with non-zero coefficients b K_plus, b K_minus ≠ 0
    and non-empty active station sets containing n0, m0 > 0 with strictly positive weights on the active support),
    the discrete correlation measure nu_b CANNOT vanish identically:
        (∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0) → False.
    This discharges the measure-to-collision bridge of the TC reductio. -/
theorem tc_extremal_correlation_nonvanishing_corollary
    (tau : ℝ) (htau : 0 < tau)
    (h_trans : tau_transcendence tau)
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
    (atoms : List (ℤ × ℤ × ℕ × ℕ))
    (h_a_supp : ∀ (p : ℤ × ℤ × ℕ × ℕ), p ∈ atoms → 0 < a p.1 p.2.2.1 ∧ 0 < a p.2.1 p.2.2.2)
    (h_atoms_in_G : ∀ p ∈ atoms, p.1 ∈ G ∧ p.2.1 ∈ G)
    (h_atoms_pos : ∀ p ∈ atoms, 0 < p.2.2.1 ∧ 0 < p.2.2.2)
    (n0 m0 : ℕ) (hn0 : 0 < n0) (hm0 : 0 < m0)
    (h_p0_in : (K_plus, K_minus, n0, m0) ∈ atoms)
    (h_nu_zero : ∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0) :
    False := by
  let a_ext := positive_weight_extension a atoms
  have h_a_ext_pos : ∀ K n, 0 < a_ext K n := positive_weight_extension_pos a atoms h_a_supp
  have h_nu_ext_zero : ∀ y : ℝ, nu_b_mass_at atoms a_ext b tau y = 0 := by
    intro y
    rw [nu_b_mass_at_extension_eq]
    exact h_nu_zero y
  exact full_finite_correlation_transcendence_contradiction
    tau htau h_trans G K_plus K_minus hK_plus hK_minus h_max h_min h_diff_grades
    b hb_plus hb_minus a_ext h_a_ext_pos atoms h_atoms_in_G h_atoms_pos
    n0 m0 hn0 hm0 h_p0_in h_nu_ext_zero

#print axioms full_finite_extremal_grade_correlation_theorem
#print axioms full_finite_correlation_transcendence_contradiction
#print axioms full_finite_extremal_grade_correlation_theorem_support
#print axioms tc_extremal_correlation_nonvanishing_corollary

end RiemannScope
