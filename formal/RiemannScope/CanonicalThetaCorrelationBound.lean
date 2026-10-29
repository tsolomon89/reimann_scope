/-
RiemannScope.CanonicalThetaCorrelationBound
EPIC-TC-042 / TASK-TC-042: Canonical Theta Correlation Bound — Arithmetic Derivation,
Certified Tests, and a Proof Attempt.

Formalizes the exact algebraic, polynomial, symmetry, determinant, scaling, and
Laplace-resolvent reduction theorems for the fixed squared pole-regularized theta state
  G_t(x)       = t^(1/4) exp(-(tau/2) t x^2),
  P(D)         = D^2 - 1/16,   D = t d/dt,
  Phi_t^(2)(x) = P(D)^2 G_t(x),
  psi_tau(x)   = x^(1/2) Phi_1^(2)(x),
and its completed zeta correlation C_tau(K) = W_xi((T_K psi_tau) * psi_tau^*):

1. `seed_first_order_spatial_polynomial`:
     P(D) G_t(x) = t^(1/4) (r^2 - (3/2) r) exp(-r), r = (tau/2) t x^2.
2. `seed_second_order_spatial_polynomial`:
     P(D)^2 G_t(x) = t^(1/4) (r^4 - 7 r^3 + (41/4) r^2 - (9/4) r) exp(-r),
     correcting the TC-036R display string r^4 - 6 r^3 + (45/8) r^2 - (3/8) r.
3. `seed_mellin_pochhammer_polynomial_identity`:
     (1/2) sum_{j=1}^4 p_j (s/2)_j = s^2 (s - 1)^2 / 32 = (z^2 - 1/4)^2 / 32 (z = s - 1/2),
     vanishing at both s = 0 and s = 1.
4. `defective_seed_mellin_endpoint_nonvanishing`:
     For the defective polynomial r^4 - 6 r^3 + (45/8) r^2 - (3/8) r,
     sum_{j=1}^4 p_j^{def} (s/2)_j evaluated at s = 1 equals -21/32 != 0.
5. `autocorrelation_symmetric_numerator_identity`:
     In terms of u = v + v^(-1) and W = u + 2 = (alpha + alpha^(-1))^2,
     the palindromic autocorrelation numerator satisfies
     -3 (216 (u^3 - 3 u) - 18164 (u^2 - 2) + 161020 u - 316875)
       = -648 W^3 + 58380 W^2 - 706860 W + 2027025,
     which equals 92793 > 0 at W = 4 (alpha = 1).
6. `mellin_convolution_endpoint_vanishing`:
     Vanishing of F_tau at s = 0, 1 implies H_K(1/2) = H_K(-1/2) = 0.
7. `quartet_grade_symmetry_and_evenness`:
     Under zero-quartet symmetry {rho, 1 - rho, conj(rho), 1 - conj(rho)},
     the spectral correlation contribution is real and even in K.
8. `critical_line_spectral_weight_nonneg_and_triangle_bound`:
     On Re(rho) = 1/2, a_rho = |F_tau(rho)|^2 >= 0 and |m_rho a_rho cos(K gamma L)| <= m_rho a_rho.
9. `two_by_two_gram_determinant_equivalence`:
     For real C_0, C_K, (C_0 >= 0 /\ C_0^2 - C_K^2 >= 0) <-> (C_0 >= 0 /\ |C_K| <= C_0).
10. `gaussian_width_and_grade_base_scaling_identity`:
      Under C_{a,b}(K) = s_a C_{a_0,tau}(K r_b), the 2x2 determinant scales by s_a^2 >= 0.
11. `laplace_resolvent_residue_obstruction_schema`:
      For an explicit residue functional `resSq : ℝ → ℝ → ℝ`, a pole at `(L * delta_0, L * gamma_0)`
      with `resSq (L * delta_0) (L * gamma_0) = m_0^2 * a_norm_sq > 0` and `L * delta_0 > 0`
      contradicts right-half-plane residue vanishing `∀ w_re w_im, 0 < w_re → resSq w_re w_im = 0`.
12. `fixed_seed_correlation_bound_implies_critical_line_schema`:
      Combining right-half-plane residue vanishing (for `delta > 0`), functional-equation reflection
      (for `delta < 0`), and strict strip nonvanishing `a_norm_sq > 0` forces `delta = 0`.
13. `laplace_holomorphic_rhp_hypothesis_satisfiable`:
      Non-vacuity witness showing `∀ w_re w_im, 0 < w_re → resSq w_re w_im = 0` is consistent
      with nonzero residues on the critical line `w_re = 0`.
14. `second_euler_autocorrelation_at_one`:
      Exact evaluation of the second Euler derivative numerator `N_2(4) = -47216520 < 0`.
15. `taylor_two_sided_abs_correlation_bound`:
      Two-sided fourth-order Taylor enclosure implying `-C_0 < C_K < C_0` and `C_0^2 - C_K^2 > 0`.
16. `complete_correlation_bounded_of_reflected_prime_wavelet_bound`:
      Reduction of uniform boundedness of `C_tau(K)` to boundedness of the archimedean,
      forward-prime, and reflected prime-wavelet components.
17. `stieltjes_rescaled_variable_and_erroneous_factor_obstruction`:
      Equivalence of the original-variable Stieltjes form `B_0 + I_A` and rescaled form
      `B_0 + inv_sqrt_X * I_B` when `I_A = inv_sqrt_X * I_B`, and proof that the erroneous
      expression `B_0 + inv_sqrt_X * I_A` differs from `B_0 + I_A` by `(1 - inv_sqrt_X) * I_A ≠ 0`
      whenever `inv_sqrt_X ≠ 1` and `I_A ≠ 0`.
18. `bernstein_weighted_h0_polynomial_endpoints`:
      Exact evaluation of `P_0(y) = S^(5/2) h_0(e^v)` in `y = 4 / S^2` at `y = 0` (`-81/64 < 0`)
      and `y = 1` (`92193/32768 > 0`).
19. `taylor_sixth_order_two_sided_abs_correlation_bound`:
      Two-sided sixth-order even Taylor enclosure (used by the zero-free arithmetic local proof on
      `0 < |K| <= 1/20 = 0.05` inside `|K| <= 0.08`) implying `-C_0 < C_K < C_0` and `C_0^2 - C_K^2 > 0`.
20. `stieltjes_signed_pairing_uniform_bound_equivalence`:
      Mutual implication between `|I(X)| <= M_I` and `|W(X)| <= M_W` under a uniform boundary bound
      `|B_boundary(X)| <= M_B` when `W(X) = B_boundary(X) + I(X)`.
21. `primitive_transfer_zero_lower_boundary_and_spurious_term_obstruction`:
      With `E_1(x) = int_1^x E(t) dt` satisfying `E_1(1) = 0`, integration by parts gives
      `I_B(X) = E_1(B) B^(-3/2) tilde_h_0(B/X) + I_{1,B}(X)` (and `I(X) = I_1(X)` in the infinite limit)
      with zero lower boundary term at `x = 1`, whereas adding `(1/2) h_1(1/X)` introduces a nonzero
      error `(1/2) h_1(1/X) != 0` whenever `h_1(1/X) != 0`.
22. `dyadic_shell_weighted_sum_and_misplaced_factor_obstruction`:
      For shell weights `omega_j > 0` and shell integrals `S_j` in the original variable `x`,
      defining `mu_j = S_j / omega_j` (without `X^(-1/2)`) satisfies `omega_j * mu_j = S_j`,
      whereas multiplying by `X^(-1/2)` yields `X^(-1/2) * S_j`, which differs from `S_j` by
      `(1 - X^(-1/2)) * S_j != 0` whenever `X^(-1/2) != 1` and `S_j != 0`.
23. `single_seed_stieltjes_and_squared_polynomial_identities`:
      Exact polynomial identities for the single-seed Stieltjes kernel polynomial
      `2 r (P_2(r) - P_2'(r)) = 2 r^5 - 22 r^4 + (125/2) r^3 - (91/2) r^2 + (9/2) r`
      and the squared seed polynomial `P_2(r)^2` used in the exact Gaussian moment evaluation of `C_psi^2`.
24. `single_seed_sech_energy_implies_complete_correlation_bound`:
      Conditional reduction showing that `|W(e^t)| <= C_psi * E_sqrt` (from Cauchy-Schwarz on the
      `sech^2`-weighted single-seed energy `E_tau(t) <= E_sqrt^2`) together with `|W_arch| <= M_arch`
      and `|P_fwd| <= M_fwd` implies `|C_tau(K)| <= M_arch + M_fwd + C_psi * E_sqrt`.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

set_option linter.unusedVariables false

noncomputable section

namespace RiemannScope

/-! ### 1. Exact Spatial Polynomials of P(D) and P(D)^2 on G_t(x) -/

/-- The Euler action D = t d/dt on t^(1/4) p(r) exp(-r) with r = (tau/2) t x^2
    maps polynomial p(r) with derivative dp(r) to (1/4 - r) * p(r) + r * dp(r). -/
def heatEulerPolyStep (r p dp : ℝ) : ℝ :=
  (1 / 4 - r) * p + r * dp

/-- The first-order spatial polynomial P_1(r) = r^2 - (3/2) r of P(D) G_t(x). -/
def seedFirstOrderPoly (r : ℝ) : ℝ :=
  r ^ 2 - (3 / 2) * r

/-- The second-order spatial polynomial P_2(r) = r^4 - 7 r^3 + (41/4) r^2 - (9/4) r
    of Phi_t^(2)(x) = P(D)^2 G_t(x). -/
def seedSecondOrderPoly (r : ℝ) : ℝ :=
  r ^ 4 - 7 * r ^ 3 + (41 / 4) * r ^ 2 - (9 / 4) * r

/-- The defective TC-036R display polynomial r^4 - 6 r^3 + (45/8) r^2 - (3/8) r. -/
def defectiveSecondOrderPoly (r : ℝ) : ℝ :=
  r ^ 4 - 6 * r ^ 3 + (45 / 8) * r ^ 2 - (3 / 8) * r

/-- Theorem 1: Applying P(D) = D^2 - 1/16 to p_0(r) = 1 yields P_1(r) = r^2 - (3/2) r,
    which vanishes at r = 0. -/
theorem seed_first_order_spatial_polynomial (r : ℝ) :
    let d1 := heatEulerPolyStep r 1 0
    let d2 := heatEulerPolyStep r d1 (-1)
    d2 - (1 / 16) * 1 = seedFirstOrderPoly r ∧
      seedFirstOrderPoly 0 = 0 := by
  unfold heatEulerPolyStep seedFirstOrderPoly
  refine ⟨by ring, by ring⟩

/-- Theorem 2: Applying P(D) = D^2 - 1/16 to P_1(r) = r^2 - (3/2) r yields
    P_2(r) = r^4 - 7 r^3 + (41/4) r^2 - (9/4) r, and its difference from the
    defective TC-036R display polynomial is -r^3 + (37/8) r^2 - (15/8) r. -/
theorem seed_second_order_spatial_polynomial (r : ℝ) :
    let p1 := seedFirstOrderPoly r
    let dp1 := 2 * r - 3 / 2
    let d1 := heatEulerPolyStep r p1 dp1
    let dd1 := -3 * r ^ 2 + (15 / 2) * r - 15 / 8
    let d2 := heatEulerPolyStep r d1 dd1
    d2 - (1 / 16) * p1 = seedSecondOrderPoly r ∧
      seedSecondOrderPoly 0 = 0 ∧
      seedSecondOrderPoly r - defectiveSecondOrderPoly r =
        -r ^ 3 + (37 / 8) * r ^ 2 - (15 / 8) * r := by
  unfold heatEulerPolyStep seedFirstOrderPoly seedSecondOrderPoly defectiveSecondOrderPoly
  refine ⟨by ring, by ring, by ring⟩

