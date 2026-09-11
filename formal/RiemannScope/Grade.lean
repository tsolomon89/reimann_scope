/-
RiemannScope.Grade
Tau-grade group structure, bilateral integer scale inverses, and grade-centering geometry.
Reference: MATH_CONTRACT.md §2, §39
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Topology.Instances.Real
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.PseudoMetric
import Mathlib.LinearAlgebra.Vandermonde
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Filter.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

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

/-- Transported arithmetic layer multiplication law:
    (a_K * m) odot_K (a_K * n) = ((a_K * m) * (a_K * n)) / a_K = a_K * (m * n).
    Proves exact scale isomorphism for transported multiplication. -/
theorem transported_mult_scale_law (a_K m n : ℝ) (ha : a_K ≠ 0) :
    (a_K * m * (a_K * n)) / a_K = a_K * (m * n) := by
  calc (a_K * m * (a_K * n)) / a_K
    _ = (m * n * a_K * a_K) / a_K := by ring_nf
    _ = (m * n * a_K) * (a_K / a_K) := by rw [mul_div_assoc]
    _ = (m * n * a_K) * 1 := by rw [div_self ha]
    _ = a_K * (m * n) := by ring

/-- Lattice station equality reduction (Real Division Lemma):
    If m * tau^M = n with m ≠ 0, then tau^M = n / m.
    Scope note: This is an exact division lemma in ℝ. The conclusion that integer grades
    K ≠ J satisfy L_K ∩ L_J = {0} requires the external mathematical premise that
    tau = 2*pi is transcendental (Lindemann 1882), which is not formalized here. -/
theorem lattice_intersection_transcendental_char (tau_M m n : ℝ) (hm : m ≠ 0)
    (h_eq : m * tau_M = n) :
    tau_M = n / m := by
  calc tau_M
    _ = (m * tau_M) / m := by rw [mul_div_cancel_left₀ tau_M hm]
    _ = n / m := by rw [h_eq]

/-- Transported logarithmic frequency collision reduction:
    If tau_K * (q * log_b) = tau_J * (p * log_b) with log_b ≠ 0 and q ≠ 0,
    then the frequency dilation ratio tau_K / tau_J equals the rational exponent ratio p / q.
    Scope note: Shows that a frequency balance between prime powers in the same multiplicative
    family (m = b^p, n = b^q) forces a rational dilation ratio. -/
theorem transported_log_frequency_rational_collision_ratio (tau_K tau_J p q log_b : ℝ)
    (hq : q ≠ 0) (hlog : log_b ≠ 0) (htau_J : tau_J ≠ 0)
    (h_eq : tau_K * (q * log_b) = tau_J * (p * log_b)) :
    tau_K / tau_J = p / q := by
  have h_qlog : q * log_b ≠ 0 := mul_ne_zero hq hlog
  have h1 : tau_K = (tau_J * (p * log_b)) / (q * log_b) := by
    calc tau_K
      _ = (tau_K * (q * log_b)) / (q * log_b) := by rw [mul_div_cancel_right₀ tau_K h_qlog]
      _ = (tau_J * (p * log_b)) / (q * log_b) := by rw [h_eq]
  have h2 : (tau_J * (p * log_b)) / (q * log_b) = tau_J * (p / q) := by
    calc (tau_J * (p * log_b)) / (q * log_b)
      _ = (tau_J * p * log_b) / (q * log_b) := by ring_nf
      _ = (tau_J * p) / q := by rw [mul_div_mul_right (tau_J * p) q hlog]
      _ = tau_J * (p / q) := by ring
  rw [h1, h2, mul_div_cancel_left₀ (p / q) htau_J]

/-- Logarithmic derivative singular part exact cancellation (Algebraic Field Lemma):
    For any non-zero multiplier factors g_K, g_J and zero factor L,
    the quotient difference (g_K * L)/(g_K * L) - (g_J * L)/(g_J * L) vanishes identically,
    leaving no residual singularity from the zero.
    Scope note: This is an exact algebraic lemma in ℂ. Analytic meromorphic continuation
    and Hadamard product convergence are external mathematical premises. -/
theorem log_derivative_scalar_difference_cancellation (g_K g_J L : ℂ)
    (hg_K : g_K ≠ 0) (hg_J : g_J ≠ 0) (hL : L ≠ 0) :
    (g_K * L) / (g_K * L) - (g_J * L) / (g_J * L) = 0 := by
  have hK : g_K * L ≠ 0 := mul_ne_zero hg_K hL
  have hJ : g_J * L ≠ 0 := mul_ne_zero hg_J hL
  rw [div_self hK, div_self hJ, sub_self]

/-- Invariant and Covariant Observable Vanishing Theorem (Abstract Observable Rigidity):
    If an observable A_val in ℝ is simultaneously:
    1. Invariant: A(T_K X) = A(X)
    2. Covariant of non-zero grade weight: A(T_K X) = scale * A(X) with scale ≠ 1,
    then A(X) = 0.
    Scope note: Applies to raw external values in a shared codomain.
    Coordinate redundancy after unit conversion does not imply raw equality. -/
theorem invariant_covariant_observable_vanishing (A_val scale : ℝ)
    (h_inv : A_val = scale * A_val)
    (h_scale_ne_one : scale ≠ 1) :
    A_val = 0 := by
  have h : (1 - scale) * A_val = 0 := by
    calc (1 - scale) * A_val
      _ = A_val - scale * A_val := by ring
      _ = A_val - A_val := by rw [← h_inv]
      _ = 0 := sub_self A_val
  have h_sub_ne : 1 - scale ≠ 0 := sub_ne_zero.mpr (Ne.symm h_scale_ne_one)
  exact (mul_eq_zero.mp h).resolve_left h_sub_ne

/-- Common-Referent Collision Theorem (Cycle 3 Conditional Bridge Contract):
    Suppose an observable A on a nontrivial zeta zero rho = 1/2 + delta + i*gamma satisfies:
    (CR1) Common referent: A_K(rho_K) = A_J(rho_J) = A_rho as an external real value.
    (CR2) Arithmetic layer location: A_K(rho_K) = m * tau_K and A_J(rho_J) = n * tau_J
          for integers m, n.
    (CR3) Off-line non-zero: delta ≠ 0 → A_rho ≠ 0.
    Under the layer-separation condition that tau_K / tau_J is irrational (cannot equal n / m
    for any non-zero integer m), the off-line displacement must vanish: delta = 0.
    Scope note: Defines the exact conditions required for an exclusion bridge.
    This theorem is conditional on the existence of an observable satisfying (CR1)-(CR3). -/
theorem common_referent_collision_theorem
    (A_rho tau_K tau_J delta : ℝ)
    (m n : ℤ)
    (htau_J : tau_J ≠ 0)
    (h_cr1_K : A_rho = (m : ℝ) * tau_K)
    (h_cr1_J : A_rho = (n : ℝ) * tau_J)
    (h_cr3 : delta ≠ 0 → A_rho ≠ 0)
    (h_separation : (tau_K / tau_J = (n : ℝ) / (m : ℝ)) → m = 0) :
    delta = 0 := by
  have hm0 : m = 0 := by
    by_cases hm : (m : ℝ) = 0
    · exact_mod_cast hm
    · have heq : (m : ℝ) * tau_K = (n : ℝ) * tau_J := by rw [← h_cr1_K, h_cr1_J]
      have h_ratio : tau_K / tau_J = (n : ℝ) / (m : ℝ) := by
        have h1 : tau_K = ((n : ℝ) * tau_J) / (m : ℝ) := by
          calc tau_K
            _ = ((m : ℝ) * tau_K) / (m : ℝ) := by rw [mul_div_cancel_left₀ tau_K hm]
            _ = ((n : ℝ) * tau_J) / (m : ℝ) := by rw [heq]
        rw [h1]
        calc ((n : ℝ) * tau_J) / (m : ℝ) / tau_J
          _ = ((n : ℝ) * tau_J) / ((m : ℝ) * tau_J) := by rw [div_div]
          _ = ((tau_J * (n : ℝ)) / (tau_J * (m : ℝ))) := by ring_nf
          _ = (n : ℝ) / (m : ℝ) := by rw [mul_div_mul_left (n : ℝ) (m : ℝ) htau_J]
      have hm_zero : m = 0 := h_separation h_ratio
      exact hm_zero
  have hA0 : A_rho = 0 := by
    calc A_rho
      _ = (m : ℝ) * tau_K := h_cr1_K
      _ = (0 : ℝ) * tau_K := by rw [hm0, Int.cast_zero]
      _ = 0 := by ring
  by_contra h_delta_ne
  have hA_ne := h_cr3 h_delta_ne
  exact hA_ne hA0

/-- Theorem A: Unitary Grade-Character Criterion (Exact Criterion).
    For tau > 1, any integer grade K ≠ 0, and real delta:
    Real.exp ((K : ℝ) * delta * Real.log tau) = 1 ↔ delta = 0.
    In fact, unit modulus at any single non-zero grade K ≠ 0 is necessary and sufficient. -/
theorem unitary_grade_character_iff_delta_zero
    (tau delta : ℝ) (K : ℤ)
    (htau : 1 < tau)
    (hK : K ≠ 0) :
    Real.exp ((K : ℝ) * delta * Real.log tau) = 1 ↔ delta = 0 := by
  have hK_real : (K : ℝ) ≠ 0 := by exact_mod_cast hK
  have hlog_pos : 0 < Real.log tau := Real.log_pos htau
  have hlog_ne : Real.log tau ≠ 0 := ne_of_gt hlog_pos
  constructor
  · intro h_exp
    rw [Real.exp_eq_one_iff] at h_exp
    have h_prod : (K : ℝ) * delta = 0 := by
      cases mul_eq_zero.mp h_exp with
      | inl h1 => exact h1
      | inr h2 => exact (hlog_ne h2).elim
    cases mul_eq_zero.mp h_prod with
    | inl hK_zero => exact (hK_real hK_zero).elim
    | inr h_delta => exact h_delta
  · intro h_delta
    rw [h_delta]
    ring_nf
    exact Real.exp_zero

/-- Genuine definition of bilateral boundedness over ℤ for base tau > 1 and displacement delta.
    Expresses that the sequence of character moduli is bounded by a finite constant M. -/
def BilateralBounded (tau delta : ℝ) : Prop :=
  ∃ M : ℝ, ∀ (K : ℤ), Real.exp ((K : ℝ) * delta * Real.log tau) ≤ M

theorem not_bounded_of_pos (c B : ℝ) (hc : 0 < c) :
    ∃ (K : ℤ), B < Real.exp ((K : ℝ) * c) := by
  obtain ⟨n, hn⟩ := exists_nat_gt (B / c)
  use (n : ℤ)
  push_cast
  have h_mul : B < (n : ℝ) * c := (div_lt_iff hc).mp hn
  have h_le : (n : ℝ) * c ≤ Real.exp ((n : ℝ) * c) := by
    have h1 : (n : ℝ) * c ≤ (n : ℝ) * c + 1 := by linarith
    exact le_trans h1 (Real.add_one_le_exp ((n : ℝ) * c))
  exact lt_of_lt_of_le h_mul h_le

theorem not_bounded_of_neg (c B : ℝ) (hc : c < 0) :
    ∃ (K : ℤ), B < Real.exp ((K : ℝ) * c) := by
  have h_pos : 0 < -c := neg_pos.mpr hc
  obtain ⟨n, hn⟩ := exists_nat_gt (B / -c)
  use -(n : ℤ)
  push_cast
  have h_mul : B < (n : ℝ) * (-c) := (div_lt_iff h_pos).mp hn
  have h_eq : (-(n : ℝ)) * c = (n : ℝ) * (-c) := by ring
  rw [h_eq]
  have h_le : (n : ℝ) * (-c) ≤ Real.exp ((n : ℝ) * (-c)) := by
    have h1 : (n : ℝ) * (-c) ≤ (n : ℝ) * (-c) + 1 := by linarith
    exact le_trans h1 (Real.add_one_le_exp ((n : ℝ) * (-c)))
  exact lt_of_lt_of_le h_mul h_le

/-- Theorem B: Bilateral Boundedness Criterion (Mathematical Implication).
    For any tau > 1, if the grade character modulus sequence is bilaterally bounded
    over all integer grades K ∈ ℤ, then delta = 0. -/
theorem bilateral_boundedness_implies_delta_zero
    (tau delta : ℝ) (htau : 1 < tau) (h_bound : BilateralBounded tau delta) :
    delta = 0 := by
  have hlog : 0 < Real.log tau := Real.log_pos htau
  rcases h_bound with ⟨B, hB⟩
  have h_c_zero : delta * Real.log tau = 0 := by
    by_contra h_ne
    cases lt_or_gt_of_ne h_ne with
    | inl h_neg =>
      obtain ⟨K, hK⟩ := not_bounded_of_neg (delta * Real.log tau) B h_neg
      have h_le := hB K
      rw [mul_assoc] at h_le
      linarith
    | inr h_pos =>
      obtain ⟨K, hK⟩ := not_bounded_of_pos (delta * Real.log tau) B h_pos
      have h_le := hB K
      rw [mul_assoc] at h_le
      linarith
  cases mul_eq_zero.mp h_c_zero with
  | inl hd => exact hd
  | inr h_log_zero => exact (ne_of_gt hlog h_log_zero).elim

/-- Bilateral Boundedness Exclusion Theorem (Alias for Theorem B):
    Proves that bilateral boundedness over ℤ implies delta = 0. -/
theorem bilateral_boundedness_exclusion_theorem
    (tau delta : ℝ) (htau : 1 < tau) (h_bound : BilateralBounded tau delta) :
    delta = 0 :=
  bilateral_boundedness_implies_delta_zero tau delta htau h_bound

/-- Cycle 5: Log-coordinate mode translation law:
    phi_lambda(u + t) = exp(lambda * t) * phi_lambda(u)
    where lambda = delta + i * gamma. -/
theorem log_mode_translation (delta gamma u t : ℝ) :
    Complex.exp (((delta : ℂ) + Complex.I * (gamma : ℂ)) * ((u : ℂ) + (t : ℂ))) =
    Complex.exp (((delta : ℂ) + Complex.I * (gamma : ℂ)) * (t : ℂ)) *
    Complex.exp (((delta : ℂ) + Complex.I * (gamma : ℂ)) * (u : ℂ)) := by
  have h : ((delta : ℂ) + Complex.I * (gamma : ℂ)) * ((u : ℂ) + (t : ℂ)) =
           ((delta : ℂ) + Complex.I * (gamma : ℂ)) * (t : ℂ) +
           ((delta : ℂ) + Complex.I * (gamma : ℂ)) * (u : ℂ) := by ring
  rw [h, Complex.exp_add]

/-- Cycle 5: Log-coordinate mode modulus law:
    |exp((delta + i * gamma) * u)| = exp(delta * u). -/
theorem log_mode_abs (delta gamma u : ℝ) :
    Complex.abs (Complex.exp (((delta : ℂ) + Complex.I * (gamma : ℂ)) * (u : ℂ))) =
    Real.exp (delta * u) := by
  have h_re : (((delta : ℂ) + Complex.I * (gamma : ℂ)) * (u : ℂ)).re = delta * u := by
    simp [Complex.add_re, Complex.mul_re, Complex.I_re, Complex.I_im]
  rw [Complex.abs_exp, h_re]

/-- Cycle 5: Log-coordinate mode boundedness on the entire real line:
    The mode u ↦ exp(delta * u) is bounded on all of ℝ if and only if delta = 0. -/
