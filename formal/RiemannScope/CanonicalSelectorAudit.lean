/-
RiemannScope.CanonicalSelectorAudit — Canonical Zeta Selector Principle and Uniqueness Audit (TASK-TC-035)

Formalizes the exact algebraic identities and dichotomy theorems governing the Canonical
Selector Audit (`TASK-TC-035`):
1. Separable tensor-square curvature reduction:
     F_0(x, y) = f(x) f(y) ==>
     A_0 = m_0^2, A_1 = 2 m_0 m_1, A_2 = 2 m_0 m_2 + 2 m_1^2,
     and C_arith(f x f) = 2 m_0^2 (m_0 m_2 - m_1^2).
2. Additive-to-multiplicative Euler chain-rule drift identity for Jacobi theta / heat kernels:
     (t d/dt)^2 = t^2 d^2/dt^2 + t d/dt ==>
     C_arith(Theta_t) = c^2 (M_0 M_2 - M_1^2) - 2 c M_0 M_1,
   together with strict negativity when the chain-rule drift dominates the Bernstein variance
   and exact negativity at a single dominant station pair.
3. Multiplicative log-Gaussian variance-threshold theorem:
     F_{a, w_0}(x, y) = exp(-a (log(xy) - w_0)^2) ==>
     C_arith(F_{a, w_0}) = 16 a^2 (S_0 S_2 - S_1^2) - 8 a S_0^2,
   with exact negative, zero (critical width), and positive sign characterization.
4. Selector Trilemma algebraic dichotomy and complement-positivity contradiction requirement.

Note: Hamburger's uniqueness theorem, Burnol's co-Poisson distribution dictionary,
Nyman-Beurling L^2 completeness, and Connes-Consani semi-local trace formulas are external
analytic theorems and are NOT claimed as formalized Lean theorems here.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import RiemannScope.TransportMismatchCurvature

namespace RiemannScope

/-- 1D Euler curvature determinant c_1D(f) = m_0 m_2 - m_1^2 for 1D prime-station moments. -/
def oneDimCurvature (m0 m1 m2 : ℝ) : ℝ :=
  m0 * m2 - m1 ^ 2

/-- Separable tensor-square zeroth Euler moment: A_0(f x f) = m_0 * m_0 = m_0^2. -/
theorem tensor_square_moment_A0 (m0 : ℝ) :
    m0 * m0 = m0 ^ 2 := by
  ring

/-- Separable tensor-square first Euler moment: A_1(f x f) = m_1 m_0 + m_0 m_1 = 2 m_0 m_1. -/
theorem tensor_square_moment_A1 (m0 m1 : ℝ) :
    m1 * m0 + m0 * m1 = 2 * m0 * m1 := by
  ring

/-- Separable tensor-square second Euler moment:
    A_2(f x f) = m_2 m_0 + 2 m_1 m_1 + m0 m_2 = 2 m_0 m_2 + 2 m_1^2. -/
theorem tensor_square_moment_A2 (m0 m1 m2 : ℝ) :
    m2 * m0 + 2 * m1 * m1 + m0 * m2 = 2 * m0 * m2 + 2 * m1 ^ 2 := by
  ring

/-- Separable tensor-square curvature reduction:
    C_arith(f x f) = A_0 A_2 - A_1^2 = 2 m_0^2 (m_0 m_2 - m_1^2). -/
theorem tensor_square_curvature_reduction (m0 m1 m2 : ℝ) :
    curvatureDet (m0 ^ 2) (2 * m0 * m1) (2 * m0 * m2 + 2 * m1 ^ 2) =
      2 * m0 ^ 2 * oneDimCurvature m0 m1 m2 := by
  unfold curvatureDet oneDimCurvature
  ring

/-- For a nonzero 1D zeroth moment m_0 != 0, the 2D tensor-square curvature is strictly positive
    if and only if the 1D Euler curvature m_0 m_2 - m_1^2 is strictly positive. -/
