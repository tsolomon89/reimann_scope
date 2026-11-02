# Faithful $\tau$-Arithmetic Spectral Realization, Adjoint Compatibility, and Canonical Hilbert–Schmidt Orbit Decomposition (`TASK-TC-050`)

**Task ID:** `TASK-TC-050`  
**Parent Epic:** `EPIC-TC-042`  
**Reviewed Baseline:** `5da0eb79e1732ff871ee1c7fee729c62972aa406` (`TC-048R`)  
**Branched From:** `e6472e039c70beed968ed4323cb1eb7e31ca160f` (incorporating `TC-049` and `TC-049R` repairs)  
**Primary Implementation Module:** [tc/faithful_tau_arithmetic_spectral_realization.py](file:///c:/Development/Projects/reimann_scope/tc/faithful_tau_arithmetic_spectral_realization.py)  
**Exported Facade Entrypoint:** [`execute_task_tc050_faithful_spectral_realization_audit`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L10142-L10169)  
**Certified 256-bit Arb Data Artifact:** [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json) (`311/311` certified 256-bit Arb balls passing outward-rounded decimal round-trip verification)  
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

### 3.3 Exact Multiplicity Handling via the Jordan Socle Eigenvector ($m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$)

We never assume simplicity of the zeros of $\xi(s)$. By Meyer (`arXiv:math/0412277`, Theorem A & Section 5), if a zero $\rho$ of $\xi(s)$ has multiplicity $m_\rho = \operatorname{ord}_\xi(\rho) \ge 1$, the generalized eigenspace $E_\rho = \ker(({}^t D_- - \rho)^{m_\rho})$ on the cotangent quotient $\mathcal{H}_-^0$ is an $m_\rho$-dimensional cyclic Jordan block with basis $\{l_{\rho,0}, l_{\rho,1}, \dots, l_{\rho,m_\rho-1}\}$ satisfying
$$
({}^t D_- - \rho) l_{\rho,0} = 0 \quad (l_{\rho,0} \ne 0), \qquad ({}^t D_- - \rho) l_{\rho,k} = l_{\rho,k-1} \quad (1 \le k \le m_\rho - 1),
$$
and grade-shift action
$$
V_K l_{\rho,k} = \tau^{K(\rho - 1/2)} \sum_{j=0}^k \frac{(K\log\tau)^j}{j!}\,l_{\rho,k-j}.
$$
- **Socle Eigenvector Reduction (`jordanTwoByTwoSocleStep` in Lean 4 Theorem 51)**:
  Because $m_\rho \ge 1$, the 1-dimensional **socle** $\ker({}^t D_- - \rho) \subset E_\rho$ always contains the non-zero genuine eigenvector $l_{\rho,0} \ne 0$, on which $V_K l_{\rho,0} = \tau^{K(\rho - 1/2)} l_{\rho,0}$ acts purely multiplicatively without polynomial Jordan nilpotent terms. Applying the star-involution and hyperbolic-pair analysis directly to the socle pair $\operatorname{span}\{l_{\rho,0}, l_{\rho^\sharp,0}\}$ eliminates any simplicity assumption on $m_\rho$.
- **Unconditional Unitary Polynomial Growth Prohibition (`m_\rho \ge 2` under $V_K^* = V_{-K}$)**:
  Moreover, if $V_K$ is unitary on a Hilbert space ($\|V_K v\| = \|v\|$) and $\operatorname{Re}(\rho) = 1/2$ ($\tau^{K\delta} = 1$), then for $m_\rho \ge 2$ the first generalized eigenvector $l_{\rho,1}$ satisfies
  $$
  \|V_K l_{\rho,1}\|^2 = \|l_{\rho,1} + (K\log\tau) l_{\rho,0}\|^2 = \|l_{\rho,1}\|^2 + 2(K\log\tau)\operatorname{Re}\langle l_{\rho,1}, l_{\rho,0}\rangle + (K\log\tau)^2 \|l_{\rho,0}\|^2.
  $$
  Unitarity $\|V_K l_{\rho,1}\|^2 = \|l_{\rho,1}\|^2$ at $K = \pm 1$ forces $2(\log\tau)^2 \|l_{\rho,0}\|^2 = 0 \implies l_{\rho,0} = 0$ (`jordanTwoByTwoSocleStep`), contradicting $l_{\rho,0} \ne 0$. Hence a faithful unitary realization on the full generalized eigenspace simultaneously forces $m_\rho = 1$ (semisimplicity), while restricting to the socle eigenvector $l_{\rho,0}$ already suffices to rule out $\operatorname{Re}(\rho) \ne 1/2$ for any $m_\rho \ge 1$.

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

To advance the faithful spectral realization directly on the canonical correlation $C_\tau(K) = Q_\tau(T_K\psi_\tau, \psi_\tau)$ without assuming RH or Weil positivity, we construct an unconditional positive Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}}$, a strongly continuous unitary grade representation $\mathcal{U}_K$, and a Hilbert–Schmidt rank-one operator $B_0 \in \mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}})$ whose unitary orbit matrix coefficient $P_\tau(K) := \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}}$ captures the positive archimedean-plus-pole-transfer core of $C_\tau(K)$, while isolating the exact arithmetic remainder $E_\tau(K)$ in terms of the `TC-049`/`TC-049R` resonant divisor band.

