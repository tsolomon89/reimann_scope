/-
RiemannScope.ZeroCharacter
Generic-base zero character modulus: |q_b(rho)^K| = b^(K * delta).
Reference: docs/LEAN_FORMALIZATION_PLAN.md §11
-/

import Mathlib.Analysis.SpecialFunctions.Complex.Exp
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace RiemannScope

/-- Multiplicative zero-character generator for base b > 1:
    q_b(s) = exp((s - 1/2) * log b) -/
noncomputable def zeroCharacter (b : ℝ) (s : ℂ) : ℂ :=
  Complex.exp ((s - ⟨1 / 2, 0⟩) * (Real.log b : ℂ))

/-- Modulus of single zero-character: |q_b(1/2 + delta + i*gamma)| = b^delta -/
theorem zeroCharacter_abs (b δ γ : ℝ) (hb : 0 < b) :
    Complex.abs (zeroCharacter b ⟨1 / 2 + δ, γ⟩) = b ^ δ := by
  dsimp [zeroCharacter]
  have h_arg : (⟨1 / 2 + δ, γ⟩ : ℂ) - ⟨1 / 2, 0⟩ = ⟨δ, γ⟩ := by
    ext <;> simp <;> ring
  rw [h_arg]
  have h_prod : (⟨δ, γ⟩ : ℂ) * (Real.log b : ℂ) = ⟨δ * Real.log b, γ * Real.log b⟩ := by
    ext <;> simp <;> ring
  rw [h_prod, Complex.abs_exp]
  dsimp
  rw [Real.exp_mul, Real.exp_log hb]

end RiemannScope
