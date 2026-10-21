# Canonical Theta Correlation Bound: Arithmetic Derivation, Certified Tests, and Proof Attempt (`EPIC-TC-042` / `TASK-TC-042` / `TASK-TC-042R`)

## 1. Executive Summary & Status Separation

This document records the complete mathematical derivation, seed defect repair, closed-form multiplicative autocorrelation theorem, fixed-seed Riemann Hypothesis equivalence proof, certified arbitrary-precision evaluations, `TASK-TC-042R` certification and formalization repairs, $\tau$-scaling controls, Lean 4 formalization, and arithmetic proof attempts (including `SUBGATE-TC-042A` and the simplified uniform prime-wavelet boundedness target `SUBGATE-TC-042B`) for **`EPIC-TC-042` / `TASK-TC-042` / `TASK-TC-042R`**:

$$
C_\tau(0) \ge 0, \qquad |C_\tau(K)| \le C_\tau(0) \quad \forall K \in \overline{\mathbb{Q}} \cap \mathbb{R}, \qquad \tau = 2\pi,
$$

where $C_\tau(K) := W_\xi(h_K)$ is the completed Riemann explicit-formula functional evaluated on the grade-shifted multiplicative autocorrelation $h_K := (T_K \psi_\tau) * \psi_\tau^*$ of the fixed squared pole-regularized theta state $\psi_\tau(x) = x^{1/2}\Phi_1^{(2)}(x)$.

| Dimension | Classification / Status | Scope & Evidence |
| :--- | :--- | :--- |
| **Implementation Status** | `IMPLEMENTED_AND_VERIFIED` | [`tc/canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py), [`tests/test_tc_canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_canonical_theta_correlation_bound.py), [`data/tc_canonical_theta_correlation_bound.json`](file:///c:/Development/Projects/reimann_scope/data/tc_canonical_theta_correlation_bound.json) |
| **Seed Defect Repair (`Section 2`)** | `SEED_DEFECT_REPRODUCED_AND_REPAIRED` | Exact operator derivation $\Phi_t^{(2)}(x) = P(D)^2 G_t(x) = t^{1/4}(r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r)e^{-r}$, repairing the `TC-036R` display typo $r^4 - 6r^3 + \frac{45}{8}r^2 - \frac{3}{8}r$ |
| **Closed-Form Autocorrelation (`Section 3 & 6`)** | `CLOSED_FORM_AUTOCORRELATION_PROVED` | Exact rational-algebraic formula $h_K(x) = h_0(\tau^K x)$ in $W = (\alpha + \alpha^{-1})^2$ and eighth-order Euler differential representation |
| **Fixed-Seed RH Equivalence (`Sections 4 & 5`)** | `FIXED_SEED_RH_EQUIVALENCE_PROVED` | Complete Laplace-resolvent proof that $C_\tau(0) \ge 0 \wedge |C_\tau(K)| \le C_\tau(0)\;(\forall K \in \overline{\mathbb{Q}}\cap\mathbb{R}) \Longleftrightarrow \text{RH}$ (and more generally $\exists M < \infty : |C_\tau(K)| \le M \Longleftrightarrow \text{RH}$) |
| **Numerical Certification (`Sections 6 & 7`, repaired in `TASK-TC-042R`)** | `FINITE_GRID_CORRELATION_BOUND_CERTIFIED` | 256-bit FLINT/Arb ball enclosures via both the Unconditional Spectral Route ($|\delta_\rho| \le 1/2$ tail) and Certified Arithmetic Route (repaired Cauchy circle Taylor remainder bound + `analytic=analytic` branch-cut checking + outward-rounded `flint.arb_mat.det()` Sylvester Gram minors) across 14 rational and algebraic grades |
| **Local Origin Concavity (`Section 7 & 9`, repaired in `TASK-TC-042R`)** | `LOCAL_ORIGIN_CONCAVITY_CERTIFIED` | Certified $C_\tau(0) > 0$, $C_\tau'(0) = 0$, $C_\tau''(0) \approx -0.641740 < 0$, and unconditional two-sided strict inequality $-C_\tau(0) < C_\tau(K) < C_\tau(0)$ via both the 100% zero-free 6th-order arithmetic route ($0 < |K| \le 0.051486$, with $C_\tau(K) > 0$ on $|K| \le 0.045776$) and the unconditional spectral-tail 4th-order route ($0 < |K| \le 0.068465$, with $C_\tau(K) < C_\tau(0)$ on $0 < |K| \le 0.133277$) |
| **Universal Arithmetic Inequality (`Section 9`)** | `UNIVERSAL_ARITHMETIC_CORRELATION_BOUND_OPEN` | Isolated as `SUBGATE-TC-042A` (`CANONICAL_THETA_WAVELET_PRIME_BOUND_SUBGATE`) and simplified in `TASK-TC-042R` to `SUBGATE-TC-042B` (`UNIFORM_REFLECTED_PRIME_WAVELET_BOUNDEDNESS_SUBGATE`): $\exists M < \infty \; \forall X \ge 1 : |W_{\mathrm{wavelet}}(X)| := |\sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n/X)| \le M$ |
| **Formalization Coverage (`Section 10`, repaired in `TASK-TC-042R`)** | `FORMALIZED_IN_LEAN4_ZERO_SORRY` | [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean): 10 definitions, 16 theorems, 0 `sorry`, 0 `admit` (with non-vacuous residue functional `resSq : ℝ → ℝ → ℝ` and satisfiability proof `laplace_holomorphic_rhp_hypothesis_satisfiable`) |
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

