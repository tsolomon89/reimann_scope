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


