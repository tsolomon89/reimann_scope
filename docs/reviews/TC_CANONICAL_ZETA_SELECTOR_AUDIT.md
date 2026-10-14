# TASK-TC-035 — Canonical Zeta Selector Principle and Uniqueness Audit

**Task ID:** `TASK-TC-035`  
**Parent Commit (`TASK-TC-034R`):** `d06d13c9cbd5f66589692f8eae41409781b18908`  
**Principal Classification:** `NO_ZERO_INDEPENDENT_SINGLE_KERNEL_SELECTOR_FOUND_IN_STANDARD_ZETA_AXIOMS`  
**Secondary Trilemma Classification:** `CANONICAL_SELECTOR_TRILEMMA_PROVED_OBL_CT_001A_OPEN`  
**Canonical Open Obligation:** `OBL-CT-001A = OPEN`  
**Evidence Artifacts:**
- Implementation & Arb Verifier: `tc/canonical_selector_audit.py`
- Certified Audit Payload: `data/tc_canonical_zeta_selector_audit.json`
- Formal Lean 4 Module: `formal/RiemannScope/CanonicalSelectorAudit.lean` (`1 def` + `15 theorem` declarations, `0 sorry`, `0 admit`; repository total: `580` compiled `theorem` declarations)
- Test Suite: `tests/test_tc_canonical_selector_audit.py`

---

## 1. Mission and Exact Problem Statement

In `TASK-TC-033`, the repository established `TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`: for the transported two-variable kernel family
$$F_{K,b}(x,y) = \tau^{aK} F_0(\tau^{-bK}x, \tau^{-bK}y), \qquad \tau = 2\pi,$$
the unique transport exponent $b = 1$ that preserves the same prime-power labels across all grades $K$ also cancels the zero-dependent spectral exponent $\tau^{(b-1)K(\rho+\sigma)}|_{b=1} = 1$.

In `TASK-TC-034` and `TASK-TC-034R`, we passed to the infinitesimal transport-mismatch curvature around $b = 1$ ($\eta = b - 1$):
$$\widehat{\mathcal M}_K(\eta) = \sum_{n,m \ge 2} \Lambda(n)\Lambda(m)\,F_0(\tau^{-\eta K}n, \tau^{-\eta K}m), \qquad \partial_\eta^j \widehat{\mathcal M}_K(0) = (-K\log\tau)^j A_j(F_0),$$
where $\mathcal E = x\partial_x + y\partial_y$ is the multiplicative Euler scaling generator,
$$A_j(F_0) = \sum_{n,m \ge 2} \Lambda(n)\Lambda(m)\,(\mathcal E^j F_0)(n,m), \qquad j \in \{0, 1, 2\},$$
and the normalized log-mismatch curvature is
$$\partial_\eta^2\log\widehat{\mathcal M}_K(0) = \frac{(K\log\tau)^2}{A_0(F_0)^2}\,\mathfrak C_{\mathrm{arith}}(F_0), \qquad \mathfrak C_{\mathrm{arith}}(F_0) := A_0(F_0)A_2(F_0) - A_1(F_0)^2.$$
`TASK-TC-034R` certified in 128-bit Arb ball arithmetic that on generic admissible compactly supported nonnegative kernels $F_0 \in C_c^\infty((0,\infty)^2)$, the complete arithmetic curvature $\mathfrak C_{\mathrm{arith}}(F_0)$ is **sign-indefinite** ($\mathfrak C_{\mathrm{arith}}(\widetilde G_-) < 0 < \mathfrak C_{\mathrm{arith}}(\widetilde G_+)$).

Therefore, generic smooth admissibility cannot supply an unconditional curvature sign constraint. This isolated the **Canonical Selector Problem** (`TASK-TC-035`):

$$\boxed{\begin{gathered}
\textbf{Which zero-independent axioms, derived from the completed zeta }\xi(s)\\
\textbf{and its prime-side structure, uniquely select a non-scalar arithmetic functional}\\
\textbf{from the otherwise arbitrary kernel space before curvature or spectral positivity is tested?}
\end{gathered}}$$

### Formal Admissibility Requirements for a Canonical Zeta Selector

A valid single-kernel canonical zeta selector $\mathcal S$ on the label-compatible ($b=1$) transport family must satisfy four conditions:
1. **Zero-Independence:** $\mathcal S$ is defined exclusively from prime-power labels $(n, \Lambda(n))$, the Archimedean factor $\Gamma_{\mathbb R}(s) = \pi^{-s/2}\Gamma(s/2)$, the functional equation involution $s \leftrightarrow 1-s$, and multiplicative scaling structure—never from the nontrivial zeros $\rho$ of $\zeta(s)$.
2. **Projective Uniqueness (or Invariant Sign-Definite Subspace):** $\mathcal S(F_0) = 0$ selects either a unique nonzero projective ray $\mathbb R_{>0}\cdot F_0^\star$ or an invariant subspace $\mathcal V_{\mathcal S}$ on which $\mathfrak C_{\mathrm{arith}}(F_0)$ has a fixed sign.
3. **Arithmetic Curvature Sign Control:** On the selected kernel $F_0^\star$ (or subspace $\mathcal V_{\mathcal S}$), the arithmetic Euler curvature satisfies $\mathfrak C_{\mathrm{arith}}(F_0^\star) \le 0$ unconditionally.
4. **Spectral Positive-Curvature Detection:** The Mellin transform $\widehat F_0^\star(s, w)$ isolates a strictly positive off-critical radial curvature contribution $S_{\mathrm{diag}}(F_0^\star) > 0$ whenever $\exists \rho_0$ with $\delta_{\rho_0} = \operatorname{Re}(\rho_0) - \tfrac{1}{2} \ne 0$, with nonnegative remainder $R_{\mathrm{comp}}(F_0^\star) \ge 0$, without assuming Weil positivity across the full test space.

---

## 2. Executive Classification Summary of the Six Candidate Selectors