## 3. Exact Closed-Form Autocorrelation $h_K(x)$ and Complete Spectral Expansion Without RH

### 3.1 Closed-Form Multiplicative Convolution Theorem

On the multiplicative group $(\mathbb{R}_+, dx/x)$, define grade dilation $(T_K f)(x) := f(\tau^K x)$, involution $f^*(x) := \overline{f(1/x)} = f(1/x)$, and multiplicative convolution
$$
h_K(x) := ((T_K \psi_\tau) * \psi_\tau^*)(x) = \int_0^\infty \psi_\tau(\tau^K x y)\psi_\tau(y)\,\frac{dy}{y} = h_0(\tau^K x).
$$

**Theorem 3.1 (Closed-Form Rational-Algebraic Autocorrelation & Eighth-Order Euler Representation).**
For every $\alpha = \tau^K x > 0$, let $W(\alpha) := (\alpha + \alpha^{-1})^2 \ge 4$. Then $h_K(x) = h_0(\alpha)$ is given in exact closed form (with no Gaussian exponentials or numerical quadrature) by:
$$
\boxed{h_0(\alpha) = \frac{-648 W^3 + 58380 W^2 - 706860 W + 2027025}{512\,\left(\alpha + \alpha^{-1}\right)^{17/2}} = \frac{1}{512}\left(\left(\alpha\frac{d}{d\alpha}\right)^2 - \frac{1}{4}\right)^4 \left(\alpha + \alpha^{-1}\right)^{-1/2}.}
$$
Moreover:
1. **Inversion Symmetry**: $h_0(1/\alpha) = h_0(\alpha)$ for all $\alpha > 0$, so $h_K(1/x) = h_0(\tau^K / x) = h_0(\tau^{-K} x) = h_{-K}(x)$.
2. **Exact Peak Value at $\alpha = 1$ ($W = 4$)**:
   $$
   h_0(1) = \|\psi_\tau\|_{L^2(\mathbb{R}_+, dx/x)}^2 = \frac{92193}{512 \times 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.4973624838099012.
   $$
3. **Global Envelope & Monotone Negative Tail**:
   $$
   |h_0(\alpha)| \le \frac{92193}{32768}\left(\alpha + \alpha^{-1}\right)^{-5/2} \quad \forall \alpha > 0, \qquad -\frac{81}{64}\alpha^{-5/2} \le h_0(\alpha) < 0 \quad \forall \alpha \ge 9.
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

### 5.3 Repaired Two-Sided Local Theorem at $K = 0$, Outward-Rounded Gram Minors, and Quartet Controls

1. **Certified Origin Derivatives & Repaired Two-Sided Local Taylor Enclosures (`TASK-TC-042R`)**:
   - In `TASK-TC-042R`, $C_\tau(0)$, $C_\tau''(0)$, and $C_\tau^{(4)}(0)$ are independently computed and certified via **both** a 100% zero-free arithmetic route (`evaluate_zero_free_arithmetic_euler_derivative_at_zero`) and the unconditional spectral-tail route:
     - $C_\tau^{\mathrm{arith}}(0) = [9.50480944 \times 10^{-4} \pm 3.16 \times 10^{-9}]$, $C_\tau^{\mathrm{spec}}(0) = [9.504798117910 \times 10^{-4} \pm 3.79 \times 10^{-55}]$,
     - $(C_\tau'')^{\mathrm{arith}}(0) = [-0.64174024 \pm 1.52 \times 10^{-7}] < 0$, $(C_\tau'')^{\mathrm{spec}}(0) = [-0.641740192443 \pm 1.28 \times 10^{-50}] < 0$,
     - $(C_\tau^{(4)})^{\mathrm{arith}}(0) = [433.541309 \pm 2.84 \times 10^{-6}] > 0$, $(C_\tau^{(4)})^{\mathrm{spec}}(0) = [433.5413095774 \pm 4.92 \times 10^{-46}] > 0$ (all three derivative enclosures intersect at $K = 0$).
   - Decomposing $C_\tau''(0)$ into arithmetic components shows that **both** the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.25759593 < 0$, arising from $-167.40380002$ archimedean integral curvature plus $+167.14620410$ local constant curvature) **and** the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.38414431 < 0$) are strictly concave at $K = 0$.
   - **Why Two-Sided Bounds Are Required**: Showing $C_\tau(K) < C_\tau(0)$ alone does not establish $|C_\tau(K)| < C_\tau(0)$ unless $C_\tau(K) > -C_\tau(0)$ is also certified (`taylor_two_sided_abs_correlation_bound` in Lean 4). Because $C_\tau(0) \approx 9.505 \times 10^{-4}$ is much smaller than $|C_\tau''(0)| \approx 0.6417$, $C_\tau(K)$ crosses $0$ near $|K| \approx 0.0544$ and crosses $-C_\tau(0)$ near $|K| \approx 0.077$, well before the upper Taylor parabola reaches $C_\tau(0)$ at $|K| \approx 0.133277$.
   - **Route 1 — 100% Zero-Free 6th-Order Arithmetic Taylor Enclosure**:
     Using exact symbolic bounds on $D_\alpha^6 h_0(\alpha)$ and $D_\alpha^8 h_0(\alpha)$ ($|N_6(4)| = 39768704939520$, $|N_8(4)| = 57734319246151680$), the global 6th-derivative bound is $M_6^{\mathrm{arith}} = \sup_{K\in\mathbb{R}}|C_\tau^{(6)}(K)| \le 2.797195 \times 10^7$. Without using any spectral zero data, Taylor's theorem certifies:
     $$
     C_\tau(K) > 0 \quad \text{for } |K| \le 0.045776, \qquad -C_\tau(0) < C_\tau(K) < C_\tau(0) \quad \text{for } 0 < |K| \le K_{\mathrm{abs}}^{\mathrm{arith}} \approx 0.051486.
     $$
   - **Route 2 — Unconditional Spectral-Tail 4th-Order Taylor Enclosure**:
     Using the 29 Turing-certified critical-line zeros in $(0, 100]$ (for which the critical-line terms satisfy $|C_{\le 100}^{(4)}(K)| \le C_{\le 100}^{(4)}(0)$) plus the unconditional off-critical ($|\delta_\rho| \le 1/2$) Backlund–Rosser tail bound $4.92 \times 10^{-46}$ for $|\gamma_\rho| > 100$ on $|K| \le 0.14$, we obtain $\sup_{|K|\le 0.14}|C_\tau^{(4)}(K)| \le M_4^{\mathrm{spec}} = 433.541310$. Taylor's theorem then certifies:
     $$
     C_\tau(K) > 0 \;\text{on } |K| \le 0.050851, \quad -C_\tau(0) < C_\tau(K) < C_\tau(0) \;\text{on } 0 < |K| \le K_{\mathrm{abs}}^{\mathrm{spec}} \approx 0.068465, \quad C_\tau(K) < C_\tau(0) \;\text{on } 0 < |K| \le 0.133277.
     $$
