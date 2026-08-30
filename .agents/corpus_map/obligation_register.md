# Mathematical Obligation and Test Vector Register

This register details all unresolved proof obligations, mandatory deterministic test vectors, and falsification test standards required by the research harness.

## 1. Mandatory Contract Test Vectors (from `MATH_CONTRACT.md` §13)

| Vector ID | Name | Mathematical Parameters | Expected Symbolic / Numerical Output | Test Harness Module |
| :--- | :--- | :--- | :--- | :--- |
| `VEC-A` | Identity Transform | $K = 0$ | All scale factors equal $1$; $\Re(s') = 1/2$; $\rho' = \rho$. | `test_contract_identities.py::test_vector_a_identity` |
| `VEC-B` | Origin Dilation | $K = 1, \tau = 2\pi$ | $\Re(s') = \tau/2 = \pi$; Zero map $\rho' = \tau\rho$. | `test_contract_identities.py::test_vector_b_origin_dilation` |
| `VEC-C` | Centered Dilation | $K = 1, \tau = 2\pi$ | $\Re(s') = 1/2$; Zero map $\rho' = 1/2 + \tau(\rho - 1/2)$. | `test_contract_identities.py::test_vector_c_centered_dilation` |
| `VEC-D` | Inverse Kernel Lock | $A = 2, B = 1/2, C = D = 0$ | $AB = 1$; $\mathcal{Z}_{2,0,1/2,0}(s) = \zeta(s)$ identically. | `test_contract_identities.py::test_vector_d_inverse_kernel_lock` |
| `VEC-E` | Radial Centrifuge | $\delta = 10^{-4}, K = 100, \tau = 2\pi$ | $\log\|q_\rho^K\| = 0.01 \log\tau$; $\|q_\rho^K\| = \tau^{0.01}$. | `test_contract_identities.py::test_vector_e_radial_centrifuge` |
| `VEC-F` | On-Line Centrifuge | $\delta = 0, \forall K \in \mathbb{R}$ | $\|q_\rho^K\| = 1$; $\log\|q_\rho^K\| = 0$; $\frac{d}{dK}\log\|q_\rho^K\| = 0$. | `test_contract_identities.py::test_vector_f_online_centrifuge` |

---

## 2. Core Mathematical Trust Obligations (from `SPEC.md` §12)

| Obligation ID | Property | Mathematical Definition | Verification Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| `OBL-001` | Generic $\zeta(s)$ Evaluation | High-precision certified evaluation across complex plane | Arb/Flint ball enclosure | `Verified in Harness` |
| `OBL-002` | Schwarz Reflection Symmetry | $\zeta(\bar s) = \overline{\zeta(s)}$ | Exact SymPy + Arb ball check at generic non-real $s$ | `Verified in Harness` |
| `OBL-003` | Functional Equation | $\xi(s) = \xi(1-s)$ where $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ | Arbitrary precision error bound $|\xi(s) - \xi(1-s)| < 10^{-50}$ | `Verified in Harness` |
| `OBL-004` | Baseline Zero Discovery | Independent root bracket & refinement on $\Re(s)=1/2$ | Hardy $Z(t)$ sign change scanning + Newton/Arb solver | `Specified in Harness` |
| `OBL-005` | Zero Residual Guarantee | Enclosure of discovered roots $\gamma_n$ with $|\zeta(1/2+i\gamma_n)| < \varepsilon$ | Certified Arb evaluation at root | `Specified in Harness` |
| `OBL-006` | Explicit Formula Truncation | Prime reconstruction $J_N(x)$ and $\pi_N(x)$ convergence | Möbius inversion unit tests against known prime sieve | `Specified in Harness` |
| `OBL-007` | Single Zero Perturbation Response | Exact differential update $\Delta C_n(x) = C(x, \rho'_n) - C(x, \rho_n)$ | Unit test comparing delta update to full recomputation | `Specified in Harness` |
| `OBL-008` | Centrifuge Derivative Invariant | $\frac{d}{dK} \log \|q_\rho^K\| = \delta \log \tau$ | Exact symbolic derivation & numerical gradient test | `Verified in Harness` |
| `OBL-EF-003` | Projection Trap Resolution (Linear 1-Point Statistics) | Independent arithmetic representation of $\mathcal P_0(\mathcal D_\zeta)$ via direct linear 1-point test functions | No-go theorem: CLOSED for fixed linear combinations and locally uniform limits of direct 1-point holomorphic statistics over open displacement family (Cauchy-Riemann on $2\Re G(\delta+i\gamma)$) | `CLOSED (NO-GO FOR LINEAR 1-POINT)` |
| `OBL-RDQ-001` | Nonlinear Paired / Relative Trace Realization | Derive divisor-independent arithmetic realization of relative trace $\operatorname{Tr}\mathcal R = \sum \kappa_1(\lambda, \lambda^\#)$ or Fredholm determinant $\det_{\mathrm F}(I+\mathcal R) = L_Q^{-1}$ without evaluating $\mathcal P_0(\mathcal D_\zeta)$ | Divisor-independent reflection pairing kernel evaluation | `OPEN OBLIGATION` |
| `OBL-ARB-D1` | Divisor-Independent Determinant Arithmetic Definition | Construct arithmetic evaluator $\mathfrak A_{K,D}^{\mathrm{arith}}$ from prime powers and archimedean factors without zero inputs | Epistemic firewall verification | `OPEN` |
| `OBL-ARB-D2` | Exact Determinant Bridge Identity | Prove $\mathfrak A_{K,D}^{\mathrm{arith}} = D = \sum 2n_j \log(1+r_j)$ | Exact arithmetic/spectral derivation | `OPEN` |
| `OBL-ARB-D3` | Independent Determinant Arithmetic Anchor | Prove $\mathfrak A_{K,D}^{\mathrm{arith}} = 0$ or $\lim_{K\to+\infty}\mathfrak A_{K,D}^{\mathrm{arith}} = 0$ | Independent arithmetic evaluation | `OPEN` |
| `OBL-ARB-D4` | Determinant Defect Rigidity | Prove $D = 0 \implies \forall j, r_j = 0$ ($r_j \ge 0$) | Lean 4 `list_sum_nonneg_eq_zero_iff` | `FORMALLY_PROVED` |
| `OBL-ARB-T1` | Divisor-Independent Trace Arithmetic Definition | Construct arithmetic evaluator $\mathfrak A_{K,T}^{\mathrm{arith}}$ from prime powers and archimedean factors without zero inputs | Epistemic firewall verification | `OPEN` |
| `OBL-ARB-T2` | Exact Trace Bridge Identity | Prove $\mathfrak A_{K,T}^{\mathrm{arith}} = T = \sum 2n_j r_j$ | Exact arithmetic/spectral derivation | `OPEN` |
| `OBL-ARB-T3` | Independent Trace Arithmetic Anchor | Prove $\mathfrak A_{K,T}^{\mathrm{arith}} = 0$ or $\lim_{K\to+\infty}\mathfrak A_{K,T}^{\mathrm{arith}} = 0$ | Independent arithmetic evaluation | `OPEN` |
| `OBL-ARB-T4` | Trace Defect Rigidity | Prove $T = 0 \implies \forall j, r_j = 0$ ($r_j \ge 0$) | Lean 4 `list_sum_nonneg_eq_zero_iff` | `FORMALLY_PROVED` |
| `OBL-ARB-SS1` | Separated Signal Arithmetic Construction | Construct divisor-independent arithmetic signal $S_K(x, t)$ | Epistemic firewall verification | `OPEN` |
| `OBL-ARB-SS2` | Exact Radial/Frequency Separation | Prove spectral term separates into $a_K(\gamma) e^{x\delta} e^{it\gamma}$ | Direct 1-point realization closed; nonlinear sesquilinear open | `SCOPED STATUS` |
| `OBL-ARB-SS3` | Arbitrary Finite Radial Curvature Identity | Prove $\sum_{i,j=1}^N (d_i+d_j)^2 = 2N\sum d_i^2 + 2(\sum d_i)^2$ for arbitrary real lists, reducing to $2N\sum d_i^2$ under $\sum d_i = 0$ | Lean 4 `list_pairs_sq_sum_eq`, `list_pairs_sq_sum_symmetric`, `list_pairs_sq_sum_nonneg`, `list_pairs_sq_sum_eq_zero_iff` | `FORMALLY_PROVED` |
| `OBL-ARB-SS4` | Separated Signal Curvature Rigidity | Prove $M_K''(0) = 0 \implies \forall \lambda, \delta_\lambda = 0$ | Lean 4 `ConditionalSeparatedSignalBridge.all_variances_zero` | `FORMALLY_PROVED` |
| `OBL-CMSA-001` | Completed Log-Derivative Pointwise Decomposition | Prove $P(u) = A(u) - \Xi'/\Xi(u-1/2)$ on $\Re(u) > 1$ | Analytic derivation; Lean 4 premise `ConditionalCompletedLogDerivativeDecomposition` | `PROVED / EXACT` |
| `OBL-CMSA-003` | Spectral Resolvent Mean-Square Regularization (Gate G4) | Gate G4 is the earliest open gate in the present CMSA derivation: regularize translation-average integral on $L^2$ zero resolvents; raw finite Fejér response and additive scalar class classified as `FAIL_RADIAL_POSITIVITY`; recomputed remainder and fixed finite perturbation classified as `FAIL_LIMIT_ORDER_DEPENDENCE`; subcritical norm condition $\|\Delta_T\| = o(\sqrt{T}) \implies V_T \to 0$ proved (`CLM-CMSA-025`); full infinite growing perturbation $\Delta_{H(T)}$ classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` | Analysis / Regularization barrier (Gate G4) | `OPEN (GATE G4)` |
| `OBL-CMSA-003-G4-BOUNDARY` | Non-Additive Cofinal Boundary Functional Construction | Construct an operator $\mathcal R_{\mathrm{op}}$ measuring noncommutation defect $\mathcal D = \mathcal R_{\mathrm{op}}(Z_\infty) - \lim_{H\to\infty} \mathcal R_{\mathrm{op}}(Z_H)$ for growing perturbations $\Delta_{H(T)}$ satisfying all 12 criteria (finite truncation, complete object, window normalization, relative trace/pairing, limit order, schedule $H(T)$, remainder bound, unequal-height pairs, reflection partners, arithmetic evaluation, grade covariance, algebraic non-collapse) | Mathematical definition & proof | `OPEN (GATE G4)` |
| `OBL-CMSA-003-G4-COFINAL-ESTIMATE` | Live Cofinal Growth and Cross-Term Asymptotic Evaluation | Determine the asymptotic behavior and sign bounds of $E_T = \|\Delta_{H(T)}\|^2/(2T)$ and $C_T = (1/T)\Re\langle P_\sigma, \Delta_{H(T)}\rangle$ for growing zero perturbation families along grade-covariant schedules $H(T) = cT$, testing whether supercritical norm growth $\|\Delta_{H(T)}\| \ge c\sqrt{T}$ produces a strictly positive normalized response $V_T = E_T - C_T > 0$ without cross-term cancellation | Asymptotic analysis & off-diagonal kernel integration | `OPEN (GATE G4)` |




| `OBL-CMSA-004` | Universal Scale Dilation Invariance & Coordinate Redundancy | Prove $s D_s(su) = f(u)$ for all $s > 0$ and coordinate redundancy of $\tau^K D_K^\xi(\tau^K u) = \xi'/\xi(u)$ across grades | Lean 4 `generic_scale_dilation_cancellation`, `coordinate_redundant` | `PROVED / FORMALLY_PROVED` |
| `OBL-CMSA-005` | Complete Finite Spectral Expansion Closure | Prove algebraic decomposition $S_{N,T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}$ and verify closed-form kernels $J_T, K_T$ | Arbitrary-precision verification in `math_core.py` ($< 10^{-15}$) | `PROVED / VERIFIED` |
| `OBL-ARB-STRUCT-SUM` | Infinite Trace/Determinant Summability | Prove $\sum n_j \delta_j^2/\gamma_j^2 < \infty$ under Hadamard order 1 | Analytic Dirichlet series bound | `PROVED` |
| `OBL-ARB-STRUCT-PAIR` | Involution Pair Isolation | Isolate reflection pairs $(\lambda, \lambda^\#)$ without unrestricted all-pairs cross-term contamination | Candidate B-D falsification analysis | `OPEN` |
| `OBL-ARB-STRUCT-NONRED` | Grade Non-Redundancy | Verify that cross-grade arithmetic pairings are not coordinate pullbacks | Single grades coordinate-redundant (PROVED); cross-grade nonredundancy for $2\pi$ OPEN | `SCOPED STATUS` |
| `OBL-ARB-STRUCT-UNIF` | Grade-Limit Uniformity | Prove limit uniformity and exclude raw coordinate compression | Classical asymptotic analysis | `PROVED` |
| `OBL-ARB-STRUCT-RH` | Radial Defect to RH Connection | Prove $\forall j, \delta_j = 0 \implies \mathrm{RH}$ predicate | Lean 4 `radial_rigidity_offline_zero_contradiction` | `FORMALLY_PROVED` |
| `OBL-RADIAL-DEFECT-DESCENT` | Master Radial-Defect Descent Obligation | Derive an exact, zero-independent arithmetic evaluator for a nonnegative radial-defect invariant ($D = -\log L_Q$, $T = \operatorname{Tr}\mathcal R$, $\sum W_\rho \delta_\rho^2$, or $N_\xi - C_\xi$) without circular reliance on zero data or assuming RH equivalences | Epistemic firewall verification across all 4 candidate routes (RDQ, CT, WH, CMSA) | `ACTIVE MASTER OBLIGATION` |
| `OBL-CT-001A` | Non-Scalar Arithmetic Functional Construction | Construct a zero-independent, non-scalar arithmetic functional \(\mathscr A_\tau(\xi)\) (or \(Q_H(g)\)) from prime powers and archimedean factors, specifying convergence domains and certified regularization without supplying zero inputs or assuming Weil positive-type factorization | Mathematical definition & regularization (`CURVATURE_TRANSPORT.md` §15) | `OPEN (CANONICAL EARLIEST OBLIGATION)` |
| `OBL-CT-001B` | Curvature Spectral Expansion Derivation | Derive meromorphic/contour spectral expansion \(\mathscr A_\tau(\xi) = \sum_{\rho\in\Lambda^+/\#} W_\rho \delta_\rho^2\) from the non-scalar functional | Meromorphic/contour expansion derivation | `OPEN` |
| `OBL-CT-001C` | Absolute Convergence, Pair Isolation & Positivity | Prove absolute convergence of the spectral sum, complete isolation of reflection pairs \((\rho, \rho^\#)\) without uncancelled cross-terms \((\rho_1, \rho_2)\), and strict weight positivity \(W_\rho > 0\) | Asymptotic kernel & pairing analysis | `OPEN` |
| `OBL-CT-001D` | Arithmetic Vanishing & Curvature Rigidity | Prove independent arithmetic vanishing \(\mathscr A_\tau(\xi) = 0\) and combine with positive-weight rigidity to establish \(\forall \rho, \delta_\rho = 0 \iff \mathrm{RH}\) | Lean 4 `ConditionalCurvatureRigidityBridge.all_defects_zero` | `OPEN (CONDITIONAL RIGIDITY PROVED)` |
| `OBL-WH-001` | Non-Circular Arithmetic Hermitian Companion Construction | Construct arithmetic Hermitian companion form \(Q_H(f)\) matching \(\sum |\Phi_f(\rho)|^2\) and evaluate \(Q_H(\Phi_0) = N_\xi\) without assuming \(Q_W(f * f^*) \ge 0\) or supplying zeta zeros | Arithmetic explicit formula & GNS factorization analysis | `KNOWN_RH_EQUIVALENCE / OPEN_ARITHMETIC_NORM` |
| `OBL-WH-002` | Admissible Probe Regularization & Limit Interchange | Construct admissible smoothing family \(f_\varepsilon \in C_c^\infty(\mathbb R)\) approaching spectral probe \(\Phi_0(s) = 1/s\), proving convergence of every zero, prime, pole, and Archimedean term in the explicit formula | Classical analysis & dominated convergence | `OPEN (ACTIVE OBLIGATION)` |
| `OBL-BG-001` | Bilateral Grade Centered Second Variation | Construct symmetric second difference $C_h = Q(F, \Delta_h) + Q(F, \Delta_{-h}) - 2Q(F, 0)$ under coordinate dilation $\Delta_{\pm h}(z) = \Delta Z(\tau^{\pm h}z)$ to cancel background cross-terms | Asymmetric coordinate dilation leaves residual cross-term $4h^2\Re(F\bar B) \ne 0$ (Lean 4 `bilateral_second_order_asymmetry_cross_term`); reported diagonal cross-term $\mathfrak X_{\zeta,\mathrm{diag}}$ has exact positive cancelling variances $v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)} > 0$ for all $a > 1/\log 2$, falsifying universal non-vanishing (`DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES`, Lean 4 `diagonal_crossterm_cancelling_variance_zero`, `cancelling_variance_pos_of_bounds`, `cancelling_variance_pos_of_log2_bound`); Formalized load-bearing arithmetic descent count remains 0 | `CLOSED (NO-GO / FAIL_BILATERAL_CROSS_TERM_CANCELLATION / DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES)` |
| `OBL-DERIVE-FULL-WINDOWED-ZETA-CROSS-TERM` | Complete Windowed and Completed-Zeta Cross-Term Derivation | Derive the complete windowed Dirichlet and completed-$\xi$ cross-term $\langle F_0, \ddot F_0 \rangle_W$, including all off-diagonal terms $\sum_{m\ne n} c_m \bar d_n \widehat W(\log(m/n))$, pole, and gamma factor contributions, and determine if an admissible window $W$ exists that cancels the complete non-diagonalized cross-term | Full double-sum Fourier analysis & completed xi jet analysis | `OPEN (ACTIVE OBLIGATION)` |
| `OBL-CMSA-INT-SIGMA` | Integrated-$\sigma$ Mean-Square Variation | Integrate resolvent variation over $\sigma \in [\sigma_0, \infty)$ to eliminate boundary divergence and isolate radial defect | Proved: Unnormalized integration diverges on base prime diagonal ($\int |P_\sigma|^2 = \infty$), losing arithmetic anchor; normalized averaging renders finite perturbation invisible | `CLOSED (FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT)` |






---

## 3. Retained Falsification Controls and Negative Probes

1. **Non-Euler Product Control (Davenport-Heilbronn)**:
   $$f(s) = \frac{1-i\kappa}{2} L(s, \chi_5) + \frac{1+i\kappa}{2} L(s, \bar\chi_5)$$
   Satisfies functional equation $f(s) = \chi(s) f(1-s)$ but has zeros off the critical line in the critical strip (e.g. at $\sigma \approx 0.808, t \approx 85.699$).
   *Purpose*: Proves that satisfying a functional equation and real-symmetry is insufficient to ensure all zeros are on the critical line without the Euler product.

2. **Off-Line Zero Amplification Control**:
   Artificially set $\delta = 10^{-3}$ and test $K = 50 \implies |q_\rho^K| = \tau^{0.05} \approx 1.0963 \neq 1$.
   *Purpose*: Proves that the centrifuge cleanly separates on-line ($\delta=0$) from off-line ($\delta \neq 0$) zeros.

3. **Dirichlet Divergence Control**:
   Evaluate partial sum $\sum_{n=1}^{1000} n^{-(0.5 + 14.134725i)}$ and compare with true $\zeta(0.5 + 14.134725i) = 0$.
   *Purpose*: Proves that naive Dirichlet summation in the critical strip produces massive truncation error and cannot be used as an analytic continuation.
