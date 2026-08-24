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

/-- Involution operator sending centered coordinate z = δ + iγ to z^# = -δ + iγ. -/
noncomputable def involutionSharp (z : ℂ) : ℂ :=
  ⟨-z.re, z.im⟩

/-- Rational pairing kernel kappa_1(z, w) = 4*z*w / (z+w)^2 - 1. -/
noncomputable def kappa1 (z w : ℂ) : ℂ :=
  (4 * z * w) / (z + w) ^ 2 - 1

/-- Rational involution pairing algebraic reduction on real components:
    (4 * (δ^2 + γ^2)) / (4 * γ^2) - 1 = δ^2 / γ^2 for any γ ≠ 0. -/
theorem kappa1_pairing_algebraic (δ γ : ℝ) (hγ : γ ≠ 0) :
    (4 * (δ ^ 2 + γ ^ 2)) / (4 * γ ^ 2) - 1 = δ ^ 2 / γ ^ 2 := by
  have h4 : (4 : ℝ) ≠ 0 := by norm_num
  have hγ2 : γ ^ 2 ≠ 0 := pow_ne_zero 2 hγ
  have h4γ2 : 4 * γ ^ 2 ≠ 0 := mul_ne_zero h4 hγ2
  calc (4 * (δ ^ 2 + γ ^ 2)) / (4 * γ ^ 2) - 1
    _ = (4 * δ ^ 2 + 4 * γ ^ 2) / (4 * γ ^ 2) - 1 := by ring_nf
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) + (4 * γ ^ 2) / (4 * γ ^ 2) - 1 := by rw [add_div]
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) + 1 - 1 := by rw [div_self h4γ2]
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) := by ring
    _ = (4 / 4) * (δ ^ 2 / γ ^ 2) := by ring
    _ = 1 * (δ ^ 2 / γ ^ 2) := by rw [div_self h4]
    _ = δ ^ 2 / γ ^ 2 := by ring

/-- Finite non-negative sum vanishing firewall: r1 ≥ 0 ∧ r2 ≥ 0 ∧ r1 + r2 = 0 ⟹ r1 = 0 ∧ r2 = 0. -/
theorem nonneg_sum_two_eq_zero (r1 r2 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h : r1 + r2 = 0) :
    r1 = 0 ∧ r2 = 0 := by
  constructor <;> linarith

/-- Finite non-negative sum vanishing firewall for 3 terms. -/
theorem nonneg_sum_three_eq_zero (r1 r2 r3 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h : r1 + r2 + r3 = 0) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 := by
  refine ⟨by linarith, by linarith, by linarith⟩

/-- Finite non-negative sum vanishing firewall for 4 terms. -/
theorem nonneg_sum_four_eq_zero (r1 r2 r3 r4 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h4 : 0 ≤ r4) (h : r1 + r2 + r3 + r4 = 0) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 ∧ r4 = 0 := by
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- Finite Fredholm determinant product firewall: (1 + r1)(1 + r2) = 1 ⟹ r1 = 0 ∧ r2 = 0 for non-negative r_i. -/
theorem nonneg_prod_two_eq_one (r1 r2 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h : (1 + r1) * (1 + r2) = 1) :
    r1 = 0 ∧ r2 = 0 := by
  have h_exp : (1 + r1) * (1 + r2) = 1 + r1 + r2 + r1 * r2 := by ring
  rw [h_exp] at h
  have h_sum : r1 + r2 + r1 * r2 = 0 := by linarith [h]
  have h_mul_nonneg : 0 ≤ r1 * r2 := mul_nonneg h1 h2
  have hr1 : r1 = 0 := by linarith [h1, h2, h_mul_nonneg, h_sum]
  have hr2 : r2 = 0 := by linarith [h1, h2, h_mul_nonneg, h_sum]
  exact ⟨hr1, hr2⟩

/-- Finite Fredholm determinant product firewall for 3 terms. -/
theorem nonneg_prod_three_eq_one (r1 r2 r3 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h : (1 + r1) * (1 + r2) * (1 + r3) = 1) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 := by
  have h12_nonneg : 0 ≤ r1 + r2 + r1 * r2 := by
    have hm : 0 ≤ r1 * r2 := mul_nonneg h1 h2
    linarith
  have h_pair : (1 + (r1 + r2 + r1 * r2)) * (1 + r3) = 1 := by
    calc (1 + (r1 + r2 + r1 * r2)) * (1 + r3)
      _ = (1 + r1) * (1 + r2) * (1 + r3) := by ring
      _ = 1 := h
  have h_two := nonneg_prod_two_eq_one (r1 + r2 + r1 * r2) r3 h12_nonneg h3 h_pair
  have h12 := h_two.1
  have hr3 := h_two.2
  have h_exp : (1 + r1) * (1 + r2) = 1 := by
    calc (1 + r1) * (1 + r2)
      _ = 1 + (r1 + r2 + r1 * r2) := by ring
      _ = 1 + 0 := by rw [h12]
      _ = 1 := by ring
  have h_sub := nonneg_prod_two_eq_one r1 r2 h1 h2 h_exp
  exact ⟨h_sub.1, h_sub.2, hr3⟩

end RiemannScope
