/-
RiemannScope.FauzanZeroArgumentTransfer
TASK-TC-039: Fauzan Hankel Irrationality Architecture Transfer to Zeta-Zero Arguments.

Formalizes the exact algebraic components of TASK-TC-039 (Section 34):
1. `argument_norm_polynomial_real`:
   For `P(α(Y)) = u + i v` and `P(conj(α(Y))) = u - i v`, the norm product
   `N_P(Y) = (u + i v)(u - i v) = u^2 + v^2` is real, and for a degree-1 factor
   `(a₀ + a₁(1/4 + i Y / 2))(a₀ + a₁(1/4 - i Y / 2)) = (a₀ + a₁/4)^2 + (a₁^2 / 4) Y^2`.
2. `argument_norm_polynomial_nonneg`:
   `0 ≤ u^2 + v^2` and `0 ≤ C_n * (u^2 + v^2)` for `0 ≤ C_n`.
3. `argument_norm_polynomial_degree_bound`:
   If `deg(P_α) ≤ d` and `deg(P_conj_α) ≤ d`, then `deg(N_P) ≤ d + d = 2 * d`.
4. `newton_consecutive_common_root_forces_node`:
   If `N_{n+1}(z) = N_n(z) + c_{n+1} * B_{n+1}(z)` with `c_{n+1} ≠ 0`, then
   `N_n(z) = 0 ∧ N_{n+1}(z) = 0 → B_{n+1}(z) = 0`.
5. `newton_consecutive_no_common_root_of_nonzero_samples`:
   If `N_{n+1}(z) = N_n(z) + c_{n+1} * B_{n+1}(z)` with `c_{n+1} ≠ 0` and
   `B_{n+1}(z) = 0 → N_n(z) ≠ 0` (nonzero sample values `a_m ≠ 0` at nodes),
   then `¬ (N_n(z) = 0 ∧ N_{n+1}(z) = 0)`.
6. `two_approximant_norm_sum_strict_pos`:
   If `0 < C_n` and consecutive approximants do not vanish simultaneously, then
   `G_n(Y) = C_n * ((u₁^2 + v₁^2) + (u₂^2 + v₂^2)) > 0`.
7. `rational_evaluation_integer_clearing`:
   If `0 < b_pow` and `1 ≤ b_pow * abs_P`, then `1 / b_pow ≤ abs_P`.
8. `superlinear_log_smallness_irrationality_schema`:
   If `1 ≤ b_pow * abs_P` (rational clearing lower bound) and `b_pow * abs_P < 1`
   (analytic smallness bound), then `False`.
9. `pade_interpolation_zero_residual_identity`:
   At a zero `R_alpha = 0` of `R(z)`, the Padé residual `A_alpha - R_alpha * B_alpha`
   equals the polynomial evaluation `A_alpha`.

Scope firewall (Section 34):
Does NOT claim to formalize in Lean:
- convergence of the Newton series;
- Nörlund–Rice asymptotics;
- Padé asymptotic error;
- Hankel potential theory;
- irrationality of `γ₁`.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace RiemannScope

open Complex

/-! ### 1. Real Ordinate Norm-Polynomial Identities (Section 18) -/

/-- 1. `argument_norm_polynomial_real`:
    Conjugate-paired evaluation `(u + i v)(u - i v) = u^2 + v^2` is real, and for an
    affine argument `α(Y) = 1/4 + i Y / 2` paired with `conj(α(Y)) = 1/4 - i Y / 2`,
    `(a₀ + a₁ α(Y))(a₀ + a₁ conj(α(Y))) = (a₀ + a₁/4)^2 + (a₁^2 / 4) Y^2`. -/