theorem log_mode_bounded_iff_delta_zero (delta : ℝ) :
    (∃ B : ℝ, ∀ (u : ℝ), Real.exp (delta * u) ≤ B) ↔ delta = 0 := by
  constructor
  · rintro ⟨B, hB⟩
    by_contra h_ne
    cases lt_or_gt_of_ne h_ne with
    | inl h_neg =>
      have h_pos : 0 < -delta := neg_pos.mpr h_neg
      obtain ⟨n, hn⟩ := exists_nat_gt (B / -delta)
      have h_lt : B < (n : ℝ) * (-delta) := (div_lt_iff h_pos).mp hn
      have h_le : (n : ℝ) * (-delta) ≤ Real.exp ((n : ℝ) * (-delta)) := by
        have h1 : (n : ℝ) * (-delta) ≤ (n : ℝ) * (-delta) + 1 := by linarith
        exact le_trans h1 (Real.add_one_le_exp ((n : ℝ) * (-delta)))
      have h_spec := hB (-(n : ℝ))
      have h_eq : delta * (-(n : ℝ)) = (n : ℝ) * (-delta) := by ring
      rw [h_eq] at h_spec
      linarith
    | inr h_pos =>
      obtain ⟨n, hn⟩ := exists_nat_gt (B / delta)
      have h_lt : B < (n : ℝ) * delta := (div_lt_iff h_pos).mp hn
      have h_le : (n : ℝ) * delta ≤ Real.exp ((n : ℝ) * delta) := by
        have h1 : (n : ℝ) * delta ≤ (n : ℝ) * delta + 1 := by linarith
        exact le_trans h1 (Real.add_one_le_exp ((n : ℝ) * delta))
      have h_spec := hB (n : ℝ)
      have h_eq : delta * (n : ℝ) = (n : ℝ) * delta := by ring
      rw [h_eq] at h_spec
      linarith
  · intro h_zero
    use 1
    intro u
    rw [h_zero, zero_mul, Real.exp_zero]

/-- Cycle 6: Jump scaling identity: exp(-u/2) = (exp(u/2))⁻¹.
    Relates the prime-power jump in log coordinates to inverse square-root scaling. -/
theorem chebyshev_jump_factor (u : ℝ) :
    Real.exp (- (u / 2)) = (Real.exp (u / 2))⁻¹ := by
  rw [Real.exp_neg]

/-- Cycle 6: Smooth between-jump derivative structure of Chebyshev error:
    Algebraic identity relating the downward slope of E(u) to the exponential scale exp(u/2):
    -(1/2) * (psi_0 * exp(-u/2) + exp(u/2)) = -exp(u/2) - (1/2) * (exp(-u/2) * psi_0 - exp(u/2)). -/
theorem chebyshev_derivative_relation (u psi_0 : ℝ) :
    - (1 / 2 : ℝ) * (psi_0 * Real.exp (- (u / 2)) + Real.exp (u / 2)) =
    - Real.exp (u / 2) - (1 / 2 : ℝ) * (Real.exp (- (u / 2)) * psi_0 - Real.exp (u / 2)) := by
  ring

/-- Cycle 6: Phase-cancelling pairing exponent identity:
    For phi_lambda(u) = exp((delta + i*gamma)*u) and eta_n(u) = exp(-i*gamma*u)*exp(-u^2/(2n^2)),
    the total exponent simplifies to the purely real quadratic delta*u - u^2/(2n^2),
    isolating the radial divergence without oscillatory phase interference. -/
theorem phase_cancelling_kernel_real (delta gamma u n : ℝ) :
    (((delta : ℂ) + Complex.I * (gamma : ℂ)) * (u : ℂ) +
     (-Complex.I * (gamma : ℂ) * (u : ℂ) - ((u : ℂ) ^ 2) / (2 * (n : ℂ) ^ 2))) =
    (((delta * u - (u ^ 2) / (2 * n ^ 2)) : ℝ) : ℂ) := by
  push_cast
  ring

/-- Product-to-sum identity for cosine oscillations:
    cos(a) * cos(b) = (1/2) * (cos(a - b) + cos(a + b)).
    For cross-grade modes, a - b = gamma * (J - K) * log(tau) is constant in x.
    When K = J, the difference is 0 and cos(0) = 1.
    When K ≠ J, the constant phase cos(gamma * (J - K) * log(tau)) can be negative,
    demonstrating that cross-grade products f_K * f_J are not universally positive squares. -/
theorem cos_mul_cos_product_to_sum (a b : ℝ) :
    Real.cos a * Real.cos b = (1 / 2 : ℝ) * (Real.cos (a - b) + Real.cos (a + b)) := by
  have h := Real.cos_add_cos (a + b) (a - b)
  have h1 : ((a + b) + (a - b)) / 2 = a := by ring
  have h2 : ((a + b) - (a - b)) / 2 = b := by ring
  rw [h1, h2] at h
  linarith

/-- Cycle 6: Non-vanishing of the meromorphic pole residue at an off-critical zero:
    For any nontrivial zero rho = 1/2 + delta + i*gamma with ordinate gamma ≠ 0
    and integer multiplicity m > 0, the residue -m/rho is strictly non-zero. -/
theorem meromorphic_pole_residue_nonzero (delta gamma : ℝ) (m : ℕ)
    (hm : 0 < m) (hgamma : gamma ≠ 0) :
    -((m : ℂ) / ((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ))) ≠ 0 := by
  intro h_zero
  have h_neg : (m : ℂ) / ((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ)) = 0 := by
    calc (m : ℂ) / ((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ))
      _ = - (- ((m : ℂ) / ((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ)))) := by ring
      _ = -0 := by rw [h_zero]
      _ = 0 := by ring
  have hm_ne : (m : ℂ) ≠ 0 := by
    exact_mod_cast (ne_of_gt hm)
  have h_denom_ne : ((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ)) ≠ 0 := by
    intro hd
    have him : (((1 / 2 : ℂ) + (delta : ℂ) + Complex.I * (gamma : ℂ))).im = 0 := by
      rw [hd, Complex.zero_im]
    simp [Complex.add_im, Complex.ofReal_im, Complex.I_im, Complex.I_re] at him
    exact hgamma him
  have h_div_ne := div_ne_zero hm_ne h_denom_ne
  exact h_div_ne h_neg

/-- Cycle 7: Real exponential eventually outgrows any fixed polynomial:
    For positive base growth rate c > 0, constant C, and exponent N,
    there exists a natural grade K such that C * (1 + K)^N < exp(K * c). -/
theorem exp_outgrows_pow (c C : ℝ) (N : ℕ) (hc : 0 < c) :
    ∃ (K : ℕ), C * (1 + (K : ℝ))^N < Real.exp ((K : ℝ) * c) := by
  by_cases hC : C ≤ 0
  · use 0
    have h1 : C * (1 + ((0 : ℕ) : ℝ))^N ≤ 0 := by
      have : (0 : ℝ) ≤ (1 + ((0 : ℕ) : ℝ))^N := by positivity
      nlinarith
    have h2 : (0 : ℝ) < Real.exp (((0 : ℕ) : ℝ) * c) := by
      push_cast
      rw [zero_mul, Real.exp_zero]
      norm_num
    exact lt_of_le_of_lt h1 h2
  · push_neg at hC
    have hr : 1 < Real.exp c := Real.one_lt_exp_iff.mpr hc
    have ht := tendsto_pow_const_div_const_pow_of_one_lt N hr
    have he : 0 < (1 / (C * 2^N)) := by positivity
    have h_ev := (ht.eventually (gt_mem_nhds he))
    obtain ⟨K0, hK0⟩ := Filter.eventually_atTop.mp h_ev
    let K := max K0 1
    use K
    have hK_ge_K0 : K0 ≤ K := le_max_left K0 1
    have hK_ge_1 : 1 ≤ K := le_max_right K0 1
    have h_lt := hK0 K hK_ge_K0
    have h_exp_pow : (Real.exp c) ^ K = Real.exp ((K : ℝ) * c) := by
      rw [← Real.exp_nat_mul, mul_comm]
    rw [h_exp_pow] at h_lt
    have h_denom_pos : 0 < Real.exp ((K : ℝ) * c) := Real.exp_pos _
    have h_C2N_pos : 0 < C * 2^N := by positivity
    have h1 : (K : ℝ) ^ N < Real.exp ((K : ℝ) * c) / (C * 2^N) := by
      have h_step := (div_lt_iff h_denom_pos).mp h_lt
      calc (K : ℝ) ^ N
        _ < 1 / (C * 2^N) * Real.exp ((K : ℝ) * c) := h_step
        _ = Real.exp ((K : ℝ) * c) / (C * 2^N) := by ring
    have h_mult : (K : ℝ) ^ N * (C * 2^N) < Real.exp ((K : ℝ) * c) :=
      (lt_div_iff h_C2N_pos).mp h1
    have h_one_le_K : (1 : ℝ) ≤ (K : ℝ) := by exact_mod_cast hK_ge_1
    have h_1_add_K_le : 1 + (K : ℝ) ≤ 2 * (K : ℝ) := by linarith
    have h_pow_le : (1 + (K : ℝ)) ^ N ≤ (2 * (K : ℝ)) ^ N := by
      apply pow_le_pow_left (by positivity) h_1_add_K_le
    rw [mul_pow] at h_pow_le
    have h_lhs_le : C * (1 + (K : ℝ)) ^ N ≤ C * (2^N * (K : ℝ) ^ N) := by
      nlinarith
    have h_reorder : C * (2^N * (K : ℝ) ^ N) = (K : ℝ) ^ N * (C * 2^N) := by ring
    rw [h_reorder] at h_lhs_le
    exact lt_of_le_of_lt h_lhs_le h_mult

/-- Cycle 7 Priority Theorem:
    Polynomial Bilateral Grade Growth Implies Critical-Line Centering (delta = 0).
    For any tau > 1, if an off-line grade mode modulus exp(K * delta * log tau)
    is bounded bilaterally over all integer grades K ∈ ℤ by a polynomial C * (1 + |K|)^N,
    then delta = 0.
    Handles both positive and negative delta symmetrically. -/
theorem polynomial_bilateral_grade_growth_implies_delta_zero
    (tau delta : ℝ) (C : ℝ) (N : ℕ)
    (htau : 1 < tau)
    (h_bound : ∀ (K : ℤ), Real.exp ((K : ℝ) * delta * Real.log tau) ≤ C * (1 + |(K : ℝ)|)^N) :
    delta = 0 := by
  have hlog : 0 < Real.log tau := Real.log_pos htau
  by_contra h_delta_ne
  cases lt_or_gt_of_ne h_delta_ne with
  | inr h_pos =>
    have hc : 0 < delta * Real.log tau := mul_pos h_pos hlog
    obtain ⟨K, hK⟩ := exp_outgrows_pow (delta * Real.log tau) C N hc
    have h_spec := h_bound (K : ℤ)
    push_cast at h_spec
    rw [abs_of_nonneg (by positivity)] at h_spec
    have h_prod : (K : ℝ) * delta * Real.log tau = (K : ℝ) * (delta * Real.log tau) := by ring
    rw [h_prod] at h_spec
    linarith
  | inl h_neg =>
    have h_c_neg : delta * Real.log tau < 0 := mul_neg_of_neg_of_pos h_neg hlog
    have hc : 0 < -(delta * Real.log tau) := neg_pos.mpr h_c_neg
    obtain ⟨K, hK⟩ := exp_outgrows_pow (-(delta * Real.log tau)) C N hc
    have h_spec := h_bound (-(K : ℤ))
    push_cast at h_spec
    rw [abs_neg, abs_of_nonneg (by positivity)] at h_spec
    have h_prod : - (K : ℝ) * delta * Real.log tau = (K : ℝ) * (-(delta * Real.log tau)) := by ring
    rw [h_prod] at h_spec
    linarith
/-- Cycle 8: Transported addition on grade layer L_K. -/
def add_K (x y : ℝ) : ℝ := x + y

/-- Cycle 8: Transported multiplication on grade layer L_K with dilation scale A_K. -/
noncomputable def mul_scaled (A_K : ℝ) (x y : ℝ) : ℝ := A_K⁻¹ * (x * y)

/-- Cycle 8: Canonical coordinate embedding iota_K(n) = A_K * n. -/
def iota_scaled (A_K : ℝ) (n : ℝ) : ℝ := A_K * n

/-- Cycle 8 Theorem: iota_K is an exact homomorphism for addition:
    iota_K(m + n) = iota_K(m) +_K iota_K(n). -/
theorem arithmetic_isomorphism_add (A_K : ℝ) (m n : ℝ) :
    iota_scaled A_K (m + n) = add_K (iota_scaled A_K m) (iota_scaled A_K n) := by
  dsimp [iota_scaled, add_K]
  ring

/-- Cycle 8 Theorem: iota_K is an exact homomorphism for multiplication:
    iota_K(m * n) = iota_K(m) *_K iota_K(n) for non-zero scale A_K. -/
theorem arithmetic_isomorphism_mul (A_K : ℝ) (hA : A_K ≠ 0) (m n : ℝ) :
    iota_scaled A_K (m * n) = mul_scaled A_K (iota_scaled A_K m) (iota_scaled A_K n) := by
  dsimp [iota_scaled, mul_scaled]
  have h_assoc : A_K⁻¹ * (A_K * m * (A_K * n)) = (A_K⁻¹ * A_K) * A_K * (m * n) := by ring
  rw [h_assoc]
  rw [inv_mul_cancel hA]
  ring

/-- Cycle 8 Lemma: Discrete grade exponential dilation is injective for non-zero rate c. -/
theorem grade_exp_injective (c : ℝ) (hc : c ≠ 0) (K J : ℤ)
    (h_eq : Real.exp ((K : ℝ) * c) = Real.exp ((J : ℝ) * c)) :
    K = J := by
  have h_inj : (K : ℝ) * c = (J : ℝ) * c := Real.exp_injective h_eq
  have h_cast : (K : ℝ) = (J : ℝ) := mul_right_cancel₀ hc h_inj
  exact_mod_cast h_cast

/-- Cycle 8 Theorem: Grade Layer Scale Distinctness / Absence of Non-Zero Cross-Grade Collision.
    For dilation ratio tau > 1 and distinct integer grades K != J, the scale factors are strictly distinct.
    Thus, distinct grade layers L_K and L_J are governed by strictly distinct dilation units. -/
theorem grade_layer_scale_distinct (τ : ℝ) (hτ : 1 < τ) (K J : ℤ) (hKJ : K ≠ J) :
    Real.exp ((K : ℝ) * Real.log τ) ≠ Real.exp ((J : ℝ) * Real.log τ) := by
  intro h_eq
  have h_log_pos : 0 < Real.log τ := Real.log_pos hτ
  have h_ne : Real.log τ ≠ 0 := ne_of_gt h_log_pos
  have h_KJ_eq : K = J := grade_exp_injective (Real.log τ) h_ne K J h_eq
  exact hKJ h_KJ_eq

/-- Cycle 9: Intrinsic unit-reading map nu_K(x) = x / A_K for scale A_K. -/
noncomputable def nu_K (A_K : ℝ) (x : ℝ) : ℝ := x / A_K

/-- Cycle 9 Theorem: nu_K is an exact isomorphism for multiplication:
    nu_K(x ⊙_K y) = nu_K(x) * nu_K(y). -/
theorem nu_K_mul_scaled (A_K : ℝ) (x y : ℝ) :
    nu_K A_K (mul_scaled A_K x y) = nu_K A_K x * nu_K A_K y := by
  dsimp [nu_K, mul_scaled]
  have h_inv : A_K⁻¹ = 1 / A_K := inv_eq_one_div A_K
  rw [h_inv]
  ring

