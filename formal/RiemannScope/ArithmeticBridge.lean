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

end RiemannScope
