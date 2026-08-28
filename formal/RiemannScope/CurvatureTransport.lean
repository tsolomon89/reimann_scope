/-
RiemannScope.CurvatureTransport
Curvature-Transport Unification, Fourier Lattice Geometry, Grade Invariants,
Reflection Pair Curvature Rigidity, and Symmetry-Complete Countermodel.
Reference: docs/CURVATURE_TRANSPORT.md, MATH_CONTRACT.md §43
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.BigOperators.Group.List
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import RiemannScope.ArithmeticBridge

namespace RiemannScope

/-- Fundamental full-turn constant tau = 2 * pi. -/
noncomputable def tauConst : ℝ := 2 * Real.pi

/-- 1. Radial unit and curvature are reciprocal at every grade K:
    r_K * kappa_K = tau^(-K) * tau^K = 1. -/
theorem radial_unit_curvature_reciprocal (K : ℤ) (tau : ℝ) (htau : 0 < tau) :
    (tau ^ (-(K : ℝ))) * (tau ^ (K : ℝ)) = 1 := by
  have h_add := (Real.rpow_add htau (-(K : ℝ)) (K : ℝ)).symm
  rw [h_add]
  have h_sum : -(K : ℝ) + (K : ℝ) = 0 := by ring
  rw [h_sum, Real.rpow_zero]

/-- 2. Grade-shift law for radius: r_{K+1} = tau^(-1) * r_K. -/
theorem grade_shift_radius (K : ℤ) (tau : ℝ) (htau : 0 < tau) :
    tau ^ (-((K + 1 : ℤ) : ℝ)) = tau ^ (-1 : ℝ) * tau ^ (-(K : ℝ)) := by
  have h_cast : (-((K + 1 : ℤ) : ℝ)) = (-1 : ℝ) + (-(K : ℝ)) := by
    push_cast; ring
  rw [h_cast, Real.rpow_add htau]

/-- 3. Grade-shift law for circle circumference: C_{K+1} = tau^(-1) * C_K. -/
theorem grade_shift_circumference (K : ℤ) (tau : ℝ) (htau : 0 < tau) :
    tau * tau ^ (-((K + 1 : ℤ) : ℝ)) = tau ^ (-1 : ℝ) * (tau * tau ^ (-(K : ℝ))) := by
  rw [grade_shift_radius K tau htau]
  ring

/-- 4. Grade-shift law for curvature: kappa_{K+1} = tau * kappa_K. -/
theorem grade_shift_curvature (K : ℤ) (tau : ℝ) (htau : 0 < tau) :
    tau ^ (((K + 1 : ℤ) : ℝ)) = tau * tau ^ (K : ℝ) := by
  have h_cast : (((K + 1 : ℤ) : ℝ)) = 1 + (K : ℝ) := by
    push_cast; ring
  rw [h_cast, Real.rpow_add htau]
  have h_one : tau ^ (1 : ℝ) = tau := Real.rpow_one tau
  rw [h_one]

/-- 5. Unit circumference at K=1: C_1 = tau * r_1 = tau * tau^(-1) = 1. -/
theorem unit_circumference_K1 (tau : ℝ) (htau : 0 < tau) :
    tau * tau ^ (-1 : ℝ) = 1 := by
  have h_inv : tau ^ (-1 : ℝ) = tau⁻¹ := Real.rpow_neg_one tau
  rw [h_inv, mul_inv_cancel (ne_of_gt htau)]

/-- 6. Angular Fourier lattice spacing: Delta omega_K = tau / C_K = tau^K,
    generating lattice L_K = tau^K * Z. -/
theorem fourier_lattice_spacing_eq (K : ℤ) (tau : ℝ) (htau : 0 < tau) :
    tau / (tau * tau ^ (-(K : ℝ))) = tau ^ (K : ℝ) := by
  have htau_ne : tau ≠ 0 := ne_of_gt htau
  have h_div : tau / (tau * tau ^ (-(K : ℝ))) = (tau / tau) * (1 / tau ^ (-(K : ℝ))) := by
    ring
  rw [h_div, div_self htau_ne, one_mul, one_div]
  rw [← Real.rpow_neg (le_of_lt htau)]
  have h_neg : -(-(K : ℝ)) = (K : ℝ) := by ring
  rw [h_neg]

