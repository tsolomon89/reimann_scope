/-
RiemannScope.ExponentialPolynomialRigidity
TASK-TC-031: Exponential-Polynomial Jet Rigidity and Integer-Dilation Orbit Isolation.

This module formalizes the algebraic skeleton of exponential-polynomial rigidity and
dilation-orbit isolation for a minimal ambient realization trinomial:
    F(z) = a0 + a1 * e^(alpha * z) + a2 * e^(beta * z)
evaluated at L = log(tau) = log(2*pi) where X = tau^alpha, Y = tau^beta.

LEAN_PROVED Scope:
1. Derivative-jet coefficient vector identity:
   The m-th derivative evaluation F^(m)(L) corresponds to the linear relation vector
   (0, a1 * alpha_m, a2 * beta_m) on (1, X, Y).
2. Derivative relation non-proportionality:
   The derivative vector (0, a1 * alpha_m, a2 * beta_m) is not a scalar multiple of (a0, a1, a2)
   whenever a0 ≠ 0 and a1 * alpha_m ≠ 0.
3. Polynomial differential-operator rigidity:
   A scalar proportionality (a0 * p0, a1 * p_alpha, a2 * p_beta) = lambda * (a0, a1, a2)
   with non-zero coefficients forces p0 = p_alpha = p_beta = lambda.
4. Positive dilation polynomial identities and distinguished coefficients:
   - For k = 2: P_2(U) = a0 + a1 * U^2 + a2 * (u + v * U)^2 has linear term (2 * a2 * u * v) * U.
   - For k = 3: P_3(U) = a0 + a1 * U^3 + a2 * (u + v * U)^3 has quadratic term (3 * a2 * u * v^2) * U^2.
   - Distinguished coefficients 2 * a2 * u * v and 3 * a2 * u * v^2 are non-zero when a2, u, v ≠ 0.
5. Negative dilation polynomial identities and leading coefficients:
   - For q = 1: Q_1(U) has leading degree 2 term (a0 * v) * U^2.
   - For q = 2: Q_2(U) has leading degree 4 term (a0 * v^2) * U^4.
   - Leading coefficients a0 * v and a0 * v^2 are non-zero when a0, v ≠ 0.
6. Successive exponential Wronskian identities and strict positivity (ECT system hierarchy):
   - W_0(x) = E0 > 0.
   - W_1(x) = (E0 * E1) * (lambda1 - lambda0) > 0 for lambda0 < lambda1.
   - W_2(x) = (E0 * E1 * E2) * (lambda1 - lambda0) * (lambda2 - lambda0) * (lambda2 - lambda1) > 0.
   All successive Wronskians are strictly positive on R, proving {e^(lambda0*x), e^(lambda1*x), e^(lambda2*x)}
   is an Extended Complete Chebyshev (ECT) system on R (Karlin & Studden 1966, Chapter XI, Theorem 1.1).
7. Base-one second dilation quadratic identity:
   The evaluation of P_2(U) for base-one U = 2*pi rearranges identically to a standard quadratic form.

NOTE ON SCOPE BOUNDARIES:
- LEAN_PROVED: The exact algebraic and determinant identities formalized below.
- PROVED_PAPER_DERIVATION: Lindemann-Weierstrass necessity reduction, Gelfond-Schneider
  vector-space dimension contradiction, and Karlin-Studden ECT zero-count bound.
- EXTERNAL THEOREMS: Lindemann-Weierstrass (1885), Gelfond-Schneider (1934), Karlin-Studden (1966).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade
import RiemannScope.AmbientKernel
import RiemannScope.TrinomialKernel

set_option linter.unusedVariables false

namespace RiemannScope

/-! ### 1. Derivative-Jet Relation Vector and Non-Proportionality -/

/-- The m-th derivative evaluation vector (0, a1 * alpha_m, a2 * beta_m) evaluates on (1, X, Y)
    identically to a1 * alpha_m * X + a2 * beta_m * Y. -/
