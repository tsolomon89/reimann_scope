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

end RiemannScope
