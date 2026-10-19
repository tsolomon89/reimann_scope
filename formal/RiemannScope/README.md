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

12. **`ModularThetaConductorCurvature.lean`** (2 `def` + 17 `theorem` declarations):
   - Heat-drift coefficient `heatDriftCoeff` ($4 - 2c$), exact Euler-to-heat scaling on $\Theta_t$ (`theta_heat_euler_scaling`), general drift expansion $\mathcal L_c\Theta_t = 4t^2\partial_t^2\Theta_t + (4-2c)t\partial_t\Theta_t$ (`heat_drift_operator_expansion`), and unique heat-drift compensator $c = 2$ ($\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$) (`heat_drift_compensator_unique`)
   - Modular weight-normalization involution $\widetilde f(1/t) = \widetilde f(t)$ (`modular_weight_normalization_involution`), self-dual vanishing $\nabla_w f(1) = 0$ (`modular_covariant_deriv_vanishes_at_self_dual`), exact operator difference $4\mathcal H_{\mathrm{mod},1} - \mathcal L_{\mathrm{heat}} = 8\mathcal D + 1 = 4\mathcal E + 1$ (`heat_and_modular_hessian_difference`), and incompatibility of joint modular Hessian and heat-drift axioms at second order (`heat_and_modular_hessian_incompatibility`)
   - Dilation–conductor commutator cancellation $[\mathcal A, A] + [\mathcal A, B] = 1 - 1 = 0 \implies [\mathcal A, \mathcal C] = 0$ (`dilation_conductor_commutator_cancellation`)
   - Prime-only drift-compensated variance identity $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t) = 4\pi^2 t^2(M_0 M_2 - M_1^2)$ and two-point nonnegativity (`covariant_prime_variance_identity`, `covariant_prime_variance_nonneg`)
   - No-contradiction firewall for nonnegative arithmetic and spectral signs (`arithmetic_sign_and_spectral_sign_no_contradiction`), conditional complement-sign contradiction (`complement_nonnegativity_contradiction`), and generic scale-base $q > 1$ homogeneity control (`generic_quadratic_heat_base_control`)
   - Pole-regularization repair (`TASK-TC-036R`): Mellin multiplier definition `poleRegMultiplier`, unshifted operator defect $\mathcal D(\mathcal D - 1/2) \mapsto s^2/4 - 1/16$ (`unshifted_regularizer_mellin_defect`), repaired pole-annihilator identity $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - 1/16 \mapsto \frac{1}{4}s(s-1) = \frac{1}{4}(z^2 - 1/4)$ (`corrected_pole_regularizer_mellin_identity`), annihilation of both quarter-power modes $t^{\pm 1/4}$ (`corrected_pole_regularizer_annihilates_quarter_powers`), and spatial polynomial jet $r^2 - \frac{3}{2}r$ vanishing at $u = 0$ (`corrected_pole_regularizer_spatial_jet`)
   - *Scope note:* Does not formalize Burnol's functional-analytic conductor domain $\mathcal S_0 / \Delta$, the complete Riemann–Weil explicit formula, Jacobi theta Poisson summation, global Weil positivity, trace-class/Sonin operator theory, or `OBL-CT-001A`.