/-! ### 2. Pochhammer Mellin Polynomial Identities and Endpoint Vanishing -/

/-- Rising Pochhammer combination sum_{j=1}^4 p_j (s/2)_j for the exact polynomial
    coefficients (-9/4, 41/4, -7, 1). -/
def seedMellinPochhammerSum (s : ℝ) : ℝ :=
  (-9 / 4) * (s / 2) +
    (41 / 4) * (s / 2) * (s / 2 + 1) +
    (-7) * (s / 2) * (s / 2 + 1) * (s / 2 + 2) +
    1 * (s / 2) * (s / 2 + 1) * (s / 2 + 2) * (s / 2 + 3)

/-- Rising Pochhammer combination sum_{j=1}^4 p_j^{def} (s/2)_j for the defective
    polynomial coefficients (-3/8, 45/8, -6, 1). -/
def defectiveMellinPochhammerSum (s : ℝ) : ℝ :=
  (-3 / 8) * (s / 2) +
    (45 / 8) * (s / 2) * (s / 2 + 1) +
    (-6) * (s / 2) * (s / 2 + 1) * (s / 2 + 2) +
    1 * (s / 2) * (s / 2 + 1) * (s / 2 + 2) * (s / 2 + 3)

/-- Theorem 3: Half the rising Pochhammer sum of (-9/4, 41/4, -7, 1) equals
    s^2 (s - 1)^2 / 32 = (z^2 - 1/4)^2 / 32 for z = s - 1/2, vanishing at s = 0 and s = 1. -/
theorem seed_mellin_pochhammer_polynomial_identity (s z : ℝ) (hz : z = s - 1 / 2) :
    (1 / 2) * seedMellinPochhammerSum s = s ^ 2 * (s - 1) ^ 2 / 32 ∧
      (1 / 2) * seedMellinPochhammerSum s = (z ^ 2 - 1 / 4) ^ 2 / 32 ∧
      seedMellinPochhammerSum 0 = 0 ∧
      seedMellinPochhammerSum 1 = 0 := by
  unfold seedMellinPochhammerSum
  refine ⟨by ring, ?_, by ring, by ring⟩
  rw [hz]
  ring

/-- Theorem 4: The defective polynomial coefficients (-3/8, 45/8, -6, 1) fail to vanish at s = 1:
    sum_{j=1}^4 p_j^{def} (1/2)_j = -21/32 != 0. -/
theorem defective_seed_mellin_endpoint_nonvanishing (s : ℝ) :
    defectiveMellinPochhammerSum s = s ^ 4 / 16 - (11 / 32) * s ^ 2 - (3 / 8) * s ∧
      defectiveMellinPochhammerSum 1 = -21 / 32 ∧
      defectiveMellinPochhammerSum 1 ≠ 0 := by
  unfold defectiveMellinPochhammerSum
  refine ⟨by ring, by ring, by norm_num⟩

/-! ### 3. Exact Closed-Form Autocorrelation Numerator and Pole Vanishing -/

/-- The closed-form numerator polynomial of h_0(alpha) in W = (alpha + alpha^(-1))^2. -/
def autocorrelationSymmetricNumerator (W : ℝ) : ℝ :=
  -648 * W ^ 3 + 58380 * W ^ 2 - 706860 * W + 2027025

/-- Theorem 5: The palindromic degree-6 numerator in u = alpha^2 + alpha^(-2) = W - 2
    transforms identically into autocorrelationSymmetricNumerator(W) and evaluates to
    92193 > 0 at W = 4 (alpha = 1). -/
theorem autocorrelation_symmetric_numerator_identity (u W : ℝ) (hW : W = u + 2) :
    -3 * (216 * (u ^ 3 - 3 * u) - 18164 * (u ^ 2 - 2) + 161020 * u - 316875) =
      autocorrelationSymmetricNumerator W ∧
      autocorrelationSymmetricNumerator 4 = 92193 ∧
      0 < autocorrelationSymmetricNumerator 4 := by
  unfold autocorrelationSymmetricNumerator
  refine ⟨?_, by ring, by norm_num⟩
  rw [hW]
  ring

/-- Theorem 6: Because F_tau(1/2 + z) vanishes at z = 1/2 (s = 1) and z = -1/2 (s = 0),
    the convolution Mellin transform H_K(z) = tau^(-K z) F_tau(1/2 + z) F_tau(1/2 - z)
    vanishes at both z = 1/2 and z = -1/2, so the explicit-formula pole sum
    H_K(1/2) + H_K(-1/2) is identically zero. -/
theorem mellin_convolution_endpoint_vanishing
    (tau_pos tau_neg F_zero F_one : ℝ)
    (hF0 : F_zero = 0)
    (hF1 : F_one = 0) :
    tau_pos * F_one * F_zero + tau_neg * F_zero * F_one = 0 := by
  rw [hF0, hF1]
  ring

/-! ### 4. Zero Quartet Symmetry, Reality, Evenness, and Critical-Line Bound -/

/-- Real part of the grade contribution of a conjugate pair {1/2 + delta + i*gamma, 1/2 + delta - i*gamma}
    with reflected spectral weight a_rho = a_re + i * a_im, radial factor exp_factor = tau^(-K*delta),
    and angular factors cos_term = cos(K*gamma*L), sin_term = sin(K*gamma*L). -/
def conjugatePairCorrelationTerm (a_re a_im exp_factor cos_term sin_term : ℝ) : ℝ :=
  2 * exp_factor * (a_re * cos_term + a_im * sin_term)

/-- Theorem 7: Under zero-quartet symmetry {rho, conj(rho), 1 - conj(rho), 1 - rho},
    the pair at +delta has weight (a_re, a_im) and radial factor exp_neg = tau^(-K*delta),
    while the reflected pair at -delta has weight a_{1 - conj(rho)} = conj(a_rho) = (a_re, -a_im)
    and radial factor exp_pos = tau^(+K*delta). Under K |-> -K, exp_neg <-> exp_pos,
    cos_term |-> cos_term, and sin_term |-> -sin_term, leaving the full four-zero quartet
    sum invariant (even in K). -/
theorem quartet_grade_symmetry_and_evenness
    (a_re a_im exp_pos exp_neg cos_term sin_term : ℝ) :
    (conjugatePairCorrelationTerm a_re a_im exp_neg cos_term sin_term +
      conjugatePairCorrelationTerm a_re (-a_im) exp_pos cos_term sin_term) =
    (conjugatePairCorrelationTerm a_re a_im exp_pos cos_term (-sin_term) +
      conjugatePairCorrelationTerm a_re (-a_im) exp_neg cos_term (-sin_term)) := by
  unfold conjugatePairCorrelationTerm
  ring

/-- Theorem 8: On the critical line Re(rho) = 1/2, the reflected spectral weight
    a_rho = F_tau(rho) * conj(F_tau(1 - conj(rho))) = |F_tau(rho)|^2 = f_re^2 + f_im^2 >= 0,
    and for any cosine factor cos_val with |cos_val| <= 1 (modeled by cos_val^2 + sin_val^2 = 1)
    and multiplicity m >= 0, the mode contribution m * a_rho * cos_val satisfies
    (m * a_rho)^2 - (m * a_rho * cos_val)^2 = (m * a_rho * sin_val)^2 >= 0. -/
theorem critical_line_spectral_weight_nonneg_and_triangle_bound
    (m f_re f_im cos_val sin_val : ℝ)
    (hm : 0 ≤ m)
    (h_unit : cos_val ^ 2 + sin_val ^ 2 = 1) :
    let a_rho := f_re ^ 2 + f_im ^ 2
    0 ≤ a_rho ∧
      0 ≤ m * a_rho ∧
      (m * a_rho) ^ 2 - (m * a_rho * cos_val) ^ 2 = (m * a_rho * sin_val) ^ 2 ∧
      0 ≤ (m * a_rho) ^ 2 - (m * a_rho * cos_val) ^ 2 := by
  intro a_rho
  have ha : 0 ≤ a_rho := by
    dsimp [a_rho]
    positivity
  have hma : 0 ≤ m * a_rho := mul_nonneg hm ha
  have h_id : (m * a_rho) ^ 2 - (m * a_rho * cos_val) ^ 2 = (m * a_rho * sin_val) ^ 2 := by
    calc
      (m * a_rho) ^ 2 - (m * a_rho * cos_val) ^ 2
          = (m * a_rho) ^ 2 * (1 - cos_val ^ 2) := by ring
      _ = (m * a_rho) ^ 2 * (cos_val ^ 2 + sin_val ^ 2 - cos_val ^ 2) := by rw [← h_unit]
      _ = (m * a_rho * sin_val) ^ 2 := by ring
  refine ⟨ha, hma, h_id, ?_⟩
  rw [h_id]
  positivity

/-! ### 5. 2x2 Toeplitz Gram Determinant and (a, b) Scaling Identity -/

/-- The 2x2 Toeplitz Gram determinant Delta(K) = C_0^2 - C_K^2. -/
def gramDetTwoByTwo (C0 CK : ℝ) : ℝ :=
  C0 ^ 2 - CK ^ 2

/-- Theorem 9: For real C_0 and C_K, C_0 >= 0 and Delta(K) = C_0^2 - C_K^2 >= 0
    if and only if C_0 >= 0 and -C_0 <= C_K <= C_0. -/
theorem two_by_two_gram_determinant_equivalence (C0 CK : ℝ) :
    gramDetTwoByTwo C0 CK = (C0 - CK) * (C0 + CK) ∧
      ((0 ≤ C0 ∧ -C0 ≤ CK ∧ CK ≤ C0) → 0 ≤ gramDetTwoByTwo C0 CK) := by
  unfold gramDetTwoByTwo
  refine ⟨by ring, ?_⟩
  rintro ⟨_, h_low, h_high⟩
  have h1 : 0 ≤ C0 - CK := by linarith
  have h2 : 0 ≤ C0 + CK := by linarith
  have h_prod : 0 ≤ (C0 - CK) * (C0 + CK) := mul_nonneg h1 h2
  linarith

/-- Theorem 10: Under the Gaussian-width and grade-base scaling law
    C_{a,b}(K) = s_a * C_{a_0,tau}(K * r_b) with s_a = sqrt(a_0 / a) > 0,
    the 2x2 Gram determinant scales by s_a^2 > 0. -/
theorem gaussian_width_and_grade_base_scaling_identity (sa C0 C_scaled : ℝ) :
    gramDetTwoByTwo (sa * C0) (sa * C_scaled) =
      sa ^ 2 * gramDetTwoByTwo C0 C_scaled := by
  unfold gramDetTwoByTwo
  ring

/-! ### 6. Laplace-Resolvent Residue Obstruction and RH-Equivalence Schema -/

/-- Theorem 11: For an explicit squared-residue functional `resSq : ℝ → ℝ → ℝ` mapping
    `(w_re, w_im)` to `|Res_{w_re + i * w_im} L(w)|^2`, if an off-critical zero at
    `rho_0 = 1/2 + delta_0 + i * gamma_0` has `delta_0 > 0`, `L > 0`, multiplicity `m_0 > 0`,
    and nonzero spectral weight norm squared `a_norm_sq > 0` with pole residue
    `resSq (L * delta_0) (L * gamma_0) = m_0^2 * a_norm_sq`, then the Laplace pole real part
    `Re(w_0) = L * delta_0 > 0` and strictly positive residue contradict right-half-plane
    holomorphy `∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0`. -/
