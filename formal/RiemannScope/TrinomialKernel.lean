/-
RiemannScope.TrinomialKernel
TASK-TC-030: Minimal Rank-Two Trinomial Kernel, Relation-Space Rigidity, and Sparse Orbit Theorems.

This module formalizes the algebraic skeleton of the minimal unresolved ambient realization kernel:
    a0 + a1 * tau^alpha + a2 * tau^beta = 0
for generators X = tau^alpha, Y = tau^beta with alpha/beta ∉ Q.

LEAN_PROVED Scope:
1. Support translation invariance for 3-term ambient sums:
   a0 * tau^K0 + a1 * tau^K1 + a2 * tau^K2 = tau^K0 * (a0 + a1 * tau^(K1-K0) + a2 * tau^(K2-K0))
2. Sign geometry: All-positive or all-negative coefficients are impossible for positive X, Y.
3. Linear algebra coordinate forcing: Two independent linear relations uniquely determine (X, Y)
   via Cramer's rule in terms of coefficient rational functions.
4. Exceptional-direction exclusion:
   - If X is known/algebraic, Y is algebraically determined: Y = (-a0 - a1 * X) / a2.
   - If Y is known/algebraic, X is algebraically determined: X = (-a0 - a2 * Y) / a1.
   - If ratio Y/X is known/algebraic, X is algebraically determined: X = -a0 / (a1 + a2 * (Y / X)).
5. Three-consecutive dilation orbit determinant identity:
   det [1, Xn, Yn; 1, Xn*X, Yn*Y; 1, Xn*X^2, Yn*Y^2] = Xn * Yn * (X - 1) * (Y - 1) * (Y - X).
6. Three-consecutive dilation orbit rigidity:
   A nonzero trinomial vector (a0, a1, a2) cannot vanish on three consecutive dilation grades
   for pairwise distinct positive bases 1, X, Y.
7. Base-dilation pairwise distinct powers for strictly positive base > 1 and distinct exponents.

NOTE ON SCOPE BOUNDARIES:
- LEAN_PROVED: The algebraic identities and deduction theorems formalized below.
- PROVED_PAPER_DERIVATION: Complex coefficient real normalization (Hilbert 90),
  Gelfond-Schneider external bound (dim_Q S_tau <= 1), Laurent's theorem /
  Evertse-Schlickewei-Schmidt S-unit finiteness, and the generalized Vandermonde positivity.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade
import RiemannScope.AmbientKernel

set_option linter.unusedVariables false

namespace RiemannScope

/-! ### 1. Support Translation for Trinomial Kernel -/

/-- Support translation identity for a 3-term linear combination:
    Translating all grades by K0 factors out tau^K0. -/
theorem trinomial_support_translation (tau_val : ℝ) (htau : 0 < tau_val)
    (K0 K1 K2 a0 a1 a2 : ℝ) :
    a0 * (tau_val ^ K0) + a1 * (tau_val ^ K1) + a2 * (tau_val ^ K2) =
    (tau_val ^ K0) * (a0 + a1 * (tau_val ^ (K1 - K0)) + a2 * (tau_val ^ (K2 - K0))) := by
  have hK1 : tau_val ^ K1 = tau_val ^ K0 * tau_val ^ (K1 - K0) :=
    tau_pow_translation tau_val htau K1 K0
  have hK2 : tau_val ^ K2 = tau_val ^ K0 * tau_val ^ (K2 - K0) :=
    tau_pow_translation tau_val htau K2 K0
  rw [hK1, hK2]
  ring

/-! ### 2. Sign Geometry: Mixed Signs are Necessary -/

/-- All strictly positive coefficients cannot sum to zero with positive generators. -/
theorem trinomial_same_sign_pos_impossible (a0 a1 a2 X Y : ℝ)
    (ha0 : 0 < a0) (ha1 : 0 < a1) (ha2 : 0 < a2)
    (hX : 0 < X) (hY : 0 < Y) :
    a0 + a1 * X + a2 * Y ≠ 0 := by
  have h1 : 0 < a1 * X := mul_pos ha1 hX
  have h2 : 0 < a2 * Y := mul_pos ha2 hY
  have hsum : 0 < a0 + a1 * X + a2 * Y := by linarith
  exact ne_of_gt hsum