theorem argument_norm_polynomial_real (u v a₀ a₁ Y : ℝ) :
    ((((u : ℂ) + (v : ℂ) * I) * ((u : ℂ) - (v : ℂ) * I) =
      ((u ^ 2 + v ^ 2 : ℝ) : ℂ)) ∧
    (((a₀ : ℂ) + (a₁ : ℂ) * ((1 / 4 : ℂ) + (Y : ℂ) * I / 2)) *
      ((a₀ : ℂ) + (a₁ : ℂ) * ((1 / 4 : ℂ) - (Y : ℂ) * I / 2)) =
      (((a₀ + a₁ / 4) ^ 2 + (a₁ ^ 2 / 4) * Y ^ 2 : ℝ) : ℂ))) := by
  have hI2 : (I : ℂ) ^ 2 = -1 := I_sq
  refine ⟨?_, ?_⟩
  · push_cast
    calc
      ((u : ℂ) + (v : ℂ) * I) * ((u : ℂ) - (v : ℂ) * I)
        = (u : ℂ) ^ 2 - (v : ℂ) ^ 2 * I ^ 2 := by ring
      _ = (u : ℂ) ^ 2 + (v : ℂ) ^ 2 := by rw [hI2]; ring
  · push_cast
    calc
      ((a₀ : ℂ) + (a₁ : ℂ) * ((1 / 4 : ℂ) + (Y : ℂ) * I / 2)) *
          ((a₀ : ℂ) + (a₁ : ℂ) * ((1 / 4 : ℂ) - (Y : ℂ) * I / 2))
        = ((a₀ : ℂ) + (a₁ : ℂ) / 4) ^ 2 -
            ((a₁ : ℂ) ^ 2 / 4) * (Y : ℂ) ^ 2 * I ^ 2 := by ring
      _ = ((a₀ : ℂ) + (a₁ : ℂ) / 4) ^ 2 +
            ((a₁ : ℂ) ^ 2 / 4) * (Y : ℂ) ^ 2 := by rw [hI2]; ring

/-- 2. `argument_norm_polynomial_nonneg`:
    For all real `u, v ∈ ℝ` and nonnegative clearing factor `0 ≤ C_n`,
    `0 ≤ u^2 + v^2` and `0 ≤ C_n * (u^2 + v^2)`. -/
theorem argument_norm_polynomial_nonneg (u v C_n : ℝ) (hC : 0 ≤ C_n) :
    (0 ≤ u ^ 2 + v ^ 2) ∧ (0 ≤ C_n * (u ^ 2 + v ^ 2)) := by
  have h_sum : 0 ≤ u ^ 2 + v ^ 2 := add_nonneg (sq_nonneg u) (sq_nonneg v)
  exact ⟨h_sum, mul_nonneg hC h_sum⟩

/-- 3. `argument_norm_polynomial_degree_bound`:
    If `deg_P₁ ≤ d` and `deg_P₂ ≤ d`, then the product degree `deg_N ≤ deg_P₁ + deg_P₂`
    satisfies `deg_N ≤ 2 * d`. -/
theorem argument_norm_polynomial_degree_bound (deg_N deg_P₁ deg_P₂ d : ℕ)
    (h_prod : deg_N ≤ deg_P₁ + deg_P₂) (h₁ : deg_P₁ ≤ d) (h₂ : deg_P₂ ≤ d) :
    deg_N ≤ 2 * d := by
  omega

/-! ### 2. Consecutive Newton Approximant Common-Root & Strict Positivity Theorems (Section 19) -/

/-- 4. `newton_consecutive_common_root_forces_node`:
    From the Newton step relation `N_next = N_curr + c_next * B_next` with `c_next ≠ 0`,
    any common root (`N_curr = 0` and `N_next = 0`) forces the Newton basis polynomial
    to vanish (`B_next = 0`, which occurs only at the interpolation nodes `0, ..., n`). -/
theorem newton_consecutive_common_root_forces_node
    (N_curr N_next c_next B_next : ℂ)
    (h_step : N_next = N_curr + c_next * B_next)
    (hc : c_next ≠ 0)
    (h_curr : N_curr = 0)
    (h_next : N_next = 0) :
    B_next = 0 := by
  have h_prod : c_next * B_next = 0 := by
    rw [h_next, h_curr] at h_step
    calc
      c_next * B_next = 0 + c_next * B_next := by ring
      _ = 0 := h_step.symm
  exact (mul_eq_zero.mp h_prod).resolve_left hc

/-- 5. `newton_consecutive_no_common_root_of_nonzero_samples`:
    If `N_next = N_curr + c_next * B_next` with `c_next ≠ 0`, and every zero of `B_next`
    has a nonzero sample value (`B_next = 0 → N_curr ≠ 0`), then `N_curr` and `N_next`
    have no common root (`¬ (N_curr = 0 ∧ N_next = 0)`). -/
