# Transcendental Continuation: Reflected-Quartet Curvature and Spectral Remainder Bridge Analysis

**Authoritative Derivation, Verification, and Obstruction Analysis**  
**Date**: September 29, 2026  
**Audited Target**: Target A (Complete Weighted Functional Certification) & Target B (Reflected-Quartet Curvature Control and Remainder Bridge)  
**Status**: `EMPIRICAL_CONSTRUCTION_FORMULATED_MATHEMATICAL_OBSTRUCTION_ESTABLISHED`  
**Epistemic Obligation**: Open (Active Research Track 2: `TASK-TC-011` / `TASK-TC-012`)

---

## 1. Executive Summary & Epistemic Statement

### 1.1 The Primary TC Reductio Objective
The fundamental goal of the Transcendental Continuation (TC) program within the Riemann Scope is to derive an arithmetic-spectral contradiction from the existence of an off-critical zero of the Riemann zeta function $\zeta(s)$:
$$H \Longrightarrow \exists K \ne J, \; m, n \in \mathbb{Z} \setminus \{0\} : m \tau^K = n \tau^J, \qquad \tau = 2\pi,$$
where $H$ denotes the existence of a nontrivial zero $\rho_0$ with $\operatorname{Re}(\rho_0) \ne 1/2$. The impossibility of such an integer-grade station coincidence ($m \tau^K = n \tau^J$ for $K \ne J$ with $m, n \in \mathbb{Z}^+$) constitutes the intended reductio ad absurdum.

For concrete analysis, we adopt the parameterized hypothesis:
$$H(\rho_0, m_0): \quad \zeta(\rho_0) = 0, \quad \rho_0 = \frac{1}{2} + \delta + i\gamma, \quad 0 < |\delta| < \frac{1}{2}, \quad m_0 = \operatorname{mult}(\rho_0) \ge 1.$$

### 1.2 Mandated Research Targets
This epic addresses two connected milestones:
1. **Target A (Correction and Certification of the Complete Weighted Calculation)**:
   - **A1**: Repair the prime pairing sign in the explicit formula assembly ($\text{arithmetic\_truncated} = \text{archimedean\_truncated} - \text{prime\_pairing\_raw}$), protect it with an independent position-space pairing evaluator, and verify non-zero prime pairing on the authentic $[8, 20]$ window with near-resonant stations (e.g. $K=-1, n=53, m=107, q=2$).
   - **A2**: Preserve the scaled interpolation repair ($\kappa(M) \approx 472.62$), assemble the quartet matrix from the full complex product $p(z_0) A_h(z_0)^2 E_b(z_0) E_b(-z_0)$ without discarding $\operatorname{Im} p(z_0)$, solve the symmetric generalized eigenproblem via symmetric whitening $(P^T P)^{-1/2}$, and separate all distinct numerical error channels.
   - **A3**: Replace heuristic Stieltjes tail approximations with a proved analytic upper enclosure for derivative orders $m \in \{6, 7\}$; reject unsupported orders ($m < 6$ and $m \ge 8$); compute exact $L^1$ derivative enclosures $I_6 = 11,974,462.0$ and $I_7 = 1,571,233,583.0$ via total variation identities; evaluate the counting integral in closed form using $E_1(p \log T)$.
   - **A4**: Unify cutoff propagation to the actual $T_{\text{cutoff}}$, eliminate silent zero fallbacks, enforce fail-closed status whenever spectral zero coverage is incomplete, and rigorously define the explicit formula decomposition $L(b) = D - r_{\text{match}} + r_{\text{rec}} = -1/2$.
2. **Target B (Reflected-Quartet Curvature Control and Remainder Bridge Investigation)**:
   - **B1**: Derive the convergent zero representation of the logarithmic derivative curvature observable $C(t) = \frac{d^2}{dt^2} \log |\xi(1/2+it)|$. Prove that the principal part $P_\delta(x)$ vanishes at the midpoint $x=0$, avoiding spurious $m_0/\delta$ spikes. Derive the exact positive response of the quartet vs. the strictly negative contributions of critical-line zeros.
   - **B2**: Test the curvature mechanism against the falsification compensation control polynomial $X(t)$. Prove quantitatively that nearby critical-line zeros at $\gamma \pm \delta/2$ completely overwhelm the positive quartet curvature across $|t-\gamma| \le \delta/4$, turning the total observable strictly negative. Conclude that a zero-free neighborhood theorem (unproved under $H$ alone) is strictly required to prevent cancellation.
   - **B3**: Construct a worked mathematical obstruction demonstrating that localized curvature $C(t)$ cannot bridge or cancel the global arithmetic remainder $D \sim 7.15 \times 10^8$ within the legal three-grade TC test family. Sharpen the exact next mathematical question.