13. **`GradeCharacterProjection.lean`** (5 `def` + 17 `theorem` declarations, `TASK-TC-037` / `TASK-TC-037R`):
   - Centered zero coordinate `centeredZeroCoord`, uncentered zero `uncenteredZero`, complex conjugation `complexConjCoord`, same-height reflection `centeredReflectionR`, and Klein-four zero-symmetry / involution identities $R^2 = I$ (`centered_zero_reflection_identity`)
   - Reflection-pair stationarity theorem $z_\rho + \bar z_\sigma = 0 \iff \sigma = 1 - \bar\rho$ and self-reflection characterization $\rho = 1 - \bar\rho \iff \delta_\rho = 0$ (`reflection_stationary_iff`)
   - Grade pair character modulus identity $\tau^{r\delta_1}\tau^{r\delta_2} = \tau^{r(\delta_1+\delta_2)}$ (`grade_pair_character_modulus`) and off-critical diagonal character nonunitarity $\tau^{2\delta_\rho} \ne 1 \iff \delta_\rho \ne 0$ (`offcritical_diagonal_character_nonunitary`)
   - Finite polynomial / Laurent projector root no-go over $\mathbb{R}[X]$ (`finite_polynomial_projector_root_no_go`) and $\mathbb{C}[X]$ (`finite_complex_polynomial_projector_root_no_go`), finite differential projector root no-go over $\mathbb{R}[X]$ (`finite_differential_projector_root_no_go`) and $\mathbb{C}[X]$ (`finite_complex_differential_projector_root_no_go`), and discrete Cesàro unit-character / bilateral nonunitary excess identity $q^N + q^{-N} - 2 = (q^N - 1)^2 / q^N > 0$ (`cesaro_unit_character_limit_control`)
   - Reflection quartet imaginary cancellation $P(z_\rho, -\bar z_\rho) + P(\bar z_\rho, -z_\rho) = 8\delta_\rho^2$ (`reflection_quartet_imaginary_cancellation`), corrected sesquilinear relative-grade exponent $(r - d)z_\rho + (r + d)\bar z_\sigma = -2d z_\rho = -2d\delta_\rho - 2id\gamma_\rho$ (`sesquilinear_relative_exponent_at_reflection`), and relative-grade second-derivative non-radial quartet sum $8(\log\tau)^2(\delta_\rho^2 - \gamma_\rho^2)$ (`relative_grade_second_derivative_not_radial`)
   - Inversion-even Mellin symmetrization algebra $\widehat{\Psi}^+(z) = \frac{1}{2}(M_z + M_{-z})$ and cancellation control (`inversion_even_mellin_symmetry_algebra`), together with reflection weight nonnegativity $8 m_\rho^2(u^2 + v^2)\delta_\rho^2 \ge 0$ (`reflection_quartet_radial_defect_nonneg`, `reflection_weight_nonnegative`)
   - Common-shift transport–projection incompatibility $(b - 1)r(s + t) = 0$ at $b = 1$ and scale-invariant ratio-kernel erasure on $s + t = 0$ (`transport_projection_incompatibility_algebra`), together with conditional contradiction vs. same-sign consistency firewall (`projected_arithmetic_zero_and_positive_radial_contradiction`)
   - *Scope note:* Does not formalize the Riemann–von Mangoldt zero-counting formula $N(T)$, simple critical-line zero density $N_0^*(T)$, infinite spectral series convergence, Følner/Cesàro convergence on the actual zeta spectrum, the global Weil explicit formula, or Weil positivity.

14. **`ZeroArithmeticInvariants.lean`** (12 `theorem` declarations, `TASK-TC-038` / `TASK-TC-038R`):
   - Shifted-ordinate rationality equivalence $\gamma \in \mathbb{Q} \iff \gamma + \frac{1}{2} \in \mathbb{Q}$ (`shifted_ordinate_rational_iff`), subfield/algebraicity equivalence $\gamma \in A \iff \gamma + \frac{1}{2} \in A$ (`half_mem_subfield`, `shifted_ordinate_algebraic_iff`), and transcendence (subfield-complement) equivalence $\gamma \notin A \iff \gamma + \frac{1}{2} \notin A$ (`shifted_ordinate_transcendental_iff`)
   - Full complex zero vs. real and imaginary part conjugation reconstruction $(\rho + \bar\rho)/2 = \beta$, $(\rho - \bar\rho)/(2i) = \gamma$, and RH-conditional subfield equivalence (`complex_zero_re_im_algebraicity`)
   - Functional-equation reflection reciprocal partial-fraction identity $\frac{1}{\rho(1-\rho)} = \frac{1}{\rho} + \frac{1}{1-\rho}$ and centered product $\rho(1-\rho) = \frac{1}{4} - z^2$ (`reflection_reciprocal_identity`)
   - Centered quartet monic polynomial identity $(X-z)(X+z)(X-\bar z)(X+\bar z) = X^4 - 2(\delta^2-\gamma^2)X^2 + (\delta^2+\gamma^2)^2$ (`centered_quartet_polynomial_identity`) and real symmetric coordinates $z^2+\bar z^2 = 2(\delta^2-\gamma^2)$, $z^2\bar z^2 = (\delta^2+\gamma^2)^2 \ge 0$ (`centered_quartet_coefficients_real`)
   - First Li coefficient finite algebraic identity $1 - (1 - 1/\rho)^1 = 1/\rho$ and reflection-pair sum $\frac{1}{\rho(1-\rho)}$ (`li_first_coefficient_finite_algebra_identity`), together with reciprocal-power log-derivative sign normalization and centered odd-power cancellation $z^{2k+1} + (-z)^{2k+1} = 0$ vs. even-power doubling (`reciprocal_power_log_derivative_sign_identity`)
   - Stieltjes notation disambiguation algebraic invariance (`stieltjes_notation_no_effect_algebra`) and equivalent closed forms for $S_2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}} = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi)$ with residual $\frac{3}{4}\gamma_E^2 - \gamma_E + 3\gamma_1^{\mathrm{St}}$ against the erroneous historical expression (`s2_equivalent_closed_forms`)
   - *Scope note:* Does not formalize the Hadamard factorization of $\xi(s)$, transcendence status of zeta zeros, Fauzan's 2026 $\zeta(5)$ irrationality proof (formalized externally in `mo271/Zeta5`), Bui–Conrey–Young zero density, Li's criterion, or Voros superzeta analytic continuation.

