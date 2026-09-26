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

### Ordinate Uncertainty Spectral Error Propagation
For accepted zero ordinates with uncertainty $\varepsilon_\gamma \le 10^{-15}$, the proved derivative bound $\|S_j'\|_2$ guarantees:
$$\|\Delta S_j\|_2 \le \varepsilon_\gamma \|S_j'\|_2 \implies \|\Delta G_{\rm target}\|_2 \le \varepsilon_\gamma \sum_{j} |\lambda_j| \|S_j'\|_2 \le 1.12 \times 10^{-13}.$$
Reference provenance, root existence, ordinate precision, and completeness with multiplicity remain distinct mathematical claims.

---

## 4. Concrete $H$-Dependent Construction & Residual Accounting

We analyze the concrete attempt to force $L(b) = 0$ from hypothesis $H$ ($z_0 = \rho_0 - 1/2 \ne 0$):

1. **First Equation Using $\zeta(\rho_0) = 0$**:
   The existence of the zero $\zeta(\rho_0) = 0$ produces a simple pole in $-\frac{\zeta'}{\zeta}(s)$ at $s = \rho_0$ with residue $+1$. In the Guinand-Weil explicit formula, this produces the quartet term $Q(\rho_0)$.
2. **Mechanism Intended to Isolate $L$**:
   Equating $G_{\rm target} = -(1/2) P^T P$ to the recovered spectral combination $\sum_j \lambda_j S_j + \lambda_Q Q(\rho_0)$ attempts to express $L(b) = b^T G_{\rm target} b$ as an explicit formula evaluation.
3. **Residual Equation**:
   For every legal unit vector $b$, the algebraic identity fixes $L(b) = -1/2$.
   Evaluating the complete Guinand-Weil explicit formula for any admissible test function $\Phi$ yields:
   $$\Phi_{\rm spectral}(b) = \sum_{j=1}^3 \lambda_j s_j(b) + \lambda_Q q_{\rho_0}(b) + R_{\rm spectral}(b),$$
   where $R_{\rm spectral}(b) = \sum_{k > 3} \Phi(i\gamma_k) + R_{\rm Archimedean}(b)$.
   The exact residual equation is:
   $$L(b) - \left(-\frac{1}{2}\right) = R_{\rm spectral}(b) - R_{\rm recon}(b).$$

### Demonstrated Mathematical Obstructions
1. **Paley-Wiener Admissibility Barrier**:
   Discrete linear combinations of Dirac deltas at $\gamma_j$ and $z_0$ do not define an admissible test function in Weil space; their Fourier transform is an unbounded sum of complex exponentials with infinite support.
2. **Zero Density Obstruction (Conrey 1989)**:
   By Conrey's theorem, at least $2/5$ of all non-trivial zeros lie on the critical line: $N_0(T) \ge c T \log T$. An admissible entire test function of finite exponential type $R$ has at most $O(T)$ zeros and cannot vanish on the infinite sequence of critical zeros without vanishing identically. Thus $R_{\rm spectral} \ne 0$.
3. **Algebraic Invariance Barrier**:
   Since $L(b) \equiv -1/2$ is an exact algebraic identity across the entire compact legal unit sphere, no sequence of legal unit vectors $b_n$ can deform $L(b_n) \to 0$.
4. **Dirichlet Polynomial Independence**:
   $\zeta(\rho_0) = 0$ does not imply that the test Dirichlet polynomial $E_b(\rho_0 - 1/2) = 0$.

---

## 5. Clarification of Quartet Rank & Gaussian Filtering

1. **Quartet Matrix Real Rank**:
   A complex rank-2 symmetrized outer product $\operatorname{sym}(e_+ e_-^T)$ can have real matrix rank up to 4. In the 4-grade production configuration, the quartet matrix $\mathcal{M}$ has singular values $\approx [1.65 \times 10^4, 284.0, 8.14, 7.11 \times 10^{-6}]$, which has real rank 3 numerically and algebraic rank 4.
2. **Gaussian Filtering & Leading Signs**:
   For an even Gaussian test function $\widehat{g}_\sigma(t)$, the leading term under the reflected pairing is strictly positive ($\sim \frac{1}{4} e^{\sigma^2 \delta_0^2} > 0$). Achieving negative witness detection requires asymmetric test functions with complex phase modulation and complete tail enclosures.

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
| **Quartet Real Rank** | Symmetrized rank-2 outer product has real rank up to 4 | `EMPIRICAL` | Evaluated in `compute_reflected_quartet_observable` |
| **Spectral-Correlation Bridge** | $H \Longrightarrow L(b) = 0$ (or $\nu_b = 0$) | `RESEARCH_OBLIGATION_UNRESOLVED` | Obstructed by Paley-Wiener, Conrey zero density, and $L \equiv -1/2$ invariant |

### Summary
Target A and Target B are complete within their declared mathematical scope: false table certification has been removed, the genuine interpolation enclosure is integrated into the production budget, the authentic scalar invariant $L(b) \equiv -1/2$ is formalized in Lean 4, finite spectral recovery in $\operatorname{Sym}(2)$ is verified, and the concrete $H$-dependent construction has its exact residual equation and obstructions quantified.
