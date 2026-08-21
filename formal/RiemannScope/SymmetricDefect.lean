/-
RiemannScope.SymmetricDefect
Symmetric grade defect formula for off-line zero pairs:
D_K = q_+^K + q_-^K - 2 * q_0^K.
Reference: docs/LEAN_FORMALIZATION_PLAN.md §12
-/

import RiemannScope.ZeroCharacter

namespace RiemannScope

/-- Symmetric grade defect for off-line perturbation quartet -/
noncomputable def symmetricGradeDefect (b : ℝ) (K : ℤ) (δ γ : ℝ) : ℂ :=
  (zeroCharacter b ⟨1 / 2 + δ, γ⟩) ^ K + (zeroCharacter b ⟨1 / 2 - δ, γ⟩) ^ K - 2 * (zeroCharacter b ⟨1 / 2, γ⟩) ^ K

/-- When delta = 0 (on-line zero), symmetric defect vanishes identically -/
theorem symmetricGradeDefect_zero_delta (b : ℝ) (K : ℤ) (γ : ℝ) :
    symmetricGradeDefect b K 0 γ = 0 := by
  dsimp [symmetricGradeDefect]
  have h_same : (zeroCharacter b ⟨1 / 2 + 0, γ⟩) = (zeroCharacter b ⟨1 / 2, γ⟩) := by
    simp
  have h_same2 : (zeroCharacter b ⟨1 / 2 - 0, γ⟩) = (zeroCharacter b ⟨1 / 2, γ⟩) := by
    simp
  rw [h_same, h_same2]
  ring

end RiemannScope