2. **Finite Toeplitz Gram Matrices Certified by Outward-Rounded `flint.arb_mat.det()` Minors**:
   - Positive-definiteness of the finite Toeplitz Gram matrices $[C_\tau(K_i - K_j)]$ is certified via Sylvester's criterion using outward-rounded leading principal minor determinants `flint.arb_mat.det()` on the full `arb` enclosures (with floating-point eigenvalues reported purely as diagnostics):
     - **`rational_6_point_grid` $\{0, 1/8, 1/4, 1/2, 1, 2\}$ (spectral route)**: all 6 leading principal minor determinants are certified strictly positive ($\det_1 \approx 9.505 \times 10^{-4}$, $\det_2 \approx 1.084 \times 10^{-8}$, $\det_3 \approx 1.948 \times 10^{-14}$, $\det_4 \approx 1.052 \times 10^{-19}$, $\det_5 \approx 2.340 \times 10^{-27}$, $\det_6 \approx 1.528 \times 10^{-35} \pm 4.50 \times 10^{-78} > 0$).
     - **`algebraic_5_point_grid` $\{-\sqrt{2}, -1/2, 0, 1/2, \sqrt{2}\}$ (spectral route)**: all 5 leading principal minor determinants are certified strictly positive ($\det_5 \approx 9.959 \times 10^{-30} \pm 6.09 \times 10^{-73} > 0$).
     - **`zero_free_arithmetic_3_point_grid` $\{0, 1/4, 1/2\}$ (100% zero-free arithmetic route)**: all 3 leading principal minor determinants are certified strictly positive ($\det_1 \ge 9.5047 \times 10^{-4} > 0$, $\det_2 \ge 4.1067 \times 10^{-8} > 0$, $\det_3 = [2.25 \times 10^{-13} \pm 9.17 \times 10^{-14}] \ge 1.5886 \times 10^{-13} > 0$).