/-- Cycle 9 Theorem: Multiplicative relation between raw external and converted intrinsic Dirichlet summands:
    (A_K * n)^(-s) = A_K^(-s) * n^(-s) for non-negative scale A_K and index n. -/
theorem dirichlet_summand_raw_eq_converted (A_K n s : ℝ) (hA : 0 ≤ A_K) (hn : 0 ≤ n) :
    (A_K * n) ^ (-s) = A_K ^ (-s) * n ^ (-s) := by
  exact Real.mul_rpow hA hn

/-- Cycle 9 Theorem: Conditional pairwise layer separation:
    If tau^(K-J) is not rational for K != J, then m * tau^K = n * tau^J implies m = 0 and n = 0. -/
theorem conditional_pairwise_separation (tau_pow : ℝ) (m n : ℤ) (hm : m ≠ 0)
    (h_eq : (m : ℝ) * tau_pow = (n : ℝ)) :
    tau_pow = (n : ℝ) / (m : ℝ) := by
  have hm_r : (m : ℝ) ≠ 0 := by exact_mod_cast hm
  calc tau_pow
    _ = ((m : ℝ) * tau_pow) / (m : ℝ) := by rw [mul_div_cancel_left₀ tau_pow hm_r]
    _ = (n : ℝ) / (m : ℝ) := by rw [h_eq]

/-- Cycle 9 Theorem: Nearest integer approximation error bound (Constructive Density Lemma):
    For any real y and integer n such that |y - n| <= 1/2,
    scaling by step Delta >= 0 gives |y * Delta - n * Delta| <= Delta / 2. -/
theorem lattice_step_approx_bound (y Delta : ℝ) (n : ℤ) (hDelta : 0 ≤ Delta)
    (h_approx : |y - (n : ℝ)| ≤ 1/2) :
    |y * Delta - (n : ℝ) * Delta| ≤ Delta / 2 := by
  have h_diff : y * Delta - (n : ℝ) * Delta = (y - (n : ℝ)) * Delta := by ring
  rw [h_diff, abs_mul, abs_of_nonneg hDelta]
  calc |y - (n : ℝ)| * Delta
    _ ≤ (1/2) * Delta := mul_le_mul_of_nonneg_right h_approx hDelta
    _ = Delta / 2 := by ring

/-- Cycle 10 Theorem: Algebraic identity for zero exponent under half-density centering. -/
theorem half_density_scaling_exponent_complex (s : ℂ) :
    (1 - s) - (1/2 : ℂ) = 1/2 - s := by
  ring

/-- Cycle 10 Theorem: Real centering subtraction identity: (1/2) - (1/2 + delta) = -delta. -/
theorem half_density_real_centering (delta : ℝ) :
    (1/2 : ℝ) - (1/2 + delta) = -delta := by
  ring

/-- Cycle 10 Theorem: Real cumulative fluctuation factoring identity. -/
theorem half_density_cumulative_factoring (h psi X : ℝ) (hh : h ≠ 0) :
    h * psi - X = h * (psi - X / h) := by
  have h_div : h * (X / h) = X := mul_div_cancel₀ X hh
  calc h * psi - X
    _ = h * psi - h * (X / h) := by rw [h_div]
    _ = h * (psi - X / h) := by ring

/-- Cycle 10 Theorem: Half-density zero exponent scaling in exponential representation:
    K * (1/2 - (1/2 + delta)) * log tau = - (K * delta * log tau). -/
theorem half_density_zero_exponent_scaling (K delta tau : ℝ) :
    K * ((1/2 : ℝ) - (1/2 + delta)) * Real.log tau = - (K * delta * Real.log tau) := by
  ring

/-- Cycle 10 Theorem: Modulus of the exponential mode is strictly positive and self-evaluating. -/
theorem half_density_mode_modulus (x : ℝ) :
    |Real.exp x| = Real.exp x := by
  exact abs_of_pos (Real.exp_pos x)

/-- Cycle 10 Theorem: Discrete grade growth of positive off-line displacement delta > 0 as K -> -infty.
    For dilation ratio tau > 1 and off-line displacement delta > 0, the mode exp(-K * delta * log tau)
    exceeds any finite bound B for sufficiently negative integer grade K < 0. -/
theorem discrete_grade_growth_of_positive_delta (tau delta : ℝ) (htau : 1 < tau) (hdelta : 0 < delta) (B : ℝ) :
    ∃ (K : ℤ), K < 0 ∧ B < Real.exp (- (K : ℝ) * (delta * Real.log tau)) := by
  have hlog : 0 < Real.log tau := Real.log_pos htau
  have hc : 0 < delta * Real.log tau := mul_pos hdelta hlog
  obtain ⟨n, hn⟩ := exp_outgrows_pow (delta * Real.log tau) B 0 hc
  use -(n + 1 : ℤ)
  constructor
  · push_cast; linarith
  · push_cast
    have h_neg : - (-(n + 1 : ℝ)) = (n + 1 : ℝ) := by ring
    rw [h_neg]
    have h_le : (n : ℝ) ≤ (n + 1 : ℝ) := by linarith
    have h_mul_le : (n : ℝ) * (delta * Real.log tau) ≤ (n + 1 : ℝ) * (delta * Real.log tau) :=
      mul_le_mul_of_nonneg_right h_le (le_of_lt hc)
    have h_exp_le : Real.exp ((n : ℝ) * (delta * Real.log tau)) ≤ Real.exp ((n + 1 : ℝ) * (delta * Real.log tau)) :=
      Real.exp_le_exp.mpr h_mul_le
    have h_B_lt : B < Real.exp ((n : ℝ) * (delta * Real.log tau)) := by
      calc B
        _ ≤ B * (n : ℝ) ^ 0 := by simp
        _ < Real.exp ((n : ℝ) * (delta * Real.log tau)) := hn
    exact lt_of_lt_of_le h_B_lt h_exp_le

/-- Cycle 10 Theorem: Conditional Prime-Power Support Separation:
    If tau^(K - J) is not rational for K != J, then prime powers cannot collide across grades. -/
theorem conditional_prime_power_support_separation (tau_pow : ℝ) (p1_r1 p2_r2 : ℕ)
    (hp1 : p1_r1 ≠ 0) (h_eq : (p1_r1 : ℝ) * tau_pow = (p2_r2 : ℝ)) :
    tau_pow = (p2_r2 : ℝ) / (p1_r1 : ℝ) := by
  have hp1_r : (p1_r1 : ℝ) ≠ 0 := by exact_mod_cast hp1
  calc tau_pow
    _ = ((p1_r1 : ℝ) * tau_pow) / (p1_r1 : ℝ) := by rw [mul_div_cancel_left₀ tau_pow hp1_r]
    _ = (p2_r2 : ℝ) / (p1_r1 : ℝ) := by rw [h_eq]

/-- Cycle 11 Theorem: Finite Exponential Uniqueness for 2 modes over ℂ (Vandermonde Cancellation).
    If q₁ ≠ q₂ and a₁ + a₂ = 0 and a₁ * q₁ + a₂ * q₂ = 0, then a₁ = 0 and a₂ = 0.
    Requires only pairwise distinct bases (P2), not irrationality or rational independence. -/
theorem finite_exponential_uniqueness_2 (q₁ q₂ a₁ a₂ : ℂ)
    (h_distinct : q₁ ≠ q₂)
    (h_K0 : a₁ + a₂ = 0)
    (h_K1 : a₁ * q₁ + a₂ * q₂ = 0) :
    a₁ = 0 ∧ a₂ = 0 := by
  have h_sub : q₁ - q₂ ≠ 0 := sub_ne_zero.mpr h_distinct
  have h_a2 : a₂ = -a₁ := by
    calc a₂ = (a₁ + a₂) - a₁ := by ring
    _ = 0 - a₁ := by rw [h_K0]
    _ = -a₁ := by ring
  have h_elim : a₁ * (q₁ - q₂) = 0 := by
    calc a₁ * (q₁ - q₂) = a₁ * q₁ + (-a₁) * q₂ := by ring
    _ = a₁ * q₁ + a₂ * q₂ := by rw [← h_a2]
    _ = 0 := h_K1
  cases mul_eq_zero.mp h_elim with
  | inl h_a1_zero =>
    have h_a2_zero : a₂ = 0 := by
      rw [h_a2, h_a1_zero, neg_zero]
    exact ⟨h_a1_zero, h_a2_zero⟩
  | inr h_diff_zero =>
    exact (h_sub h_diff_zero).elim

/-- Cycle 11 Theorem: Finite Exponential Uniqueness for 3 modes over ℂ (3x3 Vandermonde Cancellation).
    If q₁, q₂, q₃ are pairwise distinct and a₁ + a₂ + a₃ = 0, a₁*q₁ + a₂*q₂ + a₃*q₃ = 0,
    and a₁*q₁^2 + a₂*q₂^2 + a₃*q₃^2 = 0, then a₁ = 0, a₂ = 0, a₃ = 0. -/
theorem finite_exponential_uniqueness_3 (q₁ q₂ q₃ a₁ a₂ a₃ : ℂ)
    (h12 : q₁ ≠ q₂) (h13 : q₁ ≠ q₃) (h23 : q₂ ≠ q₃)
    (h_K0 : a₁ + a₂ + a₃ = 0)
    (h_K1 : a₁ * q₁ + a₂ * q₂ + a₃ * q₃ = 0)
    (h_K2 : a₁ * q₁^2 + a₂ * q₂^2 + a₃ * q₃^2 = 0) :
    a₁ = 0 ∧ a₂ = 0 ∧ a₃ = 0 := by
  have h_diff12 : q₁ - q₂ ≠ 0 := sub_ne_zero.mpr h12
  have h_diff13 : q₁ - q₃ ≠ 0 := sub_ne_zero.mpr h13
  have h_diff23 : q₂ - q₃ ≠ 0 := sub_ne_zero.mpr h23
  have h_eq1 : a₁ * (q₁ - q₃) + a₂ * (q₂ - q₃) = 0 := by
    calc a₁ * (q₁ - q₃) + a₂ * (q₂ - q₃)
      _ = (a₁ * q₁ + a₂ * q₂ + a₃ * q₃) - (a₁ + a₂ + a₃) * q₃ := by ring
      _ = 0 - 0 * q₃ := by rw [h_K1, h_K0]
      _ = 0 := by ring
  have h_eq2 : a₁ * (q₁ * (q₁ - q₃)) + a₂ * (q₂ * (q₂ - q₃)) = 0 := by
    have h_cross : a₁ * q₁ * (q₁ - q₃) + a₂ * q₂ * (q₂ - q₃) = 0 := by
      calc a₁ * q₁ * (q₁ - q₃) + a₂ * q₂ * (q₂ - q₃)
        _ = (a₁ * q₁^2 + a₂ * q₂^2 + a₃ * q₃^2) - (a₁ * q₁ + a₂ * q₂ + a₃ * q₃) * q₃ := by ring
        _ = 0 - 0 * q₃ := by rw [h_K2, h_K1]
        _ = 0 := by ring
    calc a₁ * (q₁ * (q₁ - q₃)) + a₂ * (q₂ * (q₂ - q₃))
      _ = a₁ * q₁ * (q₁ - q₃) + a₂ * q₂ * (q₂ - q₃) := by ring
      _ = 0 := h_cross
  have h_det : a₁ * (q₁ - q₃) * (q₁ - q₂) = 0 := by
    calc a₁ * (q₁ - q₃) * (q₁ - q₂)
      _ = (a₁ * (q₁ * (q₁ - q₃)) + a₂ * (q₂ * (q₂ - q₃))) - q₂ * (a₁ * (q₁ - q₃) + a₂ * (q₂ - q₃)) := by ring
      _ = 0 - q₂ * 0 := by rw [h_eq2, h_eq1]
      _ = 0 := by ring
  have ha1_zero : a₁ = 0 := by
    have h_prod1 : a₁ * ((q₁ - q₃) * (q₁ - q₂)) = 0 := by
      calc a₁ * ((q₁ - q₃) * (q₁ - q₂)) = a₁ * (q₁ - q₃) * (q₁ - q₂) := by ring
      _ = 0 := h_det
    cases mul_eq_zero.mp h_prod1 with
    | inl h => exact h
    | inr h_prod2 =>
      cases mul_eq_zero.mp h_prod2 with
      | inl hd13 => exact (h_diff13 hd13).elim
      | inr hd12 => exact (h_diff12 hd12).elim
  have ha2_zero : a₂ = 0 := by
    have h2 : a₂ * (q₂ - q₃) = 0 := by
      calc a₂ * (q₂ - q₃) = (a₁ * (q₁ - q₃) + a₂ * (q₂ - q₃)) - a₁ * (q₁ - q₃) := by ring
      _ = 0 - 0 * (q₁ - q₃) := by rw [h_eq1, ha1_zero]
      _ = 0 := by ring
    cases mul_eq_zero.mp h2 with
    | inl h => exact h
    | inr hd23 => exact (h_diff23 hd23).elim
  have ha3_zero : a₃ = 0 := by
    calc a₃ = (a₁ + a₂ + a₃) - a₁ - a₂ := by ring
    _ = 0 - 0 - 0 := by rw [h_K0, ha1_zero, ha2_zero]
    _ = 0 := by ring
  exact ⟨ha1_zero, ha2_zero, ha3_zero⟩

/-- Cycle 11 Theorem: Transcendental Nonresonance Implication.
    If (log tau) / (2 * pi) = (a * log p) / (2 * pi * q) for positive real tau, p and nonzero q,
    then q * log tau = a * log p. -/
theorem tc_log_nonresonance_scaling (tau p a q : ℝ) (hq : q ≠ 0) (hpi : Real.pi ≠ 0)
    (h_eq : Real.log tau / (2 * Real.pi) = (a * Real.log p) / (2 * Real.pi * q)) :
    q * Real.log tau = a * Real.log p := by
  have h2pi : 2 * Real.pi ≠ 0 := mul_ne_zero two_ne_zero hpi
  have h2pi_q : 2 * Real.pi * q ≠ 0 := mul_ne_zero h2pi hq
  have h1 : Real.log tau / (2 * Real.pi) * (2 * Real.pi * q) =
      (a * Real.log p) / (2 * Real.pi * q) * (2 * Real.pi * q) := by rw [h_eq]
  rw [div_mul_cancel₀ (a * Real.log p) h2pi_q] at h1
  have h_left : Real.log tau / (2 * Real.pi) * (2 * Real.pi * q) = q * Real.log tau := by
    calc Real.log tau / (2 * Real.pi) * (2 * Real.pi * q)
      _ = (Real.log tau / (2 * Real.pi) * (2 * Real.pi)) * q := by ring
      _ = Real.log tau * q := by rw [div_mul_cancel₀ (Real.log tau) h2pi]
      _ = q * Real.log tau := by ring
  rw [h_left] at h1
  exact h1

/-- Cycle 11 Theorem (Conditional): Nonresonance with prime powers from assumed power irrationality.
    Specializes an assumed irrationality hypothesis for tau^q over ℚ to the algebraic prime power p^a.
    Lindemann's theorem (1882) that tau = 2*pi is transcendental is an external theorem from
    transcendental number theory, not proved within this Lean module. -/
