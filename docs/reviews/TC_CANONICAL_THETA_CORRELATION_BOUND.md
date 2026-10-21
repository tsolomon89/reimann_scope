# Canonical Theta Correlation Bound: Arithmetic Derivation, Certified Tests, and Proof Attempt (`EPIC-TC-042` / `TASK-TC-042` / `TASK-TC-042R` / `TASK-TC-042R2`)

## 1. Executive Summary & Status Separation

This document records the complete mathematical derivation, seed defect repair, closed-form multiplicative autocorrelation theorem, exact rational Bernstein weighted kernel envelopes, fixed-seed Riemann Hypothesis equivalence proof, certified arbitrary-precision evaluations, `TASK-TC-042R` and `TASK-TC-042R2` certification/formalization repairs, $\tau$-scaling controls, Lean 4 formalization, and arithmetic proof attempts (including `SUBGATE-TC-042A` and the simplified uniform prime-wavelet boundedness target `SUBGATE-TC-042B`) for **`EPIC-TC-042` / `TASK-TC-042` / `TASK-TC-042R` / `TASK-TC-042R2`**:

$$
C_\tau(0) \ge 0, \qquad |C_\tau(K)| \le C_\tau(0) \quad \forall K \in \overline{\mathbb{Q}} \cap \mathbb{R}, \qquad \tau = 2\pi,
$$

where $C_\tau(K) := W_\xi(h_K)$ is the completed Riemann explicit-formula functional evaluated on the grade-shifted multiplicative autocorrelation $h_K := (T_K \psi_\tau) * \psi_\tau^*$ of the fixed squared pole-regularized theta state $\psi_\tau(x) = x^{1/2}\Phi_1^{(2)}(x)$.