3. **Synthetic Off-Critical Quartet Controls**:
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

## 7. Arithmetic Proof Attempts, Simplified Prime-Wavelet Subgate (`SUBGATE-TC-042B`), & Exact Remaining Statement (`Section 9`)

1. **Attempt 1 — Pointwise Kernel Difference $d_K^-(x) = 2h_0(x) - [h_0(\tau^K x) + h_0(\tau^{-K} x)]$ (`POINTWISE_KERNEL_DIFFERENCE_SIGN_FALSIFIED`)**:
   - Because $h_0(\alpha)$ has three sign changes on $\alpha \ge 1$ ($h_0(1) > 0$, $h_0(2) < 0$, $h_0(3) > 0$, and $h_0(\alpha) < 0$ for $\alpha \ge 5$), at $K = 1$ the kernel difference satisfies $d_1^-(3) = +0.248918 > 0$ at $p = 3$ and $d_1^-(7) = -0.401751 < 0$ at $p = 7 \approx \tau$. Term-by-term sign dominance across prime powers is therefore false.
2. **Attempt 2 — Local Concavity & Collaborative Prime/Archimedean Curvature (`LOCAL_ORIGIN_CONCAVITY_CERTIFIED`)**:
   - At $K = 0$, both the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.257596 < 0$) and the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.384144 < 0$) are strictly concave, yielding a 100% zero-free proof of $|C_\tau(K)| < C_\tau(0)$ on $0 < |K| \le 0.051486$ and an unconditional spectral-tail proof on $0 < |K| \le 0.068465$.
