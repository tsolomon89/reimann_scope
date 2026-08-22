/-
RiemannScope.Contradiction
Conditional contradiction skeleton for radial leaf rigidity closed via functional equation reflection.
Reference: MATH_CONTRACT.md §8, DECISIONS.md
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace RiemannScope

/-- Radial displacement delta(s) = Re(s) - 1/2 -/
noncomputable def radialDelta (s : ℂ) : ℝ :=
  s.re - 1 / 2

/-- Functional equation reflection s ↦ 1 - s negates the radial coordinate:
    radialDelta (1 - s) = - radialDelta s -/
theorem radialDelta_reflection (s : ℂ) :
    radialDelta (1 - s) = - radialDelta s := by
  dsimp [radialDelta]
  simp
  ring

/-- Conditional Reflection Theorem:
    If a non-empty zero spectrum S is closed under reflection s ↦ 1 - s,
    and all zeros in S share a common radial coordinate delta_0 (radial rigidity),
    then delta_0 must equal 0, so every zero in S is strictly on the critical line. -/
theorem radial_rigidity_reflection_forces_critical_line
    (S : Set ℂ)
    (h_nonempty : S.Nonempty)
    (h_reflection : ∀ s ∈ S, (1 - s) ∈ S)
    (delta_0 : ℝ)
    (h_rigidity : ∀ s ∈ S, radialDelta s = delta_0) :
    delta_0 = 0 ∧ (∀ s ∈ S, s.re = 1 / 2) := by
  rcases h_nonempty with ⟨s0, hs0⟩
  have h_refl_in : (1 - s0) ∈ S := h_reflection s0 hs0
  have h1 : radialDelta s0 = delta_0 := h_rigidity s0 hs0
  have h2 : radialDelta (1 - s0) = delta_0 := h_rigidity (1 - s0) h_refl_in
  have h3 : radialDelta (1 - s0) = - radialDelta s0 := radialDelta_reflection s0
  rw [h1] at h3
  have h_zero : delta_0 = 0 := by linarith [h2, h3]
  constructor
  · exact h_zero
  · intro s hs
    have hs_del : radialDelta s = delta_0 := h_rigidity s hs
    rw [h_zero] at hs_del
    dsimp [radialDelta] at hs_del
    linarith


/-- Contradiction corollary: Under reflection symmetry and radial rigidity,
    the existence of an off-line zero (s.re ≠ 1/2) is impossible. -/
theorem radial_rigidity_offline_zero_contradiction
    (S : Set ℂ)
    (h_nonempty : S.Nonempty)
    (h_reflection : ∀ s ∈ S, (1 - s) ∈ S)
    (delta_0 : ℝ)
    (h_rigidity : ∀ s ∈ S, radialDelta s = delta_0)
    (s_off : ℂ)
    (hs_off : s_off ∈ S)
    (h_not_online : s_off.re ≠ 1 / 2) :
    False := by
  have ⟨_, h_all_online⟩ := radial_rigidity_reflection_forces_critical_line S h_nonempty h_reflection delta_0 h_rigidity
  have h_online : s_off.re = 1 / 2 := h_all_online s_off hs_off
  exact h_not_online h_online

end RiemannScope