| Selector ID | Candidate Principle | Unique Object Selected by Zero-Independent Axioms | Arithmetic Curvature $\mathfrak C_{\mathrm{arith}}$ Status | Spectral Isolation / Positivity Status | Evidence Class | Canonical Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SELECTOR-I** | **Functional Equation Uniqueness** (Hamburger / Burnol Co-Poisson Dictionary) | (1) Functional equation + growth/support assumptions characterize the zeta-side distribution $\zeta(s) = \sum_{n\ge 1} n^{-s}$; (2) Euler product and logarithmic differentiation determine the von Mangoldt prime-power distribution $-\zeta'(s)/\zeta(s) = \sum_{n\ge 2}\Lambda(n)n^{-s}$; (3) **neither theorem selects a unique test kernel $F_0$** | Sign-indefinite even on compact kernels satisfying $F_0 \ge 0$, $F_0(x,y)=F_0(y,x)$, and $F_0(c_0^2/x, c_0^2/y)=F_0(x,y)$ ($\mathfrak C_{\mathrm{arith}}(\widetilde G_-^{\mathrm{inv}}) < 0 < \mathfrak C_{\mathrm{arith}}(\widetilde G_+^{\mathrm{inv}})$) | Double spectral sum over $(\rho,\sigma)$ is unchanged by kernel involution symmetry $\rho \leftrightarrow 1-\rho$ | `CERTIFIED_FINITE_AND_EXTERNAL_THEOREM` | `FUNCTIONAL_EQUATION_SELECTS_DISTRIBUTION_RAY_NOT_TEST_KERNEL` |
| **SELECTOR-II** | **Jacobi Theta Self-Duality** ($\vartheta(1/t) = \sqrt{t}\vartheta(t)$ & Ground-State Gaussian) | The Gaussian $\Theta_1(x,y) = e^{-\pi(x^2+y^2)}$ at $t = 1$ is uniquely selected **within the specified positive heat-semigroup, harmonic-oscillator ground-state, or minimum-uncertainty class** (the full self-Fourier space is not one-dimensional) | **Strictly negative** at $t=1$: $\mathfrak C_{\mathrm{arith}}(\Theta_1) = 4\pi^2(M_0 M_2 - M_1^2) - 4\pi M_0 M_1 \approx -3.432247\times 10^{-21} < 0$ because the Euler chain-rule drift $-4\pi M_0 M_1$ dominates the positive Bernstein variance by $5$ orders of magnitude | Separable tensor square $\Theta_1 = \theta_1 \otimes \theta_1$ factorizes the 2D spectral sum into the square of a 1D linear explicit-formula sum (`tensor_square_curvature_reduction`), giving no diagonal zero isolation | `LEAN_PROVED_AND_CERTIFIED_FINITE` | `THETA_SELF_DUAL_GAUSSIAN_HAS_NEGATIVE_EULER_CURVATURE_BY_DRIFT` |
| **SELECTOR-III** | **Prime / Archimedean Explicit-Formula Balance** & Burnol Conductor Operator $\log\|x\|+\log\|y\|$ | Selects the universal explicit-formula distribution $W_\zeta \in \mathcal D'(\mathbb R_{>0})$ (an identity valid for **all** admissible test functions) | Imposing support separation to force $Q_\varepsilon = 0$ triggers exact complement cancellation $R_\varepsilon = -D_\varepsilon$ (`exact_cancellation_precludes_strict_subordination`) | Exact cancellation precludes isolating a strictly positive zero block from the Archimedean/polar terms | `LEAN_PROVED_AND_EXTERNAL_THEOREM` | `PRIME_ARCHIMEDEAN_BALANCE_IS_UNIVERSAL_DISTRIBUTIONAL_IDENTITY` |
| **SELECTOR-IV** | **Extremal / Variational Principles** (Nyman–Beurling–Baez-Duarte $d_N^2$, Li $\lambda_n$, Suzuki $\lambda_1(R)$) | For each fixed $N$ or $R$, strict $L^2$ convexity selects a unique finite-stage minimizer $f_N^\star$ (an **infinite sequence**, not a single kernel) | At any single finite stage $N$, $d_N^2 > 0$ holds unconditionally whether or not RH holds; Mellin dilation $\mathcal D_K$ is an $L^2$ isometry (`PURE_COORDINATE_RESCALING_NO_GAIN`) | Critical-line zero confinement requires the asymptotic limit $\lim_{N\to\infty} d_N = 0$ (or $\forall n, \lambda_n \ge 0$; $\forall R, \lambda_1(R) \ge 0$), which is RH-equivalent | `PROVED_PAPER_DERIVATION_AND_EXTERNAL_THEOREM` | `VARIATIONAL_SELECTORS_REQUIRE_INFINITE_ASYMPTOTIC_FAMILY_RH_EQUIVALENT` |
| **SELECTOR-V** | **Canonical Operator Trace** (Connes–Consani Semi-Local Trace & Sonin Compression) | Compression of scaling onto Sonin's space ($\Lambda = 1$) selects the prolate spheroidal wave function basis and compressed trace $\operatorname{Tr}_{\mathrm{Sonin}}$ | Positivity holds at the single Archimedean place via prolate/Toeplitz control (Connes–Consani 2020) | Including prime places in the semi-local trace formula makes global trace positivity equivalent to Weil positivity (`CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`) | `EXTERNAL_THEOREM` | `OPERATOR_TRACE_COMPRESSION_REDUCES_TO_SEMI_LOCAL_WEIL_POSITIVITY` |
| **SELECTOR-VI** | **Functorial & Multi-Grade Naturality** Stronger than Ordinary Rescaling | Ordinary coboundary naturality selects $b=1$ (leaving $F_0$ arbitrary); strengthened Euler homogeneity $\mathcal E F_0 = d F_0$ selects $F_0 \equiv 0$ on $C_c^\infty((0,\infty)^2)$ | Ordinary naturality leaves $\mathcal E^j F_0$ $K$-independent and sign-indefinite; Euler homogeneity forces $\mathfrak C_{\mathrm{arith}} = 0$ algebraically (`homogeneous_arithmetic_curvature_zero`) but vanishes identically on compact support | At $b=1$, value-level covariance cancels $\tau^{(b-1)K(\rho+\sigma)} = 1$; noncompact homogeneous powers diverge on the critical strip | `LEAN_PROVED_AND_PROVED_PAPER_DERIVATION` | `STRONGER_SCALE_NATURALITY_COLLAPSES_TO_HOMOGENEITY_NO_GO` |

---

## 3. Detailed Mathematical Audit of the Six Candidate Selectors

### 3.1 Selector I: Uniqueness under the Functional Equation (Hamburger / Burnol Co-Poisson Dictionary)

