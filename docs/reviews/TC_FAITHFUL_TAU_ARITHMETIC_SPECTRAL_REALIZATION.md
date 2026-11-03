# Faithful $\tau$-Arithmetic Spectral Realization, Adjoint Compatibility, Canonical Hilbert–Schmidt Orbit Decomposition, and Resonant-Band Prime-Separation / Summation-by-Parts Analysis (`TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2` / `TASK-TC-051` / `TASK-TC-051R`)

**Task ID:** `TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2` / `TASK-TC-051` / `TASK-TC-051R`  
**Parent Epic:** `EPIC-TC-042`  
**Reviewed Baselines:** `5da0eb79e1732ff871ee1c7fee729c62972aa406` (`TC-048R`), `2f7871fff666091c4152ecc8657f2345aacdd4fa` (`TC-050` + `TC-049R`), `0e6ae36ce995ef3037652b3dfb67645325f990b1` (`TC-050R` HEAD; implementation commit `f5521363ea94774938fd37152d67d743413327ae`), `d93ab512c2df75af2365a3963804c172baf0e867` (`TC-050R2` merged on `main`), `b6f22dfee0dd6177ee855189304e7930f9ba3e20` (`TC-051` merged on `main`; branch tip `7ac0546b1177970ff0d87824f61643da2405c4c0`, implementation commit `333661eecd69738e8a67143e635b6db4f40170ce`)  
**Branched From:** `b6f22dfee0dd6177ee855189304e7930f9ba3e20` (`task/tc-051r-identity-certificate-and-report-reconciliation`)  
**Primary Implementation Module:** [tc/faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)  
**Exported Facade Entrypoints:** [`execute_task_tc050_faithful_spectral_realization_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10175), [`execute_task_tc051_prime_arithmetic_resonant_band_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10175)  
**Certified 256-bit Arb Data Artifact:** [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json) (`708/708` certified 256-bit Arb balls passing outward-rounded decimal round-trip verification)  
**Formal Verification Module:** [formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) (`44` definitions, `56` theorems = `100` declarations, `0` `sorry`, `0` `admit`, `0` custom axioms)  
**Regression Test Suite:** [tests/test_tc_faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tests/test_tc_faithful_tau_arithmetic_spectral_realization.py)  
**Status Classification:** `ADJOINT_COMPATIBILITY_HYPERBOLIC_NULL_CONE_AND_CANONICAL_HILBERT_SCHMIDT_ORBIT_DECOMPOSITION_PROVED_RESONANT_BAND_EQUIVALENCE_ISOLATED_SUBGATE_OPEN` (`PROVED_CONDITIONAL` + `CERTIFIED_FINITE`; `SUBGATE-TC-043A` remains `OPEN`; `rh_proved: false`)

---

## 1. Objective and Preserved TC Architecture

The objective of `TASK-TC-050` is to investigate and advance the missing implication in the Transcendental Continuation (TC) programme:
$$
\text{Actual prime arithmetic and }\tau\text{-normalized Fourier duality}
\;\Longrightarrow\;
\text{a faithful spectral realization excluding off-critical growth.}
$$

Throughout this work we preserve the project's native mathematical conventions:
1. **Circle Constant and Concurrent Algebraic Grades**:
   $$
   \tau = 2\pi \approx 6.2831853071795865, \qquad L = \log\tau \approx 1.8378770664093455, \qquad K \in \mathbb{A}_{\mathbb{R}} := \overline{\mathbb{Q}} \cap \mathbb{R},
   $$
   including both positive and negative rational and irrational real algebraic grades.
2. **Lindemann–Weierstrass & Gelfond–Schneider Scope Hygiene**:
   Because $\tau = 2\pi$ is transcendental by Lindemann (1882), $\tau^q$ is transcendental for every nonzero rational grade $q \in \mathbb{Q} \setminus \{0\}$, so integer ratios $m/n \in \mathbb{Q}_{>0}$ can never collide with $\tau^{q_1 - q_2}$ for distinct rational grades $q_1 \ne q_2$. We **do not** assume transcendence of $\tau^K$ for general irrational algebraic $K \in \mathbb{A}_{\mathbb{R}} \setminus \mathbb{Q}$ (which remains an open Schanuel-type problem); where density of $\mathbb{Q}$ in $\mathbb{A}_{\mathbb{R}}$ and $\mathbb{R}$ suffices for the spectral and Laplace–Carleman continuation steps, we state that explicitly.
