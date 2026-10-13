/-
RiemannScope.TransportMismatchCurvature
TASK-TC-034: Infinitesimal Transport-Mismatch Curvature and Non-Scalar Arithmetic Descent.

This module formalizes:
1. `single_exponential_log_curvature_zero`: A single exponential M(eta) = w * exp(eta * x)
   has zero log-curvature determinant M(0)*M''(0) - M'(0)^2 = 0.
2. `two_exponential_positive_log_curvature`: A two-term positive exponential mixture
   has strictly positive curvature w1 * w2 * (x1 - x2)^2 > 0 for distinct exponents.
3. `positive_finite_exponential_curvature_nonneg`: Nonnegativity of curvature for
   nonnegative exponential mixtures (2-point and 3-point Lagrange identities).
4. `reciprocal_pair_curvature_strict_pos`: Opposite/reciprocal pair exponents (x, -x)
   with x != 0 and positive weights yield strictly positive curvature 4 * w1 * w2 * x^2 > 0.
5. `homogeneous_arithmetic_curvature_zero`: If an arithmetic kernel satisfies Euler
   homogeneity E F_0 = d F_0 (so A_1 = d * A_0 and A_2 = d^2 * A_0), then
   arithmetic transport curvature A_0 * A_2 - A_1^2 vanishes identically.
6. `arithmetic_zero_curvature_and_spectral_positive_contradiction`: Logical incompatibility
   between vanishing arithmetic curvature and strictly positive spectral curvature.
7. Euler-generator low-order scaling algebra and K-independence of normalized
   mismatch curvature for K != 0.
8. Even second-difference identity (canceling odd mismatch terms) and centered
   conjugate vs reflection spectral pairing identities.
9. `signed_weight_curvature_negative`: Signed-weight countermodel demonstrating that
   signed weights defeat curvature positivity.
10. `generic_base_mismatch_curvature_scaling`: Generic-base control showing the
    Euler-generator normalization holds for any base log_q != 0.

NOTE ON SCOPE BOUNDARIES:
- LEAN_PROVED: Exact algebraic identities for transport mismatch curvature, Lagrange
  sum-of-squares decomposition, Euler homogeneity flatness, K-independence of normalized
  curvature, even second-difference identity, centered pairing algebra, and countermodels.
- NOT CLAIMED IN LEAN: Complete explicit formula expansion, theta-Mellin analytic descent,
  compact-support PDE homogeneity theorem, or global spectral positivity.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade
import RiemannScope.Contradiction

set_option linter.unusedVariables false

namespace RiemannScope

/-! ### 1. Arithmetic & Moment Curvature Determinant -/

/-- The transport-mismatch curvature determinant C = A_0 * A_2 - A_1^2. -/
def curvatureDet (A0 A1 A2 : ℝ) : ℝ :=
  A0 * A2 - A1 ^ 2

/-- Theorem 1: A single exponential M(eta) = w * exp(eta * x) has moments
    M_0 = w, M_1 = w * x, M_2 = w * x^2, yielding zero log-curvature. -/
theorem single_exponential_log_curvature_zero (w x : ℝ) :
    curvatureDet w (w * x) (w * x ^ 2) = 0 := by
  unfold curvatureDet
  ring

/-! ### 2. Positive Exponential Mixture Curvature Identities -/

/-- Exact two-exponential Lagrange identity:
    For M_0 = w1 + w2, M_1 = w1*x1 + w2*x2, M_2 = w1*x1^2 + w2*x2^2,
    M_0 * M_2 - M_1^2 = w1 * w2 * (x1 - x2)^2. -/
theorem two_exponential_curvature_identity (w1 w2 x1 x2 : ℝ) :
    curvatureDet (w1 + w2) (w1 * x1 + w2 * x2) (w1 * x1 ^ 2 + w2 * x2 ^ 2) =
      w1 * w2 * (x1 - x2) ^ 2 := by
  unfold curvatureDet
  ring

/-- Theorem 2: Two positive exponentials with distinct exponents have strictly
    positive log-curvature. -/
theorem two_exponential_positive_log_curvature (w1 w2 x1 x2 : ℝ)
    (hw1 : 0 < w1) (hw2 : 0 < w2) (h_dist : x1 ≠ x2) :
    0 < curvatureDet (w1 + w2) (w1 * x1 + w2 * x2) (w1 * x1 ^ 2 + w2 * x2 ^ 2) := by
  rw [two_exponential_curvature_identity]
  have hw : 0 < w1 * w2 := mul_pos hw1 hw2
  have hsq : 0 < (x1 - x2) ^ 2 := sq_pos_of_ne_zero (sub_ne_zero.mpr h_dist)
  exact mul_pos hw hsq

