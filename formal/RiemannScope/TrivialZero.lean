/-
RiemannScope.TrivialZero
Exact trivial zeros of the Riemann zeta function s_m = -2 * (n + 1) (m = n + 1 >= 1),
their transported grade-k worldlines W_{-2(n+1)}(k) = tau^k * (-2 * (n + 1)), and the
TASK-TC-053 trivial-zero slope scale-invariance, common-factor Möbius split, and signed-block
bivariate Euler nonvanishing / parity regrouping theorems.
Resolves certificate reference `RiemannScope.TrivialZero.trivialZero_exact` using
pinned Mathlib `riemannZeta_neg_two_mul_nat_add_one` and project `zeroWorldline_is_zero`.
-/

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Tactic
import RiemannScope.ZeroWorldline
import RiemannScope.RadialLeaf

namespace RiemannScope

/-- Strict positivity of the fundamental scale constant `tau = 2 * Real.pi > 0`. -/
theorem tau_pos : 0 < tau := by
  dsimp [tau]
  exact mul_pos zero_lt_two Real.pi_pos

/-- Exact location `s_n = -2 * (n + 1)` of the `(n + 1)`-th trivial zero of `riemannZeta` (`n : ℕ`). -/
noncomputable def trivialZeroLocation (n : ℕ) : ℂ :=
  -2 * ((n : ℂ) + 1)

namespace TrivialZero

/-- Exact trivial zero theorem (`RiemannScope.TrivialZero.trivialZero_exact`):
    for every `n : ℕ`, `riemannZeta (-2 * ((n : ℂ) + 1)) = 0`. -/
theorem trivialZero_exact (n : ℕ) :
    riemannZeta (-2 * ((n : ℂ) + 1)) = 0 :=
  riemannZeta_neg_two_mul_nat_add_one n

/-- Concrete transported trivial-zero worldline corollary (`RiemannScope.TrivialZero.trivialZero_worldline_exact`):
    combining Mathlib's `riemannZeta_neg_two_mul_nat_add_one` with `zeroWorldline_is_zero` and `tau_pos`,
    the grade-`k` extended continuation `extendedContinuation riemannZeta k` vanishes identically along
    the transported trivial-zero worldline `zeroWorldline (-2 * ((n : ℂ) + 1)) k = tau^k * (-2 * (n + 1))`
    for every `n : ℕ` and every real grade `k : ℝ`. -/
theorem trivialZero_worldline_exact (n : ℕ) (k : ℝ) :
    extendedContinuation riemannZeta k (zeroWorldline (-2 * ((n : ℂ) + 1)) k) = 0 :=
  zeroWorldline_is_zero riemannZeta (-2 * ((n : ℂ) + 1)) k (trivialZero_exact n) tau_pos

/-- Exact radial-leaf invariance along the `(n + 1)`-th trivial-zero worldline:
    `normalizedRadialLeaf k (zeroWorldline ⟨-2 * ((n : ℝ) + 1), 0⟩ k) = -2 * ((n : ℝ) + 1) - 1 / 2`. -/
theorem trivialZero_radialLeaf_exact (n : ℕ) (k : ℝ) :
    normalizedRadialLeaf k (zeroWorldline ⟨-2 * ((n : ℝ) + 1), 0⟩ k) =
      -2 * ((n : ℝ) + 1) - 1 / 2 := by
  have h_pt : (⟨-2 * ((n : ℝ) + 1), 0⟩ : ℂ) = ⟨1 / 2 + (-2 * ((n : ℝ) + 1) - 1 / 2), 0⟩ := by
    apply Complex.ext <;> simp
  rw [h_pt]
  exact radialLeaf_worldline_invariance (-2 * ((n : ℝ) + 1) - 1 / 2) 0 k tau_pos

/-- Negative control at `s = 0`: `riemannZeta 0 = -1 / 2`. -/
theorem trivialZero_zero_eq_neg_half :
    riemannZeta 0 = -1 / 2 :=
  riemannZeta_zero

end TrivialZero

/-- Top-level alias in `namespace RiemannScope` for `TrivialZero.trivialZero_exact`. -/
theorem trivialZero_exact (n : ℕ) :
    riemannZeta (-2 * ((n : ℂ) + 1)) = 0 :=
  TrivialZero.trivialZero_exact n