3. **Preserved `TC-049`/`TC-049R` Arithmetic Cancellation Baseline**:
   All work preserves the `TC-049`/`TC-049R` repaired 4th-order Euler–Maclaurin decay bound $|W_{\log}(X)| \le C_{\log,\mathrm{EM}}\,X^{-5/2}$ ($C_{\log,\mathrm{EM}} = [13.46851 \pm 4.74 \times 10^{-6}] < 13.468515$ for all $X \ge 1$) and the unconditional three-zone divisor reduction of $R_\mu(X) = \sum_{m\ge 2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ to the localized resonant divisor band $X^{5/6} < m \le M(X) := \lceil\max(2, X^{5/4})\rceil$ (`SUBGATE-TC-043A`).

---

## 2. Classification of $\tau$-Coupled Roles and Arithmetic vs. Analytic Prime Transformations (`Section 1`, Theorem 52)

### 2.1 Four Distinct Roles of $\tau = 2\pi$

To avoid conflating distinct mechanisms, we separate the four places where $\tau = 2\pi$ enters the construction:

1. **Role 1 — Tate Adelic Rational-Diagonal Character Normalization (Cassels–Fröhlich Ch. XV, §2.2)**:
   For each finite prime $p$, let $\{x_p\}_p \in \mathbb{Z}[1/p] \cap [0, 1)$ denote the $p$-adic fractional part (principal part at $p$), and define the local additive character
   $$
   \psi_p(x_p) := \exp\!\bigl(i\,\tau\,\{x_p\}_p\bigr) = \exp\!\bigl(2\pi i\,\{x_p\}_p\bigr), \qquad \ker(\psi_p) = \mathbb{Z}_p.
   $$
   For any rational number $q \in \mathbb{Q}$ embedded diagonally in $\mathbb{A}_{\mathbb{Q}}$, partial-fraction decomposition over prime powers gives
   $$
   q = \sum_p \{q\}_p + n(q), \qquad n(q) \in \mathbb{Z},
   $$
   where $\{q\}_p = 0$ for all $p \nmid \operatorname{denom}(q)$ and $q - \{q\}_p \in \mathbb{Z}_{(p)}$. Therefore, for an archimedean character $\psi_\infty(x_\infty) = \exp(-i c_\infty x_\infty)$, the global product over all places $v \le \infty$ evaluates on $q \in \mathbb{Q}$ to
   $$
   \prod_{v \le \infty} \psi_v(q) = \exp\!\left(i\sum_p \tau\{q\}_p - i c_\infty q\right) = \exp\!\bigl(i(\tau - c_\infty)q - i\tau\,n(q)\bigr) = \exp\!\bigl(i(\tau - c_\infty)q\bigr)
   $$
   because $\exp(-i\tau\,n(q)) = \exp(-2\pi i\,n(q)) = 1$ for every $n(q) \in \mathbb{Z}$. Vanishing of the phase discrepancy (`adelicPhaseDiscrepancy` in Lean 4) for all $q \in \mathbb{Q}$ uniquely forces
   $$
   \boxed{c_\infty = \tau = 2\pi, \qquad \psi_\infty(x_\infty) = e^{-i\tau x_\infty}, \qquad \psi\big|_{\mathbb{Q}} \equiv 1, \qquad (\mathbb{A}_{\mathbb{Q}}/\mathbb{Q})^\wedge \cong \mathbb{Q}.}
   $$
   With this canonical character, the self-dual Fourier transform $\widehat{f}(y) = \int_{\mathbb{R}} f(x)e^{-i\tau xy}\,dx$ and multiplicative convolution $(f_1 * f_2)(x) = \int_0^\infty f_1(x/y)f_2(y)\,\frac{dy}{y}$ satisfy both Plancherel $\|\widehat{f}\|_{L^2(\mathbb{R})} = \|f\|_{L^2(\mathbb{R})}$ and Mellin convolution multiplicativity (`tate_rational_diagonal_character_rigidity_and_convolution_isometry`, Theorem 52 in Lean 4).

2. **Role 2 — Opposite-Grade Poisson Lattice Duality**:
   Under $\widehat{f}(y) = \int_{\mathbb{R}} f(x)e^{-i\tau xy}\,dx$, the integer lattice $\mathbb{Z} \subset \mathbb{R}$ has unit covolume and equals its own Pontryagin dual $\mathbb{Z}^\perp = \mathbb{Z}$. Scaling the spatial lattice to $\tau^K \mathbb{Z}$ scales the dual lattice to the **opposite grade** $(\tau^K\mathbb{Z})^\perp = \tau^{-K}\mathbb{Z}$ with invariant covolume product $\tau^K \cdot \tau^{-K} = 1$, yielding opposite-grade Poisson summation:
   $$
   \sum_{n \in \mathbb{Z}} f(n\tau^K) = \tau^{-K} \sum_{m \in \mathbb{Z}} \widehat{f}(m\tau^{-K}).
   $$

3. **Role 3 — Grade Base $\tau^K$ and Prime-Power Station Transport**:
   The unitary grade dilation on $L^2(\mathbb{R}_{>0}, d^\times x)$ ($d^\times x = dx/x$) or $L^2(\mathbb{R}, dx)$ is
   $$
   (T_K f)(x) := f(\tau^{-K} x) \quad \text{on } L^2(\mathbb{R}_{>0}, d^\times x), \qquad (U_K f)(x) := \tau^{-K/2} f(\tau^{-K} x) \quad \text{on } L^2(\mathbb{R}, dx),
   $$
   which shifts prime-power stations $n = p^k$ to $n\tau^K$ (additive translation $\log n + K\log\tau$ in logarithmic coordinates $u = \log x$).

4. **Role 4 — Canonical Self-Dual Theta Gaussian & Pole-Annihilation Operator $P(D)$**:
   The self-dual Gaussian $G_t(x) = t^{1/4} e^{-(\tau/2)t x^2} = t^{1/4} e^{-\pi t x^2}$ has quadratic exponent $\tau/2 = \pi$ locked to the Fourier kernel $e^{-i\tau xy}$. Its Mellin transform carries the archimedean factor $(\tau/2)^{-s/2}\Gamma(s/2) = \pi^{-s/2}\Gamma(s/2)$, and the differential operator $P(D) = D^2 - \frac{1}{16}$ ($D = t\frac{d}{dt}$) simultaneously annihilates both endpoint poles at $s = 0$ and $s = 1$.

---

### 2.2 Arithmetic Grade Shifts $p\tau^K$ vs. Analytic Prime Powers $p^{\tau^{-K}}$ and Exact Semidirect Intertwining

A foundational requirement of `TASK-TC-050` is to keep the two prime-indexed grade actions strictly distinct:

| Operation | Spatial Action on $f(x)$ | Logarithmic Action on $F(u) = f(e^u)$ ($u = \log x$) | Role in TC Programme |
| :--- | :--- | :--- | :--- |
| **Arithmetic Grade Shift** $D_{p,K}$ (station $p\tau^K$) | $(D_{p,K} f)(x) = f(p^{-1}\tau^{-K} x)$ | $(D_J F)(u) = F(u - J)$ with $J = \log p + K\log\tau$ (`logPrimeShiftAction`) | Multiplicative dilation / log-translation shifting prime stations in $W(\tau^K)$ and Zeta sampling |
| **Analytic Prime Power** $A_K$ (power $p^{\tau^{-K}}$) | $(A_K f)(x) = f(x^{\tau^{-K}})$ | $(A_K F)(u) = F(\tau^{-K} u)$ (`logScaleAction`) | Exponent rescaling $p^{-s} \mapsto p^{-\tau^{-K} s} = (p^{\tau^{-K}})^{-s}$ in $\mathcal{Z}_\tau(s, K) = \zeta(\tau^{-K} s)$ |

- **Exact Semidirect Intertwining Law (Verified in SymPy & Lean 4 Theorem 52)**:
  For any logarithmic translation $D_J F(u) = F(u - J)$ and logarithmic scaling $A_K F(u) = F(\tau^{-K} u)$,
  $$
  (D_J A_K F)(u) = F\bigl(\tau^{-K}(u - J)\bigr) = F\bigl(\tau^{-K} u - J\tau^{-K}\bigr) = (A_K D_{J\tau^{-K}} F)(u),
  $$
  and equivalently
  $$
  \boxed{D_J A_K = A_K D_{J\tau^{-K}}, \qquad A_K D_J = D_{J\tau^K} A_K.}
  $$
  Thus $\{D_J\}$ and $\{A_K\}$ do **not** commute for $K \ne 0$: they generate the non-abelian affine semidirect product $\mathbb{R} \rtimes \mathbb{R}_{>0}$ acting on the logarithmic line $u = \log x$.
- **Exact Zeta-Operator Grade-Sampling Identity**:
  For the summation operator $(Zf)(x) := \sum_{n=1}^\infty f(nx)$, evaluating $Z$ on the grade-dilated state $U_{-K} f$ at $x = 1$ yields the exact arithmetic grade-shifted lattice sum:
  $$
  \boxed{Z(U_{-K} f)(1) = \sum_{n=1}^\infty (U_{-K} f)(n) = \tau^{K/2} \sum_{n=1}^\infty f(n\tau^K) = \tau^{K/2}\,(Zf)(\tau^K).}
  $$
- **Exact Generator Identity with Connes–Consani–Moscovici (`arXiv:2511.22755`, Lemma 7.1)**:
  With $r = \frac{\tau}{2}x^2 = \pi x^2$, the single-pole-annihilated generator $P(D)G_1(x) = (r^2 - \frac{3}{2}r)e^{-r}$ and its normalized counterpart $f_\tau(x) = 8\,P(D)G_1(x) = 2(\tau^2 x^4 - 3\tau x^2)e^{-(\tau/2)x^2}$ satisfy identically (`symbolic_f_tau_minus_8_h_CCM_zero == True` in SymPy):
  $$
  \boxed{P(D)G_1(x) = \frac{\pi}{2}x^2(2\pi x^2 - 3)e^{-\pi x^2} = h_{\mathrm{CCM}}(x) = \frac{\sqrt{3}}{2^{11/4}}h_4(x) - \frac{3}{2^{17/4}}h_0(x), \qquad f_\tau(x) = 8\,h_{\mathrm{CCM}}(x),}
  $$
  where $h_n(x) = \frac{2^{1/4}}{\sqrt{n!\,4^n}}(-1)^n e^{\pi x^2}\frac{d^n}{dx^n}(e^{-2\pi x^2})$ is the Hermite basis of $L^2(\mathbb{R})^{\mathrm{ev}}$ in Connes–Consani–Moscovici (`arXiv:2511.22755`, Lemma 7.1). Passing from $P(D)G_1(x)$ to the squared pole-regularized seed $\Phi_1^{(2)}(x) = P(D)^2 G_1(x) = (r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r)e^{-r}$ upgrades the simple endpoint zeros at $s = 0, 1$ to double zeros $F_\tau(s) = \frac{s^2(s-1)^2}{32}\pi^{-s/2}\Gamma(s/2)$.

---

## 3. Adjoint Compatibility on the Grade Algebra, the Hyperbolic Pair Null-Cone Obstruction, and Multiplicity Socle Eigenvectors (`Section 2`, Theorem 51)

### 3.1 Multiplicative vs. Star-Involution Compatibility on $\mathbb{C}[\mathbb{A}_{\mathbb{R}}]$

Let $\mathcal{A}_{\mathrm{grade}} = \mathbb{C}[\mathbb{A}_{\mathbb{R}}]$ be the commutative group star-algebra generated by formal grade shifts $\{V_K : K \in \mathbb{A}_{\mathbb{R}}\}$ with group law and involution
$$
V_K V_J = V_{K+J}, \qquad V_0 = I, \qquad V_K^* := V_{-K}.
$$
In any spectral realization on which grade shifts act on the zero eigenspace at $\rho = \frac{1}{2} + \delta + i\gamma$ ($\delta = \operatorname{Re}(\rho) - \frac{1}{2}$) via the character
$$
\chi_\rho(V_K) := \tau^{K(\rho - 1/2)} = \tau^{K\delta}\,e^{i K\gamma\log\tau},
$$
we separate two properties that are frequently conflated:

1. **Multiplicative Homomorphism Holds Unconditionally for Every $\rho \in \mathbb{C}$**:
   $$
   \chi_\rho(V_K V_J) = \tau^{(K+J)(\rho - 1/2)} = \tau^{K(\rho - 1/2)}\,\tau^{J(\rho - 1/2)} = \chi_\rho(V_K)\,\chi_\rho(V_J).
   $$
   Hence mere multiplicative compatibility across grades $K, J$ imposes **zero restriction** on $\delta = \operatorname{Re}(\rho) - \frac{1}{2}$.
2. **Star-Involution Compatibility Holds If and Only If $\operatorname{Re}(\rho) = 1/2$**:
   Compare $\chi_\rho(V_K^*)$ against $\overline{\chi_\rho(V_K)}$:
   $$
   \chi_\rho(V_K^*) = \chi_\rho(V_{-K}) = \tau^{-K\delta}\,e^{-i K\gamma\log\tau},
   \qquad
   \overline{\chi_\rho(V_K)} = \tau^{+K\delta}\,e^{-i K\gamma\log\tau}.
   $$
   Their radial difference (`gradeRadialCharacter r (-1) - gradeRadialCharacter r 1` in Lean 4, where $r = \tau^{K\delta} > 0$) is:
   $$
   \boxed{\tau^{-K\delta} - \tau^{K\delta} = \frac{1 - \tau^{2K\delta}}{\tau^{K\delta}} = -2\sinh(K\delta\log\tau) = 0 \quad (\forall K \ne 0) \iff \tau^{K\delta} = 1 \iff \delta = \operatorname{Re}(\rho) - \frac{1}{2} = 0.}
   $$

---

### 3.2 Why Functional-Equation Pairing $\rho \leftrightarrow 1 - \bar{\rho}$ Produces a Signature-$(1,1)$ Null Cone When $\delta \ne 0$

By the functional equation $\xi(1 - s) = \xi(s)$, an off-critical zero $\rho = \frac{1}{2} + \delta + i\gamma$ ($\delta \ne 0$) is paired with the distinct zero
$$
\rho^\sharp := 1 - \bar{\rho} = \frac{1}{2} - \delta + i\gamma \ne \rho, \qquad \text{for which} \qquad \chi_{\rho^\sharp}(V_K) = \tau^{-K\delta}\,e^{i K\gamma\log\tau} = \overline{\chi_\rho(V_K^*)}.
$$
Let $B : W_\rho \times W_\rho \to \mathbb{C}$, $W_\rho = \operatorname{span}\{e_\rho, e_{\rho^\sharp}\}$, be any Hermitian sesquilinear form satisfying adjoint invariance $B(V_K u, v) = B(u, V_{-K} v)$ for all $K \in \mathbb{A}_{\mathbb{R}}$. Then:
1. **Isotropic Diagonal Forced by $\delta \ne 0$**:
   $$
   B(V_K e_\rho, e_\rho) = \tau^{K(\delta + i\gamma)} B(e_\rho, e_\rho) = B(e_\rho, V_{-K} e_\rho) = \tau^{K(-\delta + i\gamma)} B(e_\rho, e_\rho)
   \implies \bigl(\tau^{K\delta} - \tau^{-K\delta}\bigr) B(e_\rho, e_\rho) = 0.
   $$
   Choosing $K = 1$ ($\tau^\delta \ne \tau^{-\delta}$ since $\delta \ne 0$) forces
   $$
   B_{11} := B(e_\rho, e_\rho) = 0, \qquad\text{and identically}\qquad B_{22} := B(e_{\rho^\sharp}, e_{\rho^\sharp}) = 0.
   $$
2. **Indefinite Hyperbolic Plane (`hyperbolicPairForm`, Lean 4 Theorem 51)**:
   On the cross-term $B_{12} := B(e_\rho, e_{\rho^\sharp})$, the radial factors $\tau^{K\delta}$ and $\tau^{-K\delta}$ cancel identically:
   $$
   B(V_K e_\rho, e_{\rho^\sharp}) = \tau^{K(\delta + i\gamma)} B_{12} = \overline{\tau^{-K(-\delta - i\gamma)}} B_{12} = B(e_\rho, V_{-K} e_{\rho^\sharp}).
   $$
   In a normalized basis with $B_{12} = 1$, the Hermitian form on $W_\rho$ is the hyperbolic form (`hyperbolicPairForm`):
   $$
   \boxed{B(c_1 e_\rho + c_2 e_{\rho^\sharp},\; c_1 e_\rho + c_2 e_{\rho^\sharp}) = 2\operatorname{Re}(\bar{c}_1 c_2) = \frac{1}{2}|c_1 + c_2|^2 - \frac{1}{2}|c_1 - c_2|^2, \qquad \det\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = -1 < 0,}
   $$
   which has **signature $(1, 1)$**:
   - **Null cone**: $B(e_\rho, e_\rho) = B(e_{\rho^\sharp}, e_{\rho^\sharp}) = 0$;
   - **Positive vector**: $u_+ = e_\rho + e_{\rho^\sharp}$ gives $B(u_+, u_+) = +2 > 0$;
   - **Strictly negative vector**: $u_- = e_\rho - e_{\rho^\sharp}$ gives $B(u_-, u_-) = -2 < 0$.
   Consequently, if $(B, W_\rho)$ is embedded into any Hilbert space (where $\langle v, v\rangle \ge 0$ for all $v$), then $B(u_-, u_-) \ge 0$ forces $B_{12} = 0$, killing $W_\rho$ identically. Thus a **faithful** Hilbert-space realization of the nontrivial zeros of $\xi(s)$ with unitary grade shifts $V_K^* = V_{-K}$ can exist if and only if $\delta = 0$ for every zero.

---

### 3.3 Exact Multiplicity Handling: Scalar Correlation Boundedness vs. Socle and Full Generalized-Eigenspace Realizations ($m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$)

We never assume simplicity of the zeros of $\xi(s)$, and we keep the **scalar correlation equivalence** and the **two operator-level realization statements** strictly distinct (`TASK-TC-050R2` Section 5 reconciliation):

1. **Scalar Correlation Boundedness vs. RH Holds Unconditionally in Multiplicity ($m_\rho \ge 1$ in Both Directions)**:
   In the Weil explicit formula for $C_\tau(K) = Q_\tau(T_K\psi_\tau, \psi_\tau)$, the zero sum comes from Cauchy's residue theorem applied to the logarithmic derivative $\xi'(s)/\xi(s)$ (or $-\xi'(s)/\xi(s)$ with opposite contour orientation) integrated against the holomorphic Mellin kernel $H_K(s - 1/2) = \tau^{-K(s - 1/2)} H_0(s - 1/2)$. Because $\xi'(s)/\xi(s)$ has a **simple pole** of residue $\operatorname*{Res}_{s=\rho}\bigl(\xi'(s)/\xi(s)\bigr) = m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$ at each distinct zero $\rho$ (equivalently $\operatorname*{Res}_{s=\rho}\bigl(-\xi'(s)/\xi(s)\bigr) = -m_\rho$, so shifting the contour across $s = \rho$ extracts $+m_\rho H_K(\rho - 1/2)$, never a higher-order pole that would differentiate $\tau^{-K(s - 1/2)}$ with respect to $s$), a zero $\rho$ of multiplicity $m_\rho \ge 1$ contributes
   $$
   m_\rho\,H_0(\rho - 1/2)\,\tau^{-K(\rho - 1/2)}
   $$
   with **no polynomial $(K\log\tau)^j$ drift** even when $m_\rho \ge 2$. Therefore:
   - **Forward Direction ($\text{RH} \implies \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| \le C_\tau(0) < \infty$, any $m_\rho \ge 1$)**: If $\operatorname{Re}(\rho) = 1/2$ for every zero, then $H_0(i\gamma_\rho) = |F_\tau(1/2 + i\gamma_\rho)|^2 \ge 0$ and $|\tau^{-iK\gamma_\rho}| = 1$, so the triangle inequality gives
     $$
     \bigl|C_\tau(K)\bigr| = \biggl|\sum_{\rho\text{ distinct}} m_\rho\,\bigl|F_\tau(1/2 + i\gamma_\rho)\bigr|^2 \tau^{-iK\gamma_\rho}\biggr| \le \sum_{\rho\text{ distinct}} m_\rho\,\bigl|F_\tau(1/2 + i\gamma_\rho)\bigr|^2 = C_\tau(0) \approx 9.5048\times 10^{-4} < \infty
     $$
     for all $K \in \mathbb{R}$, without assuming $m_\rho = 1$. (In Theorem 8 of `CanonicalThetaCorrelationBound.lean`, the finite-sum triangle inequality `|∑ c_j cos(u_j)| ≤ ∑ c_j` for `c_j ≥ 0` applies directly with $c_\rho = m_\rho |F_\tau(1/2 + i\gamma_\rho)|^2 \ge 0$.)
   - **Converse Direction ($\sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \implies \text{RH}$, any $m_\rho \ge 1$)**: Established in `TASK-TC-037` (`docs/reviews/TC_GRADE_CHARACTER_PROJECTION.md` Theorem 12 & `CanonicalThetaCorrelationBound.lean` Theorem 12) via the Laplace–Carleman transform $R_+(\lambda) = \int_0^\infty C_\tau(u)e^{-\lambda u}\,du$: boundedness of $C_\tau$ makes $R_+(\lambda)$ holomorphic on $\operatorname{Re}(\lambda) > 0$, whereas any off-critical zero $\rho_0 = \frac{1}{2} + \delta_0 + i\gamma_0$ with $\delta_0 > 0$ (of any multiplicity $m_{\rho_0} \ge 1$, since the zeros of the entire function $\xi(s)$ are isolated in $\mathbb{C}$ and $m_{\rho_0} H_0(\rho_0 - 1/2) \ne 0$) creates an isolated simple pole of $R_+(\lambda)$ at $\lambda = (\delta_0 - i\gamma_0)\log\tau$ in the right half-plane $\operatorname{Re}(\lambda) > 0$.
   - **Unconditional Scalar Equivalence**:
     $$
     \boxed{\text{RH} \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| \le C_\tau(0) \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| < \infty \qquad (\text{unconditional in } m_\rho \ge 1).}
     $$

2. **Operator-Level Unitary Realization on the Jordan Socle vs. the Algebraic Direct Sum $\bigoplus_\rho E_\rho$ and Meyer's Full Cotangent Quotient $\mathcal{H}_-^0$**:
   By Meyer (`arXiv:math/0412277`, Theorem A & Section 5), if a zero $\rho$ of $\xi(s)$ has multiplicity $m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$, the generalized eigenspace $E_\rho = \ker(({}^t D_- - \rho)^{m_\rho})$ on the cotangent quotient $\mathcal{H}_-^0$ is an $m_\rho$-dimensional cyclic Jordan block with basis $\{l_{\rho,0}, l_{\rho,1}, \dots, l_{\rho,m_\rho-1}\}$ satisfying
   $$
   ({}^t D_- - \rho) l_{\rho,0} = 0 \quad (l_{\rho,0} \ne 0), \qquad ({}^t D_- - \rho) l_{\rho,k} = l_{\rho,k-1} \quad (1 \le k \le m_\rho - 1),
   $$
   and grade-shift action
   $$
   V_K l_{\rho,k} = \tau^{K(\rho - 1/2)} \sum_{j=0}^k \frac{(K\log\tau)^j}{j!}\,l_{\rho,k-j}.
   $$
   - **Socle Eigenvector Realization ($\iff \text{RH}$ alone, any $m_\rho \ge 1$)**: Because $m_\rho \ge 1$, the 1-dimensional **socle** $\ker({}^t D_- - \rho) \subset E_\rho$ always contains the non-zero genuine eigenvector $l_{\rho,0} \ne 0$, on which $V_K l_{\rho,0} = \tau^{K(\rho - 1/2)} l_{\rho,0}$ acts purely multiplicatively without polynomial Jordan nilpotent terms. Applying the star-involution and hyperbolic-pair analysis (`Theorem 51`) directly to the socle subspace $\bigoplus_\rho \operatorname{span}\{l_{\rho,0}\}$ shows that a faithful Hilbert-space realization of the socle eigenvectors with $V_K^* = V_{-K}$ exists if and only if $\operatorname{Re}(\rho) = 1/2$ for every zero (**$\text{RH}$ alone**, with no simplicity restriction).
   - **Algebraic Direct Sum $\bigoplus_\rho E_\rho$ of Generalized Eigenspaces ($\iff \text{RH} + \text{Simplicity}$, $m_\rho = 1$) vs. Meyer's Full Topological Quotient $\mathcal{H}_-^0$**: If $V_K$ acts unitarily on the generalized eigenspace $E_\rho$ ($\|V_K v\| = \|v\|$) and $\operatorname{Re}(\rho) = 1/2$ ($\tau^{K\delta} = 1$), then for $m_\rho \ge 2$ the first generalized eigenvector $l_{\rho,1}$ satisfies
     $$
     \|V_K l_{\rho,1}\|^2 = \|l_{\rho,1} + (K\log\tau) l_{\rho,0}\|^2 = \|l_{\rho,1}\|^2 + 2(K\log\tau)\operatorname{Re}\langle l_{\rho,1}, l_{\rho,0}\rangle + (K\log\tau)^2 \|l_{\rho,0}\|^2.
     $$
     In Lean 4 Theorem 51, `jordanTwoByTwoSocleStep` proves the $2 \times 2$ Jordan basis-action identities `jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 1 0 = (gradeRadialCharacter tau K delta, 0)` and `(jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 0 1).1 ≠ 0`, while the Hilbert-norm deduction $\|V_1 l_{\rho,1}\|^2 + \|V_{-1} l_{\rho,1}\|^2 - 2\|l_{\rho,1}\|^2 = 2(\log\tau)^2 \|l_{\rho,0}\|^2 = 0 \implies l_{\rho,0} = 0$ (contradicting $l_{\rho,0} \ne 0$) is proved analytically outside Lean. Consequently:
     1. On the **algebraic direct sum $\bigoplus_\rho E_\rho$** of generalized eigenspaces, a faithful Hilbert-space inner product making $V_K$ unitary exists **if and only if** $\text{RH} + \text{Simplicity}$ ($m_\rho = 1$ for all zeros) holds (since when $\operatorname{Re}(\rho) = 1/2$ and $m_\rho = 1$, declaring $\{l_{\rho,0}\}$ orthonormal gives an explicit unitary realization on $\bigoplus_\rho E_\rho$).
     2. On **Meyer's full nuclear Fréchet quotient $\mathcal{H}_-^0$**, any Hilbert-space realization into which the generalized eigenspaces $E_\rho \subset \mathcal{H}_-^0$ embed with unitary $V_K$ forces $\text{RH} + \text{Simplicity}$ ($m_\rho = 1$) as a **necessary condition**; the converse completion of the topological Fréchet quotient $\mathcal{H}_-^0$ is equivalent to Weil positivity on $\mathcal{H}_-^0$ rather than the elementary finite-block identity alone.

---

## 4. Primary-Source Audit: Meyer (`0412277`), Connes–Consani (`2006.13771`), and Connes–Consani–Moscovici (`2511.22755`) (`Section 3`)

### 4.1 Meyer (`arXiv:math/0412277`): Spectral Realization on $\mathcal{H}_-^0$ without Positivity

Meyer constructs two mutually dual nuclear Fréchet spaces $\mathcal{H}_+ \subset \mathcal{S}(\mathbb{A}_{\mathbb{Q}}/\mathbb{Q}^\times)$ and $\mathcal{H}_-$ such that:
1. The Zeta summation operator $Z : \mathcal{H}_+ \to \mathcal{H}_-$ has a 1-dimensional kernel and 1-dimensional cokernel corresponding to the poles at $s = 0$ and $s = 1$, and restricts to a topological isomorphism on $\mathcal{H}_+ \cap \mathcal{H}_-$.
2. The quotient space
   $$
   \mathcal{H}_-^0 := \mathcal{H}_- \big/ Z(\mathcal{H}_+ \cap \mathcal{H}_-)
   $$
   has discrete spectrum equal to the nontrivial zeros $\rho$ of $\xi(s)$ with algebraic multiplicity $\operatorname{mult}(\rho) = \operatorname{ord}_\xi(\rho)$, and its character trace formula reproduces the exact explicit formula:
   $$
   \operatorname{Tr}_{\mathcal{H}_-^0}(\widetilde{U}(g)) = \sum_{\xi(\rho)=0} \operatorname{ord}_\xi(\rho)\,\widehat{g}(\rho) = \widehat{g}(0) + \widehat{g}(1) - \sum_{v \le \infty} W_v(g).
   $$
3. **Why Meyer's Construction is Unconditional (`Section 5` of `0412277`)**:
   $\mathcal{H}_-^0$ is a **nuclear Fréchet space**, **not** a Hilbert space. It carries no inner product and no star-compatible adjoint $V_K^* = V_{-K}$ on the zero eigenspaces; functional-equation duality pairs $\mathcal{H}_-^0$ with its dual space $(\mathcal{H}_-^0)'$ rather than positively with itself. Upgrading $\mathcal{H}_-^0$ to a Hilbert space on which $\widetilde{U}(\tau^K)$ acts unitarily is equivalent to Weil positivity on $\mathcal{H}_-^0$.

---

### 4.2 Connes–Consani (`arXiv:2006.13771`, §2.2, Proposition 2.2 & Eq. `\eqref{sch18}`): The Exact Scaling-Trace Deficit $\delta(\rho) > 0$

In `arXiv:2006.13771` (`weil-compo.tex`, §2.2, lines 410–578), Connes and Consani compress the theta map by the orthogonal projection $S = 1 - P + \widehat{P}\widehat{Q}\widehat{P}$ onto **Sonin's space** (even functions vanishing together with their Fourier transform on $(-2^{-1/2}, 2^{-1/2})$). For a test function $g \in C_c^\infty(2^{-1/2}, 2^{1/2})$ supported on a single dyadic interval where only the archimedean place and $p = 2$ contribute:
1. The compressed operator $\Theta(g) := \sum_{\alpha \in 2^{\mathbb{Z}}} g(\alpha)\,S U(\alpha) S$ is trace-class on $L^2(\mathbb{R})^{\mathrm{ev}}$ with explicit trace
   $$
   \operatorname{Tr}\bigl(\Theta(g)\bigr) = \int_{2^{-1/2}}^{2^{1/2}} g(\rho)\,\delta(\rho)\,d^\times\rho, \qquad d^\times\rho = \frac{d\rho}{\rho}.
   $$
2. **Exact Closed-Form Formula for $\delta(\rho)$ (Proposition 2.2, Eq. `(2.18)` / `\eqref{sch18}`)**:
   For $r := \max(\rho, \rho^{-1}) \ge 1$,
   $$
   \boxed{\delta(\rho) = 2\,r^{1/2}\left(\frac{\operatorname{Si}(2\pi(r+1))}{2\pi(r+1)} + \frac{\operatorname{Si}(2\pi(r-1))}{2\pi(r-1)}\right), \qquad \operatorname{Si}(x) := \int_0^x \frac{\sin t}{t}\,dt,}
   $$
   where $\lim_{u\to 0}\frac{\operatorname{Si}(u)}{u} = 1$.
3. **Certified 256-bit Arb Properties of $\delta(\rho)$ (`Section 3.2` of JSON Artifact)**:
   - **Exact Inversion Symmetry**: $\delta(\rho^{-1}) = \delta(\rho)$ holds identically because $r(\rho^{-1}) = \max(\rho^{-1}, \rho) = r(\rho)$ (`inversion_symmetry_diff_encloses_zero == True` at every tested point);
   - **Value at $\rho = 1$**:
     $$
     \delta(1) = 2\left(\frac{\operatorname{Si}(4\pi)}{4\pi} + 1\right) = \frac{\operatorname{Si}(4\pi)}{2\pi} + 2 = 2.2374848349418275\ldots > 0;
     $$
   - **Derivative Jump at $\rho = 1$**:
     $$
     \delta'(1^+) - \delta'(1^-) = +2;
     $$
   - **Non-Comparison with $W_{\mathbb{R},2}(g) = W_\infty(g) + W_2(g)$**:
     While $W_\infty(g)$ has both a distributional singularity at $\rho = 1$ and the smooth term $(\log\pi + \gamma_E)g(1)$, and $W_2(g) = (\log 2)\,2^{-1/2}(g(2) + g(1/2))$ is supported at the boundary $\rho = 2^{\pm 1}$, $\delta(\rho)$ is a continuous $L^\infty$ density on $[2^{-1/2}, 2^{1/2}]$ bounded by $\delta(1) \approx 2.2375$. Thus $\operatorname{Tr}(\Theta(g))$ differs from the semilocal Weil functional $W_{\mathbb{R},2}(g)$ by a singular distributional boundary-plus-scaling deficit.

| $\rho$ | $r = \max(\rho, \rho^{-1})$ | Certified 256-bit Arb $\delta(\rho)$ | Certified $\delta(\rho^{-1})$ | $0 \in \delta(\rho) - \delta(\rho^{-1})$ | $\delta(\rho) > 0$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $1/2$ | $2$ | $1.1862598290708943$ | $1.1862598290708943$ | `True` | `True` |
| $2/3$ | $3/2$ | $1.1897822367576531$ | $1.1897822367576531$ | `True` | `True` |
| $3/4$ | $4/3$ | $1.2361977041561592$ | $1.2361977041561592$ | `True` | `True` |
| $1$ | $1$ | $2.2374848349418275$ | $2.2374848349418275$ | `True` | `True` |
| $4/3$ | $4/3$ | $1.2361977041561592$ | $1.2361977041561592$ | `True` | `True` |
| $3/2$ | $3/2$ | $1.1897822367576531$ | $1.1897822367576531$ | `True` | `True` |
| $2$ | $2$ | $1.1862598290708943$ | $1.1862598290708943$ | `True` | `True` |

---

### 4.3 Connes–Consani–Moscovici (`arXiv:2511.22755`): Zeta Cycles, Infrared Radical $R_{\mathrm{inf}}$, and Separated-Grade Prime Support

In `arXiv:2511.22755`:
1. **Infrared Radical $R_{\mathrm{inf}} = \bigcap_{\lambda > 1} I_\lambda$**:
   Functions $f \in \mathcal{S}(\mathbb{R})^{\mathrm{ev}}$ whose Poisson–Zeta cycle vanishes for all scaling parameters $\lambda > 1$ form the infrared radical $R_{\mathrm{inf}}$, characterized by vanishing at the origin together with their Fourier transform ($\int_{\mathbb{R}} f(x)\,dx = 0$ and $f(0) = 0$) and by Mellin vanishings at the nontrivial zeros of $\zeta(s)$.
2. **Semilocal $S$-Adelic Compression vs. Multi-Grade Prime Activation**:
   At fixed finite cutoff $\lambda$, compressing the quadratic form to functions supported on $[\lambda^{-1}, \lambda]$ restricts the explicit formula to finitely many primes $p^k \le \lambda^2$, where positive-definite inner-product completions exist and the lowest eigenvalue of the compressed quadratic form decays super-exponentially toward $0$ as $\lambda$ increases (`arXiv:2511.22755`, §§4–6).
3. **Why Concurrent $\tau$-Grades Activate All Primes $p \ge 2$**:
   In our $\tau$-graded architecture, the grade-shifted correlation $h_K(x) = ((T_K\psi_\tau)*\psi_\tau^*)(x) = h_0(\tau^K x)$ peaks around $x \sim \tau^{-K}$ and $x \sim \tau^K$. Whenever $|K| > \frac{\log 2}{2\log\tau} \approx 0.188585$, the support crosses the prime thresholds $p = 2, 3, 5, \dots$, and as $K$ ranges over $\mathbb{A}_{\mathbb{R}}$, the reflected prime-wavelet sum $W(\tau^{|K|}) = \sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n/\tau^{|K|})$ sweeps across **all** prime powers $n = p^k \sim \tau^{|K|}$.

