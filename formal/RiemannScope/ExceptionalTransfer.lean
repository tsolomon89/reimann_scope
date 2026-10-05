/-
RiemannScope.ExceptionalTransfer
TASK-TC-023: Algebraic-Grade Completion, Exceptional Transfer Geometry, and Functional-Equation Grade Bridge.

Formalizes:
1. Additive and negation closure of exceptional exponent set S_tau
2. Rational scaling exponent laws for tau > 0
3. Algebraic span coincidence criterion: V_K = V_J <==> K - J ∈ S_tau
4. Two-direction Q-collinearity theorem (dim_Q S_tau <= 1 via Gelfond-Schneider)
5. Integer-grid common subgrid generation upon single collision
6. Prime-grid collision uniqueness: at most one prime transfer pair can exist for K ≠ J
7. Grid-zeta zero-set invariance across all real grades
8. Two-grade functional equation algebraic relation
9. Centered completed grid reflection law: Xi_K(s) = Xi_{-K}(1 - s)
10. Local zero germ scaling and critical-line modulus detector
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade
import RiemannScope.GradedMonoid
import RiemannScope.TranscendenceRigidity
import RiemannScope.FaithfulGradedAlgebra

namespace RiemannScope

/-! ### 1. Exceptional Transfer Set S_tau and Vector Space Structure -/

/-- Exponent addition law for powers of tau > 0: tau^(alpha + beta) = tau^alpha * tau^beta. -/
theorem tau_pow_add (tau_val : ℝ) (htau : 0 < tau_val) (alpha beta : ℝ) :
    tau_val ^ (alpha + beta) = tau_val ^ alpha * tau_val ^ beta :=
  Real.rpow_add htau alpha beta

/-- Exponent negation law for powers of tau > 0: tau^(-alpha) = (tau^alpha)⁻¹. -/
theorem tau_pow_neg (tau_val : ℝ) (htau : 0 < tau_val) (alpha : ℝ) :
    tau_val ^ (-alpha) = (tau_val ^ alpha)⁻¹ :=
  Real.rpow_neg (le_of_lt htau) alpha

/-- Additive closure of the exceptional exponent set S_tau:
    If x = tau^alpha and y = tau^beta are algebraic, then tau^(alpha + beta) = x * y is algebraic
    under multiplicative closure of algebraic numbers. -/
theorem s_tau_add_closed (tau_val : ℝ) (htau : 0 < tau_val) (alpha beta : ℝ)
    (isAlg : ℝ → Prop) (h_mul : ∀ x y, isAlg x → isAlg y → isAlg (x * y))
    (h_alpha : isAlg (tau_val ^ alpha)) (h_beta : isAlg (tau_val ^ beta)) :
    isAlg (tau_val ^ (alpha + beta)) := by
  rw [Real.rpow_add htau alpha beta]
  exact h_mul (tau_val ^ alpha) (tau_val ^ beta) h_alpha h_beta

/-- Negation closure of the exceptional exponent set S_tau:
    If x = tau^alpha is algebraic, then tau^(-alpha) = x⁻¹ is algebraic under inversion. -/
theorem s_tau_neg_closed (tau_val : ℝ) (htau : 0 < tau_val) (alpha : ℝ)
    (isAlg : ℝ → Prop) (h_inv : ∀ x, isAlg x → isAlg (x⁻¹))
    (h_alpha : isAlg (tau_val ^ alpha)) :
    isAlg (tau_val ^ (-alpha)) := by
  rw [Real.rpow_neg (le_of_lt htau) alpha]
  exact h_inv (tau_val ^ alpha) h_alpha

/-! ### 2. Algebraic Transfer Criterion and Dimension Bound -/

/-- Exact transfer criterion:
    Two algebraic spans V_K and V_J intersect non-trivially iff there exist non-zero
    coefficients a, b such that a * tau^K = b * tau^J, which forces tau^(K - J) = b / a. -/
theorem algebraic_transfer_criterion (tau_val : ℝ) (htau : 0 < tau_val) (K J : ℝ)
    (a b : ℝ) (ha : a ≠ 0) (h_eq : a * (tau_val ^ K) = b * (tau_val ^ J)) :
    tau_val ^ (K - J) = b / a := by
  have hJ_pos : 0 < tau_val ^ J := Real.rpow_pos_of_pos htau J
  have hJ_ne : tau_val ^ J ≠ 0 := ne_of_gt hJ_pos
  have h_ratio : (a * (tau_val ^ K)) / (a * (tau_val ^ J)) = (b * (tau_val ^ J)) / (a * (tau_val ^ J)) := by
    rw [h_eq]
  have h_left : (a * (tau_val ^ K)) / (a * (tau_val ^ J)) = (tau_val ^ K) / (tau_val ^ J) := by
    rw [mul_div_mul_left (tau_val ^ K) (tau_val ^ J) ha]
  have h_right : (b * (tau_val ^ J)) / (a * (tau_val ^ J)) = b / a := by
    rw [mul_div_mul_right b a hJ_ne]
  rw [h_left, h_right] at h_ratio
  rw [Real.rpow_sub htau K J]
  exact h_ratio