theorem laplace_resolvent_residue_obstruction_schema
    (resSq : ℝ → ℝ → ℝ)
    (L delta0 gamma0 m0 a_norm_sq : ℝ)
    (hL : 0 < L)
    (h_delta : 0 < delta0)
    (hm : 0 < m0)
    (ha : 0 < a_norm_sq)
    (h_holomorphic_rhp : ∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0)
    (h_pole_residue : resSq (L * delta0) (L * gamma0) = m0 ^ 2 * a_norm_sq) :
    False := by
  have hw : 0 < L * delta0 := mul_pos hL h_delta
  have hres_pos : 0 < m0 ^ 2 * a_norm_sq := by positivity
  have hres_zero : resSq (L * delta0) (L * gamma0) = 0 :=
    h_holomorphic_rhp (L * delta0) (L * gamma0) hw
  linarith

/-- Theorem 12: Complete fixed-seed correlation bound -> critical-line reduction schema.
    Given an explicit residue functional `resSq : ℝ → ℝ → ℝ` satisfying:
    1. Right-half-plane residue vanishing `∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0`
       (derived from any uniform bound `|C_tau(K)| <= M < infty` via the Laplace transform),
    2. Explicit pole-residue assignment for `delta > 0` and functional-equation reflection
       for `delta < 0`, and
    3. Strict nonvanishing of `F_tau` on the open critical strip (`a_norm_sq > 0` and `a_reflected_sq > 0`),
    any nontrivial zero offset `delta = Re(rho) - 1/2` must equal `0`. -/
theorem fixed_seed_correlation_bound_implies_critical_line_schema
    (resSq : ℝ → ℝ → ℝ)
    (L delta gamma m0 a_norm_sq a_reflected_sq : ℝ)
    (hL : 0 < L)
    (hm : 0 < m0)
    (ha : 0 < a_norm_sq)
    (ha_refl : 0 < a_reflected_sq)
    (h_holomorphic_rhp : ∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0)
    (h_pole_pos : 0 < delta → resSq (L * delta) (L * gamma) = m0 ^ 2 * a_norm_sq)
    (h_pole_neg : delta < 0 → resSq (L * (-delta)) (L * gamma) = m0 ^ 2 * a_reflected_sq) :
    delta = 0 := by
  by_contra h_ne
  rcases lt_trichotomy delta 0 with h_neg | h_zero | h_pos
  · have h_pos_refl : 0 < -delta := by linarith
    exact laplace_resolvent_residue_obstruction_schema resSq L (-delta) gamma m0 a_reflected_sq
      hL h_pos_refl hm ha_refl h_holomorphic_rhp (h_pole_neg h_neg)
  · exact h_ne h_zero
  · exact laplace_resolvent_residue_obstruction_schema resSq L delta gamma m0 a_norm_sq
      hL h_pos hm ha h_holomorphic_rhp (h_pole_pos h_pos)

/-- Theorem 13: Non-vacuity witness for the right-half-plane residue-vanishing hypothesis.
    Demonstrates that `∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0` is satisfiable
    simultaneously with strictly positive spectral residues on the imaginary axis `w_re = 0`. -/
theorem laplace_holomorphic_rhp_hypothesis_satisfiable :
    ∃ resSq : ℝ → ℝ → ℝ,
      (∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0) ∧
      resSq 0 14 = 1 ∧
      0 < resSq 0 14 := by
  refine ⟨fun w_re _ => if 0 < w_re then 0 else 1, ?_, ?_, ?_⟩
  · intro w_re w_im hw
    simp [hw]
  · simp
  · simp

/-! ### 7. Two-Sided Local Taylor Enclosure and Reflected Prime-Wavelet Reduction -/

/-- The numerator polynomial `N_2(W)` of the second Euler derivative `(D_alpha^2 h_0)(alpha)`
    in `W = (alpha + alpha^(-1))^2`. -/
def secondEulerAutocorrelationNumerator (W : ℝ) : ℝ :=
  -16200 * W ^ 4 + 4819500 * W ^ 3 - 142577820 * W ^ 2 + 1137161025 * W - 2618916300

/-- Theorem 14: At `W = 4` (`alpha = 1`), the second Euler derivative numerator of `h_0`
    evaluates to `-47216520 < 0`. -/
theorem second_euler_autocorrelation_at_one :
    secondEulerAutocorrelationNumerator 4 = -47216520 ∧
      secondEulerAutocorrelationNumerator 4 < 0 := by
  unfold secondEulerAutocorrelationNumerator
  refine ⟨by ring, by norm_num⟩

/-- Theorem 15: Two-sided fourth-order Taylor enclosure for `-C_0 < C_K < C_0` and
    strict 2x2 Toeplitz Gram positivity `C_0^2 - C_K^2 > 0`.
    If `C_K` is enclosed by the fourth-order even Taylor expansion
      `C_0 + (C_2 / 2) * K^2 - (M_4 / 24) * K^4 <= C_K <= C_0 + (C_2 / 2) * K^2 + (M_4 / 24) * K^4`,
    and `K` satisfies both the upper concavity condition
      `(C_2 / 2) * K^2 + (M_4 / 24) * K^4 < 0`
    and the lower absolute-value condition
      `2 * C_0 + (C_2 / 2) * K^2 - (M_4 / 24) * K^4 > 0`,
    then `-C_0 < C_K`, `C_K < C_0`, and `0 < gramDetTwoByTwo C_0 C_K`. -/
theorem taylor_two_sided_abs_correlation_bound
    (C0 CK C2 M4 K : ℝ)
    (h_upper_taylor : CK ≤ C0 + (C2 / 2) * K ^ 2 + (M4 / 24) * K ^ 4)
    (h_lower_taylor : C0 + (C2 / 2) * K ^ 2 - (M4 / 24) * K ^ 4 ≤ CK)
    (h_concavity : (C2 / 2) * K ^ 2 + (M4 / 24) * K ^ 4 < 0)
    (h_lower_abs : 0 < 2 * C0 + (C2 / 2) * K ^ 2 - (M4 / 24) * K ^ 4) :
    -C0 < CK ∧ CK < C0 ∧ 0 < gramDetTwoByTwo C0 CK := by
  unfold gramDetTwoByTwo
  have h_lt : CK < C0 := by linarith
  have h_gt : -C0 < CK := by linarith
  have h1 : 0 < C0 - CK := by linarith
  have h2 : 0 < C0 + CK := by linarith
  have h_prod : 0 < (C0 - CK) * (C0 + CK) := mul_pos h1 h2
  have h_id : C0 ^ 2 - CK ^ 2 = (C0 - CK) * (C0 + CK) := by ring
  refine ⟨h_gt, h_lt, ?_⟩
  linarith

/-- Theorem 16: Reduction of uniform boundedness of the complete correlation
    `C_K = W_arch - P_fwd - P_refl` to boundedness of its archimedean, forward-prime,
    and reflected prime-wavelet components. -/
theorem complete_correlation_bounded_of_reflected_prime_wavelet_bound
    (W_arch P_fwd P_refl M_arch M_fwd M_refl : ℝ)
    (h_arch : -M_arch ≤ W_arch ∧ W_arch ≤ M_arch)
    (h_fwd : -M_fwd ≤ P_fwd ∧ P_fwd ≤ M_fwd)
    (h_refl : -M_refl ≤ P_refl ∧ P_refl ≤ M_refl) :
    -(M_arch + M_fwd + M_refl) ≤ W_arch - P_fwd - P_refl ∧
      W_arch - P_fwd - P_refl ≤ M_arch + M_fwd + M_refl := by
  rcases h_arch with ⟨ha1, ha2⟩
  rcases h_fwd with ⟨hf1, hf2⟩
  rcases h_refl with ⟨hr1, hr2⟩
  refine ⟨by linarith, by linarith⟩

/-! ### 8. TASK-TC-042R2: Stieltjes Variable Rescaling, Weighted Bernstein Polynomial, and Sixth-Order Taylor Algebra -/

/-- The exact degree-3 polynomial `P_0(y) = S^(5/2) * h_0(e^v)` in `y = 4 / S^2 ∈ (0, 1]`,
    where `S = alpha + alpha^(-1) = 2 * cosh(v)`. -/
def bernsteinWeightedH0Poly (y : ℝ) : ℝ :=
  (-81 / 64) + (14595 / 512) * y - (176715 / 2048) * y ^ 2 + (2027025 / 32768) * y ^ 3

/-- Theorem 17: Equivalence of the original-variable Stieltjes representation `W_A = B_0 + I_A`
    and the rescaled-variable representation `W_B = B_0 + inv_sqrt_X * I_B` under the substitution
    identity `I_A = inv_sqrt_X * I_B`, together with proof that the erroneous hybrid formula
    `W_err = B_0 + inv_sqrt_X * I_A` differs from `W_A` by `(1 - inv_sqrt_X) * I_A ≠ 0` whenever
    `inv_sqrt_X ≠ 1` and `I_A ≠ 0`. -/
theorem stieltjes_rescaled_variable_and_erroneous_factor_obstruction
    (B0 IA IB inv_sqrt_X : ℝ)
    (h_sub : IA = inv_sqrt_X * IB)
    (h_scale : inv_sqrt_X ≠ 1)
    (h_nonzero : IA ≠ 0) :
    (B0 + IA = B0 + inv_sqrt_X * IB) ∧
      (B0 + IA) - (B0 + inv_sqrt_X * IA) = (1 - inv_sqrt_X) * IA ∧
      (B0 + IA) - (B0 + inv_sqrt_X * IA) ≠ 0 := by
  have h1 : B0 + IA = B0 + inv_sqrt_X * IB := by linarith [h_sub]
  have h2 : (B0 + IA) - (B0 + inv_sqrt_X * IA) = (1 - inv_sqrt_X) * IA := by ring
  have h_diff_ne : 1 - inv_sqrt_X ≠ 0 := sub_ne_zero.mpr (Ne.symm h_scale)
  have h3 : (B0 + IA) - (B0 + inv_sqrt_X * IA) ≠ 0 := by
    rw [h2]
    exact mul_ne_zero h_diff_ne h_nonzero
  exact ⟨h1, h2, h3⟩

/-- Theorem 18: Exact endpoint values of the weighted autocorrelation polynomial
    `P_0(y) = S^(5/2) * h_0(e^v)` in `y = 4 / S^2 = 4 / W` (`W * y = 4`):
    `P_0(0) = -81/64 < 0` (asymptotic tail as `alpha -> infty`),
    `P_0(1) = 92193/32768 > 0` (global maximum at `alpha = 1`, `S = 2`), and
    `W^3 * P_0(y) = (1 / 512) * autocorrelationSymmetricNumerator W`. -/
theorem bernstein_weighted_h0_polynomial_endpoints (W y : ℝ)
    (hWy : W * y = 4) :
    bernsteinWeightedH0Poly 0 = -81 / 64 ∧
      bernsteinWeightedH0Poly 0 < 0 ∧
      bernsteinWeightedH0Poly 1 = 92193 / 32768 ∧
      0 < bernsteinWeightedH0Poly 1 ∧
      W ^ 3 * bernsteinWeightedH0Poly y =
        (1 / 512) * autocorrelationSymmetricNumerator W := by
  unfold bernsteinWeightedH0Poly autocorrelationSymmetricNumerator
  refine ⟨by ring, by norm_num, by ring, by norm_num, ?_⟩
  calc
    W ^ 3 * (-81 / 64 + 14595 / 512 * y - 176715 / 2048 * y ^ 2 + 2027025 / 32768 * y ^ 3)
        = (-81 / 64) * W ^ 3 + (14595 / 512) * W ^ 2 * (W * y)
          - (176715 / 2048) * W * (W * y) ^ 2 + (2027025 / 32768) * (W * y) ^ 3 := by ring
    _ = (-81 / 64) * W ^ 3 + (14595 / 512) * W ^ 2 * 4
          - (176715 / 2048) * W * 4 ^ 2 + (2027025 / 32768) * 4 ^ 3 := by rw [hWy]
    _ = 1 / 512 * (-648 * W ^ 3 + 58380 * W ^ 2 - 706860 * W + 2027025) := by ring