---

## 5. Target 2 Construction: Canonical Hilbert–Schmidt Unitary Orbit Decomposition $C_\tau(K) = P_\tau(K) + E_\tau(K)$ (`Section 4`, Theorem 53)

To advance the faithful spectral realization directly on the canonical correlation $C_\tau(K) = Q_\tau(T_K\psi_\tau, \psi_\tau)$ without assuming RH or Weil positivity, we construct an unconditional positive Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}}$, a strongly continuous unitary grade representation $\mathcal{U}_K$, and a Hilbert–Schmidt rank-one operator $B_0 \in \mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}})$ whose unitary orbit matrix coefficient $P_\tau(K) := \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}}$ captures the positive archimedean-plus-pole-transfer core of $C_\tau(K)$, while isolating the exact arithmetic remainder $E_\tau(K)$ in terms of the restored `TC-049`/`TC-049R` resonant divisor band.

### 5.1 The Unconditional Positive Hilbert Space $\mathcal{H}_\tau^{\mathrm{pos}}$, One-Sided Shift-Difference Operator $A_\tau^B$, and Unitary Grade Orbit

1. **Positive Hilbert Space and One-Sided Shift-Difference Operator (`TC-042F`/`TC-043` Attempt B)**:
   Define unconditionally (with zero dependence on RH or the zeros of $\zeta$):
   $$
   \mathcal{H}_\tau^{\mathrm{pos}} := \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y),
   \qquad
   \mathcal{H}_\tau^B := L^2\!\left([1, \infty)\times \mathbb{R}_{>0},\; \frac{x^{-3/2}}{x - x^{-1}}\,\frac{dx}{x}\,\frac{dy}{y}\right),
   $$
   equipped with the **one-sided shift-difference operator** from `TC-042F` (Section 6) and `TC-043` (Section 5.1):
   $$
   \boxed{(A_\tau^B f)(x, y) := \bigl((I - S_x^{-1})f\bigr)(y) = f(y) - f(y/x), \qquad (S_x f)(y) := f(xy),}
   $$
   together with the causal $s = 0$ Euler resolvent (`TC-043` Section 6.2 & `TC-043R` Section 12.2, with $D = y\frac{d}{dy}$ and $f \in \mathcal{S}_\tau$):
   $$
   \boxed{(R_0 f)(y) := \int_0^y \left(\frac{t}{y}\right)^{1/2} (D f)(t)\,\frac{dt}{t} = f(y) - \frac{1}{2}\int_0^y \left(\frac{t}{y}\right)^{1/2} f(t)\,\frac{dt}{t} = \bigl((I - \tfrac{1}{2}K_0)f\bigr)(y),}
   $$
   where $(K_0 f)(y) := y^{-1/2}\int_0^y f(t)t^{1/2}\,\frac{dt}{t}$ is the derivative-free causal operator with Mellin multiplier $\frac{1}{1/2 + it}$, so $R_0 = K_0 D = I - \frac{1}{2}K_0$ has Mellin multiplier $\frac{it}{1/2 + it}$ and Plancherel symbol $|\widehat{R_0 f}(it)|^2 = \frac{t^2}{t^2 + 1/4}|\widehat{f}(it)|^2 = \bigl(1 - \frac{1/4}{t^2 + 1/4}\bigr)|\widehat{f}(it)|^2$.
   > **Reconciliation Note (`TC-050R` & `TC-050R2`):**
   > 1. *One-Sided Shift-Difference Operator $A_\tau^B$*: In `TC-042F`/`TC-043`, the Attempt B shift-difference identity uses the **one-sided** difference $(I - S_x^{-1})f(y) = f(y) - f(y/x)$:
   >    $$
   >    \int_0^\infty (A_\tau^B T_K\psi_\tau)(x, y)\,\overline{(A_\tau^B\psi_\tau)(x, y)}\,\frac{dy}{y}
   >    = 2\,h_0(\tau^{|K|}) - h_0(\tau^{|K|} x) - h_0(\tau^{|K|} x^{-1})
   >    = 2\,h_0(e^\kappa) - h_0(e^{\kappa + u}) - h_0(e^{\kappa - u}) \qquad (x = e^u, \; \kappa = |K|\log\tau).
   >    $$
   >    By contrast, a two-sided difference $f(xy) - f(y/x)$ would shift the relative argument by $x^2 = e^{2u}$ and evaluate to $2h_0(e^\kappa) - h_0(e^{\kappa+2u}) - h_0(e^{\kappa-2u})$ unless $x$ is replaced by $x^{1/2}$ via the unitary change of variables $y \mapsto x^{-1/2} y$ (which maps $f(y) - f(y/x) \mapsto f(x^{1/2} y) - f(x^{-1/2} y)$ without changing the $L^2(\mathbb{R}_{>0}, dy/y)$ inner product). We adopt the canonical one-sided operator $(A_\tau^B f)(x, y) = f(y) - f(y/x)$ throughout code, certificates, Lean comments, and prose.
   > 2. *Euler Derivative $D = y\frac{d}{dy}$ in $R_0$ vs. Derivative-Free $K_0$, and the Exact $e^{-u/2}$ Weight in $J(\kappa)$*: By integration by parts on $(0, y]$ (using $\lim_{t\to 0^+} t^{1/2}f(t) = 0$ for $f \in \mathcal{S}_\tau$), $\int_0^y (t/y)^{1/2}(Df)(t)\frac{dt}{t} = f(y) - \frac{1}{2}\int_0^y (t/y)^{1/2}f(t)\frac{dt}{t}$ (certified in 256-bit Arb at $y \in \{1/2, 1, 2\}$ in `verify_euler_resolvent_R0_spatial_and_mellin_identity_arb`, with spatial difference enclosing $0$). By Mellin–Plancherel and $\frac{1}{\tau}\int_{-\infty}^\infty \frac{e^{it v}}{t^2 + 1/4}\,dt = e^{-|v|/2}$, the pole-integral term is
   >    $$
   >    \boxed{J(\kappa) := \langle K_0 T_K\psi_\tau, K_0\psi_\tau\rangle_{L^2(d^\times y)} = \frac{1}{\tau}\int_{-\infty}^\infty \frac{H_0(it)}{t^2 + 1/4}\,e^{i\kappa t}\,dt = \int_0^\infty e^{-u/2}\bigl(h_0(e^{\kappa+u}) + h_0(e^{\kappa-u})\bigr)\,du,}
   >    $$
   >    carrying the exponential weight $e^{-u/2}\,du$ (whereas the hyperbolic weight $\frac{e^{-3u/2}}{2\sinh u}\,du = \frac{x^{-3/2}}{x - x^{-1}}\frac{dx}{x}$ belongs to $P_\tau^B(K)$). Omitting $D$ (replacing $R_0$ by $K_0$) would yield $4\langle K_0 T_K\psi_\tau, K_0\psi_\tau\rangle_{L^2} = 4J(\kappa)$ ($4J(0) = 0.1038390451376241\ldots$ at $K = 0$) instead of $4\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2} = 4h_0(e^\kappa) - J(\kappa)$ ($4h_0(1) - J(0) \approx 1.96349017$ at $K = 0$), which would fail to cancel $-J(\kappa)$ in $P_\tau^B(K) + 4\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2}$.

2. **Positive Embedding and Unitary Grade Representation**:
   Define the grade-covariant linear map $\mathcal{J}_\tau : \mathcal{S}_\tau \to \mathcal{H}_\tau^{\mathrm{pos}}$ and unitary group $\mathcal{U}_K$ ($K \in \mathbb{R}$) by
   $$
   \mathcal{J}_\tau(f) := \bigl(A_\tau^B f,\; 2\,R_0 f\bigr) \in \mathcal{H}_\tau^{\mathrm{pos}},
   \qquad
   \mathcal{U}_K(\Phi, g)(x, y) := \bigl(\Phi(x, \tau^{-K} y),\; g(\tau^{-K} y)\bigr) = \bigl((U_K^B \Phi)(x, y),\; (T_K g)(y)\bigr).
   $$
   Because multiplicative dilation in $y$ commutes with $y \mapsto y/x$ and with $R_0$, $\mathcal{J}_\tau$ intertwines $T_K$ with $\mathcal{U}_K$:
   $$
   \mathcal{J}_\tau(T_K f) = \mathcal{U}_K\,\mathcal{J}_\tau(f), \qquad \|\mathcal{U}_K \Psi\|_{\mathcal{H}_\tau^{\mathrm{pos}}} = \|\Psi\|_{\mathcal{H}_\tau^{\mathrm{pos}}} \qquad (\forall K \in \mathbb{R}).
   $$

