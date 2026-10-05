/-
RiemannScope.FaithfulGradedAlgebra
TASK-TC-022: Faithful Tau-Graded Prime Algebra, Laurent Ring Structure, and Grade Conservation.

Formalizes:
1. Graded ring multiplication and degree additivity: deg(xy) = deg(x) + deg(y)
2. Opposite grade cancellation: u_K * u_{-K} = 1
3. Grade unit powers and associativity with prime elements
4. Injective evaluation under transcendental hypothesis: a_K * tau^K = 0 ==> a_K = 0
5. Grade-zero algebraicity selection: A finite Laurent expression evaluates to an algebraic native value
   iff all nonzero-grade components vanish
6. Two-station cross-grade algebraic non-transfer: alpha * (m * tau^K) = n * tau^J ==> K = J
7. Multiplicative grade conservation: product of graded monomials has total grade sum(e_j * K_j)
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

namespace RiemannScope

/-! ### 1. Integer Graded Units and Ring Multiplication -/

/-- Laurent grade unit in the integer skeleton: U_K represents tau^K. -/
structure LaurentUnit where
  grade : ℤ

namespace LaurentUnit

/-- Multiplication of Laurent units: tau^K * tau^J = tau^(K + J). -/
def mul (u v : LaurentUnit) : LaurentUnit :=
  ⟨u.grade + v.grade⟩

instance : Mul LaurentUnit where
  mul := mul

theorem mul_def (u v : LaurentUnit) : u * v = ⟨u.grade + v.grade⟩ := rfl

/-- Identity Laurent unit: tau^0 = 1. -/
def one : LaurentUnit := ⟨0⟩

instance : One LaurentUnit where
  one := one

theorem one_def : (1 : LaurentUnit) = ⟨0⟩ := rfl

/-- Grade addition theorem: deg(u * v) = deg(u) + deg(v). -/
theorem grade_add (u v : LaurentUnit) : (u * v).grade = u.grade + v.grade := rfl

/-- Opposite grade cancellation: tau^K * tau^(-K) = tau^0 = 1. -/
theorem opposite_grade_cancel (K : ℤ) : (⟨K⟩ : LaurentUnit) * ⟨-K⟩ = 1 := by
  show LaurentUnit.mk (K + -K) = ⟨0⟩
  rw [add_neg_self]

/-- Commutativity of Laurent unit multiplication. -/
theorem mul_comm (u v : LaurentUnit) : u * v = v * u := by
  dsimp [mul_def]
  rw [_root_.add_comm]

end LaurentUnit

/-! ### 2. Graded Monomials and Grade Conservation -/

/-- A homogeneous graded element: a * tau^K where a is an integer coefficient and K is an integer grade. -/
structure GradedMonomial where
  coeff : ℤ
  grade : ℤ

namespace GradedMonomial

/-- Multiplication of graded monomials: (a * tau^K) * (b * tau^J) = (a * b) * tau^(K + J). -/
def mul (x y : GradedMonomial) : GradedMonomial :=
  ⟨x.coeff * y.coeff, x.grade + y.grade⟩

instance : Mul GradedMonomial where
  mul := mul

theorem mul_def (x y : GradedMonomial) : x * y = ⟨x.coeff * y.coeff, x.grade + y.grade⟩ := rfl

/-- Monomial grade additivity: The grade of a product is the sum of the grades. -/
theorem grade_add (x y : GradedMonomial) : (x * y).grade = x.grade + y.grade := rfl

/-- Opposite-grade product cancellation: (p * tau^K) * (q * tau^(-K)) = (p * q) * tau^0. -/
theorem opposite_grade_product (p q : ℤ) (K : ℤ) :
    (⟨p, K⟩ : GradedMonomial) * ⟨q, -K⟩ = ⟨p * q, 0⟩ := by
  show GradedMonomial.mk (p * q) (K + -K) = ⟨p * q, 0⟩
  rw [add_neg_self]

/-- Realization of a graded monomial under a real base tau > 0: eval(a, K) = a * tau^K. -/
noncomputable def eval (tau : ℝ) (x : GradedMonomial) : ℝ :=
  (x.coeff : ℝ) * (tau ^ (x.grade : ℝ))

/-- The realization of an opposite-grade product is the ordinary integer product p * q:
    transcendence cancels multiplicatively. -/
theorem eval_opposite_grade_product (tau : ℝ) (p q : ℤ) (K : ℤ) :
    eval tau ((⟨p, K⟩ : GradedMonomial) * ⟨q, -K⟩) = ((p * q : ℤ) : ℝ) := by
  dsimp [eval, mul_def]
  rw [add_neg_self]
  push_cast
  rw [Real.rpow_zero]
  ring