/-- Theorem 3a: Nonnegative two-exponential mixture has nonnegative curvature. -/
theorem positive_finite_exponential_curvature_nonneg (w1 w2 x1 x2 : ℝ)
    (hw1 : 0 ≤ w1) (hw2 : 0 ≤ w2) :
    0 ≤ curvatureDet (w1 + w2) (w1 * x1 + w2 * x2) (w1 * x1 ^ 2 + w2 * x2 ^ 2) := by
  rw [two_exponential_curvature_identity]
  have hw : 0 ≤ w1 * w2 := mul_nonneg hw1 hw2
  have hsq : 0 ≤ (x1 - x2) ^ 2 := sq_nonneg (x1 - x2)
  exact mul_nonneg hw hsq

/-- Three-exponential Lagrange sum-of-squares identity. -/
theorem three_exponential_curvature_identity (w1 w2 w3 x1 x2 x3 : ℝ) :
    curvatureDet
      (w1 + w2 + w3)
      (w1 * x1 + w2 * x2 + w3 * x3)
      (w1 * x1 ^ 2 + w2 * x2 ^ 2 + w3 * x3 ^ 2) =
      w1 * w2 * (x1 - x2) ^ 2 + w1 * w3 * (x1 - x3) ^ 2 + w2 * w3 * (x2 - x3) ^ 2 := by
  unfold curvatureDet
  ring

/-- Theorem 3b: Nonnegative three-exponential mixture has nonnegative curvature. -/
theorem three_exponential_curvature_nonneg (w1 w2 w3 x1 x2 x3 : ℝ)
    (hw1 : 0 ≤ w1) (hw2 : 0 ≤ w2) (hw3 : 0 ≤ w3) :
    0 ≤ curvatureDet
      (w1 + w2 + w3)
      (w1 * x1 + w2 * x2 + w3 * x3)
      (w1 * x1 ^ 2 + w2 * x2 ^ 2 + w3 * x3 ^ 2) := by
  rw [three_exponential_curvature_identity]
  have h12 : 0 ≤ w1 * w2 * (x1 - x2) ^ 2 :=
    mul_nonneg (mul_nonneg hw1 hw2) (sq_nonneg (x1 - x2))
  have h13 : 0 ≤ w1 * w3 * (x1 - x3) ^ 2 :=
    mul_nonneg (mul_nonneg hw1 hw3) (sq_nonneg (x1 - x3))
  have h23 : 0 ≤ w2 * w3 * (x2 - x3) ^ 2 :=
    mul_nonneg (mul_nonneg hw2 hw3) (sq_nonneg (x2 - x3))
  linarith

/-- Theorem 4: Reciprocal pair (symmetric exponents x and -x with x != 0)
    under positive weights yields strictly positive curvature 4 * w1 * w2 * x^2 > 0. -/
theorem reciprocal_pair_curvature_strict_pos (w1 w2 x : ℝ)
    (hw1 : 0 < w1) (hw2 : 0 < w2) (hx : x ≠ 0) :
    0 < curvatureDet (w1 + w2) (w1 * x + w2 * (-x)) (w1 * x ^ 2 + w2 * (-x) ^ 2) := by
  have h_ident :
      curvatureDet (w1 + w2) (w1 * x + w2 * (-x)) (w1 * x ^ 2 + w2 * (-x) ^ 2) =
        4 * (w1 * w2) * x ^ 2 := by
    unfold curvatureDet
    ring
  rw [h_ident]
  have hw : 0 < 4 * (w1 * w2) := by
    have h12 : 0 < w1 * w2 := mul_pos hw1 hw2
    linarith
  have hx2 : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  exact mul_pos hw hx2

/-! ### 3. Homogeneous Kernel Flatness & Contradiction Logic -/

/-- Theorem 5: If E F_0 = d F_0 so that A_1 = d * A_0 and A_2 = d^2 * A_0,
    then the arithmetic transport curvature vanishes identically. -/
theorem homogeneous_arithmetic_curvature_zero (A0 d : ℝ) :
    curvatureDet A0 (d * A0) (d ^ 2 * A0) = 0 := by
  unfold curvatureDet
  ring

/-- Theorem 6: Contradiction between vanishing arithmetic curvature and
    strictly positive spectral curvature. -/
theorem arithmetic_zero_curvature_and_spectral_positive_contradiction (C : ℝ)
    (h_arith : C = 0) (h_spec : 0 < C) : False := by
  linarith

/-! ### 4. Euler-Generator Low-Order Algebra & K-Independence -/

