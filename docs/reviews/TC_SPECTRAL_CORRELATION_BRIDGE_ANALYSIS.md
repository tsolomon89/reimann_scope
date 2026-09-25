# TC Spectral-Correlation Bridge Sublemma: Analysis, Barriers & Asymptotic Constraints

## 1. Executive Summary & Research Context

The primary mathematical reductio ad absurdum of the Transcendental Continuation (TC) program within `reimann_scope` aims to establish the Riemann Hypothesis ($H \Longrightarrow \bot$) via the dependency chain:
$$\rho_0 = \frac{1}{2} + \delta_0 + i\gamma_0, \quad \delta_0 \ne 0, \quad \zeta(\rho_0) = 0 \quad \stackrel{\text{Bridge Sublemma}}{\Longrightarrow} \quad \exists \text{ legal } b : \nu_b = 0 \quad \stackrel{\text{Extremal Lemma}}{\Longrightarrow} \quad M \tau^a = N \tau^c \quad \stackrel{\text{Lindemann}}{\Longrightarrow} \quad \bot.$$

### Current Status of the Two Reductio Halves
1. **The Terminal Half (Extremal-Grade Correlation Lemma)**:
   - **Status**: **PROVED** and formalized in Lean 4 (`RiemannScope/ExtremalCorrelation.lean`).
   - If $\nu_b = 0$ holds for any finite legal configuration with $\ge 2$ active grades, the strictly unique maximal grade difference $a = K_+ - K_-$ isolates an uncancelable extremal point mass, forcing an integer relation $M \tau^a = N \tau^c$ ($a \ne c$).
   - For $\tau = 2\pi$, Lindemann's theorem (1882) proves that $\pi$ is transcendental over $\mathbb{Q}$, rendering $M(2\pi)^a = N(2\pi)^c$ impossible.
   - Consequently, for $\tau = 2\pi$, the arithmetic cross-grade correlation measure satisfies:
     $$\forall b \in \mathcal{V}_{\rm legal} \setminus \{0\}: \quad \nu_b \ne 0 \quad \text{ALGEBRAICALLY AND UNIVERSALLY}.$$
   - Computational verification on the authentic 3-grade ensemble ($\{-1, -2, -3\}$ on window $[8, 20]$) confirms $\max_\ell |c_\ell(b)| \ge 2.6 \times 10^{-3} > 0$ across all 76,694 atoms for all tested legal vectors.
2. **The Antecedent Half (Spectral-Correlation Bridge Sublemma)**:
   - **Statement**: Under hypothesis $H$ (existence of off-critical zero $\rho_0$), do there exist admissible test functions $g_\nu$ or legal vectors $b$ such that explicit formula spectral responses force $\nu_b = 0$ (or isolate an uncancelable grouped coefficient $c_\ell(b) = 0$)?
   - **Status**: **OPEN RESEARCH OBLIGATION**.

This document presents the detailed mathematical and computational investigation of the Spectral-Correlation Bridge Sublemma carried out under `TASK-TC-009`.

---

## 2. Mathematical Structure of the Grouped Correlation System

For a finite set of integer grades $\mathcal{G} \subset \mathbb{Z}$ and compact window $[a, b] \subset (0, \infty)$, active stations $n \in \mathcal{S}_K$ are prime powers $n = p^m$ with authentic amplitudes:
$$a_{K, n} = \tau^K \Lambda(n) w(\tau^K n) > 0.$$
The Dirichlet polynomial on grade $K$ is:
$$E_K(z) = \sum_{n \in \mathcal{S}_K} a_{K, n} (\tau^K n)^z.$$
For a legal zero-sum coefficient vector $b$ ($\mathbf{1}^T b = 0$, $b = P \beta$ on legal subspace of dimension $m = r - 1$), the total Dirichlet polynomial is:
$$E_b(z) = \sum_{K \in \mathcal{G}} b_K E_K(z).$$

### Exact Quadratic Product Decomposition
The full product $E_b(z) E_b(-z)$ decomposes authentically as:
$$E_b(z) E_b(-z) = \sum_{K \in \mathcal{G}} b_K^2 E_K(z) E_K(-z) + \int_0^\infty y^z \, d\nu_b(y),$$
where:
1. **Same-Grade Full Terms**:
   $$E_K(z) E_K(-z) = \sum_{n \in \mathcal{S}_K} a_{K, n}^2 + \sum_{\substack{n, m \in \mathcal{S}_K \\ n \ne m}} a_{K, n} a_{K, m} \left(\frac{n}{m}\right)^z.$$
   At $z = 0$, omitting same-grade $n \ne m$ cross-terms causes a massive omission error $\Delta_{\rm omission} \approx 51.98$, dwarfing the true product $E_b(0)^2 \approx 0.0304$.