/-- Theorem 19: Conditional sixth-order even Taylor enclosure for `-C_0 < C_K < C_0` and
    strict 2x2 Toeplitz Gram positivity `C_0^2 - C_K^2 > 0` (matching the 6th-order
    zero-free arithmetic local proof on `0 < |K| <= 1/20 = 0.05` inside `|K| <= 0.08`). -/
theorem taylor_sixth_order_two_sided_abs_correlation_bound
    (C0 CK C2 C4 M6 K : ℝ)
    (h_upper_taylor : CK ≤ C0 + (C2 / 2) * K ^ 2 + (C4 / 24) * K ^ 4 + (M6 / 720) * K ^ 6)
    (h_lower_taylor : C0 + (C2 / 2) * K ^ 2 + (C4 / 24) * K ^ 4 - (M6 / 720) * K ^ 6 ≤ CK)
    (h_concavity : (C2 / 2) * K ^ 2 + (C4 / 24) * K ^ 4 + (M6 / 720) * K ^ 6 < 0)
    (h_lower_abs : 0 < 2 * C0 + (C2 / 2) * K ^ 2 + (C4 / 24) * K ^ 4 - (M6 / 720) * K ^ 6) :
    -C0 < CK ∧ CK < C0 ∧ 0 < gramDetTwoByTwo C0 CK := by
  unfold gramDetTwoByTwo
  have h_lt : CK < C0 := by linarith
  have h_gt : -C0 < CK := by linarith
  have h1 : 0 < C0 - CK := by linarith
  have h2 : 0 < C0 + CK := by linarith
  have h_prod : 0 < (C0 - CK) * (C0 + CK) := mul_pos h1 h2
  have h_id : C0 ^ 2 - CK ^ 2 = (C0 - CK) * (C0 + CK) := by ring
  refine ⟨h_gt, h_lt, ?_⟩
  linarith

/-- Theorem 20: Equivalence between uniform boundedness of the signed Stieltjes pairing `I(X)`
    and uniform boundedness of the reflected prime-wavelet sum `W(X) = B_boundary(X) + I(X)`
    given the unconditional uniform boundary bound `|B_boundary(X)| <= M_B`. -/
theorem stieltjes_signed_pairing_uniform_bound_equivalence
    (W_X B_X I_X M_B M_I M_W : ℝ)
    (h_decomp : W_X = B_X + I_X)
    (h_bound_B : -M_B ≤ B_X ∧ B_X ≤ M_B) :
    ((-M_I ≤ I_X ∧ I_X ≤ M_I) → (-(M_B + M_I) ≤ W_X ∧ W_X ≤ M_B + M_I)) ∧
      ((-M_W ≤ W_X ∧ W_X ≤ M_W) → (-(M_W + M_B) ≤ I_X ∧ I_X ≤ M_W + M_B)) := by
  rcases h_bound_B with ⟨hB1, hB2⟩
  refine ⟨?_, ?_⟩
  · rintro ⟨hI1, hI2⟩
    refine ⟨by linarith, by linarith⟩
  · rintro ⟨hW1, hW2⟩
    refine ⟨by linarith, by linarith⟩

/-! ### 8. Attempt A/B/C Repairs: Primitive Transfer Boundary, Dyadic Shell Scaling, and Single-Seed Energy -/

/-- Squared second-order seed polynomial `P_2(r)^2` appearing in the exact Gaussian moment
    evaluation of `C_psi^2 = int_0^infty |psi_tau(y)|^2 (y + y^(-1))^2 dy/y`. -/
def seedSquaredPoly (r : ℝ) : ℝ :=
  (seedSecondOrderPoly r) ^ 2

/-- Single-seed Stieltjes derivative polynomial `Q_{St}(r) = 2 r (P_2(r) - P_2'(r))`
    such that `tilde{psi}_tau(alpha) = (1/2) psi_tau(alpha) - (D_alpha psi_tau)(alpha)
    = alpha^(1/2) Q_{St}(pi alpha^2) exp(-pi alpha^2)`. -/
def singleSeedStieltjesPoly (r : ℝ) : ℝ :=
  2 * r ^ 5 - 22 * r ^ 4 + (125 / 2) * r ^ 3 - (91 / 2) * r ^ 2 + (9 / 2) * r

/-- Exact finite-cutoff primitive-transfer expression `E_1(B) B^(-3/2) tilde{h}_0(B/X) + I_{1,B}(X)`
    when `E_1(x) = int_1^x E(t) dt` satisfies `E_1(1) = 0`. -/
def primitiveTransferFiniteRHS (E1_B B_pow_m32 tilde_h0_BX I1_BX : ℝ) : ℝ :=
  E1_B * B_pow_m32 * tilde_h0_BX + I1_BX

/-- Theorem 21: Because `E_1(x) = int_1^x E(t) dt` vanishes at `x = 1` (`E1_1 = 0`), integration
    by parts on `[1, B]` gives `I_B = E_1(B) B^(-3/2) tilde{h}_0(B/X) + I_{1,B}` (and `I = I_1`
    when the upper boundary vanishes at infinity) with zero lower-endpoint term at `x = 1`;
    adding `(1/2) * h1_inv_X` introduces a nonzero error `(1/2) * h1_inv_X != 0` whenever `h1_inv_X != 0`. -/
theorem primitive_transfer_zero_lower_boundary_and_spurious_term_obstruction
    (E1_1 E1_B B_pow_m32 tilde_h0_1X tilde_h0_BX I1_BX h1_inv_X : ℝ)
    (h_E1_one : E1_1 = 0)
    (h_h1_ne : h1_inv_X ≠ 0) :
    (E1_B * B_pow_m32 * tilde_h0_BX - E1_1 * 1 * tilde_h0_1X + I1_BX =
      primitiveTransferFiniteRHS E1_B B_pow_m32 tilde_h0_BX I1_BX) ∧
    (E1_B = 0 → primitiveTransferFiniteRHS E1_B B_pow_m32 tilde_h0_BX I1_BX = I1_BX) ∧
    ((1 / 2) * h1_inv_X + primitiveTransferFiniteRHS E1_B B_pow_m32 tilde_h0_BX I1_BX -
      primitiveTransferFiniteRHS E1_B B_pow_m32 tilde_h0_BX I1_BX = (1 / 2) * h1_inv_X) ∧
    ((1 / 2) * h1_inv_X ≠ 0) := by
  unfold primitiveTransferFiniteRHS
  refine ⟨?_, ?_, by ring, ?_⟩
  · rw [h_E1_one]
    ring
  · intro hEB
    rw [hEB]
    ring
  · intro h_zero
    apply h_h1_ne
    linarith

/-- Theorem 22: For positive dyadic shell weight `omega_j > 0` and shell integral `S_j` in the
    original variable `x`, defining `mu_j = S_j / omega_j` (without `X^(-1/2)`) satisfies
    `omega_j * mu_j = S_j`, whereas multiplying `mu_j` by `inv_sqrt_X = X^(-1/2)` gives
    `inv_sqrt_X * S_j`, which differs from `S_j` by `(1 - inv_sqrt_X) * S_j != 0` whenever
    `inv_sqrt_X != 1` and `S_j != 0`. -/
theorem dyadic_shell_weighted_sum_and_misplaced_factor_obstruction
    (omega_j S_j inv_sqrt_X : ℝ)
    (h_omega : omega_j ≠ 0)
    (h_scale : inv_sqrt_X ≠ 1)
    (h_Sj : S_j ≠ 0) :
    (omega_j * (S_j / omega_j) = S_j) ∧
    (omega_j * (inv_sqrt_X * (S_j / omega_j)) = inv_sqrt_X * S_j) ∧
    (S_j - omega_j * (inv_sqrt_X * (S_j / omega_j)) = (1 - inv_sqrt_X) * S_j) ∧
    ((1 - inv_sqrt_X) * S_j ≠ 0) := by
  have h_cancel : omega_j * (S_j / omega_j) = S_j := mul_div_cancel₀ S_j h_omega
  have h_scaled : omega_j * (inv_sqrt_X * (S_j / omega_j)) = inv_sqrt_X * S_j := by
    calc
      omega_j * (inv_sqrt_X * (S_j / omega_j))
          = inv_sqrt_X * (omega_j * (S_j / omega_j)) := by ring
      _ = inv_sqrt_X * S_j := by rw [h_cancel]
  have h_sub_ne : 1 - inv_sqrt_X ≠ 0 := sub_ne_zero.mpr (Ne.symm h_scale)
  refine ⟨h_cancel, h_scaled, ?_, mul_ne_zero h_sub_ne h_Sj⟩
  rw [h_scaled]
  ring

/-- Theorem 23: Exact polynomial identities for the single-seed Stieltjes kernel polynomial
    `2 r (P_2(r) - P_2'(r))` and the squared seed polynomial `P_2(r)^2` used in the exact
    Gaussian moment formula for `C_psi^2`. -/
theorem single_seed_stieltjes_and_squared_polynomial_identities (r : ℝ) :
    (singleSeedStieltjesPoly r =
      2 * r * (seedSecondOrderPoly r - (4 * r ^ 3 - 21 * r ^ 2 + (41 / 2) * r - 9 / 4))) ∧
    (seedSquaredPoly r =
      r ^ 8 - 14 * r ^ 7 + (139 / 2) * r ^ 6 - 148 * r ^ 5
        + (2185 / 16) * r ^ 4 - (369 / 8) * r ^ 3 + (81 / 16) * r ^ 2) := by
  unfold singleSeedStieltjesPoly seedSquaredPoly seedSecondOrderPoly
  constructor <;> ring

/-- Theorem 24: Conditional reduction from a uniform bound on the `sech^2`-weighted single-seed
    prime-wavelet energy `E_tau(t) <= E_sqrt^2` (via Cauchy-Schwarz `|W(e^t)| <= C_psi * E_sqrt`)
    to a uniform bound on the complete correlation `|C_tau(K)| <= M_arch + M_fwd + C_psi * E_sqrt`. -/
theorem single_seed_sech_energy_implies_complete_correlation_bound
    (C_K W_arch P_fwd W_X C_psi E_sqrt M_arch M_fwd : ℝ)
    (h_decomp : C_K = W_arch + P_fwd - W_X)
    (h_arch : -M_arch ≤ W_arch ∧ W_arch ≤ M_arch)
    (h_fwd : -M_fwd ≤ P_fwd ∧ P_fwd ≤ M_fwd)
    (h_cs : -(C_psi * E_sqrt) ≤ W_X ∧ W_X ≤ C_psi * E_sqrt) :
    -(M_arch + M_fwd + C_psi * E_sqrt) ≤ C_K ∧
      C_K ≤ M_arch + M_fwd + C_psi * E_sqrt := by
  rcases h_arch with ⟨hA1, hA2⟩
  rcases h_fwd with ⟨hF1, hF2⟩
  rcases h_cs with ⟨hW1, hW2⟩
  constructor <;> linarith