theorem tensor_square_curvature_pos_iff (m0 m1 m2 : ℝ) (hm0 : m0 ≠ 0) :
    0 < curvatureDet (m0 ^ 2) (2 * m0 * m1) (2 * m0 * m2 + 2 * m1 ^ 2) ↔
      0 < oneDimCurvature m0 m1 m2 := by
  rw [tensor_square_curvature_reduction]
  have hm0_sq : 0 < 2 * m0 ^ 2 := by positivity
  constructor <;> intro h <;> nlinarith

/-- For a nonzero 1D zeroth moment m_0 != 0, the 2D tensor-square curvature is strictly negative
    if and only if the 1D Euler curvature m_0 m_2 - m_1^2 is strictly negative. -/
theorem tensor_square_curvature_neg_iff (m0 m1 m2 : ℝ) (hm0 : m0 ≠ 0) :
    curvatureDet (m0 ^ 2) (2 * m0 * m1) (2 * m0 * m2 + 2 * m1 ^ 2) < 0 ↔
      oneDimCurvature m0 m1 m2 < 0 := by
  rw [tensor_square_curvature_reduction]
  have hm0_sq : 0 < 2 * m0 ^ 2 := by positivity
  constructor <;> intro h <;> nlinarith

/-- Additive-to-multiplicative Euler chain-rule drift identity for Jacobi theta / Laplace sums:
    when A_0 = M_0, A_1 = -c M_1, and A_2 = c^2 M_2 - 2 c M_1 (with c = 2*pi*t),
    C_arith = c^2 (M_0 M_2 - M_1^2) - 2 c M_0 M_1. -/
theorem euler_chain_rule_second_deriv_curvature (M0 M1 M2 c : ℝ) :
    curvatureDet M0 (-c * M1) (c ^ 2 * M2 - 2 * c * M1) =
      c ^ 2 * curvatureDet M0 M1 M2 - 2 * c * M0 * M1 := by
  unfold curvatureDet
  ring

/-- Whenever the negative Euler chain-rule drift 2 M_0 M_1 strictly exceeds c (M_0 M_2 - M_1^2)
    for c > 0, the resulting multiplicative arithmetic Euler curvature is strictly negative. -/
theorem euler_drift_strictly_negative_of_dominant (M0 M1 M2 c : ℝ)
    (hc : 0 < c) (hbound : c * curvatureDet M0 M1 M2 < 2 * M0 * M1) :
    curvatureDet M0 (-c * M1) (c ^ 2 * M2 - 2 * c * M1) < 0 := by
  rw [euler_chain_rule_second_deriv_curvature]
  nlinarith

/-- At a single dominant prime-power station pair with weight w > 0 and quadratic radius r > 0,
    the Bernstein variance M_0 M_2 - M_1^2 vanishes identically while the Euler chain-rule drift
    makes the arithmetic curvature strictly negative: C_arith = -2 c w^2 r < 0. -/
theorem single_station_theta_gaussian_curvature_neg (w r c : ℝ)
    (hw : 0 < w) (hr : 0 < r) (hc : 0 < c) :
    curvatureDet w (-c * (w * r)) (c ^ 2 * (w * r ^ 2) - 2 * c * (w * r)) = -2 * c * w ^ 2 * r ∧
      curvatureDet w (-c * (w * r)) (c ^ 2 * (w * r ^ 2) - 2 * c * (w * r)) < 0 := by
  have hid :
      curvatureDet w (-c * (w * r)) (c ^ 2 * (w * r ^ 2) - 2 * c * (w * r)) =
        -2 * c * w ^ 2 * r := by
    unfold curvatureDet
    ring
  refine ⟨hid, ?_⟩
  rw [hid]
  have hpos : 0 < 2 * c * w ^ 2 * r := by positivity
  linarith

/-- Multiplicative log-Gaussian curvature identity:
    for F_{a, w_0}(x, y) = exp(-a (log(xy) - w_0)^2), the Euler moments satisfy
    A_0 = S_0, A_1 = -4 a S_1, A_2 = 16 a^2 S_2 - 8 a S_0, yielding
    C_arith = 16 a^2 (S_0 S_2 - S_1^2) - 8 a S_0^2. -/