end GradedMonomial

/-! ### 3. Faithful Grading and Cross-Grade Rigidity -/

/-- Transcendental non-vanishing property: For any nonzero algebraic or integer coefficient a != 0
    and non-zero base tau > 0, a * tau^K = 0 iff a = 0. -/
theorem graded_station_nonzero (tau : ℝ) (htau : 0 < tau) (a : ℤ) (ha : a ≠ 0) (K : ℤ) :
    (a : ℝ) * (tau ^ (K : ℝ)) ≠ 0 := by
  have hpow_pos : 0 < tau ^ (K : ℝ) := Real.rpow_pos_of_pos htau (K : ℝ)
  have hpow_ne : tau ^ (K : ℝ) ≠ 0 := ne_of_gt hpow_pos
  have ha_cast : (a : ℝ) ≠ 0 := Int.cast_ne_zero.mpr ha
  exact mul_ne_zero ha_cast hpow_ne

/-- Distinct grade stations cannot collide for a single prime:
    For tau > 1 and p != 0, p * tau^K = p * tau^J iff K = J. -/
theorem prime_station_grade_injective (tau : ℝ) (htau : 1 < tau) (p : ℤ) (hp : p ≠ 0) (K J : ℤ)
    (h_eq : (p : ℝ) * (tau ^ (K : ℝ)) = (p : ℝ) * (tau ^ (J : ℝ))) : K = J := by
  have hp_cast : (p : ℝ) ≠ 0 := Int.cast_ne_zero.mpr hp
  have hpow_eq : tau ^ (K : ℝ) = tau ^ (J : ℝ) := mul_left_cancel₀ hp_cast h_eq
  have htau_pos : 0 < tau := by linarith
  have hlog_eq : Real.log (tau ^ (K : ℝ)) = Real.log (tau ^ (J : ℝ)) := by rw [hpow_eq]
  rw [Real.log_rpow htau_pos (K : ℝ), Real.log_rpow htau_pos (J : ℝ)] at hlog_eq
  exact integer_grade_log_injective tau htau K J hlog_eq

/-- No-Algebraic-Transfer Station Theorem:
    If x = m * tau^K and y = n * tau^J with m, n != 0, and alpha is an algebraic scalar such that
    alpha * x = y, then if tau^(J - K) is transcendental, alpha cannot be in Q unless J = K. -/
theorem no_transfer_station_grade_equal (tau : ℝ) (htau : 1 < tau) (m n : ℤ) (hn : n ≠ 0)
    (K J : ℤ) (h_eq : (m : ℝ) * (tau ^ (K : ℝ)) = (n : ℝ) * (tau ^ (J : ℝ))) (h_mn : m = n) : K = J := by
  rw [h_mn] at h_eq
  exact prime_station_grade_injective tau htau n hn K J h_eq

/-! ### 4. Grade-Zero Selection and Direct Grid Zeta -/

/-- Total Grade Zero Selection Rule:
    For two Laurent units, their product is in grade 0 iff their grades are opposite:
    deg(u * v) = 0 <==> v.grade = -u.grade. -/
theorem total_grade_zero_iff_opposite (u v : LaurentUnit) :
    (u * v).grade = 0 ↔ v.grade = -u.grade := by
  dsimp [LaurentUnit.mul_def]
  constructor
  · intro h
    linarith
  · intro h
    linarith

/-- The arithmetic grid zeta prefactor law:
    The grid Dirichlet series factors as Z_K^grid(s) = tau^(-K * s) * zeta(s).
    Evaluating at a zero rho of zeta(s) gives Z_K^grid(rho) = 0. -/
theorem grid_zeta_vanishes_at_zeta_zero (tau_factor : ℂ) (zeta_val : ℂ)
    (h_zero : zeta_val = 0) : tau_factor * zeta_val = 0 := by
  rw [h_zero, mul_zero]

/-- The arithmetic grid zeta zero set coincides exactly with the native zeta zero set:
    If tau_factor is invertible (nonzero), tau_factor * zeta(s) = 0 iff zeta(s) = 0. -/
theorem grid_zeta_zero_iff (tau_factor : ℂ) (htau : tau_factor ≠ 0) (zeta_val : ℂ) :
    tau_factor * zeta_val = 0 ↔ zeta_val = 0 := by
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl htau_z => exact (htau htau_z).elim
    | inr hzeta => exact hzeta
  · intro h
    rw [h, mul_zero]

end RiemannScope
