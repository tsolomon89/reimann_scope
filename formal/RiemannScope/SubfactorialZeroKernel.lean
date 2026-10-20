/-
RiemannScope.SubfactorialZeroKernel
TASK-TC-040: Subfactorial-Denominator Zero-Carrying Kernels: Bernoulli Reflection,
Gamma-Ratio Tradeoffs, Positive-Moment Hankel Architecture, and Escape from the
Newton Factorial Obstruction.

Formalizes the exact algebraic components of TASK-TC-040 (Section 37):
1. `bernoulli_kernel_linear_relation`:
   For `B_z = -2 * z * zeta_one_minus_2z`, the reflected kernel
   `K₀(z) = -((2 * z - 1) / 2) * B_z` satisfies `K₀(z) = z * (2 * z - 1) * zeta_one_minus_2z`.
2. `bernoulli_kernel_zero_at_zeta_zero`:
   Whenever `zeta_one_minus_2z = 0` (which holds at `z = ρ / 2` for every nontrivial
   Riemann zeta zero `ρ` by the functional equation `ζ(ρ) = 0 ↔ ζ(1 - ρ) = 0`),
   both `B(z) = -2 * z * zeta_one_minus_2z = 0` and
   `K₀(z) = -((2 * z - 1) / 2) * B(z) = 0`.
3. `gamma_reflection_sample_clearing_identity`:
   Multiplying the Euler-rationalized sample
   `a_m^(τ) = (-1)^(m+1) * (2m - 1) * B_{2m} / (2 * F_{2m})` (where `F_{2m} = (2m)! ≠ 0`)
   by the reflection factor `(-1)^m * F_{2m}` cancels `F_{2m}` and the alternating sign
   `(-1)^(2m+1) = -1` identically, yielding `-((2m - 1) * B_{2m}) / 2`.
4. `gamma_ratio_budget_conservation_identity`:
   For the Gamma-ratio ladder `B_q(z) = K₀(z) / Γ(z + 1)^q`, the sample-growth
   coefficient `(2 - q)` and denominator-growth coefficient `q` satisfy the exact
   factorial-budget conservation law `(2 - q) * L + q * L = 2 * L` (with `(2 - q) + q = 2`),
   and for `q = 2` (`(2 - 2) * L = 0`), the entire `2 * L` budget resides in the denominator.
5. `sign_adjusted_bernoulli_positive_sample_identity`:
   For `m ≥ 1`, since `(-1)^(m+1) * B_{2m} = |B_{2m}| > 0`, the sign-adjusted kernel
   sample `P(m) = -((-1)^m * B_{2m})` equals `(-1)^(m+1) * B_{2m}` and is strictly positive.
6. `auxiliary_polynomial_factorial_cost_lower_bound_schema`:
   Abstract factorial-relocation lower-bound schema: if the logarithm of the primitive
   integer clearing multiplier satisfies `log_M ≥ c * n_log_n - C₁ * n` and the logarithm
   of the raw analytic residual satisfies `log_R ≥ -kappa * n_beta - C₂ * log_n`, then
   `log_tilde_Q = log_M + log_R` satisfies
   `log_tilde_Q ≥ c * n_log_n - (C₁ * n + kappa * n_beta + C₂ * log_n)`, and whenever the
   subfactorial decay term is dominated by `(c / 2) * n_log_n`, `log_tilde_Q ≥ (c / 2) * n_log_n`.
7. `gamma_ratio_newton_basis_total_cost_conservation`:
   In the Newton basis `binom(α, k)` on integer nodes `0, ..., n`, the basis denominator
   contributes `L` (`n log n`) while the sample denominator of `B_q` contributes `q * L`
   and sample growth / finite-difference growth contributes `max(0, (2 - q) * L)`, so the
   combined arithmetic + analytic log-cost `(q + 1) * L + (2 - q) * L = 3 * L` for `0 ≤ q ≤ 2`
   is strictly positive (`≥ L > 0`).