theorem log_gaussian_curvature_identity (S0 S1 S2 a : ℝ) :
    curvatureDet S0 (-4 * a * S1) (16 * a ^ 2 * S2 - 8 * a * S0) =
      16 * a ^ 2 * curvatureDet S0 S1 S2 - 8 * a * S0 ^ 2 := by
  unfold curvatureDet
  ring

/-- Multiplicative log-Gaussian negative curvature regime:
    for a > 0 and 2 a (S_0 S_2 - S_1^2) < S_0^2, the arithmetic curvature is strictly negative. -/
theorem log_gaussian_curvature_neg_of_subcritical_variance (S0 S1 S2 a : ℝ)
    (ha : 0 < a) (hvar : 2 * a * curvatureDet S0 S1 S2 < S0 ^ 2) :
    curvatureDet S0 (-4 * a * S1) (16 * a ^ 2 * S2 - 8 * a * S0) < 0 := by
  rw [log_gaussian_curvature_identity]
  nlinarith

/-- Multiplicative log-Gaussian positive curvature regime:
    for a > 0 and S_0^2 < 2 a (S_0 S_2 - S_1^2), the arithmetic curvature is strictly positive. -/
theorem log_gaussian_curvature_pos_of_supercritical_variance (S0 S1 S2 a : ℝ)
    (ha : 0 < a) (hvar : S0 ^ 2 < 2 * a * curvatureDet S0 S1 S2) :
    0 < curvatureDet S0 (-4 * a * S1) (16 * a ^ 2 * S2 - 8 * a * S0) := by
  rw [log_gaussian_curvature_identity]
  nlinarith

/-- Multiplicative log-Gaussian critical-width vanishing:
    at the tuned width 2 a (S_0 S_2 - S_1^2) = S_0^2, the arithmetic curvature vanishes. -/
theorem log_gaussian_critical_width_zero (S0 S1 S2 a : ℝ)
    (hcrit : 2 * a * curvatureDet S0 S1 S2 = S0 ^ 2) :
    curvatureDet S0 (-4 * a * S1) (16 * a ^ 2 * S2 - 8 * a * S0) = 0 := by
  rw [log_gaussian_curvature_identity]
  calc
    16 * a ^ 2 * curvatureDet S0 S1 S2 - 8 * a * S0 ^ 2 =
        8 * a * (2 * a * curvatureDet S0 S1 S2 - S0 ^ 2) := by ring
    _ = 8 * a * (S0 ^ 2 - S0 ^ 2) := by rw [hcrit]
    _ = 0 := by ring

/-- Selector Trilemma algebraic dichotomy:
    if an arithmetic-spectral identity C_arith = S_diag + R_comp holds with C_arith <= 0 and
    selected off-critical diagonal curvature S_diag > 0, then the remaining spectral/Archimedean
    complement R_comp is forced to be strictly negative (absorbing the gap unless R_comp >= 0
    is independently proved). -/
theorem selector_trilemma_algebraic_dichotomy (A0 A1 A2 S_diag R_comp : ℝ)
    (h_id : curvatureDet A0 A1 A2 = S_diag + R_comp)
    (h_arith_nonpos : curvatureDet A0 A1 A2 ≤ 0)
    (h_diag_pos : 0 < S_diag) :
    R_comp < 0 := by
  linarith

/-- Selector Trilemma contradiction under independent complement nonnegativity:
    if C_arith = S_diag + R_comp with C_arith <= 0, S_diag > 0, AND R_comp >= 0 is independently
    established (OBL-CT-001A), a contradiction follows immediately. -/
theorem selector_trilemma_contradiction_of_nonneg_complement (A0 A1 A2 S_diag R_comp : ℝ)
    (h_id : curvatureDet A0 A1 A2 = S_diag + R_comp)
    (h_arith_nonpos : curvatureDet A0 A1 A2 ≤ 0)
    (h_diag_pos : 0 < S_diag)
    (h_comp_nonneg : 0 ≤ R_comp) :
    False := by
  linarith

end RiemannScope
