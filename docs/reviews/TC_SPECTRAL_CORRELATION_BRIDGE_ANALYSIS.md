# TC Spectral-Correlation Bridge Sublemma: Analysis, Barriers & Asymptotic Constraints

## 1. Executive Summary & Research Context

The primary mathematical reductio ad absurdum of the Transcendental Continuation (TC) program within `reimann_scope` aims to establish the Riemann Hypothesis ($H \Longrightarrow \bot$) via the dependency chain:
$$\rho_0 = \frac{1}{2} + \delta_0 + i\gamma_0, \quad \delta_0 \ne 0, \quad \zeta(\rho_0) = 0 \quad \stackrel{\text{Bridge Sublemma}}{\Longrightarrow} \quad \exists \text{ legal } b : \nu_b = 0 \quad \stackrel{\text{Extremal Lemma}}{\Longrightarrow} \quad M \tau^a = N \tau^c \quad \stackrel{\text{Lindemann}}{\Longrightarrow} \quad \bot.$$

### Current Status of the Two Reductio Halves
1. **The Terminal Half (Extremal-Grade Correlation Lemma & Algebraic Invariants)**:
   - **Status**: **PROVED** and formalized in Lean 4 (`RiemannScope/ExtremalCorrelation.lean`, 0 `sorry`).
   - If $\nu_b = 0$ holds for any finite legal configuration with $\ge 2$ active grades, the strictly unique maximal grade difference $a = K_+ - K_-$ isolates an uncancelable extremal point mass, forcing an integer relation $M \tau^a = N \tau^c$ ($a \ne c$).
   - For $\tau = 2\pi$, Lindemann's theorem (1882) proves that $\pi$ is transcendental over $\mathbb{Q}$, rendering $M(2\pi)^a = N(2\pi)^c$ impossible.
   - For the authentic 3-grade ensemble ($\{-1, -2, -3\}$ on window $[8, 20]$), three grouped keys $(1, 89, 563)$, $(2, 89, 3511)$, and $(1, 563, 3511)$ have unique prime-power station pairs with strictly positive amplitudes.
   - The three-coefficient vanishing theorem (`three_coefficient_legal_vanishing`) proves:
     $$c_{12}(b) = 0 \land c_{13}(b) = 0 \land c_{23}(b) = 0 \land \sum_{i=1}^3 b_i = 0 \Longrightarrow b = 0.$$
   - On the legal unit sphere ($\sum b_i = 0$, $\|b\|_2 = 1$), the normalized scalar bridge functional:
     $$L(b) = \frac{c_{12}(b)}{a_{12}} + \frac{c_{13}(b)}{a_{13}} + \frac{c_{23}(b)}{a_{23}} = b_1 b_2 + b_1 b_3 + b_2 b_3 = \frac{(b_1+b_2+b_3)^2 - \|b\|_2^2}{2} \equiv -\frac{1}{2}$$
     is an exact algebraic invariant (`scalar_bridge_L_invariant`, `legal_unit_scalar_invariant`).
2. **The Antecedent Half (Spectral-Correlation Bridge Sublemma)**:
   - **Statement**: Under hypothesis $H$ (existence of off-critical zero $\rho_0$), do there exist admissible test functions $g_\nu$ or legal vectors $b$ such that explicit formula spectral responses force $\nu_b = 0$ (or isolate an uncancelable grouped coefficient $c_\ell(b) = 0$, or force $L(b) = 0$)?
   - **Status**: **OPEN RESEARCH OBLIGATION WITH IDENTIFIED OBSTRUCTIONS**.

---

## 2. Target A: Production Convolution Table Enclosure & Certification Rigor

### Mathematical Formulation
The position-space convolution kernel is:
$$C_h(v) = \int_{\mathbb{R}} \psi_h(u) \psi_h(u - v) \, du, \qquad \psi_h(u) = h^{-3} \kappa''(u/h) - \frac{1}{4} h^{-1} \kappa(u/h),$$
with $\operatorname{supp}(\kappa) = [-1, 1]$. Under the dimensionless decomposition ($\xi = v/h \in [0, 2]$):
$$C_h(v) = h^{-5} K_{2,2}(\xi) - \frac{1}{2} h^{-3} K_{2,0}(\xi) + \frac{1}{16} h^{-1} K_{0,0}(\xi).$$

