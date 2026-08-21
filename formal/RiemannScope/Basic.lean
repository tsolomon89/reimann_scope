/-
RiemannScope.Basic
Exact coordinate transforms: origin dilation and centered coordinate dilation.
Reference: docs/LEAN_FORMALIZATION_PLAN.md §3, §4
-/

import Mathlib.Data.Complex.Basic

namespace RiemannScope

/-- Origin dilation by real scale A > 0: T_A(s) = A * s -/
def originDilation (A : ℝ) (s : ℂ) : ℂ :=
  (A : ℂ) * s

theorem originDilation_apply (A δ γ : ℝ) :
    originDilation A (⟨1 / 2 + δ, γ⟩ : ℂ) = ⟨A / 2 + A * δ, A * γ⟩ := by
  dsimp [originDilation]
  ext
  · simp [mul_add, add_mul]
    ring
  · simp [mul_add]
    ring

theorem originDilation_critical_line (A γ : ℝ) :
    (originDilation A ⟨1 / 2, γ⟩).re = A / 2 := by
  dsimp [originDilation]
  simp

/-- Centered coordinate dilation: C_A(s) = 1/2 + A * (s - 1/2) -/
def centeredDilation (A : ℝ) (s : ℂ) : ℂ :=
  ⟨1 / 2, 0⟩ + (A : ℂ) * (s - ⟨1 / 2, 0⟩)

theorem centeredDilation_apply (A δ γ : ℝ) :
    centeredDilation A ⟨1 / 2 + δ, γ⟩ = ⟨1 / 2 + A * δ, A * γ⟩ := by
  dsimp [centeredDilation]
  ext
  · simp
    ring
  · simp
    ring

theorem centeredDilation_fixes_critical_line (A γ : ℝ) :
    (centeredDilation A ⟨1 / 2, γ⟩).re = 1 / 2 := by
  dsimp [centeredDilation]
  simp

end RiemannScope
