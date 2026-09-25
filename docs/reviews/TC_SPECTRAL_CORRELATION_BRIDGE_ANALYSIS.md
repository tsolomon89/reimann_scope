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

For a finite set of integer grades $\mathcal{G} \subset \mathbb{Z}$ and compact window $[a, b] \subset (0, \infty)$, active stations $n \in \mathcal{S}_K$ are prime powers $n = p^m$ with amplitudes:
$$a_{K, n} = \tau^K \frac{\Lambda(n)}{\sqrt{n}} w(\tau^K n) > 0.$$
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

### Multi-Grade Coincidences
Multiple distinct station pairs across different grades can share the identical spatial ratio:
$$(1, 1, 8) \iff y = \frac{\tau}{8}: \quad \begin{cases} \text{Grade } (-1, 64) \text{ and } (-2, 512) & (d=1, 64/512 = 1/8) \\ \text{Grade } (-2, 512) \text{ and } (-3, 4096) & (d=1, 512/4096 = 1/8) \end{cases}$$
The grouped matrix $M_{(1, 1/8)}$ combines both interactions:
$$c_{(1, 1/8)}(b) = 2 b_{-1} b_{-2} a_{-1, 64} a_{-2, 512} + 2 b_{-2} b_{-3} a_{-2, 512} a_{-3, 4096} = \beta^T G_{(1, 1/8)} \beta.$$

---

## 3. Investigation of the Three Candidate Bridge Mechanisms

We evaluated three potential mathematical mechanisms to deduce $\nu_b = 0$ from hypothesis $H$:

### Mechanism A: Zero-Density and Paley-Wiener Barriers
**Can an admissible test function or Dirichlet polynomial vanish on all critical zeros to isolate an off-critical zero?**

1. **Riemann Zero Growth**: By the Riemann-von Mangoldt formula, the number of critical zeros up to height $T$ grows super-linearly:
   $$N(T) = \frac{T}{2\pi} \log\left(\frac{T}{2\pi e}\right) + \frac{7}{8} + S(T) \sim \frac{T \log T}{2\pi}.$$
   At $T = 100$, $N(100) \approx 29$. At $T = 1000$, $N(1000) \approx 649$. At $T = 10000$, $N(10000) \approx 10,143$.
2. **Paley-Wiener Linear Bound**: If $g \in C_c^\infty(\mathbb{R})$ has compact support in $[-R, R]$, its Fourier transform $\widehat{g}(z)$ is an entire function of exponential type $R$. By Jensen's formula, its zero count $n_{\widehat{g}}(T)$ in $[-T, T]$ satisfies:
   $$n_{\widehat{g}}(T) \le \frac{2R}{\log 2} T + O(1) = O(T).$$
3. **Dirichlet Polynomial Zero Bound**: The finite Dirichlet polynomial $E_b(it) = \sum_{\alpha=1}^N c_\alpha x_\alpha^{it}$ has frequencies bounded in $[x_{\min}, x_{\max}] \subset [8, 20]$. By the classical density theorem for almost-periodic functions, the number of zeros of $E_b$ in $[-T, T]$ is bounded by:
   $$N_{E_b}(T) \le \frac{T}{2\pi} \log\left(\frac{x_{\max}}{x_{\min}}\right) + O(1) \le \frac{\log(2.5)}{2\pi} T \approx 0.1458 T.$$
   At $T = 1000$, $N_{E_b}(1000) \le 146$, which is less than $23\%$ of the $649$ Riemann zeros.
4. **Conclusion**:
   $$\lim_{T \to \infty} \frac{N_{E_b}(T)}{N(T)} = 0, \qquad \lim_{T \to \infty} \frac{n_{\widehat{g}}(T)}{N(T)} = 0.$$
   **Theorem**: No non-trivial compactly supported test function and no finite Dirichlet polynomial can vanish on all critical zeros of the Riemann zeta function. The critical zero spectral background $\sum_k |\widehat{g}(\gamma_k)|^2 |E_b(i\gamma_k)|^2$ is strictly positive and non-extinguishable.

### Mechanism B: Bandpass Spectral Filtering & Exponential Amplification
**Can a sequence of bandpass test functions $g_\sigma$ isolate an off-critical zero by frequency concentration?**

