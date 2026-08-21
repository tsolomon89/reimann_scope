/-
RiemannScope.RadialLeaf
Critical surface and normalized radial leaf invariance:
R_tau(s, k) = tau^(-k) * Re(s) - 1/2.
Reference: MATH_CONTRACT.md §8
-/

import RiemannScope.ZeroWorldline

namespace RiemannScope

/-- Critical surface coordinate at grade k: sigma_c(k) = tau^k / 2 -/
noncomputable def criticalSurfaceSigma (k : ℝ) : ℝ :=
  gradeScale k / 2

/-- Normalized radial leaf coordinate R_tau(s, k) -/
noncomputable def normalizedRadialLeaf (k : ℝ) (s : ℂ) : ℝ :=
  gradeScale (-k) * s.re - 1 / 2

/-- Radial leaf invariance theorem: R_tau(W_rho(k), k) = delta identically for all k -/
theorem radialLeaf_worldline_invariance (δ γ k : ℝ) (htau : 0 < tau) :
    normalizedRadialLeaf k (zeroWorldline ⟨1 / 2 + δ, γ⟩ k) = δ := by
  dsimp [normalizedRadialLeaf, zeroWorldline, gradeScale]
  simp
  have h_cancel : tau ^ (-k) * tau ^ k = 1 := by
    rw [← Real.rpow_add htau]
    simp
  calc
    tau ^ (-k) * (tau ^ k * (2⁻¹ + δ)) - 2⁻¹ = (tau ^ (-k) * tau ^ k) * (2⁻¹ + δ) - 2⁻¹ := by ring
    _ = 1 * (2⁻¹ + δ) - 2⁻¹ := by rw [h_cancel]
    _ = δ := by ring

/-- Zero is on-line (delta = 0) iff worldline lies on critical surface sigma_c(k) for all k -/
theorem radialLeaf_on_critical_surface_iff (δ γ k : ℝ) (htau : 0 < tau) :
    (zeroWorldline ⟨1 / 2 + δ, γ⟩ k).re = criticalSurfaceSigma k ↔ δ = 0 := by
  dsimp [zeroWorldline, criticalSurfaceSigma, gradeScale]
  simp
  constructor
  · intro h
    have htau_pos : 0 < tau ^ k := Real.rpow_pos_of_pos htau k
    have h1 : tau ^ k * (2⁻¹ + δ) = tau ^ k * 2⁻¹ := by
      linarith
    have h_div : 2⁻¹ + δ = 2⁻¹ := mul_left_cancel₀ (ne_of_gt htau_pos) h1
    linarith
  · intro h
    subst h
    ring

end RiemannScope