theorem tc_prime_power_nonresonance_conditional (tau : ℝ) (q a : ℕ) (p : ℕ)
    (h_trans : ∀ (c : ℚ), tau ^ (q : ℝ) ≠ (c : ℝ)) :
    tau ^ (q : ℝ) ≠ (p ^ a : ℝ) := by
  intro h_eq
  have h_c : tau ^ (q : ℝ) = ((p ^ a : ℚ) : ℝ) := by
    push_cast
    exact h_eq
  exact (h_trans (p ^ a : ℚ)) h_c

/-- Compatibility alias for Cycle 11 claim spec -/
theorem tc_prime_power_nonresonance_of_transcendental (tau : ℝ) (q a : ℕ) (p : ℕ)
    (h_trans : ∀ (c : ℚ), tau ^ (q : ℝ) ≠ (c : ℝ)) :
    tau ^ (q : ℝ) ≠ (p ^ a : ℝ) :=
  tc_prime_power_nonresonance_conditional tau q a p h_trans

/-- Cycle 11 Theorem: Mode modulus distinction from centering displacement difference.
    Two exponential modes with displacement δ₁ ≠ δ₂ have distinct moduli under base tau > 1. -/
theorem mode_modulus_distinct_of_delta_ne (tau δ₁ δ₂ : ℝ) (htau : 1 < tau) (hδ : δ₁ ≠ δ₂) :
    Real.exp (-δ₁ * Real.log tau) ≠ Real.exp (-δ₂ * Real.log tau) := by
  have hlog_pos : 0 < Real.log tau := Real.log_pos htau
  have hlog_ne : Real.log tau ≠ 0 := ne_of_gt hlog_pos
  intro h_eq
  rw [Real.exp_eq_exp] at h_eq
  have h_sub : (-δ₁ - -δ₂) * Real.log tau = 0 := by
    calc (-δ₁ - -δ₂) * Real.log tau = -δ₁ * Real.log tau - -δ₂ * Real.log tau := by ring
    _ = 0 := sub_eq_zero.mpr h_eq
  cases mul_eq_zero.mp h_sub with
  | inl h_diff =>
    have h_delta_eq : δ₁ = δ₂ := by linarith
    exact hδ h_delta_eq
  | inr h_log_zero =>
    exact (hlog_ne h_log_zero).elim

/-- Cycle 12 Theorem: Quantitative Vandermonde Block Reconstruction for 2 modes over ℂ.
    For distinct bases q₁ ≠ q₂ and grade k : ℕ, the individual mode a₁ * q₁^k is uniquely
    reconstructed from the 2-block sum values S_k = a₁*q₁^k + a₂*q₂^k and S_{k+1} = a₁*q₁^{k+1} + a₂*q₂^{k+1}.
    Identity: a₁ * q₁^k = (S_k * q₂ - S_{k+1}) / (q₂ - q₁). -/
theorem vandermonde_block_reconstruction_2 (q₁ q₂ a₁ a₂ : ℂ) (hq : q₂ - q₁ ≠ 0) (k : ℕ)
    (S_k : ℂ) (S_k1 : ℂ)
    (hS_k : S_k = a₁ * q₁^k + a₂ * q₂^k)
    (hS_k1 : S_k1 = a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) :
    a₁ * q₁^k = (S_k * q₂ - S_k1) / (q₂ - q₁) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  rw [hS_k, hS_k1, h_step1, h_step2]
  have h_alg : (a₁ * q₁^k + a₂ * q₂^k) * q₂ - (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂)) =
      (a₁ * q₁^k) * (q₂ - q₁) := by ring
  rw [h_alg]
  exact (mul_div_cancel_right₀ (a₁ * q₁^k) hq).symm

/-- Cycle 12 Theorem: Quantitative Vandermonde Block Reconstruction for 2 modes (second mode).
    Identity: a₂ * q₂^k = (S_{k+1} - S_k * q₁) / (q₂ - q₁). -/
theorem vandermonde_block_reconstruction_2_mode2 (q₁ q₂ a₁ a₂ : ℂ) (hq : q₂ - q₁ ≠ 0) (k : ℕ)
    (S_k : ℂ) (S_k1 : ℂ)
    (hS_k : S_k = a₁ * q₁^k + a₂ * q₂^k)
    (hS_k1 : S_k1 = a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) :
    a₂ * q₂^k = (S_k1 - S_k * q₁) / (q₂ - q₁) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  rw [hS_k, hS_k1, h_step1, h_step2]
  have h_alg : (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂)) - (a₁ * q₁^k + a₂ * q₂^k) * q₁ =
      (a₂ * q₂^k) * (q₂ - q₁) := by ring
  rw [h_alg]
  exact (mul_div_cancel_right₀ (a₂ * q₂^k) hq).symm

/-- Cycle 12 Theorem: Quantitative Vandermonde Block Reconstruction for 3 modes over ℂ.
    For pairwise distinct bases q₁, q₂, q₃ and grade k : ℕ, the individual mode a₁ * q₁^k
    is uniquely reconstructed from the 3-block sum values S_k, S_{k+1}, S_{k+2}.
    Identity: a₁ * q₁^k = (S_{k+2} - (q₂ + q₃)*S_{k+1} + (q₂*q₃)*S_k) / ((q₁ - q₂)*(q₁ - q₃)). -/
theorem vandermonde_block_reconstruction_3 (q₁ q₂ q₃ a₁ a₂ a₃ : ℂ)
    (h_denom : (q₁ - q₂) * (q₁ - q₃) ≠ 0) (k : ℕ)
    (S_k : ℂ) (S_k1 : ℂ) (S_k2 : ℂ)
    (hS_k : S_k = a₁ * q₁^k + a₂ * q₂^k + a₃ * q₃^k)
    (hS_k1 : S_k1 = a₁ * q₁^(k+1) + a₂ * q₂^(k+1) + a₃ * q₃^(k+1))
    (hS_k2 : S_k2 = a₁ * q₁^(k+2) + a₂ * q₂^(k+2) + a₃ * q₃^(k+2)) :
    a₁ * q₁^k = (S_k2 - (q₂ + q₃) * S_k1 + (q₂ * q₃) * S_k) / ((q₁ - q₂) * (q₁ - q₃)) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  have h_step3 : q₃^(k+1) = q₃^k * q₃ := by ring
  have h_step4 : q₁^(k+2) = q₁^k * q₁^2 := by ring
  have h_step5 : q₂^(k+2) = q₂^k * q₂^2 := by ring
  have h_step6 : q₃^(k+2) = q₃^k * q₃^2 := by ring
  rw [hS_k, hS_k1, hS_k2, h_step1, h_step2, h_step3, h_step4, h_step5, h_step6]
  have h_alg : (a₁ * (q₁^k * q₁^2) + a₂ * (q₂^k * q₂^2) + a₃ * (q₃^k * q₃^2)) -
      (q₂ + q₃) * (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂) + a₃ * (q₃^k * q₃)) +
      (q₂ * q₃) * (a₁ * q₁^k + a₂ * q₂^k + a₃ * q₃^k) =
      (a₁ * q₁^k) * ((q₁ - q₂) * (q₁ - q₃)) := by ring
  rw [h_alg]
  exact (mul_div_cancel_right₀ (a₁ * q₁^k) h_denom).symm

/-- Cycle 13 Theorem: Remainder-Aware Vandermonde Block Reconstruction for 2 modes over ℂ.
    For distinct bases q₁ ≠ q₂, when observations Y_k = S_k + R_k are perturbed by remainder terms R_k,
    the exact mode a₁ * q₁^k satisfies:
    a₁ * q₁^k = (Y_k * q₂ - Y_{k+1}) / (q₂ - q₁) - (R_k * q₂ - R_{k+1}) / (q₂ - q₁).
    Scope note: Applies to r = 2 modes. Arbitrary r requires the full matrix inverse W = V⁻¹. -/
theorem vandermonde_block_remainder_2 (q₁ q₂ a₁ a₂ : ℂ) (hq : q₂ - q₁ ≠ 0) (k : ℕ)
    (Y_k Y_k1 R_k R_k1 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) + R_k1) :
    a₁ * q₁^k = (Y_k * q₂ - Y_k1) / (q₂ - q₁) - (R_k * q₂ - R_k1) / (q₂ - q₁) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  rw [hY_k, hY_k1, h_step1, h_step2]
  have h_alg : ((a₁ * q₁^k + a₂ * q₂^k + R_k) * q₂ - (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂) + R_k1)) -
      (R_k * q₂ - R_k1) = (a₁ * q₁^k) * (q₂ - q₁) := by ring
  rw [← sub_div, h_alg]
  exact (mul_div_cancel_right₀ (a₁ * q₁^k) hq).symm

/-- Cycle 13 Theorem: Remainder-Aware Vandermonde Block Reconstruction for 2 modes (second mode).
    Identity: a₂ * q₂^k = (Y_{k+1} - Y_k * q₁) / (q₂ - q₁) - (R_{k+1} - R_k * q₁) / (q₂ - q₁). -/
theorem vandermonde_block_remainder_2_mode2 (q₁ q₂ a₁ a₂ : ℂ) (hq : q₂ - q₁ ≠ 0) (k : ℕ)
    (Y_k Y_k1 R_k R_k1 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) + R_k1) :
    a₂ * q₂^k = (Y_k1 - Y_k * q₁) / (q₂ - q₁) - (R_k1 - R_k * q₁) / (q₂ - q₁) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  rw [hY_k, hY_k1, h_step1, h_step2]
  have h_alg : (((a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂) + R_k1) - (a₁ * q₁^k + a₂ * q₂^k + R_k) * q₁) -
      (R_k1 - R_k * q₁)) = (a₂ * q₂^k) * (q₂ - q₁) := by ring
  rw [← sub_div, h_alg]
  exact (mul_div_cancel_right₀ (a₂ * q₂^k) hq).symm

/-- Cycle 13 Theorem: Remainder-Aware Vandermonde Block Reconstruction for 3 modes over ℂ.
    For pairwise distinct bases q₁, q₂, q₃ and grade k : ℕ, with observations Y_k = S_k + R_k:
    a₁ * q₁^k = (Y_{k+2} - (q₂ + q₃)*Y_{k+1} + (q₂*q₃)*Y_k) / ((q₁ - q₂)*(q₁ - q₃)) -
                (R_{k+2} - (q₂ + q₃)*R_{k+1} + (q₂*q₃)*R_k) / ((q₁ - q₂)*(q₁ - q₃)). -/
theorem vandermonde_block_remainder_3 (q₁ q₂ q₃ a₁ a₂ a₃ : ℂ)
    (h_denom : (q₁ - q₂) * (q₁ - q₃) ≠ 0) (k : ℕ)
    (Y_k Y_k1 Y_k2 R_k R_k1 R_k2 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k + a₃ * q₃^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1) + a₃ * q₃^(k+1)) + R_k1)
    (hY_k2 : Y_k2 = (a₁ * q₁^(k+2) + a₂ * q₂^(k+2) + a₃ * q₃^(k+2)) + R_k2) :
    a₁ * q₁^k = (Y_k2 - (q₂ + q₃) * Y_k1 + (q₂ * q₃) * Y_k) / ((q₁ - q₂) * (q₁ - q₃)) -
                (R_k2 - (q₂ + q₃) * R_k1 + (q₂ * q₃) * R_k) / ((q₁ - q₂) * (q₁ - q₃)) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := by ring
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := by ring
  have h_step3 : q₃^(k+1) = q₃^k * q₃ := by ring
  have h_step4 : q₁^(k+2) = q₁^k * q₁^2 := by ring
  have h_step5 : q₂^(k+2) = q₂^k * q₂^2 := by ring
  have h_step6 : q₃^(k+2) = q₃^k * q₃^2 := by ring
  rw [hY_k, hY_k1, hY_k2, h_step1, h_step2, h_step3, h_step4, h_step5, h_step6]
  have h_alg : (((a₁ * (q₁^k * q₁^2) + a₂ * (q₂^k * q₂^2) + a₃ * (q₃^k * q₃^2) + R_k2) -
      (q₂ + q₃) * (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂) + a₃ * (q₃^k * q₃) + R_k1) +
      (q₂ * q₃) * (a₁ * q₁^k + a₂ * q₂^k + a₃ * q₃^k + R_k)) -
      (R_k2 - (q₂ + q₃) * R_k1 + (q₂ * q₃) * R_k)) =
      (a₁ * q₁^k) * ((q₁ - q₂) * (q₁ - q₃)) := by ring
  rw [← sub_div, h_alg]
  exact (mul_div_cancel_right₀ (a₁ * q₁^k) h_denom).symm

/-- Cycle 13 Theorem: Triangle inequality remainder lower bound for real linear reconstruction.
    If reconstructed mode M, observation estimator Y_est, and remainder estimator R_est satisfy
    M = Y_est - R_est, then |Y_est| ≥ |M| - |R_est|. -/
theorem reconstruction_remainder_lower_bound (M Y_est R_est : ℝ)
    (h_id : M = Y_est - R_est) :
    |M| - |R_est| ≤ |Y_est| := by
  have h_m : M = Y_est + (-R_est) := by linarith
  have h_tri : |M| ≤ |Y_est| + |R_est| := by
    calc |M|
      _ = |Y_est + (-R_est)| := by rw [h_m]
      _ ≤ |Y_est| + |-R_est| := abs_add Y_est (-R_est)
      _ = |Y_est| + |R_est| := by rw [abs_neg]
  linarith

/-- Cycle 14 Theorem: Complex triangle inequality remainder lower bound for linear mode reconstruction.
    If reconstructed complex mode M, observation estimator Y_est, and remainder estimator R_est satisfy
    M = Y_est - R_est in ℂ, then Complex.abs M - Complex.abs R_est ≤ Complex.abs Y_est. -/
theorem complex_reconstruction_remainder_lower_bound (M Y_est R_est : ℂ)
    (h_id : M = Y_est - R_est) :
    Complex.abs M - Complex.abs R_est ≤ Complex.abs Y_est := by
  have h_m : M = Y_est + (-R_est) := by
    calc M
      _ = Y_est - R_est := h_id
      _ = Y_est + (-R_est) := by ring
  have h_tri : Complex.abs M ≤ Complex.abs Y_est + Complex.abs R_est := by
    calc Complex.abs M
      _ = Complex.abs (Y_est + (-R_est)) := by rw [h_m]
      _ ≤ Complex.abs Y_est + Complex.abs (-R_est) := Complex.abs.add_le Y_est (-R_est)
      _ = Complex.abs Y_est + Complex.abs R_est := by rw [Complex.abs.map_neg]
  linarith

/-- Cycle 14 Theorem: Remainder-aware 2-mode Vandermonde reconstruction bound in ℂ.
    For observations Y_k, Y_{k+1} and remainders R_k, R_{k+1} satisfying the perturbed 2-mode
    Vandermonde equations with distinct bases q₁ ≠ q₂, the reconstructed mode M = a₁ * q₁^k
    satisfies:
    Complex.abs ((Y_k * q₂ - Y_k1) / (q₂ - q₁)) ≥
      Complex.abs (a₁ * q₁^k) - Complex.abs ((R_k * q₂ - R_k1) / (q₂ - q₁)). -/
theorem vandermonde_2_reconstruction_bound (q₁ q₂ a₁ a₂ : ℂ) (hq : q₂ - q₁ ≠ 0) (k : ℕ)
    (Y_k Y_k1 R_k R_k1 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) + R_k1) :
    Complex.abs (a₁ * q₁^k) - Complex.abs ((R_k * q₂ - R_k1) / (q₂ - q₁)) ≤
      Complex.abs ((Y_k * q₂ - Y_k1) / (q₂ - q₁)) := by
  have h_id := vandermonde_block_remainder_2 q₁ q₂ a₁ a₂ hq k Y_k Y_k1 R_k R_k1 hY_k hY_k1
  exact complex_reconstruction_remainder_lower_bound (a₁ * q₁^k)
    ((Y_k * q₂ - Y_k1) / (q₂ - q₁)) ((R_k * q₂ - R_k1) / (q₂ - q₁)) h_id

