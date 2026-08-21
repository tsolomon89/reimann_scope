/-
RiemannScope.Grade
Tau-grade group structure and bilateral integer scale inverses.
Reference: docs/LEAN_FORMALIZATION_PLAN.md §5
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace RiemannScope

/-- Fundamental period constant tau = 2 * pi -/
noncomputable def tau : ℝ := 2 * Real.pi

/-- Grade scale map a(k) = tau^k for real k -/
noncomputable def gradeScale (k : ℝ) : ℝ :=
  tau ^ k

/-- Integer grade scale A_K = tau^K for K : ℤ -/
noncomputable def integerGradeScale (K : ℤ) : ℝ :=
  tau ^ (K : ℝ)

theorem integerGradeScale_zero : integerGradeScale 0 = 1 := by
  dsimp [integerGradeScale]
  simp

theorem integerGradeScale_neg (K : ℤ) (htau : 0 < tau) :
    integerGradeScale (-K) = (integerGradeScale K)⁻¹ := by
  dsimp [integerGradeScale]
  push_cast
  exact Real.rpow_neg (le_of_lt htau) (K : ℝ)

theorem integerGradeScale_bilateral_inverse (K : ℤ) (htau : 0 < tau) :
    integerGradeScale K * integerGradeScale (-K) = 1 := by
  rw [integerGradeScale_neg K htau]
  have hpos : 0 < integerGradeScale K := by
    dsimp [integerGradeScale]
    exact Real.rpow_pos_of_pos htau (K : ℝ)
  exact mul_inv_cancel₀ (ne_of_gt hpos)

end RiemannScope
