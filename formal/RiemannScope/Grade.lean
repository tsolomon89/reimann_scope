/-
RiemannScope.Grade
Tau-grade group structure, bilateral integer scale inverses, and grade-centering geometry.
Reference: MATH_CONTRACT.md §2, §39
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Pow.Real
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

end RiemannScope


