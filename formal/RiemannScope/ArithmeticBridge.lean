/-
RiemannScope.ArithmeticBridge
Arithmetic radial bridge definitions, covariance countermodel, and weighted positivity firewalls.
Reference: MATH_CONTRACT.md §39, ARITHMETIC_RADIAL_BRIDGE.md
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.BigOperators.Group.List
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import RiemannScope.Basic
import RiemannScope.Grade
import RiemannScope.RadialDefect

set_option linter.unnecessarySeqFocus false

namespace RiemannScope

/-- Non-negativity lemma for zipped product sum of non-negative reals. -/
lemma list_zipWith_mul_nonneg (w l : List ℝ) (hw : ∀ x ∈ w, 0 ≤ x) (hl : ∀ x ∈ l, 0 ≤ x) :
    0 ≤ (List.zipWith (· * ·) w l).sum := by
  induction l generalizing w with
  | nil =>
    simp
  | cons hl_hd hl_tl ih =>
    cases w with
    | nil => simp
    | cons hw_hd hw_tl =>
      simp only [List.zipWith_cons_cons, List.sum_cons]
      have h_hd : 0 ≤ hw_hd * hl_hd := mul_nonneg (hw hw_hd (List.Mem.head _)) (hl hl_hd (List.Mem.head _))
      have hw_tl_all : ∀ x ∈ hw_tl, 0 ≤ x := fun x hx => hw x (List.Mem.tail _ hx)
      have hl_tl_all : ∀ x ∈ hl_tl, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
      have h_tl := ih hw_tl hw_tl_all hl_tl_all
      exact add_nonneg h_hd h_tl

/-- Arbitrary finite-family weighted sum vanishing firewall:
    For any strictly positive weight list w and non-negative defect list l of matching length,
    the weighted sum is zero if and only if every defect is zero. -/
theorem list_weighted_sum_nonneg_eq_zero_iff (w l : List ℝ)
    (hw : ∀ x ∈ w, 0 < x) (hl : ∀ x ∈ l, 0 ≤ x) (hlen : w.length = l.length) :
    (List.zipWith (· * ·) w l).sum = 0 ↔ ∀ x ∈ l, x = 0 := by
  induction l generalizing w with
  | nil =>
    cases w with
    | nil => simp
    | cons hw_hd hw_tl =>
      simp only [List.length_nil, List.length_cons] at hlen
  | cons hl_hd hl_tl ih =>
    cases w with
    | nil =>
      simp only [List.length_nil, List.length_cons] at hlen
    | cons hw_hd hw_tl =>
      simp only [List.zipWith_cons_cons, List.sum_cons, List.mem_cons, forall_eq_or_imp]
      have h_w_pos : 0 < hw_hd := hw hw_hd (List.Mem.head _)
      have h_l_nonneg : 0 ≤ hl_hd := hl hl_hd (List.Mem.head _)
      have hw_tl_all : ∀ x ∈ hw_tl, 0 < x := fun x hx => hw x (List.Mem.tail _ hx)
      have hl_tl_all : ∀ x ∈ hl_tl, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
      have hlen_tl : hw_tl.length = hl_tl.length := by
        simp only [List.length_cons] at hlen
        exact Nat.succ.inj hlen
      have ih' := ih hw_tl hw_tl_all hl_tl_all hlen_tl
      have hw_tl_nonneg : ∀ x ∈ hw_tl, 0 ≤ x := fun x hx => le_of_lt (hw_tl_all x hx)
      have h_prod_nonneg : 0 ≤ hw_hd * hl_hd := mul_nonneg (le_of_lt h_w_pos) h_l_nonneg
      have h_tail_sum_nonneg : 0 ≤ (List.zipWith (· * ·) hw_tl hl_tl).sum :=
        list_zipWith_mul_nonneg hw_tl hl_tl hw_tl_nonneg hl_tl_all
      constructor
      · intro h_sum
        have h_zeroes : hw_hd * hl_hd = 0 ∧ (List.zipWith (· * ·) hw_tl hl_tl).sum = 0 := by
          constructor <;> linarith [h_prod_nonneg, h_tail_sum_nonneg, h_sum]
        have h_hd_zero : hl_hd = 0 := by
          cases mul_eq_zero.mp h_zeroes.1 with
          | inl h => linarith
          | inr h => exact h
        have h_tl_zero := ih'.mp h_zeroes.2
        exact ⟨h_hd_zero, h_tl_zero⟩
      · intro ⟨h_hd_zero, h_tl_zero⟩
        rw [h_hd_zero, mul_zero, zero_add]
        exact ih'.mpr h_tl_zero