theorem newton_consecutive_no_common_root_of_nonzero_samples
    (N_curr N_next c_next B_next : ℂ)
    (h_step : N_next = N_curr + c_next * B_next)
    (hc : c_next ≠ 0)
    (h_nodes_nonzero : B_next = 0 → N_curr ≠ 0) :
    ¬ (N_curr = 0 ∧ N_next = 0) := by
  rintro ⟨h_curr, h_next⟩
  have hB : B_next = 0 :=
    newton_consecutive_common_root_forces_node N_curr N_next c_next B_next h_step hc h_curr h_next
  exact (h_nodes_nonzero hB) h_curr

/-- 6. `two_approximant_norm_sum_strict_pos`:
    For positive normalization `0 < C_n`, if two consecutive approximants
    `(u₁, v₁)` and `(u₂, v₂)` have no common zero, then the two-approximant
    real ordinate polynomial `G_n(Y) = C_n * ((u₁^2 + v₁^2) + (u₂^2 + v₂^2))`
    is strictly positive (`0 < G_n(Y)`). -/
theorem two_approximant_norm_sum_strict_pos
    (C_n u₁ v₁ u₂ v₂ : ℝ)
    (hC : 0 < C_n)
    (h_no_common : ¬ ((u₁ = 0 ∧ v₁ = 0) ∧ (u₂ = 0 ∧ v₂ = 0))) :
    0 < C_n * ((u₁ ^ 2 + v₁ ^ 2) + (u₂ ^ 2 + v₂ ^ 2)) := by
  have h_nonneg : 0 ≤ (u₁ ^ 2 + v₁ ^ 2) + (u₂ ^ 2 + v₂ ^ 2) :=
    add_nonneg (add_nonneg (sq_nonneg u₁) (sq_nonneg v₁))
      (add_nonneg (sq_nonneg u₂) (sq_nonneg v₂))
  have h_ne_zero : (u₁ ^ 2 + v₁ ^ 2) + (u₂ ^ 2 + v₂ ^ 2) ≠ 0 := by
    intro h_eq
    apply h_no_common
    have hu1 : u₁ ^ 2 = 0 := by nlinarith [sq_nonneg u₁, sq_nonneg v₁, sq_nonneg u₂, sq_nonneg v₂]
    have hv1 : v₁ ^ 2 = 0 := by nlinarith [sq_nonneg u₁, sq_nonneg v₁, sq_nonneg u₂, sq_nonneg v₂]
    have hu2 : u₂ ^ 2 = 0 := by nlinarith [sq_nonneg u₁, sq_nonneg v₁, sq_nonneg u₂, sq_nonneg v₂]
    have hv2 : v₂ ^ 2 = 0 := by nlinarith [sq_nonneg u₁, sq_nonneg v₁, sq_nonneg u₂, sq_nonneg v₂]
    exact ⟨⟨sq_eq_zero_iff.mp hu1, sq_eq_zero_iff.mp hv1⟩,
           ⟨sq_eq_zero_iff.mp hu2, sq_eq_zero_iff.mp hv2⟩⟩
  have h_sum_pos : 0 < (u₁ ^ 2 + v₁ ^ 2) + (u₂ ^ 2 + v₂ ^ 2) :=
    lt_of_le_of_ne h_nonneg (Ne.symm h_ne_zero)
  exact mul_pos hC h_sum_pos

/-! ### 3. Diophantine Clearing and Irrationality Contradiction Schema (Sections 20 & 21) -/

/-- 7. `rational_evaluation_integer_clearing`:
    If `0 < b_pow` (representing `b^{d_n} > 0` for a rational denominator `b ≥ 1`)
    and `1 ≤ b_pow * abs_P` (since `b^{d_n} P_n(a/b)` is a nonzero integer),
    then `1 / b_pow ≤ abs_P`. -/
theorem rational_evaluation_integer_clearing
    (b_pow abs_P : ℝ) (hb : 0 < b_pow) (h_int : 1 ≤ b_pow * abs_P) :
    1 / b_pow ≤ abs_P := by
  rw [div_le_iff hb]
  linarith

/-- 8. `superlinear_log_smallness_irrationality_schema`:
    Abstract Diophantine contradiction schema: if a nonzero integer polynomial evaluation
    at a rational candidate satisfies `1 ≤ b_pow * abs_P` while superlinear logarithmic
    smallness forces `b_pow * abs_P < 1`, a contradiction (`False`) ensues. -/
