/-
RiemannScope.CurvatureTransport
Curvature-Transport Unification, Fourier Lattice Geometry, Grade Invariants,
Reflection Pair Curvature Rigidity, Scalar No-Go Algebraic Lemmas,
and Symmetry-Complete Countermodel.
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

/-- 1. Radial unit and curvature are reciprocal at every integer grade K:
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

/-- 10. Grade-character complex product identity for continuous grade k ∈ ℝ:
    (δ + iγ) * log(tau) * k = (k * δ * log tau) + i * (k * γ * log tau). -/
theorem grade_character_complex_product (δ γ k tau : ℝ) :
    (⟨δ, γ⟩ : ℂ) * (Complex.ofReal (Real.log tau)) * (Complex.ofReal k) =
    ⟨k * δ * Real.log tau, k * γ * Real.log tau⟩ := by
  dsimp [Complex.ofReal]
  apply Complex.ext
  · dsimp; ring
  · dsimp; ring

/-- 11. Continuous grade-character modulus: |chi_rho(k)| = exp(k * delta * log tau). -/
theorem grade_character_modulus_def (δ γ k tau : ℝ) :
    Complex.abs (Complex.exp (⟨k * δ * Real.log tau, k * γ * Real.log tau⟩ : ℂ)) =
    Real.exp (k * δ * Real.log tau) := by
  rw [Complex.abs_exp]