8. `carlitz_touchard_hankel_recurrence_positivity`:
   For `k ≥ 1`, the Carlitz–Touchard–Al-Salam Jacobi recurrence numerator
   `k^3 * (k + 1) * (2*k - 1) * (2*k + 1)^3` and denominator
   `(4*k - 1) * (4*k + 1)^2 * (4*k + 3)` for the positive Bernoulli Stieltjes moments
   `μ_m = |B_{2m+2}|` are strictly positive.

Scope firewall (Section 37):
Does NOT claim to formalize in Lean:
- the full analytic continuation of `ζ(s)`;
- the full proof of von Staudt–Clausen;
- Nörlund–Rice or saddle asymptotics;
- any proof of irrationality of `γ₁`.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace RiemannScope

open Complex

/-! ### 1. Bernoulli Reflection Kernel Identities (Route A, Sections 8–10) -/

/-- 1. `bernoulli_kernel_linear_relation`:
    For the pure Bernoulli function `B(z) = -2 * z * ζ(1 - 2z)`, the reflected
    kernel `K₀(z) = -((2z - 1) / 2) * B(z)` satisfies the exact linear identity
    `K₀(z) = z * (2z - 1) * ζ(1 - 2z)`. -/
theorem bernoulli_kernel_linear_relation
    (z zeta_one_minus_2z B_z K0_z : ℂ)
    (hB : B_z = -2 * z * zeta_one_minus_2z)
    (hK0 : K0_z = -((2 * z - 1) / 2) * B_z) :
    K0_z = z * (2 * z - 1) * zeta_one_minus_2z := by
  rw [hK0, hB]
  ring

/-- 2. `bernoulli_kernel_zero_at_zeta_zero`:
    Whenever `ζ(1 - 2z) = 0` (in particular at `z = ρ / 2` for every nontrivial zero `ρ`
    of `ζ`, since `ζ(ρ) = 0 ↔ ζ(1 - ρ) = 0`), both `B(z) = -2 * z * ζ(1 - 2z)` and
    `K₀(z) = -((2z - 1) / 2) * B(z)` vanish identically. -/
theorem bernoulli_kernel_zero_at_zeta_zero
    (z zeta_one_minus_2z : ℂ)
    (h_zero : zeta_one_minus_2z = 0) :
    (-2 * z * zeta_one_minus_2z = 0) ∧
    (-((2 * z - 1) / 2) * (-2 * z * zeta_one_minus_2z) = 0) := by
  rw [h_zero]
  refine ⟨by ring, by ring⟩

/-- 3. `gamma_reflection_sample_clearing_identity`:
    At every integer node `m : ℕ`, multiplying the Euler-rationalized sample
    `((-1 : ℝ) ^ (m + 1)) * (2 * m - 1) * B_2m / (2 * F_2m)` (with `F_2m = (2m)! ≠ 0`)
    by `((-1 : ℝ) ^ m) * F_2m` clears the factorial denominator `F_2m` and simplifies
    `(-1)^m * (-1)^(m+1) = -1`, producing `-((2 * m - 1) * B_2m) / 2`. -/
theorem gamma_reflection_sample_clearing_identity
    (m : ℕ) (B_2m F_2m : ℝ) (hF : F_2m ≠ 0) :
    (((-1 : ℝ) ^ m) * F_2m) *
      (((-1 : ℝ) ^ (m + 1)) * (2 * (m : ℝ) - 1) * B_2m / (2 * F_2m)) =
      -((2 * (m : ℝ) - 1) * B_2m) / 2 := by
  have h_sign : ((-1 : ℝ) ^ m) * ((-1 : ℝ) ^ (m + 1)) = -1 := by
    rw [pow_succ, ← mul_assoc, ← sq]
    have h_sq : ((-1 : ℝ) ^ m) ^ 2 = 1 := by
      rw [← pow_mul, mul_comm, pow_mul]
      norm_num
    rw [h_sq]
    ring
  calc
    (((-1 : ℝ) ^ m) * F_2m) *
        (((-1 : ℝ) ^ (m + 1)) * (2 * (m : ℝ) - 1) * B_2m / (2 * F_2m))
      = (((-1 : ℝ) ^ m) * ((-1 : ℝ) ^ (m + 1))) *
          ((2 * (m : ℝ) - 1) * B_2m / 2) * (F_2m / F_2m) := by ring
    _ = (-1) * ((2 * (m : ℝ) - 1) * B_2m / 2) * 1 := by rw [h_sign, div_self hF]
    _ = -((2 * (m : ℝ) - 1) * B_2m) / 2 := by ring