/-- Abstract finite off-line zero quartet in standard coordinates s = 1/2 + δ + iγ:
    {1/2 + δ + iγ, 1/2 - δ + iγ, 1/2 + δ - iγ, 1/2 - δ - iγ}. -/
def offlineQuartet (δ γ : ℝ) : Set ℂ :=
  {⟨1 / 2 + δ, γ⟩, ⟨1 / 2 - δ, γ⟩, ⟨1 / 2 + δ, -γ⟩, ⟨1 / 2 - δ, -γ⟩}

/-- The off-line quartet is closed under functional equation reflection s ↦ 1 - s. -/
theorem offlineQuartet_reflection (δ γ : ℝ) :
    ∀ s ∈ offlineQuartet δ γ, (1 - s) ∈ offlineQuartet δ γ := by
  intro s hs
  simp only [offlineQuartet, Set.mem_insert_iff, Set.mem_singleton_iff] at hs ⊢
  rcases hs with rfl | rfl | rfl | rfl
  · right; right; right
    apply Complex.ext <;> dsimp <;> ring
  · right; right; left
    apply Complex.ext <;> dsimp <;> ring
  · right; left
    apply Complex.ext <;> dsimp <;> ring
  · left
    apply Complex.ext <;> dsimp <;> ring

/-- The off-line quartet is closed under complex conjugation s ↦ conj(s). -/
theorem offlineQuartet_conj (δ γ : ℝ) :
    ∀ s ∈ offlineQuartet δ γ, (⟨s.re, -s.im⟩ : ℂ) ∈ offlineQuartet δ γ := by
  intro s hs
  simp only [offlineQuartet, Set.mem_insert_iff, Set.mem_singleton_iff] at hs ⊢
  rcases hs with rfl | rfl | rfl | rfl
  · right; right; left
    rfl
  · right; right; right
    rfl
  · left
    apply Complex.ext <;> dsimp <;> ring
  · right; left
    apply Complex.ext <;> dsimp <;> ring

/-- The off-line quartet contains an off-line zero whenever δ ≠ 0. -/
theorem offlineQuartet_has_offline_zero (δ γ : ℝ) (hδ : δ ≠ 0) :
    ∃ s ∈ offlineQuartet δ γ, s.re ≠ 1 / 2 := by
  use ⟨1 / 2 + δ, γ⟩
  constructor
  · simp only [offlineQuartet, Set.mem_insert_iff, true_or]
  · dsimp
    intro h_eq
    have : δ = 0 := by linarith [h_eq]
    exact hδ this

/-- Covariance Countermodel Theorem:
    Functional equation reflection, conjugation, and grade transport symmetries
    are jointly compatible with the existence of off-line zeros (δ ≠ 0). -/
theorem covariance_countermodel_offline_compatible (δ γ : ℝ) (hδ : δ ≠ 0) :
    (∀ s ∈ offlineQuartet δ γ, (1 - s) ∈ offlineQuartet δ γ) ∧
    (∀ s ∈ offlineQuartet δ γ, (⟨s.re, -s.im⟩ : ℂ) ∈ offlineQuartet δ γ) ∧
    (∃ s ∈ offlineQuartet δ γ, s.re ≠ 1 / 2) := by
  refine ⟨offlineQuartet_reflection δ γ, offlineQuartet_conj δ γ, offlineQuartet_has_offline_zero δ γ hδ⟩

/-- Explicitly conditional arithmetic radial bridge structure.
    Represents a hypothetical divisor-independent arithmetic evaluator matching a positive spectral sum. -/