### Rigorous Linear Interpolation Remainder Theorem
For linear interpolation on a uniform mesh with cell width $\Delta v = 2h / (N_{\rm tab} - 1)$:
$$\|C_h - \Pi C_h\|_\infty \le \frac{(\Delta v)^2}{8} \|\psi_h'\|_2^2,$$
where:
$$\|\psi_h'\|_2^2 = h^{-7} \|\kappa'''\|_2^2 + \frac{1}{2} h^{-5} \|\kappa''\|_2^2 + \frac{1}{16} h^{-3} \|\kappa'\|_2^2 \approx 2.079712 \times 10^{13} \quad (h = 0.05).$$
For $N_{\rm tab} = 2001$ ($\Delta v = 5 \times 10^{-5}$):
$$\varepsilon_{\rm interp} = \frac{(5 \times 10^{-5})^2}{8} \times 2.079712 \times 10^{13} \approx 6499.101197.$$

### Midpoint Enclosure & Error Dimension Separation
1. **First Cell Midpoint Discrepancy**:
   - At $v = 0.000025$, independent 50-digit mpmath integration yields $C_h(v) \approx 175873407.882075$.
   - The linear interpolant between $v_0 = 0$ and $v_1 = 0.00005$ yields $C_{\rm interp}(v) \approx 175866910.181177$.
   - The observed discrepancy $|C_h(v) - C_{\rm interp}(v)| \approx 6497.700898$ is strictly enclosed by the analytic interpolation bound:
     $$6497.700898 \le 6499.101197.$$
2. **Absolute vs Peak-Normalized Error**:
   - The peak-normalized allowance is $\varepsilon_{\rm interp} / C_h(0) \approx 3.695 \times 10^{-5}$.
   - However, uniform relative error across $[0, 2h]$ is mathematically unbounded because $C_h(v)$ crosses zero at $v \approx 0.00941$. Therefore, the absolute $L^\infty$ bound $6499.101197$ is the declared uniform bound.
3. **Reproduction and Removal of Quadrature Defects**:
   - Previously, `certify_production_convolution_table(n_nodes=1)` returned `CONVOLUTION_TABLE_CERTIFIED` with claimed allowance $\approx 6499.10$, whereas the true 1-node error at $v = 0.00005$ is $\approx 1.58 \times 10^8$.
   - Repaired: all unsupported quadrature orders ($n_{\rm nodes} \ne 256$) immediately fail closed with `UNCERTIFIED_UNSUPPORTED_QUADRATURE_ORDER` and `is_table_certified: False`.
   - The baseline 256-node literals $c_4 = 4 \times 10^{-12}, c_2 = 1 \times 10^{-13}, c_0 = 1 \times 10^{-15}$ lack an analytic 512th-derivative remainder proof. Per Root Rule 0, unsupported certified flags have been removed (`UNCERTIFIED_NODAL_REMAINDER_PROOF_UNRESOLVED`, `is_table_certified: False`), and this status propagates directly into `certify_baseline_canonical_weil_error_budget`.

---

## 3. Target B: Exact Scalar Spectral-Correlation Implication

### Algebraic Invariant on Legal Subspace
For the authentic 3-grade family $\{-1, -2, -3\}$, window $[8, 20]$, $h = 0.05$:
- The three selected keys are:
  - $(1, 89, 563)$ with $a_{12} = a_{-1, 89} a_{-2, 563} \approx 0.114301665 > 0$
  - $(2, 89, 3511)$ with $a_{13} = a_{-1, 89} a_{-3, 3511} \approx 0.023478160 > 0$
  - $(1, 563, 3511)$ with $a_{23} = a_{-2, 563} a_{-3, 3511} \approx 0.005266271 > 0$.
- Each key has a strictly unique station pair with positive amplitudes, giving $c_{ij}(b) = a_{ij} b_i b_j$.
- Purely algebraically:
  $$L(b) = \frac{c_{12}(b)}{a_{12}} + \frac{c_{13}(b)}{a_{13}} + \frac{c_{23}(b)}{a_{23}} = b_1 b_2 + b_1 b_3 + b_2 b_3 = \frac{(b_1+b_2+b_3)^2 - \|b\|_2^2}{2}.$$
- On the legal unit sphere ($\sum b = 0, \|b\|_2 = 1$):
  $$L(b) \equiv -\frac{1}{2}.$$