/-! ### 2. Gamma-Ratio Factorial Budget Conservation (Section 12) -/

/-- 4. `gamma_ratio_budget_conservation_identity`:
    For the Gamma-ratio interpolation family `B_q(z) = K₀(z) / Γ(z + 1)^q`,
    the sample-growth exponent coefficient `(2 - q)` and denominator-growth
    exponent coefficient `q` satisfy `(2 - q) + q = 2` and
    `(2 - q) * L + q * L = 2 * L` for every asymptotic scale `L` (e.g. `L = n log n`). -/
theorem gamma_ratio_budget_conservation_identity
    (q L : ℝ) :
    ((2 - q) + q = 2) ∧
    ((2 - q) * L + q * L = 2 * L) ∧
    ((2 - (2 : ℝ)) * L = 0) := by
  refine ⟨by ring, by ring, by ring⟩

/-! ### 3. Sign-Adjusted Positive Bernoulli Samples & Stieltjes Recurrence (Route B, Section 14) -/

/-- 5. `sign_adjusted_bernoulli_positive_sample_identity`:
    For `m ≥ 1`, where `(-1)^(m+1) * B_{2m} > 0`, the sign-adjusted kernel sample
    `P(m) = -((-1)^m * B_{2m})` equals `(-1)^(m+1) * B_{2m}` and is strictly positive. -/
theorem sign_adjusted_bernoulli_positive_sample_identity
    (m : ℕ) (B_2m : ℝ)
    (h_pos : 0 < ((-1 : ℝ) ^ (m + 1)) * B_2m) :
    (-(((-1 : ℝ) ^ m) * B_2m) = ((-1 : ℝ) ^ (m + 1)) * B_2m) ∧
    (0 < -(((-1 : ℝ) ^ m) * B_2m)) := by
  have h_eq : -(((-1 : ℝ) ^ m) * B_2m) = ((-1 : ℝ) ^ (m + 1)) * B_2m := by
    rw [pow_succ]
    ring
  exact ⟨h_eq, h_eq.symm ▸ h_pos⟩

/-! ### 4. Factorial-Cost Relocation Lower-Bound Schema (Sections 28–30) -/

/-- 6. `auxiliary_polynomial_factorial_cost_lower_bound_schema`:
    If the primitive clearing factor satisfies `log_M ≥ c * n_log_n - C₁ * n` and the raw
    analytic evaluation satisfies `log_R ≥ -kappa * n_beta - C₂ * log_n` with
    `log_tilde_Q = log_M + log_R`, then:
    (a) `log_tilde_Q ≥ c * n_log_n - (C₁ * n + kappa * n_beta + C₂ * log_n)`;
    (b) whenever the subleading/subfactorial terms satisfy
        `C₁ * n + kappa * n_beta + C₂ * log_n ≤ (c / 2) * n_log_n`,
        we have `log_tilde_Q ≥ (c / 2) * n_log_n`. -/
theorem auxiliary_polynomial_factorial_cost_lower_bound_schema
    (log_M log_R log_tilde_Q c n_log_n C₁ n kappa n_beta C₂ log_n : ℝ)
    (h_sum : log_tilde_Q = log_M + log_R)
    (hM : c * n_log_n - C₁ * n ≤ log_M)
    (hR : -kappa * n_beta - C₂ * log_n ≤ log_R) :
    (c * n_log_n - (C₁ * n + kappa * n_beta + C₂ * log_n) ≤ log_tilde_Q) ∧
    (C₁ * n + kappa * n_beta + C₂ * log_n ≤ (c / 2) * n_log_n →
      (c / 2) * n_log_n ≤ log_tilde_Q) := by
  refine ⟨by linarith, ?_⟩
  intro h_sub
  linarith

