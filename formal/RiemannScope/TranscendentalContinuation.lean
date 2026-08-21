/-
RiemannScope.TranscendentalContinuation
Generic coordinate family and covariance for transcendental continuation:
F_tau(s, k) = f(tau^(-k) * s).
Reference: MATH_CONTRACT.md §3
-/

import RiemannScope.Grade
import Mathlib.Data.Complex.Basic

namespace RiemannScope

/-- Transcendental continuation family for arbitrary complex function f -/
noncomputable def extendedContinuation (f : ℂ → ℂ) (k : ℝ) (s : ℂ) : ℂ :=
  f ((gradeScale (-k) : ℂ) * s)

/-- Coordinate covariance theorem: F_tau(tau^k * u, k) = f(u) -/
theorem extendedContinuation_covariance (f : ℂ → ℂ) (k : ℝ) (u : ℂ) (htau : 0 < tau) :
    extendedContinuation f k ((gradeScale k : ℂ) * u) = f u := by
  dsimp [extendedContinuation, gradeScale]
  have h_prod : ((tau ^ (-k) : ℝ) : ℂ) * ((tau ^ k : ℝ) : ℂ) = 1 := by
    rw [← Complex.ofReal_mul]
    have h_rpow : tau ^ (-k) * tau ^ k = 1 := by
      rw [← Real.rpow_add htau]
      simp
    rw [h_rpow]
    simp
  have h_assoc : (((tau ^ (-k) : ℝ) : ℂ) * (((tau ^ k : ℝ) : ℂ) * u)) = (((tau ^ (-k) : ℝ) : ℂ) * ((tau ^ k : ℝ) : ℂ)) * u := by
    ring
  rw [h_assoc, h_prod, one_mul]

end RiemannScope