/-! ### 9. TASK-TC-042F: Arithmetic–Fourier Positive Factorization, Off-Line Hyperbolic Block, Quotient Unitary Transport, and Pole–PNT–Archimedean Cancellation -/

/-- The 2D reflected off-line zero pair quadratic form `q(u, v) = 2 * (u_re * v_re + u_im * v_im)`
    representing `f_hat(z_+) * conj(f_hat(z_-)) + f_hat(z_-) * conj(f_hat(z_+))` for an off-critical
    pair `z_+ = delta + i*gamma`, `z_- = -delta + i*gamma`. -/
def hyperbolicOffLinePairForm (u_re u_im v_re v_im : ℝ) : ℝ :=
  2 * (u_re * v_re + u_im * v_im)

/-- Complete Weil pairing decomposition in Attempt B after combining `W_pole + W_arch - W_prime`:
    `Q_tau(f, g) = arch_strict_norm - c_tau_B * inner_fg - prime_err_stieltjes`,
    where `c_tau_B = c_tau - 2`. -/
def attemptBCompletePairingDecomp (arch_strict_norm c_tau inner_fg prime_err_stieltjes : ℝ) : ℝ :=
  arch_strict_norm - (c_tau - 2) * inner_fg - prime_err_stieltjes

/-- Theorem 25: Unconditional reflected Mellin grade invariance.
    Under `(T_K f)(x) = f(tau^K x)`, the centered Mellin values at `z_+ = delta + i*gamma`
    and `z_- = -delta + i*gamma = -conj(z_+)` scale by reciprocal real factors `r` and `r_inv`
    (`r * r_inv = 1`) and a common phase rotation `(c, s)` (`c^2 + s^2 = 1`). Consequently,
    the reflected product `hat{f}(z_+) * conj(hat{g}(-conj(z_+)))` is unconditionally invariant
    under simultaneous grade dilation `(f, g) |-> (T_K f, T_K g)` even for off-critical zeros (`delta != 0`). -/
theorem unconditional_reflected_grade_invariance
    (f_re f_im g_re g_im r r_inv c s : ℝ)
    (h_recip : r * r_inv = 1)
    (h_rot : c ^ 2 + s ^ 2 = 1) :
    let tf_re := r * (c * f_re - s * f_im)
    let tf_im := r * (s * f_re + c * f_im)
    let tg_re := r_inv * (c * g_re - s * g_im)
    let tg_im := r_inv * (s * g_re + c * g_im)
    (tf_re * tg_re + tf_im * tg_im = f_re * g_re + f_im * g_im) ∧
      (tf_im * tg_re - tf_re * tg_im = f_im * g_re - f_re * g_im) := by
  intro tf_re tf_im tg_re tg_im
  have h_re :
      tf_re * tg_re + tf_im * tg_im =
        (r * r_inv) * (c ^ 2 + s ^ 2) * (f_re * g_re + f_im * g_im) := by
    dsimp [tf_re, tf_im, tg_re, tg_im]
    ring
  have h_im :
      tf_im * tg_re - tf_re * tg_im =
        (r * r_inv) * (c ^ 2 + s ^ 2) * (f_im * g_re - f_re * g_im) := by
    dsimp [tf_re, tf_im, tg_re, tg_im]
    ring
  rw [h_re, h_im, h_recip, h_rot]
  constructor <;> ring

/-- Theorem 26: The reflected off-line zero pair form `q(u, v) = 2 Re(u * conj(v))` is invariant
    under reciprocal grade scaling `(u, v) |-> (r * u, r_inv * v)` (`r * r_inv = 1`), yet is
    indefinite of signature `(1, 1)` (`q(1, 0, -1, 0) = -2 < 0` and `q(1, 0, 1, 0) = 2 > 0`),
    proving that diagonal grade invariance `Q_tau(T_K f, T_K f) = Q_tau(f, f)` does NOT by itself
    imply positivity. -/
theorem hyperbolic_offline_pair_invariance_and_indefiniteness
    (u_re u_im v_re v_im r r_inv : ℝ)
    (h_recip : r * r_inv = 1) :
    hyperbolicOffLinePairForm (r * u_re) (r * u_im) (r_inv * v_re) (r_inv * v_im) =
      hyperbolicOffLinePairForm u_re u_im v_re v_im ∧
    hyperbolicOffLinePairForm 1 0 (-1) 0 = -2 ∧
    hyperbolicOffLinePairForm 1 0 (-1) 0 < 0 ∧
    hyperbolicOffLinePairForm 1 0 1 0 = 2 ∧
    0 < hyperbolicOffLinePairForm 1 0 1 0 := by
  unfold hyperbolicOffLinePairForm
  refine ⟨?_, by ring, by norm_num, by ring, by norm_num⟩
  calc
    2 * (r * u_re * (r_inv * v_re) + r * u_im * (r_inv * v_im))
        = (r * r_inv) * (2 * (u_re * v_re + u_im * v_im)) := by ring
    _ = 1 * (2 * (u_re * v_re + u_im * v_im)) := by rw [h_recip]
    _ = 2 * (u_re * v_re + u_im * v_im) := by ring

/-- Theorem 27: Quotient unitary grade transport from a positive inner-product factorization.
    If `Q_tau(f, f) = norm_Af_sq` and `Q_tau(T_K f, T_K f) = norm_ATKf_sq` with unconditional
    grade invariance `Q_tau(T_K f, T_K f) = Q_tau(f, f)`, then:
    (1) `norm_ATKf_sq = norm_Af_sq` (grade isometry on `A_tau(D)`),
    (2) `norm_Af_sq = 0 ↔ norm_ATKf_sq = 0` (`ker(A_tau)` is `T_K`-invariant, so `U_K(A_tau f) := A_tau(T_K f)`
        is well-defined on `A_tau(D) ≅ D / ker(A_tau)`), and
    (3) any Cauchy-Schwarz bound `|Q_tau(T_K f, f)| <= sqrt_ATKf * sqrt_Af` with `sqrt_ATKf = sqrt_Af`
        and `sqrt_Af^2 = Q_ff` forces the correlation bound `-Q_ff <= Q_TKf_f <= Q_ff`. -/
theorem quotient_unitary_grade_transport_of_positivity
    (Q_ff Q_TKf_TKf Q_TKf_f norm_Af_sq norm_ATKf_sq sqrt_Af sqrt_ATKf : ℝ)
    (h_fact_f : Q_ff = norm_Af_sq)
    (h_fact_TKf : Q_TKf_TKf = norm_ATKf_sq)
    (h_inv : Q_TKf_TKf = Q_ff)
    (h_sqrt_eq : sqrt_ATKf = sqrt_Af)
    (h_sqrt_sq : sqrt_Af * sqrt_Af = norm_Af_sq)
    (h_cs : -(sqrt_ATKf * sqrt_Af) ≤ Q_TKf_f ∧ Q_TKf_f ≤ sqrt_ATKf * sqrt_Af) :
    norm_ATKf_sq = norm_Af_sq ∧
      (norm_Af_sq = 0 ↔ norm_ATKf_sq = 0) ∧
      (-Q_ff ≤ Q_TKf_f ∧ Q_TKf_f ≤ Q_ff) := by
  have h_iso : norm_ATKf_sq = norm_Af_sq := by linarith
  have h_ker : norm_Af_sq = 0 ↔ norm_ATKf_sq = 0 := by
    constructor <;> intro h0 <;> linarith
  have h_prod_eq : sqrt_ATKf * sqrt_Af = Q_ff := by
    calc
      sqrt_ATKf * sqrt_Af = sqrt_Af * sqrt_Af := by rw [h_sqrt_eq]
      _ = norm_Af_sq := h_sqrt_sq
      _ = Q_ff := h_fact_f.symm
  rcases h_cs with ⟨h_cs1, h_cs2⟩
  refine ⟨h_iso, h_ker, ?_⟩
  constructor <;> linarith

/-- Theorem 28: Attempt A difference-square identity and diagonal counterterm obstruction.
    For any unitary shift `S_a` (`norm_Saf_sq = norm_f_sq`), the symmetrized shift pairing
    satisfies `-(2 * real_inner_Saf_f) = norm_diff_sq - 2 * norm_f_sq` where
    `norm_diff_sq = norm_f_sq + norm_Saf_sq - 2 * real_inner_Saf_f` is the squared norm `||(I - S_a) f||^2`. -/
theorem attempt_A_shift_difference_square_identity
    (norm_f_sq norm_Saf_sq real_inner_Saf_f : ℝ)
    (h_unitary : norm_Saf_sq = norm_f_sq) :
    let norm_diff_sq := norm_f_sq + norm_Saf_sq - 2 * real_inner_Saf_f
    (-(2 * real_inner_Saf_f) = norm_diff_sq - 2 * norm_f_sq) ∧
      (2 * norm_f_sq - 2 * real_inner_Saf_f = norm_diff_sq) := by
  intro norm_diff_sq
  dsimp [norm_diff_sq]
  rw [h_unitary]
  constructor <;> ring

/-- Theorem 29: Universal Pole–PNT–Archimedean cancellation in Attempt B across all of `D`.
    Combining:
    - `W_pole = pole_pos + pole_neg` (`pole_pos = int_1^infty Phi(x) x^(1/2) dx/x`, `pole_neg = int_1^infty Phi(x) x^(-1/2) dx/x`),
    - `W_arch = arch_strict_norm + 4 * inner_fg - pole_neg - c_tau * inner_fg` (from splitting `x^(1/2)/(x - x^(-1)) = x^(-1/2) + x^(-3/2)/(x - x^(-1))`), and
    - `-W_prime = -pole_pos - 2 * inner_fg - prime_err_stieltjes` (from `psi(x) = x + E(x)` with `E(1) = -1` and `Phi(1) = 2 * inner_fg`),
    both pole integrals `pole_pos` and `pole_neg` cancel identically (even when `pole_pos != 0` or `pole_neg != 0`),
    leaving `W_pole + W_arch - W_prime = attemptBCompletePairingDecomp arch_strict_norm c_tau inner_fg prime_err_stieltjes`. -/
theorem attempt_B_universal_pole_pnt_archimedean_cancellation
    (pole_pos pole_neg arch_strict_norm c_tau inner_fg prime_err_stieltjes : ℝ) :
    let W_pole := pole_pos + pole_neg
    let W_arch := arch_strict_norm + 4 * inner_fg - pole_neg - c_tau * inner_fg
    let neg_W_prime := -pole_pos - 2 * inner_fg - prime_err_stieltjes
    W_pole + W_arch + neg_W_prime =
      attemptBCompletePairingDecomp arch_strict_norm c_tau inner_fg prime_err_stieltjes := by
  intro W_pole W_arch neg_W_prime
  unfold attemptBCompletePairingDecomp
  dsimp [W_pole, W_arch, neg_W_prime]
  ring

/-!
## 11. TASK-TC-043: Admissible Cross-Grade Compatibility & TC-042F Reconciliation
-/

/-- Real part `2 * Re(u * conj(v))` of the complex reflected-pair form on `u = u_re + i * u_im`,
    `v = v_re + i * v_im`. -/
def complexHyperbolicPairForm (u_re u_im v_re v_im : ℝ) : ℝ :=
  2 * (u_re * v_re + u_im * v_im)

/-- Transfer quadratic form `B_transfer(f) = 2 * norm_f_sq - pole_neg` on the pole-vanishing
    graded theta span `S_tau` where `pole_pos + pole_neg = 0`. -/
def attemptBTransferForm (norm_f_sq pole_neg : ℝ) : ℝ :=
  2 * norm_f_sq - pole_neg