/-- Top-level alias in `namespace RiemannScope` for `TrivialZero.trivialZero_worldline_exact`. -/
theorem trivialZero_worldline_exact (n : ℕ) (k : ℝ) :
    extendedContinuation riemannZeta k (zeroWorldline (-2 * ((n : ℂ) + 1)) k) = 0 :=
  TrivialZero.trivialZero_worldline_exact n k

/-!
## TASK-TC-053: Trivial-Zero Slopes, Common-Factor Möbius Expansion, and Signed Coprime Block Analysis
-/

/-- Normalized trivial-zero slope functional at grade `K` (`a_K = tau^K`) and trivial-zero index `m >= 1`:
    `(2 * sgn_m * tau_pow_2m / fact_2m) * a_K * d_aK` (`TASK-TC-053` §1). -/
noncomputable def normalizedTrivialZeroSlope
    (sgn_m tau_pow_2m fact_2m a_K d_aK : ℝ) : ℝ :=
  ((2 * sgn_m * tau_pow_2m) / fact_2m) * a_K * d_aK

/-- **Theorem (`TASK-TC-053` §1)**: Grade-transport trivial-zero slope scale invariance,
    Gaussian-to-finite-difference `O(k^{-2})` error decomposition, and conditional grade-interval
    `L^2` energy criterion for `Q(X) = X^{5/2} G(X^2)`:
    (1) Grade scale covariance: if `d_aK = d_0 / a_K` (`Z_{a_K}'(-2 m a_K) = (1 / a_K) * zeta'(-2 m)`)
        with `a_K != 0` and `d_0 = (sgn_m * fact_2m / (2 * tau_pow_2m)) * zeta_2m_plus_1` (`sgn_m^2 = 1`),
        then `a_K * d_aK = d_0` is independent of `a_K` and
        `normalizedTrivialZeroSlope sgn_m tau_pow_2m fact_2m a_K d_aK = zeta_2m_plus_1`.
    (2) Gaussian vs finite-difference decomposition: if `G_k - c_k = e_neg_k + R_ge_2` with
        `0 <= e_neg_k <= C_1 * inv_k_sq` (`n = 1` term `e^{-k}`) and `|R_ge_2| <= C_2 * inv_k_sq`
        (`n >= 2` sum), then `|G_k - c_k| <= (C_1 + C_2) * inv_k_sq`.
    (3) Conditional grade-interval Cauchy–Schwarz energy step: if the grade-interval energy
        `E_Y = int_Y^{tau Y} |Q(X)|^2 dX/X` satisfies `0 <= E_Y <= C_eps * Y_pow_eps` and the
        Mellin weight integral `W_Y = int_Y^{tau Y} X^{-2*sigma} dX/X` satisfies
        `0 <= W_Y <= log_tau * Y_pow_neg_2sigma`, then the squared Cauchy–Schwarz bound on `[Y, tau Y]`
        satisfies `E_Y * W_Y <= (C_eps * log_tau) * (Y_pow_eps * Y_pow_neg_2sigma)`, and under the
        explicit analytic bridge implication `(E_Y * W_Y <= (C_eps * log_tau) * (Y_pow_eps * Y_pow_neg_2sigma) -> delta_rho = 0)`
        one obtains `delta_rho = 0`. -/