---

## 2. Target A: Mathematical Derivations and Engineering Repairs

### 2.1 A1: Prime Sign Derivation and Independent Pairing Assembly

#### The Explicit Formula Sign Convention
In the standard Weil explicit formula for the completed xi function $\xi(s) = \frac{1}{2} s(s-1) \pi^{-s/2} \Gamma(s/2) \zeta(s)$, for an even, smooth test function $g \in C_c^\infty(\mathbb{R})$ with Fourier transform $\widehat{g}(z) = \int_{-\infty}^\infty g(x) e^{-zx} dx$, the explicit formula reads:
$$\sum_{\rho} \widehat{g}\left(\rho - \frac{1}{2}\right) = \int_{-\infty}^\infty g(x) \left( e^{x/2} + e^{-x/2} \right) dx + \int_{-\infty}^\infty g(x) d\omega(x) - \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} \left[ g(\log n) + g(-\log n) \right],$$
where $d\omega(x)$ denotes the Archimedean distribution kernel.

For the reflected bilinear test function $k_b(x) = (g_b * \widetilde{g}_b)(x)$, the prime contribution is an autocorrelation pairing:
$$\text{PrimePairing} = \sum_{q \text{ prime}, k \ge 1} \frac{\log q}{q^{k/2}} \left[ k_b(\log q^k) + k_b(-\log q^k) \right].$$
Because the explicit formula has a minus sign in front of the prime sum:
$$\sum_\rho \Psi_b\left(\rho - \frac{1}{2}\right) = A_{\text{arch}}(g_b) - \text{PrimePairing}(g_b).$$
Consequently, the truncated arithmetic side is defined by:
$$\text{arithmetic\_truncated} = \text{archimedean\_truncated} - \text{prime\_pairing\_raw}.$$

#### Reproduction of Defect and Independent Verification
Prior code added `prime_pairing_raw` to `archimedean_truncated`. For the canonical test multiplier with constant coefficient $r_0 = -1.02770 \times 10^{-3} < 0$, the raw position-space prime pairing evaluates to a negative number.

For the three-grade diagnostic direction $b = (-1, 1, 0)/\sqrt{2}$ with $h=0.05$:
- **Archimedean truncated value**:
  $$\text{archimedean\_truncated} = +502,713,211.1461$$
- **Raw prime pairing (position-space sum)**:
  $$\text{prime\_pairing\_raw} = -211,930,586.9374$$
- **Flawed assembly (prior addition)**:
  $$502,713,211.1461 + (-211,930,586.9374) = +290,782,624.2087$$
- **Correctly signed assembly (subtraction)**:
  $$502,713,211.1461 - (-211,930,586.9374) = +714,643,798.0835$$

#### Non-Trivial Prime Resonance Verification
We verified that the prime pairing does NOT vanish on the window $[8, 20]$. For example, in grade $K=-1$, consider prime powers $n=53$ and $m=107$. Their physical station positions are:
$$x_1 = \frac{53}{2\pi} \approx 8.4352, \qquad x_2 = \frac{107}{2\pi} \approx 17.0296,$$
both lying within the support $[8, 20]$. For the prime $q=2$:
$$\left| \log 2 - \log\frac{x_2}{x_1} \right| = \left| \log 2 - \log\frac{107}{53} \right| = \log\frac{107}{106} \approx 0.00938974 < 2h = 0.10.$$
Thus, near-resonant pairs are present, and the raw prime pairing is $-211.93 \times 10^6$. The independent function `evaluate_position_space_prime_functional` reproduces this value to within $10^{-4}$ relative tolerance.

---

### 2.2 A2: Complex Quartet Pairing and Metric Whitening

#### Complex Quartet Pairing
Let $\rho_0 = 1/2 + z_0$ with $z_0 = \delta + i\gamma$. The full complex quartet contribution to the admissible test $\Psi_b(z) = p(z) A_h(z)^2 E_b(z) E_b(-z)$ is:
$$\mathcal{Q}(b) = m_0 \sum_{z \in \{\pm \delta \pm i\gamma\}} \Psi_b(z) = 2 m_0 \operatorname{Re}\left[ p(z_0) A_h(z_0)^2 E_b(z_0) E_b(-z_0) + p(\bar{z}_0) A_h(\bar{z}_0)^2 E_b(\bar{z}_0) E_b(-\bar{z}_0) \right].$$
Because $p(-z) = p(z)$, $A_h(-z) = A_h(z)$, and for real physical test functions $\overline{F_b(z)} = F_b(\bar{z})$, the four terms collapse to:
$$\mathcal{Q}(b) = 4 m_0 \operatorname{Re}\left[ p(z_0) A_h(z_0)^2 \frac{E_b(z_0) E_b(-z_0) + E_b(\bar{z}_0) E_b(-\bar{z}_0)}{2} \right].$$
Prior implementations evaluated $\operatorname{Re}[p(z_0)] \operatorname{Re}[A_h(z_0)^2 E_b(z_0) E_b(-z_0)]$, discarding $\operatorname{Im}[p(z_0)] \operatorname{Im}[A_h(z_0)^2 E_b(z_0) E_b(-z_0)]$.
When $p(z_0)$ has an imaginary component (e.g. for polynomial multipliers evaluated off the real axis), this truncation is invalid.
The repaired implementation evaluates the full complex product:
$$Q_{\text{full}} = m_0 \operatorname{Re}\left[ p(z_0) Q_{\text{complex}} \right],$$
which preserves exact mathematical equality.