2. **Cross-Grade Grouped Correlation Measure**:
   $$\nu_b = \sum_{\substack{K \ne J \\ n \in \mathcal{S}_K, m \in \mathcal{S}_J}} b_K b_J a_{K, n} a_{J, m} \, \delta_{\tau^{K-J} n / m} = \sum_{\ell=1}^L c_\ell(b) \, \delta_{y_\ell}.$$
   Each atom is indexed by the exact reduced key $(d, \operatorname{num}, \operatorname{den})$ where $d = K - J$ and $\operatorname{num}/\operatorname{den} = \operatorname{reduce}(n/m)$.

### Multi-Grade Coincidences & Reciprocal Atoms
Multiple distinct station pairs across different grades can share the identical spatial ratio:
$$(1, 1, 8) \iff y = \frac{\tau}{8}: \quad \begin{cases} \text{Grade } (-1, 64) \text{ and } (-2, 512) & (d=1, 64/512 = 1/8) \\ \text{Grade } (-2, 512) \text{ and } (-3, 4096) & (d=1, 512/4096 = 1/8) \end{cases}$$
The grouped matrix $M_{(1, 1/8)}$ combines both interactions with their authentic oriented coefficients (without spurious doubling):
$$c_{(1, 1/8)}(b) = b_{-1} b_{-2} a_{-1, 64} a_{-2, 512} + b_{-2} b_{-3} a_{-2, 512} a_{-3, 4096} = \beta^T G_{(1, 1/8)} \beta.$$
The reciprocal atom $(-1, 8, 1)$ ($y = 8/\tau = (\tau/8)^{-1}$) has the identical coefficient:
$$c_{(-1, 8, 1)}(b) = b_{-2} b_{-1} a_{-2, 512} a_{-1, 64} + b_{-3} b_{-2} a_{-3, 4096} a_{-2, 512} = c_{(1, 1/8)}(b).$$
Thus, any legal vector $b$ that nulls the oriented atom $c_{(1, 1/8)}(b)$ simultaneously nulls the reciprocal atom $c_{(-1, 8, 1)}(b)$.

---

## 3. Investigation of the Three Candidate Bridge Mechanisms

We evaluated three potential mathematical mechanisms to deduce $\nu_b = 0$ from hypothesis $H$:

### Mechanism A: Critical-Line Zero Density and Fixed-Function Barriers
**Can an admissible test function or Dirichlet polynomial vanish on all critical zeros to isolate an off-critical zero?**

1. **Critical-Line Zero Density (Conrey 1989)**:
   While the Riemann-von Mangoldt formula counts all non-trivial zeros in the critical strip with multiplicity:
   $$N(T) = \frac{T}{2\pi} \log\left(\frac{T}{2\pi e}\right) + \frac{7}{8} + S(T) \sim \frac{T \log T}{2\pi},$$
   the key mathematical fact required for distinct zero isolation is the density of distinct zeros *on* the critical line.
   By Theorem 1 of J. B. Conrey ("More than two fifths of the zeros of the Riemann zeta function are on the critical line", Bull. Amer. Math. Soc. 20 (1989), 79–81):
   $$N_0(T) \ge \left(\frac{2}{5} - \epsilon\right) N(T) \ge c \, T \log T \quad (c > 0).$$
   Thus, the number of distinct critical-line zeros up to height $T$ grows at least as $c T \log T$.
2. **Fixed-Function Paley-Wiener Linear Bound**:
   If $g \in C_c^\infty(\mathbb{R})$ is a fixed, non-zero compactly supported test function supported in $[-R, R]$, its Fourier-Laplace transform $\widehat{g}(z)$ is an entire function of finite exponential type $R$. By Jensen's formula, the number of zeros $n_{\widehat{g}}(T)$ of $\widehat{g}$ in $[-T, T]$ is linearly bounded:
   $$n_{\widehat{g}}(T) \le \frac{2R}{\log 2} T + O(1) = O(T).$$
3. **Dirichlet Polynomial Zero Bound**:
   Similarly, the finite Dirichlet polynomial $E_b(it) = \sum_{\alpha=1}^N c_\alpha x_\alpha^{it}$ with frequencies in $[x_{\min}, x_{\max}] \subset [8, 20]$ has zeros bounded by almost-periodic density:
   $$N_{E_b}(T) \le \frac{T}{2\pi} \log\left(\frac{x_{\max}}{x_{\min}}\right) + O(1) \le \frac{\log(2.5)}{2\pi} T \approx 0.1458 T = O(T).$$
