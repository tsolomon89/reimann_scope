/-
RiemannScope.LiouvilleSquareDilation
TASK-TC-054: Liouville square-dilation transfer (lambda(n) = sum_{d^2 | n} mu(n/d^2) and
mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2)), complete multiplicativity common-factor sign
cancellation lambda(d r) lambda(d s) = lambda(r) lambda(s) on Nat, Euler-Maclaurin subtransition
exponent algebra 1 - (N + 1) * delta < 0 <-> (N + 1) * delta > 1, C_2 = (f'(v_-) - f'(v_+)) / 6,
and dyadic parity energy / off-critical mode nonvanishing.
-/

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Tactic
import RiemannScope.Basic

namespace RiemannScope

namespace LiouvilleSquareDilation

/-- Prime-power Möbius value `mu(p^e)` on exponent `e : ℕ`:
    `mu(p^0) = 1`, `mu(p^1) = -1`, and `mu(p^{e+2}) = 0`. -/
def primePowerMoebius : ℕ → ℤ
  | 0 => 1
  | 1 => (-1 : ℤ)
  | _ + 2 => 0

/-- Liouville sign `lambda(n) = (-1)^{Omega(n)}` as a function of the prime-factor multiplicity
    count `omega_n = Omega(n) : ℕ` (`omega_1 = 0`, `omega_p = 1`, `omega_{m n} = omega_m + omega_n`). -/
def liouvilleSignFromOmega (omega_n : ℕ) : ℤ :=
  (-1 : ℤ) ^ omega_n

/-- Finite range sum `sum_{0 <= j < m} f(j)` over `ℕ`. -/
def finRangeSum (f : ℕ → ℤ) : ℕ → ℤ
  | 0 => 0
  | m + 1 => finRangeSum f m + f m

/-- Recursive square-divisor Möbius sum `sum_{d^2 | p^k} mu(p^k / d^2)` on prime-power exponent `k : ℕ`:
    strips squares `p^{2j}` (`0 <= 2j <= k`) to sum `mu(p^k) + mu(p^{k-2}) + ...`. -/
def squareDivisorMoebiusSum : ℕ → ℤ
  | 0 => primePowerMoebius 0
  | 1 => primePowerMoebius 1
  | k + 2 => primePowerMoebius (k + 2) + squareDivisorMoebiusSum k

/-- Indexed finite-sum representation `sum_{0 <= j <= k/2} mu(d_j) * lambda(p^k / d_j^2)`
    for the inverse square-divisor convolution `sum_{d^2 | p^k} mu(d) * lambda(p^k / d^2)` on `k : ℕ`. -/
def squareDivisorInverseLiouvilleSum (k : ℕ) : ℤ :=
  finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) (k / 2 + 1)

/-- **Theorem 1 (`TASK-TC-054` §2–§4)**: Complete multiplicativity and common-factor sign
    cancellation for `liouvilleSignFromOmega` on `ℕ`:
    (1) `liouvilleSignFromOmega 0 = 1` (`lambda(1) = 1`) and `liouvilleSignFromOmega 1 = -1` (`lambda(p) = -1`);
    (2) Complete multiplicativity: for all `omega_m, omega_n : ℕ`,
        `liouvilleSignFromOmega (omega_m + omega_n) = liouvilleSignFromOmega omega_m * liouvilleSignFromOmega omega_n`;
    (3) Unit square law: for every `omega_d : ℕ`,
        `liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1`;
    (4) Unconstrained common-factor sign cancellation: for all `omega_d, omega_r, omega_s : ℕ`
        (`m = d * r`, `n = d * s` with `Omega(d * r) = omega_d + omega_r` and `Omega(d * s) = omega_d + omega_s`),
        `liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) =
         liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s`,
        with no squarefree or coprimality restriction on `d`. -/
