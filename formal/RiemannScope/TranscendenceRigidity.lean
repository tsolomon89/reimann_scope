/-
RiemannScope.TranscendenceRigidity
TASK-TC-020: Transcendence Rigidity, Exceptional Exponents, and Shift Invariance.

Formalizes:
1. Shift cancellation of reflected pairing exponent
2. Two-pairing firewall: Reflected pairing vs ordinary Gram pairing under shift
3. AM-GM defect nonnegativity and vanishing condition
4. Rational grade noncollision via log-scale injectivity
5. Exceptional exponent collinearity: dim_Q S_tau <= 1
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace RiemannScope

/-! ### 1. Reflected Convolution and Two-Pairing Firewall -/

/-- In the reflected pairing exponent -w*h - w_refl*h, the real parts cancel identically:
    -delta*h - (-delta)*h = 0.
    Therefore, the reflected convolution (T_h f * \widetilde{T_h g}) retains exact shift invariance. -/
theorem reflected_pairing_exponent_shift_cancel (delta h : ℝ) :
    (-delta * h) + (-(-delta) * h) = 0 := by
  ring

/-- In contrast, for the ordinary Gram pairing Q_+, the diagonal exponent factor is
    -2 * delta * h, which depends exponentially on delta. -/
theorem ordinary_gram_exponent_shift_factor (delta h : ℝ) :
    -delta * h + -delta * h = -2 * delta * h := by
  ring

/-- Firewall theorem: The ordinary Gram factor is shift-invariant for all h iff delta = 0. -/
theorem ordinary_gram_shift_invariant_iff_delta_zero (delta : ℝ) :
    (∀ h : ℝ, -2 * delta * h = 0) ↔ delta = 0 := by
  constructor
  · intro h_all
    have h1 := h_all 1
    linarith
  · intro h_zero h
    rw [h_zero]
    ring

/-! ### 2. Canonical Non-Unitarity Defect (AM-GM Defect) -/

/-- For any positive real y > 0, the defect y + 1/y - 2 is nonnegative. -/
theorem am_gm_defect_nonneg (y : ℝ) (hy : 0 < y) : y + y⁻¹ - 2 ≥ 0 := by
  have h_sq : 0 ≤ (y - 1)^2 := sq_nonneg (y - 1)
  have h_ne : y ≠ 0 := ne_of_gt hy
  have h_div : 0 ≤ (y - 1)^2 / y := div_nonneg h_sq (le_of_lt hy)
  have h_id : (y - 1)^2 / y = y + y⁻¹ - 2 := by
    field_simp
    ring
  linarith [h_div, h_id]

/-- The defect y + 1/y - 2 vanishes if and only if y = 1. -/
theorem am_gm_defect_eq_zero_iff (y : ℝ) (hy : 0 < y) :
    y + y⁻¹ - 2 = 0 ↔ y = 1 := by
  have h_ne : y ≠ 0 := ne_of_gt hy
  constructor
  · intro h
    have h_id : (y - 1)^2 = y * (y + y⁻¹ - 2) := by
      field_simp
      ring
    rw [h, mul_zero] at h_id
    have h_zero : y - 1 = 0 := sq_eq_zero_iff.mp h_id
    linarith
  · intro h
    rw [h]
    ring

/-! ### 3. Rational Grade Noncollision -/

/-- For tau > 1, the map K ↦ K * log(tau) is strictly injective on integers:
    distinct grades cannot collide. -/
theorem integer_grade_log_injective (tau_val : ℝ) (htau : 1 < tau_val) (K J : ℤ)
    (h_eq : (K : ℝ) * Real.log tau_val = (J : ℝ) * Real.log tau_val) : K = J := by
  have hlog_pos : 0 < Real.log tau_val := Real.log_pos htau
  have hlog_ne : Real.log tau_val ≠ 0 := ne_of_gt hlog_pos
  have h_diff : ((K : ℝ) - (J : ℝ)) * Real.log tau_val = 0 := by
    linarith [h_eq]
  cases mul_eq_zero.mp h_diff with
  | inl hK =>
    have h_cast : (K : ℝ) = (J : ℝ) := by linarith [hK]
    exact_mod_cast h_cast
  | inr hL =>
    exfalso
    exact hlog_ne hL

/-! ### 4. Exceptional Exponent Collinearity -/

/-- The Gelfond-Schneider line theorem for exceptional exponents:
    If alpha, beta are two non-zero exceptional exponents in S_tau,
    and Gelfond-Schneider forces their ratio to be rational (r = beta / alpha ∈ ℚ),
    then beta is a rational multiple of alpha: dim_Q S_tau <= 1. -/
theorem exceptional_exponents_Q_collinear
    (alpha beta : ℝ)
    (h_alpha_ne : alpha ≠ 0)
    (h_GS : ∃ (q : ℚ), (q : ℝ) = beta / alpha) :
    ∃ (q : ℚ), beta = (q : ℝ) * alpha := by
  rcases h_GS with ⟨q, hq⟩
  use q
  rw [hq]
  exact (div_mul_cancel₀ beta h_alpha_ne).symm

end RiemannScope