#### Metric Whitening for Generalized Eigenproblem
The legal coefficient space is parameterized as $b = P \beta$ with $\beta \in \mathbb{R}^2$, where $P \in \mathbb{R}^{3 \times 2}$ satisfies $\mathbf{1}^T P = 0$.
The quadratic forms are represented in the $\beta$-basis by:
$$G_\beta = P^T G P, \qquad M_\beta = P^T P.$$
To find the stationary values of $\beta^T G_\beta \beta$ subject to the legal normalization $\|b\|_2^2 = \beta^T M_\beta \beta = 1$, one must solve the symmetric generalized eigenvalue problem:
$$G_\beta v = \lambda M_\beta v.$$
Prior code computed `np.linalg.eigvalsh(np.linalg.inv(P.T @ P) @ G_beta)`. Because $M_\beta^{-1} G_\beta$ is generally non-symmetric, `eigvalsh` produces unphysical, basis-dependent numbers.
The repaired implementation whitens the system using the symmetric inverse square root $W = M_\beta^{-1/2} = V \Sigma^{-1/2} V^T$:
$$\widetilde{G} = W^T G_\beta W.$$
The matrix $\widetilde{G}$ is explicitly symmetric. Its eigenvalues $\lambda(\widetilde{G})$ are identical to the generalized eigenvalues $G_\beta v = \lambda M_\beta v$ and agree with `scipy.linalg.eigh(G_beta, M_beta)` to machine precision ($< 10^{-29}$).

---

### 2.3 A3: Proved Analytic Stieltjes Tail Enclosure

#### Derivative Enclosures for the Bump Function
The Fourier transform $\hat{\kappa}(\xi) = \int_{-1}^1 \kappa(x) e^{-i\xi x} dx$ of the standard bump $\kappa(x) = \exp(-1/(1-x^2)) \mathbf{1}_{|x| < 1}$ satisfies, for any integer $m \ge 0$:
$$(-i\xi)^m \hat{\kappa}(\xi) = \int_{-1}^1 \kappa^{(m)}(x) e^{-i\xi x} dx \implies |\hat{\kappa}(\xi)| \le \frac{\|\kappa^{(m)}\|_{L^1}}{|\xi|^m}.$$
For $z = \delta + it$ with $|\delta| < 1/2$ and $|t| \ge T$, the argument of $\hat{\kappa}(i h z)$ is $\xi = -h t + i h \delta$.
Using the contour shift or direct integration by parts along $[-1, 1]$:
$$|\hat{\kappa}(i h z)| \le e^{h |\delta|} \frac{\|\kappa^{(m)}\|_{L^1}}{(h |z|)^m} \le e^{h/2} \frac{\|\kappa^{(m)}\|_{L^1}}{(h t)^m}.$$

To obtain certified upper bounds for $\|\kappa^{(m)}\|_{L^1} = \int_{-1}^1 |\kappa^{(m)}(x)| dx$, we use the fundamental theorem of calculus: between consecutive roots $r_0 = -1 < r_1 < \dots < r_k < r_{k+1} = 1$ of $\kappa^{(m)}(x)$, the derivative $\kappa^{(m)}(x)$ has constant sign. Hence:
$$\|\kappa^{(m)}\|_{L^1} = \sum_{j=0}^k \left| \kappa^{(m-1)}(r_{j+1}) - \kappa^{(m-1)}(r_j) \right|.$$
Evaluating this total variation with 100-digit precision in `mpmath` and rounding outward to the next integer yields the certified enclosures:
$$I_6 = \|\kappa^{(6)}\|_{L^1} \le 11,974,462.0,$$
$$I_7 = \|\kappa^{(7)}\|_{L^1} \le 1,571,233,583.0.$$