/-- 12. Reflection-pair reciprocal modulus for continuous grade k ∈ ℝ:
    |chi_rho(k)| * |chi_{rho^#}(k)| = exp(k*delta*log tau) * exp(-k*delta*log tau) = 1. -/
theorem reflection_reciprocal_modulus_prod (δ k tau : ℝ) :
    Real.exp (k * δ * Real.log tau) * Real.exp (k * (-δ) * Real.log tau) = 1 := by
  rw [← Real.exp_add]
  have h_sum : k * δ * Real.log tau + k * (-δ) * Real.log tau = 0 := by ring
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

/-- 15. Reflection-pair defect zero-rigidity for continuous grade k ≠ 0:
    For k != 0 and tau > 1, B_rho(k) = 0 iff delta = 0. -/
theorem reflection_pair_defect_eq_zero_iff (δ k tau : ℝ) (hk : k ≠ 0) (htau : 1 < tau) :
    Real.exp (k * δ * Real.log tau) + Real.exp (- (k * δ * Real.log tau)) - 2 = 0 ↔ δ = 0 := by
  have h_log_pos : 0 < Real.log tau := Real.log_pos htau
  have h_log_ne : Real.log tau ≠ 0 := ne_of_gt h_log_pos
  let u := k * δ * Real.log tau
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
    have h_k_delta : k * δ = 0 := by
      cases mul_eq_zero.mp h_u_zero with
      | inl hkd => exact hkd
      | inr hlog => contradiction
    cases mul_eq_zero.mp h_k_delta with
    | inl hk_z => contradiction
    | inr hd => exact hd
  · intro hd
    dsimp [u]
    rw [hd, mul_zero, zero_mul]
    rw [Real.exp_zero, neg_zero, Real.exp_zero]
    ring

/-- 16. Normalized curvature transport invariant algebraic normalization:
    (2 * delta^2 * (log tau)^2) / (2 * (log tau)^2) = delta^2.
    Proves exact algebraic normalization of the second-order Taylor coefficient. -/
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

/-- 17. Strictly positive grade curvature for off-line displacement delta ≠ 0:
    2 * delta^2 * (log tau)^2 > 0 for delta != 0 and tau > 1. -/
theorem reflection_grade_curvature_pos (δ tau : ℝ) (hδ : δ ≠ 0) (htau : 1 < tau) :
    0 < 2 * δ ^ 2 * (Real.log tau) ^ 2 := by
  have h2 : (0 : ℝ) < 2 := by norm_num
  have hd2 : 0 < δ ^ 2 := sq_pos_of_ne_zero hδ
  have hlog : 0 < Real.log tau := Real.log_pos htau
  have hlog2 : 0 < (Real.log tau) ^ 2 := sq_pos_of_ne_zero (ne_of_gt hlog)
  exact mul_pos (mul_pos h2 hd2) hlog2

/-- 18. Scalar multiplier zero preservation:
    Multiplying an identically vanishing L-function by any scalar g preserves the root:
    L = 0 -> g * L = 0. -/
theorem scalar_multiplier_zero_preservation (g L : ℂ) (hL : L = 0) :
    g * L = 0 := by
  rw [hL, mul_zero]

/-- 19. Non-vanishing multiplier preserves zero divisor:
    For g ≠ 0, g * L = 0 ↔ L = 0. -/
theorem scalar_multiplier_nonzero_root_iff (g L : ℂ) (hg : g ≠ 0) :
    g * L = 0 ↔ L = 0 := by
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl hg0 => contradiction
    | inr hL0 => exact hL0
  · intro h
    rw [h, mul_zero]

/-- 20. Algebraic grade-derivative coefficient vanishing at a zero:
    For any coefficient c and grade factor g_k, if L = 0 then (c * g_k) * L = 0. -/
theorem algebraic_grade_derivative_factor_vanishing (c g_k L : ℂ) (hL : L = 0) :
    (c * g_k) * L = 0 := by
  rw [hL, mul_zero]

/-- 21. Finite positive-weighted curvature sum zero-rigidity:
    For weights w_j > 0 and squared defects d_j >= 0, sum w_j * d_j = 0 implies every d_j = 0. -/
theorem finite_positive_weight_curvature_rigidity (w d : List ℝ)
    (hw_pos : ∀ x ∈ w, 0 < x) (hd_nonneg : ∀ x ∈ d, 0 ≤ x)
    (h_len : w.length = d.length)
    (h_sum : (List.zipWith (· * ·) w d).sum = 0) :
    ∀ x ∈ d, x = 0 := by
  exact (list_weighted_sum_nonneg_eq_zero_iff w d hw_pos hd_nonneg h_len).mp h_sum

/-- 22. Centered countermodel polynomial:
    P(z) = ((z - i*gamma)^2 - delta^2) * ((z + i*gamma)^2 - delta^2). -/
noncomputable def countermodelPolynomial (δ γ : ℝ) (z : ℂ) : ℂ :=
  ((z - ⟨0, γ⟩) ^ 2 - (δ ^ 2 : ℂ)) * ((z + ⟨0, γ⟩) ^ 2 - (δ ^ 2 : ℂ))

/-- 23. Symmetry-complete countermodel polynomial is even:
    P(-z) = P(z). -/
theorem countermodelPolynomial_even (δ γ : ℝ) (z : ℂ) :
    countermodelPolynomial δ γ (-z) = countermodelPolynomial δ γ z := by
  dsimp [countermodelPolynomial]
  have h1 : -z - (⟨0, γ⟩ : ℂ) = -(z + (⟨0, γ⟩ : ℂ)) := by ring
  have h2 : -z + (⟨0, γ⟩ : ℂ) = -(z - (⟨0, γ⟩ : ℂ)) := by ring
  rw [h1, h2, neg_sq, neg_sq]
  ring

/-- 24. Exact root 1 of countermodel: z = delta + i*gamma is a zero. -/
theorem countermodelPolynomial_root_pos_pos (δ γ : ℝ) :
    countermodelPolynomial δ γ ⟨δ, γ⟩ = 0 := by
  dsimp [countermodelPolynomial]
  have h_sub : (⟨δ, γ⟩ : ℂ) - ⟨0, γ⟩ = (δ : ℂ) := by
    apply Complex.ext <;> dsimp [Complex.ofReal] <;> ring
  rw [h_sub]
  have h_diff : (δ : ℂ) ^ 2 - (δ ^ 2 : ℂ) = 0 := by
    push_cast; ring
  rw [h_diff, zero_mul]

/-- 25. Exact root 2 of countermodel: z = -delta + i*gamma is a zero. -/
theorem countermodelPolynomial_root_neg_pos (δ γ : ℝ) :
    countermodelPolynomial δ γ ⟨-δ, γ⟩ = 0 := by
  dsimp [countermodelPolynomial]
  have h_sub : (⟨-δ, γ⟩ : ℂ) - ⟨0, γ⟩ = (-δ : ℂ) := by
    apply Complex.ext <;> dsimp [Complex.ofReal] <;> ring
  rw [h_sub]
  have h_diff : (-δ : ℂ) ^ 2 - (δ ^ 2 : ℂ) = 0 := by
    push_cast; ring
  rw [h_diff, zero_mul]

/-- 26. Exact root 3 of countermodel: z = delta - i*gamma is a zero. -/
theorem countermodelPolynomial_root_pos_neg (δ γ : ℝ) :
    countermodelPolynomial δ γ ⟨δ, -γ⟩ = 0 := by
  dsimp [countermodelPolynomial]
  have h_add : (⟨δ, -γ⟩ : ℂ) + ⟨0, γ⟩ = (δ : ℂ) := by
    apply Complex.ext <;> dsimp [Complex.ofReal] <;> ring
  rw [h_add]
  have h_diff : (δ : ℂ) ^ 2 - (δ ^ 2 : ℂ) = 0 := by
    push_cast; ring
  rw [h_diff, mul_zero]

/-- 27. Exact root 4 of countermodel: z = -delta - i*gamma is a zero. -/
theorem countermodelPolynomial_root_neg_neg (δ γ : ℝ) :
    countermodelPolynomial δ γ ⟨-δ, -γ⟩ = 0 := by
  dsimp [countermodelPolynomial]
  have h_add : (⟨-δ, -γ⟩ : ℂ) + ⟨0, γ⟩ = (-δ : ℂ) := by
    apply Complex.ext <;> dsimp [Complex.ofReal] <;> ring
  rw [h_add]
  have h_diff : (-δ : ℂ) ^ 2 - (δ ^ 2 : ℂ) = 0 := by
    push_cast; ring
  rw [h_diff, mul_zero]

/-- 28. Weil involution difference:
    For rho = ⟨1/2 + delta, gamma⟩, the difference between functional reflection J(rho) = 1 - rho
    and complex conjugation C(rho) = ⟨rho.re, -rho.im⟩ is J(rho) - C(rho) = - 2 * delta. -/
theorem weil_involution_difference (δ γ : ℝ) :
    (1 : ℂ) - ⟨1/2 + δ, γ⟩ - ⟨1/2 + δ, -γ⟩ = ⟨-2 * δ, 0⟩ := by
  apply Complex.ext <;> dsimp <;> ring

/-- 29. Weil involution squared discrepancy:
    The squared norm of the involution difference is exactly 4 * delta^2:
    normSq (J(rho) - C(rho)) = 4 * delta^2. -/
theorem weil_involution_norm_sq_discrepancy (δ γ : ℝ) :
    Complex.normSq ((1 : ℂ) - ⟨1/2 + δ, γ⟩ - ⟨1/2 + δ, -γ⟩) = 4 * δ ^ 2 := by
  rw [weil_involution_difference]
  dsimp [Complex.normSq]
  ring

/-- 30. Pointwise numerator identity for the rational Weil-Hermitian curvature difference:
    (N1 + N2) - 2 * (beta * (1 - beta) + gamma^2) = 4 * delta^2. -/
theorem pointwise_weil_curvature_numerator_identity (δ γ : ℝ) :
    let β := 1/2 + δ
    let N1 := β ^ 2 + γ ^ 2
    let N2 := (1 - β) ^ 2 + γ ^ 2
    (N1 + N2) - 2 * (β * (1 - β) + γ ^ 2) = 4 * δ ^ 2 := by
  intro β N1 N2
  dsimp [N1, N2, β]
  ring

/-- 31. Pointwise rational Weil-Hermitian curvature identity:
    ((N1 + N2) - 2 * (beta * (1 - beta) + gamma^2)) / (2 * D) = (2 * delta^2) / D. -/
theorem pointwise_weil_curvature_identity_algebraic (δ γ D : ℝ) :
    let β := 1/2 + δ
    let N1 := β ^ 2 + γ ^ 2
    let N2 := (1 - β) ^ 2 + γ ^ 2
    ((N1 + N2) - 2 * (β * (1 - β) + γ ^ 2)) / (2 * D) = (2 * δ ^ 2) / D := by
  intro β N1 N2
  have h_num : (N1 + N2) - 2 * (β * (1 - β) + γ ^ 2) = 4 * δ ^ 2 :=
    pointwise_weil_curvature_numerator_identity δ γ
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  calc ((N1 + N2) - 2 * (β * (1 - β) + γ ^ 2)) / (2 * D)
    _ = (4 * δ ^ 2) / (2 * D) := by rw [h_num]
    _ = (2 * (2 * δ ^ 2)) / (2 * D) := by ring_nf
    _ = (2 / 2) * ((2 * δ ^ 2) / D) := by rw [mul_div_mul_comm]
    _ = 1 * ((2 * δ ^ 2) / D) := by rw [div_self h2]
    _ = (2 * δ ^ 2) / D := one_mul _

/-- 32. Pointwise Weil-curvature weight is strictly positive:
    For D > 0, the rational curvature weight 2 / D is strictly positive. -/
theorem pointwise_weil_curvature_weight_pos (D : ℝ) (hD : 0 < D) :
    0 < 2 / D := by
  have h2 : (0 : ℝ) < 2 := by norm_num
  exact div_pos h2 hD

/-- 33. Pointwise Weil-curvature defect is non-negative:
    For D > 0, (2 * delta^2) / D >= 0. -/
theorem pointwise_weil_curvature_nonneg (δ D : ℝ) (hD : 0 < D) :
    0 ≤ (2 * δ ^ 2) / D := by
  have h_num : 0 ≤ 2 * δ ^ 2 := by
    have h2 : (0 : ℝ) ≤ 2 := by norm_num
    have hd2 : 0 ≤ δ ^ 2 := sq_nonneg δ
    exact mul_nonneg h2 hd2
  exact div_nonneg h_num (le_of_lt hD)

/-- 34. Pointwise Weil-curvature defect zero-rigidity:
    For D > 0, (2 * delta^2) / D = 0 iff delta = 0. -/
theorem pointwise_weil_curvature_zero_iff (δ D : ℝ) (hD : 0 < D) :
    (2 * δ ^ 2) / D = 0 ↔ δ = 0 := by
  have hD_ne : D ≠ 0 := ne_of_gt hD
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  constructor
  · intro h
    have h_num : 2 * δ ^ 2 = 0 := (div_eq_zero_iff.mp h).resolve_right hD_ne
    have h_sq : δ ^ 2 = 0 := (mul_eq_zero.mp h_num).resolve_left h2
    exact sq_eq_zero_iff.mp h_sq
  · intro hd
    rw [hd]
    ring_nf

/-- 35. Coordinate-pulled affine zero worldline vanishing:
    For affine zero L(s) = (s - 1/2) - z0, pulled family L_k(s) = (tau^(-k) * (s - 1/2)) - z0,
    evaluated at moving worldline s_rho(k) = 1/2 + tau^k * z0, L_k(s_rho(k)) = 0 identically. -/
theorem coordinate_pulled_affine_zero_worldline (tau_k tau_inv_k z0 : ℂ)
    (h_inv : tau_inv_k * tau_k = 1) :
    (tau_inv_k * ((1/2 + tau_k * z0) - 1/2)) - z0 = 0 := by
  have h_sub : (1/2 + tau_k * z0 : ℂ) - 1/2 = tau_k * z0 := by ring
  rw [h_sub, ← mul_assoc, h_inv, one_mul, sub_self]

/-- 36. Unpulled static affine function evaluated at moving worldline:
    For static L(s) = (s - 1/2) - z0, evaluated at moving worldline s_rho(k) = 1/2 + tau_k * z0,
    L(s_rho(k)) = (tau_k - 1) * z0, which is generically non-zero for tau_k != 1 and z0 != 0. -/
theorem unpulled_affine_zero_worldline_eval (tau_k z0 : ℂ) :
    ((1/2 + tau_k * z0 : ℂ) - 1/2) - z0 = (tau_k - 1) * z0 := by
  ring

/-- 37. Conditional Weil-Hermitian Curvature Bridge:
    Encapsulates the exact reader-facing theorem schema for the Weil-Hermitian Curvature Bridge.
    If the arithmetic Weil-Hermitian defect Q_H(g_0) - Q_W(g_0) evaluates to 0 and equals the
    positive-weighted sum of zero curvature defects (sum_j w_j * delta_j^2),
    then every represented zero off-line displacement delta_j is zero. -/
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

/-- 38. [ALGEBRAIC_IDENTITY] Exact quartet-minus-projection resolvent difference:
    For any complex w, δ ∈ ℂ with w ≠ 0, w - δ ≠ 0, w + δ ≠ 0, and w^2 - δ^2 ≠ 0:
    1 / (w - δ) + 1 / (w + δ) - 2 / w = (2 * δ^2) / (w * (w^2 - δ^2)). -/
theorem exact_quartet_resolvent_identity (w δ : ℂ)
    (hw : w ≠ 0) (hw_sub : w - δ ≠ 0) (hw_add : w + δ ≠ 0) (hw_sq : w ^ 2 - δ ^ 2 ≠ 0) :
    1 / (w - δ) + 1 / (w + δ) - 2 / w = (2 * δ ^ 2) / (w * (w ^ 2 - δ ^ 2)) := by
  have h_prod : (w - δ) * (w + δ) = w ^ 2 - δ ^ 2 := by ring
  have h_add : 1 / (w - δ) + 1 / (w + δ) = (2 * w) / (w ^ 2 - δ ^ 2) := by
    rw [div_add_div (1 : ℂ) (1 : ℂ) hw_sub hw_add]
    have h_num : 1 * (w + δ) + (w - δ) * 1 = 2 * w := by ring
    rw [h_num, h_prod]
  rw [h_add]
  rw [div_sub_div (2 * w) (2 : ℂ) hw_sq hw]
  have h_num2 : (2 * w) * w - (w ^ 2 - δ ^ 2) * 2 = 2 * δ ^ 2 := by ring
  have h_den2 : (w ^ 2 - δ ^ 2) * w = w * (w ^ 2 - δ ^ 2) := by ring
  rw [h_num2, h_den2]

/-- 39. [ALGEBRAIC_IDENTITY] Bilateral squared-norm centering under exact opposite perturbations:
    For any complex background F ∈ ℂ and perturbation Δ ∈ ℂ:
    (Q(F, Δ) + Q(F, -Δ)) = 2 * |Δ|², where Q(F, Δ) = |F + Δ|² - |F|².
    The first-order linear cross-terms exactly cancel. -/
theorem bilateral_squared_norm_centering_exact_opposite (F Δ : ℂ) :
    (Complex.normSq (F + Δ) - Complex.normSq F) +
    (Complex.normSq (F - Δ) - Complex.normSq F) =
      2 * Complex.normSq Δ := by
  have h_sub : F - Δ = F + (-Δ) := by ring
  rw [h_sub]
  rw [complex_squared_norm_difference_expansion F Δ]
  rw [complex_squared_norm_difference_expansion F (-Δ)]
  have h_norm_neg : Complex.normSq (-Δ) = Complex.normSq Δ := by
    rw [Complex.normSq_apply, Complex.normSq_apply, Complex.neg_re, Complex.neg_im]
    ring
  have h_star_neg : starRingEnd ℂ (-Δ) = - (starRingEnd ℂ Δ) := map_neg (starRingEnd ℂ) Δ
  have h_re_neg : (F * starRingEnd ℂ (-Δ)).re = - (F * starRingEnd ℂ Δ).re := by
    rw [h_star_neg, mul_neg, Complex.neg_re]
  rw [h_norm_neg, h_re_neg]
  ring

/-- 40. [ALGEBRAIC_IDENTITY] Bilateral squared-norm sum under general perturbations:
    For any complex background F ∈ ℂ and perturbations Δ₁, Δ₂ ∈ ℂ:
    (Q(F, Δ₁) + Q(F, Δ₂)) = |Δ₁|² + |Δ₂|² + 2 * Re(F * star(Δ₁ + Δ₂)). -/
theorem bilateral_squared_norm_general_sum (F Δ₁ Δ₂ : ℂ) :
    (Complex.normSq (F + Δ₁) - Complex.normSq F) +
    (Complex.normSq (F + Δ₂) - Complex.normSq F) =
      Complex.normSq Δ₁ + Complex.normSq Δ₂ + 2 * (F * starRingEnd ℂ (Δ₁ + Δ₂)).re := by
  rw [complex_squared_norm_difference_expansion F Δ₁]
  rw [complex_squared_norm_difference_expansion F Δ₂]
  have h_star_add : starRingEnd ℂ (Δ₁ + Δ₂) = starRingEnd ℂ Δ₁ + starRingEnd ℂ Δ₂ := map_add (starRingEnd ℂ) Δ₁ Δ₂
  have h_mul_add : F * (starRingEnd ℂ Δ₁ + starRingEnd ℂ Δ₂) = F * starRingEnd ℂ Δ₁ + F * starRingEnd ℂ Δ₂ := mul_add F _ _
  rw [h_star_add, h_mul_add, Complex.add_re]
  ring

/-- 41. [ALGEBRAIC_IDENTITY] Bilateral second-order asymmetry cross-term expansion:
    When perturbations satisfy Δ₂ = -Δ₁ + h² * B, the residual linear sum is Δ₁ + Δ₂ = h² * B,
    yielding the exact algebraic identity for the cross-term:
    2 * Re(F * star(Δ₁ + Δ₂)) = 2 * h² * Re(F * star(B)). -/
theorem bilateral_second_order_asymmetry_cross_term (F Δ₁ B : ℂ) (h : ℝ) :
    let Δ₂ := -Δ₁ + (Complex.ofReal (h ^ 2)) * B
    2 * (F * starRingEnd ℂ (Δ₁ + Δ₂)).re =
      2 * (h ^ 2) * (F * starRingEnd ℂ B).re := by
  intro Δ₂
  have h_sum : Δ₁ + Δ₂ = (Complex.ofReal (h ^ 2)) * B := by
    dsimp [Δ₂]
    ring
  rw [h_sum]
  have h_star_mul : starRingEnd ℂ ((Complex.ofReal (h ^ 2)) * B) = (Complex.ofReal (h ^ 2)) * starRingEnd ℂ B := by
    rw [map_mul]
    have h_conj : starRingEnd ℂ (Complex.ofReal (h ^ 2)) = Complex.ofReal (h ^ 2) := by
      exact Complex.conj_ofReal (h ^ 2)
    rw [h_conj]
  rw [h_star_mul]
  have h_assoc : F * ((Complex.ofReal (h ^ 2)) * starRingEnd ℂ B) = (Complex.ofReal (h ^ 2)) * (F * starRingEnd ℂ B) := by ring
  rw [h_assoc]
  have h_re : ((Complex.ofReal (h ^ 2)) * (F * starRingEnd ℂ B)).re = (h ^ 2) * (F * starRingEnd ℂ B).re := by
    rw [Complex.mul_re]
    dsimp [Complex.ofReal]
    ring
  rw [h_re]
  ring

/-- 42. [NO_GO_COMPONENT] Bilateral asymmetry cross-term non-vanishing:
    If the background-asymmetry coupling Re(F * star(B)) ≠ 0 and h ≠ 0,
    then the second-order cross-term 2 * h² * Re(F * star(B)) is strictly non-zero. -/
theorem bilateral_asymmetry_cross_term_nonzero_of_re_nonzero (F B : ℂ) (h : ℝ)
    (hh : h ≠ 0) (hre : (F * starRingEnd ℂ B).re ≠ 0) :
    2 * (h ^ 2) * (F * starRingEnd ℂ B).re ≠ 0 := by
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  have hh2 : h ^ 2 ≠ 0 := pow_ne_zero 2 hh
  have h2h2 : 2 * (h ^ 2) ≠ 0 := mul_ne_zero h2 hh2
  exact mul_ne_zero h2h2 hre

/-- 43. [ALGEBRAIC_IDENTITY] Finite-T grade pullback second difference decomposition:
    For any background functional M, M(T_+) + M(T_-) - 2 * M(T) decomposes into the sum of
    individual scale variations (M(T_+) - M(T)) + (M(T_-) - M(T)). -/
theorem finite_grade_pullback_second_difference_identity (M_T M_T_plus M_T_minus : ℝ) :
    M_T_plus + M_T_minus - 2 * M_T = (M_T_plus - M_T) + (M_T_minus - M_T) := by
  ring

/-- 44. [ALGEBRAIC_IDENTITY] Complete two-height quartet resolvent sum decomposition:
    The full quartet resolvent difference is the exact sum of the upper and lower single-height resolvent differences. -/
theorem exact_full_quartet_resolvent_sum (w_plus w_minus δ : ℂ)
    (hwp : w_plus ≠ 0) (hwp_sub : w_plus - δ ≠ 0) (hwp_add : w_plus + δ ≠ 0) (hwp_sq : w_plus ^ 2 - δ ^ 2 ≠ 0)
    (hwm : w_minus ≠ 0) (hwm_sub : w_minus - δ ≠ 0) (hwm_add : w_minus + δ ≠ 0) (hwm_sq : w_minus ^ 2 - δ ^ 2 ≠ 0) :
    (1 / (w_plus - δ) + 1 / (w_plus + δ) - 2 / w_plus) +
    (1 / (w_minus - δ) + 1 / (w_minus + δ) - 2 / w_minus) =
      (2 * δ ^ 2) / (w_plus * (w_plus ^ 2 - δ ^ 2)) +
      (2 * δ ^ 2) / (w_minus * (w_minus ^ 2 - δ ^ 2)) := by
  rw [exact_quartet_resolvent_identity w_plus δ hwp hwp_sub hwp_add hwp_sq]
  rw [exact_quartet_resolvent_identity w_minus δ hwm hwm_sub hwm_add hwm_sq]

/-- 45. [ALGEBRAIC_IDENTITY] Diagonal cross-term algebraic reduction:
    (a^2 - v) * S_2 - a * S_1 = a^2 * S_2 - v * S_2 - a * S_1. -/
theorem diagonal_crossterm_algebraic_reduction (a v S1 S2 : ℝ) :
    (a ^ 2 - v) * S2 - a * S1 = a ^ 2 * S2 - v * S2 - a * S1 := by
  ring

/-- 46. [ALGEBRAIC_IDENTITY] Diagonal cross-term exact cancellation at v = v_*(a):
    For S2 ≠ 0 and v_* = a^2 - a * (S1 / S2), (a^2 - v_*) * S2 - a * S1 = 0. -/
theorem diagonal_crossterm_cancelling_variance_zero (a S1 S2 : ℝ) (hS2 : S2 ≠ 0) :
    let v_star := a ^ 2 - a * (S1 / S2)
    (a ^ 2 - v_star) * S2 - a * S1 = 0 := by
  intro v_star
  dsimp [v_star]
  have h_sub : a ^ 2 - (a ^ 2 - a * (S1 / S2)) = a * (S1 / S2) := by ring
  rw [h_sub]
  have h_mul : a * (S1 / S2) * S2 = a * S1 := by
    calc a * (S1 / S2) * S2
      _ = a * ((S1 / S2) * S2) := by ring
      _ = a * S1 := by rw [div_mul_cancel₀ S1 hS2]
  rw [h_mul, sub_self]

/-- 47. [FINITE_ANALYTIC_COMPONENT] Positivity of cancelling variance:
    For positive lower bound c > 0, S1 > 0, c * S1 ≤ S2, and a > 1 / c,
    the cancelling variance v_* = a^2 - a * (S1 / S2) is strictly positive: v_* > 0. -/
theorem cancelling_variance_pos_of_bounds (a S1 S2 c : ℝ)
    (hc : 0 < c) (hS1 : 0 < S1) (h_bound : c * S1 ≤ S2) (ha : 1 / c < a) :
    0 < a ^ 2 - a * (S1 / S2) := by
  have hS2_pos : 0 < S2 := lt_of_lt_of_le (mul_pos hc hS1) h_bound
  have h_ac : 1 < a * c := by
    have h1 : (1 / c) * c < a * c := mul_lt_mul_of_pos_right ha hc
    have h2 : (1 / c) * c = 1 := one_div_mul_cancel (ne_of_gt hc)
    linarith
  have ha_pos : 0 < a := lt_trans (one_div_pos.mpr hc) ha
  have h_strict : 1 * S1 < (a * c) * S1 := mul_lt_mul_of_pos_right h_ac hS1
  have h_trans : S1 < a * S2 := by
    calc S1
      _ = 1 * S1 := by rw [one_mul]
      _ < (a * c) * S1 := h_strict
      _ = a * (c * S1) := by ring
      _ ≤ a * S2 := mul_le_mul_of_nonneg_left h_bound (le_of_lt ha_pos)
  have h_diff_pos : 0 < a * S2 - S1 := sub_pos.mpr h_trans
  have hS2_ne : S2 ≠ 0 := ne_of_gt hS2_pos
  have h_factor : a ^ 2 - a * (S1 / S2) = (a * (a * S2 - S1)) / S2 := by
    field_simp
    ring
  rw [h_factor]
  have h_num_pos : 0 < a * (a * S2 - S1) := mul_pos ha_pos h_diff_pos
  exact div_pos h_num_pos hS2_pos

/-- 48. [FINITE_ANALYTIC_COMPONENT] Positivity of cancelling variance with log 2 bound:
    For S1 > 0, (Real.log 2) * S1 ≤ S2, and 1 / (Real.log 2) < a,
    the cancelling variance v_* = a^2 - a * (S1 / S2) is strictly positive: v_* > 0. -/
theorem cancelling_variance_pos_of_log2_bound (a S1 S2 : ℝ)
    (hS1 : 0 < S1) (h_bound : (Real.log 2) * S1 ≤ S2) (ha : 1 / (Real.log 2) < a) :
    0 < a ^ 2 - a * (S1 / S2) := by
  have h_log2_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)
  exact cancelling_variance_pos_of_bounds a S1 S2 (Real.log 2) h_log2_pos hS1 h_bound ha

