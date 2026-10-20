# EPIC-TC-041 / TASK-TC-041 Review: Establish the TC Arithmetic–Spectral Quartet Connection and Resolve the Remainder Inequality

**Epic / Task ID**: `EPIC-TC-041` / `TASK-TC-041`  
**Starting Snapshot Audited**: `0930f714e66f721c16a048ddaa100bae3180997c`  
**Construction Gate**: `CONSTRUCTION_GATE_PASSED_WITH_EXACT_REMAINDER_IDENTITY`  
**Research Gate**: `RESEARCH_GATE_OPEN_REMAINDER_INEQUALITY_UNPROVED`  
**RH Gate**: `RH_GATE_OPEN_PENDING_NONCIRCULAR_REMAINDER_DOMINANCE`  
**Decisive Open Subgate**: `SUBGATE-TC-041B` (`TARGET_QUARTET_REMAINDER_LOWER_BOUND_SUBGATE`, Status: `OPEN`)  
**Implementation Module**: [tc/quartet_remainder_connection.py](file:///C:/Development/Projects/reimann_scope/tc/quartet_remainder_connection.py)  
**Test Suite**: [tests/test_tc_quartet_remainder_connection.py](file:///C:/Development/Projects/reimann_scope/tests/test_tc_quartet_remainder_connection.py)  
**Lean 4 Formalization**: [formal/RiemannScope/QuartetRemainderConnection.lean](file:///C:/Development/Projects/reimann_scope/formal/RiemannScope/QuartetRemainderConnection.lean) (`2` definitions + `12` theorems, `0 sorry`)  
**Reproducible Artifact**: [data/tc_quartet_remainder_connection.json](file:///C:/Development/Projects/reimann_scope/data/tc_quartet_remainder_connection.json) (`SHA256: 2f7f65a89a7ee4380ce8ac71ed60821098f98d229d8e2c6bf299c43b9084ee84`)

---

## 1. Executive Summary

`EPIC-TC-041` / `TASK-TC-041` independently derives, implements, audits, formalizes, and advances the symmetrized logarithmic-coordinate explicit-formula construction (Parts A–H) and Work Packages WP1–WP6 for the reductio:
$$H = \bigl(\exists \rho_0 = \tfrac{1}{2} + \delta + i\gamma \text{ with } \zeta(\rho_0)=0,\; 0 < \delta < \tfrac{1}{2},\; \gamma > 0\bigr) \implies \bigl[Q_\varepsilon = 0,\; Q_\varepsilon = C_\varepsilon + R_\varepsilon,\; C_\varepsilon > 0,\; R_\varepsilon > -C_\varepsilon\bigr] \implies \text{contradiction} \implies \neg H.$$

### Summary of Principal Results across WP1–WP6

1. **WP1 — Seed Construction (A)–(E) Independently Verified (`PROVED_PAPER_DERIVATION` + `CERTIFIED_FINITE` + `LEAN_PROVED` finite algebra)**:
   - **Part (A) Compact-Window Rational-Grade Separation**: On any fixed compact window $w \in C_c^\infty([-X_w, X_w])$ and rational grade difference $d = p/q \in \mathbb{Q}_{>0}$, shifting by $(h \pm d/2)L$ ($h \in \{-1,0,1\}$, $L = \log\tau = \log(2\pi)$) restricts active prime-power stations $\pm\log n$ to the finite enlarged interval $[-X_{\mathrm{shift}}-\varepsilon_0, X_{\mathrm{shift}}+\varepsilon_0]$ where $X_{\mathrm{shift}} = X_w + (1+d/2)L$. Any station collision $\xi\log n - \eta\log m = dL$ ($\xi,\eta \in \{\pm 1\}$) forces $\tau^{p/q} = m^\eta/n^\xi \in \mathbb{Q} \implies (2\pi)^p = (m^\eta/n^\xi)^q \in \mathbb{Q}$, contradicting Lindemann's theorem (1882). Thus $\Delta_{\min}(X_w, d, \varepsilon_0) > 0$, and for $0 < 2\varepsilon < \Delta_{\min}$, $Q_1 = Q_0 = Q_{-1} = 0$ and $D(P_\varepsilon, P_\varepsilon) = Q_1 + Q_{-1} - 2Q_0 = 0$ identically.
   - **Part (B) Exact Smoothed Explicit Formula**: Applying the Weil explicit formula to $f_x(u) = \psi_\varepsilon(x-u)$ ($\psi \in C_c^\infty([-1,1])$ even, nonnegative, $\int\psi=1$) yields $P_\varepsilon(x) = A_\varepsilon(x) - S_\varepsilon(x)$ with exact signs, origin constant $-(\log(2\tau)+\gamma_E)\psi_\varepsilon(x)$ where $\log(2\tau) = \log(4\pi)$, and removable singularity limit $\lim_{u\to 0^+} [\psi_\varepsilon(x-u)+\psi_\varepsilon(x+u)-2e^{-u/2}\psi_\varepsilon(x)]\frac{e^{u/2}}{e^u-e^{-u}} = \frac{1}{2}\psi_\varepsilon(x)$.
   - **Part (C) Bilinear Second Difference & Symmetrized Sum**: The ordered double sum $D(S_\varepsilon, S_\varepsilon)$ with shift factor $e^{-(dL/2)(z_\rho-z_\sigma)}$ and the symmetrized sum with $\cosh((dL/2)(z_\rho-z_\sigma))$ are identically equal because the prefactor $m_\rho m_\sigma c_\varepsilon(z_\rho)c_\varepsilon(z_\sigma)W(z_\rho+z_\sigma)T(z_\rho+z_\sigma)$ is symmetric under $(\rho,\sigma)\leftrightarrow(\sigma,\rho)$ while $z_\rho - z_\sigma$ is antisymmetric.
   - **Part (D) Admissible 6-Point Target-Quartet Filter**: Convolving any even nonnegative nonzero $w_0 \in C_c^\infty([-X_0, X_0])$ with the positive probability measures $\mu_a = \frac{1}{2}(\Delta_{-a}+\Delta_a)$ ($a = \tau/(8\gamma)$) and $\nu_b = \frac{1}{2(1+\kappa)}(\Delta_{-b}+2\kappa\Delta_0+\Delta_b)$ ($b = \tau/(4\gamma)$, $\kappa = \cosh(2\delta b)$) preserves evenness, nonnegativity, smoothness, and compact support $[-X_0-a-b, X_0+a+b]$ while placing exact transform zeros at $W(\pm 2i\gamma) = 0$ and $W(\pm 2\delta \pm 2i\gamma) = 0$.
   - **Part (E) Complete 16-Pair Target-Quartet Positivity**: Across the 16 ordered pairs of the quartet $S_0$ (with multiplicity $m \ge 1$), the 4 opposite pairs vanish via $T(0)=0$, the 4 self-pairs vanish via $W(\pm 2\delta \pm 2i\gamma)=0$, the 4 vertical pairs vanish via $W(\pm 2i\gamma)=0$, and the 4 conjugate pairs sum to
     $$C_\varepsilon := D(S_0, S_0) = 4m^2 |c_\varepsilon(\delta+i\gamma)|^2 W(2\delta)\cos(d\gamma L)\bigl[\tau^{2\delta}+\tau^{-2\delta}-2\bigr] > 0$$
     for rational $0 < d < \tau/(4\gamma L)$ and $0 < \varepsilon < \min\bigl(\tfrac{1}{2}\Delta_{\min}, |z_{\rho_0}|^{-1}\log 2\bigr)$.

2. **WP4 — Analytical & Numerical Investigation of the Remainder Inequality $R_\varepsilon > -C_\varepsilon$ (`SUBGATE-TC-041B` OPEN)**:
   - Without ever substituting the consistency identity $R_\varepsilon = -C_\varepsilon$, all four remainder pieces $D(A_\varepsilon, A_\varepsilon)$, $-2D(A_\varepsilon, S_0+S_{\mathrm{rest}})$, $2D(S_0, S_{\mathrm{rest}})$, and $D(S_{\mathrm{rest}}, S_{\mathrm{rest}})$ are assembled independently from their defining integrals and spectral sums.
   - Four analytical mechanisms explain why $R_\varepsilon > -C_\varepsilon$ is not automatically satisfied by the 6-point single-ordinate window:
     1. **Imaginary-Axis Multiplier Sign Inversion**: $T(z) = 4\sinh^2(Lz/2)$ satisfies $T(2\delta) = +4\sinh^2(\delta L) > 0$ on real conjugate sums, but $T(i\Omega) = 2\cos(\Omega L) - 2 = -4\sin^2(\Omega L/2) \le 0$ on purely imaginary critical-line zero sums $z_{\rho'} + z_{\sigma'} = i\Omega$.
     2. **Single-Ordinate Filter Leakage**: $\mu_a * \nu_b$ annihilates $\pm 2i\gamma$ and $\pm 2\delta \pm 2i\gamma$ for the single target ordinate $\gamma$, but does not annihilate critical-line ordinates $\gamma' \in Z_{\mathrm{rest}}$ or mixed frequencies $\pm\delta + i(\pm\gamma + \gamma')$.
     3. **Small-$\delta$ Quadratic Scaling Barrier ($\delta \to 0^+$)**: Because $W(\pm 2i\gamma) = 0$, $C_\varepsilon = 16m^2 L^2 |c_\varepsilon(i\gamma)|^2 W_0(0)\cos(d\gamma L)\delta^2 + O(\delta^4) = O(\delta^2)$, whereas $S_0(x) \to 4m c_\varepsilon(i\gamma)\cos(\gamma x) = O(1)$, so $-2D(A_\varepsilon, S_0)$ and $2D(S_0, S_{\mathrm{rest}})$ remain $O(1)$ as $\delta \to 0^+$.
     4. **Narrow-Smoothing Spectral Bandwidth Cost ($\varepsilon \to 0^+$)**: Enforcing $2\varepsilon < \Delta_{\min}(X_w, d, \varepsilon_0)$ broadens the passband of $c_\varepsilon(z_\rho)$ to $|\gamma_\rho| \lesssim \varepsilon^{-1}$, coupling $N(\varepsilon^{-1}) \asymp \frac{1}{2\pi\varepsilon}\log\frac{1}{\varepsilon}$ zeros into $S_{\mathrm{rest}}$.

3. **WP6 — Repair of the Earlier Reductio Interpretation (`REDUCTIO_SUBORDINATION_INTERPRETATION_CORRECTED`)**:
   - The algebraic incompatibility $[Q_\varepsilon = 0,\; Q_\varepsilon = C_\varepsilon + R_\varepsilon,\; C_\varepsilon > 0,\; R_\varepsilon > -C_\varepsilon] \implies \mathrm{False}$ is preserved (`remainder_subordination_contradiction`, `conditional_remainder_dominance_contradiction`).
   - The unsupported meta-inference that $Q_\varepsilon = 0 \land Q_\varepsilon = C_\varepsilon + R_\varepsilon \implies R_\varepsilon = -C_\varepsilon$ permanently closes the reductio route is retracted and replaced across code, Lean docstrings, and documentation by the valid conditional reductio structure $H \implies [Q_\varepsilon = 0,\; Q_\varepsilon = C_\varepsilon + R_\varepsilon,\; C_\varepsilon > 0,\; R_\varepsilon > -C_\varepsilon] \implies \text{contradiction} \implies \neg H$ (`conditional_reductio_negates_offcritical_hypothesis`).

---

## 2. WP1: Independent Derivation Audit of (A)–(E) and Contract Item 7

### 2.1 Part (A): Symmetrized Prime-Power Stations and Local Rational Separation

Let $\psi \in C_c^\infty([-1,1])$ be even, nonnegative, with $\int_{\mathbb{R}}\psi(u)\,du = 1$, and $\psi_\varepsilon(x) = \varepsilon^{-1}\psi(x/\varepsilon)$. For $x \in \mathbb{R}$,
$$P_\varepsilon(x) = \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\bigl[\psi_\varepsilon(x - \log n) + \psi_\varepsilon(x + \log n)\bigr].$$
For $w \in C_c^\infty([-X_w, X_w])$ even, nonnegative, nonzero, rational $d = p/q \in \mathbb{Q}_{>0}$, and $h \in \{-1, 0, 1\}$:
$$Q_h = \int_{-X_w}^{X_w} w(x) P_\varepsilon\bigl(x - (h + \tfrac{d}{2})L\bigr) P_\varepsilon\bigl(x - (h - \tfrac{d}{2})L\bigr)\,dx.$$
Let $X_{\mathrm{shift}} = X_w + (1 + \frac{d}{2})L$ and fix $\varepsilon_0 > 0$. Any prime power $n \ge 2$ whose $\varepsilon$-support ($\varepsilon \le \varepsilon_0$) can intersect $[-X_{\mathrm{shift}}, X_{\mathrm{shift}}]$ must satisfy $\log n \le X_{\mathrm{shift}} + \varepsilon_0$:
- **Interior stations**: $\log n \le X_{\mathrm{shift}}$;
- **Boundary stations**: $X_{\mathrm{shift}} < \log n \le X_{\mathrm{shift}} + \varepsilon_0$.

If two factors in $Q_h$ overlap at some $x \in [-X_w, X_w]$, there exist $\xi, \eta \in \{-1, +1\}$ and prime powers $m, n \le e^{X_{\mathrm{shift}}+\varepsilon_0}$ such that
$$\bigl|(\xi\log n - \eta\log m) - dL\bigr| < 2\varepsilon.$$
Exact equality $\xi\log n - \eta\log m = dL$ would imply $\tau^{p/q} = n^\xi / m^\eta \in \mathbb{Q}_{>0}$, hence $(2\pi)^p = (n^\xi/m^\eta)^q \in \mathbb{Q}$, which is impossible for $p \ne 0$ by Lindemann (1882). Since the set of enlarged stations is finite,
$$\Delta_{\min}(X_w, d, \varepsilon_0) := \min_{m, n,\, \xi, \eta} \bigl|(\xi\log n - \eta\log m) - dL\bigr| > 0.$$
For every $0 < 2\varepsilon < \Delta_{\min}(X_w, d, \varepsilon_0)$, the supports in all three integrals $Q_1, Q_0, Q_{-1}$ are strictly disjoint, proving:
$$Q_1 = Q_0 = Q_{-1} = 0, \qquad D(P_\varepsilon, P_\varepsilon) = Q_1 + Q_{-1} - 2Q_0 = 0.$$

| Control Case | Base $B$ | Rational $d$ | $X_w$ | Enlarged Stations (Int / Bound) | Certified $\Delta_{\min}$ | $\varepsilon_{\mathrm{test}}$ | $D(P_\varepsilon, P_\varepsilon)$ | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Canonical $\tau$ | $2\pi$ | $1/20$ | $0.45$ | $16$ ($14$ / $2$) | $0.0258891823 > 0$ | $0.005825$ | $0.0$ | `COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED` |
| Overlap violation | $2\pi$ | $1/20$ | $0.45$ | $18$ ($14$ / $4$) | $0.0258891823 > 0$ | $0.220000$ | $+9.921272$ | `OVERLAP_OR_COLLISION_DETECTED` |
| Rational base $B=2$ | $2$ | $1$ | $0.80$ | $10$ ($8$ / $2$) | $0.0$ ($-\log 4 + \log 2 = -d\log 2$) | $0.050000$ | $+3.468937$ | `OVERLAP_OR_COLLISION_DETECTED` |
| Generic transcendental $e$ | $e$ | $1/20$ | $0.45$ | $8$ ($6$ / $2$) | $0.0500000000 > 0$ | $0.011250$ | $0.0$ | `COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED` |

### 2.2 Part (B): Exact Smoothed Explicit Formula $P_\varepsilon = A_\varepsilon - S_\varepsilon$

Applying the Weil explicit formula (Weil 1952; Suzuki 2026 `arXiv:2606.09096v1` Section 3.1) to the translated even bump $f_x(u) = \psi_\varepsilon(x-u)$ gives:
1. **Prime-power side**: $\sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}[f_x(\log n)+f_x(-\log n)] = P_\varepsilon(x)$ since $\psi_\varepsilon$ is even.
2. **Nontrivial zero sum**: $\widehat{f_x}(z_\rho) = \int_{\mathbb{R}}\psi_\varepsilon(x-u)e^{z_\rho u}\,du = e^{z_\rho x}\int_{\mathbb{R}}\psi_\varepsilon(v)e^{-z_\rho v}\,dv = c_\varepsilon(z_\rho)e^{z_\rho x}$, so $\sum_{\rho\in Z} m_\rho \widehat{f_x}(z_\rho) = S_\varepsilon(x)$.
3. **Pole at $s=1$ and $s=0$**: $\widehat{f_x}(1/2) + \widehat{f_x}(-1/2) = c_\varepsilon(1/2)(e^{x/2}+e^{-x/2})$ since $c_\varepsilon(-1/2)=c_\varepsilon(1/2)$.
4. **Archimedean term and $\log(2\tau) = \log(4\pi)$**: With $\frac{\Gamma'}{\Gamma}(\frac{1}{4}+\frac{it}{2}) + \log\pi$ in the functional equation, standard Fourier inversion of the digamma kernel gives the origin constant $-(\log(4\pi)+\gamma_E)f_x(0) = -(\log(2\tau)+\gamma_E)\psi_\varepsilon(x)$ and the subtracted integral
   $$-\int_0^\infty \bigl[\psi_\varepsilon(x-u)+\psi_\varepsilon(x+u)-2e^{-u/2}\psi_\varepsilon(x)\bigr]\frac{e^{u/2}}{e^u-e^{-u}}\,du.$$
   As $u \to 0^+$, $\psi_\varepsilon(x-u)+\psi_\varepsilon(x+u)-2e^{-u/2}\psi_\varepsilon(x) = u\psi_\varepsilon(x) + O(u^2)$ and $\frac{e^{u/2}}{e^u-e^{-u}} = \frac{1}{2u} + O(1)$, so the integrand has the smooth finite limit $\frac{1}{2}\psi_\varepsilon(x)$ at $u = 0$.

### 2.3 Part (C)–(E): Complete 16-Pair Quartet Table and Three-Route Verification

For $z_1 = \delta+i\gamma$, $z_2 = \delta-i\gamma$, $z_3 = -\delta+i\gamma$, $z_4 = -\delta-i\gamma$ (with $\delta = 0.12$, $\gamma = 14.134725141734693$, $m = 1$, $d = 1/20 < \tau/(4\gamma L) \approx 0.060467$, $\varepsilon = 0.02$, $X_0 = 0.25$):

| Category | Ordered Pairs $(\rho, \sigma)$ | $z_\rho + z_\sigma$ | $z_\rho - z_\sigma$ | Vanishing / Value Mechanism | Sum of Category |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Opposite (4 pairs)** | $(z_1,z_4), (z_2,z_3), (z_3,z_2), (z_4,z_1)$ | $0$ | $\pm 2\delta \pm 2i\gamma$ | $T(0) = e^0 + e^0 - 2 = 0$ | $0.0$ |
| **Self (4 pairs)** | $(z_1,z_1), (z_2,z_2), (z_3,z_3), (z_4,z_4)$ | $\pm 2\delta \pm 2i\gamma$ | $0$ | $\cosh(b(\pm 2\delta \pm 2i\gamma)) + \cosh(2\delta b) = 0 \implies W = 0$ | $-3.47 \times 10^{-55}$ |
| **Vertical (4 pairs)** | $(z_1,z_3), (z_3,z_1), (z_2,z_4), (z_4,z_2)$ | $\pm 2i\gamma$ | $\pm 2\delta$ | $\cosh(a(\pm 2i\gamma)) = \cos(\pi/2) = 0 \implies W = 0$ | $+1.70 \times 10^{-55}$ |
| **Conjugate (4 pairs)** | $(z_1,z_2), (z_2,z_1), (z_3,z_4), (z_4,z_3)$ | $\pm 2\delta$ | $\pm 2i\gamma$ | $4m^2|c_\varepsilon|^2 W(2\delta)\cos(d\gamma L)(\tau^\delta-\tau^{-\delta})^2$ | $+0.21152308953867494$ |

- **Route 1 (16-pair ordered sum, $\exp$ form)**: `0.21152308953867494`
- **Route 1b (16-pair ordered sum, $\cosh$ form)**: `0.21152308953867494` (`|diff| = 3.18e-56`)
- **Route 2 (Closed formula E)**: `0.21152308953867494` (`|diff| = 3.34e-52`)
- **Route 3 (Direct spatial quadrature of $D(S_0, S_0)$)**: `0.21152308953867496` (`|diff| = 3.92e-17`)
- **Certified `flint.arb` lower bound**: `0.21152308953867494 > 0`.

### 2.4 Contract Item 7: Physical-to-Logarithmic Coordinate Relationship

Under $y = e^x \in (0,\infty)$ ($x = \log y$, $dy/y = dx$), a physical grade scale $a_K = \tau^K$ acts as $y \mapsto y/\tau^K \iff x \mapsto x - KL$. For $K_\pm = h \pm d/2$, a physical half-density profile $\Phi(y) = y^{-1/2}F(\log y)$ has grade-transported pairing
$$\int_0^\infty \widetilde{w}(y)\Phi\bigl(y\tau^{-(h+d/2)}\bigr)\Phi\bigl(y\tau^{-(h-d/2)}\bigr)\,dy = \tau^h \int_{\mathbb{R}} \widetilde{w}(e^x) F\bigl(x - (h+\tfrac{d}{2})L\bigr) F\bigl(x - (h-\tfrac{d}{2})L\bigr)\,dx.$$
Normalizing by the midpoint half-density Jacobian $\tau^{-h}$ recovers $B_h(F,F)$ in logarithmic coordinates with zero discrepancy (`abs_jacobian_error = 1.07e-50`).

---

## 3. WP4: Independent Remainder Assembly and the Four Structural Obstructions

By substituting $P_\varepsilon = A_\varepsilon - (S_0 + S_{\mathrm{rest}})$ into $D(P_\varepsilon, P_\varepsilon) = 0$, the exact remainder identity (H) is:
$$0 = D(P_\varepsilon, P_\varepsilon) = C_\varepsilon + R_\varepsilon, \qquad R_\varepsilon = \underbrace{D(A_\varepsilon, A_\varepsilon)}_{R_{AA}} \underbrace{- 2D(A_\varepsilon, S_0)}_{R_{AS_0}} \underbrace{- 2D(A_\varepsilon, S_{\mathrm{rest}})}_{R_{AS_{\mathrm{rest}}}} + \underbrace{2D(S_0, S_{\mathrm{rest}})}_{R_{0,\mathrm{rest}}} + \underbrace{D(S_{\mathrm{rest}}, S_{\mathrm{rest}})}_{R_{\mathrm{rest},\mathrm{rest}}}.$$

### 3.1 Independent Term-by-Term Evaluation (Without $R_\varepsilon := -C_\varepsilon$)

At the benchmark parameters ($\delta = 0.12$, $\gamma = 14.134725141734693$, $d = 1/20$, $X_0 = 0.25$, $\varepsilon = 0.08$, first $25$ critical-line zeros in $S_{\mathrm{rest}}$, `uses_consistency_identity_R_eq_minus_C = False`):
- $C_\varepsilon = D(S_0, S_0) = +0.19740718$
- $D(A_{\mathrm{pole}}, A_{\mathrm{pole}}) = 2 c_\varepsilon(1/2)^2 [W(1)\cos(0)\cdot 0 + W(1)T(1) + \dots] = +8.94277555$
- $R_{AA} = D(A_\varepsilon, A_\varepsilon) = +52.75537588$
- $R_{AS_0} = -2D(A_\varepsilon, S_0) = -3.97409194$
- $R_{AS_{\mathrm{rest}}} = -2D(A_\varepsilon, S_{\mathrm{rest}}) = -83.47670600$
- $R_{0,\mathrm{rest}} = +2D(S_0, S_{\mathrm{rest}}) = +2.44967838$
- $R_{\mathrm{rest},\mathrm{rest}} = D(S_{\mathrm{rest}}, S_{\mathrm{rest}}) = +25.51461915$.

### 3.2 The Four Analytical Mechanisms Governing $R_\varepsilon$

1. **Mechanism 1 — Imaginary-Axis Multiplier Sign Inversion**:
   Whereas the second-difference multiplier $T(z) = e^{Lz} + e^{-Lz} - 2 = 4\sinh^2(Lz/2)$ is strictly positive on the real conjugate sum $z_\rho + z_{\bar\rho} = 2\delta$ ($T(2\delta) = 4\sinh^2(\delta L) > 0$), on any pair of critical-line zeros $z_{\rho'} = i\gamma'$, $z_{\sigma'} = i\gamma''$ the sum $z_{\rho'} + z_{\sigma'} = i\Omega$ is purely imaginary and
   $$T(i\Omega) = 2\cos(\Omega L) - 2 = -4\sin^2\left(\frac{\Omega L}{2}\right) \le 0.$$
   Consequently, the diagonal contribution of each critical-line zero pair $\pm i\gamma'$ to $D(S_{\mathrm{rest}}, S_{\mathrm{rest}})$ is
   $$D(S_{\gamma'}, S_{\gamma'})_{\mathrm{diag}} = 2 m_{\gamma'}^2 c_\varepsilon(i\gamma')^2 W(2i\gamma') T(2i\gamma') = -8 m_{\gamma'}^2 c_\varepsilon(i\gamma')^2 W(2i\gamma')\sin^2(\gamma' L),$$
   whose sign flips wherever $W(2i\gamma')$ changes sign and is negative whenever $W(2i\gamma') > 0$.
2. **Mechanism 2 — Single-Ordinate Filter Leakage**:
   The 6-point convolution $\mu_a * \nu_b$ places zeros of $\cosh(az)$ at $z = \pm 2(2k+1)i\gamma$, annihilating $\pm 2i\gamma_1$, but for $\gamma_2 \approx 21.022040$ we have $W(2i\gamma_2) \approx -6.26 \times 10^{-3} \ne 0$ and $T(2i\gamma_2) \approx -2.596443 \ne 0$. A finite convolution filter can annihilate only finitely many independent frequencies unless its support grows unboundedly.
3. **Mechanism 3 — Small-$\delta$ Quadratic Scaling Barrier ($\delta \to 0^+$)**:
   Because $W(\pm 2i\gamma) = 0$ by construction, expanding (E) as $\delta \to 0^+$ yields
   $$C_\varepsilon = 16 m^2 L^2 |c_\varepsilon(i\gamma)|^2 W_0(0)\cos(d\gamma L)\,\delta^2 + O(\delta^4) = O(\delta^2).$$
   By contrast, $S_0(x) = 4m\operatorname{Re}(c_\varepsilon(\delta+i\gamma)\cosh((\delta+i\gamma)x)) = 4m c_\varepsilon(i\gamma)\cos(\gamma x) + O(\delta) = O(1)$, whose cross pairings $-2D(A_\varepsilon, S_0)$ and $2D(S_0, S_{\mathrm{rest}})$ evaluate $W(z)$ at $\pm\frac{1}{2} \pm i\gamma$ and $i(\pm\gamma \pm \gamma')$ where $W \ne 0$, remaining $O(1)$ as $\delta \to 0^+$:

| $\delta$ | $C_\varepsilon = D(S_0, S_0)$ | $C_\varepsilon / \delta^2$ | $2D(S_0, S_{\mathrm{rest}})$ ($10$ zeros) | $|2D(S_0, S_{\mathrm{rest}})| / C_\varepsilon$ |
| :--- | :--- | :--- | :--- | :--- |
| $0.200$ | $0.564667$ | $14.116676$ | $2.746775$ | $4.864 \times 10^0$ |
| $0.100$ | $0.136397$ | $13.639705$ | $2.774130$ | $2.034 \times 10^1$ |
| $0.050$ | $0.033806$ | $13.522524$ | $2.780942$ | $8.226 \times 10^1$ |
| $0.010$ | $0.001349$ | $13.485199$ | $2.783120$ | $2.064 \times 10^3$ |
| $0.001$ | $1.3484 \times 10^{-5}$ | $13.483661$ | $2.783210$ | $2.064 \times 10^5$ |

4. **Mechanism 4 — Narrow-Smoothing Spectral Bandwidth Cost ($\varepsilon \to 0^+$)**:
   Enforcing $0 < 2\varepsilon < \Delta_{\min}(X_w, d, \varepsilon_0)$ requires $\varepsilon \le 0.012945$ at $d = 1/20, X_w \in [0.317, 0.667]$, which widens the Fourier passband of $c_\varepsilon(z_\rho) = \widehat{\psi}(\varepsilon z_\rho)$ to $|\gamma_\rho| \lesssim \varepsilon^{-1} \approx 77.25$, admitting $N(\varepsilon^{-1}) \approx 19$ nontrivial zero pairs before rapid decay begins.

---

## 4. WP5: Lean 4 Formalization Scope (`formal/RiemannScope/QuartetRemainderConnection.lean`)

| # | Declaration Name | Kind | Formalized Statement | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `quartetRadialFactor` | `def` | $\tau_\delta^2 + \tau_\delta^{-2} - 2$ | Compiled (`0 sorry`) |
| 2 | `quartet_radial_factor_eq_sq` | `theorem` | $\tau_\delta \tau_\delta^{-1} = 1 \implies \tau_\delta^2 + \tau_\delta^{-2} - 2 = (\tau_\delta - \tau_\delta^{-1})^2$ | Compiled (`0 sorry`) |
| 3 | `quartet_radial_sq_pos` | `theorem` | $\tau_\delta \ne \tau_\delta^{-1} \implies 0 < (\tau_\delta - \tau_\delta^{-1})^2$ | Compiled (`0 sorry`) |
| 4 | `ordered_pair_symmetrized_cosh_equivalence` | `theorem` | $P_{rs} = P_{sr} \wedge E_+ + E_- = 2C_{\cosh} \implies P_{rs}E_+ + P_{sr}E_- = P_{rs}C_{\cosh} + P_{sr}C_{\cosh}$ | Compiled (`0 sorry`) |
| 5 | `sixteen_pair_quartet_block_reduction` | `theorem` | Vanishing of 4 opposite, 4 self, and 4 vertical pairs reduces the 16-pair sum to $4 c_{\mathrm{conj}}$ | Compiled (`0 sorry`) |
| 6 | `targetQuartetContribution` | `def` | $4 m^2 c_{\mathrm{abs}}^2 W_{2\delta}\cos(d\gamma L)(\tau_\delta - \tau_\delta^{-1})^2$ | Compiled (`0 sorry`) |
| 7 | `sixteen_pair_target_quartet_pos` | `theorem` | $m>0 \wedge c_{\mathrm{abs}}\ne 0 \wedge W_{2\delta}>0 \wedge \cos(d\gamma L)>0 \wedge \tau_\delta\ne\tau_\delta^{-1} \implies C_\varepsilon > 0$ | Compiled (`0 sorry`) |
| 8 | `sixteen_pair_multiplicity_scaling` | `theorem` | $C_\varepsilon(m) = m^2 C_\varepsilon(1)$ | Compiled (`0 sorry`) |
| 9 | `sixteen_pair_critical_line_vanishing` | `theorem` | $\tau_\delta = \tau_\delta^{-1} \implies C_\varepsilon = 0$ | Compiled (`0 sorry`) |
| 10 | `elementary_bump_nonvanishing_from_bound` | `theorem` | $1 - c_{\mathrm{abs}} \le B_{\mathrm{dev}} \wedge B_{\mathrm{dev}} < 1 \implies 0 < 1 - B_{\mathrm{dev}} \le c_{\mathrm{abs}}$ | Compiled (`0 sorry`) |
| 11 | `critical_line_multiplier_nonpos` | `theorem` | $-4\sin^2(\gamma' L) \le 0$ | Compiled (`0 sorry`) |
| 12 | `exact_remainder_consistency_identity` | `theorem` | $Q_\varepsilon = 0 \wedge Q_\varepsilon = C_\varepsilon + R_\varepsilon \implies C_\varepsilon + R_\varepsilon = 0 \wedge R_\varepsilon = -C_\varepsilon$ | Compiled (`0 sorry`) |
| 13 | `conditional_remainder_dominance_contradiction` | `theorem` | $Q_\varepsilon = 0 \wedge Q_\varepsilon = C_\varepsilon + R_\varepsilon \wedge C_\varepsilon > 0 \wedge R_\varepsilon > -C_\varepsilon \implies \mathrm{False}$ | Compiled (`0 sorry`) |
| 14 | `conditional_reductio_negates_offcritical_hypothesis` | `theorem` | $(H \to \exists Q_\varepsilon, C_\varepsilon, R_\varepsilon,\; Q_\varepsilon = 0 \wedge Q_\varepsilon = C_\varepsilon + R_\varepsilon \wedge C_\varepsilon > 0 \wedge R_\varepsilon > -C_\varepsilon) \to \neg H$ | Compiled (`0 sorry`) |

---

## 5. Primary Literature & arXiv Audit Table (`literature-search-arxiv`)

| Reference | Title / Venue | arXiv / DOI | Role in `EPIC-TC-041` |
| :--- | :--- | :--- | :--- |
| A. Weil (1952) | *Sur les "formules explicites" de la théorie des nombres premiers*, Comm. Sém. Math. Univ. Lund, 252–265 | Classical primary source | Exact distributional explicit formula for prime powers, poles, and archimedean digamma functional |
| F. Lindemann (1882) | *Über die Zahl $\pi$*, Math. Ann. 20, 213–225 | Classical primary source | Transcendence of $\tau = 2\pi$, proving $\tau^d \notin \mathbb{Q}$ for all $d \in \mathbb{Q} \setminus \{0\}$ |
| M. Suzuki (2026) | *Weil's quadratic form via the screw function* | [https://arxiv.org/abs/2606.09096v1](https://arxiv.org/abs/2606.09096v1) | Multiplicity-weighted explicit formula $W(f) = \sum_\gamma m_\gamma \widetilde{f}(\gamma)$ and compact-support kernel representation |
| J.-F. Burnol (1998/2001) | *The Explicit Formula in Simple Terms* / *An invariant subspace of theilah space* | [https://arxiv.org/abs/math/9810169v2](https://arxiv.org/abs/math/9810169v2), [https://arxiv.org/abs/math/0101068v1](https://arxiv.org/abs/math/0101068v1) | Multiplicative-to-additive logarithmic coordinates and self-dual explicit formula conventions |
| A. Connes, C. Consani, M. Marcolli (2007) | *The Weil proof and the geometry of the adeles class space* | [https://arxiv.org/abs/math/0703392v1](https://arxiv.org/abs/math/0703392v1) | Semilocal explicit formula and compact-support test function cutoff analysis |
| A. Connes, C. Consani, H. Moscovici (2025) | *Zeta zeros and prolate wave operators* | [https://arxiv.org/abs/2511.22755](https://arxiv.org/abs/2511.22755) | UV/IR compact-support localization vs. spectral passband tradeoff |
| R. Shi (2026) | *On the Positivity of Weil's Quadratic Form* | [https://arxiv.org/abs/2609.04908v1](https://arxiv.org/abs/2609.04908v1) | Explicit prime/archimedean/pole decomposition for compactly supported smooth test functions |