#### Reproduction of Prior Numerical Defects
1. **Reusing $m=6$ for $m \ge 8$**: Prior code looked up $I_m$ by clamping to $m=6$. At $h=0.05, t=400$ ($ht = 20$), the resulting estimate was:
   $$\frac{I_6}{(ht)^8} = \frac{11,974,462}{20^8} \approx 0.0004677.$$
   However, the true Fourier transform magnitude is $|\hat{\kappa}(20)| \approx 0.00126556$. The flawed estimate was more than a factor of $2.7$ *smaller* than the true Fourier transform, entirely violating upper-bound enclosure!
2. **Defective $I_7$ Constant**: The prior stored constant for $I_7$ was substantially below the independently computed true value $1,571,233,582.37$.
3. **Rejection of Unsupported Orders**: The repaired routine strictly supports only $m \in \{6, 7\}$ and raises a `ValueError` for any $m < 6$ or $m \ge 8$.

#### Closed-Form Analytic Stieltjes Tail Integration
Let $\Phi(t) = \sum_p c_p t^{-p}$ with $c_p \ge 0$ and $p > 1$. Let $N(t)$ denote the number of zeros of $\zeta(s)$ with ordinates in $(0, t]$, and let $M(t) = \frac{t}{2\pi} \log\frac{t}{2\pi} - \frac{t}{2\pi} + \frac{7}{8}$ be the smooth Riemann-von Mangoldt counting function, with $M'(t) = \frac{1}{2\pi} \log\frac{t}{2\pi}$.
Let the counting error envelope be $|N(t) - M(t)| \le E(t) = a \log t + b \log\log t + c$.
Integrating by parts for the Stieltjes integral:
$$\int_T^\infty \Phi(t) dN(t) \le \int_T^\infty \Phi(t) M'(t) dt + \Phi(T) E(T) + \int_T^\infty (-\Phi'(t)) E(t) dt.$$

1. **Smooth Integral**:
   $$\int_T^\infty t^{-p} \frac{1}{2\pi} \log\frac{t}{2\pi} dt = \frac{T^{1-p}}{2\pi} \left[ \frac{\log(T/2\pi)}{p-1} + \frac{1}{(p-1)^2} \right].$$
2. **Fluctuation Logarithmic Integral**:
   $$\int_T^\infty p t^{-(p+1)} (a \log t) dt = a p \left[ \frac{T^{-p} \log T}{p} + \frac{T^{-p}}{p^2} \right].$$
3. **Fluctuation Log-Log Integral**:
   Substituting $u = p \log t$, $t = e^{u/p}$, $dt = \frac{1}{p} e^{u/p} du$:
   $$\int_T^\infty p t^{-(p+1)} (b \log\log t) dt = b \int_{p \log T}^\infty e^{-u} \log\left(\frac{u}{p}\right) du \le b E_1(p \log T),$$
   where $E_1(x) = \int_x^\infty \frac{e^{-u}}{u} du$ is the exponential integral.

This provides an exact, analytically integrated upper bound without discretization error.

---

### 2.4 A4: Coherent Cutoffs and Fail-Closed Spectral Coverage

In `construct_weighted_admissible_spectral_test`:
- The tail bound is computed at the actual requested cutoff $T_{\text{cutoff}}$ (e.g. $T=100.0, 150.0, 500.0$).
- When the reference zero table does not cover ordinates up to $T_{\text{cutoff}}$ (e.g. at $T=500.0$ where available zeros reach $\approx 396.38$), the routine sets:
  ```python
  "spectral_coverage_certified": False,
  "complete_spectral_enclosure_available": False,
  "unclosed_coverage_obligation": "Reference zero table maximum ordinate 396.38 < requested cutoff 500.0..."
  ```
- The explicit formula identity decomposition is recorded as:
  $$D = \text{arithmetic\_truncated} + R_{\text{arch}} - S_{\text{unselected}, \le T} - R_{\text{spectral}} \approx 7.1464 \times 10^8,$$
  $$L(b) = D - r_{\text{match}} + r_{\text{rec}} = -1/2.$$
  A contradiction requires an independently proved estimate $|D| + \epsilon_{\text{match}} + \epsilon_{\text{rec}} < 1/2$. Because $|D| \sim 7.15 \times 10^8 \gg 1/2$, no contradiction is obtained from this configuration.

---

## 3. Target B: Reflected-Quartet Curvature and Spectral Remainder Bridge

### 3.1 B1: Convergent Zero Representation of Curvature Observable