- On the 2D legal subspace $b = P \beta$ ($P = [[-1, -1], [1, 0], [0, 1]]$):
  $$G_{\rm target} = \frac{G_{12}}{a_{12}} + \frac{G_{13}}{a_{13}} + \frac{G_{23}}{a_{23}} = -\frac{1}{2} P^T P = \begin{pmatrix} -1 & -1/2 \\ -1/2 & -1 \end{pmatrix}.$$

### Finite Linear Recoverability in $\operatorname{Sym}(2)$
The legal symmetric matrix space $\operatorname{Sym}(2)$ has dimension $\frac{2 \times 3}{2} = 3$.
1. **Critical Zeros Only**:
   Using the first 3 critical Riemann zeros ($\gamma_1 \approx 14.1347, \gamma_2 \approx 21.0220, \gamma_3 \approx 25.0109$):
   $$G_{\rm target} = \sum_{j=1}^3 \lambda_j S_j, \qquad \lambda \approx [1.69616 \times 10^{-4}, \; -3.82017 \times 10^{-5}, \; 1.02673 \times 10^{-5}],$$
   with residual $\|G_{\rm target} - \sum \lambda_j S_j\|_2 \approx 1.06 \times 10^{-14}$ (machine precision) and condition number $\kappa \approx 1103.77$.
2. **Critical Zeros Plus Off-Critical Quartet $Q(\rho_0)$**:
   Using the first 2 critical zeros plus an off-critical quartet ($z_0 = 0.49 + 100i$):
   $$G_{\rm target} = \lambda_1 S_1 + \lambda_2 S_2 + \lambda_Q Q(\rho_0), \qquad \lambda \approx [-6.564 \times 10^{-5}, \; -9.912 \times 10^{-6}, \; -1.028 \times 10^{-3}],$$
   with residual $\approx 2.33 \times 10^{-14}$ and condition number $\kappa \approx 3876.09$.
3. **Core Epistemic Conclusion on Recoverability**:
   Critical zeros alone fully span $\operatorname{Sym}(2)$. Therefore, **linear recoverability of $G_{\rm target}$ is completely independent of hypothesis $H$**.

### Ordinate Uncertainty Spectral Error Propagation & Certified Enclosure
For zero ordinates $\gamma$, finite-uncertainty error propagation cannot rely on a first-order linear approximation $\varepsilon_\gamma \|S_j'(\gamma)\|_2$.
Furthermore, sampling $\|S_j'(\xi)\|_2$ across seven Chebyshev nodes is **not** an upper bound on the interval supremum:
- At $\gamma = 21.022039638771556$ with $\varepsilon_\gamma = 20.0$ and anchor $-1$ on grades $[-1, -2, -3]$:
  - 7-node Chebyshev sampled maximum: $\approx 527,955.585567$
  - Interior derivative norm at $\xi = 36.2670198055$: $\approx 727,589.092037$