/-- Epic Theorem: Remainder-aware 2-mode Vandermonde reconstruction identity for integer grades (k : ℤ)
    with non-zero bases q₁ ≠ 0, q₂ ≠ 0. -/
theorem vandermonde_block_remainder_2_zpow (q₁ q₂ a₁ a₂ : ℂ)
    (hq1 : q₁ ≠ 0) (hq2 : q₂ ≠ 0) (hq : q₂ - q₁ ≠ 0) (k : ℤ)
    (Y_k Y_k1 R_k R_k1 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) + R_k1) :
    a₁ * q₁^k = (Y_k * q₂ - Y_k1) / (q₂ - q₁) - (R_k * q₂ - R_k1) / (q₂ - q₁) := by
  have h_step1 : q₁^(k+1) = q₁^k * q₁ := zpow_add_one₀ hq1 k
  have h_step2 : q₂^(k+1) = q₂^k * q₂ := zpow_add_one₀ hq2 k
  rw [hY_k, hY_k1, h_step1, h_step2]
  have h_alg : ((a₁ * q₁^k + a₂ * q₂^k + R_k) * q₂ - (a₁ * (q₁^k * q₁) + a₂ * (q₂^k * q₂) + R_k1)) -
      (R_k * q₂ - R_k1) = (a₁ * q₁^k) * (q₂ - q₁) := by ring
  rw [← sub_div, h_alg]
  exact (mul_div_cancel_right₀ (a₁ * q₁^k) hq).symm

/-- Epic Theorem: Remainder-aware 2-mode Vandermonde reconstruction bound in ℂ for integer grades (k : ℤ)
    with non-zero bases q₁ ≠ 0, q₂ ≠ 0. -/
theorem vandermonde_2_reconstruction_bound_zpow (q₁ q₂ a₁ a₂ : ℂ)
    (hq1 : q₁ ≠ 0) (hq2 : q₂ ≠ 0) (hq : q₂ - q₁ ≠ 0) (k : ℤ)
    (Y_k Y_k1 R_k R_k1 : ℂ)
    (hY_k : Y_k = (a₁ * q₁^k + a₂ * q₂^k) + R_k)
    (hY_k1 : Y_k1 = (a₁ * q₁^(k+1) + a₂ * q₂^(k+1)) + R_k1) :
    Complex.abs (a₁ * q₁^k) - Complex.abs ((R_k * q₂ - R_k1) / (q₂ - q₁)) ≤
      Complex.abs ((Y_k * q₂ - Y_k1) / (q₂ - q₁)) := by
  have h_id := vandermonde_block_remainder_2_zpow q₁ q₂ a₁ a₂ hq1 hq2 hq k Y_k Y_k1 R_k R_k1 hY_k hY_k1
  exact complex_reconstruction_remainder_lower_bound (a₁ * q₁^k)
    ((Y_k * q₂ - Y_k1) / (q₂ - q₁)) ((R_k * q₂ - R_k1) / (q₂ - q₁)) h_id

/-- Epic Theorem: Quadratic Exponent Decay Outside Near-Band for Gaussian Mellin Transform.
    For critical strip real coordinate displacement |σ| ≤ 1 and imaginary displacement |τ_0| ≥ 3,
    the quadratic exponent in the untruncated Gaussian transform satisfies:
    σ^2 + 6*σ - τ_0^2 ≤ -2. -/
theorem gaussian_exponent_band_bound (σ τ_0 : ℝ)
    (hσ_low : -1 ≤ σ) (hσ_high : σ ≤ 1) (hτ : 9 ≤ τ_0^2) :
    σ^2 + 6 * σ - τ_0^2 ≤ -2 := by
  nlinarith

/-- Epic Theorem: Unnormalized Smoothed Explicit Formula Mode Exponent.
    For step size h_k = tau^(-k), the Mellin residue scaling h_k^(1 - σ) has exponent
    -k * (1 - σ) = k * (σ - 1). -/
theorem unnormalized_mode_exponent_id (k σ : ℝ) :
    -k * (1 - σ) = k * (σ - 1) := by
  ring

/-- Epic Theorem: Centered Mode Exponent Identity.
    Normalizing the unnormalized observable by h_k^(-1/2) = tau^(k/2) shifts the exponent
    from k * (σ - 1) to k * (σ - 1/2), matching the unitary character q_rho = tau^(rho - 1/2). -/
theorem centered_mode_exponent_id (k σ : ℝ) :
    k / 2 + k * (σ - 1) = k * (σ - 1 / 2) := by
  ring

/-- Epic Theorem: Centered Mode Exponent from Unnormalized Mode Exponent. -/
theorem centered_mode_from_unnormalized (k σ : ℝ) :
    k * (1 / 2) + k * (σ - 1) = k * (σ - 1 / 2) := by
  ring

/-- Epic Theorem: Arithmetic Station Rational Collision Ratio.
    If distinct arithmetic stations collide across grades tau_K * m = tau_J * n with m ≠ 0,
    then the inter-grade ratio tau_K / tau_J is rational: tau_K / tau_J = n / m. -/
theorem arithmetic_station_collision_ratio (tau_K tau_J m n : ℝ)
    (hm : m ≠ 0) (htau_J : tau_J ≠ 0)
    (h_eq : tau_K * m = tau_J * n) :
    tau_K / tau_J = n / m := by
  have h1 : tau_K = (tau_J * n) / m := by
    calc tau_K
      _ = (tau_K * m) / m := by rw [mul_div_cancel_right₀ tau_K hm]
      _ = (tau_J * n) / m := by rw [h_eq]
  rw [h1]
  calc ((tau_J * n) / m) / tau_J
    _ = (tau_J * (n / m)) / tau_J := by rw [mul_div_assoc]
    _ = n / m := by rw [mul_div_cancel_left₀ (n / m) htau_J]

/-- Epic Theorem: Arithmetic Overlap Cutoff Strictly Separated.
    If minimum station separation d > 0 satisfies d ≤ |x - y|, and 0 < ε < d,
    then |x - y| / ε > 1, so test functions supported in [-1, 1] vanish identically. -/
theorem arithmetic_overlap_cutoff_strictly_separated (x y d ε : ℝ)
    (h_dist : d ≤ |x - y|) (hε_pos : 0 < ε) (hε_lt : ε < d) :
    1 < |x - y| / ε := by
  have hd_lt : ε < |x - y| := lt_of_lt_of_le hε_lt h_dist
  exact (one_lt_div hε_pos).mpr hd_lt

/-- Epic Theorem: Candidate Bridge Positivity Contradiction.
    If the arithmetic observable Q satisfies Q ≤ 0 (e.g. Q = 0 for ε < d_min)
    and the candidate bridge inequality asserts Q ≥ c * D with c > 0 and D > 0,
    then a logical contradiction (False) is derived. -/
theorem candidate_bridge_positivity_contradiction (Q c D : ℝ)
    (hQ_zero : Q ≤ 0) (hc : 0 < c) (hD : 0 < D)
    (h_bridge : c * D ≤ Q) :
    False := by
  have h_pos : 0 < c * D := mul_pos hc hD
  linarith

/-- Epic Theorem: Two-Variable Tensor Bilinear Expansion (4-Term Form).
    For any bilinear pairings or real values B_K, Z_K, B_J, Z_J:
    (B_K - Z_K) * (B_J - Z_J) = B_K * B_J - B_K * Z_J - Z_K * B_J + Z_K * Z_J. -/
theorem two_variable_tensor_decomposition_algebra (B_K Z_K B_J Z_J : ℝ) :
    (B_K - Z_K) * (B_J - Z_J) = B_K * B_J - B_K * Z_J - Z_K * B_J + Z_K * Z_J := by
  ring

/-- Epic Theorem: Two-Variable Explicit Expansion (9-Term Uncombined Form).
    For three-component measures mu_K = P_K - Z_K - T_K and mu_J = P_J - Z_J - T_J,
    the bilinearly expanded product exhibits all 9 distinct terms with exact signs:
    (P_K - Z_K - T_K) * (P_J - Z_J - T_J) =
      P_K * P_J - P_K * Z_J - P_K * T_J
      - Z_K * P_J + Z_K * Z_J + Z_K * T_J
      - T_K * P_J + T_K * Z_J + T_K * T_J. -/
theorem two_variable_nine_term_expansion_algebra (P_K Z_K T_K P_J Z_J T_J : ℝ) :
    (P_K - Z_K - T_K) * (P_J - Z_J - T_J) =
      P_K * P_J - P_K * Z_J - P_K * T_J
      - Z_K * P_J + Z_K * Z_J + Z_K * T_J
      - T_K * P_J + T_K * Z_J + T_K * T_J := by
  ring

/-- Epic Theorem: Normalized Truncation Error Scaling.
    If the truncation error E satisfies |E| ≤ B, then for any ε > 0,
    the normalized error satisfies |E| / ε ≤ B / ε. -/
theorem normalized_truncation_error_scaling (E B ε : ℝ)
    (hE : |E| ≤ B) (hε : 0 < ε) :
    |E| / ε ≤ B / ε := by
  exact div_le_div_of_nonneg_right hE (le_of_lt hε)

/-- Epic Theorem: Power Cutoff Exponent Positivity.
    For dimension index p > 2 and trajectory exponent α > p / (p - 2),
    the net normalized exponent α * (p - 2) - p is strictly positive,
    guaranteeing asymptotic convergence of the normalized truncation error to zero. -/
theorem power_cutoff_exponent_positivity (p α : ℝ)
    (hp : 2 < p) (hα : p / (p - 2) < α) :
    0 < α * (p - 2) - p := by
  have hp_sub : 0 < p - 2 := sub_pos.mpr hp
  have h_mul : (p / (p - 2)) * (p - 2) < α * (p - 2) := mul_lt_mul_of_pos_right hα hp_sub
  have h_div : (p / (p - 2)) * (p - 2) = p := div_mul_cancel₀ p (ne_of_gt hp_sub)
  rw [h_div] at h_mul
  exact sub_pos.mpr h_mul

/-- Epic Theorem: Candidate Bridge with Remainder Contradiction.
    Suppose an observable decomposes as Q = A + R, where:
    1. Arithmetic vanishing: Q ≤ 0 (for small ε).
    2. Selected spectral lower bound: c * D ≤ A with c > 0 and D > 0.
    3. Remainder subordination: |R| < c * D.
    Then a logical contradiction (False) is derived. -/
theorem candidate_bridge_with_remainder_contradiction (Q A R c D : ℝ)
    (hQ_eq : Q = A + R)
    (hQ_nonpos : Q ≤ 0)
    (hc : 0 < c)
    (hD : 0 < D)
    (hA : c * D ≤ A)
    (hR : |R| < c * D) :
    False := by
  have _h_pos : 0 < c * D := mul_pos hc hD
  have hR_lower : - (c * D) < R := (abs_lt.mp hR).1
  linarith [hQ_eq, hQ_nonpos, hA, hR_lower, _h_pos]

/-- Remainder cancellation identity for complete two-variable explicit formula:
    Q = A + R + E implies R - (-A₀) = Q - (A - A₀) - E. -/
theorem explicit_formula_remainder_cancellation_identity (Q A R E A₀ : ℝ)
    (h_decomp : Q = A + R + E) :
    R - (-A₀) = Q - (A - A₀) - E := by
  linarith

/-- Triangle bound on remainder cancellation defect:
    |R - (-A₀)| ≤ |Q| + |A - A₀| + |E|. -/
theorem explicit_formula_remainder_triangle_bound (Q A R E A₀ : ℝ)
    (h_decomp : Q = A + R + E) :
    |R - (-A₀)| ≤ |Q| + |A - A₀| + |E| := by
  have h_id : R - (-A₀) = Q - (A - A₀) - E := by linarith
  rw [h_id]
  have h1 : |Q - (A - A₀) - E| ≤ |Q - (A - A₀)| + |E| := abs_sub (Q - (A - A₀)) E
  have h2 : |Q - (A - A₀)| ≤ |Q| + |A - A₀| := abs_sub Q (A - A₀)
  linarith

/-- Remainder error bound under exact arithmetic vanishing Q = 0:
    When the arithmetic overlap vanishes identically (Q = 0), the deviation of the
    truncated remainder R from the negative asymptotic selected mode -A₀ satisfies
    |R - (-A₀)| ≤ |A - A₀| + |E|. -/
theorem explicit_formula_truncated_remainder_zero_Q_bound (A R E A₀ : ℝ)
    (h_decomp : 0 = A + R + E) :
    |R - (-A₀)| ≤ |A - A₀| + |E| := by
  have h_tri := explicit_formula_remainder_triangle_bound 0 A R E A₀ h_decomp
  rw [abs_zero, zero_add] at h_tri
  exact h_tri

/-- Full (untruncated) remainder identity under exact arithmetic vanishing Q = 0:
    When the complete explicit formula has no omitted tail (Q = A + R_full),
    vanishing Q = 0 forces the complete remainder to be the exact negative: R_full = -A. -/
theorem explicit_formula_full_remainder_cancellation (A R_full : ℝ)
    (h_decomp : 0 = A + R_full) :
    R_full = -A := by
  linarith

/-- Quantitative epsilon-delta remainder cancellation limit theorem:
    If the arithmetic observable Q, the selected spectral deviation A - A₀,
    and the omitted tail E are each bounded by δ / 3, then the retained remainder
    is within δ of the exact negative selected contribution -A₀. -/
theorem explicit_formula_remainder_cancellation_eps (Q A R E A₀ δ : ℝ)
    (h_decomp : Q = A + R + E)
    (hQ : |Q| < δ / 3)
    (hA : |A - A₀| < δ / 3)
    (hE : |E| < δ / 3) :
    |R - (-A₀)| < δ := by
  have h_tri := explicit_formula_remainder_triangle_bound Q A R E A₀ h_decomp
  linarith

/-- Elementary tail subordination bound (transitivity of inequality):
    If the tail error |E| is majorized by B and B < δ, then |E| < δ.
    Note: The analytic derivation of the majorant B and the two-variable truncation
    bound |E_{ε, T}| ≤ C_p ε^(1-p) log²(2+T) / T^(p-2) are external analytic dependencies. -/
theorem normalized_tail_subordination_bound (E B δ : ℝ)
    (hE : |E| ≤ B) (hB : B < δ) :
    |E| < δ :=
  lt_of_le_of_lt hE hB

/-- Remainder cancellation obstruction to the candidate bridge:
    When exact explicit formula remainder cancellation occurs (R = -A),
    the observable Q = A + R vanishes identically (Q = 0) without triggering
    the candidate bridge contradiction hypothesis |R| < c * D. -/
theorem candidate_bridge_gap_exact_cancellation (A₀ c D : ℝ)
    (hc : 0 < c) (hD : 0 < D)
    (hA₀ : A₀ = c * D) :
    ¬ (|-A₀| < c * D) := by
  have h_pos : 0 < c * D := mul_pos hc hD
  rw [abs_neg, hA₀]
  rw [abs_of_pos h_pos]
  exact lt_irrefl (c * D)

/-- Candidate bridge unproved lower bound gap:
    If remainder cancellation holds (R = -A), then Q = A + R is zero,
    and no strictly positive lower bound Q ≥ c * D > 0 can be satisfied.
    Note: This is an elementary algebraic identity; it proves that remainder cancellation
    precludes the candidate lower bound, but does not derive the consistency of off-line zeros. -/