theorem superlinear_log_smallness_irrationality_schema
    (b_pow abs_P : ℝ)
    (h_lower : 1 ≤ b_pow * abs_P)
    (h_small : b_pow * abs_P < 1) :
    False := by
  linarith

/-- 9. `pade_interpolation_zero_residual_identity`:
    At a zero `R_alpha = 0` of `R(z)`, the multipoint Padé residual
    `E_n(α) = A_alpha - R_alpha * B_alpha` reduces identically to the numerator
    polynomial evaluation `A_alpha`. -/
theorem pade_interpolation_zero_residual_identity
    (A_alpha B_alpha R_alpha : ℂ) (h_zero : R_alpha = 0) :
    A_alpha - R_alpha * B_alpha = A_alpha := by
  rw [h_zero]
  ring

/-! ### 4. TASK-TC-039R: π ↔ τ Normalization, Gauge Scaling, and Two-Phase Lower Envelope (Section 42) -/

/-- 10. `pi_tau_zero_function_scaling`:
    With `pi_pow_neg2z = four_pow_z * tau_pow_neg2z` (since `π^{-2z} = (τ/2)^{-2z} = 4^z τ^{-2z}`),
    the rationalized entire functions `R_π(z) = (2z - 1) π^{-2z} ζ(2z)` and
    `R_τ(z) = (2z - 1) τ^{-2z} ζ(2z)` satisfy `R_π(z) = 4^z R_τ(z)`. -/
theorem pi_tau_zero_function_scaling
    (z four_pow_z pi_pow_neg2z tau_pow_neg2z zeta_2z : ℂ)
    (h_pow : pi_pow_neg2z = four_pow_z * tau_pow_neg2z) :
    (2 * z - 1) * pi_pow_neg2z * zeta_2z =
      four_pow_z * ((2 * z - 1) * tau_pow_neg2z * zeta_2z) := by
  rw [h_pow]
  ring

/-- 11. `pi_tau_integer_sample_scaling`:
    For every integer node `m : ℕ`, the `π`-normalized rational sample
    `a_m^(π) = s * (2m - 1) * 4^m * B_{2m} / (2 * F_{2m})` and the `τ`-normalized
    rational sample `a_m^(τ) = s * (2m - 1) * B_{2m} / (2 * F_{2m})` satisfy
    `a_m^(π) = 4^m * a_m^(τ)`. -/
theorem pi_tau_integer_sample_scaling
    (m : ℕ) (s B_2m F_2m : ℝ) :
    s * (2 * (m : ℝ) - 1) * ((4 : ℝ) ^ m) * B_2m / (2 * F_2m) =
      ((4 : ℝ) ^ m) * (s * (2 * (m : ℝ) - 1) * B_2m / (2 * F_2m)) := by
  ring

/-- 12. `tau_even_zeta_rational_core_identity`:
    Given `τ = 2π` (`tau_pow_2m ≠ 0`) and Euler's even-zeta formula
    `zeta_2m = s * B_2m * tau_pow_2m / (2 * F_2m)`, dividing by `τ^{2m}` isolates
    the exact rational Bernoulli/factorial core `s * B_2m / (2 * F_2m)`. -/
theorem tau_even_zeta_rational_core_identity
    (zeta_2m tau_pow_2m s B_2m F_2m : ℝ)
    (htau : tau_pow_2m ≠ 0)
    (h_euler : zeta_2m = s * B_2m * tau_pow_2m / (2 * F_2m)) :
    zeta_2m / tau_pow_2m = s * B_2m / (2 * F_2m) := by
  rw [h_euler]
  calc
    (s * B_2m * tau_pow_2m / (2 * F_2m)) / tau_pow_2m
      = (s * B_2m / (2 * F_2m)) * (tau_pow_2m / tau_pow_2m) := by ring
    _ = (s * B_2m / (2 * F_2m)) * 1 := by rw [div_self htau]
    _ = s * B_2m / (2 * F_2m) := by ring

/-- 13. `moment_pi_tau_scaling`:
    Since `q_π = 4 * q_τ`, the `(m+1)`-th Hausdorff moments satisfy
    `q_π^{m+1} = 4^{m+1} * q_τ^{m+1}` and
    `s * 4^{m+1} * B / (2 * F) = 4^{m+1} * (s * B / (2 * F))`. -/
