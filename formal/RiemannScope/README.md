# Riemann Scope Lean 4 Formal Proof Scaffold

This directory houses the formal Lean 4 verification layer for `reimann_scope` conforming to [LEAN_FORMALIZATION_PLAN.md](file:///C:/Development/Projects/reimann_scope/docs/LEAN_FORMALIZATION_PLAN.md).

## Module Structure

1. **`Basic.lean`**:
   - Generic origin coordinate dilation $T_A(s) = As$
   - Centered coordinate dilation $C_A(s) = 1/2 + A(s - 1/2)$
   - Preservation/shifting of the critical line $\Re(s) = 1/2$

2. **`Grade.lean`**:
   - Canonical $\tau = 2\pi$ definition
   - Continuous and integer grade scale maps $a(k) = \tau^k$
   - Bilateral integer scale inverse identity $A_K A_{-K} = 1$

3. **`TranscendentalContinuation.lean`**:
   - Generic coordinate continuation family $F_\tau(s, k) = f(\tau^{-k} s)$
   - Exact coordinate covariance theorem $F_\tau(\tau^k u, k) = f(u)$

4. **`ZeroWorldline.lean`**:
   - Zero worldline trajectory $W_\rho(k) = \tau^k \rho$
   - Worldline root property $F_\tau(W_\rho(k), k) = 0$

5. **`RadialLeaf.lean`**:
   - Critical surface coordinate $\sigma_c(k) = \tau^k / 2$
   - Normalized radial leaf coordinate $R_\tau(s, k) = \tau^{-k} \Re(s) - 1/2$
   - Invariance theorem $R_\tau(W_\rho(k), k) = \delta$ identically for all $k$
   - Characterization of on-line zeros ($\delta = 0 \iff W_\rho(k) \in \sigma_c(k)$)

6. **`ZeroCharacter.lean`**:
   - Generic-base character generator $q_b(s) = \exp((s - 1/2) \log b)$
   - Character modulus theorem $|q_b(\rho)| = b^\delta$

7. **`SymmetricDefect.lean`**:
   - Symmetric grade defect $D_K = q_+^K + q_-^K - 2q_0^K$
   - Identical vanishing for on-line zeros ($\delta = 0 \implies D_K = 0$)

8. **`Contradiction.lean`**:
   - Radial displacement coordinate $\delta(s) = \Re(s) - 1/2$
   - Functional equation reflection theorem $\delta(1 - s) = -\delta(s)$
   - Conditional reflection theorem: reflection closure + radial rigidity ($\forall s \in S, \delta(s) = \delta_0$) forces $\delta_0 = 0$ and $\Re(s) = 1/2$ for all $s \in S$
   - Deductive contradiction corollary forbidding off-line zeros under radial rigidity

9. **`GradeHankelConstraint.lean`**:
   - Three-grade Hankel determinant $\mathcal{H}_0 = \mathcal{M}_{-1}\mathcal{M}_1 - \mathcal{M}_0^2$
   - Geometric sequence rank-one vanishing ($\mathcal{M}_K = Ac^K \implies \mathcal{H}_0 = 0$)
   - Two-point moment algebraic identity $\mathcal{H}_0 = w_1 w_2 (r_1 - r_2)^2 / (r_1 r_2)$
   - Strict positivity $\mathcal{H}_0 > 0$ for positive weights and distinct support points
   - Reciprocal pair strict positivity under off-critical reflection ($r_1 \ne 1 \implies \mathcal{H}_0 > 0$)
   - Contradiction theorem between arithmetic rank-one law and strict moment positivity
   - Transported-kernel Mellin scaling algebra: exponent $aK + (b - 1)K(s + t)$
   - Full-transport spectral factor cancellation: $b = 1 \implies (1 - 1)K(s + t) = 0$
   - Signed-weight countermodel: signed weights can yield $\mathcal{H}_0 < 0$
   - Generic-base scale covariance control: $(1 - 1)K = 0$ holds for all $q > 0$

10. **`TransportMismatchCurvature.lean`** (1 `def` + 17 `theorem` declarations):
   - Curvature determinant `curvatureDet` ($A_0 A_2 - A_1^2$) and single-exponential vanishing (`single_exponential_log_curvature_zero`)
   - Two-point and three-point positive exponential mixture Lagrange identities and nonnegativity/positivity (`two_exponential_curvature_identity`, `two_exponential_positive_log_curvature`, `positive_finite_exponential_curvature_nonneg`, `three_exponential_curvature_identity`, `three_exponential_curvature_nonneg`, `reciprocal_pair_curvature_strict_pos`)
   - Algebraic moment flatness under Euler-homogeneity relations $A_1 = d A_0, A_2 = d^2 A_0 \implies \mathfrak{C}_{\mathrm{arith}} = 0$ (`homogeneous_arithmetic_curvature_zero`) and contradiction with positive spectral curvature (`arithmetic_zero_curvature_and_spectral_positive_contradiction`)
   - Euler scaling derivative factorization and grade-$K$ cancellation (`euler_generator_scaling_algebra`, `mismatch_curvature_k_independent`)
   - Even second-difference quadratic identity (`even_second_difference_quadratic_ident`), centered conjugate ($2\delta$) vs. reflection ($0$ real part) pairing algebra (`centered_conjugate_pairing_radial`, `centered_reflection_pairing_real_zero`), and Mellin mismatch net exponent (`mellin_mismatch_net_exponent`)
   - Signed-weight countermodel (`signed_weight_curvature_negative`) and generic-base scale covariance control (`generic_base_mismatch_curvature_scaling`)
   - *Scope note:* Does not formalize the compact-support Euler-PDE homogeneity no-go (`PROVED_PAPER_DERIVATION`), the full two-variable explicit formula, the theta–Mellin regularized descent, global spectral positivity, or `OBL-CT-001A`.

11. **`CanonicalSelectorAudit.lean`** (1 `def` + 15 `theorem` declarations):
   - 1D Euler curvature determinant `oneDimCurvature` ($m_0 m_2 - m_1^2$) and separable tensor-square moment/curvature reduction $A_0 = m_0^2$, $A_1 = 2 m_0 m_1$, $A_2 = 2 m_0 m_2 + 2 m_1^2 \implies \mathfrak{C}_{\mathrm{arith}}(f \otimes f) = 2 m_0^2(m_0 m_2 - m_1^2)$ (`tensor_square_moment_A0`, `tensor_square_moment_A1`, `tensor_square_moment_A2`, `tensor_square_curvature_reduction`, `tensor_square_curvature_pos_iff`, `tensor_square_curvature_neg_iff`)
   - Additive-to-multiplicative Euler chain-rule drift identity for Jacobi theta / heat kernels $\Theta_t(x,y) = e^{-\pi t(x^2+y^2)}$: $\mathfrak{C}_{\mathrm{arith}}(\Theta_t) = c^2(M_0 M_2 - M_1^2) - 2c M_0 M_1$ (`euler_chain_rule_second_deriv_curvature`, `euler_drift_strictly_negative_of_dominant`, `single_station_theta_gaussian_curvature_neg`)
   - Multiplicative log-Gaussian curvature variance-vs-concavity identity $\mathfrak{C}_{\mathrm{arith}}(\Phi_{\alpha, w_0}) = 16\alpha^2(S_0 S_2 - S_1^2) - 8\alpha S_0^2$ and critical variance width threshold (`log_gaussian_curvature_identity`, `log_gaussian_curvature_neg_of_subcritical_variance`, `log_gaussian_critical_width_zero`)
   - Canonical Selector Trilemma conditional algebraic dichotomy (`selector_trilemma_algebraic_dichotomy`, `selector_trilemma_contradiction_of_nonneg_complement`)
   - *Scope note:* Does not formalize Hamburger's uniqueness theorem, Burnol's co-Poisson dictionary, Nyman–Beurling $L^2$ completeness, Connes–Consani's semi-local trace formula, or `OBL-CT-001A`.

12. **`ModularThetaConductorCurvature.lean`** (1 `def` + 13 `theorem` declarations):
   - Heat-drift coefficient `heatDriftCoeff` ($4 - 2c$), exact Euler-to-heat scaling on $\Theta_t$ (`theta_heat_euler_scaling`), general drift expansion $\mathcal L_c\Theta_t = 4t^2\partial_t^2\Theta_t + (4-2c)t\partial_t\Theta_t$ (`heat_drift_operator_expansion`), and unique heat-drift compensator $c = 2$ ($\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$) (`heat_drift_compensator_unique`)
   - Modular weight-normalization involution $\widetilde f(1/t) = \widetilde f(t)$ (`modular_weight_normalization_involution`), self-dual vanishing $\nabla_w f(1) = 0$ (`modular_covariant_deriv_vanishes_at_self_dual`), exact operator difference $4\mathcal H_{\mathrm{mod},1} - \mathcal L_{\mathrm{heat}} = 8\mathcal D + 1 = 4\mathcal E + 1$ (`heat_and_modular_hessian_difference`), and incompatibility of joint modular Hessian and heat-drift axioms at second order (`heat_and_modular_hessian_incompatibility`)
   - Dilation–conductor commutator cancellation $[\mathcal A, A] + [\mathcal A, B] = 1 - 1 = 0 \implies [\mathcal A, \mathcal C] = 0$ (`dilation_conductor_commutator_cancellation`)
   - Prime-only drift-compensated variance identity $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t) = 4\pi^2 t^2(M_0 M_2 - M_1^2)$ and two-point nonnegativity (`covariant_prime_variance_identity`, `covariant_prime_variance_nonneg`)
   - No-contradiction firewall for nonnegative arithmetic and spectral signs (`arithmetic_sign_and_spectral_sign_no_contradiction`), conditional complement-sign contradiction (`complement_nonnegativity_contradiction`), and generic scale-base $q > 1$ homogeneity control (`generic_quadratic_heat_base_control`)
   - *Scope note:* Does not formalize Burnol's functional-analytic conductor domain $\mathcal S_0 / \Delta$, the complete Riemann–Weil explicit formula, Jacobi theta Poisson summation, global Weil positivity, trace-class/Sonin operator theory, or `OBL-CT-001A`.