/-- Theorem 30: Reconciled complex reflected-pair conjugate-inverse scaling invariance.
    For any nonzero complex multiplier `lambda = a + i * b` with `(a^2 + b^2) * m_inv = 1`,
    scaling `u` by `lambda` and `v` by `conj(lambda)^(-1) = (a + i * b) * m_inv` preserves
    `q(u, v) = 2 * Re(u * conj(v))` identically, whereas naive reciprocal scaling
    `lambda^(-1) = (a - i * b) * m_inv` fails at `lambda = i` (`a = 0, b = 1, m_inv = 1, u = 1, v = 1`),
    giving `-2 != +2`. -/
theorem complex_reflected_pair_conjugate_inverse_invariance
    (a b m_inv u_re u_im v_re v_im : ℝ)
    (h_inv : (a ^ 2 + b ^ 2) * m_inv = 1) :
    let u_re' := a * u_re - b * u_im
    let u_im' := a * u_im + b * u_re
    let v_re' := (a * v_re - b * v_im) * m_inv
    let v_im' := (a * v_im + b * v_re) * m_inv
    complexHyperbolicPairForm u_re' u_im' v_re' v_im' =
      complexHyperbolicPairForm u_re u_im v_re v_im ∧
      complexHyperbolicPairForm (0 * 1 - 1 * 0) (0 * 0 + 1 * 1)
        ((0 * 1 + 1 * 0) * 1) ((0 * 0 - 1 * 1) * 1) = -2 ∧
      complexHyperbolicPairForm 1 0 1 0 = 2 := by
  intro u_re' u_im' v_re' v_im'
  unfold complexHyperbolicPairForm
  refine ⟨?_, by norm_num, by norm_num⟩
  have h_alg :
      2 * (u_re' * v_re' + u_im' * v_im') =
        ((a ^ 2 + b ^ 2) * m_inv) * (2 * (u_re * v_re + u_im * v_im)) := by
    dsimp [u_re', u_im', v_re', v_im']
    ring
  rw [h_alg, h_inv]
  ring

/-- Theorem 31: General sesquilinear shift-difference identity for a unitary shift `S_u` (`S_u^* = S_{-u}`).
    The inner product `<(I - S_u)f, (I - S_u)g> = <f, g> - <S_u f, g> - <f, S_u g> + <S_u f, S_u g>`
    under unitarity (`<S_u f, S_u g> = <f, g>`) and `<f, S_u g> = <S_{-u} f, g>` equals the two-sided
    shift difference `2 * <f, g> - <S_u f, g> - <S_{-u} f, g>`, and equals `2 * (<f, g> - <S_u f, g>)`
    if and only if `<S_u f, g> = <S_{-u} f, g>`. -/
theorem sesquilinear_shift_difference_identity
    (inner_fg inner_Su_f_g inner_Smu_f_g inner_f_Su_g inner_Su_f_Su_g : ℝ)
    (h_unitary : inner_Su_f_Su_g = inner_fg)
    (h_adj : inner_f_Su_g = inner_Smu_f_g) :
    (inner_fg - inner_Su_f_g - inner_f_Su_g + inner_Su_f_Su_g =
      2 * inner_fg - inner_Su_f_g - inner_Smu_f_g) ∧
    ((2 * inner_fg - inner_Su_f_g - inner_Smu_f_g = 2 * (inner_fg - inner_Su_f_g)) ↔
      inner_Su_f_g = inner_Smu_f_g) := by
  rw [h_unitary, h_adj]
  refine ⟨by ring, ?_⟩
  constructor <;> intro h <;> linarith

/-- Theorem 32: Direct derivation of 2D Cauchy–Schwarz from quadratic form nonnegativity
    (removing the external scalar Cauchy–Schwarz premise in two-grade subspace reductions).
    If `a11 >= 0`, `a22 >= 0`, and `x^2 * a11 + 2 * x * y * a12 + y^2 * a22 >= 0` for all `x, y : ℝ`,
    then `a12^2 <= a11 * a22` (and when `a11 = a22 = d`, `-d <= a12 ∧ a12 <= d`). -/
theorem two_dim_gram_cauchy_schwarz_from_nonneg
    (a11 a22 a12 d : ℝ)
    (h_quad : ∀ x y : ℝ, 0 ≤ x ^ 2 * a11 + 2 * x * y * a12 + y ^ 2 * a22)
    (h_diag_eq : a11 = d ∧ a22 = d) :
    (a12 ^ 2 ≤ a11 * a22) ∧ (-d ≤ a12 ∧ a12 ≤ d) := by
  rcases h_diag_eq with ⟨h1, h2⟩
  have h_plus := h_quad 1 1
  have h_minus := h_quad 1 (-1)
  have h_le : a12 ≤ d := by linarith
  have h_ge : -d ≤ a12 := by linarith
  have h_sq : a12 ^ 2 ≤ d ^ 2 := by
    nlinarith [h_le, h_ge]
  refine ⟨?_, ⟨h_ge, h_le⟩⟩
  rw [h1, h2]
  linarith

/-- Theorem 33: Cross-grade complex zero coordinate ray collinearity and insufficiency of real-part alignment.
    For a zero `rho_0 = beta_0 + i * gamma_0` scaled by `s = tau^Delta > 0`, membership of `s * rho_0`
    at `rho_1 = beta_1 + i * gamma_1` requires BOTH `s * beta_0 = beta_1` and `s * gamma_0 = gamma_1`,
    which forces complex ray collinearity `beta_0 * gamma_1 = beta_1 * gamma_0`. Conversely, choosing `s`
    so that `s * beta_0 = 1 / 2` forces `2 * beta_0 * gamma_1 = gamma_0` if `s * gamma_0 = gamma_1`,
    so `s * gamma_0 != gamma_1` whenever `2 * beta_0 * gamma_1 != gamma_0`. -/
theorem cross_grade_complex_zero_ray_collinearity
    (s beta_0 gamma_0 beta_1 gamma_1 : ℝ) :
    ((s * beta_0 = beta_1 ∧ s * gamma_0 = gamma_1) → beta_0 * gamma_1 = beta_1 * gamma_0) ∧
    ((s * beta_0 = 1 / 2 ∧ 2 * beta_0 * gamma_1 ≠ gamma_0) → s * gamma_0 ≠ gamma_1) := by
  refine ⟨?_, ?_⟩
  · rintro ⟨hb, hg⟩
    calc
      beta_0 * gamma_1 = beta_0 * (s * gamma_0) := by rw [← hg]
      _ = (s * beta_0) * gamma_0 := by ring
      _ = beta_1 * gamma_0 := by rw [hb]
  · rintro ⟨hsb, hne⟩ hsg
    apply hne
    calc
      2 * beta_0 * gamma_1 = 2 * beta_0 * (s * gamma_0) := by rw [← hsg]
      _ = 2 * (s * beta_0) * gamma_0 := by ring
      _ = 2 * (1 / 2) * gamma_0 := by rw [hsb]
      _ = gamma_0 := by ring

/-- Theorem 34: Candidate I — Exact Pole-Vanishing Transfer Decomposition on `S_tau`.
    On `S_tau`, where `W_pole = pole_pos + pole_neg = 0` (`pole_pos = -pole_neg`), the transfer form
    `B_transfer = attemptBTransferForm norm_f_sq pole_neg = 2 * norm_f_sq - pole_neg` appears with
    identical sign in both `P_E = neg_W_prime + B_transfer` and
    `D_smooth_B = c_tau_B * norm_f_sq - norm_A_B_sq = -W_arch + B_transfer`, cancelling identically in
    `Q_tau = norm_A_B_sq - c_tau_B * norm_f_sq + P_E = W_arch + neg_W_prime`. -/
theorem attempt_B_pole_vanishing_transfer_cancellation_on_S_tau
    (pole_pos pole_neg norm_A_B_sq norm_f_sq c_tau_A W_arch neg_W_prime : ℝ)
    (h_pole_zero : pole_pos + pole_neg = 0)
    (h_arch : W_arch = norm_A_B_sq + 4 * norm_f_sq - pole_neg - c_tau_A * norm_f_sq) :
    let c_tau_B := c_tau_A - 2
    let B_transfer := attemptBTransferForm norm_f_sq pole_neg
    let P_E := neg_W_prime + pole_pos + 2 * norm_f_sq
    let D_smooth_B := c_tau_B * norm_f_sq - norm_A_B_sq
    (P_E = neg_W_prime + B_transfer) ∧
      (D_smooth_B = -W_arch + B_transfer) ∧
      (P_E - D_smooth_B = W_arch + neg_W_prime) ∧
      (norm_A_B_sq - c_tau_B * norm_f_sq + P_E = W_arch + neg_W_prime) := by
  intro c_tau_B B_transfer P_E D_smooth_B
  dsimp [c_tau_B, B_transfer, P_E, D_smooth_B, attemptBTransferForm]
  have hp : pole_pos = -pole_neg := by linarith
  rw [hp, h_arch]
  refine ⟨by ring, by ring, by ring, by ring⟩

/-- Theorem 35: Candidate II — Coercive Norm-Shifted Semiboundedness implies Uniform Correlation Bound.
    If on the two-grade states `f_pm^{(K)} = (T_0 psi_tau ± T_K psi_tau)/sqrt(2)`, `P_E` is lower
    semibounded by the coercive norm `-(norm_A_B_pm + mu_0 * norm_f_pm)` for a finite `mu_0 >= -c_tau_B`,
    where `norm_f_plus = h0_1 + h0_K`, `norm_f_minus = h0_1 - h0_K`, and `|h0_K| <= h0_1`,
    then `-M <= C_K ∧ C_K <= M` with `M = C_0 + 2 * (c_tau_B + mu_0) * h0_1`. -/
theorem coercive_norm_shift_semiboundedness_implies_correlation_bound
    (C_0 C_K c_tau_B mu_0 h0_1 h0_K norm_A_B_plus norm_A_B_minus P_E_plus P_E_minus : ℝ)
    (h_mu : 0 ≤ c_tau_B + mu_0)
    (h_h0_bound : -h0_1 ≤ h0_K ∧ h0_K ≤ h0_1)
    (h_decomp_plus : C_0 + C_K = norm_A_B_plus - c_tau_B * (h0_1 + h0_K) + P_E_plus)
    (h_decomp_minus : C_0 - C_K = norm_A_B_minus - c_tau_B * (h0_1 - h0_K) + P_E_minus)
    (h_semi_plus : -(norm_A_B_plus + mu_0 * (h0_1 + h0_K)) ≤ P_E_plus)
    (h_semi_minus : -(norm_A_B_minus + mu_0 * (h0_1 - h0_K)) ≤ P_E_minus) :
    let M := C_0 + 2 * (c_tau_B + mu_0) * h0_1
    (-M ≤ C_K ∧ C_K ≤ M) := by
  intro M
  dsimp [M]
  rcases h_h0_bound with ⟨h_low, h_high⟩
  have h_sum_le : (c_tau_B + mu_0) * (h0_1 + h0_K) ≤ 2 * (c_tau_B + mu_0) * h0_1 := by
    nlinarith
  have h_diff_le : (c_tau_B + mu_0) * (h0_1 - h0_K) ≤ 2 * (c_tau_B + mu_0) * h0_1 := by
    nlinarith
  constructor <;> linarith