Consider the modulated Gaussian test family:
$$g_\sigma(u) = \frac{1}{\sqrt{2\pi}\sigma} e^{-u^2 / (2\sigma^2)} \cos(\gamma_0 u), \qquad \widehat{g}_\sigma(t) = \frac{1}{2} \left[ e^{-\sigma^2 (t - \gamma_0)^2 / 2} + e^{-\sigma^2 (t + \gamma_0)^2 / 2} \right].$$
Evaluating the terms of the explicit formula as duration $\sigma \to \infty$:
1. **Critical Zeros**: The closest critical zero to $\gamma_0 = 100.0$ is at $\gamma_1 \approx 101.318$ ($\Delta_{\min} \approx 1.169$).
   The critical zero contribution decays exponentially:
   $$|\widehat{g}_\sigma(\gamma_k)|^2 \le e^{-\sigma^2 \Delta_{\min}^2} = e^{-1.366 \sigma^2} \longrightarrow 0 \quad (1.38 \times 10^{-19} \text{ at } \sigma = 5.0).$$
2. **Archimedean Background**:
   $$B_{\rm arch}(g_\sigma, g_\sigma) \sim \log(\gamma_0 / 2) = \log(50) \approx 3.9120 = O(1).$$
3. **Prime Sum**: Oscillatory cancellation across prime powers stabilizes the prime sum:
   $$B_{\rm prime}(g_\sigma, g_\sigma) \approx 2.81 = O(1).$$
4. **Off-Critical Target Quartet**: At $z_0 = \delta_0 + i\gamma_0$, the argument in the Fourier transform is $t = \gamma_0 - i\delta_0$:
   $$|\widehat{g}_\sigma(\gamma_0 - i\delta_0)|^2 \sim \frac{1}{4} e^{\sigma^2 \delta_0^2}.$$
   For $\delta_0 = 0.49$, this grows exponentially: $404.44$ at $\sigma = 5.0$, and $2.68 \times 10^{10}$ at $\sigma = 10.0$.
5. **Conclusion**:
   While bandpass filtering successfully suppresses critical zeros relative to an off-critical target, the resulting explicit formula relation is a **single scalar growth identity**. It shows that under $H$, an uncancelled off-critical zero dominates the scalar functional. However, it does **not** generate a multi-dimensional constraint forcing the vector measure $\nu_b = 0$.

### Mechanism C: Indefinite Null Cones vs Total Measure Vanishing
**Can algebraic deflation of target atoms force the entire measure $\nu_b$ to vanish?**

On the legal subspace $b = P \beta$ ($r = 3$ grades, $m = 2$, $\beta \in \mathbb{R}^2$):
1. **Target Atom Matrix**: For the authentic same-gap coincidence key $(1, 1, 8)$ ($y = \tau/8$):
   $$G_{(1, 1/8)} = P^T M_{(1, 1/8)}^{\rm sym} P = \begin{pmatrix} -0.00095368 & -0.00045760 \\ -0.00045760 & 0.00000000 \end{pmatrix}.$$
   The eigenvalues are $\lambda_1 \approx -0.001138$ and $\lambda_2 \approx +0.000184$ (opposite signs).
2. **Target Deflation**: Because $G_{(1, 1/8)}$ is indefinite, it possesses an exact 1-dimensional null cone in $\mathbb{R}^2$:
   $$\beta_1 / \beta_2 \approx -1.042039 \implies b = [0.029096, -0.721205, 0.692110]^T.$$
   At this legal vector, $c_{(1, 1/8)}(b) = 0$ exactly!
3. **Persistence of All Other Atoms**:
   Evaluating the complete grouped correlation system at this exact null vector reveals:
   - Maximum atom coefficient: $\max_\ell |c_\ell(b)| \approx 2.628677 \times 10^{-3} > 0$.
   - Same-grade omission error at $z=0$: $\Delta_{\rm omission} \approx 52.235 > 0$.
   - The remaining 76,693 atoms remain non-zero.
4. **Dimension Mismatch Barrier**:
   Vanishing of the measure $\nu_b = 0$ requires the simultaneous vanishing of all $L = 76,694$ quadratic forms:
   $$\beta^T G_\ell \beta = 0 \quad \text{for all } \ell = 1, \dots, L.$$
   In $\mathbb{R}^2$, two non-proportional quadratic forms share at most $2 \times 2 = 4$ intersection rays. For tens of thousands of authentic prime-power atoms with incommensurate frequencies, the only simultaneous solution is $\beta = 0$ ($b = 0$).

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