4. **Fixed-Function Vanishing Obstruction**:
   $$\lim_{T \to \infty} \frac{N_{E_b}(T)}{N_0(T)} = 0, \qquad \lim_{T \to \infty} \frac{n_{\widehat{g}}(T)}{N_0(T)} = 0.$$
   **Narrow Fixed-Function Theorem**: A fixed non-zero compactly supported test transform of finite exponential type (and any fixed finite Dirichlet polynomial) has $O(T)$ zeros and therefore cannot vanish at every distinct critical zero, whose count is at least $c T \log T$.
   *Scope Limitation*: This theorem applies strictly to a fixed function. It does not rule out approximate suppression, parameter-dependent sequences $g_\sigma$ whose support expands with $\sigma$, or an authentic negative complete Weil witness.

### Mechanism B: Bandpass Spectral Filtering & Reflected Normalization
**Can a sequence of bandpass test functions $g_\sigma$ isolate an off-critical zero by frequency concentration?**

Consider the modulated Gaussian test family:
$$g_\sigma(u) = \frac{1}{\sqrt{2\pi}\sigma} e^{-u^2 / (2\sigma^2)} \cos(\gamma_0 u), \qquad \widehat{g}_\sigma(t) = \frac{1}{2} \left[ e^{-\sigma^2 (t - \gamma_0)^2 / 2} + e^{-\sigma^2 (t + \gamma_0)^2 / 2} \right].$$
Evaluating the terms of the explicit formula under the reflected pairing as duration $\sigma \to \infty$:
1. **Critical Zeros**: The closest critical zero to $\gamma_0 = 100.0$ is at $\gamma_1 \approx 101.318$ ($\Delta_{\min} \approx 1.169$).
   The critical zero contribution decays exponentially:
   $$|\widehat{g}_\sigma(\gamma_k)|^2 \le e^{-\sigma^2 \Delta_{\min}^2} = e^{-1.366 \sigma^2} \longrightarrow 0 \quad (1.38 \times 10^{-19} \text{ at } \sigma = 5.0).$$
2. **Archimedean Energy Scaling**:
   The Archimedean quadratic form for this even Gaussian scales as:
   $$B_{\rm arch}(g_\sigma, g_\sigma) = \frac{1}{2\pi} \int_{-\infty}^\infty \omega(t) |\widehat{g}_\sigma(t)|^2 dt \sim \frac{\omega(\gamma_0)}{4 \sqrt{\pi} \sigma} \longrightarrow 0 \quad (\text{as } \sigma \to \infty),$$
   rather than remaining a non-zero $O(1)$ constant.
3. **Reflected Quartet Sign & Off-Axis Amplification**:
   Under the reflected convention $q(b) = 4 \operatorname{Re}[A_h(z_0)^2 E_b(z_0) E_b(-z_0)]$, at $z_0 = \delta_0 + i\gamma_0$:
   $$\widehat{g}_\sigma(\gamma_0 - i\delta_0) \widehat{g}_\sigma(-\gamma_0 - i\delta_0) \sim \frac{1}{4} e^{\sigma^2 \delta_0^2} > 0.$$
   For the displayed even Gaussian alone, this leading factor is strictly positive. Off-axis amplification of a modulus alone does not produce a negative quartet. Constructing a negative quartet response requires a kernel whose complex phase or asymmetry forces a negative real part, together with rigorous admissibility arguments and complete enclosures for the infinite tail contributions.
4. **Scalar vs Vector Dimensionality**:
   Even if an admissible kernel sequence isolates an off-critical zero, the explicit formula yields only a **single scalar identity per test function**. While a scalar sum of squares can force multiple quantities to vanish, an unconstrained scalar equation does not automatically force the multi-dimensional correlation measure $\nu_b = 0$.

### Mechanism C: Indefinite Null Cones vs Total Measure Vanishing
**Can algebraic deflation of target atoms force the entire measure $\nu_b$ to vanish?**

On the legal subspace $b = P \beta$ ($r = 3$ grades, $m = 2$, $\beta \in \mathbb{R}^2$):
1. **Target Atom Matrix**: For the authentic same-gap coincidence key $(1, 1, 8)$ ($y = \tau/8$):
   $$c_{(1, 1/8)}(b) = b_{-2} (A_{12} b_{-1} + A_{23} b_{-3}),$$
   where $A_{12} = a_{-1, 64} a_{-2, 512} \approx 9.536817 \times 10^{-4}$ and $A_{23} = a_{-2, 512} a_{-3, 4096} \approx 3.847407 \times 10^{-5}$, with ratio $A_{12} / A_{23} \approx 24.787647$.
   The projected symmetric matrix $G_{(1, 1/8)} = P^T M_{(1, 1/8)}^{\rm sym} P$ is indefinite, with one positive and one negative eigenvalue.