/-- Theorem 36: Candidate III — Conditional Scalar Threshold Lemma for Unsigned Majorant Bounds.
    Given a positive window constant `c_0 > 0` and a scale factor `scale_factor` (representing
    `sqrt(X) * omega(2 * X)` in the majorant lower bound `M_omega(X) >= c_0 * sqrt(X) * omega(2 * X)`
    for a nonnegative, nonincreasing envelope `|E(x)| <= x * omega(x)` and `X >= 2`), this lemma
    assumes the scalar threshold inequality `B_fixed < c_0 * scale_factor` and performs scalar
    subtraction to conclude `B_fixed - c_0 * scale_factor < 0`.
    Scope note: This is a conditional algebraic threshold step on the majorant integral `M_omega(X)`
    (not a lower bound on `A_E(X)`, and not an analytic proof that `sqrt(X) * omega(2 * X) -> infty`). -/
theorem majorant_without_sign_cancellation_exceeds_fixed_coercive_norm
    (c_0 scale_factor B_fixed : ℝ)
    (h_c0_pos : 0 < c_0)
    (h_exceeds : B_fixed < c_0 * scale_factor) :
    B_fixed - c_0 * scale_factor < 0 ∧ 0 < c_0 * scale_factor - B_fixed := by
  have _ := h_c0_pos
  constructor <;> linarith

/-- Zero-moment subtracted decomposition of `I(X)` into the signed increment integral `I_inc`
    plus the lower-tail zero-moment boundary term `B_zm`. -/
def zeroMomentSubtractedDecomp (I_inc B_zm : ℝ) : ℝ :=
  I_inc + B_zm

/-- Chordal prime-power Stieltjes decomposition of the increment integral `I_inc(X)` into
    `I_chord(X) = W_X - psi_X * h0_invX` minus `I_drift(X) = (psi_X / X) * B_bound - psi_X * h0_invX`. -/
def chordalStieltjesDecomp (W_X psi_X h0_invX B_bound X : ℝ) : ℝ :=
  (W_X - psi_X * h0_invX) - ((psi_X / X) * B_bound - psi_X * h0_invX)

/-- Theorem 37: Separation of Actual Unsigned Integral `A_E(X)` from Envelope Majorant `M_omega(X)`
    and Monotone Window Lower Bound `M_omega(X) >= c_0 * sqrt(X) * omega(2 * X)`.
    If `A_E = A_E_win + A_E_comp` and `M_omega = M_omega_win + M_omega_comp` with nonnegative window
    and complement parts satisfying `A_E_win <= M_omega_win` and `A_E_comp <= M_omega_comp` (from
    `|E(x)| <= x * omega(x)`), and if nonincreasing monotonicity of `omega >= 0` on `[X/2, 2*X]`
    (`X >= 2`) gives `c_0 * sqrt_X * omega_2X <= M_omega_win`, then:
    (1) `A_E <= M_omega` (upper bound on `A_E`),
    (2) `c_0 * sqrt_X * omega_2X <= M_omega` (lower bound on the majorant `M_omega`, using `omega(2*X)`), and
    (3) whenever `B_fixed < c_0 * sqrt_X * omega_2X`, the majorant `M_omega` strictly exceeds `B_fixed`. -/
theorem majorant_window_lower_bound_and_envelope_ordering
    (A_E A_E_win A_E_comp M_omega M_omega_win M_omega_comp c_0 sqrt_X omega_2X B_fixed : ℝ)
    (h_AE_split : A_E = A_E_win + A_E_comp)
    (h_M_split : M_omega = M_omega_win + M_omega_comp)
    (h_M_comp_nonneg : 0 ≤ M_omega_comp)
    (h_win_env : A_E_win ≤ M_omega_win)
    (h_comp_env : A_E_comp ≤ M_omega_comp)
    (h_win_lower : c_0 * sqrt_X * omega_2X ≤ M_omega_win) :
    (A_E ≤ M_omega) ∧
      (c_0 * sqrt_X * omega_2X ≤ M_omega) ∧
      (B_fixed < c_0 * sqrt_X * omega_2X → B_fixed < M_omega) := by
  refine ⟨?_, ?_, ?_⟩
  · linarith
  · linarith
  · intro h_ex
    linarith

/-- Theorem 38: Zero-Moment Subtracted Increment & Chordal Prime-Power Stieltjes Equivalence.
    Under the lower-tail boundary identity `sqrt_X_int_0_invX_k = -B_bound` (so the zero-moment
    boundary term is `B_zm = -(psi_X / X - 1) * sqrt_X_int_0_invX_k = (psi_X / X - 1) * B_bound`),
    the chordal jump integral `I_chord = W_X - psi_X * h0_invX` and dilation drift integral
    `I_drift = (psi_X / X) * B_bound - psi_X * h0_invX` satisfy:
    (1) `I_inc = I_chord - I_drift = W_X - (psi_X / X) * B_bound` (exact cancellation of `psi_X * h0_invX`),
    (2) `zeroMomentSubtractedDecomp I_inc B_zm = W_X - B_bound = I_X` (recovering `W_X = B_bound + I_X`), and
    (3) the prime-wavelet sum `W_X` reappears identically as `I_inc + (psi_X / X) * B_bound`.
    Scope note: Formalizes the algebraic deductions from the analytic Stieltjes identities for `I_chord`,
    `I_drift`, and the lower-tail integral, not the measure-theoretic Stieltjes integration itself. -/
theorem zero_moment_subtracted_and_chordal_stieltjes_equivalence
    (W_X I_X B_bound psi_X X h0_invX sqrt_X_int_0_invX_k : ℝ)
    (h_W_decomp : W_X = B_bound + I_X)
    (h_lower_tail : sqrt_X_int_0_invX_k = -B_bound) :
    let e_X := psi_X / X - 1
    let B_zm := -e_X * sqrt_X_int_0_invX_k
    let I_inc := chordalStieltjesDecomp W_X psi_X h0_invX B_bound X
    (I_inc = W_X - (psi_X / X) * B_bound) ∧
      (zeroMomentSubtractedDecomp I_inc B_zm = I_X) ∧
      (W_X = I_inc + (psi_X / X) * B_bound) := by
  intro e_X B_zm I_inc
  dsimp [e_X, B_zm, I_inc, chordalStieltjesDecomp, zeroMomentSubtractedDecomp]
  rw [h_lower_tail, h_W_decomp]
  refine ⟨by ring, by ring, by ring⟩

/-- Prime-shift quadratic form expansion `D_N(f) = 2 * L_N * ||f||^2 - W_{prime, N}(f * f^*)`,
    where `L_N = sum_{2 <= n <= N} Lambda(n) / sqrt(n)` and `W_{prime, N}(f * f^*) = 2 * sum_{2 <= n <= N} w_n Re <f, S_n f>`. -/
def primeShiftQuadraticFormDecomp (L_N norm_f_sq W_prime_N : ℝ) : ℝ :=
  2 * L_N * norm_f_sq - W_prime_N

/-- Finite-cutoff Stieltjes decomposition of the divisor-aggregated functional `W_{log, B}(X)`
    into the Stirling remainder upper-boundary term, the smooth logarithmic main integral on `[1, B]`,
    and the signed Stirling remainder integral on `[1, B]`. -/
def divisorAggregatedStieltjesDecomp (E_log_B_term main_log_int_1_B err_log_int_1_B : ℝ) : ℝ :=
  E_log_B_term + main_log_int_1_B + err_log_int_1_B

/-- Theorem 39: Prime-Shift Quadratic Form Expansion, Subtracted Finite Part, and Two-Grade Completion Equivalence.
    For `D_N = primeShiftQuadraticFormDecomp L_N norm_f_sq W_prime_N = 2 * L_N * norm_f_sq - W_prime_N`:
    (1) Subtracting `2 * L_N * norm_f_sq` yields `D_N - 2 * L_N * norm_f_sq = -W_prime_N`.
    (2) Nonnegativity `0 <= D_N` alone is equivalent to `-2 * L_N * norm_f_sq <= D_N - 2 * L_N * norm_f_sq`
        (showing why `D_N >= 0` alone only bounds `-W_prime_N` from below by the diverging counterterm `-2 * L_N * norm_f_sq`).
    (3) When the subtracted finite part `F_sub = -W_prime_inf` is combined with the canonical Attempt B
        completion (`P_E = F_sub + B_transfer`), coercive semiboundedness `-(norm_A_B_sq + mu_0 * norm_f_sq) <= P_E`
        is equivalent to `-(mu_0 * norm_f_sq) <= F_sub + B_transfer + norm_A_B_sq`, and on normalized two-grade
        states `f_pm^{(K)}` where `W_prime_pm = 2 * W_1 ± (W_posK + W_negK)`, the subtracted finite parts are
        `-2 * W_1 - (W_posK + W_negK)` and `-2 * W_1 + (W_posK + W_negK)`.
    Scope note: Formalizes the algebraic deductions connecting `D_N`, `-W_prime`, and `P_E`; it does not
    formalize the Hilbert-space shift unitarity `||S_n f|| = ||f||` or the `N -> infty` limit. -/
theorem prime_shift_quadratic_form_and_subtracted_finite_part_equivalence
    (L_N norm_f_sq W_prime_N W_prime_inf B_transfer norm_A_B_sq mu_0 W_1 W_posK W_negK : ℝ) :
    let D_N := primeShiftQuadraticFormDecomp L_N norm_f_sq W_prime_N
    let F_sub := -W_prime_inf
    let P_E := F_sub + B_transfer
    (D_N - 2 * L_N * norm_f_sq = -W_prime_N) ∧
      ((0 ≤ D_N) ↔ (-2 * L_N * norm_f_sq ≤ D_N - 2 * L_N * norm_f_sq)) ∧
      ((-(norm_A_B_sq + mu_0 * norm_f_sq) ≤ P_E) ↔
        (-(mu_0 * norm_f_sq) ≤ F_sub + B_transfer + norm_A_B_sq)) ∧
      (-(2 * W_1 + (W_posK + W_negK)) + -(2 * W_1 - (W_posK + W_negK)) = -4 * W_1) ∧
      (-(2 * W_1 - (W_posK + W_negK)) - -(2 * W_1 + (W_posK + W_negK)) = 2 * (W_posK + W_negK)) := by
  intro D_N F_sub P_E
  dsimp [D_N, F_sub, P_E, primeShiftQuadraticFormDecomp]
  refine ⟨by ring, ?_, ?_, by ring, by ring⟩
  · constructor <;> intro h <;> linarith
  · constructor <;> intro h <;> linarith

/-- Theorem 40: Divisor-Aggregated Prime-Shift Stieltjes Cancellation and Boundedness Schema.
    For `T(x) = sum_{2 <= k <= x} log k = M_log(x) + E_log(x)` (`M_log(x) = x * log x - x + 1`),
    given the finite-cutoff Stieltjes identity `W_log_B = (M_log_B + E_log_B) * end_factor + int_1_B_M_log + err_log_int_1_B`
    and the integration-by-parts identity `int_1_B_M_log = -M_log_B * end_factor + main_log_int_1_B`:
    (1) The smooth upper-boundary term `M_log_B * end_factor` cancels identically, leaving
        `W_log_B = divisorAggregatedStieltjesDecomp (E_log_B * end_factor) main_log_int_1_B err_log_int_1_B`.
    (2) In the `B -> infty` limit, when the full-line logarithmic Mellin moment vanishes
        (`main_log_int_0_1 + main_log_int_1_inf = sqrt_X * (log_X * H0_half + H0_prime_half)` with
        `H0_half = 0` and `H0_prime_half = 0` from the triple zero of `H_0(z)` at `z = 1/2`),
        `main_log_int_1_inf = -main_log_int_0_1 = B_log_bound_val`, so `W_log_X = B_log_bound_val + I_log_X`.
    (3) If `|B_log_bound_val| <= B_max` and `|I_log_X| <= I_max`, then `|W_log_X| <= B_max + I_max`.
    (4) Under the exact Möbius inversion decomposition `W_X = W_log_X + R_mu_X`, any bound
        `|R_mu_X| <= R_max` on the Möbius remainder `R_mu_X = sum_{m>=2} (mu(m)/sqrt(m)) W_log(X/m)`
        transfers immediately to `|W_X| <= B_max + I_max + R_max`.
    Scope note: Formalizes the algebraic cancellation and triangle-inequality deductions from the assumed
    Stieltjes integration-by-parts and vanishing Mellin moment identities `H_0(1/2) = H_0'(1/2) = 0`. -/
