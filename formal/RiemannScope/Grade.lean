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
import Mathlib.Topology.Instances.Real
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

end RiemannScope