structure ConditionalArithmeticRadialBridge where
  zero_defects : List ℝ
  nonneg_defects : ∀ r ∈ zero_defects, 0 ≤ r
  arithmetic_eval : ℤ → ℝ
  spectral_eval : ℝ
  bridge_identity : ∀ K : ℤ, arithmetic_eval K = spectral_eval
  spectral_expansion : spectral_eval = zero_defects.sum
  arithmetic_anchor : ∃ K : ℤ, arithmetic_eval K = 0

/-- Conditional Bridge Rigidity Theorem:
    Under any valid ConditionalArithmeticRadialBridge, every represented zero defect vanishes (r = 0). -/
theorem ConditionalArithmeticRadialBridge.all_defects_zero
    (B : ConditionalArithmeticRadialBridge) :
    ∀ r ∈ B.zero_defects, r = 0 := by
  rcases B.arithmetic_anchor with ⟨K0, hK0⟩
  have h_spec : B.spectral_eval = 0 := by
    rw [← B.bridge_identity K0, hK0]
  have h_sum_zero : B.zero_defects.sum = 0 := by
    rw [← B.spectral_expansion, h_spec]
  exact (list_sum_nonneg_eq_zero_iff B.zero_defects B.nonneg_defects).mp h_sum_zero

/-- Arbitrary finite-family sum of squares for a list of real numbers. -/
def list_sum_sq (l : List ℝ) : ℝ :=
  (l.map (fun x => x ^ 2)).sum

/-- Arbitrary finite-family double sum of squared pair displacements (x + y)^2 over a list l. -/
def list_pairs_sq_sum (l : List ℝ) : ℝ :=
  (l.map (fun x => (l.map (fun y => (x + y) ^ 2)).sum)).sum

/-- Lemma: Inner sum of squared pairs with fixed x evaluates to (length * x^2 + 2 * x * sum + sum_sq). -/
lemma list_map_add_sq_sum (x : ℝ) (l : List ℝ) :
    (l.map (fun y => (x + y) ^ 2)).sum = (l.length : ℝ) * x ^ 2 + 2 * x * l.sum + list_sum_sq l := by
  induction l with
  | nil =>
    simp [list_sum_sq]
  | cons y tl ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    dsimp [list_sum_sq] at ih ⊢
    simp only [List.sum_cons]
    rw [ih]
    push_cast
    ring

/-- Lemma: Distributing a linear-quadratic form A * x^2 + B * x + C over a list l. -/
lemma list_map_quad_sum (A B C : ℝ) (l : List ℝ) :
    (l.map (fun x => A * x ^ 2 + B * x + C)).sum = A * list_sum_sq l + B * l.sum + (l.length : ℝ) * C := by
  induction l with
  | nil =>
    simp [list_sum_sq]
  | cons x tl ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    dsimp [list_sum_sq] at ih ⊢
    simp only [List.sum_cons]
    rw [ih]
    push_cast
    ring

/-- Arbitrary Finite Curvature Algebraic Identity:
    For any finite list l of real displacements, the double sum of all squared pair displacements
    evaluates identically to 2 * N * sum(d_i^2) + 2 * (sum d_i)^2. -/
theorem list_pairs_sq_sum_eq (l : List ℝ) :
    list_pairs_sq_sum l = 2 * (l.length : ℝ) * list_sum_sq l + 2 * (l.sum) ^ 2 := by
  dsimp [list_pairs_sq_sum]
  have h_inner : (fun x => (l.map (fun y => (x + y) ^ 2)).sum) =
                 (fun x => (l.length : ℝ) * x ^ 2 + (2 * l.sum) * x + list_sum_sq l) := by
    funext x
    have h1 := list_map_add_sq_sum x l
    have h2 : 2 * x * l.sum = (2 * l.sum) * x := by ring
    rw [h2] at h1
    exact h1
  rw [h_inner]
  have h_quad := list_map_quad_sum (l.length : ℝ) (2 * l.sum) (list_sum_sq l) l
  rw [h_quad]
  push_cast
  ring

/-- Arbitrary finite curvature reflection-symmetric reduction:
    When the family satisfies reflection symmetry (l.sum = 0), the double sum simplifies to
    2 * N * sum(d_i^2). -/
theorem list_pairs_sq_sum_symmetric (l : List ℝ) (h_sym : l.sum = 0) :
    list_pairs_sq_sum l = 2 * (l.length : ℝ) * list_sum_sq l := by
  have h_id := list_pairs_sq_sum_eq l
  rw [h_sym] at h_id
  linarith [h_id]