/-- Theorem 7a: Low-order Euler generator scaling for first and second mismatch derivatives. -/
theorem euler_generator_scaling_algebra (K log_tau A0 A1 A2 : ℝ) :
    curvatureDet A0 (-K * log_tau * A1) (K ^ 2 * log_tau ^ 2 * A2) =
      K ^ 2 * log_tau ^ 2 * curvatureDet A0 A1 A2 := by
  unfold curvatureDet
  ring

/-- Theorem 7b: Normalized mismatch curvature is K-independent for K != 0 and log_tau != 0. -/
theorem mismatch_curvature_k_independent (K log_tau A0 A1 A2 : ℝ)
    (hK : K ≠ 0) (hlog : log_tau ≠ 0) :
    curvatureDet A0 (-K * log_tau * A1) (K ^ 2 * log_tau ^ 2 * A2) / (K ^ 2 * log_tau ^ 2) =
      curvatureDet A0 A1 A2 := by
  rw [euler_generator_scaling_algebra]
  have hK2 : K ^ 2 ≠ 0 := pow_ne_zero 2 hK
  have hlog2 : log_tau ^ 2 ≠ 0 := pow_ne_zero 2 hlog
  have h_denom : K ^ 2 * log_tau ^ 2 ≠ 0 := mul_ne_zero hK2 hlog2
  exact mul_div_cancel_left₀ (curvatureDet A0 A1 A2) h_denom

/-! ### 5. Even Second-Difference Identity & Centering/Pairing Algebra -/

/-- Theorem 8a: The symmetric second difference of a quadratic Taylor polynomial
    M(eta) = M0 + eta * M1 + (1/2) * eta^2 * M2 isolates eta^2 * M2. -/
theorem even_second_difference_quadratic_ident (M0 M1 M2 eta : ℝ) :
    (M0 + eta * M1 + (1 / 2 : ℝ) * eta ^ 2 * M2) +
    (M0 + (-eta) * M1 + (1 / 2 : ℝ) * (-eta) ^ 2 * M2) - 2 * M0 =
      eta ^ 2 * M2 := by
  ring

/-- Theorem 8b: Centered conjugate pairing (rho - 1/2) + (bar_rho - 1/2) = 2 * delta
    isolates the real radial displacement and cancels the ordinate gamma. -/
theorem centered_conjugate_pairing_radial (delta : ℝ) :
    ((1 / 2 : ℝ) + delta - 1 / 2) + ((1 / 2 : ℝ) + delta - 1 / 2) = 2 * delta := by
  ring

/-- Theorem 8c: Centered reflection pairing real part vanishes:
    Re((rho - 1/2) + ((1 - bar_rho) - 1/2)) = delta + (-delta) = 0,
    while imaginary part is 2 * gamma. -/
theorem centered_reflection_pairing_real_zero (delta : ℝ) :
    ((1 / 2 : ℝ) + delta - 1 / 2) + (1 - ((1 / 2 : ℝ) + delta) - 1 / 2) = 0 := by
  ring

/-- Theorem 8d: Mellin mismatch net exponent algebra at b = 1 + eta. -/
theorem mellin_mismatch_net_exponent (K a eta s t : ℝ) :
    (K * (a + (1 + eta) * (s + t)) - K * (s + t)) - a * K = eta * K * (s + t) := by
  ring

/-! ### 6. Signed-Weight Countermodel & Generic-Base Control -/

/-- Theorem 9: Signed-weight countermodel.
    With signed weights w1 = 1, w2 = -2 and distinct exponents x1 = 0, x2 = 1,
    the curvature determinant is strictly negative (-2 < 0). -/
theorem signed_weight_curvature_negative :
    let w1 : ℝ := 1
    let w2 : ℝ := -2
    let x1 : ℝ := 0
    let x2 : ℝ := 1
    curvatureDet (w1 + w2) (w1 * x1 + w2 * x2) (w1 * x1 ^ 2 + w2 * x2 ^ 2) < 0 := by
  dsimp [curvatureDet]
  norm_num

/-- Theorem 10: Generic-base control.
    For any generic scale base q > 1 with log_q != 0 and grade K != 0,
    the normalized mismatch curvature reduces to curvatureDet A0 A1 A2,
    demonstrating that the Euler-generator curvature scaling is generic-base covariant. -/
theorem generic_base_mismatch_curvature_scaling (log_q K A0 A1 A2 : ℝ)
    (hK : K ≠ 0) (hq : log_q ≠ 0) :
    curvatureDet A0 (-K * log_q * A1) (K ^ 2 * log_q ^ 2 * A2) / (K ^ 2 * log_q ^ 2) =
      curvatureDet A0 A1 A2 := by
  exact mismatch_curvature_k_independent K log_q A0 A1 A2 hK hq

end RiemannScope