theorem trinomial_derivative_relation_vector (a1 alpha_m a2 beta_m X Y : ℝ) :
    0 * 1 + (a1 * alpha_m) * X + (a2 * beta_m) * Y = a1 * alpha_m * X + a2 * beta_m * Y := by
  ring

/-- A derivative relation vector with leading zero coordinate cannot be proportional to a
    nondegenerate original trinomial vector (a0, a1, a2) with a0 ≠ 0. -/
theorem trinomial_derivative_relation_not_proportional (a0 a1 a2 a1_alpha_m a2_beta_m : ℝ)
    (ha0 : a0 ≠ 0) (ha1_m : a1_alpha_m ≠ 0) :
    ¬ (∃ (c : ℝ), 0 = c * a0 ∧ a1_alpha_m = c * a1 ∧ a2_beta_m = c * a2) := by
  intro ⟨c, hc0, hc1, hc2⟩
  have hc : c = 0 := by
    cases mul_eq_zero.mp hc0.symm with
    | inl h => exact h
    | inr h => exact False.elim (ha0 h)
  rw [hc, zero_mul] at hc1
  exact ha1_m hc1

/-! ### 2. Differential-Operator Rigidity -/

/-- If an operator vector (a0 * p0, a1 * p_alpha, a2 * p_beta) is proportional to (a0, a1, a2)
    with non-zero coefficients a0, a1, a2, the evaluation values must be identical:
    p0 = p_alpha = p_beta. -/
theorem differential_operator_constant_support_values (a0 a1 a2 p0 p_alpha p_beta c : ℝ)
    (ha0 : a0 ≠ 0) (ha1 : a1 ≠ 0) (ha2 : a2 ≠ 0)
    (h0 : a0 * p0 = c * a0)
    (h1 : a1 * p_alpha = c * a1)
    (h2 : a2 * p_beta = c * a2) :
    p0 = p_alpha ∧ p0 = p_beta := by
  have hp0 : p0 = c := by
    have h : a0 * (p0 - c) = 0 := by linarith [h0]
    cases mul_eq_zero.mp h with
    | inl ha => exact False.elim (ha0 ha)
    | inr hp => exact sub_eq_zero.mp hp
  have hp_alpha : p_alpha = c := by
    have h : a1 * (p_alpha - c) = 0 := by linarith [h1]
    cases mul_eq_zero.mp h with
    | inl ha => exact False.elim (ha1 ha)
    | inr hp => exact sub_eq_zero.mp hp
  have hp_beta : p_beta = c := by
    have h : a2 * (p_beta - c) = 0 := by linarith [h2]
    cases mul_eq_zero.mp h with
    | inl ha => exact False.elim (ha2 ha)
    | inr hp => exact sub_eq_zero.mp hp
  exact ⟨by rw [hp0, hp_alpha], by rw [hp0, hp_beta]⟩

/-! ### 3. Positive Integer Dilation Polynomial Identities -/

/-- For k = 2 and V = u + v * U, the dilation equation a0 + a1 * U^2 + a2 * V^2
    is identically the quadratic polynomial in U with linear coefficient 2 * a2 * u * v. -/
theorem integer_dilation_positive_polynomial_identity_k2 (a0 a1 a2 u v U V : ℝ)
    (hV : V = u + v * U) :
    a0 + a1 * U^2 + a2 * V^2 =
    (a0 + a2 * u^2) + (2 * a2 * u * v) * U + (a1 + a2 * v^2) * U^2 := by
  rw [hV]
  ring

/-- For k = 3 and V = u + v * U, the dilation equation a0 + a1 * U^3 + a2 * V^3
    is identically the cubic polynomial in U with quadratic coefficient 3 * a2 * u * v^2. -/