/-- 49. [ALGEBRAIC_IDENTITY] General finite diagonal and off-diagonal decomposition over a Finset product:
    The sum of any bivariate functional f over s ×ˢ s decomposes into the diagonal sum (where p.1 = p.2)
    and the off-diagonal sum (where p.1 ≠ p.2). -/
theorem finset_double_sum_diag_offdiag_decomp {α : Type*} [DecidableEq α] (s : Finset α) (f : α × α → ℝ) :
    (∑ p ∈ (s ×ˢ s).filter (fun p => p.1 = p.2), f p) + (∑ p ∈ (s ×ˢ s).filter (fun p => p.1 ≠ p.2), f p) =
      ∑ p ∈ s ×ˢ s, f p := by
  have h_disj : Disjoint ((s ×ˢ s).filter (fun p => p.1 = p.2)) ((s ×ˢ s).filter (fun p => p.1 ≠ p.2)) := by
    exact Finset.disjoint_filter.mpr (fun _ _ h1 h2 => h2 h1)
  have h_union : (s ×ˢ s).filter (fun p => p.1 = p.2) ∪ (s ×ˢ s).filter (fun p => p.1 ≠ p.2) = s ×ˢ s := by
    exact Finset.filter_union_filter_neg_eq (fun p => p.1 = p.2) (s ×ˢ s)
  rw [← Finset.sum_union h_disj, h_union]

end RiemannScope