/-- All strictly negative coefficients cannot sum to zero with positive generators. -/
theorem trinomial_same_sign_neg_impossible (a0 a1 a2 X Y : ℝ)
    (ha0 : a0 < 0) (ha1 : a1 < 0) (ha2 : a2 < 0)
    (hX : 0 < X) (hY : 0 < Y) :
    a0 + a1 * X + a2 * Y ≠ 0 := by
  have h1 : a1 * X < 0 := mul_neg_of_neg_of_pos ha1 hX
  have h2 : a2 * Y < 0 := mul_neg_of_neg_of_pos ha2 hY
  have hsum : a0 + a1 * X + a2 * Y < 0 := by linarith
  exact ne_of_lt hsum

/-! ### 3. Two Relations Force Coordinate Dependence (Cramer's Rule) -/

/-- Two linearly independent affine relations on (1, X, Y) uniquely determine
    X and Y as rational expressions of the coefficients. -/
theorem trinomial_two_relations_cramer (a0 a1 a2 b0 b1 b2 X Y : ℝ)
    (h1 : a0 + a1 * X + a2 * Y = 0)
    (h2 : b0 + b1 * X + b2 * Y = 0)
    (hdet : a1 * b2 - a2 * b1 ≠ 0) :
    X = (a2 * b0 - a0 * b2) / (a1 * b2 - a2 * b1) ∧
    Y = (a0 * b1 - a1 * b0) / (a1 * b2 - a2 * b1) := by
  have hX_num : (a1 * b2 - a2 * b1) * X = a2 * b0 - a0 * b2 := by
    calc (a1 * b2 - a2 * b1) * X
      _ = b2 * (a0 + a1 * X + a2 * Y) - a2 * (b0 + b1 * X + b2 * Y) + (a2 * b0 - a0 * b2) := by ring
      _ = b2 * 0 - a2 * 0 + (a2 * b0 - a0 * b2) := by rw [h1, h2]
      _ = a2 * b0 - a0 * b2 := by ring
  have hY_num : (a1 * b2 - a2 * b1) * Y = a0 * b1 - a1 * b0 := by
    calc (a1 * b2 - a2 * b1) * Y
      _ = a1 * (b0 + b1 * X + b2 * Y) - b1 * (a0 + a1 * X + a2 * Y) + (a0 * b1 - a1 * b0) := by ring
      _ = a1 * 0 - b1 * 0 + (a0 * b1 - a1 * b0) := by rw [h1, h2]
      _ = a0 * b1 - a1 * b0 := by ring
  constructor
  · calc X = ((a1 * b2 - a2 * b1) * X) / (a1 * b2 - a2 * b1) := (mul_div_cancel_left₀ X hdet).symm
      _ = (a2 * b0 - a0 * b2) / (a1 * b2 - a2 * b1) := by rw [hX_num]
  · calc Y = ((a1 * b2 - a2 * b1) * Y) / (a1 * b2 - a2 * b1) := (mul_div_cancel_left₀ Y hdet).symm
      _ = (a0 * b1 - a1 * b0) / (a1 * b2 - a2 * b1) := by rw [hY_num]

/-! ### 4. Exceptional-Direction Exclusion -/

/-- If X is fixed/algebraic, solving a nondegenerate trinomial expresses Y algebraically. -/
theorem trinomial_exceptional_x_forces_exceptional_y (a0 a1 a2 X Y : ℝ)
    (ha2 : a2 ≠ 0) (h : a0 + a1 * X + a2 * Y = 0) :
    Y = (-a0 - a1 * X) / a2 := by
  have h2 : a2 * Y = -a0 - a1 * X := by linarith
  calc Y = (a2 * Y) / a2 := (mul_div_cancel_left₀ Y ha2).symm
    _ = (-a0 - a1 * X) / a2 := by rw [h2]

/-- If Y is fixed/algebraic, solving a nondegenerate trinomial expresses X algebraically. -/
theorem trinomial_exceptional_y_forces_exceptional_x (a0 a1 a2 X Y : ℝ)
    (ha1 : a1 ≠ 0) (h : a0 + a1 * X + a2 * Y = 0) :
    X = (-a0 - a2 * Y) / a1 := by
  have h2 : a1 * X = -a0 - a2 * Y := by linarith
  calc X = (a1 * X) / a1 := (mul_div_cancel_left₀ X ha1).symm
    _ = (-a0 - a2 * Y) / a1 := by rw [h2]