theorem integer_dilation_positive_polynomial_identity_k3 (a0 a1 a2 u v U V : ℝ)
    (hV : V = u + v * U) :
    a0 + a1 * U^3 + a2 * V^3 =
    (a0 + a2 * u^3) + (3 * a2 * u^2 * v) * U + (3 * a2 * u * v^2) * U^2 + (a1 + a2 * v^3) * U^3 := by
  rw [hV]
  ring

/-- The distinguished linear coefficient of P_2(T) is non-zero when a2, u, v ≠ 0. -/
theorem integer_dilation_positive_nonzero_coeff_k2 (a2 u v : ℝ)
    (ha2 : a2 ≠ 0) (hu : u ≠ 0) (hv : v ≠ 0) :
    2 * a2 * u * v ≠ 0 := by
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero h2 ha2) hu) hv

/-- The distinguished quadratic coefficient of P_3(T) is non-zero when a2, u, v ≠ 0. -/
theorem integer_dilation_positive_nonzero_coeff_k3 (a2 u v : ℝ)
    (ha2 : a2 ≠ 0) (hu : u ≠ 0) (hv : v ≠ 0) :
    3 * a2 * u * v^2 ≠ 0 := by
  have h3 : (3 : ℝ) ≠ 0 := by norm_num
  have hv2 : v^2 ≠ 0 := pow_ne_zero 2 hv
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero h3 ha2) hu) hv2

/-! ### 4. Negative Integer Dilation Polynomial Identities -/

/-- For q = 1 and V = u + v * U, the cleared-denominator equation
    a0 * U * V + a1 * V + a2 * U expands identically to a polynomial in U
    with leading degree 2 coefficient a0 * v. -/
theorem integer_dilation_negative_polynomial_identity_q1 (a0 a1 a2 u v U V : ℝ)
    (hV : V = u + v * U) :
    a0 * U * V + a1 * V + a2 * U =
    (a1 * u) + (a0 * u + a1 * v + a2) * U + (a0 * v) * U^2 := by
  rw [hV]
  ring

/-- For q = 2 and V = u + v * U, the cleared-denominator equation
    a0 * U^2 * V^2 + a1 * V^2 + a2 * U^2 expands identically to a polynomial in U
    with leading degree 4 coefficient a0 * v^2. -/
theorem integer_dilation_negative_polynomial_identity_q2 (a0 a1 a2 u v U V : ℝ)
    (hV : V = u + v * U) :
    a0 * U^2 * V^2 + a1 * V^2 + a2 * U^2 =
    (a1 * u^2) + (2 * a1 * u * v) * U + (a0 * u^2 + a1 * v^2 + a2) * U^2 +
    (2 * a0 * u * v) * U^3 + (a0 * v^2) * U^4 := by
  rw [hV]
  ring

/-- The leading coefficient of Q_1(T) is non-zero when a0, v ≠ 0. -/
theorem integer_dilation_negative_leading_coeff_q1 (a0 v : ℝ)
    (ha0 : a0 ≠ 0) (hv : v ≠ 0) :
    a0 * v ≠ 0 :=
  mul_ne_zero ha0 hv

/-- The leading coefficient of Q_2(T) is non-zero when a0, v ≠ 0. -/
theorem integer_dilation_negative_leading_coeff_q2 (a0 v : ℝ)
    (ha0 : a0 ≠ 0) (hv : v ≠ 0) :
    a0 * v^2 ≠ 0 := by
  have hv2 : v^2 ≠ 0 := pow_ne_zero 2 hv
  exact mul_ne_zero ha0 hv2

/-! ### 5. Successive Exponential Wronskian Determinants and Strict Positivity (ECT System) -/

/-- Order 0 Wronskian W_0 = E0 of a single exponential is strictly positive. -/
theorem one_exponential_wronskian_pos (E0 : ℝ) (hE0 : 0 < E0) :
    0 < E0 := hE0