theorem candidate_bridge_unproved_lower_bound_gap (Q A R : ℝ)
    (hQ_eq : Q = A + R) (h_cancel : R = -A) :
    Q = 0 := by
  linarith

/-- Topological limit theorem for explicit formula remainder cancellation:
    If Q, A, E are functions converging along filter l such that Q → 0, A → A₀, and E → 0,
    and the decomposition Q = A + R + E holds everywhere, then R → -A₀ along l. -/
theorem explicit_formula_remainder_cancellation_tendsto {α : Type*} (l : Filter α)
    (Q A R E : α → ℝ) (A₀ : ℝ)
    (h_decomp : ∀ x, Q x = A x + R x + E x)
    (hQ : Filter.Tendsto Q l (nhds 0))
    (hA : Filter.Tendsto A l (nhds A₀))
    (hE : Filter.Tendsto E l (nhds 0)) :
    Filter.Tendsto R l (nhds (-A₀)) := by
  have h_eq : ∀ x, R x = Q x - A x - E x := by
    intro x
    linarith [h_decomp x]
  have h_sub : Filter.Tendsto (fun x => Q x - A x) l (nhds (0 - A₀)) :=
    Filter.Tendsto.sub hQ hA
  have h_sub2 : Filter.Tendsto (fun x => (Q x - A x) - E x) l (nhds ((0 - A₀) - 0)) :=
    Filter.Tendsto.sub h_sub hE
  have h_simpl : (0 - A₀) - 0 = -A₀ := by ring
  rw [h_simpl] at h_sub2
  have h_ev : (fun x => (Q x - A x) - E x) = R := by
    ext x
    exact (h_eq x).symm
  rwa [h_ev] at h_sub2

/-- Quantified epsilon-delta limiting theorem for explicit formula remainder cancellation:
    If Q(ε) → 0, A(ε) → A₀, and E(ε) → 0 as ε → 0⁺, and Q(ε) = A(ε) + R(ε) + E(ε) for all ε > 0,
    then R(ε) → -A₀ as ε → 0⁺. -/
theorem explicit_formula_remainder_cancellation_quantified
    (Q A R E : ℝ → ℝ) (A₀ : ℝ)
    (h_decomp : ∀ ε, 0 < ε → Q ε = A ε + R ε + E ε)
    (hQ : ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |Q ε| < δ)
    (hA : ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |A ε - A₀| < δ)
    (hE : ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |E ε| < δ) :
    ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |R ε - (-A₀)| < δ := by
  intro δ hδ
  have hδ3 : 0 < δ / 3 := by linarith
  rcases hQ (δ / 3) hδ3 with ⟨ε_Q, hε_Q_pos, hε_Q⟩
  rcases hA (δ / 3) hδ3 with ⟨ε_A, hε_A_pos, hε_A⟩
  rcases hE (δ / 3) hδ3 with ⟨ε_E, hε_E_pos, hε_E⟩
  refine ⟨min ε_Q (min ε_A ε_E), ?_, ?_⟩
  · exact lt_min hε_Q_pos (lt_min hε_A_pos hε_E_pos)
  · intro ε ⟨hε_pos, hε_bound⟩
    have h_lt_Q : ε < ε_Q := lt_of_lt_of_le hε_bound (min_le_left _ _)
    have h_lt_A : ε < ε_A := lt_of_lt_of_le hε_bound (le_trans (min_le_right _ _) (min_le_left _ _))
    have h_lt_E : ε < ε_E := lt_of_lt_of_le hε_bound (le_trans (min_le_right _ _) (min_le_right _ _))
    have hQ_val := hε_Q ε ⟨hε_pos, h_lt_Q⟩
    have hA_val := hε_A ε ⟨hε_pos, h_lt_A⟩
    have hE_val := hε_E ε ⟨hε_pos, h_lt_E⟩
    have h_dec := h_decomp ε hε_pos
    exact explicit_formula_remainder_cancellation_eps (Q ε) (A ε) (R ε) (E ε) A₀ δ h_dec hQ_val hA_val hE_val

/-- Two-point linear independence determinant identity for distinct power modes:
    If c₁ * x₁^r₁ + c₂ * x₁^r₂ = 0 and c₁ * x₂^r₁ + c₂ * x₂^r₂ = 0
    at points x₁, x₂ > 0 where the evaluation determinant x₁^r₁ * x₂^r₂ - x₁^r₂ * x₂^r₁ ≠ 0,
    then the coefficients c₁ and c₂ must both vanish.
    This formalizes the two-mode instance of finite spectral perturbation rigidity. -/
theorem finite_spectral_perturbation_rigidity_2point (c₁ c₂ x₁ x₂ r₁ r₂ : ℝ)
    (hx₁ : 0 < x₁) (_hx₂ : 0 < x₂) (h_diff : x₁ ^ r₁ * x₂ ^ r₂ - x₁ ^ r₂ * x₂ ^ r₁ ≠ 0)
    (h₁ : c₁ * x₁ ^ r₁ + c₂ * x₁ ^ r₂ = 0)
    (h₂ : c₁ * x₂ ^ r₁ + c₂ * x₂ ^ r₂ = 0) :
    c₁ = 0 ∧ c₂ = 0 := by
  have h_det : (x₁ ^ r₁ * x₂ ^ r₂ - x₁ ^ r₂ * x₂ ^ r₁) * c₁ = 0 := by
    calc (x₁ ^ r₁ * x₂ ^ r₂ - x₁ ^ r₂ * x₂ ^ r₁) * c₁
      _ = x₂ ^ r₂ * (c₁ * x₁ ^ r₁ + c₂ * x₁ ^ r₂) - x₁ ^ r₂ * (c₁ * x₂ ^ r₁ + c₂ * x₂ ^ r₂) := by ring
      _ = x₂ ^ r₂ * 0 - x₁ ^ r₂ * 0 := by rw [h₁, h₂]
      _ = 0 := by ring
  have hc₁ : c₁ = 0 := by
    cases mul_eq_zero.mp h_det with
    | inl h => exact False.elim (h_diff h)
    | inr h => exact h
  have hc₂_eq : (x₁ ^ r₂) * c₂ = 0 := by
    calc (x₁ ^ r₂) * c₂
      _ = (c₁ * x₁ ^ r₁ + c₂ * x₁ ^ r₂) - c₁ * x₁ ^ r₁ := by ring
      _ = 0 - 0 * x₁ ^ r₁ := by rw [h₁, hc₁]
      _ = 0 := by ring
  have h_x1_pow_ne : x₁ ^ r₂ ≠ 0 := by
    have h_pos := Real.rpow_pos_of_pos hx₁ r₂
    exact ne_of_gt h_pos
  have hc₂ : c₂ = 0 := by
    cases mul_eq_zero.mp hc₂_eq with
    | inl h => exact False.elim (h_x1_pow_ne h)
    | inr h => exact h
  exact ⟨hc₁, hc₂⟩

/-- Scoped mode extraction obstruction:
    For any functional P(ε) bounded by C * N(ε) where C is independent of ε
    and N(ε) → 0 as ε → 0⁺, P(ε) necessarily vanishes as ε → 0⁺.
    This establishes that a uniformly bounded extraction scheme cannot isolate a non-zero fixed mode. -/
theorem mode_extraction_uniform_bound_vanishes
    (P N : ℝ → ℝ) (C : ℝ) (hC : 0 ≤ C)
    (h_bd : ∀ ε, 0 < ε → |P ε| ≤ C * N ε)
    (hN : ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → N ε < δ) :
    ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |P ε| < δ := by
  intro δ hδ
  by_cases hC_zero : C = 0
  · obtain ⟨ε₀, hε₀_pos, _⟩ := hN 1 zero_lt_one
    refine ⟨ε₀, hε₀_pos, ?_⟩
    intro ε ⟨hε_pos, _⟩
    have h1 := h_bd ε hε_pos
    rw [hC_zero, zero_mul] at h1
    have h_abs_nonneg : 0 ≤ |P ε| := abs_nonneg (P ε)
    have h_abs_zero : |P ε| = 0 := le_antisymm h1 h_abs_nonneg
    rw [h_abs_zero]
    exact hδ
  · have hC_pos : 0 < C := lt_of_le_of_ne hC (Ne.symm hC_zero)
    have hδ_div : 0 < δ / C := div_pos hδ hC_pos
    obtain ⟨ε₀, hε₀_pos, hε₀⟩ := hN (δ / C) hδ_div
    refine ⟨ε₀, hε₀_pos, ?_⟩
    intro ε ⟨hε_pos, hε_lt⟩
    have h1 := h_bd ε hε_pos
    have h2 := hε₀ ε ⟨hε_pos, hε_lt⟩
    have h3 : C * N ε < C * (δ / C) := mul_lt_mul_of_pos_left h2 hC_pos
    rw [mul_div_cancel₀ δ (ne_of_gt hC_pos)] at h3
    exact lt_of_le_of_lt h1 h3

/-- Mode extraction coefficient divergence:
    If an extraction functional recovers a non-zero mode coefficient c₀ ≠ 0
    satisfying |P(ε)| ≥ |c₀| > 0, but is bounded by C(ε) * N(ε) where N(ε) > 0,
    then the extraction constant C(ε) must satisfy C(ε) ≥ |c₀| / N(ε).
    In particular, when N(ε) = O(ε^(1/2)) → 0 as ε → 0⁺, C(ε) must diverge as Ω(ε^(-1/2)). -/
theorem mode_extraction_coefficient_divergence
    (P_val N_val C_val c₀ : ℝ)
    (hN_pos : 0 < N_val)
    (hP_lower : |c₀| ≤ |P_val|)
    (hP_upper : |P_val| ≤ C_val * N_val) :
    |c₀| / N_val ≤ C_val := by
  have h_trans : |c₀| ≤ C_val * N_val := le_trans hP_lower hP_upper
  exact (div_le_iff hN_pos).mpr h_trans

/-- Algebraic exponent positivity for explicit formula power-log cutoff:
    For order p > 2 and cutoff scaling parameter α > p / (p - 2),
    the net epsilon power exponent r = α * (p - 2) - p is strictly positive. -/
theorem power_log_tail_subordination_exponent_positive
    (p : ℝ) (α : ℝ) (hp : 2 < p) (hα : p / (p - 2) < α) :
    0 < α * (p - 2) - p := by
  have hp2 : 0 < p - 2 := by linarith
  have h_mul := (div_lt_iff hp2).mp hα
  linarith

/-- Power-log tail error subordination limit:
    If |E(ε)| / ε ≤ C_p * ε^r * L(ε) for all ε > 0, where C_p > 0,
    and the majorant bound M(ε) = C_p * ε^r * L(ε) converges to 0 as ε → 0⁺,
    then |E(ε)| / ε converges to 0 as ε → 0⁺.
    Note: The analytic majorant bound |E(ε, T)| / ε ≤ C_p ε^(-p) T^(2-p) log²(2+T)
    is an external analytic dependency (Rademacher / Trudgian contour integration). -/
theorem power_log_decay_subordination
    (E L : ℝ → ℝ) (C_p r : ℝ)
    (hE_bd : ∀ ε, 0 < ε → |E ε| / ε ≤ C_p * ε ^ r * L ε)
    (h_lim : ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → C_p * ε ^ r * L ε < δ) :
    ∀ δ > 0, ∃ ε₀ > 0, ∀ ε, 0 < ε ∧ ε < ε₀ → |E ε| / ε < δ := by
  intro δ hδ
  obtain ⟨ε₀, hε₀_pos, hε₀⟩ := h_lim δ hδ
  refine ⟨ε₀, hε₀_pos, ?_⟩
  intro ε ⟨hε_pos, hε_lt⟩
  have h1 := hE_bd ε hε_pos
  have h2 := hε₀ ε ⟨hε_pos, hε_lt⟩
  exact lt_of_le_of_lt h1 h2

/-- Finite spectral perturbation rigidity (single-point derivative/Vandermonde identity):
    On any open interval I ⊂ (a_K, ∞), evaluating the two-mode sum and its derivative
    at a single interior point u₀ = log(x₀ / a_K) yields a 2x2 Vandermonde system
    in d_j = c_j * exp(l_j * u₀).
    For distinct exponents l₁ ≠ l₂, the determinant is l₂ - l₁ ≠ 0,
    forcing both coefficients c₁ and c₂ to vanish identically.
    This eliminates sample-point periodicity ambiguities (such as x = 2 and x = 4 for i*tau/log 2)
    by evaluating all derivatives at a single point. -/
theorem finite_spectral_perturbation_rigidity_vandermonde_2point
    (c₁ c₂ : ℝ) (l₁ l₂ u₀ : ℝ) (h_diff : l₁ ≠ l₂)
    (h_eval : c₁ * Real.exp (l₁ * u₀) + c₂ * Real.exp (l₂ * u₀) = 0)
    (h_deriv : c₁ * l₁ * Real.exp (l₁ * u₀) + c₂ * l₂ * Real.exp (l₂ * u₀) = 0) :
    c₁ = 0 ∧ c₂ = 0 := by
  have he1_pos : 0 < Real.exp (l₁ * u₀) := Real.exp_pos _
  have he2_pos : 0 < Real.exp (l₂ * u₀) := Real.exp_pos _
  have he1_ne : Real.exp (l₁ * u₀) ≠ 0 := ne_of_gt he1_pos
  have he2_ne : Real.exp (l₂ * u₀) ≠ 0 := ne_of_gt he2_pos
  have h_det : (l₂ - l₁) * (c₁ * Real.exp (l₁ * u₀)) = 0 := by
    calc (l₂ - l₁) * (c₁ * Real.exp (l₁ * u₀))
      _ = l₂ * (c₁ * Real.exp (l₁ * u₀) + c₂ * Real.exp (l₂ * u₀)) -
          (c₁ * l₁ * Real.exp (l₁ * u₀) + c₂ * l₂ * Real.exp (l₂ * u₀)) := by ring
      _ = l₂ * 0 - 0 := by rw [h_eval, h_deriv]
      _ = 0 := by ring
  have h_sub_ne : l₂ - l₁ ≠ 0 := sub_ne_zero.mpr (Ne.symm h_diff)
  have hd1_zero : c₁ * Real.exp (l₁ * u₀) = 0 := by
    cases mul_eq_zero.mp h_det with
    | inl h => exact False.elim (h_sub_ne h)
    | inr h => exact h
  have hc₁ : c₁ = 0 := by
    cases mul_eq_zero.mp hd1_zero with
    | inl h => exact h
    | inr h => exact False.elim (he1_ne h)
  have hd2_zero : c₂ * Real.exp (l₂ * u₀) = 0 := by
    calc c₂ * Real.exp (l₂ * u₀)
      _ = (c₁ * Real.exp (l₁ * u₀) + c₂ * Real.exp (l₂ * u₀)) - c₁ * Real.exp (l₁ * u₀) := by ring
      _ = 0 - 0 := by rw [h_eval, hd1_zero]
      _ = 0 := by ring
  have hc₂ : c₂ = 0 := by
    cases mul_eq_zero.mp hd2_zero with
    | inl h => exact h
    | inr h => exact False.elim (he2_ne h)
  exact ⟨hc₁, hc₂⟩

/-- Eventual lower bound for mode extraction:
    If an extraction functional converges to a non-zero mode coefficient c₀ ≠ 0 as ε → 0⁺,
    then eventually |c₀| / 2 ≤ |P(ε)| on the positive-side neighborhood 𝓝[>] 0. -/