/-- 7. Transported radial unit recovers invariant displacement:
    r_K * d_{rho,K} = tau^(-K) * (tau^K * delta) = delta. -/
theorem centered_radial_unit_transport (K : ℤ) (tau δ : ℝ) (htau : 0 < tau) :
    (tau ^ (-(K : ℝ))) * (tau ^ (K : ℝ) * δ) = δ := by
  rw [← mul_assoc, radial_unit_curvature_reciprocal K tau htau, one_mul]

/-- 8. Transported quadratic defect invariance: (r_K * d_{rho,K})^2 = delta^2. -/
theorem transported_squared_defect_invariance (K : ℤ) (tau δ : ℝ) (htau : 0 < tau) :
    ((tau ^ (-(K : ℝ))) * (tau ^ (K : ℝ) * δ)) ^ 2 = δ ^ 2 := by
  rw [centered_radial_unit_transport K tau δ htau]

/-- 9. Generic scale base control b > 1:
    b^(-K) * (b^K * delta) = delta for any positive base b. -/
theorem generic_scale_radial_unit_transport (b : ℝ) (hb : 0 < b) (K : ℤ) (δ : ℝ) :
    (b ^ (-(K : ℝ))) * (b ^ (K : ℝ) * δ) = δ := by
  have h_recip : (b ^ (-(K : ℝ))) * (b ^ (K : ℝ)) = 1 := by
    have h_add := (Real.rpow_add hb (-(K : ℝ)) (K : ℝ)).symm
    rw [h_add]
    have h_sum : -(K : ℝ) + (K : ℝ) = 0 := by ring
    rw [h_sum, Real.rpow_zero]
  rw [← mul_assoc, h_recip, one_mul]

/-- 10. Grade-character complex product identity:
    (δ + iγ) * log(tau) * K = (K * δ * log tau) + i * (K * γ * log tau). -/
theorem grade_character_complex_product (δ γ K tau : ℝ) :
    (⟨δ, γ⟩ : ℂ) * (Complex.ofReal (Real.log tau)) * (Complex.ofReal K) =
    ⟨K * δ * Real.log tau, K * γ * Real.log tau⟩ := by
  dsimp [Complex.ofReal]
  apply Complex.ext
  · dsimp; ring
  · dsimp; ring

/-- 11. Grade-character modulus: |chi_rho(K)| = exp(K * delta * log tau). -/
theorem grade_character_modulus_def (δ γ K tau : ℝ) :
    Complex.abs (Complex.exp (⟨K * δ * Real.log tau, K * γ * Real.log tau⟩ : ℂ)) =
    Real.exp (K * δ * Real.log tau) := by
  rw [Complex.abs_exp]

