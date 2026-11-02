# Faithful $\tau$-Arithmetic Spectral Realization, Adjoint Compatibility, and Canonical Hilbert–Schmidt Orbit Decomposition (`TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2`)

**Task ID:** `TASK-TC-050` / `TASK-TC-050R` / `TASK-TC-050R2`  
**Parent Epic:** `EPIC-TC-042`  
**Reviewed Baselines:** `5da0eb79e1732ff871ee1c7fee729c62972aa406` (`TC-048R`), `2f7871fff666091c4152ecc8657f2345aacdd4fa` (`TC-050` + `TC-049R`), `0e6ae36ce995ef3037652b3dfb67645325f990b1` (`TC-050R` HEAD; implementation commit `f5521363ea94774938fd37152d67d743413327ae`)  
**Branched From:** `2f7871fff666091c4152ecc8657f2345aacdd4fa` (`task/tc-050r-cutoff-hs-certification-and-proof-scope-repair`)  
**Primary Implementation Module:** [tc/faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)  
**Exported Facade Entrypoint:** [`execute_task_tc050_faithful_spectral_realization_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10169)  
**Certified 256-bit Arb Data Artifact:** [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json) (`522/522` certified 256-bit Arb balls passing outward-rounded decimal round-trip verification)  
**Formal Verification Module:** [formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) (`40` definitions, `53` theorems, `0` `sorry`, `0` `admit`, `0` custom axioms)  
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
   All work preserves the `TC-049`/`TC-049R` repaired 4th-order Euler–Maclaurin decay bound $|W_{\log}(X)| \le C_{\log,\mathrm{EM}}\,X^{-5/2}$ ($C_{\log,\mathrm{EM}} \approx 13.468513$ for all $X \ge 1$) and the unconditional three-zone divisor reduction of $R_\mu(X) = \sum_{m\ge 2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ to the localized resonant divisor band $X^{5/6} < m \le M(X) := \lceil\max(2, X^{5/4})\rceil$ (`SUBGATE-TC-043A`).

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
   In the Weil explicit formula for $C_\tau(K) = Q_\tau(T_K\psi_\tau, \psi_\tau)$, the zero sum comes from Cauchy's residue theorem applied to the logarithmic derivative $-\xi'(s)/\xi(s)$ integrated against the holomorphic Mellin kernel $H_K(s - 1/2) = \tau^{-K(s - 1/2)} H_0(s - 1/2)$. Because $-\xi'(s)/\xi(s)$ has a **simple pole** of residue $m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$ at each distinct zero $\rho$ (never a higher-order pole that would differentiate $\tau^{-K(s - 1/2)}$ with respect to $s$), a zero $\rho$ of multiplicity $m_\rho \ge 1$ contributes
   $$
   m_\rho\,H_0(\rho - 1/2)\,\tau^{-K(\rho - 1/2)}
   $$
   with **no polynomial $(K\log\tau)^j$ drift** even when $m_\rho \ge 2$. Therefore:
   - **Forward Direction ($\text{RH} \implies \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| \le C_\tau(0) < \infty$, any $m_\rho \ge 1$)**: If $\operatorname{Re}(\rho) = 1/2$ for every zero, then $H_0(i\gamma_\rho) = |F_\tau(1/2 + i\gamma_\rho)|^2 \ge 0$ and $|\tau^{-iK\gamma_\rho}| = 1$, so the triangle inequality gives
     $$
     \bigl|C_\tau(K)\bigr| = \biggl|\sum_{\rho\text{ distinct}} m_\rho\,\bigl|F_\tau(1/2 + i\gamma_\rho)\bigr|^2 \tau^{-iK\gamma_\rho}\biggr| \le \sum_{\rho\text{ distinct}} m_\rho\,\bigl|F_\tau(1/2 + i\gamma_\rho)\bigr|^2 = C_\tau(0) \approx 9.5048\times 10^{-4} < \infty
     $$
     for all $K \in \mathbb{R}$, without assuming $m_\rho = 1$. (In Theorem 8 of `CanonicalThetaCorrelationBound.lean`, the finite-sum triangle inequality `|∑ c_j cos(u_j)| ≤ ∑ c_j` for `c_j ≥ 0` applies directly with $c_\rho = m_\rho |F_\tau(1/2 + i\gamma_\rho)|^2 \ge 0$.)
   - **Converse Direction ($\sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \implies \text{RH}$, any $m_\rho \ge 1$)**: Established in `TASK-TC-037` (`docs/reviews/TC_GRADE_CHARACTER_PROJECTION.md` Theorem 12 & `CanonicalThetaCorrelationBound.lean` Theorem 12) via the Laplace–Carleman transform $R_+(\lambda) = \int_0^\infty C_\tau(u)e^{-\lambda u}\,du$: boundedness of $C_\tau$ makes $R_+(\lambda)$ holomorphic on $\operatorname{Re}(\lambda) > 0$, whereas any zero $\rho_0$ of maximal positive real offset $\delta_{\max} > 0$ (of any multiplicity $m_{\rho_0} \ge 1$, since $m_{\rho_0} H_0(\rho_0 - 1/2) \ne 0$) creates a simple pole at $\lambda = (\delta_{\max} \pm i\gamma_{\rho_0})\log\tau$ in the right half-plane.
   - **Unconditional Scalar Equivalence**:
     $$
     \boxed{\text{RH} \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| \le C_\tau(0) \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| < \infty \qquad (\text{unconditional in } m_\rho \ge 1).}
     $$

2. **Operator-Level Unitary Realization on the Jordan Socle vs. the Full Cotangent Quotient $\mathcal{H}_-^0$**:
   By Meyer (`arXiv:math/0412277`, Theorem A & Section 5), if a zero $\rho$ of $\xi(s)$ has multiplicity $m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$, the generalized eigenspace $E_\rho = \ker(({}^t D_- - \rho)^{m_\rho})$ on the cotangent quotient $\mathcal{H}_-^0$ is an $m_\rho$-dimensional cyclic Jordan block with basis $\{l_{\rho,0}, l_{\rho,1}, \dots, l_{\rho,m_\rho-1}\}$ satisfying
   $$
   ({}^t D_- - \rho) l_{\rho,0} = 0 \quad (l_{\rho,0} \ne 0), \qquad ({}^t D_- - \rho) l_{\rho,k} = l_{\rho,k-1} \quad (1 \le k \le m_\rho - 1),
   $$
   and grade-shift action
   $$
   V_K l_{\rho,k} = \tau^{K(\rho - 1/2)} \sum_{j=0}^k \frac{(K\log\tau)^j}{j!}\,l_{\rho,k-j}.
   $$
   - **Socle Eigenvector Realization ($\iff \text{RH}$ alone, any $m_\rho \ge 1$)**: Because $m_\rho \ge 1$, the 1-dimensional **socle** $\ker({}^t D_- - \rho) \subset E_\rho$ always contains the non-zero genuine eigenvector $l_{\rho,0} \ne 0$, on which $V_K l_{\rho,0} = \tau^{K(\rho - 1/2)} l_{\rho,0}$ acts purely multiplicatively without polynomial Jordan nilpotent terms. Applying the star-involution and hyperbolic-pair analysis (`Theorem 51`) directly to the socle subspace $\bigoplus_\rho \operatorname{span}\{l_{\rho,0}\}$ shows that a faithful Hilbert-space realization of the socle eigenvectors with $V_K^* = V_{-K}$ exists if and only if $\operatorname{Re}(\rho) = 1/2$ for every zero (**$\text{RH}$ alone**, with no simplicity restriction).
   - **Full Generalized-Eigenspace Realization on $\mathcal{H}_-^0$ ($\iff \text{RH} + \text{Simplicity}$, $m_\rho = 1$)**: If $V_K$ acts unitarily on the **entire** generalized eigenspace $E_\rho$ ($\|V_K v\| = \|v\|$) and $\operatorname{Re}(\rho) = 1/2$ ($\tau^{K\delta} = 1$), then for $m_\rho \ge 2$ the first generalized eigenvector $l_{\rho,1}$ satisfies
     $$
     \|V_K l_{\rho,1}\|^2 = \|l_{\rho,1} + (K\log\tau) l_{\rho,0}\|^2 = \|l_{\rho,1}\|^2 + 2(K\log\tau)\operatorname{Re}\langle l_{\rho,1}, l_{\rho,0}\rangle + (K\log\tau)^2 \|l_{\rho,0}\|^2.
     $$
     Unitarity $\|V_K l_{\rho,1}\|^2 = \|l_{\rho,1}\|^2$ at $K = \pm 1$ forces $2(\log\tau)^2 \|l_{\rho,0}\|^2 = 0 \implies l_{\rho,0} = 0$ (`jordanTwoByTwoSocleStep` in Lean 4 Theorem 51), contradicting $l_{\rho,0} \ne 0$. Hence a faithful unitary realization of the full generalized-eigenvector action on $\mathcal{H}_-^0$ is equivalent to **$\text{RH} + \text{Simplicity}$** ($m_\rho = 1$ for all zeros).

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
   >    carrying the exponential weight $e^{-u/2}\,du$ (whereas the hyperbolic weight $\frac{e^{-3u/2}}{2\sinh u}\,du = \frac{x^{-3/2}}{x - x^{-1}}\frac{dx}{x}$ belongs to $P_\tau^B(K)$). Omitting $D$ (replacing $R_0$ by $K_0$) would yield $4\langle K_0 T_K\psi_\tau, K_0\psi_\tau\rangle_{L^2} = 4J(\kappa)$ ($4J(0) \approx 0.10383893$ at $K = 0$) instead of $4\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2} = 4h_0(e^\kappa) - J(\kappa)$ ($4h_0(1) - J(0) \approx 1.96349017$ at $K = 0$), which would fail to cancel $-J(\kappa)$ in $P_\tau^B(K) + 4\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2}$.

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
   \boxed{h_0(1) = \|\psi_\tau\|_{L^2(d^\times y)}^2 = \frac{92193}{512 \cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} = 0.4973624838099012420092607\ldots, \qquad J(0) = 0.0259597612844039196133522\ldots,}
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

| Grade $K \in \mathbb{A}_{\mathbb{R}}$ | Scale $X_K = \tau^{|K|}$ | Cutoffs $(H, M)$ | Positive Orbit $P_\tau(K)$ | Head $R_{\mu,\mathrm{head}}(X_K)$ | Direct Band $R_{\mu,\mathrm{band}}(X_K)$ | Controlled $E_{\tau,\mathrm{controlled}}(K)$ | Total Remainder $E_\tau(K)$ | Complete $C_\tau(K)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $-2$ | $39.47841760$ | $(21, 99)$ | $-0.00048360$ | $-0.01256608$ | $+0.00948794$ | $+0.01028368$ | $+0.00036032$ | $-0.00012328$ |
| $-3/2$ | $15.74960995$ | $(9, 32)$ | $-0.00443212$ | $-0.01041840$ | $+0.00339001$ | $+0.00815705$ | $+0.00471475$ | $+0.00028264$ |
| $-\sqrt{2}$ | $13.45230778$ | $(8, 26)$ | $-0.00583251$ | $-0.00370093$ | $+0.00664051$ | $+0.01305260$ | $+0.00637597$ | $+0.00054346$ |
| $-1$ | $6.28318531$ | $(4, 10)$ | $+0.02470927$ | $-0.03279411$ | $+0.03051131$ | $+0.00643952$ | $-0.02407864$ | $+0.00063063$ |
| $-1/2$ | $2.50662827$ | $(2, 4)$ | $-0.11743968$ | $+0.06496941$ | $-0.00641239$ | $+0.11189571$ | $+0.11830653$ | $+0.00086685$ |
| $-1/4$ | $1.58323349$ | $(1, 2)$ | $-1.36831275$ | $0.00000000$ | $-0.01542659$ | $+1.35381667$ | $+1.36924136$ | $+0.00092861$ |
| $0$ | $1.00000000$ | $(1, 2)$ | $+2.55825801$ | $0.00000000$ | $-0.01388599$ | $-2.57119291$ | $-2.55730753$ | $+0.00095048$ |
| $+1/4$ | $1.58323349$ | $(1, 2)$ | $-1.36831275$ | $0.00000000$ | $-0.01542659$ | $+1.35381667$ | $+1.36924136$ | $+0.00092861$ |
| $+1/2$ | $2.50662827$ | $(2, 4)$ | $-0.11743968$ | $+0.06496941$ | $-0.00641239$ | $+0.11189571$ | $+0.11830653$ | $+0.00086685$ |
| $+1$ | $6.28318531$ | $(4, 10)$ | $+0.02470927$ | $-0.03279411$ | $+0.03051131$ | $+0.00643952$ | $-0.02407864$ | $+0.00063063$ |
| $+\sqrt{2}$ | $13.45230778$ | $(8, 26)$ | $-0.00583251$ | $-0.00370093$ | $+0.00664051$ | $+0.01305260$ | $+0.00637597$ | $+0.00054346$ |
| $+3/2$ | $15.74960995$ | $(9, 32)$ | $-0.00443212$ | $-0.01041840$ | $+0.00339001$ | $+0.00815705$ | $+0.00471475$ | $+0.00028264$ |
| $+2$ | $39.47841760$ | $(21, 99)$ | $-0.00048360$ | $-0.01256608$ | $+0.00948794$ | $+0.01028368$ | $+0.00036032$ | $-0.00012328$ |

---

## 6. Lean 4 Formalization vs. External Analytic Proofs (`Section 5`)

We maintain a strict separation between what is deductively verified in Lean 4 (`0` `sorry`, `0` `admit`, `0` custom axioms) and what is established by external analytic derivations and 256-bit Arb ball enclosures:

1. **Verified Deductively in Lean 4 ([formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean), Theorems 51–53, synchronized word-for-word in `TASK-TC-050R2`)**:
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
2. **Established Externally (Analytic Derivations + SymPy + 256-bit Arb Enclosures)**:
   - Unconditional spatial and Mellin–Plancherel convergence of $\|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 + 4\|R_0\psi_\tau\|_{L^2}^2 = P_\tau(0) \approx 2.55825801$, the spatial/Mellin identity $(R_0 f)(y) = \int_0^y (t/y)^{1/2}(Df)(t)\frac{dt}{t} = f(y) - \frac{1}{2}\int_0^y (t/y)^{1/2}f(t)\frac{dt}{t}$ with $J(\kappa) = \int_0^\infty e^{-u/2}(h_0(e^{\kappa+u}) + h_0(e^{\kappa-u}))\,du$, and the unitary dilation Cauchy–Schwarz bound $|h_0(X_K)| = |\langle T_{|K|}\psi_\tau, \psi_\tau\rangle_{L^2(d^\times y)}| \le h_0(1) = \frac{92193}{512\cdot 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.4973624838$;
   - The 4th-order Euler–Maclaurin bound $|W_{\log}(X)| \le C_{\log,\mathrm{EM}}\,X^{-5/2}$ ($C_{\log,\mathrm{EM}} \approx 13.468510 < 13.468515$), small-scale bound $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ ($C_{\log,0} \approx 0.557430$), and clamped cutoff certification $M(X) = \lceil\max(2, X^{5/4})\rceil$ ($M \ge 2 \land X^5 \le M^4 \land (M = 2 \lor (M-1)^4 < X^5)$) from `TC-049`/`TC-049R` and `TC-050R2`;
   - The Connes–Consani sine-integral formula for $\delta(\rho)$ (`arXiv:2006.13771`, Prop. 2.2) and its 256-bit Arb evaluation;
   - **Both Directions of the Scalar RH Equivalence vs. Operator-Level Realization Scope**: Both directions of the scalar correlation equivalence $\text{RH} \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| \le C_\tau(0) \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty$ hold **unconditionally in zero multiplicity $m_\rho \ge 1$** (since $-\xi'(s)/\xi(s)$ has simple poles of residue $m_\rho$, so on $\operatorname{Re}(\rho) = 1/2$ each distinct zero contributes $m_\rho|F_\tau(\rho)|^2\tau^{-iK\gamma_\rho}$ with no polynomial drift in $K$, while `TASK-TC-037` / Theorem 12 proves $\sup_{K\in\mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \implies \text{RH}$ via Laplace–Carleman analytic continuation); at the operator level, realizing the **socle eigenvectors** $l_{\rho,0} \in \ker({}^t D_- - \rho)\setminus\{0\}$ unitarily is equivalent to **$\text{RH}$ alone**, whereas realizing the **full generalized-eigenvector action** on $\mathcal{H}_-^0$ unitarily is equivalent to **$\text{RH} + \text{Simplicity}$** ($m_\rho = 1$).

---

## 7. Outcome Classification and Single Surviving Open Obligation (`SUBGATE-TC-043A`)

`TASK-TC-050` and its consistency repair `TASK-TC-050R` achieve **Target 2** in full:
- They prove that multiplicative compatibility on the grade algebra holds unconditionally for all $\rho \in \mathbb{C}$, whereas star-involution compatibility $V_K^* = V_{-K}$ holds if and only if $\operatorname{Re}(\rho) = 1/2$, with any off-critical pair $\{\rho, 1 - \bar{\rho}\}$ ($\operatorname{Re}(\rho) \ne 1/2$) forcing an isotropic null cone and signature-$(1,1)$ hyperbolic plane on the Jordan socle $\operatorname{span}\{l_{\rho,0}, l_{\rho^\sharp,0}\}$ (`Theorem 51`).
- They construct the unconditional positive Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}} = \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y)$ with the one-sided Attempt B shift-difference operator $(A_\tau^B f)(x, y) = f(y) - f(y/x)$ and Hilbert–Schmidt unitary orbit $B_K = \mathcal{U}_K B_0$ with positive-definite matrix coefficient $P_\tau(K) = \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}} = W_{\mathrm{arch}}(h_K) + (c_\tau^B + 2)h_0(\tau^{|K|})$ ($|P_\tau(K)| \le P_\tau(0) \approx 2.558258$), and prove the exact decomposition $C_\tau(K) = P_\tau(K) + E_\tau(K)$ with $E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|})$ at the restored `TC-049`/`TC-049R` cutoffs $H(X) = \lfloor X^{5/6}\rfloor$ and $M(X) = \lceil\max(2, X^{5/4})\rceil$ (`Theorem 53`).
- Because $|P_\tau(K)| \le P_\tau(0) \approx 2.558258$ and $|E_{\tau,\mathrm{controlled}}(K)| \le B_{\mathrm{ctrl}} < 17.987140$ (with $\limsup_{|K|\to\infty}|E_{\tau,\mathrm{controlled}}(K)| \le \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0} < 11.502478$) are unconditionally bounded for all $K \in \mathbb{A}_{\mathbb{R}}$, uniform boundedness of $C_\tau(K)$ is equivalent to the **single surviving open arithmetic lemma (`SUBGATE-TC-043A`)**:
  $$
  \boxed{\exists M_{\mathrm{band}} < \infty \quad \forall X \ge 1 : \quad \Biggl|\sum_{\lfloor X^{5/6}\rfloor < m \le \lceil\max(2, X^{5/4})\rceil} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\Biggr| \le M_{\mathrm{band}}.}
  $$
  `SUBGATE-TC-043A` remains `OPEN` (`rh_proved: false`).