#### Classical and Distributional Uniqueness Theorem
By Hamburger's Theorem (1921) and its distributional co-Poisson formulation by Burnol ([arXiv:1106.4749v2](https://arxiv.org/abs/1106.4749v2), [arXiv:math/0407443v3](https://arxiv.org/abs/math/0407443v3)) and Baez-Duarte ([arXiv:math/0207237v1](https://arxiv.org/abs/math/0207237v1)), the space of tempered distributions supported on $\mathbb Z$ whose Fourier/Poisson transform satisfies the completed functional equation $\xi(s) = \xi(1-s)$ with the $\Gamma_{\mathbb R}(s) = \pi^{-s/2}\Gamma(s/2)$ factor and moderate polynomial growth is **one-dimensional**, spanned by the zeta-side integer counting distribution $\sum_{n\ge 1}\delta_n$ corresponding to $\zeta(s) = \sum_{n\ge 1} n^{-s}$. Separately, the Euler product and nonlinear logarithmic differentiation determine the von Mangoldt prime-power distribution $-\frac{\zeta'}{\zeta}(s) = \sum_{n\ge 2}\Lambda(n)n^{-s}$.

**Crucial Distinction (Zeta Distribution vs. von Mangoldt Distribution vs. Test Kernel):**  
The valid deductive chain is:
1. the functional equation plus growth/support assumptions characterizes the zeta-side distribution $\zeta(s) = \sum_{n\ge 1} n^{-s}$;
2. the Euler product and logarithmic differentiation determine the von Mangoldt prime-power distribution $-\frac{\zeta'}{\zeta}(s) = \sum_{n\ge 2}\Lambda(n)n^{-s}$;
3. **neither theorem selects a unique test kernel $F_0$**: the explicit formula $\langle W_\zeta \otimes W_\zeta, F_0\rangle_{\mathrm{arith}} = \langle W_\zeta \otimes W_\zeta, F_0\rangle_{\mathrm{spec}}$ is an identity holding for *every* admissible test kernel $F_0$.

#### Testing Functional-Equation Involution Symmetry on the Kernel $F_0$
In Mellin coordinates, the functional equation $s \leftrightarrow 1-s$ corresponds to multiplicative inversion $x \mapsto c_0^2 / x$ around a scale center $c_0 > 0$. One may ask whether restricting $F_0 \in C_c^\infty((0,\infty)^2)$ to satisfy simultaneously:
1. **Strict nonnegativity:** $F_0(x,y) \ge 0$ everywhere on $(0,\infty)^2$ and $F_0(n,m) > 0$ on active stations,
2. **Station permutation symmetry:** $F_0(x,y) = F_0(y,x)$, and
3. **Functional-equation multiplicative inversion symmetry:** $F_0(c_0^2/x, c_0^2/y) = F_0(x,y)$ (so that $w(x,y) = \log(xy/c_0^2)$ satisfies $w(c_0^2/x, c_0^2/y) = -w(x,y)$),

fixes the sign of $\mathfrak C_{\mathrm{arith}}(F_0)$.

We construct the multiplicative-inversion-symmetric smooth plateau cutoff $\mathcal X_{\mathrm{inv}}(x,y) = \chi_{\mathrm{inv}}(x)\chi_{\mathrm{inv}}(y)$ around $c_0 = 4$ ($c_0^2 = 16$), where $\chi_{\mathrm{inv}}(x) = \psi_{\mathrm{log}}(|\log(x/4)|)$ has:
- **Exact flat plateau:** $[16/10.25,\,10.25]^2 \approx [1.56098,\,10.25]^2$, where $\mathcal X_{\mathrm{inv}} \equiv 1$ and $\mathcal E\mathcal X_{\mathrm{inv}} = \mathcal E^2\mathcal X_{\mathrm{inv}} = 0$,
- **Compact support:** $(16/10.5,\,10.5)^2 \approx (1.52381,\,10.5)^2$, vanishing identically at $1$ and for all stations $n \ge 11$,
- **Complete active prime-power station set:** $\{2, 3, 4, 5, 7, 8, 9\}$ ($7$ stations, $49$ ordered pairs), all strictly inside the flat plateau.

Using the even functions of $w = \log(xy/16)$:
$$\widetilde G_-^{\mathrm{inv}}(x,y) = \mathcal X_{\mathrm{inv}}(x,y)\,\exp\!\left(-\frac{3}{2}\log^2\!\left(\frac{xy}{16}\right)\right),$$
$$\widetilde G_+^{\mathrm{inv}}(x,y) = \mathcal X_{\mathrm{inv}}(x,y)\,\cosh\!\left(\frac{6}{5}\log\!\left(\frac{xy}{16}\right)\right)\exp\!\left(-\frac{2}{25}\log^2\!\left(\frac{xy}{16}\right)\right),$$
128-bit Arb ball arithmetic (`certify_inversion_symmetric_witness_arb` in `tc/canonical_selector_audit.py`) certifies opposite signs for the **complete** compact-support arithmetic sums:

| Witness Kernel | Symmetries Satisfied | $A_0(F_0)$ (128-bit Arb) | $A_1(F_0)$ (128-bit Arb) | $A_2(F_0)$ (128-bit Arb) | $\mathfrak C_{\mathrm{arith}}(F_0) = A_0 A_2 - A_1^2$ (128-bit Arb) | Certified Sign |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $\widetilde G_-^{\mathrm{inv}}$ | $F \ge 0$, $F(x,y)=F(y,x)$, $F(16/x,16/y)=F(x,y)$, $C_c^\infty$ | `[31.975117919963795925... +/- 7.39e-36]` | `[-44.832273584101540208... +/- 2.33e-35]` | `[-74.099567819037551856... +/- 4.77e-35]` | `[-4379.27517355180899705054019478775897 +/- 3.99e-33]` | **Strictly Negative ($< 0$)** |
| $\widetilde G_+^{\mathrm{inv}}$ | $F \ge 0$, $F(x,y)=F(y,x)$, $F(16/x,16/y)=F(x,y)$, $C_c^\infty$ | `[90.144165027681128980... +/- 5.41e-35]` | `[91.083479042632538233... +/- 5.72e-35]` | `[374.799315297728007628... +/- 5.14e-34]` | `[+25489.7711759506050296948994043254704 +/- 2.78e-32]` | **Strictly Positive ($> 0$)** |

Hence **Selector I** is classified as:
$$\boxed{\texttt{FUNCTIONAL\_EQUATION\_SELECTS\_DISTRIBUTION\_RAY\_NOT\_TEST\_KERNEL}.}$$

---

### 3.2 Selector II: Jacobi Theta Self-Duality and the Additive-to-Multiplicative Chain-Rule Drift Theorem

#### Uniqueness of the Self-Dual Gaussian within the Ground-State Class
Riemann's second proof of the functional equation uses the Jacobi theta transformation $\vartheta(1/t) = \sqrt{t}\,\vartheta(t)$, which follows from Poisson summation applied to the Gaussian $g_t(x) = e^{-\pi t x^2}$. Under the Fourier transform $(\mathcal F f)(\xi) = \int_{\mathbb R} f(x)e^{-2\pi i x\xi}\,dx$, the full self-Fourier space $\mathcal F f = f$ is infinite-dimensional (spanned by all even Hermite functions $H_{4k}(\sqrt{2\pi}x)e^{-\pi x^2}$); however, the Gaussian $f(x) = e^{-\pi x^2}$ at scale $t = 1$ is **uniquely selected within the specified positive heat-semigroup, harmonic-oscillator ground-state ($(-\partial_x^2 + 4\pi^2 x^2)f = 2\pi f$), or minimum-uncertainty ($\|x f\|_2 \|\xi \hat f\|_2 = \frac{1}{4\pi}\|f\|_2^2$) class** (up to a positive scalar), and hence on $(0,\infty)^2$ selects the canonical radial Gaussian
$$\Theta_1(x,y) = e^{-\pi(x^2 + y^2)} = \Theta_t(x,y)\Big|_{t=1}, \qquad \Theta_t(x,y) := e^{-\pi t(x^2 + y^2)}.$$

Selector II therefore genuinely selects a **unique canonical test kernel** $\Theta_1$ within the ground-state class. We now prove two exact theorems showing what happens when $\Theta_1$ is evaluated under multiplicative prime-station transport.

#### Theorem 1 (Separable Tensor-Square Curvature Reduction — Lean: `tensor_square_curvature_reduction`)
Let $F_0(x,y) = f(x)f(y)$ be any separable tensor-square kernel with 1D prime-station Euler moments
$$m_k := \sum_{n \ge 2} \Lambda(n)\,((x\partial_x)^k f)(n), \qquad k \in \{0, 1, 2\}.$$
Since $\mathcal E(f \otimes f) = (x\partial_x f)\otimes f + f \otimes (y\partial_y f)$ and $\mathcal E^2(f \otimes f) = (x\partial_x)^2 f \otimes f + 2(x\partial_x f)\otimes(y\partial_y f) + f \otimes (y\partial_y)^2 f$, the 2D Euler moments satisfy (`tensor_square_moment_A0`, `tensor_square_moment_A1`, `tensor_square_moment_A2`):
$$A_0(f \otimes f) = m_0^2, \qquad A_1(f \otimes f) = 2 m_0 m_1, \qquad A_2(f \otimes f) = 2 m_0 m_2 + 2 m_1^2.$$
Therefore (`tensor_square_curvature_reduction`):
$$\boxed{\mathfrak C_{\mathrm{arith}}(f \otimes f) = A_0 A_2 - A_1^2 = m_0^2(2 m_0 m_2 + 2 m_1^2) - (2 m_0 m_1)^2 = 2 m_0^2(m_0 m_2 - m_1^2).}$$
Furthermore, because $\widehat F_0(s, w) = \hat f(s)\hat f(w)$, the 2D explicit formula for $f \otimes f$ is simply the square of the 1D linear explicit formula for $f$; it introduces no new cross-zero bilinear pairing beyond 1D explicit-formula evaluation.

#### Theorem 2 (Additive-to-Multiplicative Euler Chain-Rule Drift Identity — Lean: `euler_chain_rule_second_deriv_curvature`)
For the Jacobi theta / heat family $\Theta_t(x,y) = e^{-\pi t(x^2+y^2)}$, define the nonnegative additive radial moments
$$M_k(t) := \sum_{n,m \ge 2} \Lambda(n)\Lambda(m)\,(n^2 + m^2)^k e^{-\pi t(n^2 + m^2)} > 0, \qquad k \in \{0, 1, 2\}.$$
With respect to the **additive** heat parameter $t$, $\Theta_t$ is completely monotone, so its additive log-convexity determinant is strictly positive by Cauchy–Schwarz (Bernstein's theorem):
$$\partial_t^2 \log M_0(t) = \frac{\pi^2}{M_0(t)^2}\bigl(M_0(t) M_2(t) - M_1(t)^2\bigr) > 0.$$
However, multiplicative prime-station transport acts by the **Euler scaling generator** $\mathcal E = x\partial_x + y\partial_y$. Because $x^2 + y^2$ is homogeneous of degree $2$, $\mathcal E$ acts on $\Theta_t$ as $2t\partial_t$, and the second Euler derivative obeys the **chain-rule drift identity**:
$$(t\partial_t)^2 = t^2\partial_t^2 + t\partial_t \implies \mathcal E^2 \Theta_t = 4 t^2 \partial_t^2 \Theta_t + 4 t \partial_t \Theta_t.$$
Explicitly, with $c = 2\pi t$:
$$A_0(\Theta_t) = M_0(t), \qquad A_1(\Theta_t) = -c\,M_1(t), \qquad A_2(\Theta_t) = c^2 M_2(t) - 2c\,M_1(t).$$
Formalized in Lean as `euler_chain_rule_second_deriv_curvature`:
$$\boxed{\mathfrak C_{\mathrm{arith}}(\Theta_t) = c^2\bigl(M_0(t)M_2(t) - M_1(t)^2\bigr) - 2c\,M_0(t)M_1(t) = 4\pi^2 t^2(M_0 M_2 - M_1^2) - 4\pi t M_0 M_1.}$$
Thus $\mathfrak C_{\mathrm{arith}}(\Theta_t)$ is the difference between:
- the **positive additive Bernstein variance term** $+4\pi^2 t^2(M_0 M_2 - M_1^2) > 0$, and
- the **negative multiplicative Euler chain-rule drift term** $-4\pi t M_0 M_1 < 0$.

At a single dominant station pair $(n_0, m_0) = (2, 2)$ with $r = n_0^2 + m_0^2 = 8$, the variance $M_0 M_2 - M_1^2$ vanishes identically and (`single_station_theta_gaussian_curvature_neg`):
$$\frac{\mathfrak C_{\mathrm{arith}}}{A_0^2} = -2c r = -4\pi t (n_0^2 + m_0^2) = -32\pi t \approx -100.530965\,t < 0.$$

#### 128-bit Arb Certification at the Self-Dual Point $t = 1$
Evaluating $\Theta_1(x,y) = e^{-\pi(x^2+y^2)}$ at $t = 1$ in 128-bit Arb ball arithmetic (`certify_canonical_theta_gaussian_curvature_arb`), both for the compactified kernel $\widetilde\Theta_1 = \mathcal X_{15}\Theta_1$ and for the full infinite lattice $\mathbb N_{\ge 2}^2$ (where the exterior tail $\max(n,m) \ge 16$ is bounded rigorously by $4.91 \times 10^{-347}$):
- $M_0(1) \in [5.84305936627826185128361183211138217 \times 10^{-12} \pm 5.86 \times 10^{-48}]$
- $M_1(1) \in [4.67444888867549425074472651284519958 \times 10^{-11} \pm 6.09 \times 10^{-47}]$
- $M_2(1) \in [3.73956092528931269795724384242395039 \times 10^{-10} \pm 2.20 \times 10^{-46}]$
- **Positive Bernstein variance term:** $4\pi^2(M_0 M_2 - M_1^2) \in [+1.6097089323851242452337142816 \times 10^{-26} \pm 3.96 \times 10^{-55}] > 0$
- **Negative Euler chain-rule drift term:** $-4\pi M_0 M_1 \in [-3.43226315570907653944921880924324602 \times 10^{-21} \pm 4.57 \times 10^{-57}] < 0$
- **Complete arithmetic curvature:**
  $$\boxed{\mathfrak C_{\mathrm{arith}}(\widetilde\Theta_1) \in [-3.432247058619752688206766472100430 \times 10^{-21} \pm 3.80 \times 10^{-55}] < 0,}$$
  $$\boxed{\frac{\mathfrak C_{\mathrm{arith}}(\Theta_1)}{A_0(\Theta_1)^2} \in [-100.53052344669058612167632679576770 \pm 8.66 \times 10^{-33}] < 0.}$$

Because the negative Euler drift dominates the positive Bernstein variance by five orders of magnitude (`euler_drift_strictly_negative_of_dominant`), the self-dual Gaussian $\Theta_1$ has **strictly negative** multiplicative arithmetic curvature ($\mathfrak C_{\mathrm{arith}}(\Theta_1) < 0$). By `selector_trilemma_algebraic_dichotomy`, $\mathfrak C_{\mathrm{arith}}(\Theta_1) = S_{\mathrm{diag}} + R_{\mathrm{comp}} < 0$ with $S_{\mathrm{diag}} > 0$ simply forces the non-diagonal/Archimedean complement to be negative ($R_{\mathrm{comp}} < 0$) rather than yielding a contradiction.

Hence **Selector II** is classified as:
$$\boxed{\texttt{THETA\_SELF\_DUAL\_GAUSSIAN\_HAS\_NEGATIVE\_EULER\_CURVATURE\_BY\_DRIFT}.}$$

---

### 3.3 Multiplicative Log-Gaussian Variance-Threshold Theorem (Theorem 3)

What if one replaces the additive Gaussian $e^{-\pi(x^2+y^2)}$ by a **multiplicative log-Gaussian** $\Phi_{\alpha, w_0}(x,y) = \exp(-\alpha(\log(xy)-w_0)^2)$ so that the Euler operator $\mathcal E = x\partial_x + y\partial_y = 2\partial_w$ ($w = \log(xy)$) acts as a translation-invariant derivative without the exponential $x^2+y^2$ drift?

Let $z = \log(nm) - w_0$ and define the log-Gaussian weighted moments
$$S_k(\alpha, w_0) := \sum_{n,m \ge 2} \Lambda(n)\Lambda(m)\,(\log(nm)-w_0)^k e^{-\alpha(\log(nm)-w_0)^2}, \qquad k \in \{0, 1, 2\}.$$
Since $\mathcal E \Phi_{\alpha, w_0} = -4\alpha z \Phi_{\alpha, w_0}$ and $\mathcal E^2 \Phi_{\alpha, w_0} = (16\alpha^2 z^2 - 8\alpha)\Phi_{\alpha, w_0}$, we have
$$A_0 = S_0, \qquad A_1 = -4\alpha S_1, \qquad A_2 = 16\alpha^2 S_2 - 8\alpha S_0.$$
Formalized in Lean as `log_gaussian_curvature_identity`:
$$\boxed{\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) = 16\alpha^2(S_0 S_2 - S_1^2) - 8\alpha S_0^2 = 8\alpha S_0^2\bigl(2\alpha\operatorname{Var}_w(\log(nm)) - 1\bigr),}$$
where $\operatorname{Var}_w(\log(nm)) = \frac{S_0 S_2 - S_1^2}{S_0^2}$ is the weighted variance of $\log(nm)$ under the log-Gaussian measure. Consequently (`log_gaussian_curvature_neg_of_subcritical_variance`, `log_gaussian_curvature_pos_of_supercritical_variance`, `log_gaussian_critical_width_zero`):
- $\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) < 0 \iff 2\alpha\operatorname{Var}_w(\log(nm)) < 1$ (subcritical variance / local Gaussian concavity dominates);
- $\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) > 0 \iff 2\alpha\operatorname{Var}_w(\log(nm)) > 1$ (supercritical multi-station spread dominates);
- $\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) = 0 \iff \alpha = \alpha_\star := \frac{1}{2\operatorname{Var}_w(\log(nm))}$.