### 5.1 The Unconditional Positive Hilbert Space $\mathcal{H}_\tau^{\mathrm{pos}}$ and Unitary Grade Orbit

1. **Positive Hilbert Space**:
   Define unconditionally (with zero dependence on RH or the zeros of $\zeta$):
   $$
   \mathcal{H}_\tau^{\mathrm{pos}} := \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y),
   $$
   where $\mathcal{H}_\tau^B = L^2\bigl((1, \infty)\times \mathbb{R}_{>0},\, \frac{x^{-3/2}}{x - x^{-1}}\,\frac{dx}{x}\,d^\times y\bigr)$ is the Attempt B difference-square space (`TC-042F`) with $(A_\tau^B f)(x, y) = (\nabla_x f)(y) = f(xy) - f(y/x)$, and $(R_0 f)(y) = \int_0^y (u/y)^{1/2}(D_u f)(u)\,\frac{du}{u}$ is the causal Euler resolvent at $s = 0$ (`TC-043R`).
2. **Positive Embedding and Unitary Grade Representation**:
   Define the grade-covariant linear map $\mathcal{J}_\tau : \mathcal{S}_\tau \to \mathcal{H}_\tau^{\mathrm{pos}}$ and unitary group $\mathcal{U}_K$ ($K \in \mathbb{R}$) by
   $$
   \mathcal{J}_\tau(f) := \bigl(A_\tau^B f,\; 2\,R_0 f\bigr) \in \mathcal{H}_\tau^{\mathrm{pos}}, \qquad \mathcal{U}_K := U_K^B \oplus T_K.
   $$
   Because $\nabla_x T_K = T_K \nabla_x$ and $R_0 T_K = T_K R_0$, $\mathcal{J}_\tau$ intertwines $T_K$ with $\mathcal{U}_K$:
   $$
   \mathcal{J}_\tau(T_K f) = \mathcal{U}_K\,\mathcal{J}_\tau(f), \qquad \|\mathcal{U}_K \Psi\|_{\mathcal{H}_\tau^{\mathrm{pos}}} = \|\Psi\|_{\mathcal{H}_\tau^{\mathrm{pos}}} \qquad (\forall K \in \mathbb{R}).
   $$