/-- If ratio Y/X is fixed/algebraic and denominator is nonzero, X is algebraically determined. -/
theorem trinomial_exceptional_ratio_forces_exceptional_coordinates (a0 a1 a2 X Y : ℝ)
    (hX : X ≠ 0) (h_denom : a1 + a2 * (Y / X) ≠ 0) (h : a0 + a1 * X + a2 * Y = 0) :
    X = -a0 / (a1 + a2 * (Y / X)) := by
  have h_mul : (a1 + a2 * (Y / X)) * X = -a0 := by
    calc (a1 + a2 * (Y / X)) * X
      _ = a1 * X + a2 * ((Y / X) * X) := by ring
      _ = a1 * X + a2 * Y := by rw [div_mul_cancel₀ Y hX]
      _ = -a0 := by linarith
  calc X = ((a1 + a2 * (Y / X)) * X) / (a1 + a2 * (Y / X)) := (mul_div_cancel_left₀ X h_denom).symm
    _ = -a0 / (a1 + a2 * (Y / X)) := by rw [h_mul]

/-! ### 5. Three-Consecutive Dilation Orbit Identity and Rigidity -/

/-- The 3x3 consecutive dilation matrix determinant identity:
    det [ 1,   Xn,       Yn       ]
        [ 1,   Xn * X,   Yn * Y   ]
        [ 1,   Xn * X^2, Yn * Y^2 ]
    = Xn * Yn * (X - 1) * (Y - 1) * (Y - X). -/
theorem trinomial_three_consecutive_orbit_determinant (Xn Yn X Y : ℝ) :
    (1 * ((Xn * X) * (Yn * Y^2) - (Xn * X^2) * (Yn * Y)) -
     Xn * (1 * (Yn * Y^2) - 1 * (Yn * Y)) +
     Yn * (1 * (Xn * X^2) - 1 * (Xn * X))) =
    Xn * Yn * (X - 1) * (Y - 1) * (Y - X) := by
  ring

/-- Consecutive orbit determinant is strictly nonzero when generators are positive and pairwise distinct. -/
theorem trinomial_three_consecutive_orbit_det_ne_zero (Xn Yn X Y : ℝ)
    (hXn : Xn ≠ 0) (hYn : Yn ≠ 0)
    (hX1 : X ≠ 1) (hY1 : Y ≠ 1) (hYX : Y ≠ X) :
    Xn * Yn * (X - 1) * (Y - 1) * (Y - X) ≠ 0 := by
  have hX_sub : X - 1 ≠ 0 := sub_ne_zero.mpr hX1
  have hY_sub : Y - 1 ≠ 0 := sub_ne_zero.mpr hY1
  have hYX_sub : Y - X ≠ 0 := sub_ne_zero.mpr hYX
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero hXn hYn) hX_sub) hY_sub) hYX_sub

/-- Three-consecutive dilation orbit rigidity:
    If a fixed trinomial coefficient vector vanishes on three consecutive dilation grades
    for pairwise distinct positive bases, all three coefficients must vanish. -/