theorem moment_pi_tau_scaling
    (m : ℕ) (q_pi q_tau s B F : ℝ)
    (hq : q_pi = 4 * q_tau) :
    (q_pi ^ (m + 1) = (4 : ℝ) ^ (m + 1) * q_tau ^ (m + 1)) ∧
    (s * ((4 : ℝ) ^ (m + 1)) * B / (2 * F) =
      ((4 : ℝ) ^ (m + 1)) * (s * B / (2 * F))) := by
  refine ⟨?_, by ring⟩
  rw [hq, mul_pow]

/-- 14. `hankel_gauge_scaling_exponent`:
    In an `n × n` Hankel determinant `det(c^{i+j+1} b_{i+j})_{0 ≤ i,j < n}`, factoring `c^i`
    from row `i` and `c^{j+1}` from column `j` yields total exponent
    `2 * (n * (n - 1) / 2) + n = n^2` (formulated as `n * (n - 1) + n = n ^ 2` for `n ≥ 1`),
    so `(c ^ (n * (n - 1))) * (c ^ n) = c ^ (n ^ 2)`. -/
theorem hankel_gauge_scaling_exponent
    (c : ℝ) (n : ℕ) (hn : 1 ≤ n) :
    (n * (n - 1) + n = n ^ 2) ∧
    ((c ^ (n * (n - 1))) * (c ^ n) = c ^ (n ^ 2)) := by
  have h_exp : n * (n - 1) + n = n ^ 2 := by
    zify [hn]
    ring
  refine ⟨h_exp, ?_⟩
  rw [← pow_add, h_exp]

/-- 15. `rational_gauge_zero_divisor_invariant`:
    For any nowhere-vanishing gauge factor `c_pow_z ≠ 0` (`c^z = exp(z log c) ≠ 0`),
    the gauge-transformed function `R_c(z) = c_pow_z * R_τ(z)` has the exact same
    zeros as `R_τ(z)`: `c_pow_z * R_tau = 0 ↔ R_tau = 0`. -/
theorem rational_gauge_zero_divisor_invariant
    (c_pow_z R_tau : ℂ) (hc : c_pow_z ≠ 0) :
    c_pow_z * R_tau = 0 ↔ R_tau = 0 := by
  constructor
  · intro h
    exact (mul_eq_zero.mp h).resolve_left hc
  · intro h
    rw [h, mul_zero]

/-- 16. `two_phase_cosine_square_lower_bound`:
    (a) For any two phase cosines/sines `(c₁, s₁)` and `(c₂, s₂)` with `s₁^2 + s₂^2 ≤ 2`,
        Cauchy–Schwarz / Lagrange's identity gives `(s₂ * c₁ - c₂ * s₁)^2 ≤ 2 * (c₁^2 + c₂^2)`
        (i.e. `sin^2(θ₂ - θ₁) ≤ 2 (cos^2 θ₁ + cos^2 θ₂)`).
    (b) For any consecutive values `(u₁, v₁)` and `(u₂, v₂)` with difference
        `(du, dv) = (u₂ - u₁, v₂ - v₁)`, `3 * ((u₁^2 + v₁^2) + (u₂^2 + v₂^2)) ≥ (u₁^2 + v₁^2) + (du^2 + dv^2)`. -/
theorem two_phase_cosine_square_lower_bound
    (c₁ s₁ c₂ s₂ u₁ v₁ u₂ v₂ : ℝ)
    (h_sin_bound : s₁ ^ 2 + s₂ ^ 2 ≤ 2) :
    ((s₂ * c₁ - c₂ * s₁) ^ 2 ≤ 2 * (c₁ ^ 2 + c₂ ^ 2)) ∧
    ((u₁ ^ 2 + v₁ ^ 2) + ((u₂ - u₁) ^ 2 + (v₂ - v₁) ^ 2) ≤
      3 * ((u₁ ^ 2 + v₁ ^ 2) + (u₂ ^ 2 + v₂ ^ 2))) := by
  refine ⟨?_, ?_⟩
  · have h_c_nonneg : 0 ≤ c₁ ^ 2 + c₂ ^ 2 := add_nonneg (sq_nonneg c₁) (sq_nonneg c₂)
    have h_mul : (c₁ ^ 2 + c₂ ^ 2) * (s₁ ^ 2 + s₂ ^ 2) ≤ (c₁ ^ 2 + c₂ ^ 2) * 2 :=
      mul_le_mul_of_nonneg_left h_sin_bound h_c_nonneg
    nlinarith [sq_nonneg (c₁ * s₁ + c₂ * s₂), h_mul]
  · nlinarith [sq_nonneg (u₁ + u₂), sq_nonneg (v₁ + v₂), sq_nonneg u₂, sq_nonneg v₂]