theorem liouville_complete_multiplicativity_and_common_factor_cancellation_nat
    (omega_d omega_r omega_s : ℕ) :
    (liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1) ∧
    liouvilleSignFromOmega (omega_d + omega_r) =
      liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r ∧
    liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 ∧
    liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) =
      liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by
  have h_base : liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1 := by decide
  have h_mul_dr :
      liouvilleSignFromOmega (omega_d + omega_r) =
        liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r := by
    dsimp [liouvilleSignFromOmega]
    exact pow_add (-1 : ℤ) omega_d omega_r
  have h_mul_ds :
      liouvilleSignFromOmega (omega_d + omega_s) =
        liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_s := by
    dsimp [liouvilleSignFromOmega]
    exact pow_add (-1 : ℤ) omega_d omega_s
  have h_sq : liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 := by
    dsimp [liouvilleSignFromOmega]
    rw [← pow_add]
    have h_even : omega_d + omega_d = 2 * omega_d := by omega
    rw [h_even, pow_mul]
    norm_num
  have h_cancel :
      liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) =
        liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by
    rw [h_mul_dr, h_mul_ds]
    calc
      (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r) *
          (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_s) =
        (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d) *
          (liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s) := by ring
      _ = 1 * (liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s) := by rw [h_sq]
      _ = liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by ring
  exact ⟨h_base, h_mul_dr, h_sq, h_cancel⟩

/-- Helper lemma: for any `k >= 2` and any tail length `r : ℕ`, adding `r` terms with index `j + 2`
    to `finRangeSum` contributes `0` because `primePowerMoebius (j + 2) = 0`. -/
private theorem finRangeSum_primePowerMoebius_tail_eq_two
    (k : ℕ) :
    ∀ r : ℕ,
      finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) (r + 2) =
        finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) 2 := by
  intro r
  induction r with
  | zero => rfl
  | succ r ih =>
    have h_step : r + 1 + 2 = (r + 2) + 1 := by omega
    rw [h_step]
    dsimp [finRangeSum]
    have h_pm : primePowerMoebius (r + 2) = 0 := rfl
    rw [h_pm, zero_mul, add_zero]
    exact ih

/-- **Theorem 2 (`TASK-TC-054` §3)**: Exact prime-power square-divisor Möbius–Liouville
    inversion on `ℕ`:
    For every prime-power exponent `k : ℕ`:
    (1) `squareDivisorMoebiusSum k = liouvilleSignFromOmega k`
        (`sum_{d^2 | p^k} mu(p^k / d^2) = (-1)^k = lambda(p^k)`);
    (2) `squareDivisorInverseLiouvilleSum k = primePowerMoebius k`
        (`sum_{d^2 | p^k} mu(d) * lambda(p^k / d^2) = mu(p^k)`). -/
