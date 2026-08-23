/-
RiemannScope.RadialDefect
Radial projection operator, defect divisor, and second-order orbit energy.
Reference: MATH_CONTRACT.md §36
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace RiemannScope

/-- Radial projection operator sending s = 1/2 + δ + iγ to 1/2 + iγ on the critical line. -/
noncomputable def radialProjection (s : ℂ) : ℂ :=
  ⟨1 / 2, s.im⟩

/-- Radial projection projects critical-line points to themselves. -/
theorem radialProjection_on_line (γ : ℝ) :
    radialProjection ⟨1 / 2, γ⟩ = ⟨1 / 2, γ⟩ := by
  dsimp [radialProjection]

/-- Radial defect of a complex point under a test function h : ℂ → ℂ. -/
noncomputable def radialPointDefect (h : ℂ → ℂ) (s : ℂ) : ℂ :=
  h s - h (radialProjection s)

/-- Pure radial defect for a symmetry-complete quartet {1/2 ± δ ± iγ} with respect to h.
    For an even function h(t), the 4-point sum evaluates to:
    h(γ + iδ) + h(-γ - iδ) + h(γ - iδ) + h(-γ + iδ) - 2(h(γ) + h(-γ)). -/
noncomputable def pureRadialDefectQuartet (h : ℂ → ℂ) (δ γ : ℝ) : ℂ :=
  h ⟨γ, δ⟩ + h ⟨-γ, -δ⟩ + h ⟨γ, -δ⟩ + h ⟨-γ, δ⟩ - 2 * (h ⟨γ, 0⟩ + h ⟨-γ, 0⟩)

/-- When δ = 0, pure radial quartet defect vanishes identically. -/
theorem pureRadialDefectQuartet_zero_delta (h : ℂ → ℂ) (γ : ℝ) :
    pureRadialDefectQuartet h 0 γ = 0 := by
  dsimp [pureRadialDefectQuartet]
  have h1 : (⟨γ, (0:ℝ)⟩ : ℂ) = ⟨γ, 0⟩ := rfl
  have h2 : (⟨-γ, (-0:ℝ)⟩ : ℂ) = ⟨-γ, 0⟩ := by simp
  have h3 : (⟨γ, (-0:ℝ)⟩ : ℂ) = ⟨γ, 0⟩ := by simp
  have h4 : (⟨-γ, (0:ℝ)⟩ : ℂ) = ⟨-γ, 0⟩ := rfl
  rw [h1, h2, h3, h4]
  ring

/-- Second-order orbit variable u = δ^2 is non-negative for any real displacement δ. -/
theorem second_order_orbit_variable_nonneg (δ : ℝ) :
    0 ≤ δ ^ 2 := by
  exact sq_nonneg δ

end RiemannScope