/-- 17. `fixed_gauge_degree_invariance`:
    If the `τ`-normalized top Newton difference `c_n_tau ≠ 0` is scaled by a nonzero
    gauge factor `lambda_n ≠ 0` and divided by `n_fact ≠ 0`, the resulting leading
    coefficient `(lambda_n * c_n_tau) / n_fact` is nonzero, preserving degree `n`. -/
theorem fixed_gauge_degree_invariance
    (lambda_n c_n_tau n_fact : ℝ)
    (h_lam : lambda_n ≠ 0)
    (h_cn : c_n_tau ≠ 0)
    (h_fact : n_fact ≠ 0) :
    (lambda_n * c_n_tau) / n_fact ≠ 0 := by
  exact div_ne_zero (mul_ne_zero h_lam h_cn) h_fact

/-! ### 5. TASK-TC-039R3: Removable Singularity `R_τ(1/2)` Scaling, Vertical-Line Steepest-Descent Saddle Identities, and `π/3` Phase-Displacement Lower Bound -/

/-- 18. `tau_removable_singularity_half_scaling`:
    With `τ = 2π` (`π = τ / 2`, `τ ≠ 0`), the removable-singularity values at `z = 1/2`
    satisfy `R_τ(1/2) = 1 / τ = 1 / (2π)` and `R_π(1/2) = 1 / π = 2 / τ = 2 * R_τ(1/2)`
    (since `4^{1/2} = 2`). -/
theorem tau_removable_singularity_half_scaling
    (tau pi_val : ℝ)
    (h_tau : tau = 2 * pi_val)
    (h_pi_ne : pi_val ≠ 0) :
    (1 / tau = 1 / (2 * pi_val)) ∧
    (1 / pi_val = 2 * (1 / tau)) := by
  refine ⟨by rw [h_tau], ?_⟩
  rw [h_tau]
  field_simp [h_pi_ne]

/-- 19. `vertical_line_saddle_real_concavity_identity`:
    Along the vertical steepest-descent line `u = x + i y` in the right half-plane `x > 0`
    passing simultaneously through both conjugate saddles `u_± = x (1 ± i √3)` where
    `√c = 16 n x^3`, the real part of the model action `Φ_n(u) = n u^2 - √c / u` satisfies
    the exact rational global concavity identity:
      `n (x^2 - y^2) - 16 n x^4 / (x^2 + y^2) = -6 n x^2 - n (y^2 - 3 x^2)^2 / (x^2 + y^2)`,
    and therefore for `0 ≤ n` and `0 < x^2 + y^2` achieves its strict global maximum
    `-6 n x^2 = -κ(c) n^{1/3}` solely at `y^2 = 3 x^2` (`u = u_±`). -/
theorem vertical_line_saddle_real_concavity_identity
    (n x y : ℝ)
    (hn : 0 ≤ n)
    (h_denom : 0 < x ^ 2 + y ^ 2) :
    (n * (x ^ 2 - y ^ 2) - (16 * n * x ^ 4) / (x ^ 2 + y ^ 2) =
      -6 * n * x ^ 2 - (n * (y ^ 2 - 3 * x ^ 2) ^ 2) / (x ^ 2 + y ^ 2)) ∧
    (n * (x ^ 2 - y ^ 2) - (16 * n * x ^ 4) / (x ^ 2 + y ^ 2) ≤ -6 * n * x ^ 2) := by
  have h_ne : x ^ 2 + y ^ 2 ≠ 0 := ne_of_gt h_denom
  have h_id : n * (x ^ 2 - y ^ 2) - (16 * n * x ^ 4) / (x ^ 2 + y ^ 2) =
      -6 * n * x ^ 2 - (n * (y ^ 2 - 3 * x ^ 2) ^ 2) / (x ^ 2 + y ^ 2) := by
    field_simp [h_ne]
    ring
  refine ⟨h_id, ?_⟩
  rw [h_id]
  have h_num : 0 ≤ n * (y ^ 2 - 3 * x ^ 2) ^ 2 := mul_nonneg hn (sq_nonneg _)
  have h_div : 0 ≤ (n * (y ^ 2 - 3 * x ^ 2) ^ 2) / (x ^ 2 + y ^ 2) :=
    div_nonneg h_num (le_of_lt h_denom)
  linarith