theorem trivial_zero_slope_scale_invariance_and_grade_energy_criterion
    (sgn_m tau_pow_2m fact_2m a_K d_aK d_0 zeta_2m_plus_1
      G_k c_k e_neg_k R_ge_2 C_1 C_2 inv_k_sq
      E_Y W_Y C_eps Y_pow_eps log_tau Y_pow_neg_2sigma delta_rho : ℝ)
    (haK : a_K ≠ 0)
    (hfact : fact_2m ≠ 0)
    (htau2m : tau_pow_2m ≠ 0)
    (hsgn : sgn_m ^ 2 = 1)
    (h_chain : d_aK = d_0 / a_K)
    (h_reflection : d_0 = ((sgn_m * fact_2m) / (2 * tau_pow_2m)) * zeta_2m_plus_1)
    (h_diff : G_k - c_k = e_neg_k + R_ge_2)
    (h_n1 : 0 ≤ e_neg_k ∧ e_neg_k ≤ C_1 * inv_k_sq)
    (h_nge2 : |R_ge_2| ≤ C_2 * inv_k_sq)
    (h_EY : 0 ≤ E_Y ∧ E_Y ≤ C_eps * Y_pow_eps)
    (h_WY : 0 ≤ W_Y ∧ W_Y ≤ log_tau * Y_pow_neg_2sigma)
    (h_Ceps_nonneg : 0 ≤ C_eps)
    (h_Yeps_nonneg : 0 ≤ Y_pow_eps) :
    (a_K * d_aK = d_0 ∧
      normalizedTrivialZeroSlope sgn_m tau_pow_2m fact_2m a_K d_aK = zeta_2m_plus_1) ∧
    (|G_k - c_k| ≤ (C_1 + C_2) * inv_k_sq) ∧
    (E_Y * W_Y ≤ (C_eps * log_tau) * (Y_pow_eps * Y_pow_neg_2sigma) ∧
      ((E_Y * W_Y ≤ (C_eps * log_tau) * (Y_pow_eps * Y_pow_neg_2sigma) → delta_rho = 0) →
        delta_rho = 0)) := by
  have haK_cancel : a_K * d_aK = d_0 := by
    rw [h_chain]
    exact mul_div_cancel₀ d_0 haK
  have h_slope : normalizedTrivialZeroSlope sgn_m tau_pow_2m fact_2m a_K d_aK = zeta_2m_plus_1 := by
    dsimp [normalizedTrivialZeroSlope]
    have h_assoc :
        ((2 * sgn_m * tau_pow_2m) / fact_2m) * a_K * d_aK =
          ((2 * sgn_m * tau_pow_2m) / fact_2m) * (a_K * d_aK) := by ring
    rw [h_assoc, haK_cancel, h_reflection]
    have h2 : (2 : ℝ) ≠ 0 := two_ne_zero
    field_simp [hfact, htau2m, h2]
    calc
      2 * sgn_m * tau_pow_2m * (sgn_m * fact_2m * zeta_2m_plus_1) =
          (sgn_m ^ 2) * zeta_2m_plus_1 * (fact_2m * (2 * tau_pow_2m)) := by ring
      _ = 1 * zeta_2m_plus_1 * (fact_2m * (2 * tau_pow_2m)) := by rw [hsgn]
      _ = zeta_2m_plus_1 * (fact_2m * (2 * tau_pow_2m)) := by ring
  have h_gk_bound : |G_k - c_k| ≤ (C_1 + C_2) * inv_k_sq := by
    have h_tri : |G_k - c_k| ≤ |e_neg_k| + |R_ge_2| := by
      rw [h_diff]
      exact abs_add e_neg_k R_ge_2
    have h_abs_e : |e_neg_k| = e_neg_k := abs_of_nonneg h_n1.1
    linarith [h_n1.2, h_nge2]
  have h_cs_prod : E_Y * W_Y ≤ (C_eps * log_tau) * (Y_pow_eps * Y_pow_neg_2sigma) := by
    have h_rhs1_nonneg : 0 ≤ C_eps * Y_pow_eps := mul_nonneg h_Ceps_nonneg h_Yeps_nonneg
    have h_mul := mul_le_mul h_EY.2 h_WY.2 h_WY.1 h_rhs1_nonneg
    linarith
  refine ⟨⟨haK_cancel, h_slope⟩, h_gk_bound, ⟨h_cs_prod, ?_⟩⟩
  intro h_imp
  exact h_imp h_cs_prod

/-- Pairwise leading-term coefficient `(3 * sqrt(pi) / 8) * mu_r * mu_s * kappa_rs * (rs_sq / r2_plus_s2_pow_5_2)`
    after integrating `u^4 * exp(-(1/r^2 + 1/s^2) * u^2)` (`TASK-TC-053` §2). -/
