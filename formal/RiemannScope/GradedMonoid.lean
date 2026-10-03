/-
RiemannScope.GradedMonoid
Graded arithmetic monoid, grade units, and realization homomorphisms.
Reference: MATH_CONTRACT.md §9.5, TC_GRADED_ARITHMETIC_CLOSURE.md
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Group.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade

namespace RiemannScope

/-- Graded arithmetic pair (K, n) where K is a real grade (e.g. from A_R) and n is an integer. -/
structure GradedElem where
  grade : ℝ
  val : ℤ

namespace GradedElem

/-- Graded monoid multiplication: (K, n) * (J, m) = (K + J, n * m). -/
def mul (x y : GradedElem) : GradedElem :=
  ⟨x.grade + y.grade, x.val * y.val⟩

instance : Mul GradedElem where
  mul := mul

/-- Identity element: (0, 1). -/
def one : GradedElem := ⟨0, 1⟩

instance : One GradedElem where
  one := one

theorem mul_def (x y : GradedElem) :
    x * y = ⟨x.grade + y.grade, x.val * y.val⟩ := rfl

theorem one_def : (1 : GradedElem) = ⟨0, 1⟩ := rfl

theorem mul_comm (x y : GradedElem) : x * y = y * x := by
  have h1 : x.grade + y.grade = y.grade + x.grade := _root_.add_comm x.grade y.grade
  have h2 : x.val * y.val = y.val * x.val := _root_.mul_comm x.val y.val
  dsimp [mul_def]
  rw [h1, h2]

theorem mul_assoc (x y z : GradedElem) : (x * y) * z = x * (y * z) := by
  have h1 : (x.grade + y.grade) + z.grade = x.grade + (y.grade + z.grade) := _root_.add_assoc x.grade y.grade z.grade
  have h2 : (x.val * y.val) * z.val = x.val * (y.val * z.val) := _root_.mul_assoc x.val y.val z.val
  dsimp [mul_def]
  rw [h1, h2]

theorem one_mul (x : GradedElem) : 1 * x = x := by
  cases x with
  | mk g v =>
    show GradedElem.mk (0 + g) (1 * v) = GradedElem.mk g v
    rw [zero_add, _root_.one_mul]

theorem mul_one (x : GradedElem) : x * 1 = x := by
  cases x with
  | mk g v =>
    show GradedElem.mk (g + 0) (v * 1) = GradedElem.mk g v
    rw [add_zero, _root_.mul_one]

/-- Grade unit: u_K = (K, 1). -/
def gradeUnit (K : ℝ) : GradedElem := ⟨K, 1⟩

/-- Native integer embedding: iota(n) = (0, n). -/
def nativeInt (n : ℤ) : GradedElem := ⟨0, n⟩

/-- Grade unit multiplication law: u_K * u_J = u_{K + J}. -/
theorem gradeUnit_mul (K J : ℝ) : gradeUnit K * gradeUnit J = gradeUnit (K + J) := by
  dsimp [gradeUnit, mul_def]

/-- Grade unit inverse law: u_K * u_{-K} = 1. -/
theorem gradeUnit_inv (K : ℝ) : gradeUnit K * gradeUnit (-K) = 1 := by
  show GradedElem.mk (K + -K) (1 * 1) = ⟨0, 1⟩
  rw [add_neg_self, _root_.mul_one]

/-- Canonical factorization: every element factors into a grade unit and a native integer:
    (K, n) = u_K * (0, n). -/
theorem canonical_factorization (x : GradedElem) :
    x = gradeUnit x.grade * nativeInt x.val := by
  cases x with
  | mk g v =>
    show GradedElem.mk g v = GradedElem.mk (g + 0) (1 * v)
    rw [add_zero, _root_.one_mul]

/-- Realization map: Phi_tau(K, n) = n * tau^K. -/
noncomputable def realization (tau : ℝ) (x : GradedElem) : ℝ :=
  (x.val : ℝ) * (tau ^ x.grade)

/-- Realization homomorphism on elements under real powers. -/
theorem realization_mul (tau : ℝ) (htau : 0 < tau) (x y : GradedElem) :
    realization tau (x * y) = realization tau x * realization tau y := by
  dsimp [realization, mul_def]
  push_cast
  rw [Real.rpow_add htau]
  ring

end GradedElem

end RiemannScope
