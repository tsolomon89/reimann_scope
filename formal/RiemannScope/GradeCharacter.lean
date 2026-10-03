/-
RiemannScope.GradeCharacter
Zero-induced grade-unit characters, unitarity criterion, and non-unitarity defect.
Reference: TASK-TC-019, MATH_CONTRACT.md §9.6
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade

namespace RiemannScope

/-- Modulus of the zero-induced grade character: |eta_rho(K)| = tau^(-K * delta). -/
noncomputable def gradeCharModulus (tau : ℝ) (delta : ℝ) (K : ℤ) : ℝ :=
  tau ^ (-(K : ℝ) * delta)

/-- Multiplicative character law on integer grades:
    |eta_rho(K + J)| = |eta_rho(K)| * |eta_rho(J)|. -/
theorem gradeCharModulus_add (tau : ℝ) (htau : 0 < tau) (delta : ℝ) (K J : ℤ) :
    gradeCharModulus tau delta (K + J) =
      gradeCharModulus tau delta K * gradeCharModulus tau delta J := by
  dsimp [gradeCharModulus]
  push_cast
  have h_exp : -((K : ℝ) + (J : ℝ)) * delta = (-(K : ℝ) * delta) + (-(J : ℝ) * delta) := by ring
  rw [h_exp, Real.rpow_add htau]

/-- Grade character at identity is 1. -/
theorem gradeCharModulus_zero (tau : ℝ) :
    gradeCharModulus tau 0 0 = 1 := by
  dsimp [gradeCharModulus]
  push_cast
  have h0 : -(0 : ℝ) * 0 = 0 := by ring
  rw [h0, Real.rpow_zero]

/-- Inversion law: |eta_rho(-K)| = |eta_rho(K)|⁻¹. -/
theorem gradeCharModulus_neg (tau : ℝ) (htau : 0 < tau) (delta : ℝ) (K : ℤ) :
    gradeCharModulus tau delta (-K) = (gradeCharModulus tau delta K)⁻¹ := by
  dsimp [gradeCharModulus]
  push_cast
  have h_neg : -(-(K : ℝ)) * delta = -(-(K : ℝ) * delta) := by ring
  rw [h_neg, Real.rpow_neg (le_of_lt htau)]

/-- A grade character is unitary if its modulus is identically 1 across all integer grades. -/
def IsUnitaryGradeChar (tau : ℝ) (delta : ℝ) : Prop :=
  ∀ K : ℤ, gradeCharModulus tau delta K = 1

/-- If delta = 0, the grade character is unitary. -/
theorem unitary_of_delta_zero (tau : ℝ) :
    IsUnitaryGradeChar tau 0 := by
  intro K
  dsimp [gradeCharModulus]
  have h0 : -(K : ℝ) * 0 = 0 := by ring
  rw [h0, Real.rpow_zero]

/-- Non-unitarity defect of the grade character:
    B_rho(K) = |eta_rho(K)| + |eta_rho(K)|⁻¹ - 2 = tau^(K*delta) + tau^(-K*delta) - 2. -/
noncomputable def nonunitarityDefect (tau : ℝ) (delta : ℝ) (K : ℤ) : ℝ :=
  tau ^ ((K : ℝ) * delta) + tau ^ (-(K : ℝ) * delta) - 2

/-- Symmetry of the defect under grade inversion: B_rho(-K) = B_rho(K). -/
theorem nonunitarityDefect_neg (tau : ℝ) (delta : ℝ) (K : ℤ) :
    nonunitarityDefect tau delta (-K) = nonunitarityDefect tau delta K := by
  dsimp [nonunitarityDefect]
  push_cast
  have h1 : (- (K : ℝ)) * delta = - ((K : ℝ) * delta) := by ring
  have h2 : - (- (K : ℝ)) * delta = (K : ℝ) * delta := by ring
  rw [h1, h2, add_comm]

/-- Zero displacement delta = 0 implies zero non-unitarity defect. -/
theorem nonunitarityDefect_zero_of_delta_zero (tau : ℝ) (K : ℤ) :
    nonunitarityDefect tau 0 K = 0 := by
  dsimp [nonunitarityDefect]
  have h1 : (K : ℝ) * 0 = 0 := by ring
  have h2 : -(K : ℝ) * 0 = 0 := by ring
  rw [h1, h2, Real.rpow_zero]
  ring

/-- Non-unitarity defect vanishes at grade 0: B_rho(0) = 0. -/
theorem nonunitarityDefect_grade_zero (tau : ℝ) (delta : ℝ) :
    nonunitarityDefect tau delta 0 = 0 := by
  dsimp [nonunitarityDefect]
  push_cast
  have h1 : (0 : ℝ) * delta = 0 := by ring
  have h2 : -(0 : ℝ) * delta = 0 := by ring
  rw [h1, h2, Real.rpow_zero]
  ring

/-- Algebraic identity: non-unitarity defect is expressed in terms of character modulus:
    B_rho(K) = |eta_rho(-K)| + |eta_rho(K)| - 2. -/
theorem nonunitarityDefect_eq_char_sum (tau : ℝ) (delta : ℝ) (K : ℤ) :
    nonunitarityDefect tau delta K =
      gradeCharModulus tau delta (-K) + gradeCharModulus tau delta K - 2 := by
  dsimp [nonunitarityDefect, gradeCharModulus]
  push_cast
  have h : -(-(K : ℝ)) * delta = (K : ℝ) * delta := by ring
  rw [h]

end RiemannScope