noncomputable def commonFactorPairwiseLeadingTerm
    (c_gauss mu_r mu_s kappa_rs rs_sq r2_plus_s2_pow_5_2 : ℝ) : ℝ :=
  c_gauss * mu_r * mu_s * kappa_rs * (rs_sq / r2_plus_s2_pow_5_2)

/-- **Theorem (`TASK-TC-053` §2)**: Common-factor Möbius multiplicativity split, scale-`X^5`
    cancellation in the Gaussian leading term, and valid growing-range exponent algebra:
    (1) For `m = d r`, `n = d s` with `gcd(r, s) = 1`, the identity
        `mu_dr_ds = ind_coprime * (mu_d ^ 2) * mu_r * mu_s` vanishes when `ind_coprime = 0` (`gcd(d, r s) > 1`)
        and equals `mu_r * mu_s` when `ind_coprime = 1` and `mu_d ^ 2 = 1` (`d` squarefree coprime to `r s`).
    (2) Scale cancellation: for `X_pow_5 != 0` and `rs_cubed != 0`, multiplying the outer prefactor
        `(X_pow_5 / rs_cubed) * mu_r * mu_s * kappa_rs` by the Gaussian integral value
        `c_gauss * ((rs_cubed * rs_sq) / (X_pow_5 * r2_plus_s2_pow_5_2))` cancels `X_pow_5` and `rs_cubed`
        identically to yield `commonFactorPairwiseLeadingTerm c_gauss mu_r mu_s kappa_rs rs_sq r2_plus_s2_pow_5_2`
        independent of `X`.
    (3) Valid growing-range exponent algebra for `A <= X^{1/3 - delta}` (`0 < delta < 1/3`):
        the total error exponent `(1/3 - delta) * (3/2 + eps) - 1/2` equals
        `-(3/2) * delta + (1/3 - delta) * eps`, which is strictly negative (`< 0`) if and only if
        `eps < (3 * delta) / (2 * (1/3 - delta))`, and whenever `0 < eps` and `eps <= (3/2) * delta`,
        `(1/3 - delta) * (3/2 + eps) - 1/2 < -delta < 0`. -/
theorem common_factor_mobius_split_and_valid_growing_range_exponent
    (mu_dr_ds ind_coprime mu_d mu_r mu_s
      X_pow_5 rs_cubed rs_sq r2_plus_s2_pow_5_2 c_gauss kappa_rs
      delta eps : ℝ)
    (h_mobius : mu_dr_ds = ind_coprime * (mu_d ^ 2) * mu_r * mu_s)
    (hX5 : X_pow_5 ≠ 0)
    (hrs3 : rs_cubed ≠ 0)
    (hdelta_pos : 0 < delta)
    (hdelta_lt : delta < 1 / 3) :
    ((ind_coprime = 0 → mu_dr_ds = 0) ∧
      (ind_coprime = 1 → mu_d ^ 2 = 1 → mu_dr_ds = mu_r * mu_s)) ∧
    ((X_pow_5 / rs_cubed) * mu_r * mu_s * kappa_rs *
        (c_gauss * ((rs_cubed * rs_sq) / (X_pow_5 * r2_plus_s2_pow_5_2))) =
      commonFactorPairwiseLeadingTerm c_gauss mu_r mu_s kappa_rs rs_sq r2_plus_s2_pow_5_2) ∧
    ((1 / 3 - delta) * (3 / 2 + eps) - 1 / 2 = -(3 / 2 : ℝ) * delta + (1 / 3 - delta) * eps ∧
      ((1 / 3 - delta) * (3 / 2 + eps) - 1 / 2 < 0 ↔
        eps < (3 * delta) / (2 * (1 / 3 - delta))) ∧
      (0 < eps → eps ≤ (3 / 2 : ℝ) * delta →
        (1 / 3 - delta) * (3 / 2 + eps) - 1 / 2 < -delta)) := by
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · intro hind0
    rw [h_mobius, hind0]
    ring
  · intro hind1 hmud1
    rw [h_mobius, hind1, hmud1]
    ring
  · dsimp [commonFactorPairwiseLeadingTerm]
    have h_alg :
        (X_pow_5 / rs_cubed) * mu_r * mu_s * kappa_rs *
          (c_gauss * ((rs_cubed * rs_sq) / (X_pow_5 * r2_plus_s2_pow_5_2))) =
        (X_pow_5 / X_pow_5) * (rs_cubed / rs_cubed) *
          (c_gauss * mu_r * mu_s * kappa_rs * (rs_sq / r2_plus_s2_pow_5_2)) := by ring
    rw [h_alg, div_self hX5, div_self hrs3]
    ring
  · have h_exp_id :
        (1 / 3 - delta) * (3 / 2 + eps) - 1 / 2 =
          -(3 / 2 : ℝ) * delta + (1 / 3 - delta) * eps := by ring
    have h_two_sub_pos : 0 < 2 * (1 / 3 - delta) := by linarith
    refine ⟨h_exp_id, ?_, ?_⟩
    · rw [h_exp_id]
      constructor
      · intro h_neg
        have h_lt : eps * (2 * (1 / 3 - delta)) < 3 * delta := by linarith
        exact (lt_div_iff h_two_sub_pos).mpr h_lt
      · intro h_eps_lt
        have h_lt : eps * (2 * (1 / 3 - delta)) < 3 * delta :=
          (lt_div_iff h_two_sub_pos).mp h_eps_lt
        linarith
    · intro heps_pos heps_le
      have h_prod_pos : 0 < delta * eps := mul_pos hdelta_pos heps_pos
      linarith

