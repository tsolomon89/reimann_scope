# Faithful $\tau$-Arithmetic Spectral Realization, Adjoint Compatibility, Canonical Hilbert–Schmidt Orbit Decomposition, Resonant-Band Prime-Separation / Summation-by-Parts Analysis, Transition-Region / Vaughan Type I / Spectral–Dirichlet Compatibility, and Trivial-Zero Slopes / Coprime Squarefree Block Cancellation (`TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2` / `TASK-TC-051` / `TASK-TC-051R` / `TASK-TC-052` / `TASK-TC-052R` / `TASK-TC-052R2` / `TASK-TC-053`)

**Task ID:** `TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2` / `TASK-TC-051` / `TASK-TC-051R` / `TASK-TC-052` / `TASK-TC-052R` / `TASK-TC-052R2` / `TASK-TC-053`  
**Parent Epic:** `EPIC-TC-042`  
**Reviewed Baselines:** `5da0eb79e1732ff871ee1c7fee729c62972aa406` (`TC-048R`), `2f7871fff666091c4152ecc8657f2345aacdd4fa` (`TC-050` + `TC-049R`), `0e6ae36ce995ef3037652b3dfb67645325f990b1` (`TC-050R` HEAD; implementation commit `f5521363ea94774938fd37152d67d743413327ae`), `d93ab512c2df75af2365a3963804c172baf0e867` (`TC-050R2` merged on `main`), `b6f22dfee0dd6177ee855189304e7930f9ba3e20` (`TC-051` merged on `main`; branch tip `7ac0546b1177970ff0d87824f61643da2405c4c0`, implementation commit `333661eecd69738e8a67143e635b6db4f40170ce`), `1f576944c040d5b3a2bf8091ca803e3758c80d12` (`TC-051R` closeout accepted on `main`), `916440e688c66d461daa04b17d7435e10e65f0d4` (`TC-052` merged on `main`; implementation commit `8414aa66f1127c636c68fcf8594833c570a3344a`), `7dc75e83f6b48e6ef436f55b573910e93d0f4f48` (`TC-052R` merged on `main`; implementation commit `f230b1a72c2c336522834703534bbdb8c15a250a`), `c64596727e7142596acd073c6c8e4eb28f2eaee0` (`TC-052R2` merged on `main`)  
**Branched From:** `c64596727e7142596acd073c6c8e4eb28f2eaee0` (`task/tc-053-trivial-zero-slopes-and-coprime-cancellation`)  
**Primary Implementation Module:** [tc/faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)  
**Exported Facade Entrypoints:** [`execute_task_tc050_faithful_spectral_realization_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10185), [`execute_task_tc051_prime_arithmetic_resonant_band_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10185), [`execute_task_tc052_arithmetic_fourier_compatibility_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L9993-L10004), [`execute_task_tc053_trivial_zero_slopes_and_coprime_cancellation_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L9993-L10015)  
**Certified 256-bit Arb Data Artifact:** [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json) (`1175/1175` certified 256-bit Arb balls passing outward-rounded decimal round-trip verification)  
**Formal Verification Modules:** [formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) (`47` definitions, `59` theorems = `106` declarations, `0` `sorry`, `0` `admit`, `0` custom axioms) and [formal/RiemannScope/TrivialZero.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/TrivialZero.lean) (`4` definitions, `10` theorems = `14` declarations, `0` `sorry`, `0` `admit`, `0` custom axioms)  
**Regression Test Suite:** [tests/test_tc_faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tests/test_tc_faithful_tau_arithmetic_spectral_realization.py)  
**Status Classification:** `TRIVIAL_ZERO_SLOPE_IDENTITY_COMMON_FACTOR_EXPANSION_AND_DECOUPLED_L2_BLOCK_DECOMPOSITION_PROVED_BIVARIATE_EULER_CANCELLATION_OBSTRUCTED_SUBGATE_OPEN` (`PROVED_CONDITIONAL` + `CERTIFIED_FINITE`; `SUBGATE-TC-043A` remains `OPEN`; `rh_proved: false`)

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