15. **`FauzanZeroArgumentTransfer.lean`** (23 `theorem` declarations, `TASK-TC-039` / `TASK-TC-039R` / `TASK-TC-039R3` / `TASK-TC-039R4`):
   - Real ordinate norm-polynomial product $(u+iv)(u-iv) = u^2+v^2$ and degree-1 evaluation at $\alpha(Y) = \frac{1}{4} + \frac{iY}{2}$ (`argument_norm_polynomial_real`), nonnegativity $C_n(u^2+v^2) \ge 0$ (`argument_norm_polynomial_nonneg`), and degree bound $\deg \mathcal{N}_P \le 2\deg P$ (`argument_norm_polynomial_degree_bound`)
   - Consecutive Newton approximant common-root reduction $N_{n+1}(z) = N_n(z) + c_{n+1}\binom{z}{n+1} \implies (N_n(z)=0 \wedge N_{n+1}(z)=0 \implies \binom{z}{n+1}=0)$ (`newton_consecutive_common_root_forces_node`), no-common-root theorem from nonzero node samples $a_m \ne 0$ (`newton_consecutive_no_common_root_of_nonzero_samples`), and two-approximant strict positivity $G_n(Y) = C_n(|N_n(\alpha(Y))|^2 + |N_{n+1}(\alpha(Y))|^2) > 0$ (`two_approximant_norm_sum_strict_pos`)
   - Rational evaluation integer-clearing lower bound $|P_n(a/b)| \ge b^{-d_n}$ (`rational_evaluation_integer_clearing`), superlinear logarithmic smallness Diophantine contradiction schema (`superlinear_log_smallness_irrationality_schema`), and multipoint Padé zero-residual identity $A_n(\alpha) - \mathcal{R}(\alpha)B_n(\alpha) = A_n(\alpha)$ at $\mathcal{R}(\alpha) = 0$ (`pade_interpolation_zero_residual_identity`)
   - $\pi \leftrightarrow \tau$ zero-carrying normalization and rational gauge algebra (`TASK-TC-039R`): $\mathcal{R}_\pi(z) = 4^z \mathcal{R}_\tau(z)$ and zero equivalence (`pi_tau_zero_function_scaling`), integer sample scaling $a_m^{(\pi)} = 4^m a_m^{(\tau)}$ (`pi_tau_integer_sample_scaling`), Euler even-zeta $\tau$-rational core identity $2^{2m}\frac{B_{2m}}{2(2m)!} = \frac{2^{2m-1}B_{2m}}{(2m)!}$ (`tau_even_zeta_rational_core_identity`), positive moment scaling $b_m^{(c)} = c^{m+1}b_m^{(\tau)}$ and $b_m^{(\pi)} = 4^{m+1}b_m^{(\tau)}$ (`moment_pi_tau_scaling`), Hankel determinant gauge-scaling exponent $n(n-1) + n = n^2$ (`hankel_gauge_scaling_exponent`), rational gauge zero-divisor invariance $c^z\mathcal{R}_\tau(z) = 0 \iff \mathcal{R}_\tau(z) = 0$ (`rational_gauge_zero_divisor_invariant`), two-phase cosine-square lower bound $\sin^2(\theta_2-\theta_1) \le 2(\cos^2\theta_1+\cos^2\theta_2)$ and consecutive difference lower bound $3(|N_n|^2+|N_{n+1}|^2) \ge |N_n|^2+|N_{n+1}-N_n|^2$ (`two_phase_cosine_square_lower_bound`), and fixed-gauge Newton degree invariance (`fixed_gauge_degree_invariance`)
   - Removable singularity at $z=1/2$, vertical-line saddle concavity, and $+\pi/3$ phase-displacement sum-of-squares (`TASK-TC-039R3`): $\mathcal{R}_\tau(1/2) = 1/\tau = 1/(2\pi)$ and $\mathcal{R}_\pi(1/2) = 2\mathcal{R}_\tau(1/2) = 1/\pi$ (`tau_removable_singularity_half_scaling`), global vertical-line saddle concavity $\operatorname{Re}\Phi_n(x_n+iy) = -6nx_n^2 - \frac{n(y^2-3x_n^2)^2}{x_n^2+y^2} \le -6nx_n^2$ (`vertical_line_saddle_real_concavity_identity`), cubic stationary-phase expansion $\operatorname{Im}\Phi_n(x_n+iy) = 6s_3 nx_n^2 + \frac{2nx_n(y-s_3 x_n)^3}{x_n^2+y^2}$ (`vertical_line_saddle_imag_cubic_identity`), and exact $+\pi/3$ phase-displacement sum of squares $\cos^2\theta + \cos^2(\theta + \pi/3) = \frac{1}{2} + (\frac{\sqrt{3}}{2}\cos\theta - \frac{1}{2}\sin\theta)^2 \ge \frac{1}{2}$ (`phase_displacement_pi_over_three_sum_sq_lower_bound`)
   - Primitive integer norm-polynomial multiplier lower bound and leading-coefficient cancellation (`TASK-TC-039R4`): primitive multiplier lower bound $M_n = L_n/g_n \ge 1/q_{\mathrm{lead}} = 4^{n+1}((n+1)!)^2 / (\Delta^{n+1}a_0)^2$ (`primitive_multiplier_lower_bound_from_leading_coeff`) and exact leading-coefficient cancellation $\widetilde{Q}_n(\gamma_1) = M_n(|N_n(\alpha_1)|^2 + |N_{n+1}(\alpha_1)|^2) \ge \frac{1}{2}\prod_{j=0}^n ((2j-\frac{1}{2})^2 + \gamma_1^2)$ (`primitive_two_approximant_norm_cancellation_lower_bound`)
   - *Scope note:* Formalizes the exact algebraic concavity, cubic stationary-phase, $+\pi/3$ phase-displacement, and primitive integer norm-polynomial leading-coefficient cancellation identities underlying the vertical-line steepest-descent proof; does not formalize complex contour integration, upper incomplete Gamma analytic continuation, Padé asymptotic error, Hankel potential theory, Barnes $G$-function asymptotics, or irrationality of $\gamma_1$.