/-- 12. Reflection-pair reciprocal modulus:
    |chi_rho(K)| * |chi_{rho^#}(K)| = exp(K*delta*log tau) * exp(-K*delta*log tau) = 1. -/
theorem reflection_reciprocal_modulus_prod (δ K tau : ℝ) :
    Real.exp (K * δ * Real.log tau) * Real.exp (K * (-δ) * Real.log tau) = 1 := by
  rw [← Real.exp_add]
  have h_sum : K * δ * Real.log tau + K * (-δ) * Real.log tau = 0 := by ring
  rw [h_sum, Real.exp_zero]

/-- 13. Reflection-pair defect formula in terms of cosh:
    exp(u) + exp(-u) - 2 = 2 * (cosh(u) - 1). -/
theorem reflection_pair_defect_cosh (u : ℝ) :
    Real.exp u + Real.exp (-u) - 2 = 2 * (Real.cosh u - 1) := by
  rw [Real.cosh_eq]
  ring

/-- 14. Non-negativity of reflection-pair defect: exp(u) + exp(-u) - 2 >= 0 for all u. -/
theorem reflection_pair_defect_nonneg (u : ℝ) :
    0 ≤ Real.exp u + Real.exp (-u) - 2 := by
  have h_sq : 0 ≤ (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2 := sq_nonneg _
  have h_exp_half : Real.exp (u / 2) * Real.exp (-u / 2) = 1 := by
    rw [← Real.exp_add]
    have h_zero : u / 2 + -u / 2 = 0 := by ring
    rw [h_zero, Real.exp_zero]
  have h_expand : (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2 =
      Real.exp u + Real.exp (-u) - 2 := by
    calc (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2
      _ = (Real.exp (u / 2)) ^ 2 - 2 * (Real.exp (u / 2) * Real.exp (-u / 2)) + (Real.exp (-u / 2)) ^ 2 := by ring
      _ = Real.exp (2 * (u / 2)) - 2 * 1 + Real.exp (2 * (-u / 2)) := by
        rw [← Real.exp_nat_mul _ 2, ← Real.exp_nat_mul _ 2, h_exp_half]
        push_cast; rfl
      _ = Real.exp u + Real.exp (-u) - 2 := by
        have h1 : (2 : ℝ) * (u / 2) = u := by ring
        have h2 : (2 : ℝ) * (-u / 2) = -u := by ring
        rw [h1, h2]; ring
  rw [← h_expand]
  exact h_sq

/-- 15. Reflection-pair defect zero-rigidity:
    For K != 0 and tau > 1, B_rho(K) = 0 iff delta = 0. -/
theorem reflection_pair_defect_eq_zero_iff (δ K tau : ℝ) (hK : K ≠ 0) (htau : 1 < tau) :
    Real.exp (K * δ * Real.log tau) + Real.exp (- (K * δ * Real.log tau)) - 2 = 0 ↔ δ = 0 := by
  have h_log_pos : 0 < Real.log tau := Real.log_pos htau
  have h_log_ne : Real.log tau ≠ 0 := ne_of_gt h_log_pos
  let u := K * δ * Real.log tau
  have h_exp_half : Real.exp (u / 2) * Real.exp (-u / 2) = 1 := by
    rw [← Real.exp_add]
    have h_zero : u / 2 + -u / 2 = 0 := by ring
    rw [h_zero, Real.exp_zero]
  have h_sq_id : (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2 = Real.exp u + Real.exp (-u) - 2 := by
    calc (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2
      _ = (Real.exp (u / 2)) ^ 2 - 2 * (Real.exp (u / 2) * Real.exp (-u / 2)) + (Real.exp (-u / 2)) ^ 2 := by ring
      _ = Real.exp (2 * (u / 2)) - 2 * 1 + Real.exp (2 * (-u / 2)) := by
        rw [← Real.exp_nat_mul _ 2, ← Real.exp_nat_mul _ 2, h_exp_half]
        push_cast; rfl
      _ = Real.exp u + Real.exp (-u) - 2 := by
        have h1 : (2 : ℝ) * (u / 2) = u := by ring
        have h2 : (2 : ℝ) * (-u / 2) = -u := by ring
        rw [h1, h2]; ring
  constructor
  · intro h
    have h_sq_zero : (Real.exp (u / 2) - Real.exp (-u / 2)) ^ 2 = 0 := by
      rw [h_sq_id, h]
    have h_sub_zero : Real.exp (u / 2) - Real.exp (-u / 2) = 0 := sq_eq_zero_iff.mp h_sq_zero
    have h_exp_eq : Real.exp (u / 2) = Real.exp (-u / 2) := sub_eq_zero.mp h_sub_zero
    have h_arg_eq : u / 2 = -u / 2 := Real.exp_eq_exp.mp h_exp_eq
    have h_u_zero : u = 0 := by linarith
    dsimp [u] at h_u_zero
    have h_k_delta : K * δ = 0 := by
      cases mul_eq_zero.mp h_u_zero with
      | inl hkd => exact hkd
      | inr hlog => contradiction
    cases mul_eq_zero.mp h_k_delta with
    | inl hk => contradiction
    | inr hd => exact hd
  · intro hd
    dsimp [u]
    rw [hd, mul_zero, zero_mul]
    rw [Real.exp_zero, neg_zero, Real.exp_zero]
    ring

/-- 16. Normalized curvature transport invariant equals delta^2:
    B''(0) / (2 * (log tau)^2) = 2 * delta^2 * (log tau)^2 / (2 * (log tau)^2) = delta^2. -/
theorem native_grade_second_order_taylor_coefficient (δ tau : ℝ) (htau : 1 < tau) :
    (2 * δ ^ 2 * (Real.log tau) ^ 2) / (2 * (Real.log tau) ^ 2) = δ ^ 2 := by
  have hlog : Real.log tau ≠ 0 := ne_of_gt (Real.log_pos htau)
  have hlog2 : (Real.log tau) ^ 2 ≠ 0 := pow_ne_zero 2 hlog
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  have hdenom : 2 * (Real.log tau) ^ 2 ≠ 0 := mul_ne_zero h2 hlog2
  calc (2 * δ ^ 2 * (Real.log tau) ^ 2) / (2 * (Real.log tau) ^ 2)
    _ = (δ ^ 2 * (2 * (Real.log tau) ^ 2)) / (2 * (Real.log tau) ^ 2) := by ring_nf
    _ = δ ^ 2 * ((2 * (Real.log tau) ^ 2) / (2 * (Real.log tau) ^ 2)) := by rw [mul_div_assoc]
    _ = δ ^ 2 * 1 := by rw [div_self hdenom]
    _ = δ ^ 2 := mul_one _

/-- 17. Finite positive-weighted curvature sum zero-rigidity:
    For weights w_j > 0 and squared defects d_j >= 0, sum w_j * d_j = 0 implies every d_j = 0. -/
theorem finite_positive_weight_curvature_rigidity (w d : List ℝ)
    (hw_pos : ∀ x ∈ w, 0 < x) (hd_nonneg : ∀ x ∈ d, 0 ≤ x)
    (h_len : w.length = d.length)
    (h_sum : (List.zipWith (· * ·) w d).sum = 0) :
    ∀ x ∈ d, x = 0 := by
  exact (list_weighted_sum_nonneg_eq_zero_iff w d hw_pos hd_nonneg h_len).mp h_sum

/-- 18. Centered countermodel polynomial:
    P(z) = ((z - i*gamma)^2 - delta^2) * ((z + i*gamma)^2 - delta^2). -/
noncomputable def countermodelPolynomial (δ γ : ℝ) (z : ℂ) : ℂ :=
  ((z - ⟨0, γ⟩) ^ 2 - (δ ^ 2 : ℂ)) * ((z + ⟨0, γ⟩) ^ 2 - (δ ^ 2 : ℂ))

/-- 19. Symmetry-complete countermodel polynomial is even:
    P(-z) = P(z). -/
theorem countermodelPolynomial_even (δ γ : ℝ) (z : ℂ) :
    countermodelPolynomial δ γ (-z) = countermodelPolynomial δ γ z := by
  dsimp [countermodelPolynomial]
  have h1 : -z - (⟨0, γ⟩ : ℂ) = -(z + (⟨0, γ⟩ : ℂ)) := by ring
  have h2 : -z + (⟨0, γ⟩ : ℂ) = -(z - (⟨0, γ⟩ : ℂ)) := by ring
  rw [h1, h2, neg_sq, neg_sq]
  ring

/-- 20. Conditional Curvature Rigidity Bridge:
    Encapsulates the exact reader-facing theorem schema for Transcendental Curvature Rigidity.
    If a divisor-independent arithmetic functional evaluates to 0 and equals the positive-weighted
    sum of orbit curvatures (reconciled with delta_j^2), then every represented defect delta_j is zero. -/
structure ConditionalCurvatureRigidityBridge where
  arithmetic_functional_value : ℝ
  weights : List ℝ
  defects_sq : List ℝ
  weights_pos : ∀ w ∈ weights, 0 < w
  defects_sq_nonneg : ∀ d ∈ defects_sq, 0 ≤ d
  lengths_eq : weights.length = defects_sq.length
  bridge_identity : arithmetic_functional_value = (List.zipWith (· * ·) weights defects_sq).sum
  arithmetic_vanishes : arithmetic_functional_value = 0

theorem ConditionalCurvatureRigidityBridge.all_defects_zero
    (bridge : ConditionalCurvatureRigidityBridge) :
    ∀ d ∈ bridge.defects_sq, d = 0 := by
  have h_sum_zero : (List.zipWith (· * ·) bridge.weights bridge.defects_sq).sum = 0 := by
    rw [← bridge.bridge_identity, bridge.arithmetic_vanishes]
  exact finite_positive_weight_curvature_rigidity
    bridge.weights bridge.defects_sq
    bridge.weights_pos bridge.defects_sq_nonneg
    bridge.lengths_eq h_sum_zero

end RiemannScope