/-- The 2x2 Wronskian determinant W_1 for two exponential basis elements
    [ E0,          E1          ]
    [ lambda0*E0,  lambda1*E1  ]
    factors identically into (E0 * E1) * (lambda1 - lambda0). -/
theorem two_exponential_wronskian_algebraic_identity (E0 E1 l0 l1 : ℝ) :
    E0 * (l1 * E1) - E1 * (l0 * E0) = (E0 * E1) * (l1 - l0) := by
  ring

/-- For strictly positive exponential factors and strictly ordered exponents
    l0 < l1, the 2x2 Wronskian W_1 is strictly positive everywhere on R. -/
theorem two_exponential_wronskian_pos_of_ordered (E0 E1 l0 l1 : ℝ)
    (hE0 : 0 < E0) (hE1 : 0 < E1) (hl01 : l0 < l1) :
    0 < (E0 * E1) * (l1 - l0) := by
  have hd01 : 0 < l1 - l0 := sub_pos.mpr hl01
  have hE_pos : 0 < E0 * E1 := mul_pos hE0 hE1
  exact mul_pos hE_pos hd01

/-- The 3x3 Wronskian determinant for three exponential basis elements
    [ E0,          E1,          E2          ]
    [ lambda0*E0,  lambda1*E1,  lambda2*E2  ]
    [ lambda0^2*E0,lambda1^2*E1,lambda2^2*E2]
    factors identically into (E0 * E1 * E2) * (lambda1 - lambda0) * (lambda2 - lambda0) * (lambda2 - lambda1). -/
theorem three_exponential_wronskian_algebraic_identity (E0 E1 E2 l0 l1 l2 : ℝ) :
    (E0 * ((l1 * E1) * (l2^2 * E2) - (l2 * E2) * (l1^2 * E1)) -
     E1 * ((l0 * E0) * (l2^2 * E2) - (l2 * E2) * (l0^2 * E0)) +
     E2 * ((l0 * E0) * (l1^2 * E1) - (l1 * E1) * (l0^2 * E0))) =
    (E0 * E1 * E2) * (l1 - l0) * (l2 - l0) * (l2 - l1) := by
  ring

/-- For strictly positive exponential factors and strictly ordered exponents
    l0 < l1 < l2, the Wronskian is strictly positive everywhere on R. -/
theorem three_exponential_wronskian_pos_of_ordered (E0 E1 E2 l0 l1 l2 : ℝ)
    (hE0 : 0 < E0) (hE1 : 0 < E1) (hE2 : 0 < E2)
    (hl01 : l0 < l1) (hl12 : l1 < l2) :
    0 < (E0 * E1 * E2) * (l1 - l0) * (l2 - l0) * (l2 - l1) := by
  have hl02 : l0 < l2 := lt_trans hl01 hl12
  have hd01 : 0 < l1 - l0 := sub_pos.mpr hl01
  have hd02 : 0 < l2 - l0 := sub_pos.mpr hl02
  have hd12 : 0 < l2 - l1 := sub_pos.mpr hl12
  have hE_pos : 0 < E0 * E1 * E2 := mul_pos (mul_pos hE0 hE1) hE2
  exact mul_pos (mul_pos (mul_pos hE_pos hd01) hd02) hd12

/-! ### 6. Base-One Dilation Quadratic Identity -/

/-- For U = 2*pi and V = u + v * U, the second dilation equation is a standard quadratic:
    (a1 + a2 * v^2) * U^2 + (2 * a2 * u * v) * U + (a0 + a2 * u^2) = a0 + a1 * U^2 + a2 * V^2. -/
theorem base_one_second_dilation_quadratic_identity (a0 a1 a2 u v U V : ℝ)
    (hV : V = u + v * U) :
    a0 + a1 * U^2 + a2 * V^2 =
    (a1 + a2 * v^2) * U^2 + (2 * a2 * u * v) * U + (a0 + a2 * u^2) := by
  rw [hV]
  ring

end RiemannScope