/-- List sum of squares is unconditionally non-negative. -/
lemma list_sum_sq_nonneg (l : List ℝ) : 0 ≤ list_sum_sq l := by
  induction l with
  | nil => simp [list_sum_sq]
  | cons x tl ih =>
    simp only [list_sum_sq, List.map_cons, List.sum_cons]
    have hx : 0 ≤ x ^ 2 := sq_nonneg x
    exact add_nonneg hx ih

/-- List sum vanishes if all elements are zero. -/
lemma list_sum_eq_zero_of_all_zero (l : List ℝ) (h : ∀ x ∈ l, x = (0 : ℝ)) : l.sum = 0 := by
  induction l with
  | nil => simp
  | cons x tl ih =>
    simp only [List.mem_cons, forall_eq_or_imp] at h
    simp only [List.sum_cons, h.1, zero_add]
    exact ih h.2

/-- List sum of squares vanishes if and only if every element is zero. -/
lemma list_sum_sq_eq_zero_iff (l : List ℝ) : list_sum_sq l = 0 ↔ ∀ x ∈ l, x = 0 := by
  induction l with
  | nil => simp [list_sum_sq]
  | cons x tl ih =>
    simp only [list_sum_sq, List.map_cons, List.sum_cons, List.mem_cons, forall_eq_or_imp]
    have hx : 0 ≤ x ^ 2 := sq_nonneg x
    have htl : 0 ≤ list_sum_sq tl := list_sum_sq_nonneg tl
    constructor
    · intro h
      have h_sum : x ^ 2 + list_sum_sq tl = 0 := h
      have hx0 : x ^ 2 = 0 := by linarith [hx, htl, h_sum]
      have htl0 : list_sum_sq tl = 0 := by linarith [hx, htl, h_sum]
      have hx_zero : x = 0 := sq_eq_zero_iff.mp hx0
      have htl_zero := ih.mp htl0
      exact ⟨hx_zero, htl_zero⟩
    · intro ⟨hx0, htl0⟩
      rw [hx0, sq, mul_zero, zero_add]
      exact ih.mpr htl0

/-- Arbitrary finite curvature is unconditionally non-negative. -/
theorem list_pairs_sq_sum_nonneg (l : List ℝ) : 0 ≤ list_pairs_sq_sum l := by
  rw [list_pairs_sq_sum_eq]
  have : 0 ≤ list_sum_sq l := list_sum_sq_nonneg l
  positivity

/-- Arbitrary finite curvature zero-rigidity for a non-empty family (l.length > 0):
    The double sum of squared pair displacements vanishes if and only if every displacement d_i = 0. -/
theorem list_pairs_sq_sum_eq_zero_iff (l : List ℝ) (hlen : 0 < l.length) :
    list_pairs_sq_sum l = 0 ↔ ∀ x ∈ l, x = 0 := by
  rw [list_pairs_sq_sum_eq]
  have h_len_pos : 0 < (l.length : ℝ) := Nat.cast_pos.mpr hlen
  have h_sq_nonneg : 0 ≤ list_sum_sq l := list_sum_sq_nonneg l
  have h_term1_nonneg : 0 ≤ 2 * (l.length : ℝ) * list_sum_sq l := by positivity
  have h_term2_nonneg : 0 ≤ 2 * (l.sum) ^ 2 := by positivity
  constructor
  · intro h
    have h_parts1 : 2 * (l.length : ℝ) * list_sum_sq l = 0 := by linarith [h_term1_nonneg, h_term2_nonneg, h]
    have h_coeff : (2 * (l.length : ℝ)) ≠ 0 := by linarith [h_len_pos]
    have h_sq_zero : list_sum_sq l = 0 := by
      cases mul_eq_zero.mp h_parts1 with
      | inl h1 => contradiction
      | inr h2 => exact h2
    exact list_sum_sq_eq_zero_iff l |>.mp h_sq_zero
  · intro h_all
    have h_sq_zero : list_sum_sq l = 0 := list_sum_sq_eq_zero_iff l |>.mpr h_all
    have h_sum_zero : l.sum = 0 := list_sum_eq_zero_of_all_zero l h_all
    rw [h_sq_zero, h_sum_zero]
    ring

