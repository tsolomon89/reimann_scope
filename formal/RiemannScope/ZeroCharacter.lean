/-
RiemannScope.ZeroCharacter
Generic-base zero character modulus: |q_b(rho)^K| = b^(K * delta).
Reference: MATH_CONTRACT.md §11
-/

import Mathlib.Data.Complex.Exponential
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
    apply Complex.ext <;> simp
  rw [h_arg]
  have h_prod : (⟨δ, γ⟩ : ℂ) * (Real.log b : ℂ) = ⟨δ * Real.log b, γ * Real.log b⟩ := by
    apply Complex.ext <;> simp
  rw [h_prod, Complex.abs_exp]
  dsimp
  have h_exp : Real.exp (δ * Real.log b) = Real.exp (Real.log b * δ) := by
    ring_nf
  rw [h_exp]
  exact (Real.rpow_def_of_pos hb δ).symm

end RiemannScope