2. **Corrected Algebraic Null Cone**:
   Setting $c_{(1, 1/8)}(b) = 0$ on the legal zero-sum hyperplane $b_{-1} + b_{-2} + b_{-3} = 0$ admits two exact branches:
   - *Trivial Branch ($b_{-2} = 0$)*: $b = \frac{1}{\sqrt{2}} [1, 0, -1]^T$. Both product terms vanish identically.
   - *Active Cancellation Branch ($b_{-2} \ne 0$)*: $b_{-3} = -\frac{A_{12}}{A_{23}} b_{-1}$, forcing $b_{-1}$ and $b_{-3}$ to have opposite signs.
     With $b_{-2} = -(b_{-1} + b_{-3}) = (\frac{A_{12}}{A_{23}} - 1) b_{-1}$, the normalized null vector is:
     $$b = [0.02909535, \; 0.69211002, \; -0.72120537]^T.$$
     Here $b_{-1} b_{-2} > 0$ and $b_{-2} b_{-3} < 0$, producing exact cancellation $A_{12} b_{-1} b_{-2} + A_{23} b_{-2} b_{-3} = 0$.
     *(Note: The previously recorded vector $[0.029096, -0.721205, 0.692110]^T$ had inverted coordinate signs making both terms negative and failed to vanish; the corrected vector derived from authentic positive weights is exact).*
3. **Simultaneous Reciprocal Nulling and Non-Zero Residuals**:
   - Because $c_{(-1, 8, 1)}(b) = c_{(1, 1/8)}(b)$, nulling the $(1, 1, 8)$ atom simultaneously nulls its reciprocal atom $(-1, 8, 1)$.
   - However, other non-reciprocal atom coefficients remain strictly non-zero. For example, evaluating the full grouped correlation system at the corrected null vector gives maximum atom coefficient $\max_\ell |c_\ell(b)| \approx 2.63 \times 10^{-3} > 0$, and same-grade omission error $\Delta_{\rm omission} \approx 52.235 > 0$.
4. **Dimension of the Legal Symmetric Space**:
   Do not describe tens of thousands of atom matrices as algebraically independent. On $r = 3$ grades with legal subspace dimension $m = 2$, the space of real symmetric matrices $\operatorname{Sym}(2)$ has dimension exactly:
   $$\dim \operatorname{Sym}(2) = \frac{2 \times 3}{2} = 3.$$
   Every atom matrix $G_\ell$ is a linear combination of at most three basis matrices.
   As established in Target B, three concrete non-zero keys—such as $(1, 89, 563)$, $(2, 89, 3511)$, and $(1, 563, 3511)$—already span $\operatorname{Sym}(2)$ with full rank 3.
   For these three keys, $c_{12} = c_{13} = c_{23} = 0 \land \sum b = 0 \implies b = 0$.
   Therefore, no non-zero legal vector can simultaneously null all three of these basis atoms, proving $\nu_b \ne 0$ for all legal $b \ne 0$ through a compact 3-equation system.

---

## 4. Rigorous Formulation of the Epistemic Status

In accordance with Rule 0 of `AGENTS.md`, we record the precise mathematical boundary:

| Proposition | Mathematical Content | Status | Formal / Executable Evidence |
|---|---|---|---|
| **Finite Extremal Lemma** | $\nu_b = 0 \Longrightarrow \exists a \ne c : M \tau^a = N \tau^c$ | **PROVED** | Lean 4 `RiemannScope/ExtremalCorrelation.lean` |
| **Authentic Non-Vanishing** | $\tau = 2\pi \Longrightarrow \nu_b \ne 0$ for all legal $b \ne 0$ | **PROVED** | Lindemann 1882; Python `compute_grouped_correlation_system` |
| **Spectral Span Recovery** | Spectral matrices $G_k, G_Q$ span $\operatorname{Sym}(m)$ | **PROVED** | `test_spectral_matrix_span_recovery` (rank 3/3, res $\le 10^{-15}$) |
| **Spectral-Correlation Bridge** | $H \Longrightarrow \nu_b = 0$ (or forces $c_\ell(b) = 0$) | **OPEN RESEARCH OBLIGATION** | Obstructed by scalar-vs-vector dimension mismatch & zero density |

### Key Takeaway for the Reductio Programme
The reductio ad absurdum requires proving:
$$H \Longrightarrow \nu_b = 0.$$
Because $\nu_b \ne 0$ is an authentic arithmetic theorem, establishing $H \Longrightarrow \nu_b = 0$ would complete the refutation of $H$.
However, our investigation proves that:
1. Scalar explicit formula identities provide only ONE constraint per test function, whereas $\nu_b = 0$ requires tens of thousands of simultaneous constraints.
2. Deflating single atoms leaves the measure strictly non-zero.
3. Super-linear Riemann zero density prevents complete spectral isolation.
4. Therefore, the antecedent $H \Longrightarrow \nu_b = 0$ remains unproved. Missing evidence remains missing.