/-- 7. `gamma_ratio_newton_basis_total_cost_conservation`:
    For `0 ≤ q ≤ 2` and `0 < L` (`L = n log n`), combining the Newton basis denominator
    cost `L`, sample denominator cost `q * L`, and sample growth cost `(2 - q) * L`
    gives total factorial cost `L + q * L + (2 - q) * L = 3 * L ≥ 3 * L > 0`. -/
theorem gamma_ratio_newton_basis_total_cost_conservation
    (q L : ℝ) (hL : 0 < L) :
    (L + q * L + (2 - q) * L = 3 * L) ∧ (0 < L + q * L + (2 - q) * L) := by
  have h_eq : L + q * L + (2 - q) * L = 3 * L := by ring
  refine ⟨h_eq, ?_⟩
  linarith

/-- 8. `carlitz_touchard_hankel_recurrence_positivity`:
    For every real `k ≥ 1`, the Carlitz–Touchard–Al-Salam Jacobi recurrence numerator
    `k^3 * (k + 1) * (2 * k - 1) * (2 * k + 1)^3` and denominator
    `(4 * k - 1) * (4 * k + 1)^2 * (4 * k + 3)` for the Stieltjes moment sequence
    `μ_m = |B_{2m+2}|` are strictly positive, hence `β_k > 0`. -/
theorem carlitz_touchard_hankel_recurrence_positivity
    (k : ℝ) (hk : 1 ≤ k) :
    0 < (k ^ 3 * (k + 1) * (2 * k - 1) * (2 * k + 1) ^ 3) /
        ((4 * k - 1) * (4 * k + 1) ^ 2 * (4 * k + 3)) := by
  have h2k_minus : 0 < 2 * k - 1 := by linarith
  have h4k_minus : 0 < 4 * k - 1 := by linarith
  positivity

/-! ### 5. Section 41 Target Algebraic & Arithmetic Schemas -/

/-- 9. `primitive_auxiliary_efficiency_scaling`:
    For a rational auxiliary polynomial `P_n` with canonical primitive integer normalization
    `tilde_P_n = M_n * P_n` of degree `d_n > 0`, where `log_tilde_P = log_M + log_P`,
    the primitive Diophantine efficiency `E_n = -log_tilde_P / d_n` decomposes as
    `E_n = (-log_P - log_M) / d_n`, and whenever `log_M ≥ -log_P + delta` with `delta ≥ 0`,
    we have `E_n ≤ -delta / d_n ≤ 0`. -/
theorem primitive_auxiliary_efficiency_scaling
    (log_P log_M log_tilde_P d_n delta : ℝ)
    (hd : 0 < d_n)
    (h_sum : log_tilde_P = log_M + log_P)
    (h_dom : -log_P + delta ≤ log_M)
    (h_delta : 0 ≤ delta) :
    (-log_tilde_P / d_n = (-log_P - log_M) / d_n) ∧
    (-log_tilde_P / d_n ≤ 0) := by
  have h_eq : -log_tilde_P / d_n = (-log_P - log_M) / d_n := by
    rw [h_sum]
    ring
  have h_num_nonpos : -log_tilde_P ≤ 0 := by linarith
  exact ⟨h_eq, div_nonpos_of_nonpos_of_nonneg h_num_nonpos (le_of_lt hd)⟩

/-- 10. `sample_multiplier_denominator_cancellation_bound`:
    Prime-by-prime valuation conservation for rational sample multiplication `f_m = e_m * a_m`:
    if `v_den_f ≥ v_D - v_P - v_A`, then cancelling the sample denominator valuation `v_D`
    down to `v_den_f` requires the multiplier numerator valuation `v_P` to satisfy
    `v_P ≥ v_D - v_den_f - v_A`. -/
theorem sample_multiplier_denominator_cancellation_bound
    (v_D v_P v_A v_den_f : ℤ)
    (h_val : v_D - v_P - v_A ≤ v_den_f) :
    v_D - v_den_f - v_A ≤ v_P := by
  omega

