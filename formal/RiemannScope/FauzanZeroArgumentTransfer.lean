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

end RiemannScope