/-- 2-term symmetric radial curvature algebraic identity:
    (d1 + d1)^2 + (d1 + d2)^2 + (d2 + d1)^2 + (d2 + d2)^2 = 2 * 2 * (d1^2 + d2^2) + 2 * (d1 + d2)^2. -/
theorem sum_pairs_sq_two_terms (d1 d2 : ℝ) :
    (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 =
    2 * 2 * (d1 ^ 2 + d2 ^ 2) + 2 * (d1 + d2) ^ 2 := by
  ring

/-- 2-term curvature sum of squares is unconditionally non-negative. -/
theorem sum_pairs_sq_two_nonneg (d1 d2 : ℝ) :
    0 ≤ (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 := by
  positivity

/-- 2-term curvature zero-rigidity:
    The sum of squared pair displacements vanishes if and only if every displacement d_a = 0. -/
theorem sum_pairs_sq_two_eq_zero_iff (d1 d2 : ℝ) :
    (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 = 0 ↔ d1 = 0 ∧ d2 = 0 := by
  constructor
  · intro h
    have h1 : (d1 + d1) ^ 2 ≤ (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 := by
      have : 0 ≤ (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 := by positivity
      linarith
    have hd1_sq : (d1 + d1) ^ 2 ≤ 0 := by linarith [h, h1]
    have hd1_nonneg : 0 ≤ (d1 + d1) ^ 2 := sq_nonneg _
    have hd1_eq : (d1 + d1) ^ 2 = 0 := le_antisymm hd1_sq hd1_nonneg
    have hd1_zero : d1 + d1 = 0 := sq_eq_zero_iff.mp hd1_eq

    have h2 : (d2 + d2) ^ 2 ≤ (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 := by
      have : 0 ≤ (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 := by positivity
      linarith
    have hd2_sq : (d2 + d2) ^ 2 ≤ 0 := by linarith [h, h2]
    have hd2_nonneg : 0 ≤ (d2 + d2) ^ 2 := sq_nonneg _
    have hd2_eq : (d2 + d2) ^ 2 = 0 := le_antisymm hd2_sq hd2_nonneg
    have hd2_zero : d2 + d2 = 0 := sq_eq_zero_iff.mp hd2_eq
    constructor <;> linarith
  · rintro ⟨rfl, rfl⟩
    ring

/-- 2-term reflection pair curvature theorem under d1 + d2 = 0:
    The pair sum of squared displacements equals 2 * N * (d1^2 + d2^2) = 4 * (d1^2 + d2^2) = 8 * d1^2. -/
theorem curvature_pair_symmetric (d1 d2 : ℝ) (h_sum : d1 + d2 = 0) :
    (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d2 + d1) ^ 2 + (d2 + d2) ^ 2 =
    2 * 2 * (d1 ^ 2 + d2 ^ 2) := by
  have h_id := sum_pairs_sq_two_terms d1 d2
  rw [h_sum] at h_id
  linarith [h_id]

/-- 4-term symmetric radial curvature algebraic identity:
    The double sum of all pairs (d_a + d_b)^2 equals 2 * 4 * sum(d_a^2) + 2 * (sum d_a)^2. -/
theorem sum_pairs_sq_four_terms (d1 d2 d3 d4 : ℝ) :
    (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d1 + d3) ^ 2 + (d1 + d4) ^ 2 +
    (d2 + d1) ^ 2 + (d2 + d2) ^ 2 + (d2 + d3) ^ 2 + (d2 + d4) ^ 2 +
    (d3 + d1) ^ 2 + (d3 + d2) ^ 2 + (d3 + d3) ^ 2 + (d3 + d4) ^ 2 +
    (d4 + d1) ^ 2 + (d4 + d2) ^ 2 + (d4 + d3) ^ 2 + (d4 + d4) ^ 2 =
    2 * 4 * (d1 ^ 2 + d2 ^ 2 + d3 ^ 2 + d4 ^ 2) + 2 * (d1 + d2 + d3 + d4) ^ 2 := by
  ring

/-- 4-term symmetry-complete quartet curvature theorem under d1 + d2 + d3 + d4 = 0:
    The double sum of squared displacements evaluates exactly to 2 * 4 * sum(d_a^2) = 8 * sum(d_a^2). -/
theorem curvature_quartet_symmetric (d1 d2 d3 d4 : ℝ) (h_sum : d1 + d2 + d3 + d4 = 0) :
    (d1 + d1) ^ 2 + (d1 + d2) ^ 2 + (d1 + d3) ^ 2 + (d1 + d4) ^ 2 +
    (d2 + d1) ^ 2 + (d2 + d2) ^ 2 + (d2 + d3) ^ 2 + (d2 + d4) ^ 2 +
    (d3 + d1) ^ 2 + (d3 + d2) ^ 2 + (d3 + d3) ^ 2 + (d3 + d4) ^ 2 +
    (d4 + d1) ^ 2 + (d4 + d2) ^ 2 + (d4 + d3) ^ 2 + (d4 + d4) ^ 2 =
    2 * 4 * (d1 ^ 2 + d2 ^ 2 + d3 ^ 2 + d4 ^ 2) := by
  have h_id := sum_pairs_sq_four_terms d1 d2 d3 d4
  rw [h_sum] at h_id
  linarith [h_id]

/-- Single upper-half-plane frequency fibre {δ, -δ} at ordinate γ > 0 (multiplicity n=1, N=2):
    Evaluates to 8 * δ^2, strictly positive whenever δ ≠ 0. -/
theorem upper_fibre_simple_quartet_curvature_val (δ : ℝ) :
    (δ + δ) ^ 2 + (δ + -δ) ^ 2 + (-δ + δ) ^ 2 + (-δ + -δ) ^ 2 = 8 * δ ^ 2 := by
  ring

/-- Multiplicity-n upper-half-plane fibre {n*δ, n*(-δ)} has N = 2n and evaluates to 8 * n^2 * δ^2.
    For n=2 (N=4), evaluates to 32 * δ^2. -/
theorem upper_fibre_multiplicity_two_curvature_val (δ : ℝ) :
    (δ + δ) ^ 2 + (δ + δ) ^ 2 + (δ + -δ) ^ 2 + (δ + -δ) ^ 2 +
    (δ + δ) ^ 2 + (δ + δ) ^ 2 + (δ + -δ) ^ 2 + (δ + -δ) ^ 2 +
    (-δ + δ) ^ 2 + (-δ + δ) ^ 2 + (-δ + -δ) ^ 2 + (-δ + -δ) ^ 2 +
    (-δ + δ) ^ 2 + (-δ + δ) ^ 2 + (-δ + -δ) ^ 2 + (-δ + -δ) ^ 2 =
    32 * δ ^ 2 := by
  ring

/-- Normalized fibre curvature identity for simple upper-half-plane fibre (N = 2):
    C_γ = M_γ''(0) / (2 * N) = (8 * δ^2) / (2 * 2) = 2 * δ^2 = δ^2 + (-δ)^2. -/
theorem normalized_fibre_curvature_simple (δ : ℝ) :
    (8 * δ ^ 2) / (2 * 2) = δ ^ 2 + (-δ) ^ 2 := by
  ring

/-- Structure representing a hypothetical divisor-independent separated sesquilinear signal bridge.
    Models an arithmetic evaluator A_K''(0) matching the spectral second radial derivative M_K''(0). -/
structure ConditionalSeparatedSignalBridge where
    radial_variances : List ℝ
    nonneg_variances : ∀ v ∈ radial_variances, 0 ≤ v
    weights : List ℝ
    pos_weights : ∀ w ∈ weights, 0 < w
    lengths_match : weights.length = radial_variances.length
    arithmetic_curvature_eval : ℤ → ℝ
    spectral_curvature_eval : ℝ
    bridge_identity : ∀ K : ℤ, arithmetic_curvature_eval K = spectral_curvature_eval
    spectral_expansion : spectral_curvature_eval = (List.zipWith (· * ·) weights radial_variances).sum
    arithmetic_anchor : ∃ K : ℤ, arithmetic_curvature_eval K = 0

/-- Separated Signal Bridge Rigidity Theorem:
    Under any valid ConditionalSeparatedSignalBridge with arithmetic vanishing anchor,
    every represented radial variance vanishes (v_γ = 0), forcing all represented radial displacements δ = 0. -/
theorem ConditionalSeparatedSignalBridge.all_variances_zero
    (B : ConditionalSeparatedSignalBridge) :
    ∀ v ∈ B.radial_variances, v = 0 := by
  rcases B.arithmetic_anchor with ⟨K0, hK0⟩
  have h_spec : B.spectral_curvature_eval = 0 := by
    rw [← B.bridge_identity K0, hK0]
  have h_sum_zero : (List.zipWith (· * ·) B.weights B.radial_variances).sum = 0 := by
    rw [← B.spectral_expansion, h_spec]
  exact (list_weighted_sum_nonneg_eq_zero_iff B.weights B.radial_variances B.pos_weights B.nonneg_variances B.lengths_match).mp h_sum_zero

/-- Generic Scale Dilation Cancellation Theorem:
    For any non-zero real scale, if D_s(x) = s^(-1) * f(s^(-1) * x),
    then scale * D_s(scale * u) = f(u) identically. -/
theorem generic_scale_dilation_cancellation
    (scale : ℝ) (h_pos : 0 < scale)
    (f : ℝ → ℝ) (D : ℝ → ℝ)
    (h_dil : ∀ s, D s = (1 / scale) * f ((1 / scale) * s))
    (u : ℝ) :
    scale * D (scale * u) = f u := by
  rw [h_dil (scale * u)]
  have h_pos_ne : scale ≠ 0 := ne_of_gt h_pos
  have h_cancel_arg : 1 / scale * (scale * u) = u := by
    rw [← mul_assoc, one_div_mul_cancel h_pos_ne, one_mul]
  rw [h_cancel_arg]
  have h_cancel_outer : scale * (1 / scale * f u) = (scale * (1 / scale)) * f u := by ring
  rw [h_cancel_outer, mul_one_div_cancel h_pos_ne, one_mul]

/-- Explicitly conditional completed logarithmic derivative decomposition interface.
    NOTE: The field identity_on_domain models the analytic identity P(u) = A(u) - ξ'/ξ(u)
    which is proved analytically in research documentation on Re(u) > 1, not proved inside Lean. -/
structure ConditionalCompletedLogDerivativeDecomposition where
    scale : ℝ
    pos_scale : 0 < scale
    xi_log_der : ℝ → ℝ
    archimedean_A : ℝ → ℝ
    prime_P : ℝ → ℝ
    identity_on_domain : ∀ u, prime_P u = archimedean_A u - xi_log_der u
    dilated_D : ℝ → ℝ
    dilation_def : ∀ s, dilated_D s = (1 / scale) * xi_log_der ((1 / scale) * s)

/-- Theorem: The normalized dilated completed logarithmic derivative scale * D_K(scale * u)
    recovers ξ'/ξ(u) identically, proving strict coordinate redundancy across grades. -/
theorem ConditionalCompletedLogDerivativeDecomposition.coordinate_redundant
    (D : ConditionalCompletedLogDerivativeDecomposition) (u : ℝ) :
    D.scale * D.dilated_D (D.scale * u) = D.xi_log_der u := by
  exact generic_scale_dilation_cancellation D.scale D.pos_scale D.xi_log_der D.dilated_D D.dilation_def u

/-- Real algebraic identity for finite windowed quadratic expansion:
    (A - Z)^2 = A^2 - 2*A*Z + Z^2. -/
theorem finite_quadratic_expansion_identity (A Z : ℝ) :
    (A - Z)^2 = A^2 - 2 * A * Z + Z^2 := by
  ring

/-- General algebraic 4-term decomposition of quadratic difference:
    (A - Z)^2 = A*A - A*Z - Z*A + Z*Z. -/
theorem finite_quadratic_four_term_decomposition (A Z : ℝ) :
    (A - Z)^2 = A * A - A * Z - Z * A + Z * Z := by
  ring

/-- Complex algebraic 4-term decomposition of quadratic difference under conjugation:
    (A - Z) * star(A - Z) = A*star(A) - A*star(Z) - Z*star(A) + Z*star(Z). -/
theorem complex_quadratic_four_term_expansion (A Z : ℂ) :
    (A - Z) * star (A - Z) =
      A * star A - A * star Z - Z * star A + Z * star Z := by
  simp only [star_sub]
  ring

/-- Exact algebraic identity for radial defect difference numerator:
    (u - δ²)*u - ((u - δ²)² + 4*δ²*γ²) = δ²*(u - 4*γ² - δ²).
    When u = z² + γ², this yields the exact numerator factor 4*z*δ²*(z² - 3*γ² - δ²). -/
theorem radial_defect_difference_numerator (u d2 gam2 : ℝ) :
    (u - d2) * u - ((u - d2)^2 + 4 * d2 * gam2) = d2 * (u - 4 * gam2 - d2) := by
  ring

/-- Exact algebraic numerator expansion for second-order radial response coefficient:
    4*z*δ²*(z² - 3*γ² - δ²) = 4*z*δ²*(z² - 3*γ²) - 4*z*δ⁴. -/
theorem radial_second_order_numerator_decomposition (z gam d : ℝ) :
    4 * z * d^2 * (z^2 - 3 * gam^2 - d^2) = 4 * z * d^2 * (z^2 - 3 * gam^2) - 4 * z * d^4 := by
  ring

/-- Sequence countermodel witness for cofinal limit distinction:
    For f(H, n) = H / (n + 1), along the diagonal schedule H(n) = n + 1,
    the sequence is identically 1 for all n, distinct from the pointwise limit 0 at any fixed H. -/
theorem cofinal_sequence_diagonal_witness (n : ℕ) :
    ((n : ℝ) + 1) / ((n : ℝ) + 1) = 1 := by
  have h_ne : (n : ℝ) + 1 ≠ 0 := by linarith
  exact div_self h_ne

/-- Elementary cofinal limit distinction countermodel (pointwise algebraic witness):
    For f(H, T) = H / T, under proportional cofinal schedule H(T) = c * T (c ≠ 0),
    the ratio f(c*T, T) = c is constant and non-zero for all T ≠ 0. -/
theorem cofinal_schedule_distinct_from_fixed_limit
    (c : ℝ) (T : ℝ) (hT : T ≠ 0) :
    (c * T) / T = c := by
  exact mul_div_cancel_right₀ c hT

/-- Explicitly conditional structure representing a hypothetical regularized infinite spectral bridge at Gate G4.
    Models the passage of finite CMSA expansion under windowing and scaling c_T to an exact positive radial-defect functional. -/
structure ConditionalG4RegularizedBridge where
    defects : List ℝ
    nonneg_defects : ∀ d ∈ defects, 0 ≤ d
    weights : List ℝ
    pos_weights : ∀ w ∈ weights, 0 < w
    lengths_match : weights.length = defects.length
    arithmetic_regularized_anchor : ℝ
    spectral_regularized_limit : ℝ
    g4_limit_bridge_identity : arithmetic_regularized_anchor = spectral_regularized_limit
    g4_spectral_reduction : spectral_regularized_limit = (List.zipWith (· * ·) weights defects).sum
    g4_arithmetic_anchor_zero : arithmetic_regularized_anchor = 0

/-- Gate G4 Regularized Bridge Rigidity Theorem:
    Under any valid ConditionalG4RegularizedBridge with zero arithmetic anchor,
    every represented radial defect vanishes (d_j = 0), forcing all represented zeros to lie on the critical line. -/
theorem ConditionalG4RegularizedBridge.all_defects_zero
    (B : ConditionalG4RegularizedBridge) :
    ∀ d ∈ B.defects, d = 0 := by
  have h_spec : B.spectral_regularized_limit = 0 := by
    rw [← B.g4_limit_bridge_identity, B.g4_arithmetic_anchor_zero]
  have h_sum_zero : (List.zipWith (· * ·) B.weights B.defects).sum = 0 := by
    rw [← B.g4_spectral_reduction, h_spec]
  exact (list_weighted_sum_nonneg_eq_zero_iff B.weights B.defects B.pos_weights B.nonneg_defects B.lengths_match).mp h_sum_zero

end RiemannScope