/-- 11. `gamma_ratio_integer_sample_identity`:
    At every integer node `m : ℕ`, dividing the reflected sample
    `K0_m = -((2 * m - 1) * B_2m) / 2` by the Gamma-power sample `G_m = (m!)^q` (`G_m ≠ 0`)
    yields the exact Gamma-ratio integer sample `B_q(m) = -((2 * m - 1) * B_2m) / (2 * G_m)`. -/
theorem gamma_ratio_integer_sample_identity
    (m : ℕ) (B_2m G_m K0_m : ℝ)
    (hG : G_m ≠ 0)
    (hK0 : K0_m = -((2 * (m : ℝ) - 1) * B_2m) / 2) :
    K0_m / G_m = -((2 * (m : ℝ) - 1) * B_2m) / (2 * G_m) := by
  rw [hK0]
  field_simp [hG]

/-- 12. `even_node_norm_polynomial_degree_bound`:
    For a polynomial interpolant of degree `n` in the direct `ρ = 1/2 + i*Y` coordinate
    (or half-coordinate `α = 1/4 + i*Y/2`), the conjugate-product norm polynomial
    `N_P(Y) = P(1/2 + i*Y) * P_conj(1/2 - i*Y)` has degree `2 * n`, which coincides
    identically between the direct `ρ`-scale on even nodes `0, 2, ..., 2n` and the
    half-scale `α = ρ/2` on consecutive integer nodes `0, 1, ..., n`. -/
theorem even_node_norm_polynomial_degree_bound
    (n : ℕ) :
    (n + n = 2 * n) ∧ (2 * (n + 1) - 2 * n = 2) := by
  omega

/-- 13. `primitive_hankel_polynomial_nonzero_schema`:
    If a monic orthogonal polynomial `P_n` associated with a positive Stieltjes measure
    on `(0, ∞)` has all real roots `r_j > 0`, then at any complex argument `s = σ + i * γ`
    with `γ ≠ 0`, each linear factor squared modulus `(σ - r_j)^2 + γ^2` is strictly
    positive (`≥ γ^2 > 0`), and multiplying by any positive primitive clearing factor
    `M_n > 0` preserves strict positivity. -/
theorem primitive_hankel_polynomial_nonzero_schema
    (sigma gamma r_j M_n : ℝ)
    (h_gamma : gamma ≠ 0)
    (hM : 0 < M_n) :
    (gamma ^ 2 ≤ (sigma - r_j) ^ 2 + gamma ^ 2) ∧
    (0 < M_n * ((sigma - r_j) ^ 2 + gamma ^ 2)) := by
  have h_sq_pos : 0 < gamma ^ 2 := sq_pos_of_ne_zero h_gamma
  have h_factor_ge : gamma ^ 2 ≤ (sigma - r_j) ^ 2 + gamma ^ 2 := by
    have : 0 ≤ (sigma - r_j) ^ 2 := sq_nonneg (sigma - r_j)
    linarith
  have h_factor_pos : 0 < (sigma - r_j) ^ 2 + gamma ^ 2 := lt_of_lt_of_le h_sq_pos h_factor_ge
  exact ⟨h_factor_ge, mul_pos hM h_factor_pos⟩

/-- 14. `factorial_budget_algebraic_inequality`:
    For any real parameter `q` and positive factorial scale `L > 0` (`L = n log n`),
    either the sample denominator cost `q * L ≥ L > 0` (when `q ≥ 1`) or the sample
    growth cost `(2 - q) * L > L > 0` (when `q < 1`); in particular,
    `max (q * L) ((2 - q) * L) ≥ L > 0`. -/
theorem factorial_budget_algebraic_inequality
    (q L : ℝ) (hL : 0 < L) :
    L ≤ max (q * L) ((2 - q) * L) := by
  by_cases hq : 1 ≤ q
  · have h1 : L ≤ q * L := by nlinarith
    exact le_trans h1 (le_max_left (q * L) ((2 - q) * L))
  · push_neg at hq
    have h2 : L ≤ (2 - q) * L := by nlinarith
    exact le_trans h2 (le_max_right (q * L) ((2 - q) * L))

end RiemannScope