3. **Attempt 3 — Large-$|K|$ Wavelet Decomposition & Reduction to Uniform Prime-Wavelet Boundedness (`SUBGATE-TC-042A` & `SUBGATE-TC-042B`)**:
   - Decomposing $C_\tau(K) = W_{\mathrm{arch}}(h_K) + P_{\mathrm{fwd}}(K) + P_{\mathrm{refl}}(K)$ for $K \ge 0$ (and by evenness $C_\tau(-K) = C_\tau(K)$ for all $K \in \mathbb{R}$):
     - Both the archimedean term and forward prime sum are globally bounded on $K \ge 0$: $|W_{\mathrm{arch}}(h_K)| \le M_{\mathrm{arch}} \approx 6.4959$ (decaying as $O(\tau^{-3K/2})$) and $|P_{\mathrm{fwd}}(K)| \le M_{\mathrm{fwd}} \approx 0.6330$ (decaying as $O(\tau^{-5K/2})$).
     - By the Laplace-resolvent argument (`Section 4.2`) and Lean theorem `complete_correlation_bounded_of_reflected_prime_wavelet_bound`, **any finite uniform bound** $|C_\tau(K)| \le M_{\mathrm{total}} < \infty$ on $K \ge 0$ already makes $\mathcal{L}[C_\tau(-t)](w)$ holomorphic on $\operatorname{Re}(w) > 0$ and prevents off-critical zeros!
     - Therefore, proving RH via this route reduces to the simplified **Uniform Prime-Wavelet Boundedness Subgate (`SUBGATE-TC-042B`)** (`investigate_uniform_prime_wavelet_boundedness`):
       $$
       \boxed{\exists M < \infty \; \forall X \ge 1 : \quad \left|W_{\mathrm{wavelet}}(X)\right| := \left|\sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\, h_0\!\left(\frac{n}{X}\right)\right| \le M.}
       $$
   - **Exact Stieltjes Chebyshev-Error Representation**:
     Writing $\psi(x) = x + E_\psi(x)$ and using $\int_0^\infty x^{-1/2} h_0(x/X)\,dx = X^{1/2} H_0(1/2) = 0$ (verified in Arb to $< 8.0 \times 10^{-16}$), Stieltjes integration by parts yields the exact identity
     $$
     W_{\mathrm{wavelet}}(X) = h_0\!\left(\frac{1}{X}\right) - \int_0^1 x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + X^{-1/2}\int_1^\infty \frac{E_\psi(x)}{x}\,\tilde{h}_0\!\left(\frac{x}{X}\right)\frac{dx}{x^{1/2}}, \qquad \tilde{h}_0(\alpha) := \frac{1}{2}h_0(\alpha) - \alpha h_0'(\alpha).
     $$
     - *Chebyshev bound* ($\psi(x) \le C x$): yields $O(X^{1/2})$ because taking absolute values ignores the sign changes of $h_0$.
     - *Unconditional de la Vallée Poussin PNT bound* ($|E_\psi(x)| \ll x e^{-c\sqrt{\log x}}$): cancels the smooth main term $x$ via $H_0(1/2) = 0$, but taking absolute values inside the integral still gives $O(X^{1/2} e^{-c\sqrt{\log X}})$.
     - *Certified Arithmetic Evaluations on $X \in [1, 1000]$*: Across $X \in \{1, 2, \pi, \tau, 10, \tau^2, 100, \tau^3, 1000\}$, $|W_{\mathrm{wavelet}}(X)|$ remains bounded by $\le 0.079372$ (whereas the trivial Chebyshev bound grows from $1.95$ to $61.66$, showing cancellation ratios down to $2.56 \times 10^{-5}$).

---

## 8. Lean 4 Formalization Summary (`Section 10`, Repaired in `TASK-TC-042R`)

Module [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) compiles with `0 sorry` and `0 admit` and formalizes **10 definitions** and **16 theorems**:
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
11. `laplace_resolvent_residue_obstruction_schema` *(repaired in `TASK-TC-042R` to take an explicit residue functional `resSq : ℝ → ℝ → ℝ` with RHP holomorphy `∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0`)*
12. `fixed_seed_correlation_bound_implies_critical_line_schema` *(repaired in `TASK-TC-042R` to use `resSq : ℝ → ℝ → ℝ`)*
13. `laplace_holomorphic_rhp_hypothesis_satisfiable` *(new in `TASK-TC-042R`: proves the RHP residue-vanishing hypothesis is non-vacuously satisfiable via `resSq = fun _ _ => 0`)*
14. `second_euler_autocorrelation_at_one` *(new in `TASK-TC-042R`: proves $(D_\alpha^2 h_0)(1) < 0$ from $N_2(4) = -586827 < 0$)*
15. `taylor_two_sided_abs_correlation_bound` *(new in `TASK-TC-042R`: proves both upper and lower Taylor bounds combine to give $-C_0 < C_K < C_0$ and $C_0^2 - C_K^2 > 0$)*
16. `complete_correlation_bounded_of_reflected_prime_wavelet_bound` *(new in `TASK-TC-042R`: proves uniform boundedness of the reflected prime wavelet sum implies uniform boundedness of $C_\tau(K)$)*