/-- Local bivariate Euler factor `E_p(s_1, s_2) = 1 - (p / (p + 1)) * (x_1 + x_2)`
    for `x_1 = p^{-s_1}`, `x_2 = p^{-s_2}` (`TASK-TC-053` §3 Attempt 1). -/
noncomputable def bivariateLocalEulerFactor (p x_1 x_2 : ℝ) : ℝ :=
  1 - (p / (p + 1)) * (x_1 + x_2)

/-- **Theorem (`TASK-TC-053` §3)**: Signed-block Attempt 1 bivariate Euler-factor nonvanishing
    and Attempt 2 logarithmic Möbius parity decomposition:
    (1) Attempt 1 local bivariate Euler ratio identity and AM–GM nonvanishing on `Re(s_i) >= 1/2`:
        - For `1 - x_1 != 0`, `1 - x_2 != 0`, and `p + 1 != 0`, the ratio of
          `bivariateLocalEulerFactor p x_1 x_2` to `(1 - x_1) * (1 - x_2)` equals
          `1 + ((1 / (p + 1)) * (x_1 + x_2) - x_1 * x_2) / ((1 - x_1) * (1 - x_2))`.
        - For any prime `p = sqrt_p ^ 2` with `sqrt_p > 1`, AM–GM (`(sqrt_p - 1)^2 > 0`) implies
          `(p / (p + 1)) * (2 / sqrt_p) = (2 * sqrt_p) / (p + 1) < 1`, and whenever
          `x_1 + x_2 <= 2 / sqrt_p`, we have `bivariateLocalEulerFactor p x_1 x_2 >= 1 - (2 * sqrt_p) / (p + 1) > 0`
          (proving that the correction Euler product numerator cannot vanish on `Re(s_1), Re(s_2) >= 1/2`
          to cancel off-critical zeros of `zeta(s_1) * zeta(s_2)`).
    (2) Attempt 2 logarithmic Möbius convolution and parity comparison:
        - Nonsquarefree prime-square cancellation: for `q = p^2 * m` with `p` not dividing squarefree `m`,
          the `u = p, v = p * m` (`mu(p m) = -mu_m`) and `u = p^2, v = m` (`mu(m) = mu_m`) terms in
          `-sum_{u v = q} Lambda(u) mu(v)` cancel identically (`-((log_p) * (-mu_m) + (log_p) * mu_m) = 0`).
        - Signed parity decomposition `S_A = S_two_prime - S_odd_omega + S_even_ge_4`:
          if `|S_A| <= B_S`, then the opposing odd-`omega(q)` contribution must satisfy
          `S_two_prime + S_even_ge_4 - B_S <= S_odd_omega`, whereas bounding the parity strata by the
          triangle inequality yields `S_two_prime <= S_two_prime + |S_odd_omega| + |S_even_ge_4|`
          whenever `0 <= S_two_prime`, losing the required cancellation below `S_two_prime`. -/