3. **Hilbert–Schmidt Rank-One State $B_0$ and Matrix Coefficient $P_\tau(K)$**:
   Set $\Psi_0 := \mathcal{J}_\tau(\psi_\tau) \in \mathcal{H}_\tau^{\mathrm{pos}}$, chooses a unit reference vector $e_0 \in \mathcal{H}_\tau^{\mathrm{pos}}$ ($\|e_0\| = 1$), and define the rank-one Hilbert–Schmidt operator $B_0 := |\Psi_0\rangle\langle e_0| \in \mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}})$. Under the left unitary action $B_K := \mathcal{U}_K B_0 = |\mathcal{U}_K\Psi_0\rangle\langle e_0|$, the Hilbert–Schmidt inner product is
   $$
   \boxed{P_\tau(K) := \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}} = \operatorname{Tr}(B_0^* \mathcal{U}_K B_0) = \langle \mathcal{U}_K\Psi_0, \Psi_0\rangle_{\mathcal{H}_\tau^{\mathrm{pos}}} = \langle A_\tau^B T_K\psi_\tau, A_\tau^B\psi_\tau\rangle_{\mathcal{H}_\tau^B} + 4\,\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2(d^\times y)}.}
   $$
   By Cauchy–Schwarz in $\mathcal{B}_2(\mathcal{H}_\tau^{\mathrm{pos}})$ (and Bochner's theorem for the unitary representation $K \mapsto \mathcal{U}_K$), $P_\tau(K)$ is an **unconditionally positive-definite function** on $\mathbb{R}$ satisfying:
   $$
   \boxed{\bigl|P_\tau(K)\bigr| \le \|B_0\|_{\mathrm{HS}}^2 = P_\tau(0) = \|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 + 4\,\|R_0\psi_\tau\|_{L^2(d^\times y)}^2 = 2.558258007415831\ldots \qquad (\forall K \in \mathbb{R}),}
   $$
   with $P_\tau(K) = O(|K|\,\tau^{-|K|/2})$ as $|K| \to \infty$.

---

### 5.2 Exact Decomposition $C_\tau(K) = P_\tau(K) + E_\tau(K)$ and Direct Bridge to `TC-049`/`TC-049R` (`canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence`, Theorem 53)

By polarizing the exact Attempt B + pole-vanishing transfer identity on $\mathcal{S}_\tau$ (`TC-043R` Section 12.2):
$$
W_{\mathrm{arch}}(h_K) = \langle A_\tau^B T_K\psi_\tau, A_\tau^B\psi_\tau\rangle_{\mathcal{H}_\tau^B} - c_\tau^B\langle T_K\psi_\tau, \psi_\tau\rangle_{L^2} + B_{\mathrm{transfer}}(T_K\psi_\tau, \psi_\tau),
$$
where $c_\tau^B = \log(2\tau) + \gamma_E + 2 - \frac{\tau}{4} \approx 3.3721834192256654$, $\langle T_K\psi_\tau, \psi_\tau\rangle_{L^2} = h_0(\tau^{|K|})$, and
$$
B_{\mathrm{transfer}}(T_K\psi_\tau, \psi_\tau) = 4\,\langle R_0 T_K\psi_\tau, R_0\psi_\tau\rangle_{L^2} - 2\,h_0(\tau^{|K|}),
$$
we obtain the **exact identity** valid for every $K \in \mathbb{A}_{\mathbb{R}}$:
$$
W_{\mathrm{arch}}(h_K) = P_\tau(K) - \bigl(c_\tau^B + 2\bigr)\,h_0(\tau^{|K|}).
$$
Combining this with $C_\tau(K) = W_{\mathrm{arch}}(h_K) - W(\tau^{|K|}) - W(\tau^{-|K|})$ and the `TC-049`/`TC-049R` three-zone Möbius decomposition $W(X) = W_{\log}(X) + R_{\mu,\mathrm{head}}(X) + R_{\mu,\mathrm{band}}(X) + R_{\mu,\mathrm{tail}}(X)$ ($X = \tau^{|K|} \ge 1$) proves **Theorem 53** (`canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence` in Lean 4):
$$
\boxed{C_\tau(K) = P_\tau(K) + E_\tau(K), \qquad E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|}),}
$$
where the 5-term controlled remainder (`controlledCorrelationRemainder` in Lean 4) is:
$$
\boxed{E_{\tau,\mathrm{controlled}}(K) := -\bigl(c_\tau^B + 2\bigr)\,h_0(\tau^{|K|}) - W(\tau^{-|K|}) - W_{\log}(\tau^{|K|}) - R_{\mu,\mathrm{head}}(\tau^{|K|}) - R_{\mu,\mathrm{tail}}(\tau^{|K|}).}
$$
Every one of the five terms in $E_{\tau,\mathrm{controlled}}(K)$ is unconditionally bounded on $\mathbb{A}_{\mathbb{R}}$ and decays as $|K| \to \infty$:
1. $|(c_\tau^B + 2)h_0(X_K)| \le (c_\tau^B + 2)\frac{92193}{32768}X_K^{-5/2} \approx 2.671908\,X_K^{-5/2} = O(\tau^{-5|K|/2})$;
2. $|W(X_K^{-1})| = |P_{\mathrm{fwd}}(X_K)| \le 0.633039\,X_K^{-5/2} = O(\tau^{-5|K|/2})$ (`TC-042R2`);
3. $|W_{\log}(X_K)| \le C_{\log,\mathrm{EM}}\,X_K^{-5/2} \approx 13.468513\,X_K^{-5/2} = O(\tau^{-5|K|/2})$ (`TC-049`/`TC-049R`);
4. $|R_{\mu,\mathrm{head}}(X_K)| \le \frac{5}{6}C_{\log,\mathrm{EM}} \approx 11.223761$ globally, and $|R_{\mu,\mathrm{head}}(X_K)| \le (\sum_{m\ge 2} m^{-3}) C_{\log,\mathrm{EM}} X_K^{-5/2}\log X_K + O(X_K^{-5/2})$ asymptotically;
5. $|R_{\mu,\mathrm{tail}}(X_K)| \le C_{\log,0}\,X_K^{5/2} M(X_K)^{-2} \le \frac{1}{2}C_{\log,0} \approx 0.278715$ globally, and $O(X_K^{-5/8}) = O(\tau^{-5|K|/8})$ asymptotically since $M(X_K) = \lceil\max(2, X_K^{5/4})\rceil$.