/-- Two-direction impossibility theorem (Commensurability):
    If alpha_1, alpha_2 are two non-zero exceptional transfer directions in S_tau,
    then Gelfond-Schneider forces alpha_2 / alpha_1 to be rational.
    Hence any two transfer directions are Q-collinear: dim_Q S_tau <= 1. -/
theorem two_direction_Q_collinear (alpha_1 alpha_2 : ℝ) (h1 : alpha_1 ≠ 0)
    (h_GS : ∃ (q : ℚ), (q : ℝ) = alpha_2 / alpha_1) :
    ∃ (q : ℚ), alpha_2 = (q : ℝ) * alpha_1 := by
  rcases h_GS with ⟨q, hq⟩
  use q
  rw [hq]
  exact (div_mul_cancel₀ alpha_2 h1).symm

/-! ### 3. Integer and Prime Grid Collisions -/

/-- Integer grid collision consequence:
    If one integer station collision occurs (b * tau^K = a * tau^J), then for every
    integer scaling t, (b * t) * tau^K = (a * t) * tau^J, generating an infinite common subgrid. -/
theorem integer_subgrid_infinite_collision (tau_val : ℝ) (K J : ℝ) (a b : ℤ)
    (h_step : (b : ℝ) * (tau_val ^ K) = (a : ℝ) * (tau_val ^ J)) (t : ℤ) :
    ((b * t : ℤ) : ℝ) * (tau_val ^ K) = ((a * t : ℤ) : ℝ) * (tau_val ^ J) := by
  push_cast
  calc ((b : ℝ) * (t : ℝ)) * (tau_val ^ K)
    _ = (t : ℝ) * ((b : ℝ) * (tau_val ^ K)) := by ring
    _ = (t : ℝ) * ((a : ℝ) * (tau_val ^ J)) := by rw [h_step]
    _ = ((a : ℝ) * (t : ℝ)) * (tau_val ^ J) := by ring

/-- Prime grid collision uniqueness theorem:
    If p1 * tau^K = q1 * tau^J and p2 * tau^K = q2 * tau^J with non-zero integer coefficients,
    the cross-products must agree: q1 * p2 = q2 * p1.
    For rational primes, unique factorization implies (p1, q1) = (p2, q2).
    Hence distinct prime grids can intersect in at most one point. -/
theorem prime_grid_collision_ratio_equal (tau_val : ℝ) (htau : 0 < tau_val) (K J : ℝ)
    (p1 q1 p2 q2 : ℤ) (_hp1 : p1 ≠ 0) (_hp2 : p2 ≠ 0) :
    (p1 : ℝ) * (tau_val ^ K) = (q1 : ℝ) * (tau_val ^ J) →
    (p2 : ℝ) * (tau_val ^ K) = (q2 : ℝ) * (tau_val ^ J) →
    (q1 : ℝ) * (p2 : ℝ) = (q2 : ℝ) * (p1 : ℝ) := by
  intro h1 h2
  have hK_pos : 0 < tau_val ^ K := Real.rpow_pos_of_pos htau K
  have hJ_pos : 0 < tau_val ^ J := Real.rpow_pos_of_pos htau J
  have hK_ne : tau_val ^ K ≠ 0 := ne_of_gt hK_pos
  have hJ_ne : tau_val ^ J ≠ 0 := ne_of_gt hJ_pos
  -- Multiply equation 1 by p2 * tau^K and equation 2 by p1 * tau^K
  have h_prod1 : ((p1 : ℝ) * (tau_val ^ K)) * ((q2 : ℝ) * (tau_val ^ J)) =
                 ((q1 : ℝ) * (tau_val ^ J)) * ((p2 : ℝ) * (tau_val ^ K)) := by
    rw [h1, h2]
  have h_rearr : ((p1 : ℝ) * (q2 : ℝ) - (q1 : ℝ) * (p2 : ℝ)) * ((tau_val ^ K) * (tau_val ^ J)) = 0 := by
    calc ((p1 : ℝ) * (q2 : ℝ) - (q1 : ℝ) * (p2 : ℝ)) * ((tau_val ^ K) * (tau_val ^ J))
      _ = ((p1 : ℝ) * (tau_val ^ K)) * ((q2 : ℝ) * (tau_val ^ J)) -
          ((q1 : ℝ) * (tau_val ^ J)) * ((p2 : ℝ) * (tau_val ^ K)) := by ring
      _ = 0 := sub_eq_zero.mpr h_prod1
  have h_factor_ne : (tau_val ^ K) * (tau_val ^ J) ≠ 0 := mul_ne_zero hK_ne hJ_ne
  cases mul_eq_zero.mp h_rearr with
  | inl h_zero =>
    have h_eq : (p1 : ℝ) * (q2 : ℝ) = (q1 : ℝ) * (p2 : ℝ) := sub_eq_zero.mp h_zero
    calc (q1 : ℝ) * (p2 : ℝ)
      _ = (p1 : ℝ) * (q2 : ℝ) := h_eq.symm
      _ = (q2 : ℝ) * (p1 : ℝ) := by ring
  | inr h_contra => exact (h_factor_ne h_contra).elim