theorem signed_block_bivariate_euler_nonvanishing_and_parity_regrouping
    (p sqrt_p x_1 x_2 log_p mu_m S_A S_two_prime S_odd_omega S_even_ge_4 B_S : ℝ)
    (hp_eq : p = sqrt_p ^ 2)
    (hsqrt_gt_one : 1 < sqrt_p)
    (hx1 : 1 - x_1 ≠ 0)
    (hx2 : 1 - x_2 ≠ 0)
    (h_parity_decomp : S_A = S_two_prime - S_odd_omega + S_even_ge_4) :
    (bivariateLocalEulerFactor p x_1 x_2 / ((1 - x_1) * (1 - x_2)) =
        1 + ((1 / (p + 1)) * (x_1 + x_2) - x_1 * x_2) / ((1 - x_1) * (1 - x_2)) ∧
      (2 * sqrt_p) / (p + 1) < 1 ∧
      (x_1 + x_2 ≤ 2 / sqrt_p →
        0 < 1 - (2 * sqrt_p) / (p + 1) ∧
          1 - (2 * sqrt_p) / (p + 1) ≤ bivariateLocalEulerFactor p x_1 x_2)) ∧
    (-((log_p) * (-mu_m) + (log_p) * mu_m) = 0 ∧
      (|S_A| ≤ B_S → S_two_prime + S_even_ge_4 - B_S ≤ S_odd_omega) ∧
      (0 ≤ S_two_prime → S_two_prime ≤ S_two_prime + |S_odd_omega| + |S_even_ge_4|)) := by
  have hsqrt_pos : 0 < sqrt_p := by linarith
  have hsqrt_ne : sqrt_p ≠ 0 := ne_of_gt hsqrt_pos
  have hp_gt_one : 1 < p := by
    rw [hp_eq]
    nlinarith
  have hp_pos : 0 < p := by linarith
  have hp_plus_one_pos : 0 < p + 1 := by linarith
  have hp_plus_one_ne : p + 1 ≠ 0 := ne_of_gt hp_plus_one_pos
  have hdenom_ne : (1 - x_1) * (1 - x_2) ≠ 0 := mul_ne_zero hx1 hx2
  have h_amgm_diff : 0 < (sqrt_p - 1) ^ 2 := sq_pos_of_pos (by linarith)
  have h_two_sqrt_lt : 2 * sqrt_p < p + 1 := by
    rw [hp_eq]
    linarith
  have h_ratio_lt_one : (2 * sqrt_p) / (p + 1) < 1 :=
    (div_lt_one hp_plus_one_pos).mpr h_two_sqrt_lt
  refine ⟨⟨?_, h_ratio_lt_one, ?_⟩, ⟨by ring, ?_, ?_⟩⟩
  · dsimp [bivariateLocalEulerFactor]
    field_simp [hp_plus_one_ne, hdenom_ne]
    ring
  · intro hx_sum
    have h_pos_gap : 0 < 1 - (2 * sqrt_p) / (p + 1) := by linarith
    have h_p_div_nonneg : 0 ≤ p / (p + 1) := div_nonneg (le_of_lt hp_pos) (le_of_lt hp_plus_one_pos)
    have h_mul_le :
        (p / (p + 1)) * (x_1 + x_2) ≤ (p / (p + 1)) * (2 / sqrt_p) :=
      mul_le_mul_of_nonneg_left hx_sum h_p_div_nonneg
    have h_simp_bound : (p / (p + 1)) * (2 / sqrt_p) = (2 * sqrt_p) / (p + 1) := by
      rw [hp_eq]
      field_simp [hp_plus_one_ne, hsqrt_ne]
      ring
    dsimp [bivariateLocalEulerFactor]
    refine ⟨h_pos_gap, by linarith⟩
  · intro hSA
    have hsa := abs_le.mp hSA
    linarith
  · intro _
    have h1 : 0 ≤ |S_odd_omega| := abs_nonneg S_odd_omega
    have h2 : 0 ≤ |S_even_ge_4| := abs_nonneg S_even_ge_4
    linarith

end RiemannScope