| Dimension | Classification / Status | Scope & Evidence |
| :--- | :--- | :--- |
| **Implementation Status** | `IMPLEMENTED_AND_VERIFIED` | [`tc/canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py), [`tests/test_tc_canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_canonical_theta_correlation_bound.py), [`data/tc_canonical_theta_correlation_bound.json`](file:///c:/Development/Projects/reimann_scope/data/tc_canonical_theta_correlation_bound.json) |
| **Seed Defect Repair (`Section 2`)** | `SEED_DEFECT_REPRODUCED_AND_REPAIRED` | Exact operator derivation $\Phi_t^{(2)}(x) = P(D)^2 G_t(x) = t^{1/4}(r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r)e^{-r}$, repairing the `TC-036R` display typo $r^4 - 6r^3 + \frac{45}{8}r^2 - \frac{3}{8}r$ |
| **Closed-Form Autocorrelation & Bernstein Envelopes (`Section 3`)** | `CLOSED_FORM_AUTOCORRELATION_PROVED` / `BERNSTEIN_KERNEL_ENVELOPES_EXACT_RATIONAL_CERTIFIED` | Exact rational-algebraic formula $h_K(x) = h_0(\tau^K x)$ in $W_\alpha = (\alpha + \alpha^{-1})^2$ (distinct from the prime wavelet sum $W(X)$), eighth-order Euler differential representation, and exact rational Bernstein polynomial certificates for $|g^{(m)}(v)| \le |g^{(m)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ ($m \in \{0,2,4,6,8\}$) and $|\tilde{h}_0(\alpha)| \le \frac{1032993}{65536}(\alpha+\alpha^{-1})^{-5/2}$ |
| **Fixed-Seed RH Equivalence (`Sections 4 & 5`)** | `FIXED_SEED_RH_EQUIVALENCE_PROVED` | Complete Laplace-resolvent proof that $C_\tau(0) \ge 0 \wedge |C_\tau(K)| \le C_\tau(0)\;(\forall K \in \overline{\mathbb{Q}}\cap\mathbb{R}) \Longleftrightarrow \text{RH}$ (and more generally $\exists M < \infty : |C_\tau(K)| \le M \Longleftrightarrow \text{RH}$) |
| **Numerical Certification (`Sections 5 & 6`, repaired in `TASK-TC-042R` / `TASK-TC-042R2`)** | `FINITE_GRID_CORRELATION_BOUND_CERTIFIED` | 256-bit FLINT/Arb ball enclosures with outward-rounded `arb.str(15, radius=True)` strings across 14 discrete grades, 512-arc Cauchy circle Taylor remainder bound, `analytic=analytic` branch-cut checking, outward-rounded `flint.arb_mat.det()` Sylvester Gram minors, and derived uniform archimedean integral bound $\le 4.448357 < 4.95$ ($|W_{\mathrm{arch}}(h_K)| \le 5.994279\;\forall K\in\mathbb{R}$) |
| **Local Origin Concavity (`Section 5.3`, repaired in `TASK-TC-042R` / `TASK-TC-042R2`)** | `LOCAL_ORIGIN_CONCAVITY_CERTIFIED` | Certified $C_\tau(0) > 0$, $C_\tau'(0) = 0$, $C_\tau''(0) \approx -0.641739 < 0$, $C_\tau^{(4)}(0) \approx +433.541309 > 0$, scoped sixth-derivative bound $\sup_{|K|\le 0.08}|C_\tau^{(6)}(K)| \le M_6^{\mathrm{arith}} = 27971954.786589753$, and certified exact-rational local intervals $0 < |K| \le 1/20 = 0.05$ for $|C_\tau(K)| < C_\tau(0)$ and $0 \le |K| \le 9/200 = 0.045$ for $C_\tau(K) > 0$ (100% zero-free arithmetic route; lower-bound polynomial roots $0.045776$ for $C_\tau(K) > 0$ and $0.051486$ for $|C_\tau(K)| < C_\tau(0)$) and $0 < |K| \le 17/250 = 0.068$ for $|C_\tau(K)| < C_\tau(0)$ and $0 \le |K| \le 1/20 = 0.05$ for $C_\tau(K) > 0$ (unconditional spectral-tail route; lower-bound polynomial roots $0.050851$ for $C_\tau(K) > 0$, $0.068465$ for $|C_\tau(K)| < C_\tau(0)$, and $0.133277$ for $C_\tau(K) < C_\tau(0)$) |
| **Stieltjes Multiscale Reduction (`Section 7`, repaired in `TASK-TC-042R2`)** | `STIELTJES_IDENTITY_REPAIRED_AND_CERTIFIED` | Removed the extraneous $X^{-1/2}$ factor from the $x$-variable integral, fixed the denominator exponent of $(D_\alpha h_0)(\alpha)$ to $(\alpha+\alpha^{-1})^{19/2}$, and certified both Form (A) (in $x$) and Form (B) (in $\alpha = x/X$) against the finite-cutoff sum at $B = 50$ for $X \in \{1, 4, 100\}$ to $< 3 \times 10^{-31}$ |
| **Universal Arithmetic Inequality (`Section 7`)** | `UNIVERSAL_ARITHMETIC_CORRELATION_BOUND_OPEN` | Isolated as `SUBGATE-TC-042A` and reduced to `SUBGATE-TC-042B` (`UNIFORM_REFLECTED_PRIME_WAVELET_BOUNDEDNESS_SUBGATE`): $\exists M < \infty \; \forall X \ge 1 : |W(X)| := |\sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n/X)| \le M$ |
| **Formalization Coverage (`Section 8`, expanded in `TASK-TC-042R2`)** | `FORMALIZED_IN_LEAN4_ZERO_SORRY` | [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean): **11 definitions**, **20 theorems**, 0 `sorry`, 0 `admit` (formalizing exact algebraic identities, conditional Taylor/Laplace/Stieltjes implication schemas, and endpoint polynomials; analytic integration and Arb enclosures reside in Python/FLINT) |
| **Independent Review Status** | `AWAITING_INDEPENDENT_REVIEW` | Mathematical status separated from structural and test execution |

---

## 2. Exact Seed Object, Operator Polynomial Repair, and Mellin Transform $F_\tau(s)$

### 2.1 Operator Definition and Reproduction of the `TC-036R` Display Defect

Let $\tau = 2\pi$, $L = \log \tau = \log(2\pi)$, $D = t \frac{d}{dt}$, and
$$
G_t(x) = t^{1/4} \exp\!\left(-\frac{\tau}{2} t x^2\right) = t^{1/4} e^{-r}, \qquad r := \frac{\tau}{2} t x^2 = \pi t x^2 \quad (x > 0, \; t > 0),
$$
$$
P(D) := D^2 - \frac{1}{16} = \left(D - \frac{1}{4}\right)\left(D + \frac{1}{4}\right), \qquad \Phi_t^{(2)}(x) := P(D)^2 G_t(x), \qquad \psi_\tau(x) := x^{1/2} \Phi_1^{(2)}(x).
$$

Because $D(r) = r$ and $D(e^{-r}) = -r e^{-r}$, the action of $D = t\frac{d}{dt}$ on $t^{1/4} p(r) e^{-r}$ for any polynomial $p(r)$ is given by the algebraic step operator
$$
D\bigl(t^{1/4} p(r) e^{-r}\bigr) = t^{1/4} \left[\left(\frac{1}{4} - r\right)p(r) + r p'(r)\right] e^{-r}.
$$

Applying $P(D) = D^2 - \frac{1}{16}$ twice yields:
1. **First application ($p_0(r) = 1$)**:
   - $D(t^{1/4} e^{-r}) = t^{1/4}(\frac{1}{4} - r)e^{-r}$,
   - $D^2(t^{1/4} e^{-r}) = t^{1/4}\bigl((\frac{1}{4} - r)^2 - r\bigr)e^{-r} = t^{1/4}(r^2 - \frac{3}{2}r + \frac{1}{16})e^{-r}$,
   - $P(D)G_t(x) = t^{1/4} P_1(r) e^{-r}$ with
     $$
     P_1(r) = r^2 - \frac{3}{2}r.
     $$
2. **Second application ($P_1(r) = r^2 - \frac{3}{2}r$, $P_1'(r) = 2r - \frac{3}{2}$)**:
   - $D(t^{1/4} P_1(r) e^{-r}) = t^{1/4}\bigl(-r^3 + \frac{15}{4}r^2 - \frac{15}{8}r\bigr)e^{-r}$,
   - $D^2(t^{1/4} P_1(r) e^{-r}) = t^{1/4}\bigl(r^4 - 7r^3 + \frac{83}{8}r^2 - \frac{75}{32}r\bigr)e^{-r}$,
   - Subtracting $\frac{1}{16} P_1(r) = \frac{1}{16}r^2 - \frac{3}{32}r$:
     $$
     \boxed{\Phi_t^{(2)}(x) = P(D)^2 G_t(x) = t^{1/4} P_2(r) e^{-r}, \qquad P_2(r) = r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r.}
     $$

### 2.2 Rising-Pochhammer Mellin Proof and Diagnosis of the Defective Polynomial

For any polynomial $\sum_{j=1}^4 p_j r^j$ with $r = (\tau/2) x^2$ at $t = 1$, substituting $x = ((\tau/2)^{-1} r)^{1/2}$ ($dx/x = \frac{1}{2} dr/r$) gives
$$
\int_0^\infty r^j e^{-r} x^{s-1}\,dx = \frac{1}{2}\left(\frac{\tau}{2}\right)^{-s/2} \Gamma\!\left(\frac{s}{2} + j\right) = \frac{1}{2}\left(\frac{\tau}{2}\right)^{-s/2} \Gamma\!\left(\frac{s}{2}\right) \left(\frac{s}{2}\right)_j,
$$
where $(u)_j = u(u+1)\cdots(u+j-1)$ is the rising Pochhammer symbol.
- For the **exact** coefficients $(p_1, p_2, p_3, p_4) = (-9/4, 41/4, -7, 1)$ with $u = s/2$:
  $$
  \sum_{j=1}^4 p_j (u)_j = -\frac{9}{4}u + \frac{41}{4}u(u+1) - 7u(u+1)(u+2) + u(u+1)(u+2)(u+3) = u^2\left(u - \frac{1}{2}\right)^2 = \frac{s^2(s-1)^2}{16},
  $$
  so multiplying by $\frac{1}{2}(\tau/2)^{-s/2}\Gamma(s/2)$ yields
  $$
  \boxed{F_\tau(s) := \int_0^\infty \Phi_1^{(2)}(x) x^{s-1}\,dx = \frac{s^2(s-1)^2}{32}\left(\frac{\tau}{2}\right)^{-s/2}\Gamma\!\left(\frac{s}{2}\right), \qquad \widehat{\psi_\tau}(z) = F_\tau\!\left(\frac{1}{2} + z\right).}
  $$
- By contrast, for the `TC-036R` display typo $(p_1^{\mathrm{def}}, p_2^{\mathrm{def}}, p_3^{\mathrm{def}}, p_4^{\mathrm{def}}) = (-3/8, 45/8, -6, 1)$:
  $$
  \sum_{j=1}^4 p_j^{\mathrm{def}} \left(\frac{s}{2}\right)_j = \frac{s^4}{16} - \frac{11}{32}s^2 - \frac{3}{8}s,
  $$
  which at $s = 1$ evaluates to $\frac{1}{16} - \frac{11}{32} - \frac{3}{8} = -\frac{21}{32} \ne 0$, failing to annihilate the $s = 1$ pole! Both [`tc/modular_theta_conductor_curvature.py`](file:///c:/Development/Projects/reimann_scope/tc/modular_theta_conductor_curvature.py) and [`docs/reviews/TC_MODULAR_THETA_CONDUCTOR_CURVATURE.md`](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_MODULAR_THETA_CONDUCTOR_CURVATURE.md) have been repaired to use $r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r$, and this identity is formally verified in Lean 4 theorems `seed_second_order_spatial_polynomial`, `seed_mellin_pochhammer_polynomial_identity`, and `defective_seed_mellin_endpoint_nonvanishing`.

### 2.3 Analytic Strip, Endpoint Values, and Open-Strip Nonvanishing

1. **Holomorphy Strip**: Because $\Gamma(s/2)$ has simple poles at $s = 0, -2, -4, \dots$ and the double factor $s^2$ cancels the simple pole at $s = 0$, $F_\tau(s)$ extends holomorphically to $\operatorname{Re}(s) > -2$ (equivalently $\widehat{\psi_\tau}(z)$ is holomorphic on $\operatorname{Re}(z) > -5/2$).
2. **Removable Endpoint Values at $s = 0$ and $s = 1$**:
   - Since $\lim_{s\to 0} s\Gamma(s/2) = 2$, $F_\tau(s) = \frac{s(s-1)^2}{32}(\tau/2)^{-s/2}(s\Gamma(s/2)) = \frac{1}{16}s + O(s^2)$ as $s \to 0$, so $F_\tau(0) = 0$ and $F_\tau'(0) = \frac{1}{16}$.
   - At $s = 1$, $\Gamma(1/2) = \sqrt{\pi}$ is finite and $(s-1)^2$ vanishes to second order, so $F_\tau(1) = F_\tau'(1) = 0$.
3. **Nonvanishing on the Open Critical Strip $0 < \operatorname{Re}(s) < 1$**:
   On $0 < \operatorname{Re}(s) < 1$, $s \ne 0$, $s \ne 1$, $(\tau/2)^{-s/2} = e^{-(s/2)\log\pi} \ne 0$, and $\Gamma(s/2)$ has no zeros anywhere in $\mathbb{C}$. Therefore,
   $$
   F_\tau(s) \ne 0 \quad \forall s \in \mathbb{C} \text{ with } 0 < \operatorname{Re}(s) < 1.
   $$

---

## 3. Exact Closed-Form Autocorrelation $h_K(x)$, Exact Rational Bernstein Envelopes, and Spectral Expansion Without RH

### 3.1 Closed-Form Multiplicative Convolution Theorem and Exact Rational Bernstein Kernel Envelopes

On the multiplicative group $(\mathbb{R}_+, dx/x)$, define grade dilation $(T_K f)(x) := f(\tau^K x)$, involution $f^*(x) := \overline{f(1/x)} = f(1/x)$, and multiplicative convolution
$$
h_K(x) := ((T_K \psi_\tau) * \psi_\tau^*)(x) = \int_0^\infty \psi_\tau(\tau^K x y)\psi_\tau(y)\,\frac{dy}{y} = h_0(\tau^K x).
$$

**Notation Separation (`TASK-TC-042R2`)**: To prevent symbol collision, we denote the symmetric kernel variable of $h_0(\alpha)$ by
$$
W_\alpha := (\alpha + \alpha^{-1})^2 = (2\cosh v)^2 \ge 4 \qquad (\alpha = e^v > 0),
$$
and reserve $W(X) := \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\, h_0(n/X)$ exclusively for the reflected prime wavelet sum.

**Theorem 3.1 (Closed-Form Rational-Algebraic Autocorrelation & Eighth-Order Euler Representation).**
For every $\alpha = \tau^K x > 0$, $h_K(x) = h_0(\alpha)$ is given in exact closed form (with no Gaussian exponentials or numerical quadrature) by:
$$
\boxed{h_0(\alpha) = \frac{-648 W_\alpha^3 + 58380 W_\alpha^2 - 706860 W_\alpha + 2027025}{512\,\left(\alpha + \alpha^{-1}\right)^{17/2}} = \frac{1}{512}\left(\left(\alpha\frac{d}{d\alpha}\right)^2 - \frac{1}{4}\right)^4 \left(\alpha + \alpha^{-1}\right)^{-1/2}.}
$$
Moreover:
1. **Inversion Symmetry**: $h_0(1/\alpha) = h_0(\alpha)$ for all $\alpha > 0$, so $h_K(1/x) = h_0(\tau^K / x) = h_0(\tau^{-K} x) = h_{-K}(x)$.
2. **Exact Peak Value at $\alpha = 1$ ($W_\alpha = 4$)**:
   $$
   h_0(1) = \|\psi_\tau\|_{L^2(\mathbb{R}_+, dx/x)}^2 = \frac{92193}{512 \times 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.49736073812650097.
   $$
3. **Exact Rational Bernstein Proof of the Weighted Decay Envelopes (`certify_weighted_kernel_envelopes_bernstein`)**:
   Set $v = \log\alpha \in \mathbb{R}$ and $S = 2\cosh v = \alpha + \alpha^{-1} \ge 2$, and let $g(v) := h_0(e^v)$ so $g^{(m)}(v) = (D_\alpha^m h_0)(\alpha)$. Because $\frac{d^2}{dv^2}(S^q) = q^2 S^q - 4q(q-1) S^{q-2}$, for every even order $m = 2k \in \{0, 2, 4, 6, 8\}$ the rescaled function $P_m(y) := S^{5/2} g^{(m)}(v)$ is an **exact rational polynomial** of degree $k + 3$ in the bounded variable $y := 4/S^2 = 4/W_\alpha \in (0, 1]$ (with $y = 1 \iff v = 0 \iff \alpha = 1$). Expanding $P_m(y)$ in the Bernstein basis on $N = 8$ uniform rational subintervals $[j/8, (j+1)/8] \subset [0, 1]$ certifies by exact rational arithmetic (`fractions.Fraction`) that every interior Bernstein control point is strictly smaller in magnitude than the $y = 1$ endpoint value $|P_m(1)| = 2^{5/2}|g^{(m)}(0)|$ (with maximum interior-to-endpoint control-point ratios $0.766210, 0.875948, 0.914476, 0.928653, 0.934231 < 1$ for $m = 0, 2, 4, 6, 8$). This proves unconditionally (without invoking Bochner's theorem for weighted decay) that for all $v \in \mathbb{R}$ ($\alpha > 0$) and all $m \in \{0, 2, 4, 6, 8\}$:
   $$
   \boxed{\left|(D_\alpha^m h_0)(\alpha)\right| = \left|g^{(m)}(v)\right| \le \left|g^{(m)}(0)\right| 2^{5/2} \left(\alpha + \alpha^{-1}\right)^{-5/2} \le \left|g^{(m)}(0)\right|.}
   $$
   In particular, at $m = 0$, $|h_0(\alpha)| \le \frac{92193}{32768}(\alpha + \alpha^{-1})^{-5/2}$ for all $\alpha > 0$, and $-\frac{81}{64}\alpha^{-5/2} \le h_0(\alpha) < 0$ for all $\alpha \ge 9$.
4. **First Euler Derivative $(D_\alpha h_0)(\alpha)$ and Stieltjes Kernel $\tilde{h}_0(\alpha)$ Envelope**:
   Differentiating $h_0(\alpha) = N_0(W_\alpha) S^{-17/2}$ via $D_\alpha W_\alpha = 2(\alpha - \alpha^{-1})S$ yields
   $$
   (D_\alpha h_0)(\alpha) = \frac{(\alpha - \alpha^{-1})\left(3240 W_\alpha^3 - 525420 W_\alpha^2 + 9189180 W_\alpha - 34459425\right)}{1024\,\left(\alpha + \alpha^{-1}\right)^{19/2}},
   $$
   and $\tilde{h}_0(\alpha) := \frac{1}{2}h_0(\alpha) - (D_\alpha h_0)(\alpha)$. Expanding $|(D_\alpha h_0)(\alpha) S^{5/2}|^2 = (1 - y) Q_1(y)^2$ in the Bernstein basis on 32 rational subintervals of $[0, 1]$ certifies $|(D_\alpha h_0)(\alpha)| \le \frac{2871}{200}(\alpha + \alpha^{-1})^{-5/2} = 14.355(\alpha + \alpha^{-1})^{-5/2}$ and hence
   $$
   \left|\tilde{h}_0(\alpha)\right| \le \frac{1032993}{65536}\left(\alpha + \alpha^{-1}\right)^{-5/2} \approx 15.761757\left(\alpha + \alpha^{-1}\right)^{-5/2} \quad \forall \alpha > 0.
   $$

### 3.2 Complete Explicit-Formula Functional $C_\tau(K) = W_\xi(h_K)$ and Spectral Expansion Without RH

The centered Mellin transform of $h_K$ is
$$
H_K(z) = \int_0^\infty h_K(x) x^{z-1}\,dx = \tau^{-Kz} F_\tau\!\left(\frac{1}{2} + z\right)\overline{F_\tau\!\left(\frac{1}{2} - \bar{z}\right)} = \tau^{-Kz} F_\tau\!\left(\frac{1}{2} + z\right) F_\tau\!\left(\frac{1}{2} - z\right),
$$
which is holomorphic on $|\operatorname{Re}(z)| < 5/2$ and satisfies $H_K(1/2) = H_K(-1/2) = 0$ because $F_\tau(0) = F_\tau(1) = 0$. Consequently, the pole terms $H_K(1/2) + H_K(-1/2)$ in $W_\xi(h_K)$ vanish identically, and the completed correlation is given unconditionally by:
$$
\begin{aligned}
C_\tau(K) := W_\xi(h_K) &= -\sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\bigl[h_0(\tau^K n) + h_0(\tau^{-K} n)\bigr] - \bigl(\log(2\tau) + \gamma_E\bigr)h_0(\tau^K) \\
&\quad - \int_1^\infty \bigl[h_0(\tau^K x) + h_0(\tau^{-K} x) - 2 x^{-1/2} h_0(\tau^K)\bigr]\frac{x^{1/2}}{x - x^{-1}}\,\frac{dx}{x} \\
&= \sum_\rho m_\rho a_\rho \tau^{-K(\rho - 1/2)}, \qquad a_\rho := F_\tau(\rho)\overline{F_\tau(1 - \bar{\rho})},
\end{aligned}
$$
where the sum runs over all distinct nontrivial zeros $\rho$ of $\zeta(s)$ in $0 < \operatorname{Re}(\rho) < 1$ with multiplicity $m_\rho \ge 1$.
- **Without assuming RH**: Since both $\rho$ and $1 - \bar{\rho}$ lie in the open strip $0 < \operatorname{Re}(s) < 1$ where $F_\tau(s) \ne 0$, every nontrivial zero has **strictly nonvanishing spectral weight** $a_\rho \ne 0$.
- **Reality and Evenness ($C_\tau(-K) = C_\tau(K) \in \mathbb{R}$)**:
  - *Arithmetic proof*: Since $h_0(1/\alpha) = h_0(\alpha)$, $h_0(\tau^K) = h_0(\tau^{-K})$ and $h_0(\tau^K x) + h_0(\tau^{-K} x)$ is invariant under $K \mapsto -K$ for every $x > 0$.
  - *Spectral proof*: Under the zero quartet $\{\rho, \bar{\rho}, 1-\bar{\rho}, 1-\rho\}$ with $\rho = 1/2 + \delta + i\gamma$, the weights satisfy $a_{\bar{\rho}} = \overline{a_\rho}$, $a_{1-\bar{\rho}} = \overline{a_\rho}$, and $a_{1-\rho} = a_\rho$, so the quartet sum is
    $$
    C_{\mathrm{quartet}}(K) = 4\operatorname{Re}(a_\rho)\cosh(KL\delta)\cos(K\gamma L) - 4\operatorname{Im}(a_\rho)\sinh(KL\delta)\sin(K\gamma L),
    $$
    which is manifestly real and even in $K$ (formalized in Lean 4 theorem `quartet_grade_symmetry_and_evenness`).

---

## 4. Equivalent Formulations and Complete Fixed-Seed RH-Equivalence Proof

### 4.1 Equivalent Formulations (`Section 4`)

For the fixed state $\psi_\tau$, the following three statements are equivalent (formalized in `two_by_two_gram_determinant_equivalence`):
- **(A) Canonical Correlation Bound**: $C_\tau(0) \ge 0$ and $|C_\tau(K)| \le C_\tau(0)$ for all $K \in \overline{\mathbb{Q}} \cap \mathbb{R}$.
- **(B) $2 \times 2$ Toeplitz Gram Determinant Nonnegativity**: $C_\tau(0) \ge 0$ and $\Delta_\tau(K) := \det\begin{pmatrix} C_\tau(0) & C_\tau(K) \\ C_\tau(-K) & C_\tau(0) \end{pmatrix} = C_\tau(0)^2 - |C_\tau(K)|^2 \ge 0$ for all $K \in \overline{\mathbb{Q}} \cap \mathbb{R}$.
- **(C) Cyclic Trajectory Cauchy–Schwarz**: $\langle \psi_\tau, \psi_\tau \rangle_\xi \ge 0$ and $|\langle T_K\psi_\tau, \psi_\tau \rangle_\xi|^2 \le \langle T_K\psi_\tau, T_K\psi_\tau \rangle_\xi \langle \psi_\tau, \psi_\tau \rangle_\xi$ along the grade orbit $\{T_K\psi_\tau\}_{K \in \overline{\mathbb{Q}}\cap\mathbb{R}}$.

### 4.2 Complete Proof of Fixed-Seed Equivalence to RH (`Section 5`)

**Theorem 4.1 (Fixed-Seed Correlation Bound $\Longleftrightarrow$ RH).**
Statements (A)–(C) hold if and only if every nontrivial zero $\rho$ of $\zeta(s)$ satisfies $\operatorname{Re}(\rho) = 1/2$.

*Proof.*
1. **Converse ($\text{RH} \implies \text{(A)}$)**:
   If every nontrivial zero satisfies $\rho = 1/2 + i\gamma_\rho$ ($\gamma_\rho \in \mathbb{R}$), then $1 - \bar{\rho} = \rho$, so $a_\rho = |F_\tau(1/2 + i\gamma_\rho)|^2 > 0$. Hence $C_\tau(0) = \sum_\rho m_\rho |F_\tau(\rho)|^2 > 0$, and for every $K \in \mathbb{R}$,
   $$
   |C_\tau(K)| = \left|\sum_\rho m_\rho |F_\tau(\rho)|^2 \tau^{-i K \gamma_\rho}\right| \le \sum_\rho m_\rho |F_\tau(\rho)|^2 = C_\tau(0).
   $$
2. **Forward Direction ($\text{(A)} \implies \text{RH}$)**:
   - *Step 1 (Extension from $\overline{\mathbb{Q}}\cap\mathbb{R}$ to $\mathbb{R}$ by continuity and density)*:
     By Stirling's bound $|a_\rho| \ll |\gamma_\rho|^{15/2} e^{-\pi|\gamma_\rho|/2}$ and $|\tau^{-K(\rho-1/2)}| \le \tau^{|K|/2}$, the series $C_\tau(K) = \sum_\rho m_\rho a_\rho \tau^{-K(\rho-1/2)}$ converges normally on every compact interval $[-K_0, K_0] \subset \mathbb{R}$ and defines a continuous (in fact entire) function of $K$. Since $\overline{\mathbb{Q}} \cap \mathbb{R} \supset \mathbb{Q}$ is dense in $\mathbb{R}$, $|C_\tau(K)| \le C_\tau(0)$ on $\overline{\mathbb{Q}} \cap \mathbb{R}$ implies $|C_\tau(t)| \le C_\tau(0)$ for all $t \in \mathbb{R}$.
   - *Step 2 (Laplace resolvent and normal convergence of partial fractions)*:
     For $\operatorname{Re}(w) > L/2$, since $|\tau^{t(\rho - 1/2)}| = e^{t L \delta_\rho} < e^{t L / 2}$ and $\sum_\rho m_\rho |a_\rho| < \infty$, Fubini's theorem justifies term-by-term Laplace integration:
     $$
     \mathcal{L}[C_\tau(-t)](w) := \int_0^\infty e^{-wt} C_\tau(-t)\,dt = \sum_\rho m_\rho a_\rho \int_0^\infty e^{-(w - L(\rho - 1/2))t}\,dt = \sum_\rho \frac{m_\rho a_\rho}{w - L(\rho - 1/2)} =: \mathcal{R}_\tau(w).
     $$
     Because $\sum_\rho m_\rho |a_\rho| < \infty$, the partial-fraction series $\mathcal{R}_\tau(w)$ converges normally on every compact subset of $\mathbb{C} \setminus \{L(\rho - 1/2)\}$, providing the unique meromorphic continuation of $\mathcal{L}[C_\tau(-t)](w)$ to $\mathbb{C}$.
   - *Step 3 (Right-half-plane holomorphy under $|C_\tau(t)| \le C_\tau(0)$)*:
     Since $|C_\tau(-t)| \le C_\tau(0)$ for all $t \ge 0$, the integral $\int_0^\infty e^{-wt} C_\tau(-t)\,dt$ converges absolutely and defines a **holomorphic** function on the entire open right half-plane $\operatorname{Re}(w) > 0$, bounded by $|\mathcal{L}[C_\tau(-t)](w)| \le C_\tau(0)/\operatorname{Re}(w)$.
   - *Step 4 (Non-cancelling residue at any off-critical zero with $\delta_0 > 0$)*:
     Suppose $\zeta(s)$ has a nontrivial zero $\rho_0 = 1/2 + \delta_0 + i\gamma_0$ with $0 < \delta_0 < 1/2$. Then $w_0 := L(\rho_0 - 1/2) = L\delta_0 + i L\gamma_0$ lies in the open right half-plane $\operatorname{Re}(w_0) = L\delta_0 > 0$. Because the affine map $\rho \mapsto L(\rho - 1/2)$ is injective on $\mathbb{C}$ and the zeros of $\zeta(s)$ are isolated, no distinct zero $\rho \ne \rho_0$ maps to $w_0$. By normal convergence of $\sum_{\rho \ne \rho_0} \frac{m_\rho a_\rho}{w - L(\rho - 1/2)}$ on a small disk around $w_0$, $\mathcal{R}_\tau(w)$ has a simple pole at $w_0$ with residue
     $$
     \operatorname*{Res}_{w = w_0} \mathcal{R}_\tau(w) = m_{\rho_0} a_{\rho_0} = m_{\rho_0} F_\tau(\rho_0)\overline{F_\tau(1 - \bar{\rho}_0)} \ne 0,
     $$
     contradicting the holomorphy of $\mathcal{L}[C_\tau(-t)](w)$ on $\operatorname{Re}(w) > 0$.
   - *Step 5 (Functional-equation reflection for $\delta_0 < 0$)*:
     If $\rho_0 = 1/2 + \delta_0 + i\gamma_0$ had $-1/2 < \delta_0 < 0$, the functional equation $\xi(1-s) = \xi(s)$ yields the reflected zero $\rho_0' = 1 - \bar{\rho}_0 = 1/2 - \delta_0 + i\gamma_0$ with $\operatorname{Re}(\rho_0' - 1/2) = -\delta_0 > 0$, which is ruled out by Step 4. Thus $\delta_0 = 0$ for every nontrivial zero. $\blacksquare$

---

## 5. Certified Numerical Evaluation: Arithmetic vs. Unconditional Spectral Routes (`Sections 6 & 7`, Repaired in `TASK-TC-042R`)

### 5.1 Decoupled, Unconditional Evaluators and `TASK-TC-042R` Certification Repairs

1. **Unconditional Spectral Route (`evaluate_c_tau_spectral_certified`)**:
   - Sums the first 29 nontrivial zero conjugate pairs in $(0, 100]$ using the 100-digit certified enclosures in `data/certificates/zeros/zero_00001.json` .. `zero_00029.json` (which cover $(0, 100]$ with **zero intermediate spectral gaps**, backed by Turing block certificates `block_00001` .. `block_00005`).
   - Bounds all zeros with $|\gamma_\rho| > T = 100$ **unconditionally** using $|\delta_\rho| \le 1/2$ (never setting $\delta_{\max} = 0$), Stirling's complex Gamma remainder bound, and the Backlund–Rosser Riemann–von Mangoldt zero-counting bound:
     $$
     \left|R_{\mathrm{spec}}(K; 100)\right| \le 3.79 \times 10^{-55}\,\tau^{|K|/2} \le 5.91 \times 10^{-52} \quad \forall |K| \le 8.
     $$
   - In `TASK-TC-042R`, `compute_unconditional_spectral_derivative_tail_bound_arb(T_cutoff=100.0, deriv_order=m, K_max=K_max)` computes rigorous off-critical ($|\delta_\rho| \le 1/2$) Backlund–Rosser Stieltjes tail enclosures for higher $K$-derivatives (e.g., $3.79 \times 10^{-55}$ for $m=0$, $1.28 \times 10^{-50}$ for $m=2$, and $4.92 \times 10^{-46}$ for $m=4$ on $|K| \le 0.14$), replacing the earlier hard-coded `1e-45`.
2. **Certified Arithmetic Route (`evaluate_c_tau_arithmetic_certified`) and Taylor/Branch-Cut Repairs**:
   - Evaluates the exact closed-form rational-algebraic kernel $h_0(\tau^{\pm K} n)$ across all 2762 prime powers $2 \le p^k \le N_{\max} = 25000$, plus the unconditional Rosser–Schoenfeld Chebyshev summation-by-parts tail bound.
   - **Reproduction & Repair of the $[0, 0.25]$ Taylor Remainder Defect (`audit_archimedean_taylor_remainder_repair`)**:
     - At `series_order = 36` ($N = 35$ integrated terms, $0 \le k \le 34$) and $K = 0$, the exact omitted Taylor integral on $[0, 0.25]$ is
       $$
       \int_0^{0.25} \sum_{k=35}^\infty c_k u^k\,du = +2.1892962597 \times 10^{-23} \in [2.064 \times 10^{-23}, \; 2.212 \times 10^{-23}]
       $$
       (with $k = 35$ contributing $+1.983506 \times 10^{-23}$ and $k = 36$ contributing $+2.816228 \times 10^{-24}$), which is **$21.89\times$ larger** than the old hard-coded allowance `1e-24`.
     - Replaced the hard-coded `cauchy_tail = arb("1e-24")` with `compute_archimedean_taylor_cauchy_bound_arb`, which covers the circle $|u| = R_c = 1.0 < \pi/2$ by $512$ overlapping complex interval arcs (`analytic=True`) to bound $M(R_c) = \sup_{|u|=R_c}|g_K(u)|$ and upgrades `series_order = 49` ($N = 48$ integrated terms), yielding the certified Cauchy remainder bound $4.5165 \times 10^{-28}$ at $K = 0$ (strictly enclosing the true omitted integral $3.0792 \times 10^{-33}$).
   - **Branch-Cut Analyticity Flag Repair**:
     - Updated `evaluate_h0_acb`, `evaluate_h0_euler_d2_acb`, `evaluate_h0_euler_d4_acb`, `_f_d0_1`, and `_f_1_inf` to forward `analytic=analytic` into `s.sqrt(analytic=analytic)` so that `flint.acb.integral` rigorously checks branch cuts of $(\alpha + \alpha^{-1})^{-17/2}$ along $(-\infty, 0]$ across every complex quadrature ellipse.

### 5.2 Certified Grade Grid Results

| Grade $K$ | Unconditional Spectral $C_\tau^{\mathrm{spec}}(K)$ | Certified Arithmetic $C_\tau^{\mathrm{arith}}(K)$ | Enclosures Overlap | $|C_\tau(K)| / C_\tau(0)$ | $\Delta_\tau(K) = C_\tau(0)^2 - C_\tau(K)^2$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $0$ | $+9.504798117910 \times 10^{-4} \pm 3.79 \times 10^{-55}$ | $+9.50480944 \times 10^{-4} \pm 3.16 \times 10^{-9}$ | `True` | $1.00000000$ | $0$ |
| $1/8$ | $-9.447622082581 \times 10^{-4} \pm 4.25 \times 10^{-55}$ | $-9.44760884 \times 10^{-4} \pm 3.69 \times 10^{-9}$ | `True` | $0.99398451$ | $+1.083624 \times 10^{-8} > 0$ |
| $1/4$ | $+9.286153791481 \times 10^{-4} \pm 4.77 \times 10^{-55}$ | $+9.28617344 \times 10^{-4} \pm 5.48 \times 10^{-9}$ | `True` | $0.97699643$ | $+4.108535 \times 10^{-8} > 0$ |
| $1/2$ | $+8.668613749571 \times 10^{-4} \pm 6.00 \times 10^{-55}$ | $+8.66867062 \times 10^{-4} \pm 1.59 \times 10^{-8}$ | `True` | $0.91202503$ | $+1.519632 \times 10^{-7} > 0$ |
| $1$ | $+6.307301083454 \times 10^{-4} \pm 9.50 \times 10^{-55}$ | $+6.30786123 \times 10^{-4} \pm 1.56 \times 10^{-7}$ | `True` | $0.66359127$ | $+5.055914 \times 10^{-7} > 0$ |
| $\sqrt{2}$ | $+5.441316702609 \times 10^{-4} \pm 1.39 \times 10^{-54}$ | $+5.44507343 \times 10^{-4} \pm 1.05 \times 10^{-6}$ | `True` | $0.57248104$ | $+6.073326 \times 10^{-7} > 0$ |
| $2$ | $-1.133761279092 \times 10^{-4} \pm 2.38 \times 10^{-54}$ | $-1.07832481 \times 10^{-4} \pm 1.55 \times 10^{-5}$ | `True` | $0.11928305$ | $+8.905577 \times 10^{-7} > 0$ |
| $4$ | $-9.234066385075 \times 10^{-4} \pm 1.50 \times 10^{-53}$ | $+7.00765546 \times 10^{-2} \pm 1.51 \times 10^{-1}$ | `True` | $0.97151631$ | $+5.073205 \times 10^{-8} > 0$ |
| $8$ | $+8.437501317607 \times 10^{-4} \pm 5.90 \times 10^{-52}$ | $+7.12794413 \times 10^{-4} \pm 9.12 \times 10^{3}$ | `True` | $0.88770968$ | $+1.914976 \times 10^{-7} > 0$ |
| $-1/4$ | $+9.286153791481 \times 10^{-4} \pm 4.77 \times 10^{-55}$ | $+9.28617344 \times 10^{-4} \pm 5.48 \times 10^{-9}$ | `True` | $0.97699643$ | $+4.108535 \times 10^{-8} > 0$ |
| $-1/2$ | $+8.668613749571 \times 10^{-4} \pm 6.00 \times 10^{-55}$ | $+8.66867062 \times 10^{-4} \pm 1.59 \times 10^{-8}$ | `True` | $0.91202503$ | $+1.519632 \times 10^{-7} > 0$ |
| $-1$ | $+6.307301083454 \times 10^{-4} \pm 9.50 \times 10^{-55}$ | $+6.30786123 \times 10^{-4} \pm 1.56 \times 10^{-7}$ | `True` | $0.66359127$ | $+5.055914 \times 10^{-7} > 0$ |
| $-\sqrt{2}$ | $+5.441316702609 \times 10^{-4} \pm 1.39 \times 10^{-54}$ | $+5.44507343 \times 10^{-4} \pm 1.05 \times 10^{-6}$ | `True` | $0.57248104$ | $+6.073326 \times 10^{-7} > 0$ |
| $-2$ | $-1.133761279092 \times 10^{-4} \pm 2.38 \times 10^{-54}$ | $-1.07832481 \times 10^{-4} \pm 1.55 \times 10^{-5}$ | `True` | $0.11928305$ | $+8.905577 \times 10^{-7} > 0$ |

### 5.3 Repaired Two-Sided Local Theorem at $K = 0$, Scoped $M_6^{\mathrm{arith}}$ Bound, Outward-Rounded Gram Minors, and Quartet Controls

1. **Certified Origin Derivatives & Repaired Two-Sided Local Taylor Enclosures (`TASK-TC-042R` / `TASK-TC-042R2`)**:
   - $C_\tau(0)$, $C_\tau''(0)$, and $C_\tau^{(4)}(0)$ are independently computed and certified via **both** a 100% zero-free arithmetic route (`evaluate_zero_free_arithmetic_euler_derivative_at_zero`) and the unconditional spectral-tail route:
     - $C_\tau^{\mathrm{arith}}(0) = [9.50480944 \times 10^{-4} \pm 3.16 \times 10^{-9}]$, $C_\tau^{\mathrm{spec}}(0) = [9.504798117910 \times 10^{-4} \pm 3.79 \times 10^{-55}]$,
     - $(C_\tau'')^{\mathrm{arith}}(0) = [-0.64173930 \pm 1.52 \times 10^{-7}] < 0$, $(C_\tau'')^{\mathrm{spec}}(0) = [-0.641739264785 \pm 1.28 \times 10^{-50}] < 0$,
     - $(C_\tau^{(4)})^{\mathrm{arith}}(0) = [433.54130868 \pm 5.83 \times 10^{-6}] > 0$, $(C_\tau^{(4)})^{\mathrm{spec}}(0) = [433.541307975303 \pm 4.92 \times 10^{-46}] > 0$ (all three derivative enclosures intersect at $K = 0$).
   - Decomposing $C_\tau''(0)$ into arithmetic components shows that **both** the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.25759528 < 0$, arising from $-167.40379948$ archimedean integral curvature plus $+167.14620420$ local constant curvature) **and** the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.38414402 < 0$) are strictly concave at $K = 0$.
   - **Why Two-Sided Bounds Are Required**: Showing $C_\tau(K) < C_\tau(0)$ alone does not establish $|C_\tau(K)| < C_\tau(0)$ unless $C_\tau(K) > -C_\tau(0)$ is also certified (`taylor_two_sided_abs_correlation_bound` and `taylor_sixth_order_two_sided_abs_correlation_bound` in Lean 4). We distinguish the **Taylor lower-bound polynomial roots** from the actual correlation crossings.
   - **Route 1 — 100% Zero-Free 6th-Order Arithmetic Taylor Enclosure (Scoped to $|K| \le 0.08$)**:
     - Using the exact rational Bernstein polynomial certificates $|g^{(6)}(v)| \le |g^{(6)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ and $|g^{(8)}(v)| \le |g^{(8)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ (`Section 3.1`), together with the elementary prime-power sum bound
       $$
       \sum_{n \ge 2} \frac{\Lambda(n)}{n^3} \le \frac{\log 2}{8} + \frac{\log 3}{27} + \frac{\log 3}{18} + \frac{1}{36} \approx 0.21614536 < 0.225
       $$
       (and direct certified sum up to $25000$ plus Rosser–Schoenfeld tail $\le 0.164823 < 0.225$), the 6th-derivative bound on the compact interval $|K| \le 0.08$ ($\kappa_{\max} = 0.08 \log\tau$, splitting $(0, 1]$ at $u_0 = \sqrt{4 g_6(0)/g_8(0)} \approx 0.1656$) is certified as:
       $$
       \boxed{\sup_{|K| \le 0.08} \left|C_\tau^{(6)}(K)\right| \le M_6^{\mathrm{arith}} := 27971954.786589753.}
       $$
       *(Note: Because the tail majorant on $[1, \infty)$ and the prime-power sum contain the shift factor $\cosh(5\kappa/2) \le \cosh(0.20\log\tau)$, $M_6^{\mathrm{arith}}$ is explicitly scoped to the compact domain $|K| \le 0.08$, NOT all $K \in \mathbb{R}$.)*
     - Evaluating the 6th-order Taylor lower-bound polynomials in outward-rounded Arb ball arithmetic certifies the **exact rational interval** $0 < |K| \le \frac{1}{20} = 0.05$ for the two-sided inequality $-C_\tau(0) < C_\tau(K) < C_\tau(0)$ (and $0 \le |K| \le \frac{9}{200} = 0.045$ for strict positivity $C_\tau(K) > 0$) with strict positive margins:
       $$
       \forall K \in \left[-\frac{1}{20}, \frac{1}{20}\right] \setminus \{0\} : \quad -C_\tau(0) < C_\tau(K) < C_\tau(0) \quad (\text{upper margin } \ge +8.224 \times 10^{-5} > 0, \; \text{lower abs margin } \ge +6.047 \times 10^{-4} > 0),
       $$
       $$
       \forall K \in \left[-\frac{9}{200}, \frac{9}{200}\right] : \quad C_\tau(K) \ge +5.944 \times 10^{-5} > 0
       $$
       (while the approximate roots of the 6th-order Taylor lower-bound polynomials occur at $|K| \approx 0.04577570$ for $C_\tau(K) > 0$, $|K| \approx 0.05148579$ for $C_\tau(K) < C_\tau(0)$, and $|K| \approx 0.05514312$ for $C_\tau(K) > -C_\tau(0)$).
   - **Route 2 — Unconditional Spectral-Tail 4th-Order Taylor Enclosure (Scoped to $|K| \le 0.14$)**:
     - Using the 29 Turing-certified critical-line zeros in $(0, 100]$ plus the unconditional off-critical ($|\delta_\rho| \le 1/2$) Backlund–Rosser tail bound $4.92 \times 10^{-46}$ for $|\gamma_\rho| > 100$ on $|K| \le 0.14$, we obtain $\sup_{|K|\le 0.14}|C_\tau^{(4)}(K)| \le M_4^{\mathrm{spec}} = 433.54130958$. Evaluating the 4th-order Taylor lower-bound polynomials in Arb ball arithmetic certifies the **exact rational interval** $0 < |K| \le \frac{17}{250} = 0.068$ for $-C_\tau(0) < C_\tau(K) < C_\tau(0)$ (and $0 \le |K| \le \frac{1}{20} = 0.05$ for $C_\tau(K) > 0$) with strict positive margins:
       $$
       \forall K \in \left[-\frac{17}{250}, \frac{17}{250}\right] \setminus \{0\} : \quad -C_\tau(0) < C_\tau(K) < C_\tau(0) \quad (\text{upper margin } \ge +1.097 \times 10^{-3} > 0, \; \text{lower abs margin } \ge +3.102 \times 10^{-5} > 0),
       $$
       with approximate Taylor lower-bound polynomial roots at $|K| \approx 0.05085052$ for $C_\tau(K) > 0$, $|K| \approx 0.06846476$ for $|C_\tau(K)| < C_\tau(0)$, and $|K| \approx 0.13327694$ for $C_\tau(K) < C_\tau(0)$.
2. **Baseline Narrative vs. Artifact Discrepancy Reconciliation (`reconcile_baseline_narrative_discrepancies`)**:
   - **`1943.7705` vs. `433.5413086756161`**: Stale narrative in `docs/TC_CURRENT_CANONICAL_STATUS.md` reported $(C_\tau^{(4)})^{\mathrm{arith}}(0) = +1943.7705$ from an earlier un-normalized draft, whereas the certified fourth derivative at $K = 0$ in the artifact is $C_\tau^{(4)}(0) = [433.54130868 \pm 5.83 \times 10^{-6}]$ (`C_tau_fourth_deriv_0_mid = 433.5413086756161`), and the scoped sixth-derivative bound on $|K| \le 0.08$ is $\sup_{|K|\le 0.08}|C_\tau^{(6)}(K)| \le M_6^{\mathrm{arith}} = 27971954.786589753$.
   - **`0.0566039457` (and `0.0885735048`) vs. Derived Uniform Archimedean Bound `5.994279`**: Stale narrative in `docs/TC_CURRENT_CANONICAL_STATUS.md` used $0.0566039457 + 0.0319695591 = 0.0885735048$ (point values at $K = 1$) while the code used an ad-hoc `4.95`; now the uniform archimedean bound is derived and certified in `derive_and_certify_uniform_archimedean_bound` by splitting $(0, 1]$ at $u_0 = \sqrt{4 g_0(0)/|g_2(0)|} \approx 0.353502$, proving $|I_{\mathrm{arch}}(K)| \le 0.698425 + 1.970473 + 0.383932 + 1.395526 = 4.448357 < 4.95$ and $|W_{\mathrm{arch}}(h_K)| \le 1.545922 + 4.448357 = 5.994279$ for all $K \in \mathbb{R}$ (eliminating the hard-coded `4.95`).
   - **`0.0319695591` vs. `0.6330390930175781`**: `-0.0319695591` is the midpoint value of the reflected prime wavelet sum $W(\tau) = -P_{\mathrm{refl}}(1)$ at $K = 1$ ($X = \tau$), whereas the global upper bound on $|P_{\mathrm{fwd}}(X)|$ for all $X \ge 1$ is $\frac{92193}{32768} \times 0.225 = 0.6330390930175781$.
3. **Finite Toeplitz Gram Matrices Certified by Outward-Rounded `flint.arb_mat.det()` Minors**:
   - Positive-definiteness of the finite Toeplitz Gram matrices $[C_\tau(K_i - K_j)]$ is certified via Sylvester's criterion using outward-rounded leading principal minor determinants `flint.arb_mat.det()` on the full `arb` enclosures (with floating-point eigenvalues reported purely as diagnostics):
     - **`rational_6_point_grid` $\{0, 1/8, 1/4, 1/2, 1, 2\}$ (spectral route)**: all 6 leading principal minor determinants are certified strictly positive ($\det_1 \approx 9.505 \times 10^{-4}$, $\det_2 \approx 1.084 \times 10^{-8}$, $\det_3 \approx 1.948 \times 10^{-14}$, $\det_4 \approx 1.052 \times 10^{-19}$, $\det_5 \approx 2.340 \times 10^{-27}$, $\det_6 \approx 1.528 \times 10^{-35} \pm 4.50 \times 10^{-78} > 0$).
     - **`algebraic_5_point_grid` $\{-\sqrt{2}, -1/2, 0, 1/2, \sqrt{2}\}$ (spectral route)**: all 5 leading principal minor determinants are certified strictly positive ($\det_5 \approx 9.959 \times 10^{-30} \pm 6.09 \times 10^{-73} > 0$).
     - **`zero_free_arithmetic_3_point_grid` $\{0, 1/4, 1/2\}$ (100% zero-free arithmetic route)**: all 3 leading principal minor determinants are certified strictly positive ($\det_1 \ge 9.5047 \times 10^{-4} > 0$, $\det_2 \ge 4.1067 \times 10^{-8} > 0$, $\det_3 = [2.25 \times 10^{-13} \pm 9.17 \times 10^{-14}] \ge 1.5886 \times 10^{-13} > 0$).
4. **Synthetic Off-Critical Quartet Controls**:
   - For synthetic off-critical quartets at $\gamma_0 = 14.13472514$ with $\delta_0 \in \{0.05, 0.15, 0.25\}$, $|a_{\rho_0}| > 0$ in every case and $C_{\mathrm{quartet}}(K)$ grows exponentially as $\cosh(K L \delta_0)$, reaching $|C_{\mathrm{quartet}}(K)|/|C_{\mathrm{quartet}}(0)| \approx 1.422, 7.234, 42.615$ by $K = 40 \cdot \frac{2\pi}{\gamma_0 L} \approx 9.67$, violating $|C(K)| \le C(0)$.

---

## 6. Controls on the Role of $\tau = 2\pi$ (`Section 8`)

Replacing the Gaussian width $\tau/2 = \pi$ by $a > 0$ in $G_{t,a}(x) = t^{1/4} e^{-a t x^2}$ and the grade base $\tau$ by $b > 1$ in $(T_{K,b} f)(x) = f(b^K x)$ yields the exact identity (verified to $< 10^{-45}$ across all 5 tested $(a, b)$ pairs and formalized in `gaussian_width_and_grade_base_scaling_identity`):
$$
\boxed{C_{a,b}(K) = \sqrt{\frac{a_0}{a}}\,C_{a_0,\tau}\!\left(K\frac{\log b}{\log \tau}\right), \qquad a_0 = \frac{\tau}{2} = \pi.}
$$
- **Physical-space mechanism**: $\psi_a(x) = (a_0/a)^{1/4}\psi_\tau(\sqrt{a/a_0}\,x)$, so the scale-invariant Haar convolution $dy/y$ factors out $((a_0/a)^{1/4})^2 = \sqrt{a_0/a}$ while $b^K x = \tau^{K \log b / \log\tau} x$.
- **Mellin-space mechanism**: $F_a(s) = (a_0/a)^{s/2} F_\tau(s)$, so on every reflected zero pair $(\rho, 1-\bar{\rho})$ where $\rho + (1-\rho) = 1$, $F_a(\rho)\overline{F_a(1-\bar{\rho})} = \sqrt{a_0/a}\,a_\rho$ is independent of $\rho$.
- **Consequence**: Changing $b > 1$ reparametrizes the grade axis $K \mapsto K \frac{\log b}{\log\tau}$ and changing $a > 0$ scales the correlation by $\sqrt{\pi/a}$. Thus any arithmetic proof of $|C_\tau(K)| \le C_\tau(0)$ must either establish the inequality for all real shifts $\kappa = K \log\tau \in \mathbb{R}$ or use the self-dual Poisson/theta coupling between $\pi^{-s/2}\Gamma(s/2)$ and the integer lattice $\mathbb{Z}$ at $a = \pi = \tau/2$.

---

## 7. Arithmetic Proof Attempts, Repaired Stieltjes Multiscale Reduction, & Substantive Cancellation Attempts (`SUBGATE-TC-042B`) (`Section 9`)

1. **Attempt 1 — Pointwise Kernel Difference $d_K^-(x) = 2h_0(x) - [h_0(\tau^K x) + h_0(\tau^{-K} x)]$ (`POINTWISE_KERNEL_DIFFERENCE_SIGN_FALSIFIED`)**:
   - Because $h_0(\alpha)$ has three sign changes on $\alpha \ge 1$ ($h_0(1) > 0$, $h_0(2) < 0$, $h_0(3) > 0$, and $h_0(\alpha) < 0$ for $\alpha \ge 5$), at $K = 1$ the kernel difference satisfies $d_1^-(3) = +0.248918 > 0$ at $p = 3$ and $d_1^-(7) = -0.401751 < 0$ at $p = 7 \approx \tau$. Term-by-term sign dominance across prime powers is therefore false.
2. **Attempt 2 — Local Concavity & Collaborative Prime/Archimedean Curvature (`LOCAL_ORIGIN_CONCAVITY_CERTIFIED`)**:
   - At $K = 0$, both the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.257595 < 0$) and the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.384145 < 0$) are strictly concave, certifying the exact rational interval $0 < |K| \le 1/20 = 0.05$ via the 100% zero-free 6th-order arithmetic route and $0 < |K| \le 17/250 = 0.068$ via the unconditional spectral-tail 4th-order route.
3. **Attempt 3 — Large-$|K|$ Wavelet Decomposition & Reduction to Uniform Prime-Wavelet Boundedness (`SUBGATE-TC-042A` & `SUBGATE-TC-042B`)**:
   - Decomposing $C_\tau(K) = W_{\mathrm{arch}}(h_K) + P_{\mathrm{fwd}}(K) + P_{\mathrm{refl}}(K)$ for $K \ge 0$ (and by evenness $C_\tau(-K) = C_\tau(K)$ for all $K \in \mathbb{R}$):
     - Both the archimedean term and forward prime sum admit derived, unconditional global bounds on $K \ge 0$: $|W_{\mathrm{arch}}(h_K)| \le M_{\mathrm{arch}} = 5.994279$ (with $|I_{\mathrm{arch}}(K)| \le 4.448357 < 4.95$, decaying as $O(\tau^{-3K/2})$) and $|P_{\mathrm{fwd}}(K)| \le M_{\mathrm{fwd}} = 0.633039$ (decaying as $O(\tau^{-5K/2})$).
     - By the Laplace-resolvent argument (`Section 4.2`) and Lean theorem `complete_correlation_bounded_of_reflected_prime_wavelet_bound`, **any finite uniform bound** $|C_\tau(K)| \le M_{\mathrm{total}} < \infty$ on $K \ge 0$ already makes $\mathcal{L}[C_\tau(-t)](w)$ holomorphic on $\operatorname{Re}(w) > 0$ and prevents off-critical zeros.
     - Therefore, proving RH via this route reduces to the **Uniform Prime-Wavelet Boundedness Subgate (`SUBGATE-TC-042B`)** (`investigate_uniform_prime_wavelet_boundedness`):
       $$
       \boxed{\exists M < \infty \; \forall X \ge 1 : \quad \left|W(X)\right| := \left|\sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\, h_0\!\left(\frac{n}{X}\right)\right| \le M.}
       $$
4. **Repaired Stieltjes Chebyshev-Error Identities (Form A in $x$ and Form B in $\alpha = x/X$) (`TASK-TC-042R2`)**:
   - Writing $\psi(x) = \sum_{n \le x} \Lambda(n) = x + E(x)$ and noting that
     $$
     H_0(1/2) := \int_0^\infty \alpha^{-1/2} h_0(\alpha)\,d\alpha = F_\tau(1) F_\tau(0) = 0 \qquad \left(\text{distinct from } H_0(0) := \int_0^\infty h_0(\alpha)\,\frac{d\alpha}{\alpha} = F_\tau(1/2)^2 \approx 2.138047 \times 10^{-5} > 0\right),
     $$
     we have $\int_1^\infty x^{-1/2} h_0(x/X)\,dx = X^{1/2} H_0(1/2) - \int_0^1 x^{-1/2} h_0(x/X)\,dx = -\int_0^1 x^{-1/2} h_0(x/X)\,dx$.
   - Since $\frac{d}{dx}\bigl[x^{-1/2} h_0(x/X)\bigr] = -x^{-3/2}\tilde{h}_0(x/X)$ where $\tilde{h}_0(\alpha) := \frac{1}{2}h_0(\alpha) - (D_\alpha h_0)(\alpha)$, Stieltjes integration by parts yields two equivalent exact identities (`verify_finite_cutoff_stieltjes_identities_arb`, formalized in `stieltjes_rescaled_variable_and_erroneous_factor_obstruction`):
     - **Form (A) — Original variable $x$ (no $X^{-1/2}$ factor)**:
       $$
       \boxed{W(X) = h_0\!\left(\frac{1}{X}\right) - \int_0^1 x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + \int_1^\infty E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.}
       $$
     - **Form (B) — Rescaled variable $\alpha = x/X$ ($x = X\alpha$, $x^{-3/2}\,dx = X^{-1/2}\alpha^{-3/2}\,d\alpha$)**:
       $$
       \boxed{W(X) = h_0\!\left(\frac{1}{X}\right) - \int_0^1 x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + X^{-1/2}\int_{1/X}^\infty E(X\alpha)\,\alpha^{-3/2}\,\tilde{h}_0(\alpha)\,d\alpha.}
       $$
   - **Finite-Cutoff Identity & Certified Verification at $B = 50$ for $X \in \{1, 4, 100\}$**:
     For any non-prime-power cutoff $B > 1$,
     $$
     \sum_{2 \le n \le B} \frac{\Lambda(n)}{\sqrt{n}} h_0\!\left(\frac{n}{X}\right) = \int_1^B x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + B^{-1/2} h_0\!\left(\frac{B}{X}\right) E(B) + h_0\!\left(\frac{1}{X}\right) + \int_1^B E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.
     $$
     At $B = 50$ across $X \in \{1, 4, 100\}$, both Form (A) and Form (B) enclose the direct prime-power sum in 256-bit Arb arithmetic with midpoint error $< 3 \times 10^{-31}$, whereas the old formula (which erroneously multiplied the $x$-variable integral by $X^{-1/2}$) fails at $X = 4$ by $2.15176 \times 10^{-2}$ and at $X = 100$ by $4.72372 \times 10^{-2}$.
   - **Uniform Boundary Bound and Equivalence to $I(X)$ (`stieltjes_signed_pairing_uniform_bound_equivalence`)**:
     For all $X \ge 1$, $|B_{\mathrm{boundary}}(X)| := |h_0(1/X) - \int_0^1 x^{-1/2} h_0(x/X)\,dx| \le \frac{92193}{24576} X^{-5/2} \le 3.751197 X^{-5/2}$. Consequently:
     $$
     \sup_{X \ge 1} \left|I(X)\right| < \infty \iff \sup_{X \ge 1} |W(X)| < \infty \iff \sup_{K \in \mathbb{R}} |C_\tau(K)| < \infty, \qquad I(X) := \int_1^\infty E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.
     $$
   - **Certified Point Enclosures at 9 Sample Scales in $[1, 1000]$**:
     At the 9 discrete sample scales $X \in \{1, 2, \pi, \tau, 10, \tau^2, 100, \tau^3, 1000\}$ (finite point certificates, not a continuous interval certificate on $[1, 1000]$), $|W(X)|$ is certified bounded by $\le 0.079372$.
5. **Three Substantive Cancellation Attempts on `SUBGATE-TC-042B` (`execute_subgate_tc042b_cancellation_attempts`)**:
   - **Attempt A — Multiscale Euler-Operator Factorization & Iterated Primitive Transfer**:
     - Symbolic verification (`sp.simplify == 0`) establishes the exact 9th-order Euler factorization:
       $$
       \tilde{h}_0(\alpha) = \frac{1}{2}h_0(\alpha) - D_\alpha h_0(\alpha) = -\frac{1}{512}\left(D_\alpha - \frac{1}{2}\right)^5 \left(D_\alpha + \frac{1}{2}\right)^4 \left(\alpha + \alpha^{-1}\right)^{-1/2},
       $$
       which annihilates $\alpha^{1/2}$ (the smooth PNT main term $x$) to **5th order** and $\alpha^{-1/2}$ to **4th order**.
     - Integrating by parts against $E_1(x) := \int_1^x E(t)\,dt = \psi_1(x) - \frac{1}{2}x^2 + \frac{1}{2}$ yields $I(X) = \frac{1}{2}h_1(1/X) + \int_1^\infty E_1(x) x^{-5/2} h_1(x/X)\,dx$ where $h_1(\alpha) := \frac{3}{2}\tilde{h}_0(\alpha) - D_\alpha \tilde{h}_0(\alpha)$. While at the classical PNT exponent $s = 1$ (weights $\Lambda(n)/n$) the integral $\int_1^\infty E(x) x^{-2}\,dx = -\gamma_E - 1$ converges unconditionally because $E_1(x)/x^3$ is integrable, at the critical-line exponent $s = 1/2$ (weights $\Lambda(n)/\sqrt{n}$) each derivative transfer suppresses the high-frequency tail $x \gg X$ by $(X/x)^k$ but on the resonant scale band $x \in [X/4, 4X]$ the scale derivative $\frac{d}{dx}\tilde{h}_0(x/X) = x^{-1}(D_\alpha \tilde{h}_0)(x/X)$ has factor $x^{-1} \asymp X^{-1}$, which balances the extra factor of $x$ in $E_1(x)$.
   - **Attempt B — Signed Dyadic Scale Decomposition**:
     - Decomposes $I(X) = \sum_{j \in \mathbb{Z}} \omega_j \mu_j(X)$ over dyadic shells $\alpha = x/X \in [2^j, 2^{j+1}]$ with unconditionally summable shell weights $\sum_{j \in \mathbb{Z}} \omega_j \le 16.921 < \infty$, isolating the single unresolved hypothesis for Attempt B: uniform boundedness of the normalized signed shell pairings $|\mu_j(X)| \le M_{\mathrm{dyadic}}$ across $X \ge 1$ and $j \in \mathbb{Z}$.
   - **Attempt C — Exact Seed-Wavelet Multiplicative Convolution Factorization**:
     - By Fubini's theorem on $h_0(n/X) = \int_0^\infty \psi_\tau((n/X)y)\psi_\tau(y)\,\frac{dy}{y}$, the reflected prime wavelet sum factors exactly as the multiplicative convolution of the **single-seed prime wavelet** $V_\tau(u)$ with $\psi_\tau$:
       $$
       \boxed{W(X) = \int_0^\infty V_\tau\!\left(\frac{X}{y}\right)\psi_\tau(y)\,\frac{dy}{y} = \int_0^\infty V_\tau(u)\,\psi_\tau\!\left(\frac{X}{u}\right)\frac{du}{u}, \qquad V_\tau(u) := \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\,\psi_\tau\!\left(\frac{n}{u}\right).}
       $$
     - Crucially, because $F_\tau(1) = 0$ already holds for the single seed $\psi_\tau$ prior to squaring, the smooth PNT main term of $V_\tau(u)$ **already vanishes identically** ($\int_0^\infty x^{-1/2}\psi_\tau(x/u)\,dx = u^{1/2}F_\tau(1) = 0$, certified in Arb to $< 2.2 \times 10^{-25}$), and $\psi_\tau(y)$ has Gaussian decay $e^{-\pi y^2}$ for $y \ge 1$.
     - Applying Cauchy–Schwarz in Haar measure $\frac{dy}{y}$ with weight $(y + y^{-1})^2$ yields
       $$
       |W(X)| \le C_\psi \left(\int_0^\infty \frac{|V_\tau(X/y)|^2}{(y + y^{-1})^2}\,\frac{dy}{y}\right)^{1/2}, \qquad C_\psi := \left(\int_0^\infty |\psi_\tau(y)|^2 (y + y^{-1})^2\,\frac{dy}{y}\right)^{1/2} \le 2.092482,
       $$
       reducing `SUBGATE-TC-042B` from a pointwise bound on $W(X)$ to a **local scale-averaged $L^2$ energy bound** on the Gaussian-windowed prime wavelet $V_\tau(u)$ around $u \asymp X$:
       $$
       \sup_{X \ge 1} \int_0^\infty \frac{|V_\tau(X/y)|^2}{(y + y^{-1})^2}\,\frac{dy}{y} < \infty.
       $$

---

## 8. Lean 4 Formalization Summary (`Section 10`, Expanded in `TASK-TC-042R2`)

Module [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) compiles with `0 sorry` and `0 admit` and formalizes **11 definitions** and **20 theorems** (covering exact polynomial/operator identities, Bernstein endpoint polynomials, and conditional Taylor/Laplace/Stieltjes implication schemas; analytic integration and Arb ball enclosures reside in Python/FLINT):
1. `seed_first_order_spatial_polynomial`
2. `seed_second_order_spatial_polynomial`
3. `seed_mellin_pochhammer_polynomial_identity`
4. `defective_seed_mellin_endpoint_nonvanishing`
5. `autocorrelation_symmetric_numerator_identity`
6. `mellin_convolution_endpoint_vanishing`
7. `quartet_grade_symmetry_and_evenness`
8. `critical_line_spectral_weight_nonneg_and_triangle_bound`
9. `two_by_two_gram_determinant_equivalence`
10. `gaussian_width_and_grade_base_scaling_identity`
11. `laplace_resolvent_residue_obstruction_schema`
12. `fixed_seed_correlation_bound_implies_critical_line_schema`
13. `laplace_holomorphic_rhp_hypothesis_satisfiable`
14. `second_euler_autocorrelation_at_one`
15. `taylor_two_sided_abs_correlation_bound`
16. `complete_correlation_bounded_of_reflected_prime_wavelet_bound`
17. `stieltjes_rescaled_variable_and_erroneous_factor_obstruction` *(new in `TASK-TC-042R2`: proves equivalence of Form A and Form B Stieltjes expressions and proves that multiplying the $x$-variable integral by $X^{-1/2}$ creates a nonzero discrepancy $(1 - X^{-1/2}) I_{\mathrm{Stieltjes}} \ne 0$ whenever $X \ne 1$ and $I_{\mathrm{Stieltjes}} \ne 0$)*
18. `bernstein_weighted_h0_polynomial_endpoints` *(new in `TASK-TC-042R2`: proves the exact rational polynomial identity for $P_0(y) = S^{5/2} h_0(\alpha)$ in $y = 4/S^2 \in [0, 1]$ and its endpoint values $P_0(0) = -81/64$, $P_0(1) = 92193/32768$)*
19. `taylor_sixth_order_two_sided_abs_correlation_bound` *(new in `TASK-TC-042R2`: proves the conditional 6th-order Taylor algebra implying $-C_0 < C_K < C_0$, $C_K > 0$, and $C_0^2 - C_K^2 > 0$)*
20. `stieltjes_signed_pairing_uniform_bound_equivalence` *(new in `TASK-TC-042R2`: proves that given a uniform bound $|B_{\mathrm{boundary}}(X)| \le B_0$, uniform boundedness of $I(X)$ is equivalent to uniform boundedness of $W(X)$ and implies uniform boundedness of $C_\tau(K)$)*