theorem prime_power_square_divisor_moebius_liouville_inversion_nat :
    ∀ k : ℕ,
      squareDivisorMoebiusSum k = liouvilleSignFromOmega k ∧
      squareDivisorInverseLiouvilleSum k = primePowerMoebius k := by
  intro k
  constructor
  · induction' k using Nat.strong_induction_on with k ih
    rcases k with _ | _ | k'
    · decide
    · decide
    · have h_step : k' + 1 + 1 = k' + 2 := rfl
      rw [h_step]
      dsimp [squareDivisorMoebiusSum]
      have h_ih : squareDivisorMoebiusSum k' = liouvilleSignFromOmega k' :=
        ih k' (by omega)
      have h_pm : primePowerMoebius (k' + 2) = 0 := rfl
      rw [h_pm, zero_add, h_ih]
      dsimp [liouvilleSignFromOmega]
      rw [pow_add]
      norm_num
  · rcases k with _ | _ | k'
    · decide
    · decide
    · have h_step : k' + 1 + 1 = k' + 2 := rfl
      rw [h_step]
      dsimp [squareDivisorInverseLiouvilleSum]
      obtain ⟨r, hr⟩ : ∃ r, (k' + 2) / 2 + 1 = r + 2 := ⟨(k' + 2) / 2 - 1, by omega⟩
      rw [hr, finRangeSum_primePowerMoebius_tail_eq_two (k' + 2)]
      dsimp [finRangeSum, primePowerMoebius]
      have h_sub1 : k' + 2 - 2 = k' := by omega
      rw [h_sub1, pow_add]
      norm_num

/-- **Theorem 3 (`TASK-TC-054` §3)**: Reversible weighted `L^2` norm equivalence and
    grade-interval subpower energy bridge:
    (1) Dilation norm scaling: if `norm_f_a_sq = a_pow_neg_2sigma * norm_f_sq`, then for `a = d^2`
        (`a_pow_neg_2sigma = d_pow_neg_4sigma`), `norm_f_d2_sq = d_pow_neg_4sigma * norm_f_sq`;
    (2) Reversible weighted norm bounds (`sigma > 0`): if `0 <= norm_lambda <= zeta_1_2sigma * norm_mu`
        and `0 <= norm_mu <= (zeta_1_2sigma / zeta_2_4sigma) * norm_lambda` with
        `0 < zeta_1_2sigma` and `0 < zeta_2_4sigma`, then `norm_mu <= B_mu` implies
        `norm_lambda <= zeta_1_2sigma * B_mu`, and `norm_lambda <= B_lam` implies
        `norm_mu <= (zeta_1_2sigma / zeta_2_4sigma) * B_lam`;
    (3) Grade-interval energy to weighted norm bound: if `int_0_1 <= Z3_sq / (5 - 2 * sigma)` and
        `sum_tau_blocks <= C_sigma / (1 - tau_pow_neg_sigma)`, then
        `int_0_1 + sum_tau_blocks <= Z3_sq / (5 - 2 * sigma) + C_sigma / (1 - tau_pow_neg_sigma)`. -/
theorem reversible_weighted_dilation_norm_and_grade_interval_equivalence
    (norm_f_sq d_pow_neg_4sigma norm_f_d2_sq
      norm_lambda norm_mu zeta_1_2sigma zeta_2_4sigma B_mu B_lam
      int_0_1 sum_tau_blocks Z3_sq sigma C_sigma tau_pow_neg_sigma : ℝ)
    (h_dil : norm_f_d2_sq = d_pow_neg_4sigma * norm_f_sq)
    (h_z1_pos : 0 < zeta_1_2sigma)
    (h_z2_pos : 0 < zeta_2_4sigma)
    (h_fwd : norm_lambda ≤ zeta_1_2sigma * norm_mu)
    (h_rev : norm_mu ≤ (zeta_1_2sigma / zeta_2_4sigma) * norm_lambda)
    (h_01 : int_0_1 ≤ Z3_sq / (5 - 2 * sigma))
    (h_blocks : sum_tau_blocks ≤ C_sigma / (1 - tau_pow_neg_sigma)) :
    norm_f_d2_sq = d_pow_neg_4sigma * norm_f_sq ∧
    (norm_mu ≤ B_mu → norm_lambda ≤ zeta_1_2sigma * B_mu) ∧
    (norm_lambda ≤ B_lam → norm_mu ≤ (zeta_1_2sigma / zeta_2_4sigma) * B_lam) ∧
    int_0_1 + sum_tau_blocks ≤ Z3_sq / (5 - 2 * sigma) + C_sigma / (1 - tau_pow_neg_sigma) := by
  refine ⟨h_dil, ?_, ?_, by linarith⟩
  · intro hBmu
    have h_mul : zeta_1_2sigma * norm_mu ≤ zeta_1_2sigma * B_mu :=
      mul_le_mul_of_nonneg_left hBmu (le_of_lt h_z1_pos)
    linarith
  · intro hBlam
    have h_quot_pos : 0 ≤ zeta_1_2sigma / zeta_2_4sigma :=
      div_nonneg (le_of_lt h_z1_pos) (le_of_lt h_z2_pos)
    have h_mul :
        (zeta_1_2sigma / zeta_2_4sigma) * norm_lambda ≤
          (zeta_1_2sigma / zeta_2_4sigma) * B_lam :=
      mul_le_mul_of_nonneg_left hBlam h_quot_pos
    linarith

/-- **Theorem 4 (`TASK-TC-054` §4)**: Euler–Maclaurin `N = 2` inflection-root integral identity
    `C_2 = (f'(v_-) - f'(v_+)) / 6` and subtransition growing-range exponent algebra `A <= X^{1 - delta}`:
    (1) On `(0, v_-)`, `(v_-, v_+)`, and `(v_+, infty)` where `I_1 = f'(v_-) >= 0`,
        `I_2 = f'(v_+) - f'(v_-) <= 0`, and `I_3 = -f'(v_+) >= 0`, the `N = 2` Euler–Maclaurin
        constant `(1 / 12) * (|I_1| + |I_2| + |I_3|)` equals `(f'(v_-) - f'(v_+)) / 6`;
    (2) For any `N : ℝ` and `delta : ℝ`, `(N + 1) * (1 - delta) - N = 1 - (N + 1) * delta`,
        and `1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta`. -/
theorem euler_maclaurin_c2_and_subtransition_growing_range_exponent
    (f_prime_v_minus f_prime_v_plus N delta : ℝ)
    (h_v_minus_nonneg : 0 ≤ f_prime_v_minus)
    (h_v_plus_nonpos : f_prime_v_plus ≤ 0) :
    (1 / 12 : ℝ) * (|f_prime_v_minus| + |f_prime_v_plus - f_prime_v_minus| + |-f_prime_v_plus|) =
      (f_prime_v_minus - f_prime_v_plus) / 6 ∧
    ((N + 1) * (1 - delta) - N = 1 - (N + 1) * delta ∧
      (1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta)) := by
  refine ⟨?_, ?_⟩
  · have h_abs1 : |f_prime_v_minus| = f_prime_v_minus := abs_of_nonneg h_v_minus_nonneg
    have h_diff_nonpos : f_prime_v_plus - f_prime_v_minus ≤ 0 := by linarith
    have h_abs2 : |f_prime_v_plus - f_prime_v_minus| = -(f_prime_v_plus - f_prime_v_minus) :=
      abs_of_nonpos h_diff_nonpos
    have h_neg_nonneg : 0 ≤ -f_prime_v_plus := by linarith
    have h_abs3 : |-f_prime_v_plus| = -f_prime_v_plus := abs_of_nonneg h_neg_nonneg
    rw [h_abs1, h_abs2, h_abs3]
    ring
  · refine ⟨by ring, ?_⟩
    constructor <;> intro h <;> linarith

/-- **Theorem 5 (`TASK-TC-054` §6B)**: Dyadic parity energy identity with cross-scale correlation
    and off-critical mode nonvanishing:
    (1) Pointwise dyadic parity square identity: for all `Q_X Q_half_X sqrt2 : ℝ` with
        `sqrt2 ^ 2 = 2`, `(Q_X + (1 / sqrt2) * Q_half_X) ^ 2 = Q_X ^ 2 + (1 / 2) * Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X`;
    (2) Off-critical mode nonvanishing under the dyadic parity factor `1 + 2^{-rho}`:
        if `0 < two_pow_neg_beta` and `two_pow_neg_beta < 1` (`beta = Re(rho) > 0`), and
        `1 - two_pow_neg_beta <= abs_one_plus_two_pow_neg_rho`, then
        `0 < abs_one_plus_two_pow_neg_rho` (proving the elementary dyadic factor `1 + 2^{-rho}`
        cannot annihilate an off-critical mode in `Re(rho) > 0`). -/
theorem dyadic_parity_energy_and_off_critical_mode_nonvanishing
    (Q_X Q_half_X sqrt2 two_pow_neg_beta abs_one_plus_two_pow_neg_rho : ℝ)
    (h_sqrt2 : sqrt2 ^ 2 = 2)
    (h_sqrt2_ne : sqrt2 ≠ 0)
    (h_beta_lt_one : two_pow_neg_beta < 1)
    (h_rev_tri : 1 - two_pow_neg_beta ≤ abs_one_plus_two_pow_neg_rho) :
    (Q_X + (1 / sqrt2) * Q_half_X) ^ 2 =
      Q_X ^ 2 + (1 / 2 : ℝ) * Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X ∧
    (0 < 1 - two_pow_neg_beta ∧ 0 < abs_one_plus_two_pow_neg_rho) := by
  constructor
  · field_simp [h_sqrt2_ne]
    calc
      (Q_X * sqrt2 + Q_half_X) ^ 2 * 2 =
          ((sqrt2 ^ 2) * Q_X ^ 2 + Q_half_X ^ 2 + 2 * sqrt2 * Q_X * Q_half_X) * 2 := by ring
      _ = (2 * Q_X ^ 2 + Q_half_X ^ 2 + 2 * sqrt2 * Q_X * Q_half_X) * 2 := by rw [h_sqrt2]
      _ = (Q_X ^ 2 * 2 + Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X * 2) * sqrt2 ^ 2 := by
        rw [h_sqrt2]
        ring
  · refine ⟨by linarith, by linarith⟩

end LiouvilleSquareDilation

end RiemannScope