Thus the multiplicative log-Gaussian family has no intrinsic zero-independent scale parameter $\alpha$: its curvature sign depends continuously on the ratio between $\alpha$ and the station variance.

---

### 3.4 Selector III: Prime/Archimedean Explicit-Formula Balance and Conductor Operator

In Weil's explicit formula and Burnol's invariant analysis ([arXiv:math/0101068v1](https://arxiv.org/abs/math/0101068v1)), the dilaton-invariant conductor operator $\mathfrak C_{\mathrm{cond}}(f) = (\log|x| + \log|y|)f$ intertwines the prime-power von Mangoldt terms and the Archimedean Gamma term. However:
1. The explicit-formula balance $W_{\mathrm{prime}}(f) + W_{\infty}(f) = W_{\mathrm{polar}}(f) - W_{\mathrm{spec}}(f)$ is a **universal distributional identity** across all admissible $f$, not a selector for a single $f$.
2. If one selects $f$ by requiring support separation from prime-power stations so that the arithmetic side vanishes ($Q_\varepsilon = 0$), `TASK-TC-032R` (`exact_cancellation_precludes_strict_subordination`) proved that the omitted spectral/Archimedean remainder cancels the selected block identically ($R_\varepsilon = -D_\varepsilon$).

Hence **Selector III** is classified as:
$$\boxed{\texttt{PRIME\_ARCHIMEDEAN\_BALANCE\_IS\_UNIVERSAL\_DISTRIBUTIONAL\_IDENTITY}.}$$

---

### 3.5 Selector IV: Extremal and Variational Principles (Nyman–Beurling–Baez-Duarte, Li, Suzuki)

Variational formulations of RH—including the Nyman–Beurling–Baez-Duarte $L^2((0,\infty), dx/x)$ projection distance
$$d_N^2 = \inf_{c_1,\dots,c_N \in \mathbb C} \left\|\chi_{(0,1)}(x) - \sum_{k=1}^N c_k \left\{\frac{1}{kx}\right\}\right\|_{L^2((0,1))}^2$$
([arXiv:math/0307215v1](https://arxiv.org/abs/math/0307215v1), [arXiv:math/0202166v1](https://arxiv.org/abs/math/0202166v1)), Lagarias's interpretation of the Li coefficients $\lambda_n = \sum_\rho [1 - (1 - 1/\rho)^n]$ as values of Weil's quadratic functional on the canonical rational basis $\phi_n(s) = 1 - (1 - 1/s)^n$ ([arXiv:math/0404394v4](https://arxiv.org/abs/math/0404394v4)), and Suzuki's lowest eigenvalue $\lambda_1(R)$ of localized Weil operators ([arXiv:2606.09096v3](https://arxiv.org/abs/2606.09096v3))—use strict Hilbert-space convexity or canonical rational bases to select a **unique finite-stage object for each index $N$ or $R$**.

However:
1. Each principle selects an **infinite indexed sequence** $\{f_N^\star\}_{N \ge 1}$ (or $\{\phi_n\}_{n \ge 1}$, $\{f_R^\star\}_{R > 1}$), never a single finite kernel that suffices alone.
2. At any single finite $N$, $d_N^2 > 0$ holds unconditionally whether or not RH is true (`SINGLE_FINITE_STAGE_STRICTLY_POSITIVE_UNCONDITIONALLY_NO_ZERO_EXCLUSION`).
3. Excluding $\delta_\rho \ne 0$ requires the infinite asymptotic limit $\lim_{N\to\infty} d_N^2 = 0$ (or $\forall n \ge 1,\;\lambda_n \ge 0$), which is a known RH-equivalent reformulation. Moreover, by `TASK-TC-031` (`PURE_COORDINATE_RESCALING_NO_GAIN`), Mellin dilation $\mathcal D_K$ is an exact $L^2$ isometry leaving $d_N^2$ invariant.

Hence **Selector IV** is classified as:
$$\boxed{\texttt{VARIATIONAL\_SELECTORS\_REQUIRE\_INFINITE\_ASYMPTOTIC\_FAMILY\_RH\_EQUIVALENT}.}$$

---

### 3.6 Selector V: Canonical Operator Trace (Connes–Consani Semi-Local Trace and Sonin Compression)

Connes and Consani ([arXiv:2006.13771v1](https://arxiv.org/abs/2006.13771v1), [arXiv:2106.01715v1](https://arxiv.org/abs/2106.01715v1), [arXiv:2112.08820v1](https://arxiv.org/abs/2112.08820v1)) and Burnol ([arXiv:math/0105120v1](https://arxiv.org/abs/math/0105120v1)) study the compression of the multiplicative scaling action onto Sonin's space (orthogonal to cutoff projections $P_\Lambda, \widehat P_\Lambda$ at the self-dual parameter $\Lambda = 1$), where the prolate spheroidal wave functions provide a canonical eigenbasis.
- At the **single Archimedean place**, Connes and Consani prove positivity of the compressed scaling trace via prolate operator / Toeplitz matrix positivity.
- When **prime places** are adjoined in the semi-local trace formula, global positivity of the resulting trace functional is explicitly equivalent to Weil positivity across the semi-local test space (`CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`).

Hence **Selector V** is classified as:
$$\boxed{\texttt{OPERATOR\_TRACE\_COMPRESSION\_REDUCES\_TO\_SEMI\_LOCAL\_WEIL\_POSITIVITY}.}$$

---

### 3.7 Selector VI: Functorial and Multi-Grade Naturality Stronger than Ordinary Rescaling

By `TASK-TC-027` (`MULTIGRADE_NATURALITY_NO_GO_PROVED`), `TASK-TC-033` (`TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`), and `TASK-TC-034R` (`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`):
- **Ordinary coboundary naturality** $\mathcal F_K \cong \mathcal F_J$ with $c(J,K) = \tau^{J-K}$ uniquely selects the transport exponent $b = 1$, where value-level spectral grade dependence cancels ($\tau^{(b-1)K(\rho+\sigma)}|_{b=1} = 1$) and the Euler curvature moments $A_j(F_0)$ are $K$-independent while leaving $F_0$ arbitrary.
- **Strengthened infinitesimal Euler scale naturality** $\mathcal E F_0 = d F_0$ forces $A_1 = d A_0$, $A_2 = d^2 A_0$, and $\mathfrak C_{\mathrm{arith}}(F_0) = 0$ (`homogeneous_arithmetic_curvature_zero`), but by the ray ODE $g(r) = F_0(rx_0, ry_0) = r^d g(1)$, the only solution in $C_c^\infty((0,\infty)^2)$ is $F_0 \equiv 0$.

Hence **Selector VI** is classified as:
$$\boxed{\texttt{STRONGER\_SCALE\_NATURALITY\_COLLAPSES\_TO\_HOMOGENEITY\_NO\_GO}.}$$

---

## 4. The Canonical Selector Trilemma and Open Obligation `OBL-CT-001A`

**Evidence Scope Classifications:**
$$\boxed{\texttt{SIX\_STANDARD\_SELECTOR\_FAMILIES\_AUDITED}}, \qquad \boxed{\texttt{CONDITIONAL\_COMPLEMENT\_SIGN\_DICHOTOMY\_LEAN\_PROVED}}$$

Synthesizing the six audited standard selector families yields the **Canonical Selector Trilemma** (`SIX_STANDARD_SELECTOR_FAMILIES_AUDITED`) for any zero-independent selector $\mathcal S$ among those six families on label-compatible ($b=1$) two-variable kernels (note that Lean proves the conditional algebraic complement-sign dichotomy `CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED`, not that every conceivable zero-independent selector falls into the six-family research trilemma):

1. **Branch 1 — Scale-Homogeneous Flatness ($\mathcal E F_0 = d F_0$):**  
   Enforcing vanishing arithmetic curvature by scale homogeneity forces $\mathfrak C_{\mathrm{arith}}(F_0) = 0$ algebraically (`homogeneous_arithmetic_curvature_zero`), but collapses to $F_0 \equiv 0$ on compact support (`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`) and fails to converge across the critical strip on noncompact rays.
2. **Branch 2 — Classical Symmetry or Theta Self-Duality:**  
   - Imposing permutation symmetry $F_0(x,y) = F_0(y,x)$, nonnegativity $F_0 \ge 0$, and functional-equation inversion symmetry $F_0(c_0^2/x, c_0^2/y) = F_0(x,y)$ leaves an infinite-dimensional subspace on which $\mathfrak C_{\mathrm{arith}}$ is Arb-certified sign-indefinite ($\widetilde G_-^{\mathrm{inv}}$ vs. $\widetilde G_+^{\mathrm{inv}}$).
   - Imposing Fourier/theta ground-state self-duality within the positive heat-semigroup / oscillator ground-state / minimum-uncertainty class uniquely selects $\Theta_1(x,y) = e^{-\pi(x^2+y^2)}$, where the additive-to-multiplicative chain-rule drift $-4\pi M_0 M_1$ forces $\mathfrak C_{\mathrm{arith}}(\Theta_1) < 0$ (`euler_chain_rule_second_deriv_curvature`, `euler_drift_strictly_negative_of_dominant`) with $N_{\mathrm{cutoff}} = 15$ and outward tail bound $\approx 4.91 \times 10^{-347}$.
   - Whenever $\mathfrak C_{\mathrm{arith}}(F_0) \le 0$ and $\mathfrak C_{\mathrm{arith}}(F_0) = S_{\mathrm{diag}} + R_{\mathrm{comp}}$ with $S_{\mathrm{diag}} > 0$, Lean theorem `selector_trilemma_algebraic_dichotomy` proves that this merely implies $R_{\mathrm{comp}} < 0$ unless $R_{\mathrm{comp}} \ge 0$ is independently established (`selector_trilemma_contradiction_of_nonneg_complement`, which is `OBL-CT-001A`).
3. **Branch 3 — Variational or Semi-Local Trace Families:**  
   Selecting via Nyman–Beurling $L^2$ projection $d_N^2$, Li's rational basis $\lambda_n$, Suzuki's localized Rayleigh quotient $\lambda_1(R)$, or Connes–Consani's semi-local trace selects an infinite indexed family or global quadratic form whose positivity/vanishing is equivalent to RH.

### Hypothesis Fidelity: Why Candidate Selector Exhaustion Does Not Refute TC
Exhausting the six standard zero-independent selector candidates **refutes naive single-kernel selector implementations**, **not** the Transcendental Continuation (TC) hypothesis itself. The canonical obligation remains open:

$$\boxed{\texttt{OBL-CT-001A} = \texttt{OPEN}}$$

> **Statement of `OBL-CT-001A`:** Construct a zero-independent, non-scalar arithmetic functional (or multi-kernel nonlinear elimination invariant) whose complete spectral expansion detects positive off-critical radial curvature ($S_{\mathrm{diag}} > 0$ with controlled remainder $R_{\mathrm{comp}} \ge 0$) without assuming Weil positivity.

---

## 5. Exact Lean 4 Theorem Map (`formal/RiemannScope/CanonicalSelectorAudit.lean`)

The formal module `formal/RiemannScope/CanonicalSelectorAudit.lean` compiles with `0 sorry`, `0 admit`, and no nonstandard axioms, contributing `1 def` and `15 theorem` declarations (bringing the repository total from `565` to `580` compiled `theorem` declarations):

| # | Lean Identifier | Kind | Exact Formal Statement Scope | Algebraic Only? | Paper Step Supported | External Dependency |
| :---: | :--- | :---: | :--- | :---: | :--- | :--- |
| 1 | `oneDimCurvature` | `def` | `oneDimCurvature m0 m1 m2 := m0 * m2 - m1^2` | Yes | 1D prime-station Euler curvature determinant | None |
| 2 | `tensor_square_moment_A0` | `theorem` | `m0 * m0 = m0^2` | Yes | Separable tensor-square zeroth Euler moment $A_0(f\otimes f) = m_0^2$ | None |
| 3 | `tensor_square_moment_A1` | `theorem` | `m1 * m0 + m0 * m1 = 2 * m0 * m1` | Yes | Separable tensor-square first Euler moment $A_1(f\otimes f) = 2m_0 m_1$ | None |
| 4 | `tensor_square_moment_A2` | `theorem` | `m2 * m0 + 2 * m1 * m1 + m0 * m2 = 2 * m0 * m2 + 2 * m1^2` | Yes | Separable tensor-square second Euler moment $A_2(f\otimes f) = 2m_0 m_2 + 2m_1^2$ | None |
| 5 | `tensor_square_curvature_reduction` | `theorem` | `curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) = 2 * m0^2 * oneDimCurvature m0 m1 m2` | Yes | Theorem 1: $\mathfrak C_{\mathrm{arith}}(f\otimes f) = 2m_0^2(m_0 m_2 - m_1^2)$ | None |
| 6 | `tensor_square_curvature_pos_iff` | `theorem` | `m0 ≠ 0 → (0 < curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) ↔ 0 < oneDimCurvature m0 m1 m2)` | Yes | Positive curvature equivalence for separable tensor-square kernels | None |
| 7 | `tensor_square_curvature_neg_iff` | `theorem` | `m0 ≠ 0 → (curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) < 0 ↔ oneDimCurvature m0 m1 m2 < 0)` | Yes | Negative curvature equivalence for separable tensor-square kernels | None |
| 8 | `euler_chain_rule_second_deriv_curvature` | `theorem` | `curvatureDet M0 (-c * M1) (c^2 * M2 - 2 * c * M1) = c^2 * curvatureDet M0 M1 M2 - 2 * c * M0 * M1` | Yes | Theorem 2: Additive-to-multiplicative chain-rule drift identity for $\Theta_t$ | None |
| 9 | `euler_drift_strictly_negative_of_dominant` | `theorem` | `0 < c → c * curvatureDet M0 M1 M2 < 2 * M0 * M1 → curvatureDet M0 (-c * M1) (c^2 * M2 - 2 * c * M1) < 0` | Yes | Strict negativity of $\mathfrak C_{\mathrm{arith}}(\Theta_t)$ when Euler drift dominates Bernstein variance | None |
| 10 | `single_station_theta_gaussian_curvature_neg` | `theorem` | `0 < w → 0 < r → 0 < c → curvatureDet w (-c*(w*r)) (c^2*(w*r^2) - 2*c*(w*r)) = -2*c*w^2*r ∧ < 0` | Yes | Exact negative curvature $-2c w^2 r < 0$ at a single dominant prime-station pair | None |
| 11 | `log_gaussian_curvature_identity` | `theorem` | `curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) = 16 * a^2 * curvatureDet S0 S1 S2 - 8 * a * S0^2` | Yes | Theorem 3: Multiplicative log-Gaussian curvature variance-vs-concavity identity | None |
| 12 | `log_gaussian_curvature_neg_of_subcritical_variance` | `theorem` | `0 < a → 2 * a * curvatureDet S0 S1 S2 < S0^2 → curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) < 0` | Yes | Subcritical variance regime $\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) < 0$ | None |
| 13 | `log_gaussian_curvature_pos_of_supercritical_variance` | `theorem` | `0 < a → S0^2 < 2 * a * curvatureDet S0 S1 S2 → 0 < curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0)` | Yes | Supercritical variance regime $\mathfrak C_{\mathrm{arith}}(\Phi_{\alpha, w_0}) > 0$ | None |
| 14 | `log_gaussian_critical_width_zero` | `theorem` | `2 * a * curvatureDet S0 S1 S2 = S0^2 → curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) = 0` | Yes | Vanishing of multiplicative log-Gaussian curvature at $\alpha = \alpha_\star$ | None |
| 15 | `selector_trilemma_algebraic_dichotomy` | `theorem` | `curvatureDet A0 A1 A2 = S_diag + R_comp → curvatureDet A0 A1 A2 ≤ 0 → 0 < S_diag → R_comp < 0` | Yes | Selector Trilemma dichotomy: $\mathfrak C_{\mathrm{arith}} \le 0$ and $S_{\mathrm{diag}} > 0$ forces $R_{\mathrm{comp}} < 0$ | None |
| 16 | `selector_trilemma_contradiction_of_nonneg_complement` | `theorem` | `curvatureDet A0 A1 A2 = S_diag + R_comp → curvatureDet A0 A1 A2 ≤ 0 → 0 < S_diag → 0 ≤ R_comp → False` | Yes | Conditional contradiction when $R_{\mathrm{comp}} \ge 0$ (`OBL-CT-001A`) | None |

---

## 6. Primary Literature Retrieved via `literature-search-arxiv`

1. **Jean-François Burnol (2012)**, *Deux extensions de Théorèmes de Hamburger*, Expositiones Mathematicae 30 (2012), 295–308 — [https://arxiv.org/abs/1106.4749v2](https://arxiv.org/abs/1106.4749v2)
2. **Jean-François Burnol (2007)**, *Entrelacement de co-Poisson*, Annales de l'Institut Fourier 57(2) (2007), 525–602 — [https://arxiv.org/abs/math/0407443v3](https://arxiv.org/abs/math/0407443v3)
3. **Jean-François Burnol (2000)**, *Sur les Formules Explicites I: analyse invariante*, C. R. Acad. Sci. Paris, Série I, 331 (2000), 423–428 — [https://arxiv.org/abs/math/0101068v1](https://arxiv.org/abs/math/0101068v1)
4. **Jean-François Burnol (2004)**, *Two complete and minimal systems associated with the zeros of the Riemann zeta function*, Journal de Théorie des Nombres de Bordeaux 16 (2004), 65–94 — [https://arxiv.org/abs/math/0203120v7](https://arxiv.org/abs/math/0203120v7)
5. **Jean-François Burnol (2001)**, *Sur certains espaces de Hilbert de fonctions entières, liés à la transformation de Fourier et aux fonctions L de Dirichlet et de Riemann*, C. R. Acad. Sci. Paris, Série I, 333 (2001), 201–206 — [https://arxiv.org/abs/math/0105120v1](https://arxiv.org/abs/math/0105120v1)
6. **Luis Báez-Duarte (2002)**, *A general statement of the functional equation for the Riemann zeta-function* — [https://arxiv.org/abs/math/0207237v1](https://arxiv.org/abs/math/0207237v1)
7. **Luis Báez-Duarte (2003)**, *A new necessary and sufficient condition for the Riemann hypothesis* — [https://arxiv.org/abs/math/0307215v1](https://arxiv.org/abs/math/0307215v1)
8. **Jean-François Burnol (2003)**, *On an analytic estimate in the theory of the Riemann Zeta function and a Theorem of Báez-Duarte*, Acta Científica Venezolana 54 (2003), 210–215 — [https://arxiv.org/abs/math/0202166v1](https://arxiv.org/abs/math/0202166v1)
9. **Jeffrey C. Lagarias (2007)**, *Li Coefficients for Automorphic L-Functions*, Annales de l'Institut Fourier 57 (2007), 1689–1740 — [https://arxiv.org/abs/math/0404394v4](https://arxiv.org/abs/math/0404394v4)
10. **Alain Connes & Caterina Consani (2020)**, *Weil positivity and Trace formula, the archimedean place*, Selecta Mathematica 27 (2021), 77 — [https://arxiv.org/abs/2006.13771v1](https://arxiv.org/abs/2006.13771v1)
11. **Alain Connes & Caterina Consani (2021)**, *Spectral Triples and $\zeta$-Cycles* — [https://arxiv.org/abs/2106.01715v1](https://arxiv.org/abs/2106.01715v1)
12. **Alain Connes & Caterina Consani (2021)**, *BC-system, absolute cyclotomy and the quantized calculus* — [https://arxiv.org/abs/2112.08820v1](https://arxiv.org/abs/2112.08820v1)