16. **`SubfactorialZeroKernel.lean`** (8 `theorem` declarations, `TASK-TC-040`):
   - Bernoulli reflected kernel linear relation $\mathcal{B}(z) = 2\Gamma(2z+1)\mathcal{R}_\tau(z) = (2z-1)\Gamma(2z+1)\tau^{-2z}\zeta(2z)$ (`bernoulli_kernel_linear_relation`) and exact vanishing at half-zeros $\mathcal{R}_\tau(\alpha) = 0 \implies \mathcal{B}(\alpha) = 0$ (`bernoulli_kernel_zero_at_zeta_zero`)
   - Exact integer sample clearing $2(2m)!\mathcal{R}_\tau(m) = (-1)^{m+1}(2m-1)B_{2m}$ (`gamma_reflection_sample_clearing_identity`) and sign-adjusted positive sample identity $(-1)^{m+1}B_{2m} > 0 \wedge 2m-1 > 0 \implies (-1)^{m+1}(2m-1)B_{2m} > 0$ (`sign_adjusted_bernoulli_positive_sample_identity`)
   - Gamma-ratio log-factorial budget conservation $(2 - q) + q = 2$ across sample denominator vs. sample growth (`gamma_ratio_budget_conservation_identity`) and 3-term sample + Newton-basis total cost conservation $(2 - q) + q + 1 = 3$ (`gamma_ratio_newton_basis_total_cost_conservation`)
   - Auxiliary polynomial factorial cost lower bound schema $D_n |P_n(\gamma_1)| < 1 \wedge \log|P_n(\gamma_1)| \ge c_1 n \log n \implies \log D_n > -c_1 n \log n$ (`auxiliary_polynomial_factorial_cost_lower_bound_schema`)
   - Carlitz–Touchard Hankel orthogonal-polynomial recurrence coefficient positivity $\beta_k = \frac{k^4}{4(2k-1)(2k+1)} > 0$ and 4-step Hankel multiplier growth $\prod \beta_k > 0$ (`carlitz_touchard_hankel_recurrence_positivity`)
   - *Scope note:* Formalizes the exact algebraic identities of the Bernoulli reflection kernel, the Gamma-ratio log-factorial conservation law, the auxiliary polynomial factorial cost lower-bound schema, and the Carlitz–Touchard positive-moment Hankel recurrence coefficients; does not formalize the analytic functional equation of $\zeta(s)$, Stirling's asymptotic expansion, Hadamard factorization, Carlitz–Touchard hypergeometric integral identity, or irrationality/transcendence of $\gamma_1$.
