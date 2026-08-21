/-
RiemannScope.ZeroWorldline
Zero worldline trajectory: W_rho(k) = tau^k * rho.
Reference: docs/LEAN_FORMALIZATION_PLAN.md §7
-/

import RiemannScope.TranscendentalContinuation

namespace RiemannScope

/-- Zero worldline mapping across continuous grade k -/
noncomputable def zeroWorldline (rho : ℂ) (k : ℝ) : ℂ :=
  (gradeScale k : ℂ) * rho

/-- If rho is a zero of f, then the worldline W_rho(k) is a zero of F_tau(-, k) -/
theorem zeroWorldline_is_zero (f : ℂ → ℂ) (rho : ℂ) (k : ℝ)
    (h_zero : f rho = 0) (htau : 0 < tau) :
    extendedContinuation f k (zeroWorldline rho k) = 0 := by
  dsimp [zeroWorldline]
  rw [extendedContinuation_covariance f k rho htau]
  exact h_zero

end RiemannScope