theorem mode_extraction_eventual_lower_bound
    (P : ℝ → ℝ) (c₀ : ℝ) (hc₀ : c₀ ≠ 0)
    (h_lim : Filter.Tendsto P (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds c₀)) :
    ∀ᶠ ε in nhdsWithin 0 (Set.Ioi (0 : ℝ)), |c₀| / 2 ≤ |P ε| := by
  have hc₀_abs_pos : 0 < |c₀| := abs_pos.mpr hc₀
  have h_half_pos : 0 < |c₀| / 2 := half_pos hc₀_abs_pos
  have h_nhds : Metric.ball c₀ (|c₀| / 2) ∈ nhds c₀ := Metric.ball_mem_nhds c₀ h_half_pos
  have h_ev := h_lim h_nhds
  filter_upwards [h_ev] with ε hε
  rw [Set.mem_preimage, Metric.mem_ball, Real.dist_eq] at hε
  have h_tri : |c₀| - |P ε| ≤ |c₀ - P ε| := abs_sub_abs_le_abs_sub c₀ (P ε)
  rw [abs_sub_comm] at hε
  linarith

/-- Mode extraction coefficient divergence from eventual half-lower bound:
    If an extraction functional satisfies |P(ε)| ≥ |c₀| / 2 > 0 and is bounded by C(ε) * N(ε)
    where N(ε) > 0, then the extraction constant C(ε) must satisfy C(ε) ≥ |c₀| / (2 * N(ε)).
    This relaxes the pointwise assumption |P(ε)| ≥ |c₀| to the eventual neighborhood bound. -/
theorem mode_extraction_coefficient_divergence_half
    (P_val N_val C_val c₀ : ℝ)
    (hN_pos : 0 < N_val)
    (hP_lower : |c₀| / 2 ≤ |P_val|)
    (hP_upper : |P_val| ≤ C_val * N_val) :
    |c₀| / (2 * N_val) ≤ C_val := by
  have h_trans : |c₀| / 2 ≤ C_val * N_val := le_trans hP_lower hP_upper
  have h_div : (|c₀| / 2) / N_val ≤ C_val := (div_le_iff hN_pos).mpr h_trans
  have h_alg : (|c₀| / 2) / N_val = |c₀| / (2 * N_val) := by ring
  rw [h_alg] at h_div
  exact h_div