theorem trinomial_three_consecutive_orbit_rigidity (a0 a1 a2 Xn Yn X Y : ℝ)
    (hXn : Xn ≠ 0) (hX1 : X ≠ 1) (hYX : Y ≠ X) (hY1 : Y ≠ 1) (hYn : Yn ≠ 0)
    (eq0 : a0 + a1 * Xn + a2 * Yn = 0)
    (eq1 : a0 + a1 * (Xn * X) + a2 * (Yn * Y) = 0)
    (eq2 : a0 + a1 * (Xn * X^2) + a2 * (Yn * Y^2) = 0) :
    a0 = 0 ∧ a1 = 0 ∧ a2 = 0 := by
  -- Subtract eq0 from eq1
  have d1 : a1 * (Xn * (X - 1)) + a2 * (Yn * (Y - 1)) = 0 := by
    calc a1 * (Xn * (X - 1)) + a2 * (Yn * (Y - 1))
      _ = (a0 + a1 * (Xn * X) + a2 * (Yn * Y)) - (a0 + a1 * Xn + a2 * Yn) := by ring
      _ = 0 - 0 := by rw [eq1, eq0]
      _ = 0 := by ring
  -- Subtract eq1 from eq2
  have d2 : a1 * (Xn * X * (X - 1)) + a2 * (Yn * Y * (Y - 1)) = 0 := by
    calc a1 * (Xn * X * (X - 1)) + a2 * (Yn * Y * (Y - 1))
      _ = (a0 + a1 * (Xn * X^2) + a2 * (Yn * Y^2)) - (a0 + a1 * (Xn * X) + a2 * (Yn * Y)) := by ring
      _ = 0 - 0 := by rw [eq2, eq1]
      _ = 0 := by ring
  -- Eliminate a2 by computing d2 - Y * d1
  have h_a1_elim : a1 * (Xn * (X - 1) * (X - Y)) = 0 := by
    calc a1 * (Xn * (X - 1) * (X - Y))
      _ = (a1 * (Xn * X * (X - 1)) + a2 * (Yn * Y * (Y - 1))) -
          Y * (a1 * (Xn * (X - 1)) + a2 * (Yn * (Y - 1))) := by ring
      _ = 0 - Y * 0 := by rw [d2, d1]
      _ = 0 := by ring
  have hX_sub : X - 1 ≠ 0 := sub_ne_zero.mpr hX1
  have hXY_sub : X - Y ≠ 0 := sub_ne_zero.mpr (Ne.symm hYX)
  have h_factor_ne : Xn * (X - 1) * (X - Y) ≠ 0 :=
    mul_ne_zero (mul_ne_zero hXn hX_sub) hXY_sub
  have ha1 : a1 = 0 := by
    cases mul_eq_zero.mp h_a1_elim with
    | inl h => exact h
    | inr h => exact False.elim (h_factor_ne h)
  -- Now substitute a1 = 0 into d1 to get a2 = 0
  have ha2_mul : a2 * (Yn * (Y - 1)) = 0 := by
    calc a2 * (Yn * (Y - 1))
      _ = a1 * (Xn * (X - 1)) + a2 * (Yn * (Y - 1)) := by rw [ha1, zero_mul, zero_add]
      _ = 0 := d1
  have hY_sub : Y - 1 ≠ 0 := sub_ne_zero.mpr hY1
  have h_yfactor_ne : Yn * (Y - 1) ≠ 0 := mul_ne_zero hYn hY_sub
  have ha2 : a2 = 0 := by
    cases mul_eq_zero.mp ha2_mul with
    | inl h => exact h
    | inr h => exact False.elim (h_yfactor_ne h)
  -- Now substitute a1 = 0 and a2 = 0 into eq0 to get a0 = 0
  have ha0 : a0 = 0 := by
    calc a0 = a0 + 0 * Xn + 0 * Yn := by ring
      _ = a0 + a1 * Xn + a2 * Yn := by rw [ha1, ha2]
      _ = 0 := eq0
  exact ⟨ha0, ha1, ha2⟩

/-! ### 6. Power Distinctness for Positive Base > 1 -/

/-- For base tau > 1, powers tau^alpha and tau^beta are distinct whenever alpha ≠ beta. -/
theorem tau_powers_pairwise_distinct_of_ne (tau_val : ℝ) (htau : 1 < tau_val)
    (alpha beta : ℝ) (hne : alpha ≠ beta) :
    tau_val ^ alpha ≠ tau_val ^ beta := by
  intro h_eq
  have htau_pos : 0 < tau_val := by linarith
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have h_pow_lt := Real.rpow_lt_rpow_of_exponent_lt htau hlt
    exact (ne_of_lt h_pow_lt) h_eq
  · have h_pow_gt := Real.rpow_lt_rpow_of_exponent_lt htau hgt
    exact (ne_of_gt h_pow_gt) h_eq

/-- For base tau > 1, tau^alpha ≠ 1 whenever alpha ≠ 0. -/
theorem tau_pow_ne_one_of_ne_zero (tau_val : ℝ) (htau : 1 < tau_val)
    (alpha : ℝ) (hne : alpha ≠ 0) :
    tau_val ^ alpha ≠ 1 := by
  have h_zero : tau_val ^ (0 : ℝ) = 1 := Real.rpow_zero tau_val
  rw [← h_zero]
  exact tau_powers_pairwise_distinct_of_ne tau_val htau alpha 0 hne

end RiemannScope