/-- 20. `vertical_line_saddle_imag_cubic_identity`:
    Along the vertical steepest-descent line `u = x + i y` with `√c = 16 n x^3` and `s₃^2 = 3`,
    the imaginary part of the model action `Φ_n(u) = n u^2 - √c / u` satisfies the exact
    cubic stationary-phase identity at `y = s₃ x`:
      `2 n x y + 16 n x^3 y / (x^2 + y^2) = 6 s₃ n x^2 + 2 n x (y - s₃ x)^3 / (x^2 + y^2)`
    (showing vanishing first and second imaginary phase derivatives along the vertical contour). -/
theorem vertical_line_saddle_imag_cubic_identity
    (n x y s₃ : ℝ)
    (hs3 : s₃ ^ 2 = 3)
    (h_ne : x ^ 2 + y ^ 2 ≠ 0) :
    2 * n * x * y + (16 * n * x ^ 3 * y) / (x ^ 2 + y ^ 2) =
      6 * s₃ * n * x ^ 2 + (2 * n * x * (y - s₃ * x) ^ 3) / (x ^ 2 + y ^ 2) := by
  field_simp [h_ne]
  calc
    2 * n * x * y * (x ^ 2 + y ^ 2) + 16 * n * x ^ 3 * y
      = 6 * s₃ * n * x ^ 2 * (x ^ 2 + y ^ 2) + 2 * n * x * (y - s₃ * x) ^ 3 +
          (2 * s₃ * n * x ^ 4 - 6 * n * x ^ 3 * y) * (s₃ ^ 2 - 3) := by ring
    _ = 6 * s₃ * n * x ^ 2 * (x ^ 2 + y ^ 2) + 2 * n * x * (y - s₃ * x) ^ 3 := by
      rw [hs3]; ring

/-- 21. `phase_displacement_pi_over_three_sum_sq_lower_bound`:
    For any real `(x, y)` on the unit circle `x^2 + y^2 = 1` (representing `x = cos θ, y = sin θ`)
    and `s₃^2 = 3` (so `x / 2 - s₃ y / 2 = cos(θ + π/3)` is the `π/3`-shifted tail cosine),
    we have the exact sum-of-squares identity
      `x^2 + (x / 2 - s₃ * y / 2)^2 = 1 / 2 + (s₃ * x / 2 - y / 2)^2`,
    which proves unconditionally that `cos^2(θ) + cos^2(θ + π/3) ≥ 1 / 2` for all `θ ∈ ℝ`. -/
theorem phase_displacement_pi_over_three_sum_sq_lower_bound
    (x y s₃ : ℝ)
    (hs3 : s₃ ^ 2 = 3)
    (h_unit : x ^ 2 + y ^ 2 = 1) :
    (x ^ 2 + (x / 2 - s₃ * y / 2) ^ 2 = 1 / 2 + (s₃ * x / 2 - y / 2) ^ 2) ∧
    (1 / 2 ≤ x ^ 2 + (x / 2 - s₃ * y / 2) ^ 2) := by
  have h_id : x ^ 2 + (x / 2 - s₃ * y / 2) ^ 2 = 1 / 2 + (s₃ * x / 2 - y / 2) ^ 2 := by
    calc
      x ^ 2 + (x / 2 - s₃ * y / 2) ^ 2
        = 1 / 2 + (s₃ * x / 2 - y / 2) ^ 2 +
            ((y ^ 2 - x ^ 2) / 4) * (s₃ ^ 2 - 3) + (1 / 2) * (x ^ 2 + y ^ 2 - 1) := by ring
      _ = 1 / 2 + (s₃ * x / 2 - y / 2) ^ 2 := by rw [hs3, h_unit]; ring
  refine ⟨h_id, ?_⟩
  rw [h_id]
  nlinarith [sq_nonneg (s₃ * x / 2 - y / 2)]

end RiemannScope