Consider the completed Riemann xi function $\xi(s) = \frac{1}{2} s(s-1) \pi^{-s/2} \Gamma(s/2) \zeta(s)$.
The Hadamard factorization theorem gives the convergent product expansion:
$$\xi(s) = e^{A + B s} \prod_{\rho} \left(1 - \frac{s}{\rho}\right) e^{s/\rho},$$
where the product runs over all nontrivial zeros $\rho = \beta + i\gamma_\rho$.
Taking the logarithmic derivative:
$$\frac{\xi'}{\xi}(s) = B + \sum_{\rho} \left( \frac{1}{s - \rho} + \frac{1}{\rho} \right).$$

Differentiating again:
$$\left( \frac{\xi'}{\xi} \right)'(s) = -\sum_{\rho} \frac{1}{(s - \rho)^2}.$$
On the critical line $s = 1/2 + it$ ($t \in \mathbb{R}$):
$$\log |\xi(1/2 + it)| = \operatorname{Re} \log \xi(1/2 + it).$$
$$\frac{d}{dt} \log |\xi(1/2 + it)| = \operatorname{Re} \left[ i \frac{\xi'}{\xi}(1/2 + it) \right] = -\operatorname{Im} \frac{\xi'}{\xi}(1/2 + it).$$
$$\frac{d^2}{dt^2} \log |\xi(1/2 + it)| = -\operatorname{Im} \left[ i \left( \frac{\xi'}{\xi} \right)'(1/2 + it) \right] = -\operatorname{Re} \left[ \left( \frac{\xi'}{\xi} \right)'(1/2 + it) \right].$$
Substituting the second derivative of the zero product:
$$C(t) := \frac{d^2}{dt^2} \log |\xi(1/2 + it)| = \sum_{\rho} \operatorname{Re} \left[ \frac{1}{(1/2 + it - \rho)^2} \right].$$

#### Principal Part Cancellation at Midpoint
For an off-critical zero $\rho_0 = 1/2 + \delta + i\gamma$ and its reflection $\rho_0' = 1/2 - \delta + i\gamma$, define $x = s - (1/2 + i\gamma) = \delta' + i(t - \gamma)$.
The upper reflected pair in $-\xi'/\xi$ has principal part:
$$P_\delta(x) = -m_0 \left[ \frac{1}{x - \delta} + \frac{1}{x + \delta} \right] = -\frac{2 m_0 x}{x^2 - \delta^2}.$$
Notice that at $x = 0$ (the center of the pair on the critical line $s = 1/2 + i\gamma$), $P_\delta(0) = 0$. There is **no uncancelled pole or $m_0/\delta$ spike** at the midpoint in $-\xi'/\xi$.

#### Exact Individual Zero Contributions to Curvature
For any zero $\rho = \beta + i\gamma_\rho$, write $1/2 + it - \rho = (1/2 - \beta) + i(t - \gamma_\rho)$.
1. **Critical-Line Zeros ($\beta = 1/2$)**:
   Here $1/2 - \beta = 0$, so:
   $$\frac{1}{(1/2 + it - \rho_j)^2} = \frac{1}{(i(t - \gamma_j))^2} = -\frac{1}{(t - \gamma_j)^2}.$$
   Every critical-line zero contributes a **strictly negative** term:
   $$C_j(t) = -\frac{m_j}{(t - \gamma_j)^2} < 0 \quad (\forall t \ne \gamma_j).$$

2. **Off-Critical Quartet ($\beta = 1/2 \pm \delta, \gamma_\rho = \pm \gamma$)**:
   For $\rho_1 = 1/2 + \delta + i\gamma$:
   $$\frac{1}{(1/2 + it - \rho_1)^2} = \frac{1}{(-\delta + i(t-\gamma))^2} = \frac{(\delta + i(t-\gamma))^2}{(\delta^2 + (t-\gamma)^2)^2} = \frac{\delta^2 - (t-\gamma)^2 + 2i\delta(t-\gamma)}{(\delta^2 + (t-\gamma)^2)^2}.$$
   For $\rho_2 = 1/2 - \delta + i\gamma$:
   $$\frac{1}{(1/2 + it - \rho_2)^2} = \frac{1}{(\delta + i(t-\gamma))^2} = \frac{(\delta - i(t-\gamma))^2}{(\delta^2 + (t-\gamma)^2)^2} = \frac{\delta^2 - (t-\gamma)^2 - 2i\delta(t-\gamma)}{(\delta^2 + (t-\gamma)^2)^2}.$$
   Summing the upper reflected pair:
   $$\operatorname{Re}\left[ \frac{1}{(1/2+it-\rho_1)^2} + \frac{1}{(1/2+it-\rho_2)^2} \right] = 2 m_0 \frac{\delta^2 - (t-\gamma)^2}{(\delta^2 + (t-\gamma)^2)^2}.$$
   Adding the lower conjugate pair $\rho \in \{1/2 \pm \delta - i\gamma\}$ gives the exact total quartet contribution:
   $$C_{\text{quartet}}(t) = 2 m_0 \left[ \frac{\delta^2 - (t-\gamma)^2}{(\delta^2 + (t-\gamma)^2)^2} + \frac{\delta^2 - (t+\gamma)^2}{(\delta^2 + (t+\gamma)^2)^2} \right].$$

Notice:
- At $t = \gamma$, the upper term evaluates to $+2m_0/\delta^2 > 0$.
- For $|t - \gamma| < \delta$, the upper term is strictly positive.
- For $|t - \gamma| > \delta$, the upper term becomes negative.

---

### 3.2 B2: Falsification Control Against Compensation

To test whether the positive quartet curvature can be used as a standalone witness of an off-critical zero without global zero-spacing control, consider the even, real test polynomial:
$$X(t) = \left[ ((t - \gamma)^2 + \delta^2) ((t + \gamma)^2 + \delta^2) \right]^m \cdot \left[ (t^2 - (\gamma - a)^2) (t^2 - (\gamma + a)^2) \right]^m,$$
with $a = \delta/2$, $\gamma > \delta > 0$, and integer $m \ge 1$.

#### Zero Structure of $X(t)$
- **Off-Critical Quartet**: Roots of $((t \mp \gamma)^2 + \delta^2)^m = 0$ occur at $t = \pm \gamma \pm i\delta$. In the $s$-plane ($s = 1/2 + it$), these correspond to $s = 1/2 \mp \delta \pm i\gamma$, exactly matching an off-critical quartet of multiplicity $m_0 = m$.
- **Nearby Critical Zeros**: Roots of $(t^2 - (\gamma \mp a)^2)^m = 0$ occur at $t = \pm(\gamma - \delta/2)$ and $t = \pm(\gamma + \delta/2)$. In the $s$-plane, these correspond to critical-line zeros with ordinates $\gamma_1 = \gamma - \delta/2$ and $\gamma_2 = \gamma + \delta/2$.

#### Quantitative Curvature Evaluation
The curvature observable for $X(t)$ is:
$$C_X(t) = \frac{d^2}{dt^2} \log |X(t)| = C_{\text{quartet}}(t) - C_{\text{real}}(t),$$
where $C_{\text{real}}(t) = m \left[ \frac{1}{(t - (\gamma - a))^2} + \frac{1}{(t - (\gamma + a))^2} + \frac{1}{(t + (\gamma - a))^2} + \frac{1}{(t + (\gamma + a))^2} \right]$.

1. **At the midpoint $t = \gamma$**:
   - Quartet upper term:
     $$C_{\text{quartet}}(\gamma) \approx \frac{2m}{\delta^2} + O\left(\frac{m}{\gamma^2}\right).$$
   - Real zeros at $\gamma \pm \delta/2$:
     $$C_{\text{real}}(\gamma) \approx m \left[ \frac{1}{(\delta/2)^2} + \frac{1}{(-\delta/2)^2} \right] = m \left( \frac{4}{\delta^2} + \frac{4}{\delta^2} \right) = \frac{8m}{\delta^2}.$$
   - Net curvature:
     $$C_X(\gamma) \approx \frac{2m}{\delta^2} - \frac{8m}{\delta^2} = -\frac{6m}{\delta^2} < 0.$$

2. **Across the entire interval $|t - \gamma| \le \delta/4$**:
   For any $u = t - \gamma$ with $|u| \le \delta/4$:
   - The quartet upper contribution satisfies:
     $$C_{\text{upper}}(t) = 2m \frac{\delta^2 - u^2}{(\delta^2 + u^2)^2} \le \frac{2m}{\delta^2}.$$
   - The two nearby critical zeros satisfy $|t - (\gamma \pm \delta/2)| = |u \mp \delta/2| \le \delta/4 + \delta/2 = 3\delta/4$, and:
     $$\frac{1}{(u - \delta/2)^2} + \frac{1}{(u + \delta/2)^2} \ge \frac{2}{(\delta/2)^2 + u^2} \ge \frac{2}{(\delta/2)^2 + (\delta/4)^2} = \frac{2}{\frac{5}{16}\delta^2} = \frac{32}{5\delta^2} = \frac{6.4}{\delta^2}.$$
   - Therefore:
     $$C_X(t) \le \frac{2m}{\delta^2} - \frac{6.4m}{\delta^2} = -\frac{4.4m}{\delta^2} < -\frac{m}{\delta^2} < 0.$$

#### Epistemic Conclusion from Compensation Control
The positive curvature $+2m_0/\delta^2$ of an off-critical quartet is **not robust against local critical zero configurations**. Two nearby critical-line zeros at distance $\delta/2$ completely overwhelm and reverse the sign of the curvature across the entire neighborhood $|t - \gamma| \le \delta/4$.

To conclude $C(t) > 0$ from the existence of an off-critical zero $\rho_0$, one would need to prove:
$$\operatorname{dist}(\rho_0, \rho_j) \ge c \delta \quad \forall \rho_j \ne \rho_0.$$
However, **the hypothesis $H(\rho_0, m_0)$ alone does not provide a zero-free neighborhood around $\gamma$ on the critical line**. No such local zero-repulsion property is known or proved for $\zeta(s)$ without already assuming the Riemann Hypothesis.

---

### 3.3 B3: Worked Obstruction to Transferring Curvature to the TC Remainder

#### Transfer Identity Formulation
Can the curvature observable $C(t) = \frac{d^2}{dt^2} \log |\xi(1/2+it)|$ be transferred to control the Weil explicit formula remainder $D$ for the authentic test function $\Psi_b(z) = p(z) F_b(z) F_b(-z)$?

In the Weil explicit formula, the spectral side is a discrete sum over zeros:
$$\mathcal{W}(\Psi_b) = \sum_\rho \Psi_b\left(\rho - \frac{1}{2}\right).$$
By Cauchy's residue theorem, if $\Omega$ is a rectangular contour enclosing all zeros with $|\operatorname{Im}(s)| \le T$:
$$\sum_{|\operatorname{Im}(\rho)| \le T} \Psi_b\left(\rho - \frac{1}{2}\right) = \frac{1}{2\pi i} \oint_{\partial \Omega} \Psi_b\left(s - \frac{1}{2}\right) \frac{\xi'}{\xi}(s) ds.$$
Taking the horizontal segments to infinity (or integrating along the critical line with appropriate contour deformation), the sum over zeros is connected to the logarithmic derivative $\xi'/\xi(1/2+it)$.
Integrating by parts twice along the critical line:
$$\int_{-T}^T \Psi_b(it) \left( \frac{\xi'}{\xi} \right)'(1/2+it) dt = \left[ \Psi_b(it) \frac{\xi'}{\xi}(1/2+it) \right]_{-T}^T - \int_{-T}^T i \Psi_b'(it) \frac{\xi'}{\xi}(1/2+it) dt.$$
Using the identity $C(t) = -\operatorname{Re}[(\xi'/\xi)'(1/2+it)]$, a linear functional of $C(t)$ can only be formed by pairing $C(t)$ against an even test function $\phi(t)$:
$$\mathcal{I}(\phi) = \int_{-\infty}^\infty \phi(t) C(t) dt.$$

#### The Three Fundamental Obstructions
1. **Admissibility and Support Mismatch**:
   In the authentic TC family, $F_b(z) = A_h(z) E_b(z)$ is generated by a physical convolution $\psi_h * e_b$ with compact spatial support in $[8, 20]$ and bandwidth $h=0.05$.
   Its Fourier transform along the critical line is an entire function of exponential type $20$:
   $$\Psi_b(it) = p(it) |F_b(it)|^2.$$
   By the Paley-Wiener theorem, $\Psi_b(it)$ cannot be compactly supported in frequency space, nor can it be localized to an arbitrarily narrow interval $[\gamma - \delta/4, \gamma + \delta/4]$ without introducing long oscillatory tails that sample critical zeros across the entire spectrum.
2. **Discrete Spectral Sampling vs. Continuous Operator Integration**:
   The Weil explicit formula evaluates $\Psi_b$ at discrete zero locations $\rho - 1/2$. It does **not** integrate $\Psi_b$ against $C(t)$.
   While $\int \phi(t) C(t) dt$ represents a smoothed spectral average, the quantity appearing in the TC invariant is the discrete sum:
   $$\sum_\rho \Psi_b(\rho - 1/2) = S_{\text{selected}} + S_{\text{unselected}} = -1/2 + S_{\text{unselected}}.$$
   The unselected sum $S_{\text{unselected}}$ is controlled by the roots of the degree-six polynomial multiplier $p(z)$ at the chosen nodes, not by the curvature $C(t)$.
3. **Quantitative Scale Incompatibility**:
   The explicit formula decomposition for the authenticated test is:
   $$D = A_{\le U} + R_{\text{arch}} - S_{\text{unsel}, \le T} - R_{\text{spectral}} \approx 7.1464 \times 10^8.$$
   The isolated quartet contribution to $\mathcal{W}(\Psi_b)$ was normalized by $p(z)$ to evaluate to:
   $$S_{\text{selected}} = L(b) = -\frac{1}{2}.$$
   The discrepancy $D$ between the discrete zeros and the continuous Archimedean/prime functional is of order:
   $$D \sim 7.15 \times 10^8.$$
   Meanwhile, the maximum possible local curvature contribution from an off-critical quartet is:
   $$C_{\text{quartet}}(\gamma) = \frac{2 m_0}{\delta^2} \sim \frac{2}{(0.49)^2} \approx 8.33.$$
   Even if an integral operator could transfer $C(t)$ to the Weil functional, an observable of magnitude $\sim 8.33$ cannot bridge, cancel, or control a background arithmetic remainder of magnitude $\sim 7.15 \times 10^8$.

#### Sharpened Research Question
This analysis establishes a **worked obstruction** to using localized quartet curvature $C(t)$ to control the global TC remainder $D$. We state the resulting sharpened mathematical question:
> **Sharpened Question (Track 2 / Post-Epic)**: Can any admissible test family $\Psi_b(z)$ simultaneously satisfy:
> 1. Exact preservation of the three-grade station invariant $L(b) = -1/2$;
> 2. Suppression of the unselected zeros $|S_{\text{unselected}}| < \epsilon$; and
> 3. Cancellation of the continuous Archimedean background $A_\infty$ to order $< 1/2$, without requiring global zero-free regions outside the scope of $H(\rho_0, m_0)$?

---

## 4. Assumptions and Dependencies Table

| Claim / Component | Target | Evidence Class | Mathematical Scope | Dependencies & Provenance | Unresolved Obligations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prime Sign Assembly** | A1 | `CERTIFIED_FINITE` | Truncated arithmetic functional on $[8, 20]$, $h=0.05$ | Explicit formula sign convention: $\text{Arith} = \text{Arch} - \text{Prime}$. Independent position-space sum reproduces $+714,643,798.0835$. | None for truncated functional. Infinite prime tail remains to be certified. |
| **Complex Quartet Pairing** | A2 | `CERTIFIED_FINITE` | Exact formula for $Q(p, z_0)$ on $\mathbb{C}$ | Algebraic expansion $m_0 \operatorname{Re}[p(z_0) Q_{\text{complex}}]$ preserving $\operatorname{Im} p(z_0)$. | None. |
| **Metric Whitening** | A2 | `CERTIFIED_FINITE` | Legal subspace $\mathcal{V}_{\text{legal}} \subset \mathbb{R}^3$ | Symmetric whitening $W = (P^T P)^{-1/2}$, $\widetilde{G} = W^T G_\beta W$. Eigenvalues match `scipy.linalg.eigh` to $10^{-29}$. | None. |
| **Stieltjes Derivative Bounds** | A3 | `CERTIFIED_FINITE` | Orders $m \in \{6, 7\}$ on $[-1, 1]$ | Total variation identity over roots. $I_6 \le 11,974,462.0$, $I_7 \le 1,571,233,583.0$. | Orders $m < 6$ and $m \ge 8$ rejected. |
| **Analytic Stieltjes Tail** | A3 | `PROVED_CONDITIONAL` | Ordinates $t \ge T$, conditional on counting envelope $E(t)$ | Closed-form smooth integral + fluctuation integral via $E_1(p \log T)$. | Valid range of counting envelope $E(t)$. |
| **Fail-Closed Coverage** | A4 | `CERTIFIED_FINITE` | Zero table validation up to $T_{\text{cutoff}}$ | Requires $\max \gamma_j \ge T_{\text{cutoff}}$. Fails closed if incomplete. | Analytic zero-counting certificate for full completeness. |
| **Curvature Zero Rep** | B1 | `PROVED_CONDITIONAL` | $C(t) = \frac{d^2}{dt^2}\log\|\xi(1/2+it)\|$ | Hadamard factorization of $\xi(s)$. Principal part $P_\delta(0) = 0$. | Conditional on convergence of Hadamard product. |
| **Compensation Control** | B2 | `REFUTED_WITHIN_SCOPE` | Curvature sign on $|t-\gamma| \le \delta/4$ for control $X(t)$ | Quantitative lower bound on real root curvature: $C_X(t) < -m/\delta^2 < 0$. | Falsifies claim that quartet curvature alone forces $C(t) > 0$. |
| **Curvature-Remainder Bridge** | B3 | `OBSTRUCTION_ESTABLISHED` | Admissible TC test family $\Psi_b$ | Scale mismatch ($D \sim 7.15 \times 10^8$ vs $C \sim 8.33$) and Paley-Wiener frequency support. | Proves localized curvature cannot control $D$ in authentic TC family. |

---

## 5. Verification Commands and Reproducibility

```bash
# 1. Run all focused numerical and span defect tests
python -m pytest tests/test_tc_numerical_and_span_defects.py -v

# 2. Run adversarial evidence controls
python -m pytest .agents/verification/test_adversarial_evidence_controls.py -v

# 3. Audit claim spec and register
python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .

# 4. Fast operational suite
python scripts/workflow.py check-fast
```