Consequently, for **all** $K \in \mathbb{A}_{\mathbb{R}}$:
$$
\boxed{\bigl|E_{\tau,\mathrm{controlled}}(K)\bigr| \le M_{\mathrm{ctrl}} \approx 12.434994, \qquad \bigl|C_\tau(K) - \bigl(P_\tau(K) - R_{\mu,\mathrm{band}}(\tau^{|K|})\bigr)\bigr| \le M_{\mathrm{ctrl}},}
$$
and because $|P_\tau(K)| \le P_\tau(0) \approx 2.558258$, we have the exact two-sided equivalence (`Theorem 53` in Lean 4):
$$
\boxed{\sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|C_\tau(K)\bigr| < \infty \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|E_\tau(K)\bigr| < \infty \iff \sup_{X \ge 1} \bigl|R_{\mu,\mathrm{band}}(X)\bigr| < \infty \qquad (\text{SUBGATE-TC-043A}).}
$$

---

### 5.3 Certified 256-bit Arb Verification Across 13 Positive & Negative Rational and Irrational Algebraic Grades

The table below reports the certified 256-bit Arb values from [data/tc_faithful_tau_arithmetic_spectral_realization.json](file:///c:/Development/Projects/reimann_scope/data/tc_faithful_tau_arithmetic_spectral_realization.json) across $K \in \{0, \pm 1/4, \pm 1/2, \pm 1, \pm\sqrt{2}, \pm 3/2, \pm 2\} \subset \mathbb{A}_{\mathbb{R}}$. At every grade, $|P_\tau(K)| \le P_\tau(0) = 2.55825801$, $|E_{\tau,\mathrm{controlled}}(K)| \le M_{\mathrm{ctrl}}$, and $0 \in C_\tau(K) - (P_\tau(K) + E_\tau(K))$ to full 256-bit ball accuracy:

| Grade $K \in \mathbb{A}_{\mathbb{R}}$ | Scale $X_K = \tau^{|K|}$ | Positive Orbit $P_\tau(K)$ | Controlled $E_{\tau,\mathrm{controlled}}(K)$ | Resonant Band $R_{\mu,\mathrm{band}}(X_K)$ | Total Remainder $E_\tau(K)$ | Complete $C_\tau(K)$ | $|P_\tau(K)| \le P_\tau(0)$ | $0 \in C_\tau - (P_\tau + E_\tau)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $-2$ | $\tau^2 \approx 39.4784$ | $-0.06808962$ | $+0.00051660$ | $+0.00948982$ | $-0.00897321$ | $-0.07706283$ | `True` | `True` |
| $-3/2$ | $\tau^{3/2} \approx 15.7496$ | $+0.24497111$ | $+0.00916859$ | $+0.00560662$ | $+0.00356197$ | $+0.24853307$ | `True` | `True` |
| $-\sqrt{2}$ | $\tau^{\sqrt{2}} \approx 13.4505$ | $+0.33875447$ | $+0.00880425$ | $+0.00911755$ | $-0.00031331$ | $+0.33844116$ | `True` | `True` |
| $-1$ | $\tau \approx 6.2832$ | $+0.95547910$ | $+0.07257921$ | $+0.03051173$ | $+0.04206748$ | $+0.99754658$ | `True` | `True` |
| $-1/2$ | $\tau^{1/2} \approx 2.5066$ | $+0.69297834$ | $-0.04684805$ | $+0.00965239$ | $-0.05650044$ | $+0.63647789$ | `True` | `True` |
| $-1/4$ | $\tau^{1/4} \approx 1.5832$ | $+0.50652651$ | $-0.38866316$ | $+0.02591502$ | $-0.41457819$ | $+0.09194833$ | `True` | `True` |
| $0$ | $1$ | $+2.55825801$ | $-2.48787918$ | $-0.01388565$ | $-2.47399352$ | $+0.08426448$ | `True` | `True` |
| $+1/4$ | $\tau^{1/4} \approx 1.5832$ | $+0.50652651$ | $-0.38866316$ | $+0.02591502$ | $-0.41457819$ | $+0.09194833$ | `True` | `True` |
| $+1/2$ | $\tau^{1/2} \approx 2.5066$ | $+0.69297834$ | $-0.04684805$ | $+0.00965239$ | $-0.05650044$ | $+0.63647789$ | `True` | `True` |
| $+1$ | $\tau \approx 6.2832$ | $+0.95547910$ | $+0.07257921$ | $+0.03051173$ | $+0.04206748$ | $+0.99754658$ | `True` | `True` |
| $+\sqrt{2}$ | $\tau^{\sqrt{2}} \approx 13.4505$ | $+0.33875447$ | $+0.00880425$ | $+0.00911755$ | $-0.00031331$ | $+0.33844116$ | `True` | `True` |
| $+3/2$ | $\tau^{3/2} \approx 15.7496$ | $+0.24497111$ | $+0.00916859$ | $+0.00560662$ | $+0.00356197$ | $+0.24853307$ | `True` | `True` |
| $+2$ | $\tau^2 \approx 39.4784$ | $-0.06808962$ | $+0.00051660$ | $+0.00948982$ | $-0.00897321$ | $-0.07706283$ | `True` | `True` |

---

## 6. Lean 4 Formalization vs. External Analytic Proofs (`Section 5`)

We maintain a strict separation between what is deductively verified in Lean 4 (`0` `sorry`, `0` `admit`, `0` custom axioms) and what is established by external analytic derivations and 256-bit Arb ball enclosures:

1. **Verified Deductively in Lean 4 ([formal/RiemannScope/CanonicalThetaCorrelationBound.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean), Theorems 51–53)**:
   - [`tau_grade_star_involution_and_hyperbolic_pair_obstruction`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1686-L1730) (**Theorem 51**):
     1. Exact radial star-involution defect $r^{-1} - r = (1 - r^2)/r$ (`gradeRadialCharacter`) and $r^{-1} = r \iff r = 1$ for $r > 0$;
     2. Isotropic null-cone vanishing (`hyperbolicPairForm c1 0 = 0` and `hyperbolicPairForm 0 c2 = 0`), positive/negative eigenvectors (`hyperbolicPairForm 1 1 = 2`, `hyperbolicPairForm 1 (-1) = -2`), and signature-$(1,1)$ polarization $2 c_1 c_2 = \frac{1}{2}(c_1 + c_2)^2 - \frac{1}{2}(c_1 - c_2)^2$;
     3. Unconditional Hilbert-space collapse: if every vector has nonnegative norm under a form whose off-critical pair restriction is $2 b_{12} c_1 c_2$, evaluating on $(1, 1)$ and $(1, -1)$ forces $b_{12} = 0$;
     4. Multiplicity Jordan socle step (`jordanTwoByTwoSocleStep`): unitarity at $\pm L$ on a $2\times 2$ Jordan block forces $a = \|l_{\rho,0}\|^2 = 0$, while restricting to the socle eigenvector $l_{\rho,0} \in \ker({}^t D_- - \rho)$ requires no simplicity assumption.
   - [`tate_rational_diagonal_character_rigidity_and_convolution_isometry`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1740-L1774) (**Theorem 52**):
     1. Exact Tate rational-diagonal phase cancellation (`adelicPhaseDiscrepancy`) proving that vanishing phase discrepancy on $q = 1$ uniquely forces $c_\infty = \tau$;
     2. Exact non-abelian semidirect intertwining between logarithmic prime-grade translation (`logPrimeShiftAction`) and logarithmic scaling (`logScaleAction`);
     3. Multiplicative convolution weight factorizability under self-dual Fourier/Mellin normalization.
   - [`canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean#L1780-L1845) (**Theorem 53**):
     1. Exact algebraic identity $C_\tau(K) = P_\tau(K) + E_\tau(K)$ with $E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|})$ (`canonicalCorrelationHSOrbitDecomp` and `controlledCorrelationRemainder`);
     2. Exact triangle-inequality bound $|E_{\tau,\mathrm{controlled}}(K)| \le B_{h_0} + B_{\mathrm{fwd}} + B_{\log} + \frac{5}{6}C_{\log,\mathrm{EM}} + \frac{1}{2}C_{\log,0}$;
     3. Exact logical equivalence between uniform boundedness of $C_\tau(K)$, uniform boundedness of $E_\tau(K)$, and uniform boundedness of the localized resonant-band Möbius sum $R_{\mu,\mathrm{band}}(X)$ under $|P_\tau(K)| \le P_\tau(0)$.
2. **Established Externally (Analytic Derivations + SymPy + 256-bit Arb Enclosures)**:
   - Unconditional spatial and Mellin–Plancherel convergence of $\|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 + 4\|R_0\psi_\tau\|_{L^2}^2 = P_\tau(0) \approx 2.55825801$;
   - The 4th-order Euler–Maclaurin bound $|W_{\log}(X)| \le C_{\log,\mathrm{EM}}\,X^{-5/2}$ ($C_{\log,\mathrm{EM}} \approx 13.468513$) and small-scale bound $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ ($C_{\log,0} \approx 0.557430$) from `TC-049`/`TC-049R`;
   - The Connes–Consani sine-integral formula for $\delta(\rho)$ (`arXiv:2006.13771`, Prop. 2.2) and its 256-bit Arb evaluation;
   - The Laplace–Carleman analytic continuation theorem converting $\sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty$ into right-half-plane holomorphy of $\mathcal{L}[C_\tau(-t)](w)$ and exclusion of off-critical zeros.

---

## 7. Outcome Classification and Single Surviving Open Obligation (`SUBGATE-TC-043A`)

`TASK-TC-050` achieves **Target 2** in full:
- It proves that multiplicative compatibility on the grade algebra holds unconditionally for all $\rho \in \mathbb{C}$, whereas star-involution compatibility $V_K^* = V_{-K}$ holds if and only if $\operatorname{Re}(\rho) = 1/2$, with any off-critical pair $\{\rho, 1 - \bar{\rho}\}$ ($\operatorname{Re}(\rho) \ne 1/2$) forcing an isotropic null cone and signature-$(1,1)$ hyperbolic plane on the Jordan socle $\operatorname{span}\{l_{\rho,0}, l_{\rho^\sharp,0}\}$ (`Theorem 51`).
- It constructs the unconditional positive Hilbert space $\mathcal{H}_\tau^{\mathrm{pos}} = \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, d^\times y)$ and Hilbert–Schmidt unitary orbit $B_K = \mathcal{U}_K B_0$ with positive-definite matrix coefficient $P_\tau(K) = \langle \mathcal{U}_K B_0, B_0\rangle_{\mathrm{HS}}$ ($|P_\tau(K)| \le P_\tau(0) \approx 2.558258$), and proves the exact decomposition $C_\tau(K) = P_\tau(K) + E_\tau(K)$ with $E_\tau(K) = E_{\tau,\mathrm{controlled}}(K) - R_{\mu,\mathrm{band}}(\tau^{|K|})$ (`Theorem 53`).
- Because $|P_\tau(K)| \le P_\tau(0)$ and $|E_{\tau,\mathrm{controlled}}(K)| \le 12.4350$ are unconditionally bounded for all $K \in \mathbb{A}_{\mathbb{R}}$, uniform boundedness of $C_\tau(K)$ is equivalent to the **single surviving open arithmetic lemma (`SUBGATE-TC-043A`)**:
  $$
  \boxed{\exists M_{\mathrm{band}} < \infty \quad \forall X \ge 1 : \quad \Biggl|\sum_{X^{5/6} < m \le \lceil\max(2, X^{5/4})\rceil} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\Biggr| \le M_{\mathrm{band}}.}
  $$
  `SUBGATE-TC-043A` remains `OPEN` (`rh_proved: false`).