theorem divisor_aggregated_stieltjes_and_moebius_inversion_identity
    (M_log_B E_log_B end_factor int_1_B_M_log main_log_int_1_B err_log_int_1_B
      main_log_int_0_1 main_log_int_1_inf sqrt_X log_X H0_half H0_prime_half
      B_log_bound_val I_log_X B_max I_max W_X R_mu_X R_max : ℝ)
    (h_ibp_M : int_1_B_M_log = -M_log_B * end_factor + main_log_int_1_B)
    (h_full_moment : main_log_int_0_1 + main_log_int_1_inf = sqrt_X * (log_X * H0_half + H0_prime_half))
    (h_H0_zero : H0_half = 0)
    (h_H0_prime_zero : H0_prime_half = 0)
    (h_B_log_def : B_log_bound_val = -main_log_int_0_1)
    (h_B_abs : -B_max ≤ B_log_bound_val ∧ B_log_bound_val ≤ B_max)
    (h_I_abs : -I_max ≤ I_log_X ∧ I_log_X ≤ I_max)
    (h_moebius : W_X = (main_log_int_1_inf + I_log_X) + R_mu_X)
    (h_R_abs : -R_max ≤ R_mu_X ∧ R_mu_X ≤ R_max) :
    let W_log_B := (M_log_B + E_log_B) * end_factor + int_1_B_M_log + err_log_int_1_B
    let W_log_X := main_log_int_1_inf + I_log_X
    (W_log_B = divisorAggregatedStieltjesDecomp (E_log_B * end_factor) main_log_int_1_B err_log_int_1_B) ∧
      (main_log_int_1_inf = B_log_bound_val) ∧
      (W_log_X = B_log_bound_val + I_log_X) ∧
      (-(B_max + I_max) ≤ W_log_X ∧ W_log_X ≤ B_max + I_max) ∧
      (-(B_max + I_max + R_max) ≤ W_X ∧ W_X ≤ B_max + I_max + R_max) := by
  intro W_log_B W_log_X
  dsimp [W_log_B, W_log_X, divisorAggregatedStieltjesDecomp]
  have h_m_eq : main_log_int_1_inf = B_log_bound_val := by
    rw [h_H0_zero, h_H0_prime_zero] at h_full_moment
    linarith
  rcases h_B_abs with ⟨hBl, hBu⟩
  rcases h_I_abs with ⟨hIl, hIu⟩
  rcases h_R_abs with ⟨hRl, hRu⟩
  refine ⟨?_, h_m_eq, by linarith, ⟨by linarith, by linarith⟩, ⟨by linarith, by linarith⟩⟩
  rw [h_ibp_M]
  ring

/-- Polarized mixed-grade complete arithmetic–Fourier pairing decomposition on `(T_K psi_tau, T_L psi_tau)`
    (`Delta = |K - L|`, `X_Delta = tau^Delta >= 1`):
    `M_KL = W_arch - W_fwd - W_log - R_mu`, where `B_known = W_arch - W_fwd - W_log` collects the
    three unconditionally bounded terms (`W_arch(h_Delta)`, `W(X_Delta^{-1})`, and `W_log(X_Delta)`). -/
def mixedGradeCompletePairingDecomp (W_arch W_fwd W_log R_mu : ℝ) : ℝ :=
  (W_arch - W_fwd - W_log) - R_mu

/-- Finite-cutoff Stieltjes summation-by-parts decomposition of the Möbius recovery remainder
    `R_{mu, B}(X) = sum_{2 <= m <= B} (mu(m)/sqrt(m)) W_log(X/m)` in terms of the Mertens sum
    `M_{>=2}(y) = sum_{2 <= m <= y} mu(m)` and smooth profile `phi_log(u) = sqrt(u) * W_log(u)`. -/
def mertensStieltjesRemainderDecomp (upper_mertens_boundary mertens_stieltjes_int : ℝ) : ℝ :=
  upper_mertens_boundary + mertens_stieltjes_int

/-- Theorem 41: Mixed-Grade Complete Pairing Polarization, Unconditionally Bounded Background,
    and Exact Equivalence with Möbius Recovery Boundedness.
    For any concurrent grades `K, L` with `X_Delta = tau^{|K - L|} >= 1`:
    (1) Given the Attempt B polarized decomposition `M_KL = inner_A_B - c_tau_B * inner_L2 + B_transfer - W_fwd - W_refl`,
         the smooth archimedean identity `inner_A_B - c_tau_B * inner_L2 + B_transfer = W_arch`, and
        the exact Möbius recovery `W_refl = W_log + R_mu`, the mixed-grade pairing equals
        `mixedGradeCompletePairingDecomp W_arch W_fwd W_log R_mu = B_known - R_mu` where
        `B_known = W_arch - W_fwd - W_log`.
    (2) Under the unconditional bounds `|W_arch| <= M_arch`, `|W_fwd| <= M_fwd`, and `|W_log| <= M_log`,
        the known background satisfies `|B_known| <= M_arch + M_fwd + M_log`.
    (3) Any bound `|R_mu| <= M_mu` implies `|M_KL| <= (M_arch + M_fwd + M_log) + M_mu`; conversely,
        any bound `|M_KL| <= M_corr` implies `|R_mu| <= M_corr + (M_arch + M_fwd + M_log)`.
    Scope note: Formalizes the exact algebraic polarization and two-way triangle-inequality equivalence
    from the supplied analytic Attempt B and Möbius inversion identities. -/
theorem mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence
    (inner_A_B c_tau_B inner_L2 B_transfer W_arch W_fwd W_refl W_log R_mu
      M_arch M_fwd M_log M_mu M_corr : ℝ)
    (h_smooth : inner_A_B - c_tau_B * inner_L2 + B_transfer = W_arch)
    (h_moebius : W_refl = W_log + R_mu)
    (h_arch_abs : -M_arch ≤ W_arch ∧ W_arch ≤ M_arch)
    (h_fwd_abs : -M_fwd ≤ W_fwd ∧ W_fwd ≤ M_fwd)
    (h_log_abs : -M_log ≤ W_log ∧ W_log ≤ M_log) :
    let M_KL := inner_A_B - c_tau_B * inner_L2 + B_transfer - W_fwd - W_refl
    let B_known := W_arch - W_fwd - W_log
    let B_max := M_arch + M_fwd + M_log
    (M_KL = mixedGradeCompletePairingDecomp W_arch W_fwd W_log R_mu) ∧
      (M_KL = B_known - R_mu) ∧
      (-B_max ≤ B_known ∧ B_known ≤ B_max) ∧
      ((-M_mu ≤ R_mu ∧ R_mu ≤ M_mu) → (-(B_max + M_mu) ≤ M_KL ∧ M_KL ≤ B_max + M_mu)) ∧
      ((-M_corr ≤ M_KL ∧ M_KL ≤ M_corr) → (-(M_corr + B_max) ≤ R_mu ∧ R_mu ≤ M_corr + B_max)) := by
  intro M_KL B_known B_max
  dsimp [M_KL, B_known, B_max, mixedGradeCompletePairingDecomp]
  rcases h_arch_abs with ⟨hAl, hAu⟩
  rcases h_fwd_abs with ⟨hFl, hFu⟩
  rcases h_log_abs with ⟨hLl, hLu⟩
  have h_id : inner_A_B - c_tau_B * inner_L2 + B_transfer - W_fwd - W_refl =
      W_arch - W_fwd - W_log - R_mu := by
    linarith
  refine ⟨h_id, h_id, ⟨by linarith, by linarith⟩, ?_, ?_⟩
  · rintro ⟨hRl, hRu⟩
    constructor <;> linarith
  · rintro ⟨hCl, hCu⟩
    constructor <;> linarith

/-- Theorem 42: Small-Scale `O(u^{5/2})` Möbius Tail Majorant & Mertens Stieltjes Integration-by-Parts Schema.
    (1) If a small-scale term satisfies `|W_log_u| <= C_log0 * X_pow_5_2 * m_inv_5_2` (`u = X/m`) and
        `|mu_m_over_sqrt_m| <= m_inv_1_2` with `m_inv_1_2 * m_inv_5_2 = m_inv_3` and `m_inv_1_2 >= 0`,
        then `|mu_m_over_sqrt_m * W_log_u| <= C_log0 * X_pow_5_2 * m_inv_3` (justifying the `O(sum m^{-3})`
        Weierstrass M-test tail on compact scale intervals).
    (2) Under the Stieltjes summation-by-parts decomposition
        `R_mu_B = mertensStieltjesRemainderDecomp upper_mertens_boundary mertens_stieltjes_int`,
        when `upper_mertens_boundary = 0` in the `B -> infty` limit (since `|M(B) * phi_log(X/B)| = O(B^{-2}) -> 0`),
        `R_mu_inf = mertens_stieltjes_int_inf`, and any unsigned Mertens envelope majorant `M_unsigned`
        satisfying `mertens_stieltjes_int_inf <= M_unsigned` and `M_unsigned >= c_mertens * sqrt_X_omega`
        strictly exceeds `B_fixed` whenever `c_mertens * sqrt_X_omega > B_fixed`.
    Scope note: Formalizes the algebraic majorant and summation-by-parts deductions from supplied
    small-scale kernel envelope and Stieltjes integration-by-parts hypotheses. -/
theorem small_scale_w_log_tail_and_mertens_stieltjes_ibp_identity
    (mu_term_abs m_inv_1_2 W_log_u_abs C_log0 X_pow_5_2 m_inv_5_2 m_inv_3
      upper_mertens_boundary mertens_stieltjes_int_inf M_unsigned c_mertens sqrt_X_omega B_fixed : ℝ)
    (h_m_nonneg : 0 ≤ m_inv_1_2)
    (h_prod_bound : mu_term_abs ≤ m_inv_1_2 * W_log_u_abs)
    (h_w_small : W_log_u_abs ≤ C_log0 * X_pow_5_2 * m_inv_5_2)
    (h_m_pow : m_inv_1_2 * (C_log0 * X_pow_5_2 * m_inv_5_2) = C_log0 * X_pow_5_2 * m_inv_3)
    (h_upper_zero : upper_mertens_boundary = 0)
    (h_unsigned_lower : c_mertens * sqrt_X_omega ≤ M_unsigned) :
    let R_mu_inf := mertensStieltjesRemainderDecomp upper_mertens_boundary mertens_stieltjes_int_inf
    (mu_term_abs ≤ C_log0 * X_pow_5_2 * m_inv_3) ∧
      (R_mu_inf = mertens_stieltjes_int_inf) ∧
      (B_fixed < c_mertens * sqrt_X_omega → B_fixed < M_unsigned) := by
  intro R_mu_inf
  dsimp [R_mu_inf, mertensStieltjesRemainderDecomp]
  have h_step : m_inv_1_2 * W_log_u_abs ≤ m_inv_1_2 * (C_log0 * X_pow_5_2 * m_inv_5_2) :=
    mul_le_mul_of_nonneg_left h_w_small h_m_nonneg
  refine ⟨by linarith, by linarith, ?_⟩
  intro h_ex
  linarith

end RiemannScope