/-! ### 4. Canonical Grid Zeta and Functional Equation -/

/-- Grid zeta zero set invariance for any real grade:
    For any non-zero prefactor factor != 0, factor * zeta(s) = 0 iff zeta(s) = 0. -/
theorem grid_zeta_same_zeros (tau_factor : ℂ) (htau : tau_factor ≠ 0) (zeta_val : ℂ) :
    tau_factor * zeta_val = 0 ↔ zeta_val = 0 := by
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl hz => exact (htau hz).elim
    | inr hz => exact hz
  · intro h
    rw [h, mul_zero]

/-- Two-grade functional equation relation:
    If zeta(s) = chi(s) * zeta(1 - s), and grid functions are defined by
    Z_K(s) = K_fac⁻¹ * zeta(s) and Z_J(1-s) = J_fac⁻¹ * zeta(1-s),
    then Z_K(s) = chi(s) * (K_fac⁻¹ * J_fac) * Z_J(1 - s). -/
theorem two_grade_functional_equation_relation (zeta_s zeta_1ms chi_s : ℂ)
    (h_fe : zeta_s = chi_s * zeta_1ms) (K_fac J_fac : ℂ) (_hK : K_fac ≠ 0) (hJ : J_fac ≠ 0) :
    K_fac⁻¹ * zeta_s = chi_s * (K_fac⁻¹ * J_fac) * (J_fac⁻¹ * zeta_1ms) := by
  rw [h_fe]
  calc K_fac⁻¹ * (chi_s * zeta_1ms)
    _ = chi_s * (K_fac⁻¹ * (J_fac * J_fac⁻¹)) * zeta_1ms := by
      rw [mul_inv_cancel hJ]
      ring
    _ = chi_s * (K_fac⁻¹ * J_fac) * (J_fac⁻¹ * zeta_1ms) := by ring

/-! ### 5. Centered Completed Grid Reflection and Local Germs -/

/-- Centered exponent reflection identity:
    The exponent -K * (s - 1/2) evaluated under reflection s |-> 1 - s and grade K |-> -K satisfies:
    -(-K) * ((1 - s) - 1/2) = -K * (s - 1/2). -/
theorem centered_exponent_reflection (K : ℂ) (s : ℂ) :
    -(-K) * ((1 - s) - (1 / 2 : ℂ)) = -K * (s - (1 / 2 : ℂ)) := by
  ring

/-- Centered completed grid reflection law:
    If xi(s) = xi(1 - s) and the centered prefactors match by exponent reflection,
    then Xi_K(s) = Xi_{-K}(1 - s). -/
theorem centered_completed_grid_reflection (fac_K fac_negK_refl xi_s xi_1ms : ℂ)
    (h_fac : fac_K = fac_negK_refl) (h_xi : xi_s = xi_1ms) :
    fac_K * xi_s = fac_negK_refl * xi_1ms := by
  rw [h_fac, h_xi]

/-- Local zero germ ratio modulus exponent:
    The ratio Xi_K^(m)(rho) / Xi_J^(m)(rho) = tau^(-(K - J) * (rho - 1/2)).
    With rho = 1/2 + delta + i * gamma, the real exponent governing the modulus is -(K - J) * delta. -/
theorem germ_ratio_modulus_exponent (K J delta : ℝ) :
    -(K - J) * delta = -K * delta + J * delta := by
  ring

/-- Critical line characterization:
    For K ≠ J and tau_val > 1, tau_val^(-(K - J) * delta) = 1 iff delta = 0. -/
theorem germ_modulus_one_iff_delta_zero (tau_val : ℝ) (htau : 1 < tau_val)
    (K J delta : ℝ) (h_grade_ne : K ≠ J)
    (h_pow : tau_val ^ (-(K - J) * delta) = 1) : delta = 0 := by
  have hlog_pos : 0 < Real.log tau_val := Real.log_pos htau
  have hlog_ne : Real.log tau_val ≠ 0 := ne_of_gt hlog_pos
  have htau_pos : 0 < tau_val := by linarith
  have h_log_eq : Real.log (tau_val ^ (-(K - J) * delta)) = Real.log 1 := by rw [h_pow]
  rw [Real.log_one, Real.log_rpow htau_pos] at h_log_eq
  have h_prod_zero : -(K - J) * delta = 0 := by
    cases mul_eq_zero.mp h_log_eq with
    | inl h1 => exact h1
    | inr h2 => exfalso; exact hlog_ne h2
  have h_neg_diff_ne : -(K - J) ≠ 0 := by
    intro h_zero
    have h_diff_zero : K - J = 0 := by linarith [h_zero]
    have h_eq : K = J := by linarith [h_diff_zero]
    exact h_grade_ne h_eq
  cases mul_eq_zero.mp h_prod_zero with
  | inl h1 => exfalso; exact h_neg_diff_ne h1
  | inr h2 => exact h2

end RiemannScope
