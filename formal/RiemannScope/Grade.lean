/-
RiemannScope.Grade
Tau-grade group structure, bilateral integer scale inverses, and grade-centering geometry.
Reference: MATH_CONTRACT.md §2, §39
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring

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
  exact mul_inv_cancel (ne_of_gt hpos)

/-- The correct critical-line center at grade K is c_K = tau^K / 2. -/
noncomputable def gradeCenter (K : ℤ) : ℝ :=
  integerGradeScale K / 2

/-- Origin dilation on complex coordinate s at grade K: s_K = tau^K * s. -/
noncomputable def gradeDilation (K : ℤ) (s : ℂ) : ℂ :=
  ⟨integerGradeScale K * s.re, integerGradeScale K * s.im⟩

/-- Centered coordinate at grade K: z_K = s_K - c_K = tau^K * (s - 1/2). -/
noncomputable def centeredGradeCoord (K : ℤ) (s : ℂ) : ℂ :=
  ⟨integerGradeScale K * s.re - gradeCenter K, integerGradeScale K * s.im⟩

/-- Exact grade-centering identity: z_K = tau^K * (s - 1/2) in ℂ. -/
theorem centeredGradeCoord_eq_tau_pow_mul_z (K : ℤ) (s : ℂ) :
    centeredGradeCoord K s = Complex.ofReal (integerGradeScale K) * (s - ⟨1 / 2, 0⟩) := by
  dsimp [centeredGradeCoord, gradeCenter, Complex.ofReal]
  apply Complex.ext
  · dsimp
    ring
  · dsimp
    ring

end RiemannScope