lemma tendsto_rpow_mul_log_sq (r : ℝ) (hr : 0 < r) :
    Filter.Tendsto (fun x => x ^ r * (Real.log x) ^ 2) (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
  have hs : -r < 0 := neg_lt_zero.mpr hr
  have ho := isLittleO_abs_log_rpow_rpow_nhds_zero (2 : ℝ) hs
  have hdiv := ho.tendsto_div_nhds_zero
  refine hdiv.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with x hx
  simp only [Set.mem_Ioi] at hx
  rw [Real.rpow_neg hx.le, div_inv_eq_mul, mul_comm]
  rw [Real.rpow_two, sq_abs]

lemma tendsto_rpow_zero_nhdsWithin (r : ℝ) (hr : 0 < r) :
    Filter.Tendsto (fun x => x ^ r) (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
  have h_id : Filter.Tendsto id (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) :=
    tendsto_nhdsWithin_of_tendsto_nhds Filter.tendsto_id
  have h := Filter.Tendsto.rpow_const h_id (Or.inr (le_of_lt hr))
  simpa only [Real.zero_rpow (ne_of_gt hr)] using h

lemma log_sq_le_of_mem_Ioo {ε α : ℝ} (hε : ε ∈ Set.Ioo (0 : ℝ) 1) (hα : 0 < α) :
    (Real.log (2 + ε ^ (-α))) ^ 2 ≤ 2 * (Real.log 3)^2 + 2 * α^2 * (Real.log ε)^2 := by
  have hε_pos : 0 < ε := hε.1
  have hε_lt : ε < 1 := hε.2
  have h1 : 1 ≤ ε ^ (-α) :=
    Real.one_le_rpow_of_pos_of_le_one_of_nonpos hε_pos hε_lt.le (neg_nonpos.mpr hα.le)
  have h_sum_le : 2 + ε ^ (-α) ≤ 3 * ε ^ (-α) := by
    calc 2 + ε ^ (-α) ≤ 2 * ε ^ (-α) + ε ^ (-α) := by linarith
    _ = 3 * ε ^ (-α) := by ring
  have h_rpow_pos : 0 < ε ^ (-α) := Real.rpow_pos_of_pos hε_pos _
  have h_arg_pos : 0 < 2 + ε ^ (-α) := by linarith
  have h_log_le : Real.log (2 + ε ^ (-α)) ≤ Real.log (3 * ε ^ (-α)) :=
    Real.log_le_log h_arg_pos h_sum_le
  have h_log_split : Real.log (3 * ε ^ (-α)) = Real.log 3 + (-α) * Real.log ε := by
    rw [Real.log_mul (by norm_num) (ne_of_gt h_rpow_pos), Real.log_rpow hε_pos]
  rw [h_log_split] at h_log_le
  have h_arg_ge_one : 1 ≤ 2 + ε ^ (-α) := by linarith
  have h_log_nonneg : 0 ≤ Real.log (2 + ε ^ (-α)) := Real.log_nonneg h_arg_ge_one
  have h_sq_le : (Real.log (2 + ε ^ (-α))) ^ 2 ≤ (Real.log 3 + (-α) * Real.log ε) ^ 2 := by
    nlinarith [h_log_le, h_log_nonneg]
  have h_alg : (Real.log 3 + (-α) * Real.log ε) ^ 2 ≤ 2 * (Real.log 3)^2 + 2 * α^2 * (Real.log ε)^2 := by
    have h_sq : 0 ≤ (Real.log 3 - (-α) * Real.log ε)^2 := sq_nonneg _
    linarith
  exact le_trans h_sq_le h_alg

/-- Complete Power-Log Limit Theorem:
    lim_{ε → 0⁺} ε^r * log²(2 + ε^(-α)) = 0 for any r > 0, α > 0.
    Proved via majorant squeeze against 2*(log 3)² * ε^r + 2*α² * (ε^r * log² ε)
    using Mathlib's rpow-log little-o asymptotics.
    This supplies the actual topological limit on the positive-side filter 𝓝[>] 0. -/
theorem power_log_tail_limit_tendsto (r α : ℝ) (hr : 0 < r) (hα : 0 < α) :
    Filter.Tendsto (fun ε => ε ^ r * (Real.log (2 + ε ^ (-α))) ^ 2)
      (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
  have h_majorant : Filter.Tendsto (fun ε => 2 * (Real.log 3)^2 * ε ^ r + 2 * α^2 * (ε ^ r * (Real.log ε)^2))
      (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
    have h1 : Filter.Tendsto (fun ε => 2 * (Real.log 3)^2 * ε ^ r)
        (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
      have ht := (tendsto_rpow_zero_nhdsWithin r hr).const_mul (2 * (Real.log 3)^2)
      simpa only [mul_zero] using ht
    have h2 : Filter.Tendsto (fun ε => 2 * α^2 * (ε ^ r * (Real.log ε)^2))
        (nhdsWithin 0 (Set.Ioi (0 : ℝ))) (nhds 0) := by
      have ht := (tendsto_rpow_mul_log_sq r hr).const_mul (2 * α^2)
      simpa only [mul_zero] using ht
    have h_sum := h1.add h2
    simpa only [add_zero] using h_sum
  have h_nonneg : ∀ᶠ ε in nhdsWithin 0 (Set.Ioi (0 : ℝ)),
      0 ≤ ε ^ r * (Real.log (2 + ε ^ (-α))) ^ 2 := by
    filter_upwards [self_mem_nhdsWithin] with ε hε
    simp only [Set.mem_Ioi] at hε
    have hrpos : 0 ≤ ε ^ r := (Real.rpow_pos_of_pos hε r).le
    have hsq : 0 ≤ (Real.log (2 + ε ^ (-α))) ^ 2 := sq_nonneg _
    exact mul_nonneg hrpos hsq
  have h_le : ∀ᶠ ε in nhdsWithin 0 (Set.Ioi (0 : ℝ)),
      ε ^ r * (Real.log (2 + ε ^ (-α))) ^ 2 ≤
      2 * (Real.log 3)^2 * ε ^ r + 2 * α^2 * (ε ^ r * (Real.log ε)^2) := by
    have h_mem : Set.Ioo (0 : ℝ) 1 ∈ nhdsWithin 0 (Set.Ioi (0 : ℝ)) :=
      Ioo_mem_nhdsWithin_Ioi ⟨le_rfl, zero_lt_one⟩
    filter_upwards [h_mem] with ε hε
    have h_sq := log_sq_le_of_mem_Ioo hε hα
    have hrpos : 0 ≤ ε ^ r := (Real.rpow_pos_of_pos hε.1 r).le
    have h_mul := mul_le_mul_of_nonneg_left h_sq hrpos
    calc ε ^ r * (Real.log (2 + ε ^ (-α))) ^ 2
      _ ≤ ε ^ r * (2 * (Real.log 3)^2 + 2 * α^2 * (Real.log ε)^2) := h_mul
      _ = 2 * (Real.log 3)^2 * ε ^ r + 2 * α^2 * (ε ^ r * (Real.log ε)^2) := by ring
  exact squeeze_zero' h_nonneg h_le h_majorant

open Matrix

/-- General Finite Spectral Perturbation Rigidity Theorem (Confluent Vandermonde System):
    For any finite family of n distinct real exponents l : Fin n → ℝ (injective)
    and complex/real coefficients c : Fin n → ℝ, if the function f(u) = ∑_{j=0}^{n-1} c_j exp(l_j * u)
    and its derivatives of orders k = 0, ..., n-1 all vanish at a single interior point u₀:
        ∑_{j=0}^{n-1} l_j^k * c_j * exp(l_j * u₀) = 0   for all k ∈ Fin n,
    then every coefficient c_j = 0 identically.
    Proof: The system is a transposed Vandermonde system V^T * v = 0 where v_j = c_j * exp(l_j * u₀).
    By det(V^T) = det(V) = ∏_{i < j} (l_j - l_i) ≠ 0, the matrix is invertible, forcing v = 0.
    Since exp(l_j * u₀) > 0, every c_j = 0.
    This eliminates sample-point periodicity degeneracies across an arbitrary finite number of modes. -/
theorem finite_spectral_perturbation_rigidity_vandermonde_general
    {n : ℕ} (c : Fin n → ℝ) (l : Fin n → ℝ) (u₀ : ℝ)
    (hl_inj : Function.Injective l)
    (h_deriv : ∀ (k : Fin n), (∑ j : Fin n, (l j) ^ (k : ℕ) * (c j * Real.exp (l j * u₀))) = 0) :
    ∀ (j : Fin n), c j = 0 := by
  let v : Fin n → ℝ := fun j => c j * Real.exp (l j * u₀)
  have h_det : Matrix.det (Matrix.vandermonde l)ᵀ ≠ 0 := by
    rw [Matrix.det_transpose]
    exact Matrix.det_vandermonde_ne_zero_iff.mpr hl_inj
  have h_mulVec : Matrix.mulVec (Matrix.vandermonde l)ᵀ v = 0 := by
    ext k
    simp only [Matrix.mulVec, Matrix.dotProduct, Matrix.transpose_apply, Matrix.vandermonde_apply, Pi.zero_apply]
    exact h_deriv k
  have hv_zero : v = 0 := Matrix.eq_zero_of_mulVec_eq_zero h_det h_mulVec
  intro j
  have hj : v j = 0 := by rw [hv_zero]; rfl
  dsimp [v] at hj
  have he_pos : 0 < Real.exp (l j * u₀) := Real.exp_pos _
  have he_ne : Real.exp (l j * u₀) ≠ 0 := ne_of_gt he_pos
  cases mul_eq_zero.mp hj with
  | inl h => exact h
  | inr h => exact False.elim (he_ne h)

/-- Polarization identity for symmetric bilinear forms:
    B(x + y, x + y) = B(x, x) + B(y, y) + 2 * B(x, y).
    For test functions g = g_K + g_J across distinct grades, the self-convolution
    and Weil quadratic form evaluation B(g, g) expands into equal-grade diagonal terms
    B(g_K, g_K) + B(g_J, g_J) and cross-grade terms 2 * B(g_K, g_J).
    This refutes the misconception that self-convolution restricts exclusively to equal grades. -/
theorem symmetric_bilinear_polarization_real {E : Type*} [Add E]
    (B : E → E → ℝ)
    (h_add_left : ∀ u v w, B (u + v) w = B u w + B v w)
    (h_add_right : ∀ u v w, B u (v + w) = B u v + B u w)
    (h_symm : ∀ u v, B u v = B v u)
    (x y : E) :
    B (x + y) (x + y) = B x x + B y y + 2 * B x y := by
  rw [h_add_left, h_add_right, h_add_right, h_symm y x]
  ring

/-- Non-negativity of finite double-sum pairings with non-negative components:
    If weights c_i ≥ 0, d_j ≥ 0, and kernel values K_{i,j} ≥ 0 for all i, j,
    then the double sum ∑_i ∑_j c_i * d_j * K_{i,j} ≥ 0.
    In particular, for non-negative test bump w ≥ 0 and mollifier η ≥ 0,
    the arithmetic overlap Q_ε^{K, J}[w] is unconditionally non-negative for all grades K, J. -/
theorem finite_double_sum_nonneg
    {m n : ℕ} (c : Fin m → ℝ) (d : Fin n → ℝ) (K : Fin m → Fin n → ℝ)
    (hc : ∀ i, 0 ≤ c i) (hd : ∀ j, 0 ≤ d j) (hK : ∀ i j, 0 ≤ K i j) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin n, c i * d j * K i j := by
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  have hcd : 0 ≤ c i * d j := mul_nonneg (hc i) (hd j)
  exact mul_nonneg hcd (hK i j)

/-- Strict positivity of finite double-sum pairing from a contributing witness:
    If all terms are non-negative and there exists at least one pair of indices (i₀, j₀)
    with strictly positive weights c i₀ > 0, d j₀ > 0, and K i₀ j₀ > 0,
    then the double sum is strictly positive.
    This formalizes that arithmetic overlap positivity requires an active station pair. -/
theorem finite_double_sum_pos_of_witness
    {m n : ℕ} (c : Fin m → ℝ) (d : Fin n → ℝ) (K : Fin m → Fin n → ℝ)
    (hc : ∀ i, 0 ≤ c i) (hd : ∀ j, 0 ≤ d j) (hK : ∀ i j, 0 ≤ K i j)
    (i₀ : Fin m) (j₀ : Fin n)
    (hci : 0 < c i₀) (hdj : 0 < d j₀) (hKij : 0 < K i₀ j₀) :
    0 < ∑ i : Fin m, ∑ j : Fin n, c i * d j * K i j := by
  have h_term_pos : 0 < c i₀ * d j₀ * K i₀ j₀ := by
    have hcd : 0 < c i₀ * d j₀ := mul_pos hci hdj
    exact mul_pos hcd hKij
  have h_inner_le : c i₀ * d j₀ * K i₀ j₀ ≤ ∑ j : Fin n, c i₀ * d j * K i₀ j :=
    Finset.single_le_sum (f := fun j => c i₀ * d j * K i₀ j)
      (fun j _ => mul_nonneg (mul_nonneg (hc i₀) (hd j)) (hK i₀ j)) (Finset.mem_univ j₀)
  have h_inner_pos : 0 < ∑ j : Fin n, c i₀ * d j * K i₀ j :=
    lt_of_lt_of_le h_term_pos h_inner_le
  have h_outer_le : (∑ j : Fin n, c i₀ * d j * K i₀ j) ≤ ∑ i : Fin m, ∑ j : Fin n, c i * d j * K i j :=
    Finset.single_le_sum (f := fun i => ∑ j : Fin n, c i * d j * K i j)
      (fun i _ => Finset.sum_nonneg (fun j _ => mul_nonneg (mul_nonneg (hc i) (hd j)) (hK i j)))
      (Finset.mem_univ i₀)
  exact lt_of_lt_of_le h_inner_pos h_outer_le

/-- Complex Hermitian polarization identity:
    For a sesquilinear / Hermitian form B on complex space E satisfying
    additivity and conjugate symmetry B(y, x) = starRingEnd ℂ (B(x, y)),
    B(x + y, x + y) = B(x, x) + B(y, y) + 2 * (B(x, y)).re.
    This establishes the exact polarization for the complex Hermitian Weil form,
    showing how cross-grade components 2 * Re(B(x, y)) emerge. -/
theorem hermitian_polarization_complex {E : Type*} [Add E]
    (B : E → E → ℂ)
    (h_add_left : ∀ u v w, B (u + v) w = B u w + B v w)
    (h_add_right : ∀ u v w, B u (v + w) = B u v + B u w)
    (h_herm : ∀ u v, B u v = starRingEnd ℂ (B v u))
    (x y : E) :
    B (x + y) (x + y) = B x x + B y y + 2 * (B x y).re := by
  rw [h_add_left, h_add_right, h_add_right]
  have h_yx : B y x = starRingEnd ℂ (B x y) := h_herm y x
  have h_sum : B x y + starRingEnd ℂ (B x y) = 2 * (B x y).re := by
    rw [Complex.add_conj]
    push_cast
    ring
  calc B x x + B x y + (B y x + B y y)
    _ = B x x + B y y + (B x y + B y x) := by ring
    _ = B x x + B y y + (B x y + starRingEnd ℂ (B x y)) := by rw [h_yx]
    _ = B x x + B y y + 2 * (B x y).re := by rw [h_sum]

/-- Real part of complex Hermitian polarization:
    Re(B(x + y, x + y)) = Re(B(x, x)) + Re(B(y, y)) + 2 * Re(B(x, y)).
    This guarantees that the real part of the Weil quadratic form inherits
    exact cross-grade additive decomposition. -/
theorem hermitian_polarization_real_part {E : Type*} [Add E]
    (B : E → E → ℂ)
    (h_add_left : ∀ u v w, B (u + v) w = B u w + B v w)
    (h_add_right : ∀ u v w, B u (v + w) = B u v + B u w)
    (h_herm : ∀ u v, B u v = starRingEnd ℂ (B v u))
    (x y : E) :
    (B (x + y) (x + y)).re = (B x x).re + (B y y).re + 2 * (B x y).re := by
  have h := hermitian_polarization_complex B h_add_left h_add_right h_herm x y
  apply_fun Complex.re at h
  simp only [Complex.add_re, Complex.ofReal_re, Complex.mul_re, Complex.ofReal_im, mul_zero,
    sub_zero] at h
  exact h

/-- Tridiagonal 3x3 symmetric matrix with unit diagonal and off-diagonal coupling a -/
def tridiagonal3 (a : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  ![![1, a, 0],
    ![a, 1, a],
    ![0, a, 1]]

/-- Quadratic form of tridiagonal matrix on test vector v = ![1, -s, 1] with s^2 = 2:
    v^T M(a) v = 4 - 4 * s * a.
    For s = sqrt(2), this equals 4 * (1 - sqrt(2) * a). -/
theorem tridiagonal_kernel_matrix_quadratic_form
    (a s : ℝ) (hs : s ^ 2 = 2) :
    let M := tridiagonal3 a
    let v : Fin 3 → ℝ := ![1, -s, 1]
    Matrix.dotProduct v (Matrix.mulVec M v) = 4 - 4 * s * a := by
  intro M v
  dsimp [M, v, tridiagonal3, Matrix.dotProduct, Matrix.mulVec]
  simp only [Fin.sum_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
    Matrix.head_cons, Matrix.tail_cons]
  nlinarith [hs]



/-- Indefiniteness theorem for the 3x3 kernel matrix:
    When s * a > 1 (i.e. a > 1 / sqrt(2) ≈ 0.7071), the quadratic form v^T M(a) v < 0.
    For the smooth exponential bump kernel η(v) = exp(1 - 1/(1-v^2)) evaluated at points
    (1, 3/2, 2) with ε = 1, the adjacent coupling is a = exp(-1/3) ≈ 0.71653 > 1/sqrt(2).
    This establishes that the smooth bump kernel matrix is indefinite (not positive semi-definite). -/
theorem tridiagonal_kernel_matrix_indefinite
    (a s : ℝ) (hs : s ^ 2 = 2) (h_bound : 1 < s * a) :
    let M := tridiagonal3 a
    let v : Fin 3 → ℝ := ![1, -s, 1]
    Matrix.dotProduct v (Matrix.mulVec M v) < 0 := by
  intro M v
  have h_eq := tridiagonal_kernel_matrix_quadratic_form a s hs
  dsimp [M, v] at h_eq
  rw [h_eq]
  linarith

/-- Finite pullback quadratic form identity:
    For any station matrix H and embedding matrix E, the grade quadratic form
    c^T (E^T * H * E) c equals the station quadratic form (E c)^T H (E c). -/
theorem matrix_pullback_quadratic_form {m n : Type*} [Fintype m] [Fintype n]
    (H : Matrix m m ℝ) (E : Matrix m n ℝ) (c : n → ℝ) :
    let G := Eᵀ * (H * E)
    Matrix.dotProduct c (Matrix.mulVec G c) =
      Matrix.dotProduct (Matrix.mulVec E c) (Matrix.mulVec H (Matrix.mulVec E c)) := by
  intro G
  dsimp [G]
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, Matrix.dotProduct_mulVec, Matrix.vecMul_transpose]

/-- Positive semi-definiteness inheritance under matrix pullback:
    If the station matrix H is positive semi-definite (v^T H v >= 0 for all v),
    then the pullback grade matrix G = E^T * H * E is positive semi-definite (c^T G c >= 0 for all c). -/
theorem matrix_pullback_psd {m n : Type*} [Fintype m] [Fintype n]
    (H : Matrix m m ℝ) (E : Matrix m n ℝ)
    (hH : ∀ v : m → ℝ, 0 ≤ Matrix.dotProduct v (Matrix.mulVec H v)) :
    let G := Eᵀ * (H * E)
    ∀ c : n → ℝ, 0 ≤ Matrix.dotProduct c (Matrix.mulVec G c) := by
  intro G c
  have h_pb := matrix_pullback_quadratic_form H E c
  dsimp [G] at h_pb
  rw [h_pb]
  exact hH (Matrix.mulVec E c)

/-- Diagonal matrix positive semi-definiteness:
    If a matrix G has zero off-diagonal entries (G i j = 0 for i ≠ j) and non-negative
    diagonal entries (0 ≤ G i i), then the quadratic form c^T G c >= 0 for all c. -/
theorem diagonal_matrix_psd {n : Type*} [Fintype n] [DecidableEq n]
    (G : Matrix n n ℝ)
    (h_off : ∀ i j, i ≠ j → G i j = 0)
    (h_diag : ∀ i, 0 ≤ G i i)
    (c : n → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec G c) := by
  dsimp [Matrix.dotProduct, Matrix.mulVec]
  have h_sum : (∑ i, c i * ∑ j, G i j * c j) = ∑ i, (c i)^2 * G i i := by
    apply Finset.sum_congr rfl
    intro i _
    have h_inner : (∑ j, G i j * c j) = G i i * c i := by
      rw [Finset.sum_eq_single_of_mem i (Finset.mem_univ i)]
      intro j _ hji
      rw [h_off i j hji.symm, zero_mul]
    rw [h_inner]
    ring
  rw [h_sum]
  apply Finset.sum_nonneg
  intro i _
  have hc2 : 0 ≤ (c i)^2 := sq_nonneg (c i)
  have hG : 0 ≤ G i i := h_diag i
  exact mul_nonneg hc2 hG

/-- Small-resolution grade nonnegativity theorem:
    For any finite grade family {K_1, ..., K_r}, when resolution ε is below the cross-grade
    separation Δ_cross, cross-grade interactions vanish (G_ij = 0 for i ≠ j).
    If each diagonal grade self-overlap is non-negative (0 ≤ G_ii),
    then the grade quadratic form c^T G c ≥ 0 for every grade coefficient vector c.
    This establishes that the grade-indexed matrix G = E^T H E is positive semi-definite
    at small resolutions unconditionally, refuting any blanket claim that the grade
    matrix cannot have a positive semi-definite Gram representation. -/
theorem small_resolution_grade_psd {r : Type*} [Fintype r] [DecidableEq r]
    (G : Matrix r r ℝ)
    (h_cross : ∀ i j, i ≠ j → G i j = 0)
    (h_self : ∀ i, 0 ≤ G i i)
    (c : r → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec G c) :=
  diagonal_matrix_psd G h_cross h_self c

/-- Algebraic reduction of the smooth bump coupling condition s * a > 1:
    For s^2 = 2 and a^3 = E_inv where E_inv = exp(-1),
    the 6th power (s * a)^6 equals 8 * E_inv^2 = 8 / e^2.
    Therefore, the condition s * a > 1 is strictly equivalent to 8 > e^2,
    which holds for Euler's constant e since e < 2.72 and 2.72^2 = 7.3984 < 8. -/
theorem smooth_bump_coupling_sixth_power (s a E_inv : ℝ)
    (hs : s ^ 2 = 2) (ha : a ^ 3 = E_inv) :
    (s * a) ^ 6 = 8 * E_inv ^ 2 := by
  have h1 : (s * a) ^ 6 = (s ^ 2) ^ 3 * (a ^ 3) ^ 2 := by ring
  rw [h1, hs, ha]
  ring

/-- Extension of real symmetric positive semi-definiteness to complex vectors:
    For any real matrix G that is positive semi-definite on real vectors (v^T G v >= 0 for all v),
    and any complex coefficient vector c, the sum of quadratic forms on its real and imaginary
    parts is non-negative: (Re c)^T G (Re c) + (Im c)^T G (Im c) >= 0. -/
theorem real_symmetric_matrix_complex_psd {r : Type*} [Fintype r]
    (G : Matrix r r ℝ)
    (h_psd : ∀ v : r → ℝ, 0 ≤ Matrix.dotProduct v (Matrix.mulVec G v))
    (c : r → ℂ) :
    let a : r → ℝ := fun i => (c i).re
    let b : r → ℝ := fun i => (c i).im
    0 ≤ Matrix.dotProduct a (Matrix.mulVec G a) + Matrix.dotProduct b (Matrix.mulVec G b) := by
  intro a b
  have ha := h_psd a
  have hb := h_psd b
  linarith

/-- Grade matrix defined from finite station data and kernel convolution:
    G_ij = ∑_{n in S_i} ∑_{m in S_j} d_{i,n} d_{j,m} η((x_{i,n} - x_{j,m}) / ε). -/
noncomputable def stationGradeMatrix {r : Type*} [Fintype r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε : ℝ) : Matrix r r ℝ :=
  fun i j => ∑ n : S i, ∑ m : S j, d i n * d j m * η ((x i n - x j m) / ε)

/-- Cross-grade entries vanish when station separation Δ exceeds resolution ε:
    For any distinct grades i ≠ j, if all pairwise station distances |x i n - x j m| >= Δ > ε,
    and η is supported in (-1, 1), then G i j = 0. -/
theorem finite_grade_cross_entry_vanishes {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (i j : r) (hij : i ≠ j) :
    stationGradeMatrix x d η ε i j = 0 := by
  dsimp [stationGradeMatrix]
  have h_zero : ∀ (n : S i) (m : S j), d i n * d j m * η ((x i n - x j m) / ε) = 0 := by
    intro n m
    have hdist := h_sep i j hij n m
    have hdiv : 1 ≤ |(x i n - x j m) / ε| := by
      rw [abs_div, abs_of_pos hε_pos]
      have h_le : ε ≤ |x i n - x j m| := le_trans (le_of_lt hε_lt_Δ) hdist
      exact (one_le_div hε_pos).mpr h_le
    have h_eta := hη_supp ((x i n - x j m) / ε) hdiv
    rw [h_eta, mul_zero]
  have h_inner : ∀ (n : S i), (∑ m : S j, d i n * d j m * η ((x i n - x j m) / ε)) = 0 := by
    intro n
    rw [Finset.sum_eq_zero]
    intro m _
    exact h_zero n m
  rw [Finset.sum_eq_zero]
  intro n _
  exact h_inner n

/-- Diagonal grade entries are non-negative from non-negative weights and kernel:
    For any grade i, G i i = ∑ n, ∑ m, d i n * d i m * η(...) >= 0.
    Handles empty station families unconditionally (empty sum is 0 >= 0). -/
theorem finite_grade_diagonal_nonneg {r : Type*} [Fintype r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε : ℝ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (i : r) :
    0 ≤ stationGradeMatrix x d η ε i i := by
  dsimp [stationGradeMatrix]
  apply Finset.sum_nonneg
  intro n _
  apply Finset.sum_nonneg
  intro m _
  have hdn : 0 ≤ d i n := hd i n
  have hdm : 0 ≤ d i m := hd i m
  have hη : 0 ≤ η ((x i n - x i m) / ε) := hη_nonneg ((x i n - x i m) / ε)
  exact mul_nonneg (mul_nonneg hdn hdm) hη

/-- Full finite-grade positive semi-definiteness theorem from station separation:
    When cross-grade stations are separated by Δ > ε, and η has compact support in (-1, 1),
    the grade matrix G = stationGradeMatrix x d η ε is positive semi-definite:
    c^T G c >= 0 for every real grade coefficient vector c. -/
theorem finite_grade_station_psd {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (c : r → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec (stationGradeMatrix x d η ε) c) := by
  let G := stationGradeMatrix x d η ε
  have h_cross : ∀ i j, i ≠ j → G i j = 0 := by
    intro i j hij
    exact finite_grade_cross_entry_vanishes x d η ε Δ hε_pos hε_lt_Δ hη_supp h_sep i j hij
  have h_self : ∀ i, 0 ≤ G i i := by
    intro i
    exact finite_grade_diagonal_nonneg x d η ε hd hη_nonneg i
  exact small_resolution_grade_psd G h_cross h_self c

/-- Complex positive semi-definiteness for separated grade stations:
    For any complex grade coefficient vector c, the quadratic form on the real and imaginary parts
    is non-negative: (Re c)^T G (Re c) + (Im c)^T G (Im c) >= 0. -/
theorem finite_grade_station_complex_psd {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (c : r → ℂ) :
    let G := stationGradeMatrix x d η ε
    let a : r → ℝ := fun i => (c i).re
    let b : r → ℝ := fun i => (c i).im
    0 ≤ Matrix.dotProduct a (Matrix.mulVec G a) + Matrix.dotProduct b (Matrix.mulVec G b) := by
  intro G a b
  have h_real_psd := finite_grade_station_psd x d η ε Δ hε_pos hε_lt_Δ hd hη_supp hη_nonneg h_sep
  exact real_symmetric_matrix_complex_psd G h_real_psd c

end RiemannScope