3. **Hilbert–Schmidt Rank-One Operator $B_0$, Matrix Coefficient $P_\tau(K)$, and Exact $J(\kappa)$ Cancellation**:
   Set $\Psi_0^{\mathrm{pos}} := \mathcal{J}_\tau(\psi_\tau) = (A_\tau^B\psi_\tau, 2 R_0\psi_\tau) \in \mathcal{H}_\tau^{\mathrm{pos}}$, fix a unit vector $e_0 \in \mathcal{H}_\tau^{\mathrm{pos}}$ ($\|e_0\|_{\mathcal{H}_\tau^{\mathrm{pos}}} = 1$), and define the rank-one Hilbert–Schmidt operator
   $$
   B_0 := |\Psi_0^{\mathrm{pos}}\rangle\langle e_0| \in \mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}}), \qquad B_K := \mathcal{U}_K B_0 = |\mathcal{U}_K\Psi_0^{\mathrm{pos}}\rangle\langle e_0|.
   $$
   With $\kappa = |K|\log\tau$, $X_K = e^\kappa = \tau^{|K|} \ge 1$, and $J(\kappa) := \int_0^\infty e^{-u/2}(h_0(e^{\kappa+u}) + h_0(e^{\kappa-u}))\,du$, the two component inner products evaluate (`TC-042F` Section 6 and `TC-043R` Section 12.2) to:
   $$
   \begin{aligned}
   P_\tau^B(K) &:= \langle A_\tau^B T_K\psi_\tau, A_\tau^B\psi_\tau\rangle_{\mathcal{H}_\tau^B}
   = \int_0^\infty \frac{e^{-3u/2}}{2\sinh u}\bigl(2\,h_0(e^\kappa) - h_0(e^{\kappa+u}) - h_0(e^{\kappa-u})\bigr)\,du \\
   &= W_{\mathrm{arch}}(h_K) + c_\tau^B\,h_0(X_K) - \bigl(2\,h_0(X_K) - J(\kappa)\bigr), \\
   4\,\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2(d^\times y)}
   &= B_{\mathrm{transfer}}(T_K\psi_\tau, \psi_\tau) + 2\,h_0(X_K)
   = 4\,h_0(X_K) - J(\kappa).
   \end{aligned}
   $$
   Adding the two components cancels the pole-integral term $J(\kappa)$ identically (`(W_arch + c_tau_B * h0_XK - (2 * h0_XK - J_K)) + (4 * h0_XK - J_K) = W_arch + (c_tau_B + 2) * h0_XK` in Lean 4 Theorem 53):
   $$
   \boxed{P_\tau(K) := \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}} = \operatorname{Tr}(B_0^* \mathcal{U}_K B_0) = P_\tau^B(K) + 4\,\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2(d^\times y)} = W_{\mathrm{arch}}(h_K) + \bigl(c_\tau^B + 2\bigr)\,h_0(\tau^{|K|}).}
   $$
   At $K = 0$, evaluating $P_{\mathrm{sym}}(W_\alpha) = -648 W_\alpha^3 + 58380 W_\alpha^2 - 706860 W_\alpha + 2027025 = 92193 - 270924(W_\alpha - 4) + 50604(W_\alpha - 4)^2 - 648(W_\alpha - 4)^3$ at $W_1 = (1 + 1)^2 = 4$ gives the exact closed form
   $$
   \boxed{h_0(1) = \|\psi_\tau\|_{L^2(d^\times y)}^2 = \frac{92193}{512 \cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} = 0.4973624838099012444846118\ldots, \qquad J(0) = 0.0259597612844060246055966\ldots,}
   $$
   and hence:
   $$
   \begin{aligned}
   \|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 &= P_\tau^B(0) = 0.5947678334606322481483108\ldots, \\
   4\,\|R_0\psi_\tau\|_{L^2(d^\times y)}^2 &= 4\,h_0(1) - J(0) = 1.963490173955198951575709\ldots, \\
   \|B_0\|_{\mathrm{HS}}^2 &= P_\tau(0) = P_\tau^B(0) + 4\,\|R_0\psi_\tau\|_{L^2(d^\times y)}^2 = 2.558258007415831199724020\ldots
   \end{aligned}
   $$
   By Cauchy–Schwarz in $\mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}})$ (and Bochner's theorem for the unitary representation $K \mapsto \mathcal{U}_K$), both $P_\tau^B(K)$ and $P_\tau(K)$ are unconditionally positive-definite functions of $K \in \mathbb{R}$ satisfying:
   $$
   \boxed{\bigl|P_\tau^B(K)\bigr| \le P_\tau^B(0) \approx 0.59476783, \qquad \bigl|P_\tau(K)\bigr| \le \|B_0\|_{\mathrm{HS}}^2 = P_\tau(0) \approx 2.55825801 \qquad (\forall K \in \mathbb{R}),}
   $$
   with $P_\tau(K) = O(|K|\,\tau^{-|K|/2})$ as $|K| \to \infty$.

---

### 5.2 Restored `TC-049`/`TC-049R` Head–Band–Tail Decomposition and Controlled Remainder Bounds (`Section 4.2`, Theorem 53)

1. **Restored `TC-049`/`TC-049R` Divisor Cutoffs vs. Prime Cutoffs**:
   For $X = X_K = \tau^{|K|} \ge 1$, we use the exact `TC-049`/`TC-049R` head–band–tail decomposition of the Möbius remainder $R_\mu(X) = W(X) - W_{\log}(X) = \sum_{m \ge 2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$:
   $$
   \boxed{H(X) := \bigl\lfloor X^{5/6}\bigr\rfloor, \qquad M(X) := \bigl\lceil\max(2, X^{5/4})\bigr\rceil,}
   $$
   $$
   \begin{aligned}
   R_{\mu,\mathrm{head}}(X) &:= \sum_{2 \le m \le H(X)} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right) \qquad \bigl(= 0 \text{ when } H(X) < 2, \text{ i.e. } 1 \le X < 2^{6/5} \approx 2.297397\bigr), \\
   R_{\mu,\mathrm{band}}(X) &:= \sum_{H(X) < m \le M(X)} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right), \\
   R_{\mu,\mathrm{tail}}(X) &:= \sum_{m > M(X)} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right).
   \end{aligned}
   $$
   - **Clamped Exact Cutoff Characterization vs. Safe Interval Upper Helper (`TC-050R2` Section 4)**:
     - The head cutoff $H(X) = \lfloor X^{5/6}\rfloor$ (`certified_head_cutoff_H_X_arb` in [`tc/faithful_tau_arithmetic_spectral_realization.py`](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)) is characterized for $X \ge 1$ by the exact integer-power enclosure
       $$
       \boxed{H \in \mathbb{Z}_{\ge 1}, \qquad H^6 \le X^5 < (H + 1)^6,}
       $$
       and raises a `ValueError` if an input Arb ball straddles an integer boundary of $X^{5/6}$.
     - Because $M(X) := \lceil\max(2, X^{5/4})\rceil$ is clamped below at $2$ on $1 \le X \le 2^{4/5} \approx 1.741101$, the unclamped inequality $(M - 1)^4 < X^5 \le M^4$ fails at $X = 1, M = 2$ (where $(M-1)^4 = 1^4 = 1$ is not strictly less than $X^5 = 1$). The exact mathematical characterization of $M(X) = \lceil\max(2, X^{5/4})\rceil$ for all $X \ge 1$ is the **clamped characterization** (`certify_clamped_exact_cutoff_M_X_arb` in [`tc/faithful_tau_arithmetic_spectral_realization.py`](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)):
       $$
       \boxed{M \in \mathbb{Z}_{\ge 2}, \qquad X^5 \le M^4, \qquad \bigl(M = 2 \;\lor\; (M - 1)^4 < X^5\bigr).}
       $$
     - We also distinguish the exact mathematical cutoff $M(X)$ from the interval helper `certified_coupled_cutoff_M_X_arb(X)` in [`tc/prime_euler_moebius_recovery.py`](file:///c:/Development/Projects/reimann_scope/tc/prime_euler_moebius_recovery.py), which computes `max(2, int(((X**5).root(4)).upper().ceil().unique_fmpz()))`. On any wide Arb ball that straddles an exact integer boundary of $X^{5/4}$ from above (such as the regression ball $X = 16 \pm 10^{-30}$, where $16^{5/4} = 32$), `certified_coupled_cutoff_M_X_arb` returns the **certified safe upper cutoff** $M_{\mathrm{safe}} = 33 \ge M(x)$ valid for the tail inequality $\frac{C_{\log,0}x^{5/2}}{2 M_{\mathrm{safe}}^2} \le \frac{1}{2}C_{\log,0}$ across all $x \in X$, whereas `certify_clamped_exact_cutoff_M_X_arb` verifies that for all 13 sample grades $K \in \{0, \pm 1/4, \pm 1/2, \pm 1, \pm\sqrt{2}, \pm 3/2, \pm 2\}$, the 256-bit Arb ball $X_K = \tau^{|K|}$ does not straddle any boundary of $X^{5/4}$, so $M_{\mathrm{safe}}(X_K) = M_{\mathrm{exact}}(X_K)$ satisfies the clamped characterization exactly (`all_13_sample_grades_clamped_exact_M_X_certified: true`).
   - **Divisor Cutoffs vs. Prime Cutoffs**: $H(X)$ and $M(X)$ are **divisor cutoffs** on the integer summation index $m$ in $R_\mu(X)$. By contrast, the cutoff $y$ in the prime-sieved approximant $W_y(X) = \sum_{m \mid P_y}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ ($P_y = \prod_{p \le y} p = e^{\vartheta(y)}$) is a **prime factor cutoff** restricting to $y$-smooth squarefree divisors $m \mid P_y$. When $y \ge M(X)$, every squarefree integer $2 \le m \le M(X)$ divides $P_y$, so all head and band terms $2 \le m \le M(X)$ cancel identically in $W(X) - W_y(X)$.

2. **Exact Orbit Decomposition Identity**:
   Combining $W_{\mathrm{arch}}(h_K) = P_\tau(K) - (c_\tau^B + 2)h_0(X_K)$ with $C_\tau(K) = W_{\mathrm{arch}}(h_K) - W(X_K) - W(X_K^{-1})$ and $W(X_K) = W_{\log}(X_K) + R_{\mu,\mathrm{head}}(X_K) + R_{\mu,\mathrm{band}}(X_K) + R_{\mu,\mathrm{tail}}(X_K)$ yields for every $K \in \mathbb{A}_{\mathbb{R}}$:
   $$
   \boxed{C_\tau(K) = P_\tau(K) + E_\tau(K), \qquad E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(X_K),}
   $$
   where the 5-component controlled remainder (`controlledCorrelationRemainder` in Lean 4) is:
   $$
   \boxed{E_{\tau,\mathrm{controlled}}(K) := -\bigl(c_\tau^B + 2\bigr)\,h_0(X_K) - W(X_K^{-1}) - W_{\log}(X_K) - R_{\mu,\mathrm{head}}(X_K) - R_{\mu,\mathrm{tail}}(X_K).}
   $$

3. **Complete Provenance Table for the Five Controlled Remainder Components ($X_K = \tau^{|K|} \ge 1$)**:

| Component | Exact Expression & Domain ($X_K = \tau^{|K|} \ge 1$) | Inequality Used & Large-Grade Asymptotics | Provenance | Certified 256-bit Arb Global Bound (Outward `.upper()`) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Pole + Transfer Term** | $-(c_\tau^B + 2)h_0(X_K) = -c_\tau^A h_0(X_K)$ on $X_K \ge 1$ ($c_\tau^A = c_\tau^B + 2 \approx 5.37218342$) | **Unitary Dilation Cauchy–Schwarz** on $L^2(\mathbb{R}_{>0}, d^\times y)$: since $h_0(X_K) = \langle T_{|K|}\psi_\tau, \psi_\tau\rangle_{L^2(d^\times y)}$ and $\|T_{|K|}\psi_\tau\|_{L^2} = \|\psi_\tau\|_{L^2}$, $\|h_0(X_K)\| \le \|\psi_\tau\|_{L^2(d^\times y)}^2 = h_0(1) = \frac{92193}{512\cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.4973624838$ (**note:** $h_0$ is oscillatory and changes sign on $[1, \infty)$, e.g. $h_0(2) \approx -0.2174306224 < 0$; the bound uses Cauchy–Schwarz—and independently the symmetric Bernstein envelope $\|h_0(X_K)\| \le \frac{92193}{32768}(X_K + X_K^{-1})^{-5/2} \le h_0(1)$—never positivity or monotonicity of $h_0$), giving $B_{h_0} := c_\tau^A h_0(1)$; for large $X_K$, $h_0(X_K) \sim -\frac{648}{512}X_K^{6 - 17/2} = -\frac{81}{64}X_K^{-5/2} = O(X_K^{-5/2})$ ($\le \frac{92193}{32768}c_\tau^A X_K^{-5/2} \approx 15.114677\,X_K^{-5/2}$) | Unitary dilation Cauchy–Schwarz on $L^2(\mathbb{R}_{>0}, d^\times y)$ + `TASK-TC-042`/`044` symmetric Bernstein envelope + `TASK-TC-042F`/`043` | $B_{h_0} = [2.671922488868445 \pm 1.77\times 10^{-40}] < 2.671923$ |
| **2. Reflected Small-Scale Prime Sum** | $-W(X_K^{-1}) = -\sum_{n \ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n X_K)$ on $X_K \ge 1$ | $\|W(X_K^{-1})\| \le \frac{92193}{32768}\bigl(\sum_{n=2}^\infty \frac{\Lambda(n)}{n^3}\bigr) X_K^{-5/2} \le B_{\mathrm{refl}}\,X_K^{-5/2} = O(X_K^{-5/2})$ (evaluated via prime powers $n \le 25000$ plus Rosser–Schoenfeld tail $\frac{1.558245}{25000^2}$) | `TASK-TC-043` / `TASK-TC-044` cubic prime-power majorant | $B_{\mathrm{refl}} = [0.46372978 \pm 7.98\times 10^{-9}] < 0.463730$ |
| **3. Divisor-Aggregated $W_{\log}(X_K)$** | $-W_{\log}(X_K) = -\sum_{m \ge 1}\frac{\log m}{\sqrt{m}}h_0(m/X_K)$ on $X_K \ge 1$ | Global TV bound $\|W_{\log}(X_K)\| \le B_{\log} := \frac{30731}{98304} + M_{\tilde{h},0}^{(-3/2)} + \frac{1}{2}M_{\tilde{h},\log}^{(-3/2)}$ on $[1, \infty)$; 4th-order Euler–Maclaurin bound $\|W_{\log}(X_K)\| \le C_{\log,\mathrm{EM}}\,X_K^{-5/2} = O(X_K^{-5/2})$ ($C_{\log,\mathrm{EM}} = [13.46851 \pm 4.74\times 10^{-6}] < 13.468515$) | `TASK-TC-044` (7-root IBP global bound) + `TASK-TC-049R` (Euler–Maclaurin bound) | $B_{\log} = [3.349008018760691 \pm 5.40\times 10^{-27}] < 3.349009$ |
| **4. Head Divisor Sum $R_{\mu,\mathrm{head}}(X_K)$** | $-\sum_{2 \le m \le H(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$, $H(X_K) = \lfloor X_K^{5/6}\rfloor$ ($= 0$ for $1 \le X_K < 2^{6/5}$) | $\|R_{\mu,\mathrm{head}}(X_K)\| \le C_{\log,\mathrm{EM}} X_K^{-5/2}\sum_{2 \le m \le H(X_K)} m^2 \le C_{\log,\mathrm{EM}} X_K^{-5/2}\frac{5}{6}H(X_K)^3 \le \frac{5}{6}C_{\log,\mathrm{EM}} =: B_{\mathrm{head}}$ (**proved uniform $O(1)$ bound**, not $o(1)$ without cancellation) | `TASK-TC-049` / `TASK-TC-049R` resonant-band head reduction | $B_{\mathrm{head}} = [11.22376 \pm 5.61\times 10^{-6}] < 11.223763$ |
| **5. Super-Scale Tail $R_{\mu,\mathrm{tail}}(X_K)$** | $-\sum_{m > M(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$, $M(X_K) = \lceil\max(2, X_K^{5/4})\rceil$ | $\|R_{\mu,\mathrm{tail}}(X_K)\| \le C_{\log,0} X_K^{5/2}\sum_{m > M(X_K)} m^{-3} \le \frac{C_{\log,0} X_K^{5/2}}{2 M(X_K)^2} \le \frac{1}{2}C_{\log,0} =: B_{\mathrm{tail}}$ (**proved uniform $O(1)$ bound**, since $M(X_K) \ge X_K^{5/4} \implies X_K^{5/2}/M(X_K)^2 \le 1$; $C_{\log,0} = \frac{92193}{32768}(-\zeta'(3)) \approx 0.55742959$) | `TASK-TC-045` ($C_{\log,0}$ origin bound) + `TASK-TC-049`/`049R` | $B_{\mathrm{tail}} = [0.2787147935540088 \pm 3.72\times 10^{-41}] < 0.278715$ |

4. **Why Cutoff Precision Matters for Head and Tail Bounds (`TC-050R` Audit)**:
   - **Why $\lfloor X/2\rfloor$ Cannot Use the Unsigned $u^{-5/2}$ Majorant**: Applying $|W_{\log}(X/m)| \le C(X/m)^{-5/2}$ over $2 \le m \le \lfloor X/2\rfloor$ yields the unsigned majorant $C X^{-5/2}\sum_{2 \le m \le X/2} m^2 = O(X^{1/2})$, which grows like $\sqrt{X}$ rather than decaying (though failure of this unsigned triangle-inequality majorant does not prove the signed Möbius sum $\sum_{2 \le m \le X/2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ is unbounded). At $H(X) = \lfloor X^{5/6}\rfloor$, $\sum_{2 \le m \le H(X)} m^2 \le \frac{5}{6}H(X)^3 \le \frac{5}{6}X^{5/2}$ balances $X^{-5/2}$ to give the proved uniform $O(1)$ bound $B_{\mathrm{head}} = \frac{5}{6}C_{\log,\mathrm{EM}} < 11.223763$.
   - **Why $M(X) = \lceil\max(2, X^{5/4})\rceil$ Gives $O(1)$ Tail Control**: Since $M(X) \asymp X^{5/4}$, the ratio $X^{5/2}/M(X)^2$ approaches $1$ from below as $X \to \infty$, giving the proved uniform $O(1)$ bound $|R_{\mu,\mathrm{tail}}(X)| \le \frac{1}{2}C_{\log,0} < 0.278715$ (whereas $o(1)$ tail decay would require choosing a super-scale cutoff growing strictly faster than $X^{5/4}$).
   - **Global Bound and Large-Grade Limsup Bound for $E_{\tau,\mathrm{controlled}}(K)$**:
     Summing the five live 256-bit Arb bounds gives the unconditional global bound and large-grade limsup bound over all $K \in \mathbb{A}_{\mathbb{R}}$:
     $$
     \boxed{\sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|E_{\tau,\mathrm{controlled}}(K)\bigr| \le B_{\mathrm{ctrl}} := B_{h_0} + B_{\mathrm{refl}} + B_{\log} + B_{\mathrm{head}} + B_{\mathrm{tail}} = [17.98713 \pm 7.37\times 10^{-6}] < 17.987140,}
     $$
     $$
     \boxed{\limsup_{|K| \to \infty} \bigl|E_{\tau,\mathrm{controlled}}(K)\bigr| \le B_{\mathrm{head}} + B_{\mathrm{tail}} = \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [11.50247 \pm 7.07\times 10^{-6}] < 11.502478.}
     $$
   - **Two-Way Boundedness Equivalence Across $K \in \mathbb{A}_{\mathbb{R}}$ and $X \ge 1$ (`Theorem 53` in Lean 4 + `TC-045` Continuity)**:
     Because $|P_\tau(K)| \le P_\tau(0) \approx 2.558258$ and $|E_{\tau,\mathrm{controlled}}(K)| \le B_{\mathrm{ctrl}} < 17.987140$ hold unconditionally for all $K \in \mathbb{A}_{\mathbb{R}}$, Theorem 53 gives the pointwise equivalence $\sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|E_\tau(K)| < \infty \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|R_{\mu,\mathrm{band}}(\tau^{|K|})| < \infty$. Furthermore, although $R_{\mu,\mathrm{band}}(X)$ is only piecewise continuous with jumps at divisor cutoff steps of $H(X) = \lfloor X^{5/6}\rfloor$ and $M(X) = \lceil\max(2, X^{5/4})\rceil$, the full Möbius remainder $R_\mu(X)$ is **continuous** on $(0, \infty)$ (`TC-045`), $\{\tau^{|K|} : K \in \mathbb{A}_{\mathbb{R}}\}$ is dense in $[1, \infty)$, and $|R_\mu(X) - R_{\mu,\mathrm{band}}(X)| = |R_{\mu,\mathrm{head}}(X) + R_{\mu,\mathrm{tail}}(X)| \le B_{\mathrm{head}} + B_{\mathrm{tail}} < 11.502478$ holds uniformly for **every** real $X \ge 1$. Therefore:
     $$
     \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|R_{\mu,\mathrm{band}}(\tau^{|K|})\bigr| < \infty
     \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|R_\mu(\tau^{|K|})\bigr| < \infty
     \overset{\text{continuity of }R_\mu}{\Longleftrightarrow} \sup_{X \ge 1} \bigl|R_\mu(X)\bigr| < \infty
     \iff \sup_{X \ge 1} \bigl|R_{\mu,\mathrm{band}}(X)\bigr| < \infty,
     $$
     yielding the complete two-sided equivalence:
     $$
     \boxed{\sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| < \infty \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|E_\tau(K)\bigr| < \infty \iff \sup_{X \ge 1} \bigl|R_{\mu,\mathrm{band}}(X)\bigr| < \infty \qquad (\text{SUBGATE-TC-043A}).}
     $$

---

### 5.3 Certified 256-bit Arb Verification Across 13 Positive & Negative Rational and Irrational Algebraic Grades

In [tc/faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py) and [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json):
1. **Outward-Rounded Ball Inequality Certification (`certify_abs_le_bound_arb`)**:
   Every inequality $|v| \le B$ is certified using outward-rounded Arb endpoints via `(B - abs(v)).lower() >= arb(0)` (equivalently `abs(v).upper() <= B.lower()`, mode `OUTWARD_UPPER_LE_LOWER`), never the weak overlap test `abs(v).lower() <= B.upper()`. At $K = 0$, where $|P_\tau(0)| \le P_\tau(0)$, $|P_\tau^B(0)| \le P_\tau^B(0)$, and $|(c_\tau^B+2)h_0(1)| \le B_{h_0}$ compare a positive ball against itself, `certify_abs_le_bound_arb(..., exact_self_equality=True)` verifies exact midpoint/radius identity on a strictly positive ball (`EXACT_ALGEBRAIC_SELF_EQUALITY_POSITIVE_BALL`) with exact zero margin `arb(0)`.
2. **Direct Finite-Sum Band Evaluation & Independent Tail Enclosure Check**:
   At every sample grade $K$, both $R_{\mu,\mathrm{head}}(X_K) = \sum_{2 \le m \le H(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$ and $R_{\mu,\mathrm{band}}(X_K) = \sum_{H(X_K) < m \le M(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$ are computed **directly** as explicit finite sums. Their sum is compared against the independently evaluated total Möbius remainder $R_\mu(X_K) = W(X_K) - W_{\log}(X_K)$, and the resulting difference $R_\mu(X_K) - (R_{\mu,\mathrm{head}}(X_K) + R_{\mu,\mathrm{band}}(X_K))$ is certified to satisfy the analytic tail bound $\frac{C_{\log,0}X_K^{5/2}}{2 M(X_K)^2} \le \frac{1}{2}C_{\log,0}$ via `OUTWARD_UPPER_LE_LOWER` (`all_independent_tail_bounds_verified: true`).
3. **Explicit Distinction of Algebraic Consistency Checks**:
   The identity check $0 \in C_\tau(K) - (P_\tau(K) + E_\tau(K))$ is explicitly labeled `"reconstruction_verification_type": "ALGEBRAIC_CONSISTENCY_CHECK"` in the JSON artifact.
4. **Per-Observable Certified 256-bit Arb Radius Summary Across the 13 Sample Grades (`observable_radius_summary_across_13_sample_grades`)**:
   Each observable's ball radius reflects its analytical truncation and quadrature budget:
   - $W_{\log}(X_K)$, $R_{\mu,\mathrm{head}}(X_K)$, and $R_{\mu,\mathrm{band}}(X_K)$ (evaluated by 4th-order Euler–Maclaurin on $[N_0, \infty)$): maximum Arb radii $\le 6.58 \times 10^{-11}$, $\le 5.64 \times 10^{-11}$, and $\le 5.64 \times 10^{-11}$ across all 13 sample grades;
   - $P_\tau(K)$ (`P_tau_K_HS_orbit_certified`), $-(c_\tau^B+2)h_0(X_K)$, and $W(X_K^{-1})$: maximum Arb radii $\le 3.22 \times 10^{-22}$, $\le 6.34 \times 10^{-75}$, and $\le 7.01 \times 10^{-9}$;
   - $C_\tau(K)$ and $E_\tau(K)$ (which include the prime-power Rosser–Schoenfeld tail on $n > 16500$ in $W(X_K)$): radii range from $1.40 \times 10^{-8}$ at $K = 0$ up to $6.87 \times 10^{-5}$ at $|K| = 2$;
   - $R_{\mu,\mathrm{tail}}(X_K)$ and $E_{\tau,\mathrm{controlled}}(K)$ (which include the direct super-scale tail remainder $\frac{C_{\log,0}X_K^{5/2}}{2\,m_{\mathrm{tail,cut}}^2}$ at $m_{\mathrm{tail,cut}} = \max(800, 25 M(X_K))$): radii range from $1.89 \times 10^{-5}$ at $K = 0$ up to $5.42 \times 10^{-4}$ at $|K| = 2$.

| Grade $K \in \mathbb{A}_{\mathbb{R}}$ | Scale $X_K = \tau^{|K|}$ | Cutoffs $(H, M)$ | Positive Orbit $P_\tau(K)$ | Head $R_{\mu,\mathrm{head}}(X_K)$ | Direct Band $R_{\mu,\mathrm{band}}(X_K)$ | Controlled $E_{\tau,\mathrm{controlled}}(K)$ | Total Remainder $E_\tau(K)$ | Complete $C_\tau(K)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $-2$ | $39.47841760$ | $(21, 99)$ | $-0.00048360$ | $-0.00713548$ | $+0.00948700$ | $+0.00986039$ | $+0.00036032$ | $-0.00012328$ |
| $-3/2$ | $15.74960995$ | $(9, 32)$ | $-0.00443212$ | $-0.00986704$ | $+0.00338923$ | $+0.00809947$ | $+0.00471475$ | $+0.00028264$ |
| $-\sqrt{2}$ | $13.45230778$ | $(8, 26)$ | $-0.00583251$ | $-0.00332901$ | $+0.00663963$ | $+0.01302093$ | $+0.00637597$ | $+0.00054346$ |
| $-1$ | $6.28318531$ | $(4, 10)$ | $+0.02470927$ | $-0.03274068$ | $+0.03051375$ | $+0.00644530$ | $-0.02407864$ | $+0.00063063$ |
| $-1/2$ | $2.50662827$ | $(2, 4)$ | $-0.11743968$ | $+0.06497356$ | $-0.00641067$ | $+0.11190364$ | $+0.11830653$ | $+0.00086685$ |
| $-1/4$ | $1.58323349$ | $(1, 2)$ | $-1.36831275$ | $0.00000000$ | $-0.01542474$ | $+1.35383130$ | $+1.36924136$ | $+0.00092861$ |
| $0$ | $1.00000000$ | $(1, 2)$ | $+2.55825801$ | $0.00000000$ | $-0.01388540$ | $-2.57118828$ | $-2.55730753$ | $+0.00095048$ |
| $+1/4$ | $1.58323349$ | $(1, 2)$ | $-1.36831275$ | $0.00000000$ | $-0.01542474$ | $+1.35383130$ | $+1.36924136$ | $+0.00092861$ |
| $+1/2$ | $2.50662827$ | $(2, 4)$ | $-0.11743968$ | $+0.06497356$ | $-0.00641067$ | $+0.11190364$ | $+0.11830653$ | $+0.00086685$ |
| $+1$ | $6.28318531$ | $(4, 10)$ | $+0.02470927$ | $-0.03274068$ | $+0.03051375$ | $+0.00644530$ | $-0.02407864$ | $+0.00063063$ |
| $+\sqrt{2}$ | $13.45230778$ | $(8, 26)$ | $-0.00583251$ | $-0.00332901$ | $+0.00663963$ | $+0.01302093$ | $+0.00637597$ | $+0.00054346$ |
| $+3/2$ | $15.74960995$ | $(9, 32)$ | $-0.00443212$ | $-0.00986704$ | $+0.00338923$ | $+0.00809947$ | $+0.00471475$ | $+0.00028264$ |
| $+2$ | $39.47841760$ | $(21, 99)$ | $-0.00048360$ | $-0.00713548$ | $+0.00948700$ | $+0.00986039$ | $+0.00036032$ | $-0.00012328$ |

---

## 6. Lean 4 Formalization vs. External Analytic Proofs (`Section 5`)

We maintain a strict separation between what is deductively verified in Lean 4 (`0` `sorry`, `0` `admit`, `0` custom axioms) and what is established by external analytic derivations and 256-bit Arb ball enclosures:

1. **Verified Deductively in Lean 4 ([formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean), Theorems 51–56, synchronized word-for-word in `TASK-TC-050R2`, `TASK-TC-051`, and `TASK-TC-051R`)**:
   - [`tau_grade_star_involution_and_hyperbolic_pair_obstruction`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1719-L1817) (**Theorem 51**, parameters `(tau K J delta B11 B12 B22 c1 c2 : ℝ) (htau : 1 < tau) (hK : K ≠ 0) (hB12 : 0 < B12)`):
     1. **Radial Character Multiplicativity (`gradeRadialCharacter`)**: For `gradeRadialCharacter tau K delta := tau ^ (K * delta)`, proves `gradeRadialCharacter tau (K + J) delta = gradeRadialCharacter tau K delta * gradeRadialCharacter tau J delta` and `gradeRadialCharacter tau (-K) delta = gradeRadialCharacter tau K (-delta)` for all real `K, J, delta` and `tau > 1`;
     2. **Single-Mode Star-Involution Compatibility (`K ≠ 0`)**: Proves `gradeRadialCharacter tau (-K) delta = gradeRadialCharacter tau K delta ↔ delta = 0` for `tau > 1` and `K ≠ 0`;
     3. **Derived Isotropic Null-Cone Vanishing & Hyperbolic Pair Obstruction (`hyperbolicPairForm`)**: Proves that for `delta ≠ 0`, the diagonal grade-invariance equations `(tau ^ (2 * K * delta) - 1) * B11 = 0` and `(tau ^ (-(2 * K * delta)) - 1) * B22 = 0` force `B11 = 0 ∧ B22 = 0`, reducing `B11 * c1 ^ 2 + 2 * B12 * c1 * c2 + B22 * c2 ^ 2 = hyperbolicPairForm B12 c1 c2` (`= 2 * B12 * c1 * c2`) with `0 < hyperbolicPairForm B12 1 1` and `hyperbolicPairForm B12 1 (-1) < 0` for `B12 > 0`;
     4. **Jordan $2 \times 2$ Basis-Action Socle Eigenvector vs. Nonzero Nilpotent Drift (`jordanTwoByTwoSocleStep`)**: For `jordanTwoByTwoSocleStep lam c0 c1 := (lam * c0 + c1, lam * c1)`, proves `jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 1 0 = (gradeRadialCharacter tau K delta, 0)` (socle vector `(1, 0)` has zero nilpotent drift) and `jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 0 1 = (1, gradeRadialCharacter tau K delta)` with nonzero socle drift component `(jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 0 1).1 ≠ 0` (the Hilbert-norm linear growth deduction $\|V_K l_{\rho,1}\|^2 = \|l_{\rho,1} + (K\log\tau)l_{\rho,0}\|^2$ for $m_\rho \ge 2$ is an external analytic corollary of that nonzero nilpotent drift).
   - [`tate_rational_diagonal_character_rigidity_and_convolution_isometry`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1864-L1896) (**Theorem 52**, parameters `(tau c_inf q K u J C_gh C_dil : ℝ) (T_conv : ℝ → ℝ) (htau : 1 < tau)`):
     1. **Tate Adelic Rational-Diagonal Phase Rigidity (`adelicPhaseDiscrepancy`)**: Parameterized over generic real `tau > 1` (instantiated at `tau = 2 * pi` in the analytic application after applying the external partial-fraction congruence `q - sum_p {q}_p in Z`), proves `(adelicPhaseDiscrepancy tau c_inf 1 = 0 ↔ c_inf = tau) ∧ (c_inf = tau → adelicPhaseDiscrepancy tau c_inf q = 0)` where `adelicPhaseDiscrepancy tau c_inf q := (tau - c_inf) * q`;
     2. **Dual Poisson Lattice Covolume Invariance**: Proves `(tau ^ K) * (tau ^ (-K)) = 1` for `tau > 1` and real `K`;
     3. **Non-Abelian Semidirect Intertwining (`logPrimeShiftAction`, `logScaleAction`)**: For `logPrimeShiftAction u J := u - J` and `logScaleAction scale u := scale * u`, proves `logScaleAction (tau ^ (-K)) (logPrimeShiftAction u J) = logPrimeShiftAction (logScaleAction (tau ^ (-K)) u) (J * (tau ^ (-K)))` and `logScaleAction (tau ^ (-K)) (logPrimeShiftAction u J) - logPrimeShiftAction (logScaleAction (tau ^ (-K)) u) J = (1 - tau ^ (-K)) * J`;
     4. **Meyer Convolution-Trace Dilation Invariance**: Proves `C_dil = C_gh → T_conv C_dil = T_conv C_gh` for any trace map `T_conv : ℝ → ℝ` (where the multiplicative Haar change-of-variables identity `((U_K g) * (U_K h)^*)(alpha) = (g * h^*)(alpha)` supplying `C_dil = C_gh` is proved analytically in §3.1).
   - [`canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1945-L2031) (**Theorem 53**, parameters `(W_arch W_prime P_K P_0 c_tau_B h0_XK J_K c_pole_transfer_h0 W_reflected W_log_X R_head R_band_X R_tail B_h0 B_refl B_log C_log_EM C_log_0 B_head B_tail M_band M_C : ℝ)` with explicit hypotheses `h_arch : W_arch = P_K - c_pole_transfer_h0`, `h_prime : W_prime = W_reflected + W_log_X + localizedResonantBandDecomp R_head R_band_X R_tail`, `h_PK : |P_K| ≤ P_0`, `h_h0 : |c_pole_transfer_h0| ≤ B_h0`, `h_refl : |W_reflected| ≤ B_refl`, `h_log : |W_log_X| ≤ B_log`, `h_head : |R_head| ≤ B_head`, `h_tail : |R_tail| ≤ B_tail`):
     1. **Attempt B Pole-Integral $J(\kappa)$ Cancellation & Orbit Decomposition**: Proves `((W_arch + c_tau_B * h0_XK - (2 * h0_XK - J_K)) + (4 * h0_XK - J_K) = W_arch + (c_tau_B + 2) * h0_XK) ∧ (0 ≤ P_0 → |P_0| ≤ P_0) ∧ C_K = canonicalCorrelationHSOrbitDecomp P_K E_ctrl_K R_band_X ∧ C_K = P_K + E_K` (for `C_K := W_arch - W_prime`, `E_ctrl_K := controlledCorrelationRemainder c_pole_transfer_h0 W_reflected W_log_X R_head R_tail`, and `E_K := E_ctrl_K - R_band_X`);
     2. **Controlled Remainder Bound & Conditional `TC-049R` Rational Bound Discharge**: Proves `|E_ctrl_K| ≤ B_ctrl ∧ |C_K - (P_K - R_band_X)| ≤ B_ctrl` (`B_ctrl := B_h0 + B_refl + B_log + B_head + B_tail`), and proves conditionally that `(B_head = (5 / 6 : ℝ) * C_log_EM → B_tail = (1 / 2 : ℝ) * C_log_0 → B_h0 < 2671923 / 1000000 → B_refl < 463730 / 1000000 → B_log < 3349009 / 1000000 → C_log_EM < 13468515 / 1000000 → C_log_0 < 557430 / 1000000 → B_ctrl < 17987140 / 1000000)`;
     3. **Pointwise Two-Way Boundedness Equivalence**: Proves `((|R_band_X| ≤ M_band → (|E_K| ≤ B_ctrl + M_band ∧ |C_K| ≤ P_0 + B_ctrl + M_band)) ∧ (|C_K| ≤ M_C → (|E_K| ≤ M_C + P_0 ∧ |R_band_X| ≤ M_C + P_0 + B_ctrl)))` (while the integer-power cutoff predicates for $H(X) = \lfloor X^{5/6}\rfloor$ and $M(X) = \lceil\max(2, X^{5/4})\rceil$ are certified externally in Python Arb helpers rather than inside Theorem 53).
   - [`prime_separation_and_canonical_band_boundary_equivalence`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2044-L2104) (**Theorem 54**, parameters `(R_X S_p_X S_p_rescaled S_p_band_xp B_p_low B_p_high q B_log C_log_EM C_log_0 B_head B_tail M_S M_R : ℝ)` with hypotheses `(hq_nonneg : 0 ≤ q) (hq_le_one : q ≤ 1) (h_sep : R_X = primeSeparationDecomp S_p_X q S_p_rescaled) (h_rescaled : S_p_rescaled = S_p_band_xp + rescaledBandBoundarySum B_p_low B_p_high) (h_low : |B_p_low| ≤ B_log + B_head) (h_high : |B_p_high| ≤ B_tail)`):
     1. **Canonical Rescaled-Band Substitution**: Proves `R_X = S_p_X - q * S_p_band_xp - q * (B_p_low + B_p_high)` (`primeSeparationDecomp S_p_X q S_p_rescaled := S_p_X - q * S_p_rescaled`, `rescaledBandBoundarySum B_p_low B_p_high := B_p_low + B_p_high`);
     2. **Boundary Discrepancy Bound & Conditional Rational Discharge**: Proves `|B_p_low + B_p_high| ≤ B_log + B_head + B_tail ∧ (B_head = (5 / 6 : ℝ) * C_log_EM → B_tail = (1 / 2 : ℝ) * C_log_0 → B_log < 3349009 / 1000000 → C_log_EM < 13468515 / 1000000 → C_log_0 < 557430 / 1000000 → B_log + B_head + B_tail < 14851487 / 1000000)`;
     3. **Single-Step Two-Way Boundedness Transfer**: Proves `(|S_p_X| ≤ M_S ∧ |S_p_band_xp| ≤ M_S → |R_X| ≤ (1 + q) * M_S + q * (B_log + B_head + B_tail)) ∧ (|R_X| ≤ M_R ∧ |S_p_band_xp| ≤ M_S → |S_p_X| ≤ M_R + q * M_S + q * (B_log + B_head + B_tail))` (where the squarefree divisibility partition $m = pd$, the lower cutoff comparison $H(X)/p \le H(X/p)$, and the upper boundary bound $|\Delta_{p,\mathrm{high}}(X)| \le B_{\mathrm{tail}}$ across both cutoff orderings $M(X)/p \ge M(X/p)$ and $M(X)/p < M(X/p)$ are proved analytically outside Lean).
   - [`summation_by_parts_endpoint_bound_and_smooth_mertens_reduction`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2117-L2164) (**Theorem 55**, parameters `(R_X M_B F_B I_mertens M_cut X25 C_log_0 M_I M_R : ℝ)` with hypotheses `(h_sbp : R_X = summationByPartsDecomp M_B F_B I_mertens) (h_M_pos : 0 < M_cut) (h_X25_nonneg : 0 ≤ X25) (h_C_nonneg : 0 ≤ C_log_0) (h_mertens_triv : |M_B| ≤ M_cut) (h_F_bound : |F_B| * (M_cut ^ 3) ≤ C_log_0 * X25) (h_cutoff_dom : X25 ≤ M_cut ^ 2)`):
     1. **Unconditional Upper-Endpoint Cancellation**: Proves `|M_B * F_B| * (M_cut ^ 2) ≤ C_log_0 * X25 ∧ |M_B * F_B| ≤ C_log_0` (`summationByPartsDecomp M_B F_B I_mertens := M_B * F_B + I_mertens`);
     2. **Smooth Mertens Integral Transfer Discrepancy**: Proves `|R_X - I_mertens| ≤ C_log_0 ∧ (C_log_0 < 557430 / 1000000 → |R_X - I_mertens| < 557430 / 1000000)`;
     3. **Two-Way Reduction Between $R_X$ and $I_{\mathrm{mertens}}$**: Proves `(|I_mertens| ≤ M_I → |R_X| ≤ M_I + C_log_0) ∧ (|R_X| ≤ M_R → |I_mertens| ≤ M_R + C_log_0)` (where Stieltjes integration by parts and the termwise Euler derivative $\widetilde{W}_{\log}(u) = \frac{1}{2}W_{\log}(u) + u W_{\log}'(u)$ are proved analytically outside Lean).
   - [`iterated_prime_tower_telescoping_and_coprime_band_transfer`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2177-L2218) (**Theorem 56**, parameters `(S_0 S_1 S_2 R_0 R_1 B_0 B_1 q M_R B_rescaled : ℝ)` with hypotheses `(hq_nonneg : 0 ≤ q) (hq_lt_one : q < 1) (h_step0 : R_0 = S_0 - q * S_1 - q * B_0) (h_step1 : R_1 = S_1 - q * S_2 - q * B_1) (h_R0 : |R_0| ≤ M_R) (h_R1 : |R_1| ≤ M_R) (h_B0 : |B_0| ≤ B_rescaled) (h_B1 : |B_1| ≤ B_rescaled)`):
     1. **Two-Step Canonical-Band Inverse Tower Identity (`twoStepPrimeTowerSum`)**: For `twoStepPrimeTowerSum R_0 R_1 B_0 B_1 q S_2 := (R_0 + q * B_0) + q * (R_1 + q * B_1) + (q ^ 2) * S_2`, proves `S_0 = twoStepPrimeTowerSum R_0 R_1 B_0 B_1 q S_2`;
     2. **Two-Step Remainder Bound**: Proves `|S_0 - (q ^ 2) * S_2| ≤ (1 + q) * (M_R + q * B_rescaled)`;
     3. **Terminal Contraction Bound (`S_2 = 0`)**: Proves `S_2 = 0 → (1 - q) * |S_0| ≤ M_R + q * B_rescaled` (where induction over arbitrary finite depth $L \ge 1$ is proved analytically in §8.1–§8.2).
2. **Established Externally (Analytic Derivations + SymPy + 256-bit Arb Enclosures)**:
   - Unconditional spatial and Mellin–Plancherel convergence of $\|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 + 4\|R_0\psi_\tau\|_{L^2}^2 = P_\tau(0) \approx 2.55825801$, the spatial/Mellin identity $(R_0 f)(y) = \int_0^y (t/y)^{1/2}(Df)(t)\frac{dt}{t} = f(y) - \frac{1}{2}\int_0^y (t/y)^{1/2}f(t)\frac{dt}{t}$ with $J(\kappa) = \int_0^\infty e^{-u/2}(h_0(e^{\kappa+u}) + h_0(e^{\kappa-u}))\,du$, and the unitary dilation Cauchy–Schwarz bound $|h_0(X_K)| = |\langle T_{|K|}\psi_\tau, \psi_\tau\rangle_{L^2(d^\times y)}| \le h_0(1) = \frac{92193}{512\cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} = 0.49736248380990124448\ldots$;
   - The 4th-order Euler–Maclaurin bound $|W_{\log}(X)| \le C_{\log,\mathrm{EM}}\,X^{-5/2}$ ($C_{\log,\mathrm{EM}} \approx 13.468510 < 13.468515$), small-scale bound $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ ($C_{\log,0} \approx 0.557430$), and clamped cutoff certification $M(X) = \lceil\max(2, X^{5/4})\rceil$ ($M \ge 2 \land X^5 \le M^4 \land (M = 2 \lor (M-1)^4 < X^5)$) from `TC-049`/`TC-049R` and `TC-050R2`;
   - The Connes–Consani sine-integral formula for $\delta(\rho)$ (`arXiv:2006.13771`, Prop. 2.2) and its 256-bit Arb evaluation;
   - **Both Directions of the Scalar RH Equivalence vs. Operator-Level Realization Scope**: Both directions of the scalar correlation equivalence $\text{RH} \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| \le C_\tau(0) \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty$ hold **unconditionally in zero multiplicity $m_\rho \ge 1$** (since $\operatorname{Res}_{s=\rho}(\xi'(s)/\xi(s)) = m_\rho$, equivalently $\operatorname{Res}_{s=\rho}(-\xi'(s)/\xi(s)) = -m_\rho$, so on $\operatorname{Re}(\rho) = 1/2$ each distinct zero contributes $m_\rho|F_\tau(\rho)|^2\tau^{-iK\gamma_\rho}$ with no polynomial drift in $K$, while `TASK-TC-037` / Theorem 12 proves $\sup_{K\in\mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \implies \text{RH}$ via Laplace–Carleman analytic continuation); at the operator level, realizing the **socle eigenvectors** $l_{\rho,0} \in \ker({}^t D_- - \rho)\setminus\{0\}$ unitarily is equivalent to **$\text{RH}$ alone**, whereas realizing the **full generalized-eigenvector action** on $\mathcal{H}_-^0$ unitarily is equivalent to **$\text{RH} + \text{Simplicity}$** ($m_\rho = 1$).

---

## 7. Outcome Classification and Single Surviving Open Obligation (`SUBGATE-TC-043A`)

`TASK-TC-050`, `TASK-TC-050R`, `TASK-TC-050R2`, `TASK-TC-051`, and `TASK-TC-051R` achieve **Target 2** in full and derive the exact prime-separation and summation-by-parts reductions of the resonant divisor band:
- They prove that multiplicative compatibility on the grade algebra holds unconditionally for all $\rho \in \mathbb{C}$, whereas star-involution compatibility $V_K^* = V_{-K}$ holds if and only if $\operatorname{Re}(\rho) = 1/2$, with any off-critical pair $\{\rho, 1 - \bar{\rho}\}$ ($\operatorname{Re}(\rho) \ne 1/2$) forcing an isotropic null cone and signature-$(1,1)$ hyperbolic plane on the Jordan socle $\operatorname{span}\{l_{\rho,0}, l_{\rho^\sharp,0}\}$ (`Theorem 51`).
- They construct the unconditional positive Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}} = \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y)$ with the one-sided Attempt B shift-difference operator $(A_\tau^B f)(x, y) = f(y) - f(y/x)$ and Hilbert–Schmidt unitary orbit $B_K = \mathcal{U}_K B_0$ with positive-definite matrix coefficient $P_\tau(K) = \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}} = W_{\mathrm{arch}}(h_K) + (c_\tau^B + 2)h_0(\tau^{|K|})$ ($|P_\tau(K)| \le P_\tau(0) \approx 2.558258$), and prove the exact decomposition $C_\tau(K) = P_\tau(K) + E_\tau(K)$ with $E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|})$ at the restored `TC-049`/`TC-049R` cutoffs $H(X) = \lfloor X^{5/6}\rfloor$ and $M(X) = \lceil\max(2, X^{5/4})\rceil$ (`Theorem 53`).
- Because $|P_\tau(K)| \le P_\tau(0) \approx 2.558258$ and $|E_{\tau,\mathrm{controlled}}(K)| \le B_{\mathrm{ctrl}} < 17.987140$ (with $\limsup_{|K|\to\infty}|E_{\tau,\mathrm{controlled}}(K)| \le \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} < 11.502478$) are unconditionally bounded for all $K \in \mathbb{A}_{\mathbb{R}}$, uniform boundedness of $C_\tau(K)$ is equivalent to the **single surviving open arithmetic lemma (`SUBGATE-TC-043A`)**:
  $$
  \boxed{\exists M_{\mathrm{band}} < \infty \quad \forall X \ge 1 : \quad \Biggl|\sum_{\lfloor X^{5/6}\rfloor < m \le \lceil\max(2, X^{5/4})\rceil} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\Biggr| \le M_{\mathrm{band}}.}
  $$
  `SUBGATE-TC-043A` remains `OPEN` (`rh_proved: false`).

---

## 8. `TASK-TC-051` / `TASK-TC-051R`: Exact Prime-Separation Identity, Canonical Rescaled-Band Boundary Theorem, Multi-Prime Sieve Collapse, and Summation by Parts (`Section 7`, Theorems 54–56)

In `TASK-TC-051` and `TASK-TC-051R`, we analyze the resonant-band sum $R_{\mu,\mathrm{band}}(X) = \sum_{H(X) < m \le M(X)} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}(X/m)$ along two exact analytic routes—(A) multiplicative squarefree prime separation and prime-power tower inversion, and (B) summation by parts against the canonical weight $F_X(t) = t^{-1/2}W_{\log}(X/t)$—and evaluate sign-sequence discrimination across the four implemented bounded sequences.

### 8.1 Exact Single-Prime Separation Identity and Simultaneously Rescaled Tower Inversion (`Theorem 54`)

1. **Consistent Interval Sum Definitions and Single-Prime Separation**:
   For any $X > 0$, any real endpoints $0 \le A < B$, and any prime $p \ge 2$ with $q := p^{-1/2} \in (0, 1)$, define
   $$
   R(X; A, B) := \sum_{A < m \le B} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right), \qquad S_p(X; A, B) := \sum_{\substack{A < m \le B \\ p \nmid m}} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right),
   $$
   where both sums run over positive integers $m \in \mathbb{Z}_{\ge 1} \cap (A, B]$. Partitioning $m \in (A, B]$ into $p \nmid m$ and $m = p d$ with $d \in (A/p, B/p]$ gives $\mu(pd) = 0$ whenever $p \mid d$ ($p^2 \mid m$) and $\mu(pd) = -\mu(d)$, $(pd)^{-1/2} = q\,d^{-1/2}$ whenever $p \nmid d$. Hence
   $$
   \sum_{\substack{A < m \le B \\ p \mid m}} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)
   = -q \sum_{\substack{A/p < d \le B/p \\ p \nmid d}} \frac{\mu(d)}{\sqrt{d}}\,W_{\log}\!\left(\frac{X/p}{d}\right)
   = -q\,S_p\!\left(\frac{X}{p};\, \frac{A}{p},\, \frac{B}{p}\right),
   $$
   yielding the **exact single-prime separation identity**:
   $$
   \boxed{R(X; A, B) = S_p(X; A, B) - q\,S_p\!\left(\frac{X}{p};\, \frac{A}{p},\, \frac{B}{p}\right), \qquad q = p^{-1/2}.}
   $$
   (If the $p \nmid d$ exclusion in the second term were omitted—replacing $S_p(X/p; A/p, B/p)$ by $R(X/p; A/p, B/p)$—every $m \in (A, B]$ divisible by $p^2$ with $\mu(m/p) \ne 0$ would be miscounted; `all_p_squared_obstructions_detected: true` in the JSON artifact certifies this nonzero error whenever such $m$ exist.)
2. **Simultaneously Rescaled Arbitrary-Interval Tower Inversion**:
   For a fixed initial interval $(A, B]$ and scale $X > 0$, define the simultaneously rescaled sequences
   $$
   R_j := R\!\left(\frac{X}{p^j};\, \frac{A}{p^j},\, \frac{B}{p^j}\right), \qquad S_j := S_p\!\left(\frac{X}{p^j};\, \frac{A}{p^j},\, \frac{B}{p^j}\right) \qquad (j \ge 0).
   $$
   Then the single-prime separation identity at step $j$ reads $R_j = S_j - q\,S_{j+1}$, or equivalently $S_j = R_j + q\,S_{j+1}$. Iterating over $L \ge 1$ steps gives the exact finite inverse tower:
   $$
   \boxed{R_j = S_j - q\,S_{j+1}, \qquad S_0 = \sum_{j=0}^{L-1} q^j R_j + q^L S_L \qquad (L \ge 1).}
   $$
   In particular:
   - for $L = 1$: $S_0 = R_0 + q\,S_1$;
   - for $L = 2$: $S_0 = R_0 + q\,R_1 + q^2 S_2$;
   - for any terminal $L$ with $B / p^L < 1$: the interval $(A/p^L, B/p^L] \subset (0, 1)$ contains no positive integers, so $S_L = 0$ and $S_0 = \sum_{j=0}^{L-1} q^j R_j$.

### 8.2 Canonical-Band Rescaled Boundary Theorem, Canonical-Band Inverse Tower, and Multi-Prime Inclusion–Exclusion (`Theorems 54 & 56`)

1. **Canonical-Band Separation and Sub-Unit Zero Extension**:
   Define the canonical resonant-band sums for $Y \ge 1$:
   $$
   R_{\mathrm{band}}(Y) := R\bigl(Y;\, H(Y), M(Y)\bigr), \qquad S_{p,\mathrm{band}}(Y) := S_p\bigl(Y;\, H(Y), M(Y)\bigr), \qquad H(Y) = \lfloor Y^{5/6}\rfloor, \quad M(Y) = \lceil\max(2, Y^{5/4})\rceil,
   $$
   and declare the sub-unit zero extension $R_{\mathrm{band}}(Y) := 0$ and $S_{p,\mathrm{band}}(Y) := 0$ for $0 < Y < 1$. Defining the rescaled-cutoff boundary discrepancy
   $$
   B_p(X) := S_p\!\left(\frac{X}{p};\, \frac{H(X)}{p},\, \frac{M(X)}{p}\right) - S_{p,\mathrm{band}}\!\left(\frac{X}{p}\right),
   $$
   the single-prime separation identity at $(A, B) = (H(X), M(X))$ becomes
   $$
   \boxed{R_{\mathrm{band}}(X) = S_{p,\mathrm{band}}(X) - q\,S_{p,\mathrm{band}}\!\left(\frac{X}{p}\right) - q\,B_p(X), \qquad q = p^{-1/2}.}
   $$
2. **Universal Uniform Bound on $B_p(X)$ Across All $X \ge 1$, All Primes $p \ge 2$, and Both Upper-Cutoff Orderings (`Theorem 54`)**:
   Decompose $B_p(X) = \Delta_{p,\mathrm{low}}(X) + \Delta_{p,\mathrm{high}}(X)$ for $Y := X/p \ge 1$, where
   $$
   \Delta_{p,\mathrm{low}}(X) := S_p\!\left(Y;\, \frac{H(X)}{p},\, H(Y)\right), \qquad \Delta_{p,\mathrm{high}}(X) := S_p\!\left(Y;\, M(Y),\, \frac{M(X)}{p}\right) - S_p\!\left(Y;\, \frac{M(X)}{p},\, M(Y)\right).
   $$
   - **Lower Boundary $\Delta_{p,\mathrm{low}}(X)$ ($Y = X/p \ge 1$)**:
     Since $H(X)/p = \lfloor X^{5/6}\rfloor/p \le p^{-1/6}(X/p)^{5/6} < Y^{5/6}$, every integer $d \le H(X)/p$ satisfies $d \le \lfloor Y^{5/6}\rfloor = H(Y)$, so $\lfloor H(X)/p\rfloor \le H(Y)$ always holds. The integers $d \in (H(X)/p, H(Y)]$ with $p \nmid d$ consist of at most $d = 1$ (only when $H(X) < p$, bounded by $|W_{\log}(Y)| \le B_{\log}$) together with head integers $2 \le d \le H(Y)$, bounded by $C_{\log,\mathrm{EM}}Y^{-5/2}\sum_{2 \le d \le H(Y)} d^2 \le \frac{5}{6}C_{\log,\mathrm{EM}} = B_{\mathrm{head}}$. Thus $|\Delta_{p,\mathrm{low}}(X)| \le B_{\log} + B_{\mathrm{head}}$ for all $X \ge p$, and $|\Delta_{p,\mathrm{low}}(X)| \le B_{\mathrm{head}}$ whenever $H(X) \ge p$.
   - **Upper Boundary $\Delta_{p,\mathrm{high}}(X)$ Across Both Cutoff Orderings ($Y = X/p \ge 1$)**:
     Because $M(Y) = \lceil\max(2, Y^{5/4})\rceil$ is clamped at $2$ on $1 \le Y < 2^{4/5}$, both orderings between $M(X)/p$ and $M(Y)$ occur on $X \ge p$ and must be bounded explicitly:
     1. **Case 1 ($M(X)/p \ge M(Y)$)**: Here $\Delta_{p,\mathrm{high}}(X) = S_p(Y; M(Y), M(X)/p)$ sums over integers $d \in (M(Y), M(X)/p]$ with $p \nmid d$. Since every such integer satisfies $d \ge M(Y) + 1 > Y^{5/4}$, the super-scale tail bound gives
        $$
        \bigl|\Delta_{p,\mathrm{high}}(X)\bigr| \le C_{\log,0}\,Y^{5/2} \sum_{d > M(Y)} d^{-3} \le \frac{C_{\log,0}\,Y^{5/2}}{2\,M(Y)^2} \le \frac{1}{2}\,C_{\log,0} = B_{\mathrm{tail}}.
        $$
     2. **Case 2 ($M(X)/p < M(Y)$, small-$Y$ single-endpoint regime)**: Since $M(X)/p \ge X^{5/4}/p = p^{1/4}Y^{5/4} > Y^{5/4}$, the inequality $M(X)/p < M(Y) = \lceil\max(2, Y^{5/4})\rceil$ can occur only when $1 \le Y < 2^{4/5}$ so $M(Y) = 2$ and $M(X) < 2p$ (for example at $X = 2, p = 2$, where $Y = 1$, $M(2) = 3$, $M(2)/2 = 3/2 < 2 = M(1)$). Because $M(X)/p > Y^{5/4} \ge 1$, the half-open interval $(M(X)/p, M(Y)] \subset (1, 2]$ contains **at most the single integer endpoint $d = M(Y) = 2$**. Even before applying the coprime filter $p \nmid d$ (which annihilates $d = 2$ when $p = 2$), a single term at $d = M(Y) \ge 2$ with $Y^{5/2}/M(Y)^2 \le 1$ satisfies
        $$
        \bigl|\Delta_{p,\mathrm{high}}(X)\bigr| \le \frac{1}{\sqrt{M(Y)}}\Bigl|W_{\log}\!\left(\frac{Y}{M(Y)}\right)\Bigr| \le \frac{C_{\log,0}\,Y^{5/2}}{M(Y)^3} = \frac{C_{\log,0}}{M(Y)}\cdot\frac{Y^{5/2}}{M(Y)^2} \le \frac{1}{2}\,C_{\log,0} = B_{\mathrm{tail}}.
        $$
   - **Sub-Unit Regime ($1 \le X < p$, so $Y = X/p < 1$)**:
     When $1 \le X < p$, $S_{p,\mathrm{band}}(X/p) = 0$ by the sub-unit zero extension, so $B_p(X) = S_p(Y; H(X)/p, M(X)/p)$ sums over positive integers $d \ge 1$ with $Y/d \le Y < 1$, giving $|B_p(X)| \le \sum_{d \ge 1} d^{-1/2} C_{\log,0}(Y/d)^{5/2} = \zeta(3)\,C_{\log,0}\,Y^{5/2} \le \zeta(3)\,C_{\log,0} = [0.6700626 \pm 3.99 \times 10^{-8}] < B_{\mathrm{rescaled}}$.
   Combining all regimes yields the **universal unconditional bound** (`Theorem 54`):
   $$
   \boxed{\forall X \ge 1,\;\forall p \in \mathcal{P}:\quad \bigl|B_p(X)\bigr| \le B_{\mathrm{rescaled}} := B_{\log} + \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [14.85148 \pm 5.61 \times 10^{-6}] < 14.851486,}
   $$
   and whenever $H(X) \ge p$:
   $$
   \boxed{\forall X \ge 1 \text{ with } H(X) \ge p:\quad \bigl|B_p(X)\bigr| \le B_{\mathrm{head}} + B_{\mathrm{tail}} = \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [11.50247 \pm 5.61 \times 10^{-6}] < 11.502478.}
   $$
3. **Canonical-Band Finite Inverse Tower and Two-Way Coprime Band Equivalence (`Theorem 56`)**:
   Rewriting the canonical-band relation at scale $X/p^j$ as $S_{p,\mathrm{band}}(X/p^j) = \bigl(R_{\mathrm{band}}(X/p^j) + q\,B_p(X/p^j)\bigr) + q\,S_{p,\mathrm{band}}(X/p^{j+1})$ and iterating over $L \ge 1$ steps yields the exact **canonical-band inverse tower**:
   $$
   \boxed{S_{p,\mathrm{band}}(X) = \sum_{j=0}^{L-1} q^j\Bigl(R_{\mathrm{band}}\!\left(\frac{X}{p^j}\right) + q\,B_p\!\left(\frac{X}{p^j}\right)\Bigr) + q^L\,S_{p,\mathrm{band}}\!\left(\frac{X}{p^L}\right) \qquad (L \ge 1).}
   $$
   In particular:
   - for $L = 1$: $S_{p,\mathrm{band}}(X) = (R_{\mathrm{band}}(X) + q\,B_p(X)) + q\,S_{p,\mathrm{band}}(X/p)$;
   - for $L = 2$ (formalized directly as `twoStepPrimeTowerSum` in Lean **Theorem 56**):
     $$
     S_{p,\mathrm{band}}(X) = \bigl(R_{\mathrm{band}}(X) + q\,B_p(X)\bigr) + q\bigl(R_{\mathrm{band}}(X/p) + q\,B_p(X/p)\bigr) + q^2 S_{p,\mathrm{band}}(X/p^2);
     $$
   - for terminal depth $L = \lfloor\log_p X\rfloor + 1$: we have $X/p^L < 1$, so $S_{p,\mathrm{band}}(X/p^L) = 0$ by the declared sub-unit zero extension (note the distinction between the canonical-band termination condition $X/p^L < 1$ and the rescaled-interval termination condition $B/p^L < 1$ in §8.1).
   Since $\sum_{j=0}^{\lfloor\log_p X\rfloor} q^j < (1 - q)^{-1} = (1 - p^{-1/2})^{-1} < \infty$, we obtain the **unconditional two-way boundedness equivalence** for every fixed prime $p \ge 2$ (in particular $p = 2$, odd squarefree integers $2 \nmid m$):
   $$
   \boxed{\sup_{X \ge 1}\bigl|R_{\mathrm{band}}(X)\bigr| < \infty \iff \sup_{X \ge 1}\bigl|S_{p,\mathrm{band}}(X)\bigr| < \infty,}
   $$
   with explicit two-way bounds $\sup_{X\ge 1}|R_{\mathrm{band}}(X)| \le (1 + q)\sup_{Y\ge 1}|S_{p,\mathrm{band}}(Y)| + q\,B_{\mathrm{rescaled}}$ and $\sup_{X\ge 1}|S_{p,\mathrm{band}}(X)| \le (1 - q)^{-1}\bigl(\sup_{Y\ge 1}|R_{\mathrm{band}}(Y)| + q\,B_{\mathrm{rescaled}}\bigr)$.
4. **Rightly Oriented Multi-Prime Inclusion–Exclusion Formula, $P=2$ Orientation Regression, Tautological Sieve Collapse, and Qualified Coset Shift**:
   For any finite set of distinct primes $\mathcal{P}$ with squarefree product $P = \prod_{p \in \mathcal{P}} p$, define $S_P(X; A, B) := \sum_{A < m \le B,\, \gcd(m, P)=1} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}(X/m)$. Grouping $m \in (A, B]$ with $\mu(m) \ne 0$ by the squarefree divisor $d = \gcd(m, P) \mid P$ and writing $m = d k$ with $\gcd(k, P) = 1$ and $\gcd(d, k) = 1$ ($\mu(dk) = \mu(d)\mu(k)$) yields the **rightly oriented multi-prime identity**:
   $$
   \boxed{R(X; A, B) = \sum_{d \mid P} \frac{\mu(d)}{\sqrt{d}}\,S_P\!\left(\frac{X}{d};\, \frac{A}{d},\, \frac{B}{d}\right).}
   $$
   - **Orientation Regression Check at $P = 2$, $X = 1$, $(A, B] = (1, 2]$ (`p2_x1_interval_1_2_orientation_regression`)**:
     At $P = 2, X = 1, (A, B] = (1, 2]$, the only integer in $(1, 2]$ is $m = 2$, so $R(1; 1, 2) = -\frac{1}{\sqrt{2}}W_{\log}(1/2)$, $S_2(1; 1, 2) = 0$, and $S_2(1/2; 1/2, 1) = W_{\log}(1/2)$. The rightly oriented formula gives $S_2(1; 1, 2) - \frac{1}{\sqrt{2}}S_2(1/2; 1/2, 1) = -\frac{1}{\sqrt{2}}W_{\log}(1/2) = R(1; 1, 2)$ (`correct_orientation_encloses_zero: true`), whereas the reversed formula $\sum_{d \mid 2}\frac{\mu(d)}{\sqrt{d}}R(1/d; 1/d, 2/d) = R(1; 1, 2) - \frac{1}{\sqrt{2}}R(1/2; 1/2, 1) = -\sqrt{2}W_{\log}(1/2) \ne 0 = S_2(1; 1, 2)$ fails by a certified nonzero discrepancy (`reversed_formula_detected_nonzero: true`).
   - **Tautological Full-Sieve Collapse and Exact Euler-Product Expansion**:
     When $\mathcal{P} = \{p \le M(X)\}$ sieves all primes up to $M(X)$ with $P = \prod_{p \le M(X)} p$, the only positive integer $k \le M(X)/d$ coprime to $P$ is $k = 1$, which lies in $(H(X)/d, M(X)/d]$ if and only if $H(X) < d \le M(X)$. Thus $S_P(X/d; H(X)/d, M(X)/d) = \mathbf{1}_{H(X) < d \le M(X)}\,W_{\log}(X/d)$ and the multi-prime expansion $\sum_{d \mid P}\frac{\mu(d)}{\sqrt{d}}S_P(X/d; H(X)/d, M(X)/d)$ collapses tautologically back to $\sum_{H(X) < d \le M(X)}\frac{\mu(d)}{\sqrt{d}}W_{\log}(X/d) = R_{\mathrm{band}}(X)$ (`full_sieve_P_le_M_X_tautological_collapse_verified: true`). Meanwhile, taking absolute values across divisor branches $d \mid \prod_{p \le y} p$ multiplies by the Euler product $\prod_{p \le y}(1 + p^{-1/2})$, whose logarithm satisfies the second-order expansion
     $$
     \boxed{\sum_{p \le y}\log\!\left(1 + \frac{1}{\sqrt{p}}\right) = \sum_{p \le y}\frac{1}{\sqrt{p}} - \frac{1}{2}\sum_{p \le y}\frac{1}{p} + O(1) \to \infty \qquad (y \to \infty),}
     $$
     reaching $[45258011.27 \pm 1.15 \times 10^{-5}]$ at $y = 997$ ($\pi(997) = 168$).
   - **Qualified Multiplicative Coset Note (`multiplicative_coset_shift_note`)**:
     Whether $\log_\tau p = \frac{\log p}{\log(2\pi)}$ lies in $\mathbb{A}_{\mathbb{R}}$ is **not assumed**; if $\log_\tau p \notin \mathbb{A}_{\mathbb{R}}$, then prime dilation $X_K \mapsto X_K / p = \tau^{|K| - \log_\tau p}$ leaves the algebraic grade locus $\tau^{\mathbb{A}_{\mathbb{R}}}$ for the multiplicative coset $p^{-1}\tau^{\mathbb{A}_{\mathbb{R}}}$, whereas all rescaled boundary bounds in §8.2 are proved on all of $\mathbb{R}_{>0}$ without assuming $\log_\tau p \in \mathbb{A}_{\mathbb{R}}$.
   - **Certified 256-bit Arb Canonical-Band Prime-Separation Table (`sample_band_prime_table` in JSON Artifact)**:

| Scale $X$ | Prime $p$ | $(H(X), M(X))$ | $(H(X/p), M(X/p))$ | Upper-Cutoff Regime | $R_{\mu,\mathrm{band}}(X)$ | $S_{p,\mathrm{band}}(X)$ | $S_{p,\mathrm{band}}(X/p)$ | Boundary Discrepancy $B_p(X)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $2$ | $(1, 2)$ | $(0, 0)$ | $X/p < 1$ (sub-unit regime) | $-0.0138854010$ | $+0.0000000000$ | $+0.0000000000$ | $+0.0196369224$ |
| $1$ | $3$ | $(1, 2)$ | $(0, 0)$ | $X/p < 1$ (sub-unit regime) | $-0.0138854010$ | $-0.0138854010$ | $+0.0000000000$ | $+0.0000000000$ |
| $2$ | $2$ | $(1, 3)$ | $(1, 2)$ | $M(X)/p < M(X/p)$ (small-$Y$ single-endpoint regime) | $+0.0108988909$ | $-0.0202572131$ | $+0.0000000000$ | $-0.0440613848$ |
| $2$ | $3$ | $(1, 3)$ | $(0, 0)$ | $X/p < 1$ (sub-unit regime) | $+0.0108988909$ | $+0.0311561040$ | $+0.0000000000$ | $+0.0350865224$ |
| $\tau$ | $2$ | $(4, 10)$ | $(2, 5)$ | $M(X)/p \ge M(X/p)$ | $+0.0305137548$ | $+0.0440915006$ | $+0.0192018323$ | $+0.0000000000$ |
| $\tau$ | $3$ | $(4, 10)$ | $(1, 3)$ | $M(X)/p \ge M(X/p)$ | $+0.0305137548$ | $+0.0548648508$ | $+0.0421773354$ | $+0.0000000000$ |
| $16$ | $2$ | $(10, 32)$ | $(5, 14)$ | $M(X)/p \ge M(X/p)$ | $+0.0050456338$ | $+0.0184614185$ | $+0.0126828335$ | $+0.0062899512$ |
| $16$ | $3$ | $(10, 32)$ | $(4, 9)$ | $M(X)/p \ge M(X/p)$ | $+0.0050456338$ | $+0.0204293360$ | $+0.0189417684$ | $+0.0077035854$ |
| $\tau^2$ | $2$ | $(21, 99)$ | $(12, 42)$ | $M(X)/p \ge M(X/p)$ | $+0.0094869970$ | $+0.0034897521$ | $+0.0094402188$ | $-0.0179216039$ |
| $\tau^2$ | $3$ | $(21, 99)$ | $(8, 26)$ | $M(X)/p \ge M(X/p)$ | $+0.0094869970$ | $+0.0058847113$ | $-0.0021883084$ | $-0.0040510335$ |

### 8.3 Exact Summation by Parts and Smooth-Kernel Derivative $\widetilde{W}_{\log}(u)$ (`Theorem 55`)

1. **Abel Summation by Parts Identity**:
   Let $M_A(t) := \sum_{A < m \le t} \mu(m)$ denote the right-continuous relative Mertens step function (with $M_A(A) = 0$) and $F_X(t) := t^{-1/2}\,W_{\log}(X/t)$. For all $X > 0$ and $0 < A < B$,
   $$
   \boxed{R(X; A, B) = M_A(B)\,F_X(B) - \int_A^B M_A(t)\,F_X'(t)\,dt.}
   $$
2. **Exact Smooth-Kernel Derivative Formula**:
   Writing $u = X/t$ ($\frac{du}{dt} = -\frac{u}{t}$), the chain rule gives $F_X'(t) = -t^{-3/2}\bigl[\frac{1}{2}W_{\log}(u) + u W_{\log}'(u)\bigr]$. For each $k \ge 2$ and $w_k(u) = h_0(k/u)$ with $\alpha = k/u$, we have $u w_k'(u) = -\alpha h_0'(\alpha)$, so $\frac{1}{2}w_k(u) + u w_k'(u) = \frac{1}{2}h_0(\alpha) - \alpha h_0'(\alpha) = \widetilde{h}_0(\alpha)$. Differentiating term-by-term (justified by uniform convergence on compact subsets of $(0, \infty)$ via $|\frac{d}{du}h_0(k/u)| \le (\frac{1}{2}C_0 + \widetilde{C}_0)u^{3/2}k^{-5/2}$) yields the exact derivative kernel:
   $$
   \boxed{\widetilde{W}_{\log}(u) = \frac{1}{2}\,W_{\log}(u) + u\,W_{\log}'(u) = \sum_{k \ge 2} \frac{\log k}{\sqrt{k}}\left[\frac{1}{2}\,h_0\!\left(\frac{k}{u}\right) - \frac{k}{u}\,h_0'\!\left(\frac{k}{u}\right)\right] = \sum_{k \ge 2} \frac{\log k}{\sqrt{k}}\,\widetilde{h}_0\!\left(\frac{k}{u}\right), \qquad -F_X'(t) = t^{-3/2}\,\widetilde{W}_{\log}\!\left(\frac{X}{t}\right).}
   $$
   At $(A, B) = (H(X), M(X))$, the resonant-band sum decomposes as
   $$
   \boxed{R_{\mu,\mathrm{band}}(X) = M_{H(X)}\bigl(M(X)\bigr)\,F_X\bigl(M(X)\bigr) + I_{M,\mathrm{band}}(X), \qquad I_{M,\mathrm{band}}(X) := \int_{H(X)}^{M(X)} M_{H(X)}(t)\,t^{-3/2}\,\widetilde{W}_{\log}\!\left(\frac{X}{t}\right)dt.}
   $$
3. **Unconditional Upper-Endpoint Bound and Two-Way Smooth Mertens Reduction (`Theorem 55`)**:
   Using **only** the trivial counting inequality $|M_{H(X)}(M(X))| \le M(X) - H(X) \le M(X)$ (with zero unproved Mertens hypotheses) and the small-argument envelope $|W_{\log}(X/M(X))| \le C_{\log,0}(X/M(X))^{5/2}$ together with $M(X) \ge X^{5/4} \implies X^{5/2}/M(X)^2 \le 1$, the upper-endpoint term satisfies the **unconditional uniform bound** for all $X \ge 1$:
   $$
   \boxed{\bigl|M_{H(X)}(M(X))\,F_X(M(X))\bigr| \le M(X)\cdot M(X)^{-1/2}\,C_{\log,0}\!\left(\frac{X}{M(X)}\right)^{5/2} = C_{\log,0}\,\frac{X^{5/2}}{M(X)^2} \le C_{\log,0} = [0.55742959 \pm 7.45 \times 10^{-41}] < 0.557430.}
   $$
   Consequently (`Theorem 55`),
   $$
   \boxed{\sup_{X \ge 1}\bigl|R_{\mu,\mathrm{band}}(X)\bigr| < \infty \iff \sup_{X \ge 1}\bigl|I_{M,\mathrm{band}}(X)\bigr| < \infty, \qquad \bigl|R_{\mu,\mathrm{band}}(X) - I_{M,\mathrm{band}}(X)\bigr| \le C_{\log,0} < 0.557430 \quad (\forall X \ge 1).}
   $$
   - **Independent Complex-Analytic Quadrature Verification Scope (`max_quadrature_M = 32`)**:
     In `verify_summation_by_parts_and_tilde_W_log_identity_arb`, step-interval FTC summation is certified across all `7` sample scales $X \in \{1, 2, 4, \tau, 10, 16, \tau^2\}$ (`all_sbp_ftc_enclose_zero: true`). Direct unit-interval `acb.integral` quadrature of $\int_n^{n+1} t^{-3/2}\widetilde{W}_{\log}(X/t)\,dt$ is run independently on the `6` sample scales with $M(X) \le 32$ ($X \in \{1, 2, 4, \tau, 10, 16\}$, `independent_quadrature_performed_count: 6`, `independent_quadrature_passed_count: 6`, `all_performed_sbp_quadrature_enclose_zero: true`), while the $X = \tau^2$ row ($M(\tau^2) = 99 > 32$, `independent_quadrature_not_run_count: 1`) is explicitly marked `"independent_quadrature_status": "NOT_RUN"` with `"smooth_mertens_integral_I_M_band_quadrature_certified": null` and `"sbp_quadrature_identity_encloses_zero": null`:

| Scale $X$ | Cutoffs $(H, M)$ | $M_{H(X)}(M(X))$ | $R_{\mu,\mathrm{band}}(X)$ | Endpoint $M_{H(X)}(M(X))F_X(M(X))$ | Smooth Integral $I_{M,\mathrm{band}}(X)$ (FTC) | Sharp Bound $\frac{C_{\log,0}X^{5/2}}{M(X)^2}$ | Independent Quadrature Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $(1, 2)$ | $-1$ | $-0.0138854010$ | $-0.0138854010$ | $+0.0000000000$ | $0.139357$ | `CERTIFIED_QUADRATURE` |
| $2$ | $(1, 3)$ | $-2$ | $+0.0108988909$ | $-0.0405144262$ | $+0.0514133171$ | $0.350366$ | `CERTIFIED_QUADRATURE` |
| $4$ | $(3, 6)$ | $0$ | $+0.0053844056$ | $+0.0000000000$ | $+0.0053844056$ | $0.495493$ | `CERTIFIED_QUADRATURE` |
| $\tau$ | $(4, 10)$ | $0$ | $+0.0305137548$ | $+0.0000000000$ | $+0.0305137548$ | $0.551620$ | `CERTIFIED_QUADRATURE` |
| $10$ | $(6, 18)$ | $-1$ | $+0.0163613434$ | $-0.0064298269$ | $+0.0227911704$ | $0.544058$ | `CERTIFIED_QUADRATURE` |
| $16$ | $(10, 32)$ | $-3$ | $+0.0050456338$ | $-0.0104140507$ | $+0.0154596845$ | $0.557430$ | `CERTIFIED_QUADRATURE` |
| $\tau^2$ | $(21, 99)$ | $3$ | $+0.0094869970$ | $+0.0018216397$ | $+0.0076653573$ | $0.556954$ | `NOT_RUN` |

### 8.4 Certified 256-bit Arb Sign-Sequence Discrimination Across Scales $X \in \{1, 2, 4, \tau, 10, 16, 25, \tau^2, 64\}$ (`Section 7` of JSON Artifact)

To compare signed sums $\bigl|\sum_{H(X)<m\le M(X)} \sigma_m m^{-1/2} W_{\log}(X/m)\bigr|$ against the triangle-inequality majorant $\sum_{H(X)<m\le M(X)} |\sigma_m| m^{-1/2} |W_{\log}(X/m)|$, `verify_sign_sequence_cancellation_discrimination_arb` evaluates the four bounded sequences $\sigma_m \in \{\mu(m),\, 1,\, |\mu(m)|,\, |\mu(m)|\operatorname{sgn}(W_{\log}(X/m))\}$ in 256-bit Arb across $X \in \{1, 2, 4, \tau, 10, 16, 25, \tau^2, 64\}$ (values below are taken directly from `sign_discrimination_table` in [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json)):

| Scale $X$ | Cutoffs $(H, M)$ | Actual Möbius $R_{\mu,\mathrm{band}}(X)$ | Constant-One $R_{1,\mathrm{band}}(X)$ | Squarefree Indicator $R_{\|\mu\|,\mathrm{band}}(X)$ | Triangle-Inequality Majorant $\sum \frac{\|\mu(m)\|}{\sqrt{m}}\|W_{\log}(X/m)\|$ | Majorant / $\|R_{\mu,\mathrm{band}}(X)\|$ Ratio |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $(1, 2)$ | $-0.0138854010$ | $+0.0138854010$ | $+0.0138854010$ | $+0.0138854010$ | $1.00000000$ |
| $2$ | $(1, 3)$ | $+0.0108988909$ | $-0.0108988909$ | $-0.0108988909$ | $+0.0514133171$ | $4.71729810$ |
| $4$ | $(3, 6)$ | $+0.0053844056$ | $+0.0012329276$ | $+0.0232636200$ | $+0.0232636200$ | $4.32055491$ |
| $\tau$ | $(4, 10)$ | $+0.0305137548$ | $-0.0380922306$ | $-0.0576692464$ | $+0.0792159467$ | $2.59607338$ |
| $10$ | $(6, 18)$ | $+0.0163613434$ | $-0.0482983844$ | $-0.0083864514$ | $+0.0737477117$ | $4.50743620$ |
| $16$ | $(10, 32)$ | $+0.0050456338$ | $-0.0477730902$ | $-0.0448539391$ | $+0.1287989561$ | $25.52681408$ |
| $25$ | $(14, 56)$ | $+0.0105974982$ | $-0.0476609440$ | $-0.0186209133$ | $+0.1611394825$ | $15.20542676$ |
| $\tau^2$ | $(21, 99)$ | $+0.0094869970$ | $-0.0373670566$ | $-0.0343474534$ | $+0.2377820885$ | $25.06399947$ |
| $64$ | $(32, 182)$ | $+0.0305914155$ | $-0.0158336588$ | $+0.0190489418$ | $+0.2903267136$ | $9.49046356$ |

- **Key Discrimination Findings and Scope Qualifications**:
  1. **Signed Sum vs. Triangle-Inequality Majorant**: At $X = 64$ ($(H, M) = (32, 182)$), the signed sums are $R_{\mu,\mathrm{band}}(64) = +0.03059141547\ldots$ (which is also the maximum of $|R_{\mu,\mathrm{band}}(X)|$ on the 9-point grid), $R_{1,\mathrm{band}}(64) = -0.01583365880\ldots$, and $R_{|\mu|,\mathrm{band}}(64) = +0.01904894182\ldots$, whereas the triangle-inequality majorant $\sum_{32 < m \le 182}\frac{|\mu(m)|}{\sqrt{m}}|W_{\log}(64/m)| = +0.29032671364\ldots$ is $9.49046356\times$ larger than $|R_{\mu,\mathrm{band}}(64)|$ (and $25.52681408\times$ larger at $X = 16$ and $25.06399947\times$ larger at $X = \tau^2$).
  2. **Strict Separation of Signed Kernel Oscillation from Absolute-Value Sums**: The signed sums $R_{1,\mathrm{band}}(X) = \sum_{H < m \le M} m^{-1/2}W_{\log}(X/m)$ and $R_{|\mu|,\mathrm{band}}(X) = \sum_{H < m \le M} |\mu(m)| m^{-1/2}W_{\log}(X/m)$ incorporate the sign changes of $W_{\log}(X/m)$ across $m \in (H(X), M(X)]$, whereas the worst-case sequence $\sigma_m^{\mathrm{wc}}(X) = |\mu(m)|\operatorname{sgn}(W_{\log}(X/m))$ removes all sign cancellation and equals the absolute-value sum $\sum_{H < m \le M} |\mu(m)| m^{-1/2}|W_{\log}(X/m)|$.
  3. **Finite-Grid and Asymptotic Scope Hygiene**: Finite-grid values on $X \in [1, 64]$ do not determine the asymptotic behavior as $X \to \infty$ of $R_{1,\mathrm{band}}(X)$ or $R_{|\mu|,\mathrm{band}}(X)$, and $O(X^{1/2})$ is an upper bound for the triangle-inequality majorant $\sum_{H(X) < m \le M(X)} |\mu(m)| m^{-1/2}|W_{\log}(X/m)|$ unless a matching lower bound is proved. Closing `SUBGATE-TC-043A` requires proving an unconditional $O(1)$ bound on the signed Möbius sum $R_{\mu,\mathrm{band}}(X)$ (or equivalently on the smooth Mertens integral $I_{M,\mathrm{band}}(X)$).