2. **Positive Embedding, Operator Domain $\mathcal{D}(\mathcal{J}_\tau)$, Plancherel Multiplier $\nu(t)$, and Unitary Grade Representation (`TASK-TC-052R`)**:
   Define the grade-covariant linear map $\mathcal{J}_\tau : \mathcal{D}(\mathcal{J}_\tau) \to \mathcal{H}_\tau^{\mathrm{pos}}$ and unitary group $\mathcal{U}_K$ ($K \in \mathbb{R}$) by
   $$
   \mathcal{J}_\tau(f) := \bigl(A_\tau^B f,\; 2\,R_0 f\bigr) \in \mathcal{H}_\tau^{\mathrm{pos}},
   \qquad
   \mathcal{U}_K(\Phi, g)(x, y) := \bigl(\Phi(x, \tau^{-K} y),\; g(\tau^{-K} y)\bigr) = \bigl((U_K^B \Phi)(x, y),\; (T_K g)(y)\bigr).
   $$
   - **Exact Plancherel Multiplier $\nu(t)$ on $L^2(\mathbb{R}_{>0}, d^\times y)$**:
     Under the centered Mellin–Plancherel transform $\widehat{f}(t) := \int_0^\infty f(y)\,y^{-it}\frac{dy}{y}$ with $\|f\|_{L^2(\mathbb{R}_{>0}, d^\times y)}^2 = \frac{1}{\tau}\int_{-\infty}^\infty |\widehat{f}(t)|^2\,dt$ (for which $|\widehat{\psi_\tau}(t)|^2 = H_0(it) = |F_\tau(1/2 + it)|^2$):
     1. On $\mathcal{H}_\tau^B = L^2\bigl([1, \infty) \times \mathbb{R}_{>0}, \frac{x^{-3/2}}{x - x^{-1}}\frac{dx}{x}\frac{dy}{y}\bigr)$, $(A_\tau^B f)(x, y) = f(y) - f(y/x)$ has $y$-Mellin transform $(1 - x^{-it})\widehat{f}(t)$, so integrating $|1 - x^{-it}|^2 = 2(1 - \cos(t\log x))$ against $\frac{x^{-3/2}}{x - x^{-1}}\frac{dx}{x} = \frac{e^{-3u/2}}{2\sinh u}\,du$ ($x = e^u$) yields (`Gradshteyn–Ryzhik 3.541.1`)
        $$
        \nu_B(t) := \int_0^\infty \frac{e^{-3u/2}}{\sinh u}\bigl(1 - \cos(tu)\bigr)\,du
        = \operatorname{Re}\psi\!\left(\frac{5}{4} + \frac{it}{2}\right) - \psi\!\left(\frac{5}{4}\right) \ge 0.
        $$
     2. On $L^2(\mathbb{R}_{>0}, d^\times y)$, the Euler derivative $D = y\frac{d}{dy}$ acts as $it$ and $(K_0 f)(y) = \int_0^y (t/y)^{1/2}f(t)\frac{dt}{t}$ has centered Mellin multiplier $\frac{1}{1/2 + it}$, so $(R_0 f)(y) = \int_0^y (t/y)^{1/2}(Df)(t)\frac{dt}{t} = f(y) - \frac{1}{2}(K_0 f)(y)$ (`§5.1.1`) has centered Mellin multiplier $\frac{it}{1/2 + it} = 1 - \frac{1/2}{1/2 + it}$, and $2 R_0 f$ has squared Plancherel multiplier
        $$
        \boxed{\nu_{R_0}(t) := 4\left|\frac{it}{1/2 + it}\right|^2 = \frac{4t^2}{t^2 + 1/4} = 4 - \frac{1}{t^2 + 1/4} \ge 0.}
        $$
     3. Adding the two components gives the exact Plancherel multiplier of $\mathcal{J}_\tau f = (A_\tau^B f, 2 R_0 f)$:
        $$
        \boxed{\|\mathcal{J}_\tau f\|_{\mathcal{H}_\tau^{\mathrm{pos}}}^2 = \frac{1}{\tau}\int_{-\infty}^\infty \nu(t)\,\bigl|\widehat{f}(t)\bigr|^2\,dt, \qquad \nu(t) := \operatorname{Re}\psi\!\left(\frac{5}{4} + \frac{it}{2}\right) - \psi\!\left(\frac{5}{4}\right) + \frac{4t^2}{t^2 + 1/4}.}
        $$
        Since $\operatorname{Re}\psi(5/4 + it/2) = \operatorname{Re}\psi(1/4 + it/2) + \frac{1}{t^2 + 1/4}$ and $\psi(5/4) = \psi(1/4) + 4 = \log\pi - c_\tau^B + 2$ ($c_\tau^B = \log\pi - \psi(1/4) - 2$), the rational terms $\pm\frac{1}{t^2 + 1/4}$ cancel identically (`J(kappa)` cancellation), giving the equivalent form
        $$
        \boxed{\nu(t) = \left[\operatorname{Re}\psi\!\left(\frac{1}{4} + \frac{it}{2}\right) - \log\pi\right] + \bigl(c_\tau^B + 2\bigr), \qquad P_\tau(0) = \frac{1}{\tau}\int_{-\infty}^\infty \nu(t)\,H_0(it)\,dt = W_{\mathrm{arch}}(h_0) + \bigl(c_\tau^B + 2\bigr)h_0(1) = 2.558258007415831199724020\ldots}
        $$
     4. **Vanishing at $t = 0$, Quadratic Taylor Expansion, and Operator Domain $\mathcal{D}(\mathcal{J}_\tau)$ (`TASK-TC-052R` & `TASK-TC-052R2`)**:
        Because $1 - \cos(tu) = 2\sin^2(tu/2) \ge 0$, we have $\nu_B(t) \ge \nu_B(0) = 0$ and $\nu_{R_0}(t) = \frac{4t^2}{t^2 + 1/4} \ge 0$, with
        $$
        \boxed{\nu(0) = 0, \qquad \nu(t) \ge \frac{4t^2}{t^2 + 1/4} > 0 \quad (\forall t \ne 0), \qquad \nu(t) = \left(16 - \frac{\psi''(5/4)}{8}\right)t^2 + O(t^4) \quad (t \to 0),}
        $$
        where $16 - \frac{\psi''(5/4)}{8} = 16 + \frac{1}{4}\sum_{n=0}^\infty (n + 5/4)^{-3} = [16.16596749219211504166724589735549873591 \pm 2.00 \times 10^{-38}] > 16$. The operator domain is $\mathcal{D}(\mathcal{J}_\tau) := \bigl\{f \in L^2(\mathbb{R}_{>0}, d^\times y) : \int_{-\infty}^\infty \nu(t)|\widehat{f}(t)|^2\,dt < \infty\bigr\}$ (which contains $\mathcal{S}_\tau$ and $E_y(\mathcal{S}_\tau)$ because $\nu(t) = O(\log(2 + |t|))$). Because $\nu(t) > 0$ almost everywhere on $\mathbb{R}$ and $\nu(t) \asymp t^2$ as $t \to 0$, $\bigl(\mathcal{D}(\mathcal{J}_\tau),\, \|\mathcal{J}_\tau \cdot\|_{\mathcal{H}_\tau^{\mathrm{pos}}}\bigr)$ with $\|f\|_{\mathcal{J}_\tau} := \|\mathcal{J}_\tau f\|_{\mathcal{H}_\tau^{\mathrm{pos}}} = \bigl(\frac{1}{\tau}\int_{-\infty}^\infty \nu(t)|\widehat{f}(t)|^2\,dt\bigr)^{1/2}$ is an **inner-product space that is not complete** (for example, $\widehat{f}_n(t) = t^{-1}\mathbf{1}_{[1/n, 1]}(t) \in L^2(\mathbb{R})$ is Cauchy in the $\nu$-weighted norm because $\int_{1/n}^{1/m} \nu(t)t^{-2}\,dt \to 0$, whereas its $\nu$-weighted limit $t^{-1}\mathbf{1}_{(0, 1]}(t) \notin L^2(\mathbb{R})$ does not belong to any $f \in L^2(\mathbb{R}_{>0}, d^\times y)$), and $\mathcal{J}_\tau$ is an **isometric embedding of this inner-product space** into the Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}}$; because $\nu(0) = 0$, $\mathcal{J}_\tau$ is **not** bounded below by $2\|f\|_{L^2(\mathbb{R}_{>0}, d^\times y)}^2$ in the unweighted $L^2$ norm.
   - Because multiplicative dilation in $y$ commutes with $y \mapsto y/x$ and with $R_0$, $\mathcal{J}_\tau$ intertwines $T_K$ with $\mathcal{U}_K$:
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
| **1. Pole + Transfer Term** | $-(c_\tau^B + 2)h_0(X_K) = -c_\tau^A h_0(X_K)$ on $X_K \ge 1$ ($c_\tau^A = c_\tau^B + 2 \approx 5.37218342$) | **Unitary Dilation Cauchy–Schwarz** on $L^2(\mathbb{R}_{>0}, d^\times y)$: since $h_0(X_K) = \langle T_{|K|}\psi_\tau, \psi_\tau\rangle_{L^2(d^\times y)}$ and $\|T_{|K|}\psi_\tau\|_{L^2} = \|\psi_\tau\|_{L^2}$, $\|h_0(X_K)\| \le \|\psi_\tau\|_{L^2(d^\times y)}^2 = h_0(1) = \frac{92193}{512\cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.4973624838$ (**note:** $h_0$ is oscillatory and changes sign on $[1, \infty)$, e.g. $h_0(2) \approx -0.2174306224 < 0$; the bound uses Cauchy–Schwarz—and independently the symmetric Bernstein envelope $\|h_0(X_K)\| \le \frac{92193}{32768}(X_K + X_K^{-1})^{-5/2} \le h_0(1)$—never positivity or monotonicity of $h_0$), giving $B_{h_0} := c_\tau^A h_0(1)$; for large $X_K$, $h_0(X_K) \sim -\frac{648}{512}X_K^{6 - 17/2} = -\frac{81}{64}X_K^{-5/2} = O(X_K^{-5/2})$ ($\le \frac{92193}{32768}c_\tau^A X_K^{-5/2} \approx 15.114677\,X_K^{-5/2}$) | Unitary dilation Cauchy–Schwarz on $L^2(\mathbb{R}_{>0}, d^\times y)$ + `TASK-TC-042`/`044` symmetric Bernstein envelope + `TASK-TC-042F`/`043` | $B_{h_0} = [2.671922488868445008137488237241150824707 \pm 2.00 \times 10^{-39}] < 2.671923$ |
| **2. Reflected Small-Scale Prime Sum** | $-W(X_K^{-1}) = -\sum_{n \ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n X_K)$ on $X_K \ge 1$ | $\|W(X_K^{-1})\| \le \frac{92193}{32768}\bigl(\sum_{n=2}^\infty \frac{\Lambda(n)}{n^3}\bigr) X_K^{-5/2} \le B_{\mathrm{refl}}\,X_K^{-5/2} = O(X_K^{-5/2})$ (evaluated via prime powers $n \le 25000$ plus Rosser–Schoenfeld tail $\frac{1.558245}{25000^2}$) | `TASK-TC-043` / `TASK-TC-044` cubic prime-power majorant | $B_{\mathrm{refl}} = [0.46372978 \pm 7.98\times 10^{-9}] < 0.463730$ |
| **3. Divisor-Aggregated $W_{\log}(X_K)$** | $-W_{\log}(X_K) = -\sum_{m \ge 1}\frac{\log m}{\sqrt{m}}h_0(m/X_K)$ on $X_K \ge 1$ | Global TV bound $\|W_{\log}(X_K)\| \le B_{\log} := \frac{30731}{98304} + M_{\tilde{h},0}^{(-3/2)} + \frac{1}{2}M_{\tilde{h},\log}^{(-3/2)}$ on $[1, \infty)$; 4th-order Euler–Maclaurin bound $\|W_{\log}(X_K)\| \le C_{\log,\mathrm{EM}}\,X_K^{-5/2} = O(X_K^{-5/2})$ ($C_{\log,\mathrm{EM}} = [13.46851 \pm 4.74\times 10^{-6}] < 13.468515$) | `TASK-TC-044` (7-root IBP global bound) + `TASK-TC-049R` (Euler–Maclaurin bound) | $B_{\log} = [3.34900801876069131272842822 \pm 5.40\times 10^{-27}] < 3.349009$ |
| **4. Head Divisor Sum $R_{\mu,\mathrm{head}}(X_K)$** | $-\sum_{2 \le m \le H(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$, $H(X_K) = \lfloor X_K^{5/6}\rfloor$ ($= 0$ for $1 \le X_K < 2^{6/5}$) | $\|R_{\mu,\mathrm{head}}(X_K)\| \le C_{\log,\mathrm{EM}} X_K^{-5/2}\sum_{2 \le m \le H(X_K)} m^2 \le C_{\log,\mathrm{EM}} X_K^{-5/2}\frac{5}{6}H(X_K)^3 \le \frac{5}{6}C_{\log,\mathrm{EM}} =: B_{\mathrm{head}}$ (**proved uniform $O(1)$ bound**, not $o(1)$ without cancellation) | `TASK-TC-049` / `TASK-TC-049R` resonant-band head reduction | $B_{\mathrm{head}} = [11.22376 \pm 5.61\times 10^{-6}] < 11.223763$ |
| **5. Super-Scale Tail $R_{\mu,\mathrm{tail}}(X_K)$** | $-\sum_{m > M(X_K)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X_K/m)$, $M(X_K) = \lceil\max(2, X_K^{5/4})\rceil$ | $\|R_{\mu,\mathrm{tail}}(X_K)\| \le C_{\log,0} X_K^{5/2}\sum_{m > M(X_K)} m^{-3} \le \frac{C_{\log,0} X_K^{5/2}}{2 M(X_K)^2} \le \frac{1}{2}C_{\log,0} =: B_{\mathrm{tail}}$ (**proved uniform $O(1)$ bound**, since $M(X_K) \ge X_K^{5/4} \implies X_K^{5/2}/M(X_K)^2 \le 1$; $C_{\log,0} = \frac{92193}{32768}(-\zeta'(3)) \approx 0.55742958$) | `TASK-TC-045` ($C_{\log,0}$ origin bound) + `TASK-TC-049`/`049R` | $B_{\mathrm{tail}} = [0.2787147935540087649401176325966251750389 \pm 2.00 \times 10^{-40}] < 0.278715$ |

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
   Each observable's ball radius reflects its analytical truncation and quadrature budget (all upper bounds rounded strictly upward):
   - $W_{\log}(X_K)$, $R_{\mu,\mathrm{head}}(X_K)$, and $R_{\mu,\mathrm{band}}(X_K)$ (evaluated by 4th-order Euler–Maclaurin on $[N_0, \infty)$): maximum Arb radii $\le 6.59 \times 10^{-11}$ (`6.5850e-11`), $\le 5.64 \times 10^{-11}$ (`5.6362e-11`), and $\le 5.65 \times 10^{-11}$ (`5.6427e-11`) across all 13 sample grades;
   - $P_\tau(K)$ (`P_tau_K_HS_orbit_certified`), $-(c_\tau^B+2)h_0(X_K)$, and $W(X_K^{-1})$: maximum Arb radii $\le 3.22 \times 10^{-22}$ (`3.2178e-22`), $\le 6.35 \times 10^{-75}$ (`6.3439e-75`), and $\le 7.02 \times 10^{-9}$ (`7.0146e-9`);
   - $C_\tau(K)$ and $E_\tau(K)$ (which include the prime-power Rosser–Schoenfeld tail on $n > 16500$ in $W(X_K)$): radii range from $\le 1.41 \times 10^{-8}$ (`1.4029e-8`) at $K = 0$ up to $\le 6.87 \times 10^{-5}$ (`6.8692e-5`) at $|K| = 2$;
   - $R_{\mu,\mathrm{tail}}(X_K)$ and $E_{\tau,\mathrm{controlled}}(K)$ (which include the direct super-scale tail remainder $\frac{C_{\log,0}X_K^{5/2}}{2\,m_{\mathrm{tail,cut}}^2}$ at $m_{\mathrm{tail,cut}} = \max(800, 25 M(X_K))$ and inner small-tail truncations): radii range from $\le 1.89 \times 10^{-5}$ (`1.8862e-5` and `1.8869e-5`) at $K = 0$ up to $\le 5.43 \times 10^{-4}$ (`5.4202e-4`) at $|K| = 2$.

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

1. **Verified Deductively in Lean 4 ([formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean), `47` definitions + `59` theorems = `106` declarations, Theorems 51–59, synchronized word-for-word in `TASK-TC-050R2`, `TASK-TC-051R`, `TASK-TC-052`, `TASK-TC-052R`, and `TASK-TC-052R2`)**:
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
     3. **Single-Step Two-Way Boundedness Transfer**: Proves `(|S_p_X| ≤ M_S ∧ |S_p_band_xp| ≤ M_S → |R_X| ≤ (1 + q) * M_S + q * (B_log + B_head + B_tail)) ∧ (|R_X| ≤ M_R ∧ |S_p_band_xp| ≤ M_S → |S_p_X| ≤ M_R + q * M_S + q * (B_log + B_head + B_tail))` (where the squarefree divisibility partition $m = pd$, the lower cutoff comparison $\lfloor H(X)/p\rfloor \le H(X/p)$, and the upper boundary bound $|\Delta_{p,\mathrm{high}}(X)| \le B_{\mathrm{tail}}$ across both cutoff orderings $M(X)/p \ge M(X/p)$ and $N - 1 < M(X)/p < N := M(X/p)$ are proved analytically outside Lean).
   - [`summation_by_parts_endpoint_bound_and_smooth_mertens_reduction`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2117-L2164) (**Theorem 55**, parameters `(R_X M_B F_B I_mertens M_cut X25 C_log_0 M_I M_R : ℝ)` with hypotheses `(h_sbp : R_X = summationByPartsDecomp M_B F_B I_mertens) (h_M_pos : 0 < M_cut) (h_X25_nonneg : 0 ≤ X25) (h_C_nonneg : 0 ≤ C_log_0) (h_mertens_triv : |M_B| ≤ M_cut) (h_F_bound : |F_B| * (M_cut ^ 3) ≤ C_log_0 * X25) (h_cutoff_dom : X25 ≤ M_cut ^ 2)`):
     1. **Unconditional Upper-Endpoint Cancellation**: Proves `|M_B * F_B| * (M_cut ^ 2) ≤ C_log_0 * X25 ∧ |M_B * F_B| ≤ C_log_0` (`summationByPartsDecomp M_B F_B I_mertens := M_B * F_B + I_mertens`);
     2. **Smooth Mertens Integral Transfer Discrepancy**: Proves `|R_X - I_mertens| ≤ C_log_0 ∧ (C_log_0 < 557430 / 1000000 → |R_X - I_mertens| < 557430 / 1000000)`;
     3. **Two-Way Reduction Between $R_X$ and $I_{\mathrm{mertens}}$**: Proves `(|I_mertens| ≤ M_I → |R_X| ≤ M_I + C_log_0) ∧ (|R_X| ≤ M_R → |I_mertens| ≤ M_R + C_log_0)` (where Stieltjes integration by parts and the termwise Euler derivative $\widetilde{W}_{\log}(u) = \frac{1}{2}W_{\log}(u) + u W_{\log}'(u)$ are proved analytically outside Lean).
   - [`iterated_prime_tower_telescoping_and_coprime_band_transfer`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2177-L2218) (**Theorem 56**, parameters `(S_0 S_1 S_2 R_0 R_1 B_0 B_1 q M_R B_rescaled : ℝ)` with hypotheses `(hq_nonneg : 0 ≤ q) (hq_lt_one : q < 1) (h_step0 : R_0 = S_0 - q * S_1 - q * B_0) (h_step1 : R_1 = S_1 - q * S_2 - q * B_1) (h_R0 : |R_0| ≤ M_R) (h_R1 : |R_1| ≤ M_R) (h_B0 : |B_0| ≤ B_rescaled) (h_B1 : |B_1| ≤ B_rescaled)`):
     1. **Two-Step Canonical-Band Inverse Tower Identity (`twoStepPrimeTowerSum`)**: For `twoStepPrimeTowerSum R_0 R_1 B_0 B_1 q S_2 := (R_0 + q * B_0) + q * (R_1 + q * B_1) + (q ^ 2) * S_2`, proves `S_0 = twoStepPrimeTowerSum R_0 R_1 B_0 B_1 q S_2`;
     2. **Two-Step Remainder Bound**: Proves `|S_0 - (q ^ 2) * S_2| ≤ (1 + q) * (M_R + q * B_rescaled)`;
     3. **Terminal Contraction Bound (`S_2 = 0`)**: Proves `S_2 = 0 → (1 - q) * |S_0| ≤ M_R + q * B_rescaled` (where induction over arbitrary finite depth $L \ge 1$ is proved analytically in §8.1–§8.2).
   - [`transition_integral_linear_density_annihilation_and_sqrt_error_bound`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2305-L2369) (**Theorem 57**, declaration name `RiemannScope.transition_integral_linear_density_annihilation_and_sqrt_error_bound`, conditional/algebraic real-inequality lemma, parameters `(I_a R_a c_a J_band T_low T_high B_lin_M B_err_M I_err C_log_EM C_log_0 B_E C_a L_tilde_W : ℝ)` with mathematical hypotheses `(hc_a_nonneg : 0 ≤ c_a) (h_Ia : I_a = linearDensityTransitionDecomp c_a J_band B_lin_M I_err) (h_Ra : R_a = (c_a * B_lin_M + B_err_M) + I_a) (h_J_tails : J_band = -T_low - T_high) (h_T_low : |T_low| ≤ (1 / 2 : ℝ) * C_log_0) (h_T_high : |T_high| ≤ (1 / 3 : ℝ) * C_log_EM) (h_B_lin : |B_lin_M| ≤ C_log_0) (h_B_err : |B_err_M| ≤ B_E) (h_I_err : |I_err| ≤ 2 * C_a * L_tilde_W)`, verified via `lake env lean --stdin` with `import RiemannScope.CanonicalThetaCorrelationBound` and `#print axioms RiemannScope.transition_integral_linear_density_annihilation_and_sqrt_error_bound` yielding `'RiemannScope.transition_integral_linear_density_annihilation_and_sqrt_error_bound' depends on axioms: [propext, Classical.choice, Quot.sound]`, `0` custom Lean axioms): Proves the algebraic cancellation of the linear boundary terms $\pm c_a B_{\mathrm{lin},M}$ in `R_a = c_a * J_band + B_err_M + I_err`, the uniform bound `|J_band| ≤ (1 / 3 : ℝ) * C_log_EM + (1 / 2 : ℝ) * C_log_0 < 4768220 / 1000000` from the assumed tail identity `J_band = -T_low - T_high`, and the conditional `O(1)` bounds on `I_a` and `R_a` from `|I_err| ≤ 2 * C_a * L_tilde_W` (including the `c_a = 0` specialization).
   - [`vaughan_band_decomposition_and_type_I_uniform_bound`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2394-L2455) (**Theorem 58**, declaration name `RiemannScope.vaughan_band_decomposition_and_type_I_uniform_bound`, conditional/algebraic real-inequality lemma, parameters `(R_band R_I R_II S_mu_U S_mu_V J_band E_EM_I B_J C_EM_1 rho_UV M_II M_R : ℝ)` with mathematical hypotheses `(h_decomp : R_band = vaughanBandDecomp R_I R_II) (h_RI : R_I = -(S_mu_U * S_mu_V * J_band) + E_EM_I) (h_BJ_nonneg : 0 ≤ B_J) (h_CEM_nonneg : 0 ≤ C_EM_1) (h_rho_nonneg : 0 ≤ rho_UV) (h_rho_le_one : rho_UV ≤ 1) (h_landau_U : |S_mu_U| ≤ 1) (h_landau_V : |S_mu_V| ≤ 1) (h_J_bound : |J_band| ≤ B_J) (h_EM_bound : |E_EM_I| ≤ C_EM_1 * rho_UV)`, verified via `lake env lean --stdin` with `import RiemannScope.CanonicalThetaCorrelationBound` and `#print axioms RiemannScope.vaughan_band_decomposition_and_type_I_uniform_bound` yielding `'RiemannScope.vaughan_band_decomposition_and_type_I_uniform_bound' depends on axioms: [propext, Classical.choice, Quot.sound]`, `0` custom Lean axioms): Proves Landau factor contraction `|S_mu_U * S_mu_V * J_band| ≤ B_J`, `|E_EM_I| ≤ C_EM_1`, and `|R_I| ≤ B_J + C_EM_1` for `0 ≤ rho_UV ≤ 1` from the supplied hypothesis `h_EM_bound : |E_EM_I| ≤ C_EM_1 * rho_UV`, two-way boundedness equivalence between `R_band = R_I + R_II` and `R_II`, the `U = V = 1, m = 4` sign-cancellation check `((-1 : ℝ) + 1 = 0 ∧ (-1 : ℝ) + (-1 : ℝ) ≠ 0)`, and the progression bounded-variation transfer `(∀ F_sup F_var inv_sqrt_X U_V : ℝ, 0 ≤ U_V → 2 * F_sup + F_var ≤ C_EM_1 * inv_sqrt_X → (2 * F_sup + F_var) * U_V ≤ C_EM_1 * (U_V * inv_sqrt_X))`.
   - [`euler_sieved_orbit_and_complete_subgate_closure_chain`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L2480-L2550) (**Theorem 59**, declaration name `RiemannScope.euler_sieved_orbit_and_complete_subgate_closure_chain`, conditional/algebraic real-inequality lemma, parameters `(C_K P_K P_y_K Delta_arch_y_K E_ctrl_K R_band_X I_X P_0 B_ctrl C_log_0 B_I N_y N_0 delta_rho : ℝ)` with mathematical hypotheses `(h_CK : C_K = canonicalCorrelationHSOrbitDecomp P_K E_ctrl_K R_band_X) (h_PK_sieve : P_K = P_y_K - Delta_arch_y_K) (h_PK_bound : |P_K| ≤ P_0) (h_E_ctrl : |E_ctrl_K| ≤ B_ctrl) (h_sbp_diff : |R_band_X - I_X| ≤ C_log_0) (h_Py_cs : |P_y_K| ≤ N_y * N_0)`, verified via `lake env lean --stdin` with `import RiemannScope.CanonicalThetaCorrelationBound` and `#print axioms RiemannScope.euler_sieved_orbit_and_complete_subgate_closure_chain` yielding `'RiemannScope.euler_sieved_orbit_and_complete_subgate_closure_chain' depends on axioms: [propext, Classical.choice, Quot.sound]`, `0` custom Lean axioms): Proves the Approach B Euler-sieved correlation decomposition `C_K = eulerSievedCorrelationDecomp P_y_K Delta_arch_y_K E_ctrl_K R_band_X` and `|P_y_K - Delta_arch_y_K| ≤ N_y * N_0 + |Delta_arch_y_K|`, the quadratic lower bound `(∀ nu_B t : ℝ, 0 ≤ nu_B → 0 ≤ nu_B + (4 * t ^ 2) / (t ^ 2 + 1 / 4) ∧ (4 * t ^ 2) / (t ^ 2 + 1 / 4) ≤ nu_B + (4 * t ^ 2) / (t ^ 2 + 1 / 4) ∧ (t ^ 2 ≤ 1 → (16 / 5 : ℝ) * t ^ 2 ≤ nu_B + (4 * t ^ 2) / (t ^ 2 + 1 / 4)))` for the repaired Plancherel multiplier $\nu(t)$, and the conditional deduction from `|I_X| ≤ B_I` to `|R_band_X| ≤ B_I + C_log_0` and `|C_K| < 21102829 / 1000000 + B_I`, whose final step applies the explicitly assumed mathematical implication `((|C_K| ≤ P_0 + B_ctrl + B_I + C_log_0 → delta_rho = 0) → delta_rho = 0)`.
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
     Writing $N := M(Y) = \lceil\max(2, Y^{5/4})\rceil \ge 2$, both orderings between $M(X)/p$ and $N = M(Y)$ occur on $X \ge p$ and are bounded explicitly:
     1. **Case 1 ($M(X)/p \ge M(Y)$)**: Here $\Delta_{p,\mathrm{high}}(X) = S_p(Y; M(Y), M(X)/p)$ sums over integers $d \in (M(Y), M(X)/p]$ with $p \nmid d$. Since every such integer satisfies $d \ge M(Y) + 1 > Y^{5/4}$, the super-scale tail bound gives
        $$
        \bigl|\Delta_{p,\mathrm{high}}(X)\bigr| \le C_{\log,0}\,Y^{5/2} \sum_{d > M(Y)} d^{-3} \le \frac{C_{\log,0}\,Y^{5/2}}{2\,M(Y)^2} \le \frac{1}{2}\,C_{\log,0} = B_{\mathrm{tail}}.
        $$
     2. **Case 2 ($M(X)/p < M(Y)$, general single-endpoint regime $N - 1 < M(X)/p < N$)**: Write $N := M(Y) = \lceil\max(2, Y^{5/4})\rceil \ge 2$. By the cutoff definitions, when $N \ge 3$ we have $N = \lceil Y^{5/4}\rceil \implies N - 1 < Y^{5/4}$, and when $N = 2$ we have $Y \ge 1 \implies N - 1 = 1 \le Y^{5/4}$. Since $M(X) \ge X^{5/4} = p^{5/4}Y^{5/4}$, we always have $M(X)/p \ge p^{1/4}Y^{5/4} > Y^{5/4} \ge N - 1$. Therefore, whenever $M(X)/p < N = M(Y)$, the cutoff definitions give
        $$
        \boxed{N - 1 < \frac{M(X)}{p} < N \qquad \bigl(N := M(Y) \ge 2\bigr).}
        $$
        Thus the omitted interval $(M(X)/p, M(Y)] = (M(X)/p, N]$ contains **only the single integer endpoint $d = N \ge 2$**. This regime occurs both when $N = 2$ (e.g. $X = 2, p = 2, Y = 1$, where $M(2) = 3, M(1) = 2, M(X)/p = 3/2 < 2$, and the endpoint $d = 2$ is filtered out by $2 \nmid d$) and when $N \ge 3$ with a surviving coprime endpoint (e.g. $X = 18/5, p = 2, Y = 9/5$, where exact integer-power comparisons $4^4 = 256 < (18/5)^5 = 1889568/3125 \le 625 = 5^4$ and $2^4 = 16 < (9/5)^5 = 59049/3125 \le 81 = 3^4$ give $M(18/5) = 5$, $N = M(9/5) = 3$, $M(X)/p = 5/2 < 3$, and the omitted endpoint $d = 3$ survives the coprime filter $2 \nmid 3$, giving $\Delta_{2,\mathrm{high}}(18/5) = +\frac{1}{\sqrt{3}}W_{\log}(3/5) = [0.0185125613290 \pm 2.58 \times 10^{-14}] \ne 0$, certified in `single_endpoint_coprime_surviving_regime_X_18_5_p2`). Since $N \ge 2$ and $Y^{5/2}/N^2 \le 1$, the single endpoint $d = N$ satisfies in all cases:
        $$
        \bigl|\Delta_{p,\mathrm{high}}(X)\bigr| \le \frac{1}{\sqrt{N}}\Bigl|W_{\log}\!\left(\frac{Y}{N}\right)\Bigr| \le \frac{C_{\log,0}\,Y^{5/2}}{N^3} = \frac{C_{\log,0}}{N}\cdot\frac{Y^{5/2}}{N^2} \le \frac{C_{\log,0}}{2} = B_{\mathrm{tail}}.
        $$
   - **Sub-Unit Regime ($1 \le X < p$, so $Y = X/p < 1$)**:
     When $1 \le X < p$, $S_{p,\mathrm{band}}(X/p) = 0$ by the sub-unit zero extension, so $B_p(X) = S_p(Y; H(X)/p, M(X)/p)$ sums over positive integers $d \ge 1$ with $Y/d \le Y < 1$, giving $|B_p(X)| \le \sum_{d \ge 1} d^{-1/2} C_{\log,0}(Y/d)^{5/2} = \zeta(3)\,C_{\log,0}\,Y^{5/2} \le \zeta(3)\,C_{\log,0} = [0.6700620832085948550527207175609300880270 \pm 2.00 \times 10^{-40}] < B_{\mathrm{rescaled}}$.
   Combining all regimes yields the **universal unconditional bound** (`Theorem 54`):
   $$
   \boxed{\forall X \ge 1,\;\forall p \in \mathcal{P}:\quad \bigl|B_p(X)\bigr| \le B_{\mathrm{rescaled}} := B_{\log} + \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [14.85148 \pm 5.09 \times 10^{-6}] < 14.851486,}
   $$
   and whenever $H(X) \ge p$:
   $$
   \boxed{\forall X \ge 1 \text{ with } H(X) \ge p:\quad \bigl|B_p(X)\bigr| \le B_{\mathrm{head}} + B_{\mathrm{tail}} = \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [11.50247 \pm 7.07 \times 10^{-6}] < 11.502478.}
   $$
3. **Canonical-Band Finite Inverse Tower and Two-Way Coprime Band Equivalence (`Theorem 56`)**:
   Rewriting the canonical-band relation at scale $X/p^j$ as $S_{p,\mathrm{band}}(X/p^j) = \bigl(R_{\mathrm{band}}(X/p^j) + q\,B_p(X/p^j)\bigr) + q\,S_{p,\mathrm{band}}(X/p^{j+1})$ and iterating over $1 \le L \le \lfloor\log_p X\rfloor + 1$ steps (so that $X/p^j \ge 1$ for all $0 \le j \le L - 1$, where $B_p$ is defined) yields the exact **canonical-band inverse tower**:
   $$
   \boxed{S_{p,\mathrm{band}}(X) = \sum_{j=0}^{L-1} q^j\Bigl(R_{\mathrm{band}}\!\left(\frac{X}{p^j}\right) + q\,B_p\!\left(\frac{X}{p^j}\right)\Bigr) + q^L\,S_{p,\mathrm{band}}\!\left(\frac{X}{p^L}\right) \qquad \bigl(1 \le L \le \lfloor\log_p X\rfloor + 1\bigr).}
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
     with the Euler product $\prod_{p \le y}(1 + p^{-1/2})$ reaching $[127804.0331068035324510388681825571283193 \pm 2.00 \times 10^{-34}]$ at $y = 997$ ($\pi(997) = 168$).
   - **Qualified Multiplicative Coset Note (`multiplicative_coset_shift_note`)**:
     Whether $\log_\tau p = \frac{\log p}{\log(2\pi)}$ lies in $\mathbb{A}_{\mathbb{R}}$ is **not assumed**; if $\log_\tau p \notin \mathbb{A}_{\mathbb{R}}$, then prime dilation $X_K \mapsto X_K / p = \tau^{|K| - \log_\tau p}$ leaves the algebraic grade locus $\tau^{\mathbb{A}_{\mathbb{R}}}$ for the multiplicative coset $p^{-1}\tau^{\mathbb{A}_{\mathbb{R}}}$, whereas all rescaled boundary bounds in §8.2 are proved on all of $\mathbb{R}_{>0}$ without assuming $\log_\tau p \in \mathbb{A}_{\mathbb{R}}$.
   - **Certified 256-bit Arb Canonical-Band Prime-Separation Table (`sample_band_prime_table` in JSON Artifact)**:

| Scale $X$ | Prime $p$ | $(H(X), M(X))$ | $(H(X/p), M(X/p))$ | Upper-Cutoff Regime | $R_{\mu,\mathrm{band}}(X)$ | $S_{p,\mathrm{band}}(X)$ | $S_{p,\mathrm{band}}(X/p)$ | Boundary Discrepancy $B_p(X)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $2$ | $(1, 2)$ | $(0, 0)$ | $X/p < 1$ (sub-unit regime) | $-0.0138854010$ | $+0.0000000000$ | $+0.0000000000$ | $+0.0196369224$ |
| $1$ | $3$ | $(1, 2)$ | $(0, 0)$ | $X/p < 1$ (sub-unit regime) | $-0.0138854010$ | $-0.0138854010$ | $+0.0000000000$ | $+0.0000000000$ |
| $2$ | $2$ | $(1, 3)$ | $(1, 2)$ | $M(X)/p < M(X/p)$ (single-endpoint regime $N - 1 < M(X)/p < N$) | $+0.0108988909$ | $-0.0202572131$ | $+0.0000000000$ | $-0.0440613848$ |
| $18/5$ | $2$ | $(2, 5)$ | $(1, 3)$ | $M(X)/p < M(X/p)$ (single-endpoint $d = 3$ surviving $2 \nmid d$) | $+0.0377277533$ | $+0.0377277533$ | $-0.0185125613$ | $+0.0185125613$ |
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
   \boxed{\bigl|M_{H(X)}(M(X))\,F_X(M(X))\bigr| \le M(X)\cdot M(X)^{-1/2}\,C_{\log,0}\!\left(\frac{X}{M(X)}\right)^{5/2} = C_{\log,0}\,\frac{X^{5/2}}{M(X)^2} \le C_{\log,0} = [0.5574295871080175298802352651932503500777 \pm 2.00 \times 10^{-40}] < 0.557430.}
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

---

## 9. Transition-Region Vanishing Moments, Linear-Density Annihilation, Vaughan Type I Uniform Bound, Euler-Sieved Positive Orbit Intertwining, Critical-Line Factorization, and Complete Conditional Closure Chain (`TASK-TC-052` / `TASK-TC-052R` / `TASK-TC-052R2`, Theorems 57–59)

In `TASK-TC-052`, `TASK-TC-052R`, and `TASK-TC-052R2` ([`execute_task_tc052_arithmetic_fourier_compatibility_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L9993-L10004)), we investigate the closing theorem for `SUBGATE-TC-043A` across both **Approach A** (signed arithmetic cancellation in the transition region) and **Approach B** (operator action of $D_p$ and $E_y$ on $\mathcal{H}_\tau^{\mathrm{pos}}$ and $L^2(\mathbb{R}_{>0}, d^\times y)$), repair the Plancherel multiplier $\nu(t)$, operator-domain completeness characterization, Vaughan Type II coefficient, Type I bounded-variation sum–integral estimate, and whole-integrand Mellin norm certifications, and formalize the conditional/algebraic reductions (`Theorems 57–59`).

### 9.1 Exact Closure Target and Rescaled Transition-Region Integral

Throughout the framework, $\tau = 2\pi$, concurrent algebraic grades $K \in \mathbb{A}_{\mathbb{R}} := \overline{\mathbb{Q}} \cap \mathbb{R}$ include both positive and negative rational and irrational algebraic grades, and $X_K := \tau^{|K|} \ge 1$ (with $|K| = \sqrt{K^2}$, so $K = 0$ is evaluated directly at $X_0 = 1$ with zero division by $K$). With the inherited cutoffs $H(X) = \lfloor X^{5/6}\rfloor$ and $M(X) = \lceil\max(2, X^{5/4})\rceil$, relative Mertens step function $\mathcal{M}_{H(X)}(t) = \sum_{H(X) < m \le t} \mu(m)$, and derivative kernel $\widetilde{W}_{\log}(u) = \frac{1}{2}W_{\log}(u) + u W_{\log}'(u) = \sum_{k \ge 2}\frac{\log k}{\sqrt{k}}\widetilde{h}_0(k/u)$, the exact closure target for `SUBGATE-TC-043A` is:
$$
\boxed{\exists B_I \ge 0\;\forall X \ge 1:\quad \bigl|I(X)\bigr| \le B_I, \qquad I(X) := \int_{H(X)}^{M(X)} \mathcal{M}_{H(X)}(t)\,t^{-3/2}\,\widetilde{W}_{\log}\!\left(\frac{X}{t}\right)dt.}
$$
Substituting $t = X u$ ($u \in [H(X)/X, M(X)/X] \sim [X^{-1/6}, X^{1/4}]$) and $v = 1/u = X/t$ ($v \in [X/M(X), X/H(X)] \sim [X^{-1/4}, X^{1/6}]$) writes $I(X)$ as a rescaled integral against a fixed smooth kernel around the transition scale $u \asymp 1$ ($t \asymp X$):
$$
\boxed{I(X) = X^{-1/2}\int_{H(X)/X}^{M(X)/X} \mathcal{M}_{H(X)}(X u)\,u^{-3/2}\,\widetilde{W}_{\log}\!\left(\frac{1}{u}\right)du = \int_{X/M(X)}^{X/H(X)} \frac{\mathcal{M}_{H(X)}(X/v)}{\sqrt{X/v}}\,v^{-1}\,\widetilde{W}_{\log}(v)\,dv.}
$$

### 9.2 Approach A: Vanishing Endpoint Moments, Linear-Density Annihilation, Nonzero Limit $L > 0$ of $J_{\mathrm{band}}(X)$ and $R_{1,\mathrm{band}}(X)$, Scope of $R_{|\mu|,\mathrm{band}}(X)$, and Reconciled Vaughan Type I Uniform Bound (`Theorems 57 & 58`)

1. **Exact Mellin Vanishing Orders of $W_{\log}(v)$ and $\widetilde{W}_{\log}(v)$ (`verify_transition_region_vanishing_moments_and_vaughan_type_I_bound_arb`)**:
   Under the `TC-045` Mellin convention $\mathcal{M}_X[F](z) := \int_0^\infty F(v)\,v^{-z}\,\frac{dv}{v}$:
   - $\mathcal{M}_X[W_{\log}](z) = -\zeta'(1/2 + z)H_0(z)$, where $H_0(z) = H_0(-z)$ has triple zeros at $z = \pm 1/2$ and $-\zeta'(1/2 + z) = \frac{1}{(z - 1/2)^2} + O(1)$ has a double pole at $z = +1/2$ ($s = 1$) and is regular with $-\zeta'(0) = \frac{1}{2}\log\tau \ne 0$ at $z = -1/2$ ($s = 0$). Thus $\mathcal{M}_X[W_{\log}](z)$ has a **simple zero at $z = +1/2$** ($\int_0^\infty v^{-3/2}W_{\log}(v)\,dv = 0$) and a **triple zero at $z = -1/2$** ($\int_0^\infty v^{-1/2}(\log v)^j W_{\log}(v)\,dv = 0$ for $j \in \{0, 1, 2\}$).
   - Integration by parts on $\widetilde{W}_{\log}(v) = \frac{1}{2}W_{\log}(v) + v W_{\log}'(v)$ gives
     $$
     \boxed{\mathcal{M}_X[\widetilde{W}_{\log}](z) = \left(\frac{1}{2} + z\right)\mathcal{M}_X[W_{\log}](z) = -\left(\frac{1}{2} + z\right)\zeta'\!\left(\frac{1}{2} + z\right)H_0(z).}
     $$
     Because the extra factor $(\frac{1}{2} + z)$ vanishes at $z = -1/2$ and equals $1 \ne 0$ at $z = +1/2$:
     - At **$z = +1/2$**: $\mathcal{M}_X[\widetilde{W}_{\log}](z)$ has a **simple zero** ($\int_0^\infty v^{-3/2}\widetilde{W}_{\log}(v)\,dv = 0$), with first logarithmic moment $\int_0^\infty v^{-3/2}(\log v)\widetilde{W}_{\log}(v)\,dv = -H_0'''(1/2)/6 = \frac{1}{512} = +0.001953125 \ne 0$.
     - At **$z = -1/2$**: $\mathcal{M}_X[\widetilde{W}_{\log}](z)$ has a **quadruple zero (order 4)**:
       $$
       \int_0^\infty v^{-1/2}(\log v)^j\,\widetilde{W}_{\log}(v)\,dv = 0 \qquad (j \in \{0, 1, 2, 3\}),
       $$
       with fourth logarithmic moment $\int_0^\infty v^{-1/2}(\log v)^4\widetilde{W}_{\log}(v)\,dv = 4(-\zeta'(0))H_0'''(-1/2) = \frac{3\log\tau}{128} \approx +0.0430752437 \ne 0$ (5 vanishing endpoint moments in total, all certified to enclose zero in 256-bit Arb).

2. **Linear-Density Annihilation, Nonzero Limit $L > 0$ of $J_{\mathrm{band}}(X)$, and Scope of $R_{|\mu|,\mathrm{band}}(X)$ (`Theorem 57`, `transition_integral_linear_density_annihilation_and_sqrt_error_bound`)**:
   Suppose a step counting function on $(H(X), M(X)]$ decomposes as $A_{H(X)}(t) = c\,(t - H(X)) + E_A(t)$ with linear density $c \in \mathbb{R}$. Integration by parts on $\frac{d}{dt}[t^{-1/2}W_{\log}(X/t)] = -t^{-3/2}\widetilde{W}_{\log}(X/t)$ gives
   $$
   \int_{H(X)}^{M(X)} c\,(t - H(X))\,t^{-3/2}\,\widetilde{W}_{\log}\!\left(\frac{X}{t}\right)dt = -c\,\bigl(M(X) - H(X)\bigr)\,M(X)^{-1/2}W_{\log}\!\left(\frac{X}{M(X)}\right) + c\,J_{\mathrm{band}}(X),
   $$
   where, by the vanishing moment $\mathcal{M}_X[W_{\log}](1/2) = \int_0^\infty v^{-3/2}W_{\log}(v)\,dv = 0$, the smooth linear-density integral $J_{\mathrm{band}}(X) := \int_{H(X)}^{M(X)} t^{-1/2}W_{\log}(X/t)\,dt = X^{1/2}\int_{X/M(X)}^{X/H(X)} v^{-3/2}W_{\log}(v)\,dv$ equals the negative sum of its two exterior tails:
   $$
   \boxed{J_{\mathrm{band}}(X) = -T_{\mathrm{low}}(X) - T_{\mathrm{high}}(X), \qquad T_{\mathrm{low}}(X) := X^{1/2}\int_0^{X/M(X)} v^{-3/2}W_{\log}(v)\,dv, \qquad T_{\mathrm{high}}(X) := X^{1/2}\int_{X/H(X)}^\infty v^{-3/2}W_{\log}(v)\,dv,}
   $$
   satisfying for all $X \ge 1$:
   $$
   \boxed{\bigl|T_{\mathrm{high}}(X)\bigr| \le \frac{1}{3}C_{\log,\mathrm{EM}}\,X^{1/2}\!\left(\frac{X}{H(X)}\right)^{-3} \le \frac{1}{3}C_{\log,\mathrm{EM}}, \qquad \bigl|T_{\mathrm{low}}(X)\bigr| \le \frac{1}{2}C_{\log,0}\,X^{1/2}\!\left(\frac{X}{M(X)}\right)^2 \le \frac{1}{2}C_{\log,0},}
   $$
   $$
   \boxed{\bigl|J_{\mathrm{band}}(X)\bigr| \le B_J := \frac{1}{3}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} = [4.76822 \pm 3.45 \times 10^{-6}] < 4.768220.}
   $$
   Furthermore, if the remainder satisfies $|E_A(t)| \le C_E\,t^{1/2}$, then $\bigl|\int_{H(X)}^{M(X)} (E_A(t) - E_A(H(X))) t^{-3/2}\widetilde{W}_{\log}(X/t)\,dt\bigr| \le 2 C_E\int_0^\infty v^{-1}|\widetilde{W}_{\log}(v)|\,dv < \infty$ is unconditionally $O(1)$.
   - **Exact Small-Argument Sign, Nonzero Limit $\lim_{X\to\infty} J_{\mathrm{band}}(X) = L > 0$, and Asymptotic Scope of $R_{|\mu|,\mathrm{band}}(X)$ (`TASK-TC-052R` & `TASK-TC-052R2`)**:
     - As $v \to 0^+$, since $h_0(\alpha) = -\frac{81}{64}\alpha^{-5/2} + O(\alpha^{-9/2})$ ($\alpha = k/v \to \infty$) and $-\zeta'(3) = \sum_{k=2}^\infty k^{-3}\log k > 0$ ($\zeta'(3) \approx -0.19812624 < 0$), we have:
       $$
       \boxed{W_{\log}(v) = \frac{81\zeta'(3)}{64}\,v^{5/2} + O(v^{9/2}) = -\frac{81\bigl[-\zeta'(3)\bigr]}{64}\,v^{5/2} + O(v^{9/2}) < 0 \qquad (v \to 0^+).}
       $$
     - Combined with $W_{\log}(v) = -\frac{81\zeta(3)}{256\pi^2}v^{-5/2} + O(v^{-7/2})$ as $v \to \infty$ (`TC-049R`), **both** cutoffs $H(X) = \lfloor X^{5/6}\rfloor = X^{5/6} + O(1)$ (floor cutoff-rounding perturbation $O(X^{-5/6})$ since $(X/H(X))^{-3} = X^{-1/2}(1 + O(X^{-5/6}))$) and $M(X) = \lceil\max(2, X^{5/4})\rceil = X^{5/4} + O(1)$ (ceiling cutoff-rounding perturbation $O(X^{-5/4})$ since $(X/M(X))^2 = X^{-1/2}(1 + O(X^{-5/4}))$) contribute strictly positive $O(1)$ limits to $J_{\mathrm{band}}(X) = -T_{\mathrm{low}}(X) - T_{\mathrm{high}}(X)$ as $X \to \infty$:
       - Upper-$v$ tail ($m \le H(X) \sim X^{5/6}$): $-T_{\mathrm{high}}(X) \to \frac{81\zeta(3)}{256\pi^2}\cdot\frac{1}{3} = \frac{27\zeta(3)}{256\pi^2} = [+0.01284544282150966111041861441751842139795 \pm 2.00 \times 10^{-41}]$.
       - Lower-$v$ tail ($m > M(X) \sim X^{5/4}$): $-T_{\mathrm{low}}(X) \to \frac{81[-\zeta'(3)]}{64}\cdot\frac{1}{2} = \frac{81[-\zeta'(3)]}{128} = [+0.1253767630760670712483220901700480433353 \pm 2.00 \times 10^{-40}]$.
       - Consequently, $J_{\mathrm{band}}(X)$ does **not** vanish as $X \to \infty$; instead both $J_{\mathrm{band}}(X)$ and $R_{1,\mathrm{band}}(X) = J_{\mathrm{band}}(X) + O(X^{-1/2})$ converge unconditionally to:
         $$
         \boxed{\lim_{X \to \infty} J_{\mathrm{band}}(X) = \lim_{X \to \infty} R_{1,\mathrm{band}}(X) = L := \frac{27\zeta(3)}{256\pi^2} + \frac{81\bigl[-\zeta'(3)\bigr]}{128} = [+0.1382222058975767323587407045875664647333 \pm 2.00 \times 10^{-40}] > 0.}
         $$
     - For the squarefree indicator $a_m = |\mu(m)| = \mu(m)^2$, the elementary squarefree sieve $Q(t) = \sum_{d \le \sqrt{t}}\mu(d)\lfloor t/d^2\rfloor = \frac{6}{\pi^2}t + E_Q(t)$ gives the elementary bound $|E_Q(t)| \le 2\sqrt{t}$, which proves **unconditional uniform $O(1)$ boundedness** on $[1, \infty)$:
       $$
       \boxed{R_{|\mu|,\mathrm{band}}(X) = \frac{6}{\pi^2}J_{\mathrm{band}}(X) + O(1), \qquad \sup_{X \ge 1}\bigl|R_{|\mu|,\mathrm{band}}(X)\bigr| \le \frac{6}{\pi^2}B_J + B_{E,Q} + 4 L_{\widetilde{W}} < \infty.}
       $$
       Pointwise convergence $\lim_{X \to \infty} R_{|\mu|,\mathrm{band}}(X) = \frac{6}{\pi^2}L = [+0.08402902504318437033701087820794188618435 \pm 2.00 \times 10^{-41}]$ requires the stronger error bound $E_Q(t) = o(\sqrt{t})$ as $t \to \infty$ (known unconditionally in analytic number theory via Walfisz / exponential sums, e.g. $E_Q(t) = O(t^{1/2}\exp(-c(\log t)^{3/5}(\log\log t)^{-1/5}))$, whereas elementary $O(\sqrt{t})$ alone establishes $O(1)$ boundedness).

3. **Reconciled Vaughan Identity on the Resonant Band and Derivative-Based Type I Uniform Bound (`Theorem 58`, `vaughan_band_decomposition_and_type_I_uniform_bound`, `TASK-TC-052R` & `TASK-TC-052R2`)**:
   - **Exact Combinatorial Divisor Identity and $U = V = 1, m = 4$ Regression**:
     For any parameters $U, V \ge 1$ and any integer $m > \max(U, V)$, writing $m = a b$ and partitioning divisors $r \mid b$ into $r \le V$ and $r > V$ gives $\sum_{r \mid b}\mu(r) = \mathbf{1}_{b=1} = 0$ whenever $b > V \ge 1$, so
     $$
     \sum_{\substack{r \mid b \\ r > V}} \mu(r) = -\sum_{\substack{r \mid b \\ r \le V}} \mu(r) \qquad (\forall b > V \ge 1).
     $$
     Therefore, throughout the resonant band $m > H(X) \ge \max(U, V)$, $\mu(m)$ decomposes identically as
     $$
     \boxed{\mu(m) = c_{\mathrm{I}}(m; U, V) + c_{\mathrm{II}}(m; U, V) \qquad \bigl(m > \max(U, V)\bigr),}
     $$
     $$
     \boxed{c_{\mathrm{I}}(m; U, V) := -\sum_{\substack{d r n = m \\ d \le U,\; r \le V}} \mu(d)\mu(r), \qquad c_{\mathrm{II}}(m; U, V) := \sum_{\substack{a b = m \\ a > U,\; b > V}} \mu(a)\sum_{\substack{r \mid b \\ r > V}} \mu(r) = -\sum_{\substack{a b = m \\ a > U,\; b > V}} \mu(a)\sum_{\substack{r \mid b \\ r \le V}} \mu(r).}
     $$
     *Exact regression at $U = V = 1, m = 4$*: Here $c_{\mathrm{I}}(4; 1, 1) = -\mu(1)\mu(1) = -1$ ($d = 1, r = 1, n = 4$), and the unique pair $(a, b)$ with $a b = 4, a > 1, b > 1$ is $(2, 2)$ ($\mu(2) = -1$). Under the corrected formula, $\sum_{r \mid 2, r > 1}\mu(r) = \mu(2) = -1 = -\sum_{r \mid 2, r \le 1}\mu(r) = -\mu(1)$, giving $c_{\mathrm{II}}(4; 1, 1) = (-1)(-1) = +1$ and $c_{\mathrm{I}}(4; 1, 1) + c_{\mathrm{II}}(4; 1, 1) = -1 + 1 = 0 = \mu(4)$. By contrast, the un-negated $r \le V$ inner sum gives $(-1)(+1) = -1$ and $-1 + (-1) = -2 \ne \mu(4) = 0$.
   - **Admissibility of $U = V = \lfloor X^{1/4}\rfloor$ Across All $X \ge 1$**:
     For $U = V = \lfloor X^{1/4}\rfloor \ge 1$:
     - Since $X \ge 1 \implies X^{1/4} \le X^{5/6}$, monotony of the floor function directly gives $U = V = \lfloor X^{1/4}\rfloor \le \lfloor X^{5/6}\rfloor = H(X)$, and $\lfloor X^{1/4}\rfloor \le X^{1/4}$ gives $U V = \lfloor X^{1/4}\rfloor^2 \le \sqrt{X}$ across all $X \ge 1$ (in particular, when $1 \le X < 16$, $U = V = 1 \le H(X)$ and $U V = 1 \le \sqrt{X}$; when $X \ge 16$, $U = V = \lfloor X^{1/4}\rfloor \le X^{1/4} \le X^{5/6} - 1 < \lfloor X^{5/6}\rfloor = H(X)$).
   - **Derivative-Based Bounded-Variation Estimate on $F_X(t) = t^{-1/2}W_{\log}(X/t)$ and Progression Sum–Integral Discrepancy Bound (`type_I_progression_bounded_variation_theorem`)**:
     For $F_X(t) = t^{-1/2}W_{\log}(X/t) = X^{-1/2}f(X/t)$ with $f(v) := v^{1/2}W_{\log}(v)$, we have $F_X'(t) = -t^{-3/2}\widetilde{W}_{\log}(X/t)$. Under the substitution $v = X/t \in (0, \infty)$ ($t = X/v$, $dt = X v^{-2}\,dv$, so $t^{-3/2}\,dt = X^{-1/2} v^{-1/2}\,dv$),
     $$
     \boxed{\|F_X\|_{\infty,(0,\infty)} = X^{-1/2}\|f\|_{\infty,(0,\infty)} = X^{-1/2}\sup_{v > 0}\bigl(v^{1/2}|W_{\log}(v)|\bigr), \qquad \operatorname{Var}_{(0,\infty)}(F_X) = \int_0^\infty |F_X'(t)|\,dt = X^{-1/2}\int_0^\infty v^{-1/2}\bigl|\widetilde{W}_{\log}(v)\bigr|\,dv.}
     $$
     1. *Small-$v$ regime $v \in (0, 1]$*: From $|h_0(\alpha)| \le C_0 \alpha^{-5/2}$ ($C_0 = \frac{92193}{32768}$) and $|\widetilde{h}_0(\alpha)| \le \widetilde{C}_0 \alpha^{-5/2}$ ($\widetilde{C}_0 = \frac{10329937}{655360}$), we have $|W_{\log}(v)| \le C_{\log,0} v^{5/2}$ and $|\widetilde{W}_{\log}(v)| \le \widetilde{C}_{\log,0} v^{5/2}$ with $\widetilde{C}_{\log,0} := \widetilde{C}_0(-\zeta'(3)) = [3.122911998070261993078893101767253989745 \pm 2.00 \times 10^{-39}]$, giving $\sup_{v \in (0,1]}(v^{1/2}|W_{\log}(v)|) \le C_{\log,0} = [0.5574295871080175298802352651932503500777 \pm 2.00 \times 10^{-40}]$ and
        $$
        \operatorname{Var}_{(0,1]}(f) = \int_0^1 v^{-1/2}\bigl|\widetilde{W}_{\log}(v)\bigr|\,dv \le \widetilde{C}_{\log,0}\int_0^1 v^2\,dv = \frac{1}{3}\widetilde{C}_{\log,0} = \bigl[1.040970666023420664359631033922417996582 \pm 2.00 \times 10^{-39}\bigr].
        $$
     2. *Large-$v$ regime $v \in [1, \infty)$*: By $|W_{\log}(v)| \le C_{\log,\mathrm{EM}} v^{-5/2}$, $\sup_{v \ge 1}(v^{1/2}|W_{\log}(v)|) \le C_{\log,\mathrm{EM}} = [13.46851 \pm 4.74 \times 10^{-6}]$. For $\widetilde{W}_{\log}(v) = \sum_{k=2}^\infty (\log k)\widetilde{g}_v(k)$ with $\widetilde{g}_v(k) := v^{-1/2}\widetilde{\psi}_0(k/v)$ and $\widetilde{\psi}_0(\alpha) := \alpha^{-1/2}\widetilde{h}_0(\alpha) = -\alpha\psi_0'(\alpha)$, the vanishing integral $\int_0^\infty x^{-1/2}(\log x)\widetilde{h}_0(x/v)\,dx = 0$ (since $\int_0^\infty \widetilde{\psi}_0(\alpha)\,d\alpha = [-\alpha\psi_0(\alpha)]_0^\infty + \int_0^\infty \psi_0(\alpha)\,d\alpha = 0$ and $\int_0^\infty (\log\alpha)\widetilde{\psi}_0(\alpha)\,d\alpha = [-\alpha(\log\alpha)\psi_0(\alpha)]_0^\infty + \int_0^\infty (1 + \log\alpha)\psi_0(\alpha)\,d\alpha = 0$) and the exact rational Bernstein bounds $|\widetilde{\psi}_0(\alpha)| \le C_0^{\tilde{\psi}}\alpha^2(1+\alpha^2)^{-5/2}$ ($C_0^{\tilde{\psi}} = \frac{8340237}{3584}$), $|\widetilde{\psi}_0'(\alpha)| \le C_1^{\tilde{\psi}}\alpha(1+\alpha^2)^{-5/2}$ ($C_1^{\tilde{\psi}} = \frac{95924679}{4096}$), and $|\widetilde{\psi}_0''(\alpha)| \le C_2^{\tilde{\psi}}(1+\alpha^2)^{-5/2}$ ($C_2^{\tilde{\psi}} = \frac{132825555}{512}$) yield via the 2nd-order Euler–Maclaurin identity on $[1, \infty)$ the explicit pointwise estimate for all $v \ge 1$:
        $$
        \bigl|\widetilde{W}_{\log}(v)\bigr| \le \frac{7}{36}\widetilde{C}_0\,v^{-5/2} + \bigl(\widetilde{A}_1 + \widetilde{A}_2\log v\bigr)\,v^{-3/2} \qquad (v \ge 1), \qquad \widetilde{A}_1 := \frac{C_0^{\tilde{\psi}} + 2 C_1^{\tilde{\psi}}}{18} + \frac{17 C_2^{\tilde{\psi}}}{192} = \frac{17685797581}{688128}, \qquad \widetilde{A}_2 := \frac{C_2^{\tilde{\psi}}}{18} = \frac{132825555}{9216} = \frac{14758395}{1024}.
        $$
        Integrating $v^{-1/2}\bigl|\widetilde{W}_{\log}(v)\bigr|$ over $v \in [1, \infty)$ using $\int_1^\infty v^{-3}\,dv = \frac{1}{2}$, $\int_1^\infty v^{-2}\,dv = 1$, and $\int_1^\infty v^{-2}\log v\,dv = 1$ gives directly:
        $$
        \operatorname{Var}_{[1,\infty)}(f) = \int_1^\infty v^{-1/2}\bigl|\widetilde{W}_{\log}(v)\bigr|\,dv \le \frac{7}{72}\widetilde{C}_0 + \widetilde{A}_1 + \widetilde{A}_2 = \bigl[40115.34705084240625775049603174603174603 \pm 2.00 \times 10^{-35}\bigr].
        $$
     3. *Total variation $V_f$, single-interval BV constant $C_{\mathrm{BV}}$, and progression sum–integral discrepancy constant $C_{\mathrm{EM,I}}$*:
        Combining the two regimes gives
        $$
        \begin{aligned}
        V_f &:= \operatorname{Var}_{(0,\infty)}(f) \le \frac{1}{3}\widetilde{C}_{\log,0} + \frac{7}{72}\widetilde{C}_0 + \widetilde{A}_1 + \widetilde{A}_2 = \bigl[40116.38802150842967841485566277995416403 \pm 2.00 \times 10^{-35}\bigr], \\
        C_{\mathrm{BV}} &:= \|f\|_{\infty,(0,\infty)} + V_f = C_{\log,\mathrm{EM}} + V_f = \bigl[40129.85653 \pm 6.24 \times 10^{-6}\bigr] < 40130.0, \\
        C_{\mathrm{EM,I}} &:= 2\|f\|_{\infty,(0,\infty)} + V_f = 2 C_{\log,\mathrm{EM}} + V_f = \bigl[40143.3250 \pm 5.10 \times 10^{-5}\bigr] < 40148.0.
        \end{aligned}
        $$
        For any arithmetic progression $m = q n$ ($q = d r \ge 1$) on $(A_q, B_q] := (H(X)/q, M(X)/q]$, comparing each integer step against its unit interval gives (accounting for both fractional boundary intervals at $A_q$ and $B_q$)
        $$
        \Biggl|\sum_{A_q < n \le B_q} F_X(q n) - \int_{A_q}^{B_q} F_X(q y)\,dy\Biggr| \le 2\|F_X\|_{\infty,(0,\infty)} + \operatorname{Var}_{(0,\infty)}(F_X) \le C_{\mathrm{EM,I}}\,X^{-1/2}
        $$
        uniformly in $q = d r \ge 1$. Since $F_X(d r\,n) = (d r\,n)^{-1/2}W_{\log}(X/(d r\,n))$ already contains the $(dr)^{-1/2}$ weight, the outer coefficient is $-\mu(d)\mu(r)$ with $|\mu(d)\mu(r)| \le 1$; multiplying by $|\mu(d)\mu(r)| \le 1$ and summing over the $U V$ pairs $(d, r) \in [1, U] \times [1, V]$ yields:
        $$
        \boxed{R_{\mathrm{I}}(X; U, V) = \alpha_{\mathrm{I}}(U, V)\,J_{\mathrm{band}}(X) + E_{\mathrm{EM,I}}(X; U, V), \qquad \bigl|E_{\mathrm{EM,I}}(X; U, V)\bigr| \le C_{\mathrm{EM,I}}\,\frac{U V}{\sqrt{X}} \le C_{\mathrm{EM,I}},}
        $$
        and hence (`Theorem 58`):
        $$
        \boxed{\bigl|R_{\mathrm{I}}(X; U, V)\bigr| \le B_J + C_{\mathrm{EM,I}} = \bigl[40148.0933 \pm 5.15 \times 10^{-5}\bigr] < 40152.70 = O(1) \qquad (\forall X \ge 1,\; U V \le \sqrt{X},\; \max(U, V) \le H(X)),}
        $$
        reducing `SUBGATE-TC-043A` unconditionally to uniform $O(1)$ boundedness of the **Vaughan Type II bilinear sum** $R_{\mathrm{II}}(X; U, V)$:

| Scale $X$ | Cutoffs $(H, M)$ | $(U, V)$ | $R_{\mu,\mathrm{band}}(X)$ | Vaughan Type I $R_{\mathrm{I}}(X; U, V)$ | Exchanged Type I $R_{\mathrm{I}}^{\mathrm{exch}}(X; U, V)$ | Vaughan Type II $R_{\mathrm{II}}(X; U, V)$ | $R_{1,\mathrm{band}}(X)$ | $R_{\|\mu\|,\mathrm{band}}(X)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $(1, 2)$ | $(1, 1)$ | $-0.0138854010$ | $-0.0138854010$ | $-0.0138854010$ | $0$ | $+0.0138854010$ | $+0.0138854010$ |
| $2$ | $(1, 3)$ | $(1, 1)$ | $+0.0108988909$ | $+0.0108988909$ | $+0.0108988909$ | $0$ | $-0.0108988909$ | $-0.0108988909$ |
| $4$ | $(3, 6)$ | $(1, 1)$ | $+0.0053844056$ | $-0.0012329276$ | $-0.0012329276$ | $+0.0066173331$ | $+0.0012329276$ | $+0.0232636200$ |
| $\tau$ | $(4, 10)$ | $(1, 1)$ | $+0.0305137548$ | $+0.0380922306$ | $+0.0380922306$ | $-0.0075784758$ | $-0.0380922306$ | $-0.0576692464$ |
| $10$ | $(6, 18)$ | $(1, 1)$ | $+0.0163613434$ | $+0.0482983844$ | $+0.0482983844$ | $-0.0319370410$ | $-0.0482983844$ | $-0.0083864514$ |
| $16$ | $(10, 32)$ | $(2, 2)$ | $+0.0050456338$ | $+0.0216387455$ | $+0.0216387455$ | $-0.0165931117$ | $-0.0477730902$ | $-0.0448539391$ |
| $\tau^2$ | $(21, 99)$ | $(2, 2)$ | $+0.0094869970$ | $+0.0174219455$ | $+0.0174219455$ | $-0.0079349485$ | $-0.0373670566$ | $-0.0343474534$ |
| $64$ | $(32, 182)$ | $(2, 2)$ | $+0.0305914155$ | $+0.0024411914$ | $+0.0024411914$ | $+0.0281502241$ | $-0.0158336588$ | $+0.0190489418$ |

### 9.3 Approach B: Euler-Sieved Positive Orbit Intertwining, Operator-Domain Non-Completeness, Certified Critical-Line Spectral–Dirichlet Factorization, and Coherent Low-Frequency Euler Spike Obstruction (`Theorem 59`, `TASK-TC-052R` & `TASK-TC-052R2`)

1. **Intertwining of $D_p$ and $E_y$ on $\mathcal{H}_\tau^{\mathrm{pos}}$, Operator-Domain Non-Completeness, Reconciled Shift Convention $+ \log_\tau m$, and Boundedness of $P_{\tau,y}(K)$ (`Theorem 59`)**:
   On $\mathcal{H}_\tau^{\mathrm{pos}} = \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y)$ with $\mathcal{J}_\tau(f) := (A_\tau^B f, 2 R_0 f)$ on $\mathcal{D}(\mathcal{J}_\tau) = \{f \in L^2(\mathbb{R}_{>0}, d^\times y) : \int_{-\infty}^\infty \nu(t)|\widehat{f}(t)|^2\,dt < \infty\}$, $(\mathcal{D}(\mathcal{J}_\tau), \|\mathcal{J}_\tau \cdot\|_{\mathcal{H}_\tau^{\mathrm{pos}}})$ is an **inner-product space that is not complete** (since $\nu(t) \asymp t^2$ as $t \to 0$) and $\mathcal{J}_\tau$ is an **isometric embedding of this inner-product space** into $\mathcal{H}_\tau^{\mathrm{pos}}$. Prime dilation $(D_p f)(y) := f(y/p) = f(\tau^{-\log_\tau p} y) = (T_{\log_\tau p} f)(y)$ is unitary on $L^2(\mathbb{R}_{>0}, d^\times y)$ and satisfies $(D_p T_K f)(y) = f(\tau^{-(K + \log_\tau p)} y) = (T_{K + \log_\tau p} f)(y)$, while commuting with both $(A_\tau^B f)(x, y) = f(y) - f(y/x)$ and $(R_0 f)(y) = \int_0^y (t/y)^{1/2}(Df)(t)\frac{dt}{t}$. Thus for $E_y := \prod_{p \le y}(I - p^{-1/2}D_p) = \sum_{m \mid P_y}\frac{\mu(m)}{\sqrt{m}}T_{\log_\tau m}$,
   $$
   \boxed{A_\tau^B(E_y f) = E_y^B(A_\tau^B f), \qquad R_0(E_y f) = E_y(R_0 f), \qquad \mathcal{J}_\tau(E_y f) = (E_y^B \oplus E_y)\mathcal{J}_\tau(f), \qquad \mathcal{U}_K\mathcal{J}_\tau(E_y f) = \mathcal{J}_\tau(E_y T_K f).}
   $$
   Defining the asymmetric Euler-sieved orbit pairing $P_{\tau,y}(K) := \langle \mathcal{U}_K\mathcal{J}_\tau(E_y\psi_\tau), \mathcal{J}_\tau(\psi_\tau)\rangle_{\mathcal{H}_\tau^{\mathrm{pos}}}$, linearity and $(D_m T_K\psi_\tau) = T_{K + \log_\tau m}\psi_\tau$ give the reconciled shift formula (which also equals $\sum_{m \mid P_y}\frac{\mu(m)}{\sqrt{m}}P_\tau(K - \log_\tau m)$ at $K = 0$ by evenness $P_\tau(-u) = P_\tau(u)$):
   $$
   \boxed{P_{\tau,y}(K) = \sum_{m \mid P_y}\frac{\mu(m)}{\sqrt{m}}\,P_\tau\bigl(K + \log_\tau m\bigr), \qquad \Delta_{\mathrm{arch},y}(K) := P_{\tau,y}(K) - P_\tau(K) = \sum_{\substack{m \mid P_y \\ m \ge 2}}\frac{\mu(m)}{\sqrt{m}}\,P_\tau\bigl(K + \log_\tau m\bigr).}
   $$
   By Cauchy–Schwarz on $\mathcal{H}_\tau^{\mathrm{pos}}$, for every fixed $y \ge 2$ and all $K \in \mathbb{R}$:
   $$
   \boxed{\bigl|P_{\tau,y}(K)\bigr| \le \|\mathcal{J}_\tau(E_y\psi_\tau)\|_{\mathcal{H}_\tau^{\mathrm{pos}}}\sqrt{P_\tau(0)}, \qquad C_\tau(K) = P_{\tau,y}(K) - \Delta_{\mathrm{arch},y}(K) + E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|}),}
   $$
   certified to enclose zero for $y \in \{2, 3\}$ and $K \in \{0, 1\}$ in `sieve_orbit_verification_table`.

2. **Unconditional Critical-Line Spectral–Dirichlet Factorization of $R_{\mu,\mathrm{band}}(X)$ and Proved Whole-Integrand Mellin Certification (`TASK-TC-052R` & `TASK-TC-052R2`)**:
   Unlike $\mathcal{M}_X[W](z) = -\frac{\zeta'(1/2+z)}{\zeta(1/2+z)}H_0(z)$ (whose contour shift to $\operatorname{Re}(z) = 0$ crosses poles at nontrivial zeros of $\zeta$), $\mathcal{M}_X[W_{\log}](z) = -\zeta'(1/2 + z)H_0(z)$ is holomorphic across the entire open strip $-5/2 < \operatorname{Re}(z) < 5/2$ (`TC-045`). Shifting the Mellin inversion contour of $W_{\log}(X/m)$ from $\operatorname{Re}(z) = 1$ to the critical line $\operatorname{Re}(z) = 0$ ($z = it$) crosses **zero poles** and yields the exact unconditional factorization:
   $$
   \boxed{R_{\mu,\mathrm{band}}(X) = \int_{-\infty}^\infty \Omega_{\log}(t)\,M_{\mathrm{band}}\!\left(\frac{1}{2} + it;\, X\right) X^{it}\,dt, \qquad \Omega_{\log}(t) := -\frac{1}{\tau}\zeta'\!\left(\frac{1}{2} + it\right)H_0(it), \qquad M_{\mathrm{band}}(s; X) := \sum_{H(X) < m \le M(X)} \frac{\mu(m)}{m^s}.}
   $$
   - **Proved One-Sided and Two-Sided Whole-Integrand Infinite-Tail Bounds at $T = 48$ (`TASK-TC-052R` & `TASK-TC-052R2`)**:
     1. *Exact canonical archimedean identity*: At $s = 1/2 + it$, $s(s-1) = (\frac{1}{2} + it)(-\frac{1}{2} + it) = -(t^2 + 1/4)$, so $F_\tau(1/2 + it) = \frac{s^2(s-1)^2}{32}\pi^{-s/2}\Gamma(s/2)\big|_{s=1/2+it} = \frac{(t^2 + 1/4)^2}{32}\pi^{-1/4 - it/2}\Gamma(1/4 + it/2)$ and (`h0_crit_poly_identity_verified: true` in SymPy)
        $$
        \boxed{H_0(it) = \bigl|F_\tau(1/2 + it)\bigr|^2 = \frac{(t^2 + 1/4)^4}{1024\sqrt{\pi}}\,\Bigl|\Gamma\!\left(\frac{1}{4} + \frac{it}{2}\right)\Bigr|^2.}
        $$
        By the Euler–Weierstrass product for $\Gamma$, $\bigl|\frac{\Gamma(1/4 + it/2)}{\Gamma(1/4)}\bigr|^2 = \prod_{n=0}^\infty \bigl(1 + \frac{t^2}{4(n+1/4)^2}\bigr)^{-1} \le \prod_{n=0}^\infty \bigl(1 + \frac{t^2}{4(n+1/2)^2}\bigr)^{-1} = \bigl|\frac{\Gamma(1/2 + it/2)}{\Gamma(1/2)}\bigr|^2 = \frac{1}{\cosh(\pi t/2)} \le 2 e^{-\pi|t|/2}$ for all $t \in \mathbb{R}$, giving $H_0(it) \le \frac{\Gamma(1/4)^2}{512\sqrt{\pi}}(t^2 + 1/4)^4 e^{-\pi|t|/2}$.
     2. *Explicit critical-line growth bound on $|\zeta'(1/2 + it)|$*: By the 1st-order centered Euler–Maclaurin representation at $N = 1$ on $\operatorname{Re}(s) > 0$, $\zeta'(s) = -\frac{1}{(s-1)^2} + \int_1^\infty \left(\{x\} - \frac{1}{2}\right)(s\log x - 1)x^{-s-1}\,dx$, so at $s = 1/2 + it$ (since $|\{x\} - 1/2| \le 1/2$, $\int_1^\infty x^{-3/2}\log x\,dx = 4$, and $\int_1^\infty x^{-3/2}\,dx = 2$), $|\zeta'(1/2 + it)| \le (t^2 + 1/4)^{-1} + \frac{1}{2}\bigl(4\sqrt{t^2 + 1/4} + 2\bigr) = 2\sqrt{t^2 + 1/4} + 1 + (t^2 + 1/4)^{-1} \le 4(t^2 + 1/4)$ for all $|t| \ge 1$.
     3. *One-sided infinite-tail bounds $B_{\Omega,j}^{\mathrm{tail}}(T)$ on $[T, \infty)$ and two-sided tail bounds on $|t| \ge T$ ($T = 48$)*: Consequently, for $|t| \ge 1$, $|\Omega_{\log}(t)| \le C_\Omega (t^2 + 1/4)^5 e^{-\pi|t|/2}$ with $C_\Omega := \frac{\Gamma(1/4)^2}{128\tau\sqrt{\pi}} = \frac{\Gamma(1/4)^2}{256\pi^{3/2}}$. Since for $t \ge T = 48$, $\frac{d}{dt}[(t^2 + 1/4)^5] / [\frac{\pi}{2}(t^2 + 1/4)^5] = \frac{20 t}{\pi(t^2 + 1/4)} \le \frac{1}{2}$, integration by parts gives $\int_T^\infty (t^2 + 1/4)^5 e^{-\pi t/2}\,dt \le \frac{4}{\pi}(T^2 + 1/4)^5 e^{-\pi T/2}$ and $\int_T^\infty (t^2 + 1/4)^{10} e^{-\pi t}\,dt \le \frac{2}{\pi}(T^2 + 1/4)^{10} e^{-\pi T}$. We define $B_{\Omega,1}^{\mathrm{tail}}(T)$ and $B_{\Omega,2}^{\mathrm{tail}}(T)$ consistently as **one-sided** tail bounds on $[T, \infty)$:
        $$
        \boxed{\int_T^\infty |\Omega_{\log}(t)|\,dt \le B_{\Omega,1}^{\mathrm{tail}}(T) := \frac{4}{\pi}C_\Omega(T^2 + 1/4)^5 e^{-\pi T/2} = \frac{\Gamma(1/4)^2}{32\pi^{3/2}\tau}(T^2 + 1/4)^5 e^{-\pi T/2},}
        $$
        $$
        \boxed{\int_T^\infty |\Omega_{\log}(t)|^2\,dt \le B_{\Omega,2}^{\mathrm{tail}}(T) := \frac{2}{\pi}C_\Omega^2(T^2 + 1/4)^{10} e^{-\pi T} = \frac{\Gamma(1/4)^4}{8192\pi^2\tau^2}(T^2 + 1/4)^{10} e^{-\pi T},}
        $$
        which evaluate at $T = 48$ to $B_{\Omega,1}^{\mathrm{tail}}(48) = [1.371901664348456727857448422465050864052 \times 10^{-18} \pm 2.00 \times 10^{-57}] \le 1.3720 \times 10^{-18}$ and $B_{\Omega,2}^{\mathrm{tail}}(48) = [7.391045088194894744725557492971802729825 \times 10^{-37} \pm 2.00 \times 10^{-76}] \le 7.3911 \times 10^{-37}$. By evenness $|\Omega_{\log}(-t)| = |\Omega_{\log}(t)|$:
        - The **two-sided** $L^1$ norm tail on $|t| \ge T$ is bounded by $2 B_{\Omega,1}^{\mathrm{tail}}(T)$;
        - The **two-sided** squared-$L^2$ norm tail on $|t| \ge T$ is bounded by $2 B_{\Omega,2}^{\mathrm{tail}}(T)$, and $\|\Omega_{\log}\|_{L^2(\mathbb{R})}$ is obtained after enclosing $\int_{-T}^T |\Omega_{\log}(t)|^2\,dt$ plus $[-2 B_{\Omega,2}^{\mathrm{tail}}(T), +2 B_{\Omega,2}^{\mathrm{tail}}(T)]$ and taking the square root;
        - For each scale $X$, since $|M_{\mathrm{band}}(1/2 + it; X) X^{it}| \le A_X := \sum_{H(X) < m \le M(X)} |\mu(m)| m^{-1/2}$ for all $t \in \mathbb{R}$, the **two-sided** omitted tail of $R_{\mu,\mathrm{band}}(X)$ on $|t| \ge 48$ is bounded rigorously by $2 A_X B_{\Omega,1}^{\mathrm{tail}}(48)$;
        - **Why $2 B_{\Omega,1}^{\mathrm{tail}}(48)$ Also Controls the Plancherel Component Tails (`plancherel_component_tail_domination_note`)**: For all $t \in \mathbb{R}$, the partial-fraction series gives $\nu_B(t) = \sum_{n=0}^\infty \frac{t^2/4}{(n + 5/4)((n + 5/4)^2 + t^2/4)} \le \frac{\zeta(3, 5/4)}{4}\,t^2 \le 4(t^2 + 1/4)$ (since $\frac{\zeta(3, 5/4)}{4} = -\frac{\psi''(5/4)}{8} \approx 0.1659674922 < 4$) and $\nu_{R_0}(t) = \frac{4t^2}{t^2 + 1/4} < 4 \le 4(t^2 + 1/4)$, so both Plancherel component integrands $\frac{1}{\tau}\nu_B(t)H_0(it)$ and $\frac{1}{\tau}\nu_{R_0}(t)H_0(it)$ are strictly bounded on $|t| \ge 48$ by $\frac{4(t^2 + 1/4)}{\tau}H_0(it) \le C_\Omega (t^2 + 1/4)^5 e^{-\pi|t|/2}$, and their two-sided tails on $|t| \ge 48$ are therefore bounded by $2 B_{\Omega,1}^{\mathrm{tail}}(48)$.
     4. *Implemented Complex-Analytic Quadrature Method and Validated 256-bit Arb Norms of $\Omega_{\log}$*:
        In `verify_hilbert_space_euler_intertwining_and_critical_line_factorization_arb`, the holomorphic product $Z_2(z) := \zeta'(1/2 + iz)\zeta'(1/2 - iz)$ (which equals $|\zeta'(1/2 + it)|^2 > 0$ on $z = t \in \mathbb{R}$) is enclosed on each complex sub-box $z$ of `acb.integral` on $[-48, 48]$ using a **degree-6 centered Taylor expansion** of $\zeta'(s)$ at $z_0 = \operatorname{mid}(z)$ with an interval Lagrange remainder on $z$ whenever $\operatorname{rad}(z) > 0$. In `_f_omega_L1`, the integrand checks the positivity/branch guard `bool(z2.real > arb(0))` before taking the principal holomorphic square root `z2.sqrt(analytic=analytic)` (returning `acb(nan, nan)` when `analytic and not bool(z2.real > arb(0))` so `acb.integral` subdivides the interval). Adding the two-sided tail bounds $2 B_{\Omega,1}^{\mathrm{tail}}(48)$ and $2 B_{\Omega,2}^{\mathrm{tail}}(48)$ gives the generated 256-bit Arb norm enclosures:
        $$
        \boxed{\|\Omega_{\log}\|_{L^1(\mathbb{R})} = \bigl[0.10084349298 \pm 5.15 \times 10^{-12}\bigr], \qquad \|\Omega_{\log}\|_{L^2(\mathbb{R})} = \bigl[0.02590072269 \pm 3.10 \times 10^{-12}\bigr],}
        $$
        with squared $L^2$ integral $\int_{\mathbb{R}} |\Omega_{\log}(t)|^2\,dt = [0.000670847436 \pm 2.37 \times 10^{-13}]$. In particular, at $X = 1$ ($H(1) = 1, M(1) = 2$), $|M_{\mathrm{band}}(1/2 + it; 1)| = |{-2^{-1/2 - it}}| = 2^{-1/2}$, so the triangle inequality requires $|R_{\mu,\mathrm{band}}(1)| \le 2^{-1/2}\|\Omega_{\log}\|_{L^1(\mathbb{R})}$, i.e.,
        $$
        \boxed{\|\Omega_{\log}\|_{L^1(\mathbb{R})} = \bigl[0.10084349298 \pm 5.15 \times 10^{-12}\bigr] \ge \sqrt{2}\,\bigl|R_{\mu,\mathrm{band}}(1)\bigr| = \bigl[0.019636922 \pm 4.11 \times 10^{-10}\bigr] \qquad (\text{certified in 256-bit Arb}).}
        $$

| Scale $X$ | Cutoffs $(H, M)$ | $A_X = \sum \frac{\|\mu(m)\|}{\sqrt{m}}$ | Discrete Sum $R_{\mu,\mathrm{band}}(X)$ | Finite Integral on $[-48, 48]$ | Finite Integration Error Radius (`finite_integration_error_radius`) | Proved Infinite-Tail Bound $2 A_X B_{\Omega,1}^{\mathrm{tail}}(48)$ (`infinite_tail_error_bound`) | Combined Mellin Enclosure | Combined Enclosure Radius (`combined_enclosure_radius`) | Encloses Zero Diff |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $(1, 2)$ | $[0.7071067811865475244008443621048490392848 \pm 2.00 \times 10^{-40}]$ | $[-0.0138854010 \pm 8.27 \times 10^{-11}]$ | $[-0.01388540094168 \pm 3.06 \times 10^{-15}]$ | $8.012471247481316 \times 10^{-16}$ | $1.940161939963809 \times 10^{-18}$ | $[-0.01388540094168 \pm 3.06 \times 10^{-15}]$ | $8.031872868010421 \times 10^{-16}$ | `True` |
| $2$ | $(1, 3)$ | $[1.284457050376173288909993142606806494932 \pm 2.00 \times 10^{-39}]$ | $[0.010898890859 \pm 2.89 \times 10^{-13}]$ | $[0.01089889085884 \pm 5.02 \times 10^{-15}]$ | $9.112944021256708 \times 10^{-16}$ | $3.5242975303903636 \times 10^{-18}$ | $[0.01089889085884 \pm 5.02 \times 10^{-15}]$ | $9.14818701078404 \times 10^{-16}$ | `True` |
| $4$ | $(3, 6)$ | $[0.8554618859638209556480487461972371457491 \pm 2.00 \times 10^{-40}]$ | $[0.0053844055765 \pm 8.78 \times 10^{-14}]$ | $[0.00538440557646 \pm 2.08 \times 10^{-15}]$ | $7.475972076500956 \times 10^{-16}$ | $2.347219170280871 \times 10^{-18}$ | $[0.00538440557646 \pm 2.08 \times 10^{-15}]$ | $7.499444269368047 \times 10^{-16}$ | `True` |

3. **Coherent Low-Frequency Euler Spike Obstruction on $\mathcal{H}_\tau^{\mathrm{pos}}$ as $y \to \infty$ (`TASK-TC-052R` & `TASK-TC-052R2`)**:
   By Plancherel's theorem on $\mathcal{H}_\tau^{\mathrm{pos}}$, $\|\mathcal{J}_\tau(E_y\psi_\tau)\|_{\mathcal{H}_\tau^{\mathrm{pos}}}^2 = \frac{1}{\tau}\int_{-\infty}^\infty \nu(t)|E_y(it)|^2 H_0(it)\,dt$, where $\nu(t) = \operatorname{Re}\psi(5/4 + it/2) - \psi(5/4) + \frac{4t^2}{t^2 + 1/4}$ satisfies $\nu(0) = 0$ and $\nu(t) \ge \frac{4t^2}{t^2 + 1/4} \ge \frac{16}{5}t^2$ for all $|t| \le 1$ (`Theorem 59`). On the `TC-046` low-frequency interval $I_y = [\frac{7\tau}{16\log y}, \frac{\tau}{2\log y}]$ (which satisfies $I_y \subset [0, 1]$ for all $y \ge e^{\tau/2} = e^\pi \approx 23.1407$, so $y \ge 24$), $\nu(t) \ge \frac{16}{5}\bigl(\frac{7\tau}{16\log y}\bigr)^2 = \frac{49\tau^2}{80(\log y)^2}$ while $|I_y| = \frac{\tau}{16\log y}$ gives an additional $(\log y)^{-1}$ factor, yielding the $(\log y)^{-3}$ prefactor:
   $$
   \boxed{\|\mathcal{J}_\tau(E_y\psi_\tau)\|_{\mathcal{H}_\tau^{\mathrm{pos}}}^2 \ge \frac{49\tau^2\bigl(H_0(0) + o(1)\bigr)}{640\,(\log y)^3}\exp\!\left[\bigl(4\cos(\tau/16) + o(1)\bigr)\frac{\sqrt{y}}{\log y}\right] \to +\infty \qquad (y \to \infty),}
   $$
   where $4\cos(\tau/16) = 4\cos(\pi/8) = 2\sqrt{2 + \sqrt{2}} \approx 3.69551813 > 0$. Because the polynomial factor $(\log y)^{-3}$ is absorbed into the subleading $o(\sqrt{y}/\log y)$ term of the exponent, the quadratic zero $\nu(t) \asymp t^2$ at $t = 0$ does not suppress the super-polynomial low-frequency Euler spike, demonstrating why unsplit Hilbert-space norm bounds at $y = M(X_K)$ grow super-polynomially in $X_K$ and why signed phase oscillation in $R_{\mathrm{II}}(X; U, V)$ / $M_{\mathrm{band}}(1/2 + it; X) X^{it}$ cannot be bypassed by triangle or Cauchy–Schwarz inequalities.

### 9.4 Complete Conditional Implication Chain to the Riemann Hypothesis (`Theorem 59`, `euler_sieved_orbit_and_complete_subgate_closure_chain`)

In Lean **Theorem 59** (`euler_sieved_orbit_and_complete_subgate_closure_chain`), we assemble the conditional/algebraic deduction from a uniform transition-integral bound $|I(X)| \le B_I$ to $\delta_\rho = 0$ (via the explicitly assumed analytic bridge implication `h_bridge`):
$$
\boxed{\forall X \ge 1,\;\bigl|I(X)\bigr| \le B_I \;\Longrightarrow\; \forall X \ge 1,\;\bigl|R_{\mu,\mathrm{band}}(X)\bigr| \le B_I + C_{\log,0} \;\Longrightarrow\; \forall K \in \mathbb{A}_{\mathbb{R}},\;\bigl|C_\tau(K)\bigr| \le B_{\mathrm{total}} := P_\tau(0) + B_{\mathrm{ctrl}} + B_I + C_{\log,0} < 21.102829 + B_I \;\Longrightarrow\; \text{RH},}
$$
where:
1. **$K = 0$ Safety (Zero Division by $K$ or $\|f_-^{(K)}\|_{L^2}^2$)**: For all $K \in \mathbb{A}_{\mathbb{R}}$ (both positive and negative grades, and $K = 0$), $X_K = \tau^{|K|} \ge 1$ is well-defined; at $K = 0$, $X_0 = 1$, $H(1) = 1$, $M(1) = 2$, and $C_\tau(0) = P_\tau(0) + E_{\tau,\mathrm{controlled}}(0) - R_{\mu,\mathrm{band}}(1) \approx 0.00095048 \le B_{\mathrm{total}}$ holds directly without dividing by $K$ or $\|f_-^{(K)}\|_{L^2}^2$.
2. **Exact Multiplicity Preservation ($m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$, Zero Simplicity Not Assumed)**: In the explicit formula $C_\tau(t) = W_\xi(h_t)$, $-\xi'(s)/\xi(s)$ has simple poles of residue $-m_\rho = -\operatorname{ord}_\xi(\rho) \le -1$ (equivalently, $\xi'(s)/\xi(s)$ has simple poles of positive integer residue $+m_\rho \ge 1$), so contour orientation makes each distinct nontrivial zero $\rho$ contribute $+m_\rho H_0(\rho - 1/2)\tau^{-t(\rho - 1/2)}$ with $m_\rho H_0(\rho - 1/2) \ne 0$ on $0 < \operatorname{Re}(\rho) < 1$ and no polynomial $t^j$ drift.
3. **No Maximal Real Displacement Assumption ($\delta_* = \sup_\rho |\delta_\rho|$ Not Assumed)**: Two independent analytic arguments avoid assuming that $\sup_\rho \operatorname{Re}(\rho)$ is attained:
   - *Laplace–Carleman Resolvent Continuation (`TC-037` / Theorem 12)*: The partial-fraction resolvent $\mathcal{R}_\tau(w) = \sum_\rho \frac{m_\rho H_0(\rho - 1/2)}{w - L(\rho - 1/2)}$ has isolated simple poles at every individual zero $w_{\rho_0} = L(\rho_0 - 1/2)$, whereas $|C_\tau(-t)| \le B_{\mathrm{total}}$ makes $\mathcal{R}_\tau(w) = \int_0^\infty C_\tau(-t)e^{-wt}\,dt$ holomorphic on $\operatorname{Re}(w) > 0$, excluding any individual zero with $\delta_{\rho_0} > 0$ (and by $\xi(1 - s) = \xi(s)$, any $\delta_{\rho_0} \ne 0$).
   - *Direct Mellin Strip Holomorphy (`TC-045`)*: Equivalently, $|R_{\mu,\mathrm{band}}(X)| \le B_I + C_{\log,0}$ implies $|W(X)| \le M_W < \infty$ for all $X \ge 1$, so $\mathcal{M}_X[W](z) = -\frac{\zeta'(1/2+z)}{\zeta(1/2+z)}H_0(z)$ converges absolutely and holomorphically on $0 < \operatorname{Re}(z) < 5/2$, directly excluding any zero of $\zeta(1/2 + z)$ in $0 < \operatorname{Re}(z) < 1/2$.
4. **Honest Gate Status**: Because an unconditional uniform bound $|I(X)| \le B_I$ (or $|R_{\mathrm{II}}(X; U, V)| \le B_{\mathrm{II}}$) for the actual Möbius function remains unproved, `SUBGATE-TC-043A` remains `OPEN` and `rh_proved: false`.

---

## 10. Trivial-Zero Slopes, Generalized Báez–Duarte Mellin Criterion, Common-Factor Expansion, and Coprime Squarefree Block Cancellation (`TASK-TC-053`, `section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation`)

In `TASK-TC-053` (branched from the merged `TC-052R2` baseline `c64596727e7142596acd073c6c8e4eb28f2eaee0`), we investigate whether prime arithmetic forces cancellation between *different* squarefree integers once every factorization of the *same* integer has been accounted for, connecting the transported trivial-zero slopes of $Z_{a_K}(s) = \zeta(s / a_K)$ to the Gaussian-weighted Möbius sum $Q(X) = X^{5/2} G(X^2)$ and attacking the balanced coprime block $S(A) = \sum_{A^2 \le q < 4 A^2} \mu(q) w_A(q)$.

### 10.1 Transported Trivial-Zero Slopes, Generalized Báez–Duarte Sequence, Gaussian Proxy $G(k) - c_k = O(k^{-2})$, and Mellin Grade-Energy Criterion (`section_1_trivial_zero_slopes_and_mellin_energy_criterion`)

1. **Strict Separation of Grade $K$, Trivial-Zero Index $m$, and Finite-Difference Order $k$**:
   Throughout Section 9 (`TASK-TC-053`), we keep three distinct indices strictly separated:
   - $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$ is the **algebraic scale grade** (both positive and negative grades), with scale factor $a_K := \tau^K$ ($\tau = 2\pi$) and grade-dilated zeta function $Z_{a_K}(s) := \zeta(s / a_K)$;
   - $m \in \mathbb{Z}_{\ge 1}$ is the **trivial-zero index**, locating the transported trivial zero $s_{m, K} := -2 m a_K = -2 m \tau^K$ on the grade worldline $W_{-2m}(K)$;
   - $k \in \mathbb{Z}_{\ge 0}$ is the **binomial finite-difference order** in the sequence $c_k$.

2. **Exact Derivation of the Transported Trivial-Zero Slope Identity**:
   By the chain rule, $Z_{a_K}'(s) = \frac{d}{ds}\zeta(s / a_K) = a_K^{-1}\zeta'(s / a_K)$, so evaluating at the transported trivial zero $s_{m, K} = -2 m a_K$ eliminates the scale factor $a_K$:
   $$
   \boxed{a_K Z_{a_K}'(-2 m a_K) = a_K \cdot a_K^{-1}\zeta'(-2m) = \zeta'(-2m) \qquad \forall K \in \mathbb{A}_{\mathbb{R}}, \; \forall m \in \mathbb{Z}_{\ge 1}.}
   $$
   Differentiating Riemann's asymmetric functional equation $\zeta(s) = 2^s \pi^{s-1}\sin\bigl(\frac{\pi s}{2}\bigr)\Gamma(1 - s)\zeta(1 - s)$ at $s = -2m$ (where $\sin(-\pi m) = 0$ annihilates the undifferentiated terms and $\frac{d}{ds}\sin(\frac{\pi s}{2})\big|_{s=-2m} = \frac{\pi}{2}\cos(-\pi m) = \frac{\pi}{2}(-1)^m$) gives
   $$
   \zeta'(-2m) = 2^{-2m}\pi^{-2m-1}\cdot\frac{\pi}{2}(-1)^m\,\Gamma(2m + 1)\,\zeta(2m + 1) = \frac{(-1)^m (2m)!}{2\,(2\pi)^{2m}}\,\zeta(2m + 1) = \frac{(-1)^m (2m)!}{2\,\tau^{2m}}\,\zeta(2m + 1),
   $$
   and hence
   $$
   \boxed{\frac{2(-1)^m \tau^{2m}}{(2m)!}\,a_K Z_{a_K}'(-2 m a_K) = \zeta(2m + 1) \qquad (\tau = 2\pi,\; m \in \mathbb{Z}_{\ge 1},\; K \in \mathbb{A}_{\mathbb{R}}),}
   $$
   verified symbolically (`symbolic_reflection_prefactor_verified: true`) and in 256-bit Arb across $m \in \{1, 2, 3\}$ and $K \in \{-1, 0, +1, \sqrt{2}\}$ (`all_worldline_zeros_enclose_zero: true`, `all_slope_identities_enclose_zero: true`).

3. **Euler Product, Binomial Finite Differences $c_k$, and Role Separation (Grade Transport $K$ vs. Varying $m$)**:
   For $s = 2j + 3 \ge 3$ ($m = j + 1 \ge 1$), absolute convergence of the Euler product gives $\frac{1}{\zeta(2j + 3)} = \prod_p \bigl(1 - p^{-(2j + 3)}\bigr) = \sum_{n=1}^\infty \frac{\mu(n)}{n^{2j+3}}$. Forming the $k$-th binomial forward difference over $j \in \{0, 1, \dots, k\}$ and interchanging the finite sum over $j$ with the absolutely convergent series over $n \ge 1$ yields
   $$
   \boxed{c_k := \sum_{j=0}^k (-1)^j \binom{k}{j}\frac{1}{\zeta(2j + 3)} = \sum_{n=1}^\infty \frac{\mu(n)}{n^3}\sum_{j=0}^k (-1)^j \binom{k}{j} n^{-2j} = \sum_{n=1}^\infty \frac{\mu(n)}{n^3}\bigl(1 - n^{-2}\bigr)^k.}
   $$
   - **Generalized Báez–Duarte Precedent & Primary Sources**:
     - M. Riesz (1916), *Sur l'hypothèse de Riemann*, Acta Math. **40**, 185–190 (continuous power-series criterion $\sum_{k=1}^\infty \frac{(-1)^{k+1} x^k}{(k-1)!\,\zeta(2k)} = O_\varepsilon(x^{1/4 + \varepsilon})$);
     - G. H. Hardy & J. E. Littlewood (1918), *Contributions to the theory of the Riemann zeta-function and the theory of the distribution of primes*, Acta Math. **41**, 119–196 (§2.5 Mellin equivalence of Riesz's criterion);
     - L. Báez–Duarte (2003), *A new necessary and sufficient condition for the Riemann hypothesis*, `arXiv:math/0307215`, and (2005), *A sequential Riesz-like criterion for the Riemann hypothesis*, Int. J. Math. Math. Sci. **2005**(21), 3527–3537 (discrete sequence $c_k^{\mathrm{BD}} = \sum_{j=0}^k (-1)^j \binom{k}{j}\frac{1}{\zeta(2j + 2)} = \sum_{n=1}^\infty \frac{\mu(n)}{n^2}(1 - n^{-2})^k$, of which $c_k$ is the odd-argument shift $2j + 2 \mapsto 2j + 3$ obtained from the trivial-zero slopes $\zeta'(-2(j+1))$).
   - **What Grade Transport $K$ Contributes vs. What Varying $m$ Contributes**:
     - *Grade transport $K$*: Contributes **pure multiplicative scale covariance** $a_K Z_{a_K}'(-2 m a_K) = \zeta'(-2m)$, which is identically independent of $K$ at every fixed $m$; varying $K$ at fixed $m$ does not generate new Dirichlet-series moments. In the continuous Mellin setting, grade transport $Y_k = \tau^k$ partitions $[1, \infty)$ into multiplicative grade blocks $[\tau^k, \tau^{k+1}]$ of uniform logarithmic length $\log\tau$.
     - *Varying $m = j + 1 \in \{1, \dots, k + 1\}$*: Samples the reciprocal Dirichlet series $\sum_{n \ge 1}\mu(n)n^{-s} = 1/\zeta(s)$ at distinct odd integers $s = 2m + 1 = 2j + 3$, producing the polynomial weight $(1 - n^{-2})^k$ that localizes on squarefree integers $n \asymp \sqrt{k}$.

4. **Gaussian Proxy $G(t)$, $Q(X) = X^{5/2}G(X^2)$, and Explicit Proof of $G(k) - c_k = O(k^{-2})$**:
   Set
   $$
   \boxed{G(t) := \sum_{n=1}^\infty \frac{\mu(n)}{n^3} e^{-t / n^2} \quad (t > 0), \qquad Q(X) := X^{5/2} G(X^2) = X^{5/2}\sum_{n=1}^\infty \frac{\mu(n)}{n^3} e^{-X^2 / n^2} \quad (X > 0).}
   $$
   For every integer $k \ge 1$, splitting $G(k) - c_k$ into $n = 1$ and $n \ge 2$ gives:
   - **$n = 1$ Term**: At $n = 1$, $(1 - 1^{-2})^k = 0$ for all $k \ge 1$, while $e^{-k / 1^2} = e^{-k} > 0$. Since $\sup_{t > 0} t^2 e^{-t} = 4 e^{-2}$ (attained at $t = 2$, where $k^2 e^{2-k} \le 4$ for all $k \ge 1$ with exact equality at $k = 2$), the $n = 1$ term satisfies
     $$
     0 < e^{-k} \le 4 e^{-2}\,k^{-2} = C_1\,k^{-2}, \qquad C_1 := 4 e^{-2} \approx 0.5413411329.
     $$
   - **$n \ge 2$ Sum**: For $n \ge 2$, $x := n^{-2} \in (0, 1/4]$. Since $\log(1 - x) = -x - \sum_{r=2}^\infty \frac{x^r}{r}$ satisfies $0 < -x - \log(1 - x) \le \frac{x^2}{2}\sum_{r=0}^\infty (1/4)^r = \frac{2}{3}x^2$, the mean-value inequality $1 - e^{-\delta} \le \delta$ for $\delta = k(-x - \log(1-x)) > 0$ gives
     $$
     0 < e^{-k/n^2} - \bigl(1 - n^{-2}\bigr)^k = e^{-k/n^2}\bigl(1 - e^{-\delta}\bigr) \le \frac{2}{3}\,k\,n^{-4}\,e^{-k/n^2}.
     $$
     Summing over $n \ge 2$ and comparing the unimodal function $f_k(u) := u^{-7} e^{-k / u^2}$ on $(0, \infty)$ (which attains its unique global maximum $f_k(\sqrt{2k/7}) = \bigl(\frac{7}{2e}\bigr)^{7/2} k^{-7/2}$ at $u_* = \sqrt{2k/7}$ and has total integral $\int_0^\infty u^{-7} e^{-k/u^2}\,du = k^{-3}\int_0^\infty v^2 e^{-v}\,dv = k^{-3}$) gives $\sum_{n=2}^\infty n^{-7} e^{-k/n^2} \le \int_0^\infty f_k(u)\,du + \sup_{u > 0} f_k(u) \le \bigl(1 + (\frac{7}{2e})^{7/2}\bigr)k^{-3}$, and hence
     $$
     \Biggl|\sum_{n=2}^\infty \frac{\mu(n)}{n^3}\Bigl(e^{-k/n^2} - (1 - n^{-2})^k\Bigr)\Biggr| \le \frac{2}{3}\,k\sum_{n=2}^\infty n^{-7} e^{-k/n^2} \le C_2\,k^{-2}, \qquad C_2 := \frac{2}{3}\left(1 + \left(\frac{7}{2e}\right)^{7/2}\right) \approx 2.2814572550.
     $$
   - **Combined Explicit $O(k^{-2})$ Bound**:
     $$
     \boxed{\bigl|G(k) - c_k\bigr| \le C_{G,c}\,k^{-2} \qquad \forall k \ge 1, \qquad C_{G,c} := 4 e^{-2} + \frac{2}{3}\left(1 + \left(\frac{7}{2e}\right)^{7/2}\right) = \bigl[2.822798387987013361092201192203292862020 \pm 2.00 \times 10^{-39}\bigr] < \frac{7}{2} = 3.5,}
     $$
     certified in 256-bit Arb across $k \in \{0, 1, 2, 4, 8, 16, 32, 64\}$ (`all_G_k_minus_c_k_bounds_certified: true`).

5. **Mellin Identity for $Q(X)$ and Five-Step Proof of the Sufficient Grade-Energy Criterion**:
   - **Mellin Identity on $\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}$**: For $\frac{1}{2} < \sigma := \operatorname{Re} z < \frac{5}{2}$, substituting $w = X^2 / n^2$ ($X = n w^{1/2}$, $\frac{dX}{X} = \frac{1}{2}\frac{dw}{w}$) gives $\int_0^\infty X^{5/2 - z} e^{-X^2/n^2}\frac{dX}{X} = \frac{1}{2}\Gamma\!\bigl(\frac{5}{4} - \frac{z}{2}\bigr)n^{5/2 - z}$. Since $\sum_{n=1}^\infty n^{-3}\int_0^\infty X^{5/2-\sigma} e^{-X^2/n^2}\frac{dX}{X} = \frac{1}{2}\Gamma\!\bigl(\frac{5}{4} - \frac{\sigma}{2}\bigr)\sum_{n=1}^\infty n^{-(1/2 + \sigma)} = \frac{1}{2}\Gamma\!\bigl(\frac{5}{4} - \frac{\sigma}{2}\bigr)\zeta\!\bigl(\frac{1}{2} + \sigma\bigr) < \infty$ for $\frac{1}{2} < \sigma < \frac{5}{2}$, Fubini–Tonelli justifies termwise integration and yields:
     $$
     \boxed{\mathcal{M}[Q](z) := \int_0^\infty Q(X) X^{-z}\frac{dX}{X} = \frac{\Gamma(5/4 - z/2)}{2\,\zeta(1/2 + z)} \qquad \left(\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}\right),}
     $$
     certified symbolically (`mellin_symbolic_termwise_verified: true`) and in 256-bit Arb at $z \in \{1, 3/2, 2\}$ (`all_mellin_strip_checks_enclose_zero: true`).
   - **Sufficient Grade-Energy Criterion (`SUFFICIENT_CRITERION_CONDITIONAL_ON_ARITHMETIC_ENERGY_PREMISE`)**: Suppose that for every $\varepsilon > 0$ there exists $C_\varepsilon < \infty$ such that
     $$
     \int_Y^{\tau Y} |Q(X)|^2 \frac{dX}{X} \le C_\varepsilon Y^\varepsilon \qquad \forall Y \ge 1.
     $$
     Here arbitrary real $Y \ge 1$ and aligned discrete grade blocks $Y_k = \tau^k$ ($k \in \mathbb{Z}_{\ge 0}$) are equivalent with **exact covering constant $1 + \tau^\varepsilon$**: for any $Y \ge 1$, putting $k := \lfloor\log_\tau Y\rfloor \ge 0$ gives $\tau^k \le Y < \tau^{k+1}$ and $[Y, \tau Y] \subset [\tau^k, \tau^{k+1}] \cup [\tau^{k+1}, \tau^{k+2}]$, so if $\int_{\tau^j}^{\tau^{j+1}} |Q(X)|^2 \frac{dX}{X} \le C_\varepsilon (\tau^j)^\varepsilon$ for all $j \ge 0$, then
     $$
     \int_Y^{\tau Y} |Q(X)|^2 \frac{dX}{X} \le C_\varepsilon\bigl((\tau^k)^\varepsilon + (\tau^{k+1})^\varepsilon\bigr) = C_\varepsilon\bigl(1 + \tau^\varepsilon\bigr)(\tau^k)^\varepsilon \le \bigl(1 + \tau^\varepsilon\bigr)C_\varepsilon\,Y^\varepsilon.
     $$
     Under this premise, off-critical zeros of $\zeta(s)$ are excluded by the following five steps:
     1. *Small-$X$ convergence on $(0, 1]$*: Since $|G(X^2)| \le \sum_{n=1}^\infty n^{-3} = \zeta(3)$, $|Q(X)| \le \zeta(3) X^{5/2}$ for all $X > 0$, so $\int_0^1 |Q(X)| X^{-\sigma}\frac{dX}{X} \le \frac{\zeta(3)}{5/2 - \sigma} < \infty$ for every $\sigma = \operatorname{Re} z < 5/2$.
     2. *Cauchy–Schwarz on grade blocks $[\tau^k, \tau^{k+1}]$ ($k \ge 0$, $Y_k = \tau^k \ge 1$)*: For any $\sigma = \operatorname{Re} z > 0$, choosing $\varepsilon = \sigma > 0$ gives
        $$
        \int_{\tau^k}^{\tau^{k+1}} |Q(X)| X^{-\sigma}\frac{dX}{X} \le \left(\int_{\tau^k}^{\tau^{k+1}} |Q(X)|^2\frac{dX}{X}\right)^{1/2}\left(\int_{\tau^k}^{\tau^{k+1}} X^{-2\sigma}\frac{dX}{X}\right)^{1/2} \le \bigl(C_\sigma \tau^{k\sigma}\bigr)^{1/2}\bigl((\log\tau)\tau^{-2k\sigma}\bigr)^{1/2} = \sqrt{C_\sigma\log\tau}\,\tau^{-k\sigma/2}.
        $$
     3. *Geometric summation over $k \ge 0$ and holomorphy on $0 < \operatorname{Re} z < 5/2$*: Since $\tau = 2\pi > 1$ and $\sigma > 0$, $\sum_{k=0}^\infty \tau^{-k\sigma/2} = \frac{1}{1 - \tau^{-\sigma/2}} < \infty$ converges uniformly on compact subsets of $\{0 < \operatorname{Re} z < 5/2\}$, so $\mathcal{M}[Q](z)$ converges absolutely and defines a holomorphic function on the full strip $0 < \operatorname{Re} z < 5/2$.
     4. *Strip overlap and nonvanishing of $\Gamma(5/4 - z/2)$*: The strip $\{0 < \operatorname{Re} z < 5/2\}$ overlaps the initial absolute-convergence strip $\{1/2 < \operatorname{Re} z < 5/2\}$ on $\{1/2 < \operatorname{Re} z < 5/2\}$, so by analytic continuation $\mathcal{M}[Q](z) = \frac{\Gamma(5/4 - z/2)}{2\zeta(1/2 + z)}$ holds throughout $0 < \operatorname{Re} z < 5/2$. Because $\Gamma(w)$ has no zeros anywhere in $\mathbb{C}$ (and is holomorphic on $\operatorname{Re} w = 5/4 - \operatorname{Re} z / 2 > 0$), any zero $\rho = 1/2 + z_0$ of $\zeta(s)$ with $1/2 < \operatorname{Re}\rho < 1$ ($0 < \operatorname{Re} z_0 < 1/2$) would create a pole of $\frac{\Gamma(5/4 - z/2)}{2\zeta(1/2 + z)}$ at $z_0$, contradicting holomorphy of $\mathcal{M}[Q](z)$.
     5. *Functional-equation reflection*: $\xi(1 - s) = \xi(s)$ reflects any nontrivial zero with $0 < \operatorname{Re}\rho < 1/2$ to $1 - \rho$ with $1/2 < \operatorname{Re}(1 - \rho) < 1$, excluding all off-critical nontrivial zeros of $\zeta(s)$.

### 10.2 Common-Factor Expansion, Coprime Squarefree Counting across All $t > 0$, the $(29, 31, 30)$ Counterexample, Proved Replacement Pairwise Bound, and Valid Growing Range (`section_2_common_factor_expansion_and_coprime_squarefree_asymptotics`)

1. **Common-Factor Bijection $(m, n) = (dr, ds)$ and Exact Möbius Factorization**:
   Every ordered pair $(m, n) \in \mathbb{Z}_{\ge 1}^2$ factors uniquely as $m = dr$, $n = ds$ with $d = \gcd(m, n) \ge 1$ and $\gcd(r, s) = 1$. Since $\mu$ is multiplicative and vanishes on squares:
   - If $\gcd(d, rs) > 1$, some prime $p \mid d$ also divides $r$ or $s$, so $p^2 \mid dr$ or $p^2 \mid ds$, giving $\mu(dr)\mu(ds) = 0$;
   - If $\gcd(d, rs) = 1$, then $\gcd(d, r) = \gcd(d, s) = 1$, so $\mu(dr) = \mu(d)\mu(r)$ and $\mu(ds) = \mu(d)\mu(s)$, yielding
     $$
     \boxed{\mu(dr)\mu(ds) = \mathbf{1}_{\gcd(d, rs) = 1}\,\mu(d)^2\,\mu(r)\mu(s) \qquad (\gcd(r, s) = 1),}
     $$
     verified across all $60 \times 60 = 3600$ ordered pairs $1 \le m, n \le 60$ (`all_mobius_splits_exact: true`) and in Lean (`RiemannScope.common_factor_mobius_split_and_valid_growing_range_exponent`). Expanding $Q(X)^2$ over $(d, r, s)$ gives
     $$
     Q(X)^2 = \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}} I_{r,s}(X), \qquad I_{r,s}(X) := \frac{\mu(r)\mu(s)}{(rs)^3}\,X^5\sum_{\substack{d \ge 1 \\ \gcd(d, rs) = 1}} \frac{\mu(d)^2}{d^6}\exp\!\left(-\frac{X^2}{d^2}\bigl(r^{-2} + s^{-2}\bigr)\right).
     $$

2. **Coprime Squarefree Counting Estimate $N_q(t) = \kappa(q)t + R_q(t)$ across All $t > 0$ (Including $0 < t < 1$)**:
   - **Range $t \ge 1$**: Inserting $\mu(d)^2 = \sum_{a^2 \mid d}\mu(a)$ into $N_q(t) := \sum_{1 \le d \le t,\, \gcd(d, q)=1}\mu(d)^2$ gives
     $$
     N_q(t) = \sum_{\substack{1 \le a \le \sqrt{t} \\ \gcd(a, q) = 1}} \mu(a)\,\#\bigl\{m \le t / a^2 : \gcd(m, q) = 1\bigr\}.
     $$
     By inclusion-exclusion over squarefree divisors $e \mid q$, $\#\{m \le y : \gcd(m, q) = 1\} = \sum_{e \mid q}\mu(e)\lfloor y/e\rfloor = y\prod_{p \mid q}\bigl(1 - \frac{1}{p}\bigr) + \theta_q(y)$ with $|\theta_q(y)| \le \sum_{e \mid q}|\mu(e)| = 2^{\omega(q)}$. Substituting $y = t / a^2$ and completing the tail $\sum_{a > \sqrt{t}} a^{-2} \le 2 t^{-1/2}$ yields $|R_q(t)| \le (2^{\omega(q)} + 2)\sqrt{t} \le 3\cdot 2^{\omega(q)}\sqrt{t}$ for $t \ge 1$.
   - **Range $0 < t < 1$**: For $0 < t < 1$, the counting sum $N_q(t) = 0$ is empty, so $R_q(t) = -\kappa(q)t$ and
     $$
     \bigl|R_q(t)\bigr| = \kappa(q)\,t \le \frac{1}{\zeta(2)}\,t < \frac{6}{\pi^2}\sqrt{t} < 3\sqrt{t} \le \bigl(2^{\omega(q)} + 2\bigr)\sqrt{t} \le 3\cdot 2^{\omega(q)}\sqrt{t} \qquad (0 < t < 1).
     $$
   - **Uniform Bound for All $t > 0$**:
     $$
     \boxed{N_q(t) = \kappa(q)\,t + R_q(t), \qquad \kappa(q) := \frac{1}{\zeta(2)}\prod_{p \mid q}\frac{p}{p + 1}, \qquad \bigl|R_q(t)\bigr| \le \bigl(2^{\omega(q)} + 2\bigr)\sqrt{t} \le 3\cdot 2^{\omega(q)}\sqrt{t} \quad \forall t > 0,}
     $$
     certified in 256-bit Arb across $q \in \{1, 2, 6, 30, 210, 899\}$ and $t \in \{1/2, 10, 50, 200, 1000\}$ (`all_counting_bounds_certified: true`).

3. **Gaussian Integral Evaluation and Scale-Independent Pairwise Leading Term $L_{r,s}$**:
   For $\alpha := r^{-2} + s^{-2} = \frac{r^2 + s^2}{(rs)^2} > 0$, substituting $u = X / t$ ($t = X / u$, $dt = -X u^{-2} du$) in $X^5\int_0^\infty t^{-6} e^{-\alpha X^2 / t^2}\,dt$ gives
   $$
   \int_0^\infty u^4 e^{-\alpha u^2}\,du = \frac{1}{2}\alpha^{-5/2}\Gamma\!\left(\frac{5}{2}\right) = \frac{3\sqrt{\pi}}{8}\,\alpha^{-5/2} = \frac{3\sqrt{\pi}}{8}\,\frac{(rs)^5}{(r^2 + s^2)^{5/2}},
   $$
   and multiplying by $\frac{\mu(r)\mu(s)}{(rs)^3}\kappa(rs)$ confirms the exact scale-independent pairwise leading contribution:
   $$
   \boxed{L_{r, s} := \frac{3\sqrt{\pi}}{8}\,\mu(r)\mu(s)\,\kappa(rs)\,\frac{(rs)^2}{(r^2 + s^2)^{5/2}}, \qquad E_{r,s}(X) := I_{r,s}(X) - L_{r,s},}
   $$
   verified symbolically (`gaussian_symbolic_verified: true`).

4. **Reproduction of the $(r, s, X) = (29, 31, 30)$ Counterexample Falsifying the Old Pairwise Inequality (`counterexample_r29_s31_X30_falsifying_old_pairwise_bound`)**:
   In `TASK-TC-053R`, before changing the pairwise error formula, we evaluate the exact quantities at $(r, s, X) = (29, 31, 30)$ in 256-bit Arb:
   - Both $r = 29$ and $s = 31$ are prime, so $\mu(29) = \mu(31) = -1$ and $\mu(29)\mu(31) = +1$; $q = rs = 899$, $\omega(899) = 2$, $2^{\omega(899)} = 4$, $r^2 + s^2 = 841 + 961 = 1802$, and $\kappa(899) = \frac{1}{\zeta(2)}\frac{29}{30}\frac{31}{32} = \frac{899}{160\,\pi^2}$.
   - Because $\mu(29)\mu(31) = +1$, every term of the exact $d$-sum $I_{29,31}(30) = \frac{30^5}{899^3}\sum_{\gcd(d,899)=1}\frac{\mu(d)^2}{d^6}\exp\bigl(-\frac{900\cdot 1802}{899^2 d^2}\bigr)$ is strictly nonnegative (`all_d_sum_terms_nonnegative: true`), so the $d = 1$ contribution alone is a rigorous lower bound on $I_{29,31}(30)$:
     - $d = 1$ contribution:
       $$
       I_{29,31}^{(d=1)}(30) = \frac{30^5}{899^3}\exp\!\left(-\frac{900\cdot 1802}{899^2}\right) = \bigl[0.004496116626444835904165753124575485457894 \pm 2.00 \times 10^{-42}\bigr];
       $$
     - Full $d$-sum contribution ($d \le 2000$ plus tail $\le \frac{1}{5\cdot 2000^5}$):
       $$
       I_{29,31}(30) = \bigl[0.004852248120771122 \pm 2.20 \times 10^{-19}\bigr];
       $$
     - Scale-independent leading term $L_{29,31}$:
       $$
       L_{29,31} = \frac{3\sqrt{\pi}}{8}\,\kappa(899)\,\frac{899^2}{1802^{5/2}} = \bigl[0.002218597833835925105427052279021906936628 \pm 2.00 \times 10^{-42}\bigr];
       $$
     - $d = 1$ lower bound on the pairwise error $E_{29,31}(30)$:
       $$
       E_{29,31}(30) \ge E_{29,31}^{(d=1)}(30) := I_{29,31}^{(d=1)}(30) - L_{29,31} = \bigl[0.002277518792608910798738700845553578521267 \pm 2.00 \times 10^{-42}\bigr]
       $$
       (and full error $E_{29,31}(30) = [0.002633650286935197 \pm 3.20 \times 10^{-19}]$);
     - Old asserted upper bound at $(29, 31, 30)$:
       $$
       B_{\mathrm{old}}(29, 31, 30) = \bigl[0.001516389420551170594757261430873825969737 \pm 2.00 \times 10^{-42}\bigr];
       $$
     - **Certified Contradiction (Strictly Positive Lower Bound on the Excess)**:
       $$
       \boxed{E_{29,31}^{(d=1)}(30) - B_{\mathrm{old}}(29, 31, 30) = \bigl[0.0007611293720577402039814394146797525515291 \pm 2.00 \times 10^{-43}\bigr] > 0.000761129 > 0}
       $$
       (`contradiction_strictly_positive_lower_bound_certified: true`, with full excess $E_{29,31}(30) - B_{\mathrm{old}}(29, 31, 30) = [0.001117260866384026 \pm 5.20 \times 10^{-19}] > 0$). This falsifies the old uniform pairwise inequality while leaving the aggregate growing-range upper bound intact via the proved replacement pairwise bound below.

5. **Derivation of the Proved Replacement Pairwise Bound from the Exact Sum**:
   Put $L := X\sqrt{r^{-2} + s^{-2}} = \frac{X\sqrt{r^2 + s^2}}{rs} > 0$ and $\phi_L(t) := t^{-6} e^{-L^2 / t^2}$ on $(0, \infty)$. Writing $N_{rs}(t) = \kappa(rs)t + R_{rs}(t)$ for all $t > 0$, Stieltjes integration by parts of $dR_{rs}(t) = dN_{rs}(t) - \kappa(rs)\,dt$ against $\phi_L(t)$ on $(0, \infty)$ gives
   $$
   E_{r,s}(X) = \frac{\mu(r)\mu(s)}{(rs)^3}\,X^5\int_{0^+}^\infty \phi_L(t)\,dR_{rs}(t) = \frac{\mu(r)\mu(s)}{(rs)^3}\,X^5\left(\Bigl[R_{rs}(t)\,\phi_L(t)\Bigr]_{t \to 0^+}^{t \to \infty} - \int_0^\infty R_{rs}(t)\,\phi_L'(t)\,dt\right),
   $$
   where **both boundary terms vanish**:
   - as $t \to 0^+$, $N_{rs}(t) = 0$ for $0 < t < 1$, so $R_{rs}(t) = -\kappa(rs)t = O(t)$ while $\phi_L(t) = t^{-6} e^{-L^2/t^2}$ vanishes faster than any power of $t$, giving $\lim_{t \to 0^+} R_{rs}(t)\phi_L(t) = 0$;
   - as $t \to \infty$, $|R_{rs}(t)| \le 3\cdot 2^{\omega(rs)}\sqrt{t}$ while $0 < \phi_L(t) \le t^{-6}$, so $|R_{rs}(t)\phi_L(t)| \le 3\cdot 2^{\omega(rs)} t^{-11/2} \to 0$.
   Because $|R_{rs}(t)| \le (2^{\omega(rs)} + 2)\sqrt{t} \le 3\cdot 2^{\omega(rs)}\sqrt{t}$ holds for **all $t > 0$** (including $0 < t < 1$), we obtain
   $$
   \bigl|E_{r,s}(X)\bigr| \le \frac{X^5}{(rs)^3}\cdot 3\cdot 2^{\omega(rs)}\int_0^\infty \sqrt{t}\,\bigl|\phi_L'(t)\bigr|\,dt.
   $$
   Differentiating $\phi_L(t) = t^{-6} e^{-L^2 / t^2}$ ($L > 0$) gives
   $$
   \phi_L'(t) = 2 t^{-7}\bigl(L^2 / t^2 - 3\bigr)e^{-L^2 / t^2},
   $$
   which changes sign at $t = L / \sqrt{3}$ ($v = 3$). Under the change of variables
   $$
   v = \frac{L^2}{t^2}, \qquad t = L v^{-1/2}, \qquad |dt| = \frac{L}{2} v^{-3/2}\,dv,
   $$
   the factor of $2$ in $\phi_L'(t)$ and $\frac{1}{2}$ in $|dt|$ cancel to $1$, and the powers of $t$ and $L$ combine as
   $$
   \sqrt{t}\cdot t^{-7}\cdot \frac{L}{2}v^{-3/2} = \bigl(L^{1/2} v^{-1/4}\bigr)\bigl(L^{-7} v^{7/2}\bigr)\left(\frac{L}{2} v^{-3/2}\right) = \frac{1}{2} L^{-11/2}\,v^{7/4},
   $$
   where the exponent of $v$ is $-\frac{1}{4} + \frac{7}{2} - \frac{3}{2} = \frac{7}{4}$ (repairing the erroneous exponent $\frac{11}{4}$ in `TASK-TC-053R`; in the intermediate variable $u = L / t = \sqrt{v}$ with $|dt| = L u^{-2}\,du$, the equivalent integral is $2\int_0^\infty u^{9/2}\,|u^2 - 3|\,e^{-u^2}\,du$). Thus the **exact transformed Stieltjes integral identity** (`stieltjes_substitution_from_original_integrand_symbolic_verified: true`) is
   $$
   \boxed{\int_0^\infty \sqrt{t}\,\bigl|\phi_L'(t)\bigr|\,dt = L^{-11/2}\,J, \qquad J := \int_0^\infty v^{7/4}\,\bigl|v - 3\bigr|\,e^{-v}\,dv = \int_0^3 (3 - v)v^{7/4} e^{-v}\,dv + \int_3^\infty (v - 3)v^{7/4} e^{-v}\,dv.}
   $$
   Using $\frac{d}{dv}\bigl(-v^{11/4} e^{-v}\bigr) = \bigl(v - \frac{11}{4}\bigr)v^{7/4} e^{-v}$, we have $(v - 3)v^{7/4} e^{-v} = \frac{d}{dv}\bigl(-v^{11/4} e^{-v}\bigr) - \frac{1}{4} v^{7/4} e^{-v}$ (`gaussian_symbolic_verified: true`), so integrating on $[0, 3]$ and $[3, \infty)$ yields the exact incomplete-gamma formula
   $$
   \boxed{J = 2\cdot 3^{11/4} e^{-3} - \frac{1}{4}\Bigl[\Gamma\!\left(\frac{11}{4}\right) - 2\,\gamma\!\left(\frac{11}{4},\, 3\right)\Bigr] = \bigl[2.152085805199425799330038459692797743742 \pm 2.00 \times 10^{-39}\bigr]}
   $$
   (`I_abs_direct_vs_ibp_agree: true`, cross-checked against both direct $v$-quadrature on $(0, 3) \cup (3, \infty)$, direct $u$-quadrature $2\int_0^\infty u^{9/2}|u^2 - 3|e^{-u^2}\,du$, and the reference value $J \approx 2.1520858051994258$). Multiplying by $\frac{X^5}{(rs)^3} L^{-11/2} = \frac{X^5}{(rs)^3}\frac{(rs)^{11/2}}{X^{11/2}(r^2 + s^2)^{11/4}} = X^{-1/2}\frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}}$ establishes the **proved uniform pairwise inequality** for all coprime squarefree $r, s \ge 1$ and all $X > 0$:
   $$
   \boxed{\bigl|E_{r,s}(X)\bigr| \le (3 J)\,2^{\omega(rs)}\,X^{-1/2}\,\frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}} \le C\,2^{\omega(rs)}\,X^{-1/2}\,\frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}},}
   $$
   where the constant obtained from this Stieltjes estimate (without claiming global optimality across all possible integration methods) is
   $$
   3 J = \bigl[6.456257415598277397990115379078393231226 \pm 2.00 \times 10^{-39}\bigr] < 7 < 8
   $$
   (`three_J_lt_8_certified: true`, cross-checked against $3J \approx 6.4562574155982774$). Furthermore, since $\Gamma(11/4) - 2\gamma(11/4, 3) > -\Gamma(11/4)$ and $\Gamma(11/4) = \frac{7}{4}\cdot\frac{3}{4}\Gamma(3/4) = \frac{21}{16}\Gamma(3/4)$, we have the conservative closed-form upper bound
   $$
   3 J \le 6\cdot 3^{11/4} e^{-3} + \frac{63}{64}\Gamma\!\left(\frac{3}{4}\right) = \bigl[7.334728145729494680425400563915115544141 \pm 2.00 \times 10^{-39}\bigr] < 8
   $$
   (`three_J_closed_lt_8_certified: true`), so $C = 8$ is a convenient proved integer upper bound (`C_pair_convenient_upper_bound: 8`). Under simultaneous rescaling $(r, s) \mapsto (\lambda r, \lambda s)$, the factor $\frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}}$ is homogeneous of degree $5 - 11/2 = -1/2$ (`homogeneous_degree_neg_half_symbolic_verified: true`). Certified in 256-bit Arb across $(r, s) = (2, 3)$ ($X \in \{4, 16, 64, 256\}$) and $(r, s, X) = (29, 31, 30)$, where the $(3J)$-bound evaluates to $[0.1272195244161310364758966152354706030606 \pm 2.00 \times 10^{-40}] > |E_{29,31}(30)| = [0.002633650286935197 \pm 3.20 \times 10^{-19}]$ (and the $C = 8$ bound evaluates to $0.1576387262\dots > |E_{29,31}(30)|$, `all_pairwise_error_bounds_certified: true`).

6. **Summing Over $1 \le r, s \le A$ (Including Unequal Factors) and Growing-Range Upper-Bound Condition**:
   - **Summed Error over All Coprime Pairs $1 \le r, s \le A$**:
     By AM–GM, $r^2 + s^2 \ge 2rs$ for all $r, s \ge 1$ (equal and unequal factors alike), so
     $$
     \frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}} \le \frac{(rs)^{5/2}}{(2rs)^{11/4}} = 2^{-11/4}\,r^{-1/4}\,s^{-1/4}
     $$
     (or equivalently, ordering $1 \le r \le s \le A$ by symmetry gives $r^2 + s^2 > s^2 \implies \frac{(rs)^{5/2}}{(r^2 + s^2)^{11/4}} \le r^{5/2} s^{-3}$, where $\sum_{1 \le r \le s} 2^{\omega(r)} r^{5/2} \ll 2^{\omega(s)} s^{7/2}\log(2s)$ and $\sum_{1 \le s \le A} 4^{\omega(s)} s^{1/2}\log(2s) \ll A^{3/2}\log^4(2A)$). Since $2^{\omega(rs)} = 2^{\omega(r)} 2^{\omega(s)}$ for $\gcd(r, s) = 1$, summing over all coprime pairs $1 \le r, s \le A$ factors into a square:
     $$
     \sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}} \bigl|E_{r,s}(X)\bigr| \le 2^{-11/4}\,C\,X^{-1/2}\left(\sum_{1 \le r \le A} 2^{\omega(r)} r^{-1/4}\right)^2.
     $$
     Using $\sum_{r \le A} 2^{\omega(r)} \le \sum_{r \le A} d(r) \le A(\log A + 1)$ and summation by parts gives $\sum_{1 \le r \le A} 2^{\omega(r)} r^{-1/4} \ll A^{3/4}\log(2A) \ll_\varepsilon A^{3/4 + \varepsilon/2}$ for every $\varepsilon > 0$, and therefore
     $$
     \boxed{\sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}} \bigl|E_{r,s}(X)\bigr| \ll \frac{A^{3/2}\log^2(2A)}{\sqrt{X}} = O_\varepsilon\!\left(\frac{A^{3/2 + \varepsilon}}{\sqrt{X}}\right) \qquad \forall \varepsilon > 0.}
     $$
   - **Growing Range $A \le X^{1/3 - \delta}$ and Upper-Bound Exponent Condition vs. Necessity**:
     For $A \le X^{1/3 - \delta}$ with $0 < \delta < 1/3$, the $\varepsilon$-inflated upper bound $O_\varepsilon(A^{3/2 + \varepsilon} / \sqrt{X})$ is majorized by $X^{(1/3 - \delta)(3/2 + \varepsilon) - 1/2} = X^{-\frac{3}{2}\delta + (1/3 - \delta)\varepsilon}$, whose exponent is strictly negative if and only if
     $$
     \boxed{0 < \varepsilon < \frac{3\delta}{2(1/3 - \delta)}}
     $$
     (and in particular choosing $\varepsilon \in \bigl(0, \frac{3}{2}\delta\bigr]$ guarantees $-\frac{3}{2}\delta + (1/3 - \delta)\varepsilon \le -\delta < 0$, giving an $O_\delta(X^{-\delta})$ upper bound $\to 0$). This inequality is a condition on the **exponent of the $\varepsilon$-inflated upper bound** $X^{(1/3-\delta)(3/2+\varepsilon)-1/2}$ (indeed, the uninflated bound $A^{3/2}\log^2(2A)/\sqrt{X} \le X^{-\frac{3}{2}\delta}\log^2(2X) \to 0$ already tends to zero for every $0 < \delta < 1/3$ without any $\varepsilon$-inflation), NOT a necessity claim about the actual error sum (`exponent_identity_symbolic_verified: true`, formalized in Lean `RiemannScope.common_factor_mobius_split_and_valid_growing_range_exponent`).

### 10.3 Attack on the Signed Coprime Block $S(A)$: Benchmarks, $A = 5/2$ Prime-Pair Edge Case, Attempt 1 (Bivariate Euler Product & Boundary Behavior), and Attempt 2 (Complete 4-Step Uniform Convolution/Walfisz Proof) (`section_3_signed_coprime_block_attempts_and_regrouping`)

1. **Balanced Block Regrouping by $q = rs$ with $\kappa(q)$ Appearing Once**:
   On the half-open dyadic block $A \le r, s < 2A$, every coprime pair $(r, s)$ has product $q = rs \in [A^2, 4A^2)$ with $\mu(r)\mu(s) = \mu(rs) = \mu(q)$. Regrouping by $q = rs$ gives
   $$
   \boxed{S(A) := \sum_{\substack{A \le r, s < 2A \\ \gcd(r, s) = 1}} L_{r, s} = \sum_{A^2 \le q < 4 A^2} \mu(q)\,w_A(q), \qquad w_A(q) := \frac{3\sqrt{\pi}}{8}\,\kappa(q)\,q^2 \sum_{\substack{rs = q \\ A \le r, s < 2A \\ \gcd(r, s) = 1}} \frac{1}{(r^2 + s^2)^{5/2}} \ge 0,}
   $$
   where $\kappa(q) = \frac{1}{\zeta(2)}\prod_{p \mid q}\frac{p}{p + 1}$ appears **once** in $w_A(q)$.

2. **Exact 2D Antiderivative, Non-Asymptotic $O(A)$ Benchmark, and Two-Prime Stratum $S_{2\text{-prime}}(A)$ (Including the $A = 5/2$ Single-Prime Block)**:
   - **Exact 2D Antiderivative & Explicit Non-Asymptotic $O(A)$ Bound**:
     The homogeneous kernel $K(r, s) := \frac{(rs)^2}{(r^2 + s^2)^{5/2}}$ has the exact 2D antiderivative (`antiderivative_symbolic_verified: true`, `box_integral_symbolic_verified: true`):
     $$
     \frac{\partial^2}{\partial r\,\partial s}\!\left(\frac{rs}{3\sqrt{r^2 + s^2}}\right) = \frac{(rs)^2}{(r^2 + s^2)^{5/2}}, \qquad \iint_{[1, 2]^2} \frac{(xy)^2}{(x^2 + y^2)^{5/2}}\,dx\,dy = \frac{15\sqrt{2} - 8\sqrt{5}}{30} \approx 0.1108219872.
     $$
     Using $\kappa(rs) \le \frac{1}{\zeta(2)} = \frac{6}{\pi^2}$ and $(r^2 + s^2)^{-5/2} \le 2^{-5/2}(rs)^{-5/2}$ so $K(r, s) \le 2^{-5/2}(rs)^{-1/2}$, along with $\sum_{A \le r < 2A} r^{-1/2} \le 2(\sqrt{2}-1)\sqrt{A} + A^{-1/2}$ for all $A \ge 1$, we obtain the explicit non-asymptotic unsigned bound valid for all $A \ge 1$:
     $$
     \boxed{\bigl|S(A)\bigr| \le S_{\mathrm{abs}}(A) := \sum_{A^2 \le q < 4A^2} |\mu(q)|\,w_A(q) \le \frac{9}{16\sqrt{2}\,\pi^{3/2}}\bigl(2(\sqrt{2} - 1)\sqrt{A} + A^{-1/2}\bigr)^2 \le C_{\mathrm{block}}\,A \qquad \forall A \ge 1,}
     $$
     where $C_{\mathrm{block}} := \frac{9(2\sqrt{2} - 1)^2}{16\sqrt{2}\,\pi^{3/2}} = [0.2388020390525650552804189993008810046850 \pm 2.00 \times 10^{-40}] < 0.239$ (`all_unsigned_bounds_certified: true`). Moreover, writing $S_{\mathrm{pos}}(A)$ and $S_{\mathrm{neg}}(A)$ for the sums of $w_A(q)$ over $\mu(q) = +1$ and $\mu(q) = -1$, we have the **exact algebraic parity identity**
     $$
     S_{\mathrm{abs}}(A) - S(A) = 2 S_{\mathrm{neg}}(A) \ge 0, \qquad S_{\mathrm{abs}}(A) + S(A) = 2 S_{\mathrm{pos}}(A) \ge 0,
     $$
     which proves $|S(A)| \le S_{\mathrm{abs}}(A)$ identically without overlap-only ball comparisons (`parity_decomposition_S_abs_mp_S_eq_2_S_neg_pos_certified: true`).
   - **Two-Prime Stratum ($\omega(q) = 2$) and the $A = 5/2$ Single-Prime Exception**:
     For every $A > 1$, any squarefree $q = rs$ with $A \le r, s < 2A$, $\gcd(r, s) = 1$, and $\omega(q) = \omega(r) + \omega(s) = 2$ must satisfy $\omega(r) = \omega(s) = 1$ because $r, s \ge \lceil A\rceil \ge 2$ cannot equal $1$. Thus the $\omega(q) = 2$ stratum consists of ordered pairs of **distinct primes** $r = p_1 \ne p_2 = s$ in $[A, 2A)$, each carrying $\mu(p_1 p_2) = +1$.
     - *Exception when $[A, 2A)$ contains fewer than two primes ($A = 5/2$)*: At $A = 5/2$, $[5/2, 5) \cap \mathbb{Z} = \{3, 4\}$ contains only the single prime $3$ (and the nonsquarefree integer $4$ with $\mu(4) = 0$), so there are no pairs of distinct primes in $[5/2, 5)$ and $S_{2\text{-prime}}(5/2) = 0$ (`single_prime_block_A_5_over_2_two_prime_sum_zero: true`).
     - *Strict positivity for $A \ge 6$ (and $A \in \{2, 3, 4, 9/2\}$) and asymptotic*: By Ramanujan's strengthening of Bertrand's postulate (1919), $[A, 2A)$ contains at least two distinct primes for every $A \ge 6$ (as well as for $A \in \{2, 3, 4, 9/2\}$), and by the prime number theorem:
       $$
       \boxed{S_{2\text{-prime}}(A) = \sum_{\substack{A \le p_1, p_2 < 2A \\ p_1 \ne p_2}} \frac{3\sqrt{\pi}}{8}\,\kappa(p_1 p_2)\,\frac{(p_1 p_2)^2}{(p_1^2 + p_2^2)^{5/2}} = \left(\frac{3\sqrt{\pi}}{8\zeta(2)}\,\frac{15\sqrt{2} - 8\sqrt{5}}{30} + o(1)\right)\frac{A}{\log^2 A} > 0 \qquad (A \ge 6).}
       $$
       Therefore, any asymptotic saving below $\frac{A}{\log^2 A}$ requires signed cancellation between the positive $\omega(q) = 2$ prime-pair stratum (together with even $\omega(q) \ge 4$) and the negative odd-$\omega(q) \ge 3$ strata ($\mu(q) = -1$).

3. **Attempt 1 — Prime-by-Prime Bivariate Euler Product, Local vs. Infinite Product Nonvanishing, and Boundary Behavior at $s_1 = s_2 = 1/2$**:
   Removing the smooth homogeneous weight $K(r, s)$ via 2D Mellin inversion reduces the arithmetic core of $S(A)$ to the bivariate Dirichlet series of the coprime multiplicative weight $f(r, s) := \mathbf{1}_{\gcd(r,s)=1}\,\mu(r)\mu(s)\prod_{p \mid rs}\frac{p}{p + 1}$. On $\operatorname{Re} s_1 > 1, \operatorname{Re} s_2 > 1$, $f(r, s)$ factors prime-by-prime:
   $$
   \boxed{\mathcal{D}(s_1, s_2) := \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}} \frac{\mu(r)\mu(s)\widetilde{\kappa}(rs)}{r^{s_1} s^{s_2}} = \prod_p \left(1 - \frac{p}{p + 1}\bigl(p^{-s_1} + p^{-s_2}\bigr)\right) = \frac{\mathcal{H}(s_1, s_2)}{\zeta(s_1)\zeta(s_2)},}
   $$
   where $\mathcal{H}(s_1, s_2) := \prod_p \mathcal{H}_p(p^{-s_1}, p^{-s_2})$ has local Euler factor
   $$
   \mathcal{H}_p(x, y) := \frac{1 - \frac{p}{p + 1}(x + y)}{(1 - x)(1 - y)} = 1 + \frac{\frac{1}{p + 1}(x + y) - xy}{(1 - x)(1 - y)}.
   $$
   We distinguish **local factor nonvanishing**, **infinite product convergence**, and **boundary behavior on $\operatorname{Re}(s_1 + s_2) = 1$**:
   - **Open Domain of Absolute Convergence $\Omega_{\mathcal{H}}$**: Since $|\frac{1}{p+1}(p^{-s_1} + p^{-s_2})| \ll p^{-1 - \min(\operatorname{Re} s_1, \operatorname{Re} s_2)}$ and $|p^{-(s_1 + s_2)}| = p^{-\operatorname{Re}(s_1 + s_2)}$, the infinite Euler product $\mathcal{H}(s_1, s_2) = \prod_p \mathcal{H}_p(p^{-s_1}, p^{-s_2})$ converges absolutely and defines a holomorphic function on the open domain
     $$
     \Omega_{\mathcal{H}} := \bigl\{(s_1, s_2) \in \mathbb{C}^2 : \operatorname{Re} s_1 > 0,\; \operatorname{Re} s_2 > 0,\; \operatorname{Re}(s_1 + s_2) > 1\bigr\}.
     $$
   - **Local Factor Nonvanishing on $\operatorname{Re} s_1 \ge 1/2, \operatorname{Re} s_2 \ge 1/2$ vs. Infinite Product Nonvanishing on the Interior Region**:
     For $\operatorname{Re} s_1 \ge 1/2$, $\operatorname{Re} s_2 \ge 1/2$, and every prime $p \ge 2$, $|p^{-s_i}| \le p^{-1/2}$, so by AM–GM (`all_attempt1_local_factors_strictly_positive: true`, Lean `RiemannScope.signed_block_bivariate_euler_nonvanishing_and_parity_regrouping`):
     $$
     \boxed{\left|\frac{p}{p + 1}\bigl(p^{-s_1} + p^{-s_2}\bigr)\right| \le \frac{2\sqrt{p}}{p + 1} = 1 - \frac{(\sqrt{p} - 1)^2}{p + 1} < 1 \qquad \forall p \ge 2.}
     $$
     Hence every individual local factor $\mathcal{H}_p(p^{-s_1}, p^{-s_2})$ is strictly nonzero on $\operatorname{Re} s_1 \ge 1/2, \operatorname{Re} s_2 \ge 1/2$. On the intersection with the absolute-convergence domain,
     $$
     \Omega_{\mathcal{H}} \cap \{\operatorname{Re} s_1 \ge 1/2,\; \operatorname{Re} s_2 \ge 1/2\} = \bigl\{\operatorname{Re} s_1 \ge 1/2,\; \operatorname{Re} s_2 \ge 1/2,\; \operatorname{Re}(s_1 + s_2) > 1\bigr\},
     $$
     absolute convergence $\sum_p |\mathcal{H}_p(p^{-s_1}, p^{-s_2}) - 1| < \infty$ together with nonvanishing of every local factor guarantees that the **infinite product $\mathcal{H}(s_1, s_2)$ is holomorphic and strictly nonzero**. In particular, at any off-critical zero $\rho_0$ of $\zeta(s_1)$ with $\operatorname{Re}\rho_0 > 1/2$ and any $\operatorname{Re} s_2 \ge 1/2$, we have $\operatorname{Re}(\rho_0 + s_2) > 1$, so $(\rho_0, s_2)$ lies strictly inside $\Omega_{\mathcal{H}}$ and $\mathcal{H}(\rho_0, s_2) \ne 0$ can never vanish to cancel the pole of $\frac{1}{\zeta(s_1)\zeta(s_2)}$.
   - **Boundary Check at $s_1 = s_2 = 1/2$ and Zero of $1/\zeta(s_1 + s_2)$ at $s_1 + s_2 = 1$**:
     At the boundary point $s_1 = s_2 = 1/2$ (where $s_1 + s_2 = 1 \notin \Omega_{\mathcal{H}}$), each individual local factor is still positive ($\mathcal{H}_p(p^{-1/2}, p^{-1/2}) = \frac{p - 2\sqrt{p} + 1}{(p + 1)(1 - p^{-1/2})^2} = \frac{p}{p + 1} > 0$), but
     $$
     \mathcal{H}_p(p^{-1/2}, p^{-1/2}) - 1 = -\frac{1}{p + 1} = -\frac{1}{p} + O(p^{-2}), \qquad \sum_p \bigl(\mathcal{H}_p(p^{-1/2}, p^{-1/2}) - 1\bigr) = -\infty
     $$
     (`boundary_s1_eq_s2_eq_half_divergence_symbolic_verified: true`), so the infinite product $\prod_p \mathcal{H}_p(p^{-1/2}, p^{-1/2})$ diverges to $0$ on the boundary line $s_1 + s_2 = 1$. Consistently, when the coprimality condition $\gcd(r, s) = 1$ is factored out as $\mathcal{H}(s_1, s_2) = \frac{\mathcal{G}_{\mathrm{coprime}}(s_1, s_2)}{\zeta(s_1 + s_2)}$ (with $\mathcal{G}_{\mathrm{coprime}}(s_1, s_2)$ converging absolutely on $\operatorname{Re}(s_1 + s_2) > 1/2$), the factor $\frac{1}{\zeta(s_1 + s_2)}$ has a **simple zero** at $s_1 + s_2 = 1$ (because $\zeta(s_1 + s_2)$ has a simple pole at $s_1 + s_2 = 1$).

4. **Attempt 2 — Direct Regrouping by $q$, Logarithmic Möbius Identity, Decoupled $L^2$ Identity, and Complete 4-Step Uniform Convolution/Walfisz Proof**:
   - **Direct Regrouping by $q$ and Exact Exchange with $\mu(q)\log q = -\sum_{uv=q}\Lambda(u)\mu(v)$**:
     Whenever $r_{\min} = \lceil A\rceil \ge 2$ ($A > 1$), every $q \in [r_{\min}^2, r_{\max}^2]$ satisfies $q \ge 4 > 1$, so $\log q > 0$. Substituting $\mu(q)\log q = -\sum_{uv = q}\Lambda(u)\mu(v)$ into $S(A) = \sum_{A^2 \le q < 4A^2} \mu(q) w_A(q)$ and exchanging summation order yields
     $$
     \boxed{S(A) = -\sum_{2 \le u < 4A^2} \Lambda(u) \sum_{\lceil A^2 / u\rceil \le v < \lceil 4A^2 / u\rceil} \mu(v)\,\frac{w_A(uv)}{\log(uv)} \qquad (A > 1),}
     $$
     certified in 256-bit Arb across all $10$ applicable blocks $A \in \{2, 5/2, 4, 9/2, 6, 8, 16, 32, 35, 64\}$ (`applicable_log_mobius_count: 10`, `all_log_mobius_exchanges_enclose_zero: true`), while $A = 1/2$ (empty block) and $A = 1$ ($q = 1$, where $\log 1 = 0$) are explicitly marked `"SKIPPED"` (`skipped_log_mobius_count: 2`).
   - **Preserved Decoupled $L^2$-Integral Inclusion-Exclusion Identity**:
     Expanding $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ decouples $\zeta(2)\kappa(rs) = \widetilde{\kappa}(r)\widetilde{\kappa}(s)$ (for $\gcd(r, s) = 1$) into nonnegative rank-one $L^2$ Gaussian integrals:
     $$
     \boxed{S(A) = \frac{1}{\zeta(2)}\sum_{1 \le e < 2A}\frac{\mu(e)\,\widetilde{\kappa}(e)^2}{e}\,I_e\!\left(\frac{A}{e}\right), \qquad I_e(B) := \int_0^\infty u^4\Biggl(\sum_{\substack{B \le r < 2B \\ \gcd(r, e) = 1}}\frac{\mu(r)\widetilde{\kappa}(r)}{r^3}\,e^{-u^2/r^2}\Biggr)^2 du \ge 0,}
     $$
     certified in 256-bit Arb across all $12$ tested blocks (`all_direct_vs_decoupled_L2_enclose_zero: true`).
   - **Sign Change of the Mixed Partial $K_{rs}(r, s)$ and Exact Derivative Bounds on $[A, 2A]^2$**:
     For the smooth kernel $K(r, s) := \frac{(rs)^2}{(r^2 + s^2)^{5/2}}$, symbolic differentiation (`K_rs_symbolic_verified: true`) gives
     $$
     \boxed{K_{rs}(r, s) := \frac{\partial^2 K}{\partial r\,\partial s}(r, s) = \frac{rs\bigl(-6r^4 + 23r^2 s^2 - 6s^4\bigr)}{(r^2 + s^2)^{9/2}}, \qquad K_{rs}(1, 1) = \frac{11}{16\sqrt{2}} > 0, \qquad K_{rs}(1, 2) = -\frac{4\sqrt{5}}{625} \approx -0.0143108351 < 0}
     $$
     (`K_rs_at_1_2_strictly_negative: true`; whereas $\frac{\partial^2}{\partial r\partial s}\bigl(\frac{rs}{3\sqrt{r^2+s^2}}\bigr) = K(r, s) > 0$ is the mixed derivative of the *antiderivative* of $K$, not of $K$ itself). Replacing the invalid sign claim with absolute derivative bounds on $[A, 2A]^2$ (where $r, s \ge A \implies r^2 + s^2 \ge \max(2A^2, 2rs)$) gives:
     $$
     \bigl|K(r, s)\bigr| \le 2^{-5/2} A^{-1} = \frac{2}{8\sqrt{2}}\,A^{-1}, \qquad \bigl|K_r(r, s)\bigr| = \frac{rs^2|2s^2 - 3r^2|}{(r^2+s^2)^{7/2}} \le \frac{3}{4\sqrt{2}} A^{-2} = \frac{6}{8\sqrt{2}}\,A^{-2}, \qquad \bigl|K_s(r, s)\bigr| \le \frac{3}{4\sqrt{2}} A^{-2} = \frac{6}{8\sqrt{2}}\,A^{-2}, \qquad \bigl|K_{rs}(r, s)\bigr| \le \frac{11}{8\sqrt{2}} A^{-3},
     $$
     so the exact component sum for the 2D Stieltjes variation constant (repairing the arithmetic error in `TASK-TC-053R`, `M_var_symbolic_sum_verified: true`, `M_var_components_match_exact_formula: true`) is
     $$
     \boxed{M_{\mathrm{var}} := 2^{-5/2} + 2\cdot\frac{3}{4\sqrt{2}} + \frac{11}{8\sqrt{2}} = \frac{2 + 12 + 11}{8\sqrt{2}} = \frac{25}{8\sqrt{2}} = \bigl[2.209708691207961013752638631577653247765 \pm 2.00 \times 10^{-39}\bigr].}
     $$
   - **Complete Four-Step Uniform Convolution and Korobov–Vinogradov–Walfisz Proof of $|S(A)| \ll A e^{-c\Phi(A)}$**:
     To eliminate the growing coprimality parameter completely before applying Mertens bounds, we execute the four-step uniform convolution proof:
     1. *Step 1 — Bivariate Dirichlet Convolution $f = (\mu \otimes \mu) * h$, Repaired Euler-Product Tail Majorant $B(P, \theta)$, and Regenerated $C_{h, \theta}$ Enclosures*:
        Since $\mathcal{D}(s_1, s_2) = \sum_{r,s \ge 1} f(r, s) r^{-s_1} s^{-s_2} = \frac{1}{\zeta(s_1)\zeta(s_2)}\mathcal{H}(s_1, s_2)$ where $\frac{1}{\zeta(s_1)\zeta(s_2)} = \sum_{m, n \ge 1}\mu(m)\mu(n) m^{-s_1} n^{-s_2}$, expanding $\mathcal{H}(s_1, s_2) = \sum_{d, e \ge 1} h(d, e) d^{-s_1} e^{-s_2}$ gives the exact identity $f(r, s) = \sum_{d \mid r,\, e \mid s} h(d, e)\,\mu(r/d)\,\mu(s/e)$. At each prime $p$, the local series
        $$
        \mathcal{H}_p(x, y) = \frac{1 - \frac{p}{p + 1}(x + y)}{(1 - x)(1 - y)} = 1 + \frac{1}{p + 1}\left(\frac{x}{1 - x} + \frac{y}{1 - y}\right) - \frac{p - 1}{p + 1}\frac{xy}{(1 - x)(1 - y)}
        $$
        (`h_local_series_identity_symbolic_verified: true`) yields the explicit prime-power values of the multiplicative function $h(d, e)$:
        $$
        \boxed{h(1, 1) = 1, \qquad h(p^a, 1) = h(1, p^b) = \frac{1}{p + 1} \quad (a, b \ge 1), \qquad h(p^a, p^b) = -\frac{p - 1}{p + 1} \quad (a, b \ge 1),}
        $$
        verified by exact rational arithmetic across all $40 \times 40 = 1600$ pairs $1 \le r, s \le 40$ (`all_h_convolutions_exact_up_to_40: true`). For every $\theta > 1/2$, the absolute Dirichlet series is
        $$
        C_{h, \theta} := \sum_{d, e \ge 1} \frac{|h(d, e)|}{(de)^\theta} = \prod_p F_p(\theta), \qquad F_p(\theta) := 1 + \frac{2}{(p + 1)(p^\theta - 1)} + \frac{p - 1}{(p + 1)(p^\theta - 1)^2}.
        $$
        - *Failure of the discarded majorant at $\theta = 3/4, p = 2003$*: In `TASK-TC-053R`, the prime-tail bound omitted the quadratic term $\frac{p-1}{(p+1)(p^\theta - 1)^2} \sim p^{-2\theta} = p^{-3/2}$ (which dominates $\frac{2}{(p+1)(p^\theta - 1)} \sim 2 p^{-(1+\theta)} = 2 p^{-7/4}$ whenever $1/2 < \theta < 1$). At $p = 2003, \theta = 3/4$, 256-bit Arb evaluation (`discarded_majorant_fails_at_2003_certified: true`) gives
          $$
          \log F_{2003}(3/4) = \bigl[0.00001456325666387955721403184752881533273340 \pm 2.00 \times 10^{-44}\bigr] > 4(2003)^{-7/4} = \bigl[0.000006669884755011093590413754887978666600517 \pm 2.00 \times 10^{-45}\bigr].
          $$
          Thus the discarded `TASK-TC-053R` certificate lacked a valid supporting majorant (we do not claim its numerical endpoints are disproved).
        - *Proved replacement Euler-tail bound $B(P, \theta)$ for all $\theta > 1/2$ and integers $P \ge 2$*: Fix an integer $P \ge 2$ and $\theta > 1/2$, and set $a := (1 - P^{-\theta})^{-1} > 1$. For every prime $p > P$, we have $p^{-\theta} < P^{-\theta}$, so $p^\theta - 1 = p^\theta(1 - p^{-\theta}) > p^\theta(1 - P^{-\theta}) = a^{-1} p^\theta$, together with $p + 1 > p$ and $\frac{p - 1}{p + 1} < 1$. Therefore
          $$
          0 < \log F_p(\theta) \le F_p(\theta) - 1 = \frac{2}{(p + 1)(p^\theta - 1)} + \frac{p - 1}{(p + 1)(p^\theta - 1)^2} \le 2 a\,p^{-1-\theta} + a^2\,p^{-2\theta}.
          $$
          Comparing the prime sums with the corresponding sums over all integers $n > P$ and using the decreasing-integrand bound $\sum_{n > P} n^{-\alpha} \le \int_P^\infty x^{-\alpha}\,dx = \frac{P^{1 - \alpha}}{\alpha - 1}$ for $\alpha \in \{1 + \theta, 2\theta\}$ (both $> 1$ since $\theta > 1/2$) establishes
          $$
          \boxed{0 \le \sum_{p > P} \log F_p(\theta) \le B(P, \theta) := \frac{2a}{\theta P^\theta} + \frac{a^2}{(2\theta - 1) P^{2\theta - 1}}, \qquad a := \bigl(1 - P^{-\theta}\bigr)^{-1}.}
          $$
          At $P = 2000$, this gives $B(2000, 3/4) = \bigl[0.05396838768546253991162240291534870105926 \pm 2.00 \times 10^{-41}\bigr]$ and $B(2000, 1) = \bigl[0.001501000625375218875070351583996100101076 \pm 2.00 \times 10^{-42}\bigr]$ (`multi_cutoff_consistency_P_500_1000_2000_5000_certified: true`, where increasing arithmetic bit precision at a fixed prime cutoff $P$ does not reduce the truncation interval $[0, B(P, \theta)]$). Multiplying the finite product $\prod_{p \le 2000} F_p(\theta)$ by $\exp\bigl([0, B(2000, \theta)]\bigr)$ certifies
          $$
          C_{h, 3/4} := \sum_{d, e \ge 1}\frac{|h(d, e)|}{(de)^{3/4}} = \bigl[9.0 \pm 0.528\bigr] < \infty, \qquad C_{h, 1} := \sum_{d, e \ge 1}\frac{|h(d, e)|}{de} = \bigl[3.61 \pm 6.80 \times 10^{-3}\bigr] < \infty
          $$
          (with exact 256-bit outward-rounded endpoint enclosures $9.0271284729 < C_{h, 3/4} < 9.5276940167$ and $3.6032064221 < C_{h, 1} < 3.6086189151$ at $P = 2000$, and nested enclosure narrowing across $P \in \{500, 1000, 2000, 5000\}$).
        Substituting $f(r, s) = \sum_{dm = r,\, en = s} h(d, e)\mu(m)\mu(n)$ into $S(A) = \frac{3\sqrt{\pi}}{8\zeta(2)}\sum_{A \le r, s < 2A} f(r, s) K(r, s)$ gives the exact decomposition (certified across all $12$ blocks, `all_direct_vs_h_convolution_enclose_zero: true`):
        $$
        \boxed{S(A) = \frac{3\sqrt{\pi}}{8\zeta(2)}\sum_{1 \le d, e < 2A} h(d, e)\,T_{d, e}(A), \qquad T_{d, e}(A) := \sum_{A/d \le m < 2A/d}\,\sum_{A/e \le n < 2A/e} \mu(m)\,\mu(n)\,K(dm, en).}
        $$
     2. *Step 2 — Uniform Korobov–Vinogradov–Walfisz Saving on the Main Range $1 \le d, e \le \sqrt{A}$ for $A \ge A_0 := e^{2e}$*:
        In $T_{d, e}(A)$, the arithmetic weights $\mu(m)$ and $\mu(n)$ are the **ordinary unweighted Möbius function** with **no coprimality restriction**. Fix the explicit large-$A$ threshold $A \ge A_0 := e^{2e} \approx 229.6516640835$, so that for all $1 \le d, e \le \sqrt{A}$, the lower endpoints $B_1 := A/d \ge \sqrt{A} \ge e^e$ and $B_2 := A/e \ge \sqrt{A} \ge e^e$ lie inside $[e^e, \infty)$ where $\log\log x \ge 1$ and $\Phi(x) := (\log x)^{3/5}(\log\log x)^{-1/5} > 0$ is strictly increasing (since $(\log\Phi(x))' = \frac{3\log\log x - 1}{5 x\log x\log\log x} \ge \frac{2}{5 x\log x\log\log x} > 0$). Furthermore, on $x \ge e^e$, the function $x \mapsto (\log x)^{-1/5}(\log\log x)^{-1/5}$ is strictly decreasing, so $\Phi(\sqrt{A}) = 2^{-3/5}(\log A)^{3/5}(\log\log\sqrt{A})^{-1/5} \ge 2^{-3/5}\Phi(A)$. Define the 1D summatory functions $M_{B_1}(u) := \sum_{B_1 \le m \le u}\mu(m) = M(u) - M(B_1^-)$ and $M_{B_2}(v) := \sum_{B_2 \le n \le v}\mu(n) = M(v) - M(B_2^-)$, which vanish at their lower endpoints $M_{B_1}(B_1^-) = M_{B_2}(B_2^-) = 0$. By the unconditional Korobov (1958)–Vinogradov (1958)–Walfisz (1963, *Weylsche Exponentialsummen in der neueren Zahlentheorie*, Ch. V, §5, Satz 2) theorem for $M(x) = \sum_{m \le x}\mu(m)$, there exist absolute constants $C_{\mathrm{W}} > 0$ and $c_0 > 0$ such that $|M(x)| \le C_{\mathrm{W}}\,x\exp\bigl(-c_0\Phi(x)\bigr)$ for all $x \ge e^e$. Hence for all $A \ge e^{2e}$ and all $u \in [B_1, 2B_1]$, $v \in [B_2, 2B_2]$ with $B_1, B_2 \ge \sqrt{A} \ge e^e$:
        $$
        \bigl|M_{B_1}(u)\bigr| \le 4 C_{\mathrm{W}}\,\frac{A}{d}\,e^{-c_1\Phi(A)}, \qquad \bigl|M_{B_2}(v)\bigr| \le 4 C_{\mathrm{W}}\,\frac{A}{e}\,e^{-c_1\Phi(A)} \qquad \bigl(c_1 := 2^{-3/5} c_0 > 0\bigr).
        $$
        Applying 2D Stieltjes summation by parts to $T_{d, e}(A) = \int_{B_1^-}^{2B_1^-} \int_{B_2^-}^{2B_2^-} \widetilde{K}_{d,e}(u, v)\,dM_{B_1}(u)\,dM_{B_2}(v)$ with $\widetilde{K}_{d,e}(u, v) := K(du, ev)$ produces four non-zero terms (since $M_{B_1}(B_1^-) = M_{B_2}(B_2^-) = 0$ kills the lower boundary terms):
        $$
        T_{d, e}(A) = M_{B_1}(2B_1^-) M_{B_2}(2B_2^-) K(2A, 2A) - M_{B_2}(2B_2^-) d\!\int_{B_1}^{2B_1}\! M_{B_1}(u) K_r(du, 2A)\,du - M_{B_1}(2B_1^-) e\!\int_{B_2}^{2B_2}\! M_{B_2}(v) K_s(2A, ev)\,dv + de\!\int_{B_1}^{2B_1}\!\int_{B_2}^{2B_2}\! M_{B_1}(u) M_{B_2}(v) K_{rs}(du, ev)\,du\,dv.
        $$
        Substituting the uniform derivative bounds on $[A, 2A]^2$ ($|K(2A, 2A)| \le 2^{-5/2} A^{-1}$, $d(2B_1 - B_1)\sup|K_r| = A\sup|K_r| \le \frac{3}{4\sqrt{2}} A^{-1}$, $e(2B_2 - B_2)\sup|K_s| = A\sup|K_s| \le \frac{3}{4\sqrt{2}} A^{-1}$, and $de(2B_1 - B_1)(2B_2 - B_2)\sup|K_{rs}| = A^2\sup|K_{rs}| \le \frac{11}{8\sqrt{2}} A^{-1}$, whose coefficients sum to $M_{\mathrm{var}} = \frac{25}{8\sqrt{2}}$) gives
        $$
        \boxed{\bigl|T_{d, e}(A)\bigr| \le 16 C_{\mathrm{W}}^2\,M_{\mathrm{var}}\,\frac{A}{de}\,e^{-2 c_1\Phi(A)} \qquad \text{uniformly in } 1 \le d, e \le \sqrt{A} \text{ for all } A \ge e^{2e},}
        $$
        and summing over $1 \le d, e \le \sqrt{A}$ yields
        $$
        \sum_{1 \le d, e \le \sqrt{A}} |h(d, e)|\,\bigl|T_{d, e}(A)\bigr| \le 16 C_{\mathrm{W}}^2\,M_{\mathrm{var}}\,C_{h, 1}\,A\,e^{-2 c_1\Phi(A)} \qquad \bigl(16 M_{\mathrm{var}} C_{h, 1} = \bigl[127.0 \pm 0.584\bigr],\; 127.39258475 < 16 M_{\mathrm{var}} C_{h, 1} < 127.58394528\bigr).
        $$
     3. *Step 3 — Tail Range $\max(d, e) > \sqrt{A}$, Empty Intervals, Short Intervals, and Polynomial Tail $O(A^{7/8})$*:
        - *Empty intervals ($d \ge 2A$ or $e \ge 2A$)*: If $d \ge 2A$, then $2A/d \le 1$, so $[A/d, 2A/d) \cap \mathbb{Z} = \emptyset$ and $T_{d, e}(A) = 0$ identically (and symmetrically if $e \ge 2A$).
        - *Short intervals ($1 \le d, e < 2A$)*: For $1 \le d < 2A$, the half-open interval $[A/d, 2A/d)$ has length $A/d > 1/2$, so $\#(\mathbb{Z} \cap [A/d, 2A/d)) \le \frac{A}{d} + 1 < \frac{3A}{d}$, and similarly $\#(\mathbb{Z} \cap [A/e, 2A/e)) < \frac{3A}{e}$. Since $|\mu(m)\mu(n)| \le 1$ and $K(dm, en) \le 2^{-5/2} A^{-1}$ for $(dm, en) \in [A, 2A)^2$, every pair $(d, e)$ with $1 \le d, e < 2A$ satisfies the unconditional elementary bound
          $$
          \bigl|T_{d, e}(A)\bigr| \le \left(\frac{3A}{d}\right)\left(\frac{3A}{e}\right)\cdot 2^{-5/2} A^{-1} = \frac{9}{4\sqrt{2}}\,\frac{A}{de}.
          $$
        - *Using $C_{h, 3/4} < \infty$ to bound the tail $\max(d, e) > \sqrt{A}$*: Whenever $\max(d, e) > \sqrt{A}$ and $d, e \ge 1$, we have $de \ge \max(d, e) > A^{1/2}$, so $(de)^{-1} = (de)^{-1/4}(de)^{-3/4} < A^{-1/8}(de)^{-3/4}$. Summing over all contributing tail indices gives
          $$
          \boxed{\sum_{\substack{1 \le d, e < 2A \\ \max(d, e) > \sqrt{A}}} |h(d, e)|\,\bigl|T_{d, e}(A)\bigr| \le \frac{9}{4\sqrt{2}}\,A^{7/8}\sum_{d, e \ge 1}\frac{|h(d, e)|}{(de)^{3/4}} = \frac{9 C_{h, 3/4}}{4\sqrt{2}}\,A^{7/8} = O(A^{7/8}),}
          $$
          where $\frac{9 C_{h, 3/4}}{4\sqrt{2}} = [15.0 \pm 0.638]$ (with exact 256-bit outward-rounded endpoint enclosure $14.3620734065 < \frac{9 C_{h, 3/4}}{4\sqrt{2}} < 15.1584684253$, `tail_bound_coefficient_9_Ch34_over_4sqrt2_certified`).
     4. *Step 4 — Assembly of the Unconditional Signed-Block Saving and Accurate Scope*:
        Combining Steps 1–3 establishes unconditionally on the proved large-$A$ domain $A \ge A_0 := e^{2e}$:
        $$
        \boxed{\bigl|S(A)\bigr| \le \frac{3\sqrt{\pi}}{8\zeta(2)}\left(16 C_{\mathrm{W}}^2 M_{\mathrm{var}} C_{h, 1}\,A\,e^{-2 c_1\Phi(A)} + \frac{9 C_{h, 3/4}}{4\sqrt{2}}\,A^{7/8}\right) \qquad \forall A \ge e^{2e},}
        $$
        with $\Phi(A) = (\log A)^{3/5}(\log\log A)^{-1/5}$ and $c := 2 c_1 = 2^{2/5} c_0 > 0$. On the remaining bounded range $1 \le A < e^{2e}$, the proved non-asymptotic unsigned estimate $|S(A)| \le S_{\mathrm{abs}}(A) \le C_{\mathrm{block}}\,A$ ($C_{\mathrm{block}} < 0.239$) holds directly; enlarging the implied constant to absorb the compact range $[1, e^{2e}]$ yields unconditionally
        $$
        \boxed{\bigl|S(A)\bigr| \ll A\exp\!\bigl(-c\,(\log A)^{3/5}(\log\log A)^{-1/5}\bigr) \ll_D \frac{A}{(\log A)^D} \quad (\forall D > 0), \qquad S(A) = o\!\left(\frac{A}{\log^2 A}\right).}
        $$
        This **rigorously and unconditionally beats both the $O(A)$ unsigned majorant and the positive two-prime stratum $S_{2\text{-prime}}(A) \asymp \frac{A}{\log^2 A}$**. Regarding power savings: a zero-free strip $\operatorname{Re} s > 1 - \eta'$ for $\zeta(s)$ (giving power-saving cancellation in $M(x) = \sum_{m \le x}\mu(m)$) supplies a *conditional route* to a fixed power saving $|S(A)| \le C A^{1 - \eta}$ ($\eta > 0$) through the present convolution method, whereas claiming that a fixed power saving for this particular weighted block $S(A)$ *necessarily* requires a zero-free strip (or is equivalent to one) would require a separate converse proof. Moreover, controlling the single balanced block $S(A)$ on $A \le X^{1/3 - \delta}$ remains distinct from the full grade-interval $L^2$ energy bound $\int_Y^{\tau Y} |Q(X)|^2 \frac{dX}{X} \le C_\varepsilon Y^\varepsilon$ required to close `SUBGATE-TC-043A` / RH.

5. **Edge-Case Regrouping Regressions and 12-Point Balanced-Block Evaluation Table**:
   All edge-case classes are verified in 256-bit Arb (`edge_cases_verified: true`), with the regrouped $q$-sum computed independently by iterating over $q \in [r_{\min}^2, r_{\max}^2]$ and calling `_evaluate_w_A_q_arb`:
   - *Repeated coprime factorizations of the same squarefree $q$*:
     - At $A = 6$, $q = 66 = 2 \cdot 3 \cdot 11$ ($\mu(66) = -1$) has $2$ ordered coprime factorizations in $[6, 12)^2$, namely $(6, 11)$ and $(11, 6)$, with $w_6(66) = [0.005224056775485917310781671764619177988921 \pm 2.00 \times 10^{-41}]$;
     - At $A = 35$, $q = 2310 = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11$ ($\mu(2310) = -1$) has $4$ ordered coprime factorizations in $[35, 70)^2$, namely $(35, 66), (42, 55), (55, 42), (66, 35)$, with $w_{35}(2310) = [0.001527401243306262121849534637683093362364 \pm 2.00 \times 10^{-42}]$.
   - *Nonsquarefree coprime factorizations ($\mu(q) = 0$)*: At $A = 4$, $q = 20 = 4 \times 5 = 5 \times 4$ has $2$ coprime factorizations in $[4, 8)^2$ with positive weight $w_4(20) = [0.01668459039204983979825298513603613054339 \pm 2.00 \times 10^{-41}] > 0$, but $\mu(20) = 0$ annihilates $\mu(20)w_4(20) = 0$.
   - *Single-prime block ($A = 5/2$)*: $[5/2, 5) \cap \mathbb{Z} = \{3, 4\}$ has $2$ coprime pairs $(3, 4)$ and $(4, 3)$ (both nonsquarefree since $\mu(4) = 0$) and only the single prime $3$, so $S(5/2) = S_{\mathrm{abs}}(5/2) = S_{2\text{-prime}}(5/2) = 0$.
   - *Diagonal coprime pair $(r, s) = (1, 1)$*: Occurs if and only if $1 \in [A, 2A)$ (e.g. $A = 1$, where $q = 1$, $\omega(1) = 0$, $\mu(1) = +1$, $S(1) = w_1(1) \approx +0.0714303404$, and `log_mobius_status: "SKIPPED"` because $\log 1 = 0$), whereas for all $A > 1$ any diagonal pair $(r, r)$ has $\gcd(r, r) = r > 1$ (`diagonal_coprime_pair_count == 0`).
   - *Empty block ($A = 1/2$)*: $[1/2, 1) \cap \mathbb{Z} = \emptyset$, so all sum representations equal $0$ (`log_mobius_status: "SKIPPED"`).
   - *Half-open boundary $[A, 2A)$*: At $A = 4$, $r, s \in \{4, 5, 6, 7\}$ excludes $2A = 8$; at $A = 9/2 = 4.5$, $r, s \in \{5, 6, 7, 8\}$ excludes $2A = 9$.

| Block $A$ | Integer Range $[r_{\min}, r_{\max}]$ | Coprime Pairs | $S(A)$ Direct Pair Sum | $S(A)$ Regrouped $q$-Sum | $S(A)$ Decoupled $L^2$-Sum | $S(A)$ $h$-Conv Sum | Log-Möbius Status | $S_{\mathrm{abs}}(A)$ Unsigned Majorant | $S_{2\text{-prime}}(A)$ ($\omega(q)=2$) | $\|S_{\mathrm{odd}}(A)\|$ ($\omega(q)$ odd) | $S_{\mathrm{even}\ge 4,\text{or }0}(A)$ | Non-Asymptotic Bound |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $1/2$ | $\emptyset$ | $0$ | $0$ | $0$ | $0$ | $0$ | `SKIPPED` | $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $[1, 1]$ | $1$ | $+0.0714303404$ | $+0.0714303404$ | $+0.0714303404$ | $+0.0714303404$ | `SKIPPED` | $0.0714303404$ | $0$ | $0$ | $0.0714303404$ | $0.2388020391$ |
| $2$ | $[2, 3]$ | $2$ | $+0.0238727159$ | $+0.0238727159$ | $+0.0238727159$ | $+0.0238727159$ | `CERTIFIED` | $0.0238727159$ | $0.0238727159$ | $0$ | $0$ | $0.2521089044$ |
| $5/2$ | $[3, 4]$ | $2$ | $0$ | $0$ | $0$ | $0$ | `CERTIFIED` | $0$ | $0$ | $0$ | $0$ | $0.2694768881$ |
| $4$ | $[4, 7]$ | $10$ | $-0.0044669136$ | $-0.0044669136$ | $-0.0044669136$ | $-0.0044669136$ | `CERTIFIED` | $0.0351148541$ | $0.0153239703$ | $0.0197908839$ | $0$ | $0.3322953904$ |
| $9/2$ | $[5, 8]$ | $10$ | $-0.0044669136$ | $-0.0044669136$ | $-0.0044669136$ | $-0.0044669136$ | `CERTIFIED` | $0.0351148541$ | $0.0153239703$ | $0.0197908839$ | $0$ | $0.3548222320$ |
| $6$ | $[6, 11]$ | $22$ | $-0.0183496227$ | $-0.0183496227$ | $-0.0183496227$ | $-0.0183496227$ | `CERTIFIED` | $0.0387480338$ | $0.0101992055$ | $0.0285488282$ | $0$ | $0.4243869331$ |
| $8$ | $[8, 15]$ | $36$ | $-0.0222736084$ | $-0.0222736084$ | $-0.0222736084$ | $-0.0222736084$ | `CERTIFIED` | $0.0490629797$ | $0.0098218103$ | $0.0356682941$ | $0.0035728754$ | $0.5194547400$ |
| $16$ | $[16, 31]$ | $164$ | $+0.0109004064$ | $+0.0109004064$ | $+0.0109004064$ | $+0.0109004064$ | `CERTIFIED` | $0.1157340012$ | $0.0489476697$ | $0.0524167974$ | $0.0143695341$ | $0.9071666281$ |
| $32$ | $[32, 63]$ | $612$ | $-0.0329603116$ | $-0.0329603116$ | $-0.0329603116$ | $-0.0329603116$ | `CERTIFIED` | $0.2574233683$ | $0.0554931451$ | $0.1451918400$ | $0.0567383832$ | $1.6892869988$ |
| $35$ | $[35, 69]$ | $750$ | $-0.0243065366$ | $-0.0243065366$ | $-0.0243065366$ | $-0.0243065366$ | `CERTIFIED` | $0.2913348692$ | $0.0698600625$ | $0.1578207029$ | $0.0636541038$ | $1.8361617742$ |
| $64$ | $[64, 127]$ | $2502$ | $-0.0068022108$ | $-0.0068022108$ | $-0.0068022108$ | $-0.0068022108$ | `CERTIFIED` | $0.5414610658$ | $0.1087909087$ | $0.2741316383$ | $0.1585385188$ | $3.2568760373$ |

### 10.4 Trivial-Zero Lean 4 Formalization (`formal/RiemannScope/TrivialZero.lean`), Exact Namespaces, and Scope Verification (`section_4_trivial_zero_lean_formalization_and_scope`)

In [formal/RiemannScope/TrivialZero.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/TrivialZero.lean) (`4` definitions + `10` theorems = `14` declarations, `0` `sorry`, `0` `admit`, `0` custom axioms, imported in [formal/RiemannScope.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope.lean) and registered in `REQUIRED_FORMAL_SOURCES` in [certification.py](file:///c:/Development/Projects/reimann_scope/certification.py) and `FORMAL_SOURCE_FILES` in [scripts/build_formal.py](file:///c:/Development/Projects/reimann_scope/scripts/build_formal.py)), we verified all 14 declarations via `lake env lean --stdin` (`#check`, `#print`, and `#print axioms`) and record their exact namespaces and scope:
1. **Concrete Mathlib-Backed Complex Zeta Theorems in Namespace `RiemannScope.TrivialZero`**:
   - `RiemannScope.TrivialZero.trivialZero_exact (n : ℕ) : riemannZeta (-2 * ((n : ℂ) + 1)) = 0` (`'[propext, Classical.choice, Quot.sound]'`): proves $\zeta(-2(n+1)) = 0$ for all $n \in \mathbb{N}$ directly from Mathlib's `riemannZeta_neg_two_mul_nat_add_one`;
   - `RiemannScope.TrivialZero.trivialZero_worldline_exact (n : ℕ) (k : ℝ) : extendedContinuation riemannZeta k (zeroWorldline (-2 * ((n : ℂ) + 1)) k) = 0` (`'[propext, Classical.choice, Quot.sound]'`): proves transported trivial-zero vanishing along the grade worldline $W_{-2(n+1)}(k)$ by combining `trivialZero_exact` with `RiemannScope.zeroWorldline_is_zero` and `RiemannScope.tau_pos : 0 < tau`;
   - `RiemannScope.TrivialZero.trivialZero_radialLeaf_exact (n : ℕ) (k : ℝ) : normalizedRadialLeaf k (zeroWorldline ⟨-2 * ((n : ℝ) + 1), 0⟩ k) = -2 * ((n : ℝ) + 1) - 1 / 2` (`'[propext, Classical.choice, Quot.sound]'`): proves radial-leaf invariance along the $n$-th trivial-zero worldline;
   - `RiemannScope.TrivialZero.trivialZero_zero_eq_neg_half : riemannZeta 0 = -1 / 2 := riemannZeta_zero` (`'[propext, Classical.choice, Quot.sound]'`): direct wrapper around Mathlib's `riemannZeta_zero` proving $\zeta(0) = -1/2$ (does not reference `trivialZeroLocation 0`).
2. **Definitions, Worldline Helpers, and Scalar Real-Algebra Lemmas in Namespace `RiemannScope` (NOT `RiemannScope.TrivialZero`)**:
   - Definitions `RiemannScope.trivialZeroLocation`, `RiemannScope.normalizedTrivialZeroSlope`, `RiemannScope.commonFactorPairwiseLeadingTerm`, `RiemannScope.bivariateLocalEulerFactor`, and helper lemmas `RiemannScope.tau_pos`, `RiemannScope.zeroWorldline_at_zero`, `RiemannScope.zeroWorldline_is_zero`, `RiemannScope.normalizedRadialLeaf_at_zeroWorldline` live in namespace `RiemannScope`.
   - `RiemannScope.trivial_zero_slope_scale_invariance_and_grade_energy_criterion` (`'[propext, Classical.choice, Quot.sound]'`): scalar real-algebra lemma in `RiemannScope` proving scale-invariance cancellation `a_K * d_aK = d_0` and `normalizedTrivialZeroSlope sgn_m tau_pow_2m fact_2m a_K d_aK = zeta_2m_plus_1` from explicit real hypotheses `h_chain` and `h_reflection`, the triangle-inequality combination `|G_k - c_k| ≤ (C_1 + C_2) * inv_k_sq`, and the grade-interval product bound `E_Y * W_Y ≤ C_eps * log_tau * (Y_pow_eps * Y_pow_neg_2sigma)` followed by modus ponens;
   - `RiemannScope.common_factor_mobius_split_and_valid_growing_range_exponent` (`'[propext, Classical.choice, Quot.sound]'`): scalar real-algebra lemma in `RiemannScope` that receives `h_mobius : mu_dr_ds = ind_coprime * (mu_d ^ 2) * mu_r * mu_s` as an **explicit premise** over $\mathbb{R}$ and proves the case split `(ind_coprime = 0 → mu_dr_ds = 0) ∧ (ind_coprime = 1 → mu_d ^ 2 = 1 → mu_dr_ds = mu_r * mu_s)`, the algebraic cancellation of `X_pow_5` and `rs_cubed` in `commonFactorPairwiseLeadingTerm`, and the upper-bound exponent equivalence `(1 / 3 - delta) * (3 / 2 + eps) - 1 / 2 < 0 ↔ eps < (3 * delta) / (2 * (1 / 3 - delta))`;
   - `RiemannScope.signed_block_bivariate_euler_nonvanishing_and_parity_regrouping` (`'[propext, Classical.choice, Quot.sound]'`): scalar real-algebra lemma in `RiemannScope` proving the single-prime local bivariate Euler-factor ratio identity, the AM–GM inequality `(2 * sqrt_p) / (p + 1) < 1` and strict positivity `0 < 1 - (p / (p + 1)) * (x_1 + x_2)` for `x_1 + x_2 ≤ 2 / sqrt_p`, prime-square cancellation `-(log_p * (-mu_m) + log_p * mu_m) = 0`, and the parity-stratum linear inequalities from `h_parity_decomp`.
   - **External Analytic Attribution**: The arithmetic Möbius factorization over $\mathbb{Z}_{\ge 1}$, the Stieltjes derivation of the replacement pairwise bound $|E_{r,s}(X)| \le (3 J)\,2^{\omega(rs)}X^{-1/2}\frac{(rs)^{5/2}}{(r^2+s^2)^{11/4}}$ ($J = \int_0^\infty v^{7/4}|v - 3|e^{-v}\,dv = 2.1520858052\dots$, $3 J = 6.4562574156\dots \le 6\cdot 3^{11/4}e^{-3} + \frac{63}{64}\Gamma(3/4) < 8$, $C = 8$), infinite Euler-product convergence on $\Omega_{\mathcal{H}}$, the proved Euler-product tail majorant $B(P, \theta)$ for $C_{h,3/4}$ and $C_{h,1}$, the variation constant $M_{\mathrm{var}} = \frac{25}{8\sqrt{2}}$, and the 4-step uniform convolution/Korobov–Vinogradov–Walfisz proof of $|S(A)| \ll A e^{-c\Phi(A)} \ll_D A/(\log A)^D$ ($S(A) = o(A/\log^2 A)$) are proved analytically and certified in 256-bit Arb outside Lean.
3. **Certificate Verifier Repair**:
   In [certification.py](file:///c:/Development/Projects/reimann_scope/certification.py), `certify_trivial_zero` and `certify_worldline` record both `"formal_theorem_reference": "RiemannScope.TrivialZero.trivialZero_exact"` and `"transported_worldline_theorem_reference": "RiemannScope.TrivialZero.trivialZero_worldline_exact"` (verified against `formal/RiemannScope/TrivialZero.lean`).

---

## 11. Liouville Square-Dilation Transfer, Exact Common-Factor Cancellation, Euler–Maclaurin Sub-Transition Expansion, Transition Poisson Summation, Separable Gaussian Decoupling, and Dyadic Parity Obstruction (`TASK-TC-054` / `TASK-TC-054R`)

In `TASK-TC-054` and `TASK-TC-054R` (authored in full in [docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md), implemented in [tc/liouville_square_dilation.py](file:///c:/Development/Projects/reimann_scope/tc/liouville_square_dilation.py), formalized in [formal/RiemannScope/LiouvilleSquareDilation.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/LiouvilleSquareDilation.lean), and certified in [data/tc_liouville_square_dilation.json](file:///c:/Development/Projects/reimann_scope/data/tc_liouville_square_dilation.json)):
1. **Reversible Square-Dilation Transfer (`RiemannScope.LiouvilleSquareDilation.prime_power_square_divisor_moebius_liouville_inversion_nat`, `RiemannScope.LiouvilleSquareDilation.actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat`, `RiemannScope.LiouvilleSquareDilation.reversible_weighted_dilation_norm_and_grade_interval_equivalence`)**:
   Proved $\lambda(n) = \sum_{d^2 \mid n}\mu(n/d^2)$ and $\mu(n) = \sum_{d^2 \mid n}\mu(d)\lambda(n/d^2)$ unconditionally for all $n \ge 1$ via prime-power factorization (and connected to Mathlib's `ArithmeticFunction.cardFactors`, `Nat.factorization`, and `ArithmeticFunction.moebius`), establishing the exact reversible identities
   \[
   Q_\lambda(X) = \sum_{d\ge 1}\frac{Q_\mu(X/d^2)}{d}, \qquad
   Q_\mu(X) = \sum_{d\ge 1}\frac{\mu(d)\,Q_\lambda(X/d^2)}{d},
   \]
   the Mellin transform $\mathcal{M}[Q_\lambda](z) = \frac{\zeta(1+2z)}{2\zeta(1/2+z)}\Gamma(5/4 - z/2)$ on $\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}$ ($z = a + i b$, showing that $\zeta(1+2z) \ne 0$ on $\operatorname{Re} z > 0$ introduces no zeros or poles in $0 < \operatorname{Re} z < 5/2$), and the two-way grade-interval $L^2$ energy equivalence in weight variable $\eta > 0$ ($\|Q_\lambda\|_\eta \le \zeta(1+2\eta)\|Q_\mu\|_\eta$, $\|Q_\mu\|_\eta \le \frac{\zeta(1+2\eta)}{\zeta(2+4\eta)}\|Q_\lambda\|_\eta$, with $\eta\frac{\zeta(1+2\eta)}{\zeta(2+4\eta)} \to \frac{12}{\tau^2}$ as $\eta \downarrow 0$):
   \[
   \left(\forall\varepsilon > 0,\;\int_Y^{\tau Y}|Q_\mu(X)|^2\frac{dX}{X} \ll_\varepsilon Y^\varepsilon\right)
   \Longleftrightarrow
   \left(\forall\varepsilon > 0,\;\int_Y^{\tau Y}|Q_\lambda(X)|^2\frac{dX}{X} \ll_\varepsilon Y^\varepsilon\right).
   \]
2. **Exact Common-Factor Sign Cancellation & Unconstrained Euler–Maclaurin Sub-Transition Expansion (`RiemannScope.LiouvilleSquareDilation.liouville_complete_multiplicativity_and_common_factor_cancellation_nat`, `RiemannScope.LiouvilleSquareDilation.actual_omega_factorization_and_liouville_common_factor_cancellation_nat`, `RiemannScope.LiouvilleSquareDilation.euler_maclaurin_c2_and_subtransition_growing_range_exponent`)**:
   Proved $\lambda(dr)\lambda(ds) = \lambda(d)^2\lambda(r)\lambda(s) = \lambda(r)\lambda(s)$ unconditionally for all $d, r, s \ge 1$, eliminating the coprime-squarefree sieve $\mathbf{1}_{\gcd(d,rs)=1}\mu(d)^2$ so that $d$ runs over all positive integers $\mathbb{Z}_{\ge 1}$ with smooth weight $f_L(d) = d^{-6}e^{-L^2/d^2}$ ($L = \frac{X\sqrt{r^2+s^2}}{rs}$). By Euler–Maclaurin summation on $f(v) = v^{-6}e^{-1/v^2}$ ($c_0 = \frac{3\sqrt{\tau/2}}{8} \approx 0.6646701940895685$, $C_2 = \frac{f'(v_-) - f'(v_+)}{6} \approx 1.8512576670169581$, $C_4 = \frac{1}{720}\int_0^\infty |f^{(4)}(v)|\,dv \approx 8.7523717600353656$; full 256-bit Arb enclosures in [docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md)), the leading pairwise coefficient becomes a constant independent of prime factors of $rs$,
   \[
   L_{r,s}^{(\lambda)} = c_0\,\lambda(r)\lambda(s)\frac{(rs)^2}{(r^2+s^2)^{5/2}}, \qquad c_0 = \frac{3\sqrt{\tau/2}}{8},
   \]
   and the pairwise remainder satisfies $|E_{r,s}^{(\lambda)}(X)| \le C_N 2^{-(N+5)/2} X^{-N}(rs)^{(N-1)/2}$, expanding the valid sub-transition growing range from $A \le X^{1/3-\delta}$ (`TC-053R2`) all the way to $A \le X^{1-\delta}$ ($\delta \in (0, 1)$).
3. **Non-Schwartz Transition Poisson Summation, Certified Sign Changes of $\widehat{f}(\xi)$, Exact Separable Gaussian Decoupling & Global Stieltjes Energy Saving (Attack A), and Dyadic Parity Obstruction (Attack B) (`RiemannScope.LiouvilleSquareDilation.dyadic_parity_energy_and_off_critical_mode_nonvanishing`, `RiemannScope.LiouvilleSquareDilation.abel_scaling_fourier_ratio_and_unequal_block_algebra`)**:
   At the transition scale $L \asymp 1$ ($r, s \asymp X$), $f(v) = |v|^{-6}e^{-1/v^2}$ ($f(0)=0$) is not in $\mathcal{S}(\mathbb{R})$ (since $v^6 f(v) \to 1$), but its periodization lies in $C^1(\mathbb{R}/\mathbb{Z})$ ([DLMF 1.8.14](https://dlmf.nist.gov/1.8#E14)), giving $\sum_{d\ge 1}f_L(d) = L^{-5}\bigl(c_0 + \sum_{k\ge 1}\widehat{f}(kL)\bigr)$, where $\widehat{f}(\xi) = 2\int_0^\infty v^{-6}e^{-1/v^2}\cos(\tau\xi v)\,dv$ is **not positive definite** (certified sign changes via monotonically ratio-guarded Mellin–Barnes residue series and independent `acb.integral` quadrature: $\widehat{f}(0) = 2c_0 > 0$, $\widehat{f}(1/2) = -0.5628546550\dots < 0$, $\widehat{f}(4/\tau) = -0.7757751802\dots < 0$, $\widehat{f}(1) = -0.3668367827\dots < 0$, $\widehat{f}(3/2) = +0.2636171832\dots > 0$, $\widehat{f}(2) = +0.1247126116\dots > 0$). Widely unequal blocks satisfy $|B_{A,B}(X)| \le \frac{7}{3}C_*\frac{\min(A,B)^3}{\max(A,B)^2}$ ($C_* = \max\{\zeta(6), c_0 + 27 e^{-3}\} \approx 2.0089210400$). Under **Attack A**, retaining the exact separable Gaussian $e^{-X^2(r^{-2}+s^{-2})/d^2} = e^{-X^2/(d^2 r^2)}e^{-X^2/(d^2 s^2)}$ and applying $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e\mid\gcd(r,s)}\mu(e)$ decouples every rectangular block $B_{A,B}(X)$ into 1D unweighted Liouville Gaussian sums $U_\lambda(\frac{X}{de}; \frac{A}{e})U_\lambda(\frac{X}{de}; \frac{B}{e})$ (with exact rational cutoffs and repaired dyadic Abel bound $|U_\lambda(Y; M)| \ll M^{1/2}\min(M/Y, (Y/M)^{5/2})e^{-c\Phi(M)}$ for $M \ge 16$), while global Stieltjes integration by parts on $Q_\lambda(X) = -X^{5/2}\int_1^\infty L_\lambda(t)\frac{d}{dt}(t^{-3}e^{-X^2/t^2})\,dt$ split at $t = \sqrt{X}$ ($X \ge 256$) proves $|Q_\lambda(X)| \ll \sqrt{X}e^{-c_1\Phi(X)}$ and the **unconditional global super-polynomial logarithmic energy saving**
   \[
   E_\lambda(Y) = \int_Y^{\tau Y}|Q_\lambda(X)|^2\frac{dX}{X} \ll Y\exp\!\bigl(-2c_2\Phi(Y)\bigr) \ll_D Y(\log Y)^{-D} \qquad (\forall D > 0,\; Y \ge 2).
   \]
   Under **Attack B**, dyadic parity $\lambda(2m) = -\lambda(m)$ gives $Q_{\lambda,\mathrm{odd}}(X) = Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2)$ and $Q_\lambda(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}Q_{\lambda,\mathrm{odd}}(X/2^j)$, where on any off-critical mode $X^{\rho-1/2}$ ($\rho = x + i y$ with $x > 0$) the multiplier $1 + 2^{-\rho}$ satisfies $0 < 1 - 2^{-x} \le |1 + 2^{-\rho}| \le 1 + 2^{-x} < 2$, so 2-adic parity cannot annihilate any off-critical zero contribution (`SUBGATE-TC-043A` remains `OPEN`, `rh_proved: false`).