- This refutes the claim that the sampled Chebyshev maximum is a certified supremum enclosure ($727,589.09 > 527,955.59$).
- To address this rigorously:
  1. We derived a conservative, closed-form analytic majorant over the continuous interval $[\gamma - \varepsilon_\gamma, \gamma + \varepsilon_\gamma]$:
     $$\|S'(\xi)\|_2 \le \|P\|_2^2 \left( 4 B_A B_{A'} E_0^2 + 4 B_A^2 E_0 E_1 \right),$$
     where $B_A = \xi_{\max}^2 + 1/4$, $B_{A'} = 2\xi_{\max} + (\xi_{\max}^2 + 1/4)h$, $E_0 = \sqrt{\sum_K (\sum_n a_{K,n})^2}$, and $E_1 = \sqrt{\sum_K (\sum_n a_{K,n} |\log(\tau^K n)|)^2}$.
     At the reproduced parameters, this analytic majorant yields $\approx 1.497 \times 10^{10} \ge 727,589.09$.
  2. Because numerical kernel quadrature and roundoff are not enclosed via certified ball arithmetic, the evaluator fails closed: it sets `certified_mvt_error_bound = None`, `is_derivative_enclosure_certified = False`, and emits `diagnostic_mvt_error_bound`.
  3. The scalar bridge consumer propagates uncertainty through $\sum_j |\lambda_j| \varepsilon_j$ using the interval MVT bounds rather than the central-point derivative $\|S_j'(\gamma)\|_2$.

---

## 4. Arithmetic Dilation Repair & Bookkeeping Balance

### Arithmetic Normalization with Grade Dilation $D = \operatorname{diag}(\tau^K)$
The raw matrices $W_{\rm arch}$ and $W_{\rm prime}$ use station weights $\Lambda(n) w(\tau^K n)$, whereas the authentic spectral amplitudes are $a_{K,n} = \tau^K \Lambda(n) w(\tau^K n)$. Consequently, the legal subspace arithmetic matrix is:
$$W_G = P^T D (W_{\rm arch} - W_{\rm prime}) D P, \qquad D = \operatorname{diag}(\tau^K), \quad 1^T P = 0, \quad b = P \beta.$$
Omitting $D$ exaggerated the arithmetic quadratic form by roughly $2\times 10^2$ (for negative grades $[-1, -2, -3]$).

#### Reproduction Benchmarks ($b = (-1, 1, 0)/\sqrt{2}$, $h = 0.05$, window $[8, 20]$):
- **Missing dilation ($U = 320, N_t = 2000$)**: $A_\Phi(b) \approx 1.4802 \times 10^{11}$
- **Correct dilation ($U = 320, N_t = 2000$)**: $A_\Phi(b) \approx 7.4076 \times 10^8$
- **Correct dilation ($U = 640, N_t = 4000$)**: $A_\Phi(b) \approx 1.1622 \times 10^9$
- **Direct station contraction**: Evaluated directly as $(D b)^T (W_{\rm arch} - W_{\rm prime}) (D b)$, matching $\beta^T W_G \beta$ identically across multiple legal directions and under all permutations of the grade ensemble.

### Removal of Circular Spectral Verification
Defining $r_{\rm rec} = L - S_{\rm sel}$ and $R_\Phi = A_\Phi - S_{\rm sel}$ makes:
$$A_\Phi - L = R_\Phi - r_{\rm rec}$$
an algebraic identity for arbitrary $A_\Phi$ by subtraction:
$$(A_\Phi - L) - (R_\Phi - r_{\rm rec}) = (A_\Phi - L) - ((A_\Phi - S_{\rm sel}) - (L - S_{\rm sel})) \equiv 0.$$
- This is retained solely as an internal algebraic bookkeeping check (`is_tautological_bookkeeping_identity: True`).
- It does **not** certify explicit-formula agreement, independently measure the omitted spectral tail, or prove spectral compensation.
- A regression test confirms that modifying $A_\Phi$ arbitrarily still produces $0.0$ discrepancy.

---

## 5. Target B: Explicit Admissible Spectral Realization Analysis

### 1. Object, Scope, and Quantifiers
- **Object**: Admissible test function $\Phi$ in the Guinand-Weil explicit formula on the authentic 3-grade family $\{-1, -2, -3\}$ on window $[8, 20]$, with amplitudes $a_{K,n} = \tau^K \Lambda(n) w(\tau^K n)$, legal zero-sum constraint $\sum b_i = 0$, and unit normalization $\|b\|_2 = 1$.
- **Scope**: Concrete candidate off-critical zero instance $\rho_0 = 1/2 + 0.49 + 100i$ (hypothetical response calculation, not evidence of zero existence).
- **Contradiction Criterion**: Proving that hypothesis $H$ forces $|L(b)| < 1/2$ (or $L(b) = 0$) for a legal unit vector, where $L(b) = b_1 b_2 + b_1 b_3 + b_2 b_3 \equiv -1/2$.

### 2. Candidate Test Function & Selected-Weight Realization Mismatch
- **Candidate**: Canonical quadratic form $\Phi_b(z) = |A_h(z)|^2 |E_b(z)|^2$.
- **Admissibility**: Entire, even ($\Phi(z) = \Phi(-z) = \Phi(\bar{z})$), rapid decay in vertical strips ($\mathcal{O}(|t|^{-N})$).
- **Weight Realization**:
  In the explicit formula for a single quadratic test function $\Phi_b$, every zero enters with unit positive multiplicity ($+1$).
  Evaluating $\Phi_b$ on the selected zeros yields:
  - Critical zero $\gamma_1 \approx 14.1347$: $s_1(b) \approx 38,915.82$
  - Critical zero $\gamma_2 \approx 21.0220$: $s_2(b) \approx 354,326.37$
  - Off-critical quartet $Q(\rho_0)$ ($z_0 = 0.49 + 100i$): $q(b) \approx -5,416.65$
  - Single test selected sum: $S_{\Phi,\text{sel}}(b) = s_1(b) + s_2(b) + q(b) \approx +387,825.54$.
- **Finite Matrix Recovery Comparison**:
  Finite linear recovery of $G_{\rm target} = -(1/2) P^T P$ requires the specific recovery coefficients:
  $$\lambda = [\lambda_1, \lambda_2, \lambda_Q] \approx [-6.564 \times 10^{-5}, \; -9.912 \times 10^{-6}, \; -1.028 \times 10^{-3}],$$
  yielding $S_{\rm sel}(b) = \lambda_1 s_1 + \lambda_2 s_2 + \lambda_Q q = -0.50000000000007$ ($r_{\rm rec} \approx 6.9 \times 10^{-14}$).
- **The Selected-Weight Mismatch**:
  $$r_{\rm match}(b) = S_{\Phi,\text{sel}}(b) - S_{\rm sel}(b) \approx 387,825.54 - (-0.50) \approx 387,826.04.$$

### 3. Complete Explicit Formula Identity & First Use of $H$
The complete explicit formula identity for $\Phi_b$ decomposes as:
$$A_\Phi(b) = S_{\Phi,\text{sel}}(b) + R_{\Phi,\text{tail}}(b) = S_{\rm sel}(b) + r_{\rm match}(b) + R_{\Phi,\text{tail}}(b)$$
$$\Longrightarrow \boxed{A_\Phi(b) - L(b) = R_{\Phi,\text{tail}}(b) + r_{\rm match}(b) - r_{\rm rec}(b)}.$$
- **Where Hypothesis $H$ First Acts**:
  At a zero of multiplicity $m$, $-\frac{\zeta'}{\zeta}(s)$ has residue $-m$. The contour integral produces $+m \sum \Phi(\rho - 1/2)$.
  Hypothesis $H$ asserts that the set of zeros contains $\rho_0 = 1/2 + \delta_0 + i\gamma_0$ ($\delta_0 \ne 0$). By reflection and functional equation, this quartet adds the discrete term $Q(\rho_0)(b)$ to the spectral sum. Without $H$, $Q(\rho_0)$ is strictly absent.

### 4. Quantitative Deficit & The First Unresolved Analytic Step
- **Independent Critical Zero Sum**: The partial sum of the 29 critical zeros up to $T = 100$ is $\Sigma_{\text{crit},\le 100}(b) \approx 5.492 \times 10^7$.
- **Arithmetic Energy**: With correct dilation $D$, $A_\Phi(b) \approx 7.4076 \times 10^8$ (at $U = 320$).
- **Cancellation Precision Needed**:
  To force $|L(b)| < 0.5$ from the explicit formula, the spectral remainder $R_\Phi(b)$ would have to cancel $A_\Phi(b)$ to within $< 0.5$:
  $$\frac{0.5}{7.4076 \times 10^8} \approx 6.75 \times 10^{-10} \quad (\sim 9 \text{ decimal places of exact cancellation}).$$
- **The First Unresolved Analytic Barrier**:
  1. A single positive quadratic form $\Phi_b$ has unit positive weights $+1$ on every zero, generating huge positive energy ($A_\Phi \sim 7.4 \times 10^8$) and large mismatch ($r_{\rm match} \sim 3.88 \times 10^5$), preventing $|L(b)| < 0.5$.
  2. To match the recovered weights $(\lambda_1, \lambda_2, \lambda_Q)$ and suppress unwanted zeros, one must form a **signed linear combination** of explicit formulas $\Phi = \sum w_m \Phi_m$.
  3. A signed combination loses positive definiteness ($R_U \not\succeq 0$). Controlling the omitted infinite tail $\sum_{\gamma > 100} \Phi(\rho - 1/2)$ then requires unconditional two-sided bounds on the off-critical zero distribution without assuming RH.
  4. This isolates the exact open mathematical barrier: constructing an admissible signed combination whose physical transform cancels the Archimedean energy while rigorously bounding the uncontrolled off-critical spectral tail.

---

## 6. Rigorous Epistemic Separation Table

In strict compliance with Root Rule 0 of `AGENTS.md`:

| Proposition / Deliverable | Mathematical Content | Status Class | Verification / Artifact Reference |
|---|---|---|---|
| **Finite Extremal Lemma** | $\nu_b = 0 \Longrightarrow \exists a \ne c : M \tau^a = N \tau^c$ | `PROVED` | Formal Lean 4 `full_finite_extremal_grade_correlation_theorem` |
| **Authentic Non-Vanishing** | $\tau = 2\pi \Longrightarrow \nu_b \ne 0$ for all legal $b \ne 0$ | `PROVED` | Lindemann (1882); Python `compute_grouped_correlation_system` |
| **3-Coefficient Vanishing** | $c_{12} = c_{13} = c_{23} = 0 \land \sum b = 0 \implies b = 0$ | `PROVED` | Formal Lean 4 `three_coefficient_legal_vanishing` (0 sorry) |
| **Scalar Invariant $L(b) \equiv -1/2$** | $L(b) = b_1 b_2 + b_1 b_3 + b_2 b_3 = -1/2$ on legal unit sphere | `PROVED` | Formal Lean 4 `scalar_bridge_L_invariant` (0 sorry) |
| **Convolution Interpolation Enclosure** | $\|C_h - \Pi C_h\|_\infty \le (\Delta v)^2 \|\psi_h'\|_2^2 / 8 \approx 6499.10$ | `CERTIFIED_FINITE` | Python `certify_production_convolution_table` (encloses midpoint $6497.70$) |
| **Nodal Quadrature Enclosure** | 256-node Gauss-Legendre error bound on compact bump | `NUMERICALLY_UNRESOLVED` | $c_4, c_2, c_0$ literals lack 512th-derivative proof; certified flag removed |
| **1-Node Quadrature Gate** | $n_{\rm nodes} = 1$ fails closed ($1.58 \times 10^8$ error reproduced) | `REFUTED_WITHIN_SCOPE` | Status `UNCERTIFIED_UNSUPPORTED_QUADRATURE_ORDER` |
| **Spectral Span Recovery** | Critical zeros alone span $\operatorname{Sym}(2)$ (rank 3/3, res $\le 10^{-14}$) | `EMPIRICAL` | Python `investigate_scalar_spectral_bridge_target_b` |
| **Chebyshev Derivative Enclosure Refutation** | 7 Chebyshev nodes under-report supremum ($5.28 \times 10^5 < 7.28 \times 10^5$) | `REFUTED_WITHIN_SCOPE` | Counterexample at $\xi = 36.267$ on $[1.02, 41.02]$; certified flag removed |
| **Analytic Derivative Majorant** | Closed-form proved bound $\|S'(\xi)\|_2 \le \|P\|_2^2 (4 B_A B_{A'} E_0^2 + 4 B_A^2 E_0 E_1)$ | `EMPIRICAL_PROVED_BOUND` | Evaluated in `compute_critical_zero_observable` ($\approx 1.50 \times 10^{10} \ge 7.28 \times 10^5$) |
| **Arithmetic Dilation Normalization** | $W_G = P^T D (W_{\rm arch} - W_{\rm prime}) D P$ with $D = \operatorname{diag}(\tau^K)$ | `EMPIRICAL_BENCHMARK_REPRODUCED` | Benchmarks reproduced: missing dilation $\approx 1.48 \times 10^{11}$, correct $\approx 7.41 \times 10^8$ |
| **Bookkeeping Residual Balance** | $A_\Phi - L == R_\Phi - r_{\rm rec}$ identically by subtraction | `TAUTOLOGY_BOOKKEEPING` | Holds for arbitrary $A_\Phi$; independent certification flag removed |
| **Target B Admissible Realization** | Canonical bump explicit formula forces $|L(b)| < 1/2$ | `SPECIFIED_CONSTRUCTION_ANALYZED_BOUND_NOT_FORCED` | Mismatch $r_{\rm match} \approx 3.88 \times 10^5$, energy $A_\Phi \approx 7.41 \times 10^8$, deficit $\approx 6.75 \times 10^{-10}$ |
| **Spectral-Correlation Bridge** | $H \Longrightarrow \exists \text{ admissible } \Phi : |L(b)| < 1/2$ (or $\nu_b = 0$) | `NUMERICALLY_UNRESOLVED_CONSTRUCTION_INCOMPLETE` | Open research obligation under Root Rule 0 |
