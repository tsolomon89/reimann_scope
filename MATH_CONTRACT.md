# Mathematical Contract

This is the authoritative implementation-level mathematical contract for `reimann_scope`.

Its purpose is to prevent the UI, numerical engine, batch runner, and formal layer from silently using different meanings for the same transformation or research object.

Every identity marked **EXACT** should have a direct unit or formal regression test where practical.

---

# 1. Constants and coordinates

Use

\[
\boxed{\tau=2\pi.}
\]

Ordinary complex coordinate:

\[
\boxed{s=\sigma+it.}
\]

Centered coordinate:

\[
\boxed{
z=s-\frac12=\delta+it.
}
\]

Therefore

\[
s=\frac12+z
\]

and

\[
\boxed{
\delta=\Re(s)-\frac12.
}
\]

The ordinary critical line is

\[
\boxed{
\Re(s)=\frac12.
}
\]

---

# 2. Grade notation

The repository establishes the canonical grade hierarchy:

## 2.1 Canonical algebraic grade domain

\[
\boxed{K \in \mathbb A_{\mathbb R} = \overline{\mathbb Q} \cap \mathbb R.}
\]

Define for any algebraic grade $K \in \mathbb A_{\mathbb R}$:

\[
\boxed{
A_K = \tau^K.
}
\]

Properties:
- $A_K > 0$ for all real algebraic $K$.
- $A_{K_1 + K_2} = A_{K_1} A_{K_2}$.
- $A_{-K} = A_K^{-1}$.
- $A_0 = 1$.

The field of real algebraic numbers $\mathbb A_{\mathbb R}$ is the canonical domain for Transcendental Continuation.

## 2.2 Canonical discrete integer skeleton

\[
\boxed{K \in \mathbb Z.}
\]

The canonical bilateral integer sequence is:

\[
\ldots, \tau^{-2}, \tau^{-1}, 1, \tau, \tau^2, \ldots
\]

with $A_{-K} = A_K^{-1}$.

## 2.3 Rational/root grade refinement

For

\[
q \in \mathbb Q,
\]

define

\[
\boxed{
A_q = \tau^q.
}
\]

Rational grades provide exact root refinements of the integer-grade family.

## 2.4 Ambient continuous scale flow

\[
\boxed{k \in \mathbb R.}
\]

Define

\[
\boxed{
a(k) = \tau^k.
}
\]

Continuous real $k$ serves as an ambient interpolation and differentiation parameter where genuinely required (e.g. continuous character variation, zero worldlines $s_\rho(k) = \tau^k \rho$, and curvature $B_\rho''(0)$). However, continuous $k$ must not silently replace the canonical algebraic TC domain $\mathbb A_{\mathbb R}$.

Do not use one variable interchangeably for continuous $k$, canonical algebraic $K \in \mathbb A_{\mathbb R}$, integer $K \in \mathbb Z$, and rational $q \in \mathbb Q$.

---

# 3. Auxiliary analytic-pullback family (Historical)

> [!IMPORTANT]
> **HISTORICAL / AUXILIARY PULLBACK NOTATION (SUPERSEDED AS CANONICAL ARITHMETIC TC)**
> Classification: `ANALYTIC_PULLBACK`.
> Under the canonical four-way architecture established in TASK-TC-025, TASK-TC-026, and TASK-TC-027 (Sections 21–23 below), $\mathcal Z_\tau(s, k) = \zeta(\tau^{-k}s)$ is the **auxiliary analytic pullback** $Z_k^{\mathrm{pull}}(s)$. The moving-zero law $\rho \mapsto \tau^k \rho$ belongs *only* to this auxiliary pullback.
> In canonical arithmetic TC, the intrinsic fiber is $\mathcal{F}_K = \{K\} \times \mathbb{Z} \cong \mathbb{Z}$, the intrinsic zeta is $\zeta_K^{\mathrm{int}}(s) = \zeta(s)$ (identically constant with stationary zeros), and the ambient coordinate transform is $Z_K^{\mathrm{amb}}(s) = \tau^{-Ks}\zeta(s)$ (zeros invariant).

The historical auxiliary analytic-pullback family uses origin-dilation semantics.

Define

\[
\boxed{
\mathcal Z_\tau(s,k)
=
\zeta(\tau^{-k}s).
}
\]

This is an exact family built from the analytically continued zeta function.

At native grade,

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s).
}
\]

For any \(u\in\mathbb C\),

\[
\boxed{
\mathcal Z_\tau(\tau^k u,k)=\zeta(u).
}
\]

This is **EXACT COORDINATE COVARIANCE**.

It is not an RH result.

---

# 4. Completed auxiliary analytic pullback

Define

\[
\boxed{
\xi(s)
=
\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s).
}
\]

For proof-facing nontrivial-zero work, define

\[
\boxed{
\mathcal X_\tau(s,k)
=
\xi(\tau^{-k}s).
}
\]

Then

\[
\boxed{
\mathcal X_\tau(s,0)=\xi(s).
}
\]

The zeros of \(\xi\) are the nontrivial zeros of \(\zeta\).

---

# 5. Zero worldlines under auxiliary analytic pullback

Let

\[
\zeta(\rho)=0.
\]

Then

\[
\mathcal Z_\tau(s,k)=0
\]

iff

\[
\tau^{-k}s=\rho.
\]

Hence the exact zero map is

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

At integer grade,

\[
\boxed{
s_{\rho,K}=\tau^K\rho.
}
\]

Define the continuous zero worldline

\[
\boxed{
W_\rho
=
\{(\tau^k\rho,k):k\in\mathbb R\}.
}
\]

For proof-facing nontrivial zeros, the same map holds for \(\mathcal X_\tau\).

---

# 6. Critical surface

The ordinary critical line is

\[
\Re(s)=\frac12.
\]

Under grade \(k\), its image is

\[
\boxed{
\Re(s)=\frac{\tau^k}{2}.
}
\]

Define

\[
\boxed{
\mathcal C_\tau
=
\left\{
(s,k):
\Re(s)=\frac{\tau^k}{2}
\right\}.
}
\]

A critical-line zero worldline lies entirely on \(\mathcal C_\tau\).

---

# 7. Transcendental radial coordinate

Define

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

Let

\[
\rho=\frac12+\delta+i\gamma.
\]

Along its worldline,

\[
s_\rho(k)
=
\tau^k
\left(
\frac12+\delta+i\gamma
\right).
\]

Then

\[
\boxed{
R_\tau(s_\rho(k),k)=\delta.
}
\]

This is an **EXACT WORLDLINE INVARIANT**.

It is a coordinate identity.

It does not prove that only \(\delta=0\) occurs.

---

# 8. Radial leaves

For each

\[
\delta\in\mathbb R,
\]

define

\[
\boxed{
\mathcal R_\delta
=
\{(s,k):R_\tau(s,k)=\delta\}.
}
\]

The critical surface is

\[
\boxed{
\mathcal R_0=\mathcal C_\tau.
}
\]

A native zero

\[
\rho=\frac12+\delta+i\gamma
\]

generates a worldline entirely contained in \(\mathcal R_\delta\).

RH is equivalent to:

\[
\boxed{
\text{all nontrivial zero worldlines occupy }\mathcal R_0.
}
\]

---

# 9. Arithmetic grade grids and incommensurability

For any algebraic grade $K \in \mathbb A_{\mathbb R}$, define the nonzero arithmetic grid:

\[
\boxed{
L_K = \{n\tau^K : n \in \mathbb Z \setminus \{0\}\}.
}
\]

Each grid is countably infinite and scale-isomorphic to $\mathbb Z \setminus \{0\}$.

A collision between distinct grades $J \ne K \in \mathbb A_{\mathbb R}$ requires:

\[
m\tau^K = n\tau^J \iff \tau^{K-J} = \frac{n}{m} \in \mathbb Q^\times.
\]

Two cases must be rigorously distinguished:

### 9.1 Rational grade differences ($K - J \in \mathbb Q \setminus \{0\}$) — PROVED

If $K - J = p/q \in \mathbb Q \setminus \{0\}$ with $p \in \mathbb Z \setminus \{0\}, q \in \mathbb N^+$, then $\tau^{p/q} = n/m$ implies:

\[
\tau^p = \left(\frac{n}{m}\right)^q \in \mathbb Q.
\]

This would mean that a nonzero integer power of $\tau = 2\pi$ is algebraic, contradicting the transcendence of $\tau = 2\pi$ (Lindemann 1882). Therefore:

\[
\boxed{
L_J \cap L_K = \emptyset \qquad \forall J \ne K \in \mathbb A_{\mathbb R} \text{ with } K - J \in \mathbb Q.
}
\]

Rational-difference grade grids are strictly noncoincident.

### 9.2 Irrational algebraic grade differences ($K - J \in \mathbb A_{\mathbb R} \setminus \mathbb Q$) — OPEN

For $K - J \in \mathbb A_{\mathbb R} \setminus \mathbb Q$, the arithmetic nature of $\tau^{K-J}$ is strictly open:

\[
\boxed{\text{Status: } \texttt{OPEN\_TAU\_ALGEBRAIC\_EXPONENT\_ARITHMETIC}}
\]

**Crucial negative control**: Gelfond–Schneider requires an algebraic base ($\alpha^\beta$ with algebraic $\alpha \ne 0, 1$ and irrational algebraic $\beta$ is transcendental). It does **not** apply to the transcendental base $\tau = 2\pi$. The control counterexample:

\[
b = 2^{1/\sqrt 2}
\]

is transcendental by Gelfond–Schneider, yet:

\[
b^{\sqrt 2} = 2 \in \mathbb Q.
\]

This proves that base transcendence alone does not exclude rational powers under irrational algebraic exponents. Disjointness across all algebraic grades must not be asserted as a theorem or used downstream.

### 9.3 Scale-generator multiples

For nonzero algebraic $a \in \mathbb A_{\mathbb R}^\times$, $a\tau$ is transcendental, but:

\[
n(a\tau)^K = (n a^K)\tau^K
\]

does not imply membership in $L_K = \{m\tau^K : m \in \mathbb Z \setminus \{0\}\}$ because $n a^K$ is not generally an integer. Therefore, do not claim that $\tau, \pi, \tau/4, a\tau$ generate identical grid universes. Their relations remain an open comparison problem.

Do not infer from grid noncoincidence that zeta zero sets at distinct grades are automatically disjoint.

### 9.4 Analytic vs Arithmetic-Grid Dilation Operators

The mathematical contract rigorously separates two distinct grade operators:

1. **Analytic TC Dilation Operator ($A_K$)**:
   \[
   \boxed{A_K[F](s) = F(\tau^{-K} s).}
   \]
   Acts on Dirichlet series as base-power dilation $n \mapsto n^{\tau^{-K}}$, which in log-space $x = \log n$ is pure **dilation**:
   \[
   T_K(x) = \tau^{-K} x.
   \]
   Preserves multiplicativity ($(mn)^{\tau^{-K}} = m^{\tau^{-K}} n^{\tau^{-K}}$) and the Euler product. Transports zeros as $s_\rho(K) = \tau^K \rho$.

2. **Arithmetic-Grid Dilation Operator ($D_K$)**:
   \[
   \boxed{D_K[F](s) = \tau^{-K s} F(s).}
   \]
   Acts on Dirichlet series by scaling grid elements $n \mapsto \tau^K n$, which in log-space $x = \log n$ is pure **translation**:
   \[
   S_K(x) = x + K \log \tau.
   \]
   Preserves addition ($\tau^K(m+n) = \tau^K m + \tau^K n$), but breaks multiplicativity ($(\tau^K m)(\tau^K n) = \tau^{2K} m n \notin L_K$). The grid $L_K$ cannot carry an Euler product. Leaves zero locus fixed ($Z(D_K[F]) = Z(F)$).

**Defect Classification `CONFLATED_ANALYTIC_AND_GRID_DILATION`**:
Any identification of base-power dilation $n^{\tau^{-K}}$ with grid scaling $\tau^K n$, or Fourier frequency dilation $\tau^{-K} \log n$ with the grid shift $\log n + K \log \tau$, is strictly prohibited and classified as `CONFLATED_ANALYTIC_AND_GRID_DILATION`.

**Semidirect Commutation Law**:
$A_K$ and $D_J$ do not commute; they satisfy:
\[
\boxed{A_K D_J = D_{J \tau^{-K}} A_K \iff A_K D_J A_K^{-1} = D_{J \tau^{-K}}.}
\]
The log-space commutator discrepancy is $S_K T_J(x) - T_J S_K(x) = (1 - \tau^{-J}) K \log \tau$.

**Commutator Zero-Evaluation Identity**:
Evaluating the prefactor ratio of $A_K D_J$ and $D_J A_K$ at a zero $s = \tau^K \rho$ yields normalized modulus $\tau^{K_{\mathrm{eff}} \delta}$ with $K_{\mathrm{eff}} = J(\tau^K - 1)$. Its reflection defect is identically:
\[
\boxed{|R_{\mathrm{norm}}(\rho)| + |R_{\mathrm{norm}}(\rho^\#)| - 2 = 4\sinh^2\left(\frac{K_{\mathrm{eff}}\delta\log\tau}{2}\right) = B_\rho(K_{\mathrm{eff}}).}
\]

### 9.5 Graded Arithmetic Monoid, Grade Units, and Resolution of Fork B

The full family of TC arithmetic grids forms an $\mathbb A_{\mathbb R}$-graded commutative monoid:
\[
\boxed{\mathcal M_\tau = \mathbb A_{\mathbb R} \times \mathbb Z_{\ne 0} = (\mathbb A_{\mathbb R}, +) \times (\mathbb Z_{\ne 0}, \times),}
\]
with multiplication law:
\[
(K, n) \star (J, m) = (K + J, n m), \qquad e = (0, 1).
\]
The realization map $\Phi_\tau(K, n) = n \tau^K$ is a monoid homomorphism into $(\mathbb R^\times, \times)$.

1. **Grade Units and Unique Factorization**:  
   The unit group is $U(\mathcal M_\tau) = \mathbb A_{\mathbb R} \times \{\pm 1\}$. Every grade defines an invertible **grade unit** $u_K = (K, 1)$ satisfying $u_K \star u_J = u_{K+J}$ and $u_K^{-1} = u_{-K}$. Every element factors uniquely as:
   \[
   (K, n) = u_K \star (0, \operatorname{sgn} n) \star \prod_{p \in \mathcal P} (0, p)^{v_p(|n|)}.
   \]
   **TC grades do not create new primes.** Realized elements $p\tau^K$ are native rational primes transported by grade units.

2. **Quotient Recovers Native Integer Arithmetic**:  
   The projection $\pi: \mathcal M_\tau \to \mathbb Z_{\ne 0}$, $\pi(K, n) = n$ has kernel $\ker \pi = U_{\mathrm{grade}} = \{ u_K : K \in \mathbb A_{\mathbb R} \}$, proving:
   \[
   \mathcal M_\tau / U_{\mathrm{grade}} \cong (\mathbb Z_{\ne 0}, \times).
   \]
   Every coset in $\mathcal M_\tau / U_{\mathrm{grade}}$ comprises all graded representations of one native integer referent.

3. **Refined Euler-Product Interpretation**:  
   The fixed-grade Dirichlet series is a single global grade-unit twist of the universal native Euler product:
   \[
   D_K[\zeta](s) = \chi_s(u_K) \zeta(s) = \tau^{-K s} \prod_{p \in \mathcal P} (1 - p^{-s})^{-1}.
   \]
   The grid does not possess an independent Euler product.

4. **Rational-Grade Escape Theorem**:  
   For all $K \in \mathbb Q \setminus \{0\}$ and $J \in \mathbb A_{\mathbb R} \setminus \{0\}$, $J \tau^{-K} \notin \mathbb A_{\mathbb R}$ by Lindemann (1882) transcendence of $\pi$. Analytic dilation $(J, n) \mapsto (J\tau^{-K}, n^{\tau^{-K}})$ simultaneously escapes both $\mathbb A_{\mathbb R}$ and $\mathbb Z$.
   - *Base coordinate nonintegrality*: For $K > 0$ and $n = 2$, $1 < 2^{\tau^{-K}} < 2$, so $2^{\tau^{-K}} \notin \mathbb Z$.
   - *Status classification*: General transcendence of $n^{\tau^{-K}}$ is OPEN. Gelfond–Schneider does not apply because $\tau^{-K}$ is transcendental. Counter-control: $\alpha = \log_2 3$ is transcendental yet $2^\alpha = 3 \in \mathbb Z$.

5. **Resolution of Governing Decision Point (Fork B)**:  
   Algebraic-grade closure is an imposed indexing skeleton, not an intrinsic constraint of $\zeta(s)$. The escape $J \tau^{-K} \notin \mathbb A_{\mathbb R}$ holds unconditionally whether RH is true or false ($\delta$-independent). The analytic action naturally lives in the ambient completion $\mathcal M_\tau^{\mathrm{ambient}} = \Gamma_\tau \times \exp(\Lambda_\tau) \subset \mathbb R \times \mathbb R_{>0}$, where $\Gamma_\tau = \operatorname{span}_{\mathbb A_{\mathbb R}}\{\tau^K : K \in \mathbb A_{\mathbb R}\}$ is a countable algebraic-transcendental ring and $\Lambda_\tau = \operatorname{span}_{\mathbb Z}\{\tau^K \log p : K \in \mathbb A_{\mathbb R}, p \in \mathcal P\}$, with no contradiction and no required closure.

6. **Origin of the Spectral Detector from Grade Units**:  
   The reflection defect $B_\rho(K)$ is the exact reflection defect of the normalized grade-unit character $\widehat\chi_s(u_K) = \tau^{-K(s - 1/2)}$:
   \[
   \boxed{|\widehat\chi_\rho(u_K)| + |\widehat\chi_{1-\rho}(u_K)| - 2 = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right) = B_\rho(K).}
   \]
   Positivity and zero-rigidity ($B_\rho(K) = 0 \iff \delta = 0$) arise algebraically from the grade-unit character under functional equation reflection.

### 9.6 Zero-Induced Grade Characters, Unitarity, and the Positive-Definite Constraint

TASK-TC-019 establishes the representation-theoretic reformulation of the Riemann Hypothesis via grade-unit characters:

1. **Normalized Zero-Induced Grade Character**:  
   For a nontrivial zero $\rho = 1/2 + \delta + i\gamma$ and integer grade $K \in \mathbb Z$:
   \[
   \boxed{\eta_\rho(K) \coloneqq \tau^{-K(\rho - 1/2)} = \tau^{-K(\delta + i\gamma)}, \qquad |\eta_\rho(K)| = \tau^{-K\delta}.}
   \]
   $\eta_\rho: (\mathbb Z, +) \to (\mathbb C^\times, \times)$ is a multiplicative group character: $\eta_\rho(K + J) = \eta_\rho(K)\eta_\rho(J)$, $\eta_\rho(0) = 1$, $\eta_\rho(-K) = \eta_\rho(K)^{-1}$.

2. **TC Unitarity Reformulation of RH**:  
   A character $\eta$ on $\mathbb Z$ is unitary if $|\eta(K)| = 1$ for all $K \in \mathbb Z$.
   \[
   \boxed{\eta_\rho \text{ is unitary on } \mathbb Z \iff \delta = 0.}
   \]
   \[
   \boxed{\text{Riemann Hypothesis} \iff \forall \rho \in \mathcal Z(\zeta), \; \eta_\rho \text{ is unitary on } \mathbb Z.}
   \]

3. **$B_\rho(K)$ as Non-Unitarity Defect**:  
   \[
   \boxed{B_\rho(K) = |\eta_\rho(K)| + |\eta_\rho(K)|^{-1} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right).}
   \]
   $B_\rho(K)$ is the exact non-unitarity defect of the grade character.

4. **Mellin Dilation Unitarity and Natural $1/2$ Centering**:  
   Multiplicative dilation $x \mapsto \tau^K x$ is strictly unitary on $L^2(\mathbb R_{>0}, dx/x)$. On $L^2(\mathbb R_{>0}, dx)$, normalized dilation $(U_K f)(x) = \tau^{K/2} f(\tau^K x)$ is unitary, with Mellin multiplier:
   \[
   \mathcal M[U_K f](s) = \tau^{-K(s - 1/2)} \mathcal M[f](s) = \eta_s(K) \mathcal M[f](s).
   \]
   The $1/2$ centering is the unique shift aligning multiplicative dilation with the Lebesgue-measure Mellin-Plancherel isometry line $\operatorname{Re}(s) = 1/2$.

5. **Dual = Adjoint Equivalence**:  
   Inversion equals complex conjugation on $\mathbb Z$ if and only if $\delta = 0$:
   \[
   \eta_\rho(K)^{-1} = \overline{\eta_\rho(K)} \iff |\eta_\rho(K)| = 1 \iff \delta = 0.
   \]

6. **Herglotz Analysis and Weil Equivalence**:  
   By Herglotz's Theorem (1911), positive-definite sequences on $\mathbb Z$ admit only unitary characters in their spectral measure on $\mathbb T$. Deducing that the zero characters $\eta_\rho$ are unitary from an arithmetic correlation requires Weil positivity. The positive-definite TC constraint is classified as `EQUIVALENT_REFORMULATION_OF_WEIL`.

### 9.7 Suzuki Localized Weil Positivity and Failure of Scale Propagation

TASK-TC-020 resolves the interaction between TC grade actions and Masatoshi Suzuki's localized Weil/screw-function theory (Suzuki 2023 [W2], 2026 [W10]):

1. **Unconditional Local Positivity vs Global Positivity**:  
   Suzuki (2026) proves that on a localized interval $[-R, R]$ with $R < R_0$, the lowest eigenvalue $\lambda_1(R)$ of the localized Weil operator $A_R$ is strictly positive ($\lambda_1(R) = \frac{3}{2R^2} + O(1/R) > 0$). However, global screw-function positivity on all of $\mathbb R$ is strictly `RH_EQUIVALENT` (Suzuki 2023).

2. **Dilation Operator Non-Intertwining**:  
   Under analytic dilation $(S_K v)(x) = \tau^{K/2} v(\tau^K x)$, the quadratic form $Q_W(S_K v) = \tau^{-K} \sum_\rho |\widehat{v}(\tau^{-K} z_\rho)|^2$ evaluates against dilated frequencies $\{\tau^{-K} z_\rho\}$ rather than zeta zeros. In log-space, dilation moves the discrete arithmetic prime impulses $\log p$ to non-arithmetic stations $\tau^{-K} \log p$. The explicit formula kernel $k(t)$ is not homogeneous, so $S_K^* A_{\tau^{-K} R} S_K \ne A_R$ (`NO_NATURAL_INTERTWINER`).

3. **Pure Rescaling and No Propagation Gain**:  
   Coordinate dilation scales the interval and operator simultaneously without controlling new physical domain (`PURE_COORDINATE_RESCALING_NO_GAIN`). Log-test translation $T_h v$ preserves individual form values ($Q_W(T_h v) = Q_W(v)$), but controlling linear combinations across translates requires cross-grade positivity, which is mathematically identical to full Weil positivity ($C_h(0) = Q_W(h) \ge 0$). TC grade covariance cannot propagate local positivity to global scales without assuming an RH-equivalent hypothesis.

4. **Suzuki Compact-Uniform Limit**:  
   The limiting route to RH in Suzuki (2026, Corollary 1.6) requires shift parameter $\lambda(R) = 0$ for all large $R$, which is equivalent to $A_R > 0$ and RH. TC adds no new control (`TC_COMPATIBLE_BUT_NO_NEW_CONTROL`).

### 9.8 Two-Pairing Firewall and Exceptional Exponent Rigidity

1. **The Two-Pairing Firewall**:  
   The mathematical contract strictly enforces separation between the two core pairings:
   - **Reflected Weil Pairing**: $Q_W(f, g) = \sum_\rho F(w_\rho) \overline{G(-\overline{w_\rho})}$. It is unconditionally shift-invariant ($Q_W(T_h f, T_h g) = Q_W(f, g)$), but its positivity is `RH_EQUIVALENT`.
   - **Ordinary Gram Pairing**: $Q_+(f, g) = \sum_\rho F(w_\rho) \overline{G(w_\rho)}$. It is unconditionally positive, but off-line modes scale under translation by $e^{-2\delta h}$, breaking shift-invariance unless $\delta = 0$.
   Never conflate positivity from $Q_+$ with invariance from $Q_W$ without proving $\delta = 0$.

2. **Exceptional Exponent Collinearity Theorem**:  
   Let $S_\tau = \{\alpha \in \mathbb A_{\mathbb R} : \tau^\alpha \in \overline{\mathbb Q}\}$.
   - $S_\tau \cap \mathbb Q = \{0\}$ by Lindemann (1882) transcendence of $\tau = 2\pi$.
   - For any nonzero $\alpha, \beta \in S_\tau$, Gelfond–Schneider proves that $\beta/\alpha \in \mathbb Q$.
   - Therefore:
     \[
     \boxed{\dim_{\mathbb Q} S_\tau \le 1 \qquad (\texttt{PROVED\_FROM\_GELFOND\_SCHNEIDER}).}
     \]
   *Epistemic qualification*: This does not prove $S_\tau = \{0\}$; all exceptional exponents are $\mathbb Q$-collinear on at most one rational line in $\mathbb A_{\mathbb R}$.

3. **Rational-Grade Algebraic Separation**:  
   For $m, n \in \overline{\mathbb Q}^\times$ and $K, J \in \mathbb Q$:
   \[
   \boxed{m\tau^K = n\tau^J \iff K = J \text{ and } m = n \qquad (\texttt{PROVED\_EXACT}).}
   \]
   Noncollision of transcendental grids extends from integer coefficients to arbitrary nonzero algebraic coefficients.

4. **Two-Direction Collision Architecture**:  
   An audit of all current TC mechanisms confirms that an off-critical zero $\rho = 1/2 + \delta + i\gamma$ supplies at most one displacement direction $\delta$. No existing mechanism forces two $\mathbb Q$-independent algebraic exponents into $S_\tau$. Status is classified as `TWO_DIRECTION_COLLISION_BRIDGE_OPEN` (Report: `NO_EXISTING_TWO_DIRECTION_BRIDGE`).

### 9.9 Riemann Converter Scale Covariance and Prime Staircase Compatibility (TASK-TC-021)

1. **Riemann Converter Formula**:
   The single-frequency Möbius-inverted Riemann/Gram harmonic building block of the prime-counting function $\pi(x)$ is:
   \[
   T_{\sigma,t}(x) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \int_{-\infty + i\,t\log(x)/n}^{(\sigma + it)\log(x)/n} \frac{e^z}{z} dz \right) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \operatorname{Ei}\left( \frac{(\sigma+it)\log x}{n} \right) \right).
   \]
2. **Scale Covariance**:
   $T_{c\sigma, ct}(x^{1/c}) = T_{\sigma, t}(x)$ holds term-by-term for all real $c > 0$ (`GENERIC_CONVERTER_SCALE_COVARIANCE`). Specializing to $c = \tau^K$ yields exact TC covariance $T_{\tau^K\sigma, \tau^Kt}(x^{\tau^{-K}}) = T_{\sigma, t}(x)$.
3. **Dilation vs. Translation of Prime Stations**:
   Analytic dilation jumps at $p^{\tau^{-K}}$, whereas arithmetic realization translates primes to $p\tau^K$. Dilation and translation cannot coincide on any two distinct primes: $(\tau^{-K}-1)\log p_1 = (\tau^{-K}-1)\log p_2 \implies p_1 = p_2$. Classification: `PURE_CONVERTER_COVARIANCE_AND_ARITHMETIC_REALIZATION_MISMATCH`.

### 9.10 Faithful Tau-Graded Prime Algebra (TASK-TC-022)

1. **The Graded Ring $R_\tau$**:
   Integer-grade arithmetic realizations form the ring $R_\tau = \mathbb Z[\tau, \tau^{-1}] \subset \mathbb R$ with $\tau = 2\pi$. By Lindemann (1882) transcendence of $\tau$, $\operatorname{ev}_\tau : \mathbb Z[X, X^{-1}] \to R_\tau$ is an injective ring isomorphism: $R_\tau \cong \mathbb Z[X, X^{-1}]$.
2. **Faithful Direct Sum Grading & Grade-Zero Selection**:
   $R_\tau = \bigoplus_{K \in \mathbb Z} \mathbb Z \tau^K$. Distinct integer grades are $\overline{\mathbb Q}$-linearly independent (`FINITE_CROSS_GRADE_LINEAR_INDEPENDENCE`). A finite Laurent polynomial $F(X) \in \overline{\mathbb Q}[X, X^{-1}]$ evaluates to an algebraic native value $F(\tau) \in \overline{\mathbb Q}$ iff all nonzero-grade components vanish identically (`GRADE_ZERO_ALGEBRAICITY_SELECTION`).
3. **Primes and Graded Associates**:
   $U(R_\tau) = \{\pm\tau^K : K \in \mathbb Z\}$. For $p \in \mathbb P$, $p$ is a prime element of $R_\tau$, and $p\tau^K$ is an associate prime element. Multiplicative grades add: $(p\tau^K)(q\tau^{-K}) = pq \in \mathbb Z$.
4. **Canonical Grid Zeta**:
   $Z_K^{\mathrm{grid}}(s) = \tau^{-Ks}\zeta(s)$ has stationary zero sets ($Z_K(s) = 0 \iff \zeta(s) = 0$). Status: `ARITHMETIC_TC_IS_GRID_UNIT_TWIST`.

### 9.11 Algebraic-Grade Completion, Exceptional Transfer Geometry, and Functional-Equation Grade Bridge (TASK-TC-023)

1. **Canonical Grade Domain**:
   The full canonical grade domain of Transcendental Continuation is the field of real algebraic numbers:
   \[
   \boxed{\mathcal A = \mathbb A_{\mathbb R} = \overline{\mathbb Q} \cap \mathbb R.}
   \]
   The discrete integer skeleton $K \in \mathbb Z$ and rational extension $K \in \mathbb Q$ are proved subcases where $V_K \cap V_J = \{0\}$ for all $K - J \in \mathbb Q \setminus \{0\}$.

2. **Exceptional Algebraic Transfer Set $S_\tau$**:
   Let $S_\tau = \{\alpha \in \mathcal A : \tau^\alpha \in \overline{\mathbb Q}\}$ with $\tau = 2\pi$.
   - $S_\tau$ is a vector space over $\mathbb Q$ (closed under addition, negation, and positive real rational scaling).
   - $S_\tau \cap \mathbb Q = \{0\}$ by Lindemann's theorem.
   - Gelfond–Schneider proves $\dim_{\mathbb Q} S_\tau \le 1$ (`ONE_EXCEPTIONAL_Q_DIRECTION_ONLY`).
   - Two $\mathbb Q$-independent algebraic transfer directions cannot exist: if $\alpha_1, \alpha_2 \in S_\tau \setminus \{0\}$, then $\alpha_2 / \alpha_1 \in \mathbb Q$.
   - Unconditionally, whether $S_\tau = \{0\}$ is an OPEN problem in transcendental number theory.

3. **Exact Transfer Criterion and Subgrid Collisions**:
   - $V_K = V_J \iff K - J \in S_\tau \iff \exists a, b \in \overline{\mathbb Q}^\times : a\tau^K = b\tau^J$.
   - Integer grid collision $L_K \cap L_J \ne \emptyset \iff \tau^{K-J} \in \mathbb Q_{>0}$. If one station collides ($b\tau^K = a\tau^J$), the intersection is an infinite common subgrid $\{bt\tau^K : t \in \mathbb Z \setminus \{0\}\}$.
   - Prime grid collision uniqueness: for $K \ne J$, distinct prime grids share at most one point ($|P_K \cap P_J| \le 1$).

4. **Canonical Grid Zeta Family & Functional Equation**:
   - For all $K \in \mathcal A$, $Z_K(s) = \tau^{-Ks}\zeta(s)$ has stationary zero sets ($Z_K(s) = 0 \iff \zeta(s) = 0$).
   - Two-grade functional equation: $Z_K(s) = \chi(s)\tau^{J(1-s) - Ks} Z_J(1-s)$ with cross-grade exponent $E_{K,J}(s) = J(1-s) - Ks$.
   - Centered completed grid family $\Xi_K(s) = \tau^{-K(s-1/2)}\xi(s)$ satisfies the exact reflection law $\Xi_K(s) = \Xi_{-K}(1-s)$.
   - Local zero germ scaling: $\Xi_K^{(m)}(\rho)/\Xi_J^{(m)}(\rho) = \tau^{-(K-J)(\rho-1/2)}$. Modulus is $\tau^{-(K-J)\delta}$, which equals $1 \iff \delta = 0$. Valid detector, not an independent proof.

5. **Euler–Bernoulli Special Value Relations**:
   - $Z_1(2n) = \tau^{-2n}\zeta(2n) = (-1)^{n+1} \frac{B_{2n}}{2(2n)!} \in \mathbb Q$.
   - $Z_0(1-2n) = \zeta(1-2n) = -\frac{B_{2n}}{2n} \in \mathbb Q$.
   - Exact cross-grade relation: $Z_1(2n) = \frac{(-1)^n}{2(2n-1)!} Z_0(1-2n)$.
   - The functional equation transfers $\tau$-periods across reflection $s \leftrightarrow 1-s$, narrowing the TASK-TC-022 ledger classification to `SPECIAL_VALUE_GRADE_TRANSFER_ONLY`.
   - At nontrivial zeros, values vanish identically and local germs supply no algebraic relation (`NO_NONTRIVIAL_ZERO_GRADE_BRIDGE`, `NO_TWO_DIRECTION_ZETA_TRANSFER_FOUND` within audited structures).

6. **Local Zero Germ, Prime-Side Unit Change, and Intrinsic Grade Invariance (TASK-TC-024)**:
   - Canonical leading local zero germ: $c_F(\rho) = F^{(m)}(\rho)/m!$.
   - Transformation under grade change: $c_{\Xi_K}(\rho) = \tau^{-K(\rho - 1/2)} c_\xi(\rho)$.
   - Modulus ratio: $|c_{\Xi_K}(\rho)/c_{\Xi_J}(\rho)| = \tau^{-(K-J)\delta}$.
   - Generic entire-function control: holds for any holomorphic function multiplied by $e^{-a(s-s_0)}$ (`GENERIC_NONVANISHING_PREFACTOR_COVARIANCE`).
   - Hadamard factorization: zero divisor and canonical Weierstrass product are invariant; only linear exponent $B \mapsto B - K\log\tau$ changes (`NORMALIZATION_DEPENDENT`).
   - Unit-normalized local germ: $\widehat{c}_K(\rho) = \tau^{K(\rho - 1/2)} c_{\Xi_K}(\rho) = c_\xi(\rho)$ is identically grade-invariant, removing the $\tau^{-K\delta}$ modulus variation.
   - Unitarity audit: zero modes $e^{(\rho - 1/2)x} \notin L^2(\mathbb{R})$ for $\delta \ne 0$; translation unitarity does not force $\delta = 0$ (`RH_EQUIVALENT_REFORMULATION`).
   - Principal classification: `LOCAL_GERM_IS_GENERIC_GAUGE_DATA`. Local-germ route toward RH proof is formally FROZEN.

7. **Intrinsic Grade-Fiber Arithmetic, Ambient Realization, and Four Strata (TASK-TC-025)**:
   - Tagged arithmetic fibers: $\mathcal{F}_K = \{K\} \times \mathbb{Z} \cong \mathbb{Z}$ with internal operations $(K, m) \oplus_K (K, n) = (K, m+n)$, $(K, m) \odot_K (K, n) = (K, mn)$, and unit $1_K = (K, 1)$.
   - Realized multiplication: $(m\tau^K) \odot_K (n\tau^K) = mn\tau^K = \frac{(m\tau^K)(n\tau^K)}{\tau^K}$. Isomorphism $(L_K, +, \odot_K) \cong \mathbb{Z}$ is base-independent (`GENERIC_BASE_FIBER_INVARIANCE`).
   - Canonical transfer maps: $T_{J \leftarrow K}: (K, n) \mapsto (J, n)$ are ring isomorphisms with $\Phi_J(T_{J \leftarrow K}(x)) = \tau^{J-K}\Phi_K(x)$.
   - Normalized size & metric: $N_K(K, n) = n$, $d_K(m\tau^K, n\tau^K) = |m - n|$. Transfer maps are exact isometries.
   - Intrinsic zeta function: $\zeta_K^{\mathrm{int}}(s) = \sum_{n \ge 1} N_K(K, n)^{-s} = \zeta(s)$ is strictly grade-invariant, with canonical Euler product $\prod_p (1 - p^{-s})^{-1}$.
   - Ambient Dirichlet series: $Z_K^{\mathrm{amb}}(s) = \tau^{-Ks}\zeta_K^{\mathrm{int}}(s) = \tau^{-Ks}\zeta(s)$ (`AMBIENT_COORDINATE_DIRICHLET_SERIES`). The prefactor $\tau^{-Ks}$ is the dimensional unit realization factor.
   - Ambient group algebra: $\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ with evaluation $\operatorname{ev}_\tau: \sum a_j [K_j] \mapsto \sum a_j \tau^{K_j}$.
   - Injectivity status: $\operatorname{ev}_\tau$ is injective on $\mathbb{Z}$ (Lindemann 1882) and $\mathbb{Q}$ (clearing denominators), but open on full $\mathbb{A}_{\mathbb{R}}$ (`OPEN_FINITE_ALGEBRAIC_CROSS_GRADE_COLLAPSE`).
   - Four canonical strata: `INTRINSIC_FIBER_ARITHMETIC`, `AMBIENT_REALIZATION`, `AMBIENT_CROSS_GRADE_ALGEBRA`, and `ANALYTIC_PULLBACK`.
   - Principal classification: `DUAL_INTRINSIC_AMBIENT_STRUCTURE_REQUIRED` (and `INTRINSIC_TC_IS_TRANSPORT_OF_STRUCTURE_ONLY`).

---

# 10. Structural versus numerical grade representation

An integer-grade point can be represented structurally by

\[
\boxed{
(K,n)
}
\]

with numerical realization

\[
n\tau^K.
\]

The structural pair is exact.

The authoritative numerical realization is finite-precision/arbitrary-precision and must carry declared precision.

The implementation must not represent \(\tau\) by a hand-entered authoritative decimal constant.

Compute it from the high-precision library.

---

# 11. Camera transform

Camera zoom and pan do not alter mathematical coordinates.

\[
\boxed{
T_{\mathrm{camera}}(s)=s.
}
\]

Classification:

```text
RENDERING ONLY
```

---

# 12. Height microscope / macroscope

For selected center \(t_0\), centered horizontal displacement \(\delta\), and continuous scale \(k\), define

\[
\boxed{
s_k(u)
=
\frac12+\delta+i(t_0+\tau^k u).
}
\]

This changes only the sampled ordinate range.

The sampling line remains

\[
\boxed{
\Re(s)=\frac12+\delta.
}
\]

Classification:

```text
SAMPLING-RANGE TRANSFORM
```

This is not the same object as transcendental continuation of the complete \(s\)-coordinate.

---

# 13. Generic origin coordinate dilation

For arbitrary positive scale

\[
A>0,
\]

define

\[
\boxed{
s'=As.
}
\]

For the same zeta object expressed in the new coordinate,

\[
\boxed{
f_A(s')=\zeta(s'/A).
}
\]

If

\[
\zeta(\rho)=0,
\]

then

\[
\boxed{
\rho'=A\rho.
}
\]

The critical line maps to

\[
\boxed{
\Re(s')=\frac A2.
}
\]

Transcendental continuation is the canonical subfamily

\[
\boxed{
A=\tau^k.
}
\]

---

# 14. Centered coordinate dilation

For

\[
A>0,
\]

define

\[
\boxed{
s'
=
\frac12+A\left(s-\frac12\right).
}
\]

Equivalently,

\[
z'=Az.
\]

The same zeta object in the transformed centered coordinate is

\[
\boxed{
f_A(s')
=
\zeta\left(
\frac12+\frac{s'-\frac12}{A}
\right).
}
\]

The exact zero map is

\[
\boxed{
\rho'
=
\frac12+A\left(\rho-\frac12\right).
}
\]

The critical line remains

\[
\boxed{
\Re(s')=\frac12.
}
\]

This is not the same operation as origin dilation.

---

# 15. Zeta argument transform

Define

\[
\boxed{
f_A(s)=\zeta(As).
}
\]

Then

\[
f_A(s)=0
\iff
As=\rho.
\]

Hence

\[
\boxed{
s=\rho/A.
}
\]

Critical-line zeros map to

\[
\boxed{
\Re(s)=\frac1{2A}.
}
\]

This changes the function being evaluated in the displayed coordinate.

Do not conflate it with origin coordinate dilation.

---

# 16. Kernel transformation

Start from

\[
n^{-s}=e^{-s\log n}.
\]

Transform

\[
\log n\mapsto A\log n+C
\]

and

\[
s\mapsto Bs+D.
\]

Then

\[
\left(e^C n^A\right)^{-(Bs+D)}
=
e^{-C(Bs+D)}
n^{-A(Bs+D)}.
\]

Where the Dirichlet series converges,

\[
\boxed{
\mathcal Z_{A,C,B,D}(s)
=
e^{-C(Bs+D)}
\zeta(A(Bs+D)).
}
\]

The analytically continued right-hand side is the canonical implementation outside the convergence half-plane.

The exponential prefactor has no zeros.

For

\[
AB\neq0,
\]

the zero map is

\[
\boxed{
s_\rho
=
\frac{\rho/A-D}{B}.
}
\]

---

# 17. Inverse Scale Lock

When enabled,

\[
\boxed{
AB=1.
}
\]

Then

\[
(Bs)(A\log n)=s\log n.
\]

For

\[
C=D=0,
\]

\[
\boxed{
\mathcal Z_{A,0,1/A,0}(s)=\zeta(s).
}
\]

This is an exact identity.

Classification:

```text
EXACT KERNEL PAIRING PRESERVED
```

---

# 18. Centered kernel mode

With

\[
s=\frac12+z,
\]

define

\[
\boxed{
\mathcal Z^{\mathrm{ctr}}_{A,B}(z)
=
\zeta\left(
\frac12+ABz
\right).
}
\]

When

\[
AB=1,
\]

\[
\boxed{
\mathcal Z^{\mathrm{ctr}}_{A,1/A}(z)
=
\zeta\left(
\frac12+z
\right).
}
\]

---

# 19. Anisotropic centered deformation

For exploratory visualization only,

\[
\boxed{
z=\delta+i\gamma
\mapsto
A_\delta\delta+iA_\gamma\gamma.
}
\]

If

\[
A_\delta\neq A_\gamma,
\]

label it:

```text
NON-HOLOMORPHIC DEFORMATION
```

Do not describe it as conformal or analytic.

---

# 20. Tau-grade zero character and translation

For a nontrivial zero

\[
\rho = \frac{1}{2} + \delta + i\gamma,
\]

define the centered TC character for any algebraic grade $K \in \mathbb A_{\mathbb R}$:

\[
\boxed{
\chi_\rho(K) = \tau^{K(\rho - \frac{1}{2})}.
}
\]

Using the real logarithm of positive $\tau = 2\pi$:

\[
\chi_\rho(K) = e^{K(\rho - \frac{1}{2})\log\tau} = \tau^{K\delta} e^{iK\gamma\log\tau}.
\]

Therefore:

\[
\boxed{
|\chi_\rho(K)| = \tau^{K\delta}.
}
\]

For the reflected partner $\rho^\# = 1 - \bar\rho = \frac{1}{2} - \delta + i\gamma$:

\[
\boxed{
|\chi_{\rho^\#}(K)| = \tau^{-K\delta} = |\chi_\rho(K)|^{-1}.
}
\]

On the critical line ($\delta = 0$):

\[
|\chi_\rho(K)| = 1 \qquad \forall K \in \mathbb A_{\mathbb R}.
\]

### 20.1 Common-grade shift translation

For grades $K, J \in \mathbb A_{\mathbb R}$, define the bivariate grade correlator:

\[
\boxed{
G_\rho(K, J) = \chi_\rho(K)\overline{\chi_\rho(J)}.
}
\]

Under a common grade shift by $A \in \mathbb A_{\mathbb R}$:

\[
\boxed{
G_\rho(K+A, J+A) = \tau^{2A\delta} G_\rho(K, J).
}
\]

Hence common-grade shift invariance $G(K+A, J+A) = G(K, J)$ holds if and only if $\delta = 0$.

---

# 21. Minimal finite-grade reflection defect

Define the finite-grade reflection defect:

\[
\boxed{
B_\rho(K) = |\chi_\rho(K)| + |\chi_{\rho^\#}(K)| - 2.
}
\]

Substituting the moduli:

\[
\boxed{
B_\rho(K) = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right).
}
\]

### 21.1 Exact spectral detection theorem

For every nonzero real algebraic grade $K \in \mathbb A_{\mathbb R} \setminus \{0\}$:
1. **Universal Nonnegativity**:
   \[
   B_\rho(K) \ge 0.
   \]
2. **Sharp Critical-Line Rigidity**:
   \[
   \boxed{
   B_\rho(K) = 0 \iff \delta = 0.
   }
   \]

This is the **minimal exact spectral detector**. It requires no numerical evidence, no high-precision evaluation, and no continuous-grade derivative.

### 21.2 Generic-base control

For any real base $b > 1$, define:

\[
B_{\rho, b}(K) = b^{K\delta} + b^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log b}{2}\right).
\]

Then:

\[
B_{\rho, b}(K) \ge 0 \qquad \text{and} \qquad B_{\rho, b}(K) = 0 \iff \delta = 0.
\]

**Crucial Control Finding**: The positivity and zero-rigidity of $B_\rho(K)$ are generic properties of hyperbolic functions and are **not** specific to $\tau = 2\pi$ or to the Riemann zeta function. Therefore, the $\tau$-specific and zeta-specific mathematical content cannot reside in the detector itself; it must reside entirely in the arithmetic construction of the same-referent functional $\mathscr A_K$.

### 21.3 Connection to continuous curvature

Expanding $B_\rho(k)$ near $k = 0$ for continuous grade $k \in \mathbb R$:

\[
B_\rho(k) = (k\delta\log\tau)^2 + O((k\delta)^4).
\]

Taking the second derivative at $k = 0$:

\[
\boxed{
B_\rho''(0) = 2\delta^2(\log\tau)^2.
}
\]

Thus the continuous curvature transport invariant $B_\rho''(0)$ is the infinitesimal limit of the finite algebraic-grade defect $B_\rho(K)$. The finite algebraic-grade defect $B_\rho(K)$ is exact on its own and eliminates the need to treat continuous $k$-differentiation as foundational.

---

# 22. Explicit formula for \(\psi\)

For suitable \(x>1\), with the nontrivial zero sum interpreted in the standard symmetric sense,

\[
\boxed{
\psi(x)
=
x
-
\sum_\rho\frac{x^\rho}{\rho}
-
\log(2\pi)
-
\frac12\log(1-x^{-2}).
}
\]

Set

\[
x=\tau^K,
\qquad
K>0.
\]

Since

\[
x^\rho
=
\tau^{K/2}q_\rho^K,
\]

we obtain the exact spectrum-wide grade identity

\[
\boxed{
\sum_\rho
\frac{q_\rho^K}{\rho}
=
\tau^{-K/2}
\left[
\tau^K
-
\psi(\tau^K)
-
\log\tau
-
\frac12\log(1-\tau^{-2K})
\right].
}
\]

Important:

- this displayed arithmetic realization uses \(K>0\);
- do not call it bilateral without a separate derivation;
- do not impose an RH-equivalent size bound and call that an intermediate proof.

---

# 23. Riemann explicit-formula converter

For a declared set of positive-imaginary nontrivial zeros,

\[
\boxed{
J_N(x)
=
\operatorname{Li}(x)
-
2\Re
\sum_{0<\Im\rho\le T_N}
\operatorname{Li}(x^\rho)
-
\log2
+
R(x),
}
\]

where

\[
\boxed{
R(x)
=
\int_x^\infty
\frac{du}
{u(u^2-1)\log u}.
}
\]

For

\[
x>1,
\]

use the exact expansion

\[
\boxed{
R(x)
=
\sum_{m=1}^{\infty}
E_1(2m\log x)
=
-
\sum_{m=1}^{\infty}
\operatorname{Ei}(-2m\log x).
}
\]

Then recover the prime-counting approximation through Möbius inversion:

\[
\boxed{
\pi_N(x)
=
\sum_{m\ge1}
\frac{\mu(m)}{m}
J_N(x^{1/m}),
}
\]

stopping once

\[
x^{1/m}<2.
\]

The remainder term encodes the trivial-zero / archimedean correction. The nontrivial-zero sum alone is not the complete formula.

---

# 24. Branch convention for complex \(\operatorname{Li}\)

For real

\[
x>1
\]

and complex \(\rho\), use real

\[
\log x>0
\]

and define

\[
\boxed{
\operatorname{Li}(x^\rho)
=
\operatorname{Ei}(\rho\log x)
}
\]

with one documented principal branch convention for \(\operatorname{Ei}\).

Preview and Audit implementations must use compatible branch semantics.

---

# 25. Single-zero converter contribution

For an upper-half-plane zero and conjugate pair, define

\[
\boxed{
C_J(x,\rho)
=
-2\Re
\operatorname{Ei}(\rho\log x).
}
\]

For Möbius inversion,

\[
\boxed{
C_\pi(x,\rho)
=
\sum_{m\ge1}
\frac{\mu(m)}{m}
C_J(x^{1/m},\rho),
}
\]

subject to the same truncation rule as the full converter.

---

# 26. Coupled converter covariance

Let

\[
A>0.
\]

Transform

\[
\rho'=A\rho
\]

and

\[
x'=x^{1/A}.
\]

Then

\[
\rho'\log x'
=
A\rho
\frac{\log x}{A}
=
\rho\log x.
\]

Therefore

\[
\boxed{
C_J(x^{1/A},A\rho)
=
C_J(x,\rho).
}
\]

Similarly,

\[
\boxed{
C_\pi(x^{1/A},A\rho)
=
C_\pi(x,\rho)
}
\]

under matching domain and truncation semantics.

This is exact coupled coordinate covariance, not a nontrivial automorphism of zeta.

---

# 27. Symmetry-complete converter split

Let

\[
C(\beta)
\]

be a sufficiently smooth converter contribution at fixed \(x,\gamma\).

Define

\[
\boxed{
S(\delta)
=
C\left(\frac12+\delta\right)
+
C\left(\frac12-\delta\right)
-
2C\left(\frac12\right).
}
\]

Then

\[
\boxed{
S(-\delta)=S(\delta),
}
\]

\[
\boxed{
S(0)=0,
}
\]

and Taylor expansion gives

\[
\boxed{
S(\delta)
=
C''\left(\frac12\right)\delta^2
+
O(\delta^4).
}
\]

Therefore, where the quadratic coefficient is nonzero,

\[
\boxed{
\frac{S(\lambda\delta)}{S(\delta)}
\to
\lambda^2
}
\]

as

\[
\delta\to0.
\]

In particular,

\[
S(\delta)/S(\delta/2)\to4
\]

is generic quadratic-even behavior, not evidence of an exact universal hyperbolic converter law.

---

# 28. Local cross-height normalization

For a numerically verified simple critical-line zero

\[
\rho_n
=
\frac12+i\gamma_n,
\]

define the baseline asymptotic mean-spacing scale

\[
\boxed{
\Delta_n
=
\frac{\tau}
{\log(\gamma_n/\tau)}.
}
\]

Define

\[
\boxed{
s_n(u)
=
\frac12+i(\gamma_n+\Delta_nu).
}
\]

Then define derivative-normalized path

\[
\boxed{
P_n(u)
=
\frac{
\zeta(s_n(u))
}{
i\Delta_n\zeta'(\rho_n)
}.
}
\]

Since

\[
\zeta(\rho_n)=0,
\]

\[
\boxed{
P_n(0)=0.
}
\]

Differentiating in \(u\),

\[
\boxed{
P_n'(0)=1.
}
\]

This normalization is valid only for a verified simple zero with numerically well-conditioned nonzero derivative.

---

# 29. Local shape coefficients

Expand

\[
P_n(u)
=
u
+
c_{2,n}u^2
+
c_{3,n}u^3
+\cdots.
\]

Then

\[
\boxed{
c_{m,n}
=
\frac{
(i\Delta_n)^{m-1}
\zeta^{(m)}(\rho_n)
}{
m!\zeta'(\rho_n)
},
\qquad
m\ge2.
}
\]

These are defined observables.

They are not asserted to be constant, convergent, or RH-forcing.

---

# 30. Generic-base control

For any

\[
b>1,
\]

define

\[
\boxed{
q_{\rho,b}
=
b^{\rho-\frac12}.
}
\]

Then

\[
\boxed{
|q_{\rho,b}^K|
=
b^{K\delta}.
}
\]

Therefore the bare radial-amplification formula is generic in the positive base.

Any claim of specifically tau-dependent proof leverage must identify an additional exact property tied to

\[
\tau=2\pi.
\]

---

# 31. Exact versus conjectural classifications

Every active mathematics card or research artifact should classify a formula as one of:

```text
EXACT_IDENTITY
COORDINATE_CONTROL
DEFINED_OBSERVABLE
NUMERICAL_OBSERVATION
CANDIDATE_INVARIANT
CONJECTURAL_IMPLICATION
SYNTHETIC_DIAGNOSTIC
```

Do not display a conjectural implication as an exact identity.

---

# 32. Forbidden shortcuts

The implementation must not:

1. use the raw Dirichlet series
   \[
   \sum n^{-s}
   \]
   as the numerical definition of zeta in the critical strip;

2. seed baseline zero discovery from the external reference list and then call the result independent validation;

3. conflate camera, height sampling, origin dilation, centered dilation, argument scaling, kernel transformation, or transcendental continuation;

4. treat integer \(K\) and real \(k\) as semantically interchangeable;

5. infer zero-slice disjointness from arithmetic-lattice noncoincidence;

6. claim that compression forces an off-line zero onto the critical surface;

7. call synthetic moved-zero configurations another zeta function;

8. silently cast authoritative decimal inputs to Python `float` or NumPy `complex128` before the authoritative metric is formed;

9. infer RH from finite zero verification;

10. promote an RH-equivalent bound as a softer intermediate lemma.

---

# 33. Deterministic trust vectors

These are minimum mathematical regression vectors.

## Vector A — native transcendental grade

Set

\[
k=0.
\]

Require

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s).
}
\]

## Vector B — grade composition

For arbitrary test values \(k_1,k_2\),

\[
\boxed{
\tau^{k_1+k_2}
=
\tau^{k_1}\tau^{k_2}
}
\]

to declared precision.

## Vector C — reciprocal grades

For nonzero integer \(K\),

\[
\boxed{
\tau^K\tau^{-K}=1.
}
\]

## Vector D — zero worldline

For a reference zero \(\rho\) and selected real \(k\),

\[
\boxed{
\mathcal Z_\tau(\tau^k\rho,k)=0
}
\]

to the declared numerical residual tolerance.

## Vector E — critical surface

For

\[
s=\frac12+it,
\]

require

\[
\boxed{
\Re(\tau^k s)=\frac{\tau^k}{2}.
}
\]

## Vector F — radial invariant

For

\[
\rho=\frac12+\delta+i\gamma,
\]

require

\[
\boxed{
R_\tau(\tau^k\rho,k)=\delta.
}
\]

## Vector G — origin dilation

For generic \(A>0\),

\[
\boxed{
f_A(A s)=\zeta(s).
}
\]

## Vector H — centered dilation

For

\[
s'
=
\frac12+A(s-\frac12),
\]

require inverse mapping back to the original zeta argument.

## Vector I — argument transform zero map

For

\[
f_A(s)=\zeta(As),
\]

require predicted zero

\[
s=\rho/A.
\]

## Vector J — inverse kernel lock

For

\[
AB=1,
\quad
C=D=0,
\]

require

\[
\boxed{
\mathcal Z_{A,0,B,0}(s)=\zeta(s).
}
\]

## Vector K — zero character

Require

\[
\boxed{
|q_\rho^K|=\tau^{K\delta}.
}
\]

## Vector L — symmetric grade defect

Require

\[
\boxed{
|D_K|
=
4\sinh^2
\left(
\frac{K\delta\log\tau}{2}
\right).
}
\]

## Vector M — converter remainder

Audit numerical integration of

\[
R(x)
\]

against the \(E_1\) series at controlled \(x\).

## Vector N — converter covariance

Require

\[
\boxed{
C_J(x^{1/A},A\rho)=C_J(x,\rho).
}
\]

## Vector O — split quadratic behavior

For sufficiently small declared \(\delta\), verify the computed split against the exact Taylor expansion order without claiming an exact hyperbolic converter law.

## Vector P — cross-height normalization

At a verified simple zero require

\[
\boxed{
P_n(0)=0,
\qquad
P_n'(0)=1
}
\]

to declared numerical tolerance.

---

# 34. Proof-facing non-identity

The following is deliberately **not** part of the mathematical contract:

\[
\boxed{
\text{Transcendental Coherence}
\Longrightarrow
\text{one occupied radial leaf}.
}
\]

That is the central open research theorem.

The implementation may test candidate forms but must not encode the conclusion as an identity, axiom, or automatic verdict.

---

# 35. Riemann–Weil Explicit Formula & Grade-Indexed Constraints

## 35.1 Authoritative explicit formula normalization

For an even holomorphic test function \(h(t)\) on \(|\Im(t)| \le 1/2 + \delta\) satisfying rapid Schwartz decay on \(\mathbb R\), define the Fourier transform convention:

\[
\boxed{
\widehat h(x) = \int_{-\infty}^\infty h(t) e^{-i x t} \, dt = 2 \int_0^\infty h(t) \cos(x t) \, dt.
}
\]

The Riemann–Weil Explicit Formula residual is defined as:

\[
\boxed{
\operatorname{EF}[h; \mathcal D, \mathcal A] = \sum_{\rho \in \mathcal D} h\left(\frac{\rho - 1/2}{i}\right) - \left[ 2 \Re h(i/2) - \frac{1}{\pi} \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} \widehat h(\log n) + \frac{1}{\pi} \int_0^\infty h(t) \Re\left(\psi\left(\frac{1}{4} + \frac{it}{2}\right) - \log \pi\right) dt \right],
}
\]

where:
- \(\mathcal D\) is the zero divisor (for native \(\zeta\), \(\rho_n = 1/2 \pm i\gamma_n\));
- \(\mathcal A\) represents the fixed arithmetic data: primes, von Mangoldt weights \(\Lambda(n)\), pole at \(s=1\), and gamma factor \(\Gamma(s/2)\);
- \(\psi(z) = \Gamma'(z)/\Gamma(z)\) is the digamma function;
- \(2 \Re h(i/2)\) is the pole contribution at \(s=0, 1\).

For the true zeta divisor \(\mathcal D_\zeta\) and arithmetic data \(\mathcal A_\zeta\):

\[
\boxed{
\operatorname{EF}[h; \mathcal D_\zeta, \mathcal A_\zeta] = 0.
}
\]

## 35.2 Definition of \(\mathcal C_{K,j}\) and Fourier grade scaling

For a shared test function \(H_j(t)\) defined in grade coordinates, the grade-\(K\) representation induces:

\[
\boxed{
h_{K,j}(t) = H_j(a_K t), \qquad a_K = \tau^K = (2\pi)^K.
}
\]

The grade constraint is defined as:

\[
\boxed{
\mathcal C_{K,j} = \operatorname{EF}[h_{K,j}; \mathcal D_\zeta, \mathcal A_\zeta].
}
\]

Under the project Fourier convention, the Fourier transform scales as:

\[
\boxed{
\widehat h_{K,j}(x) = a_K^{-1} \widehat H_j(a_K^{-1} x).
}
\]

Therefore, prime frequencies scale as \(a_K^{-1} \log n = \tau^{-K} \log n\).

## 35.3 Mandatory coordinate-equivalence control

By direct substitution, the grade-\(K\) constraint is an evaluation of the native explicit formula against a scaled test function:

\[
\boxed{
\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K].
}
\]

The constraint subspace spanned by \(\{ \mathcal C_{K,j} : K \in \mathcal K, j \in \mathcal J \}\) is identical to that spanned by the expanded \(K=0\) native basis \(\{ \mathcal C_0[H_j(a_K \cdot)] : K \in \mathcal K, j \in \mathcal J \}\).
The exact theoretical classification is:

\[
\boxed{
\text{coordinate\_redundant}
}
\]

When compared strictly against a finite unexpanded \(K=0\) basis \(\{ H_j(t) \}\), the classification is:

\[
\boxed{
\text{finite\_basis\_enrichment\_only}
}
\]

These two classifications address distinct mathematical questions and must never be combined into a single interchangeable label.

## 35.4 Finite divisor defect \(\Delta \mathcal C_{K,j}\) and decomposition

When arithmetic data \(\mathcal A_\zeta\) is held fixed while the zero divisor is modified \(\mathcal D \to \mathcal D + \Delta \mathcal D\), all arithmetic, pole, and gamma terms cancel identically:

\[
\boxed{
\Delta \mathcal C_{K,j} = \operatorname{EF}[h_{K,j}; \mathcal D_\zeta + \Delta\mathcal D, \mathcal A_\zeta] - \operatorname{EF}[h_{K,j}; \mathcal D_\zeta, \mathcal A_\zeta] = \langle \Delta\mathcal D, h_{K,j} \rangle = \sum_{\rho \in \mathcal D_{\text{new}}} h_{K,j}\left(\frac{\rho - 1/2}{i}\right) - \sum_{\rho \in \mathcal D_{\text{old}}} h_{K,j}\left(\frac{\rho - 1/2}{i}\right).
}
\]

A non-zero divisor perturbation produces a non-zero defect on at least some separating test functions in the infinite space of admissible test functions, though it may have smaller projection onto any finite selected family.

- **Critical-line height perturbation**: For \(1/2 \pm i\gamma_n \mapsto 1/2 \pm i(\gamma_n + \varepsilon)\):
  - Exact defect:
    \[
    \Delta \mathcal C_{K,j}(\varepsilon) = 2 \left[ H_j(a_K(\gamma_n + \varepsilon)) - H_j(a_K \gamma_n) \right].
    \]
  - Linearized defect and Jacobian column:
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{linear}}(\varepsilon) = 2 a_K H_j'(a_K \gamma_n) \varepsilon = J_{(K,j), n} \varepsilon.
    \]
  - Non-linear remainder:
    \[
    R_{K,j}(\varepsilon) = \Delta \mathcal C_{K,j}(\varepsilon) - \Delta \mathcal C_{K,j}^{\mathrm{linear}}(\varepsilon) = \mathcal O(\varepsilon^2).
    \]

- **Symmetry-complete radial quartet decomposition**: Replacing pairs \(1/2 \pm i\gamma_a\) and \(1/2 \pm i\gamma_b\) with quartet \(1/2 \pm \delta \pm i\gamma_0\) (\(\gamma_0 = (\gamma_a + \gamma_b)/2\), total 4 zeros):
  - Height-merging baseline defect (independent of \(\delta\)):
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{merge}} = 4 H_j(a_K \gamma_0) - 2 H_j(a_K \gamma_a) - 2 H_j(a_K \gamma_b).
    \]
  - Pure radial defect (strictly vanishes at \(\delta = 0\), even in \(\delta\)):
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{radial}}(\delta) = 4 \Re\left[ H_j(a_K(\gamma_0 + i\delta)) \right] - 4 H_j(a_K \gamma_0) = 4 \Re\left[ H_j(a_K \gamma_0 + i a_K \delta) - H_j(a_K \gamma_0) \right].
    \]
  - Total defect:
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{total}}(\delta) = \Delta \mathcal C_{K,j}^{\mathrm{merge}} + \Delta \mathcal C_{K,j}^{\mathrm{radial}}(\delta).
    \]

- **Divisor perturbation validation**: Any proposed zero-divisor mutation must be verified by `validate_divisor_perturbation` to confirm symmetry completeness (\(\rho \mapsto \overline\rho\) and \(\rho \mapsto 1-\rho\)) and multiplicity preservation before evaluation. Single un-partnered complex zero mutations are rejected.

- **Epistemic boundary**: These perturbation metrics constitute a local sensitivity diagnostic under frozen arithmetic data. They do not constitute an alternative zeta function or a proof of global non-compensation across the infinite zero set.

## 35.5 Explicit formula grade independence and future candidates

1. The explicit formula family \(\mathcal C_{K,j}\) operates exclusively via the coordinate pullback identity \(\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K]\) and is **coordinate-redundant** with respect to the native explicit formula evaluated on scaled test functions.
2. Any prospective mathematical mechanism attempting to impose cross-grade constraints without test-function dilation remains an **OPEN / UNDEFINED CANDIDATE** and must not be identified with \(\mathcal C_{K,j}\).
3. The coordinate dilation \(a_K = \tau^K\) does not imply or assume any non-trivial automorphism \(\zeta(\tau^K s) = \zeta(s)\).

# 36. Second-Order Radial Variation and Defect Divisor Formulation

## 36.1 Radial projection operator and defect divisor

Let \(\mathcal D\) be a divisor of points in the critical strip \(0 < \Re(s) < 1\).
For \(\rho = 1/2 + \delta + i\gamma\), define the radial projection onto the critical line:

\[
\boxed{
\mathcal P_0(\rho) = \frac{1}{2} + i\gamma.
}
\]

For a general zero divisor \(\mathcal D = \sum_{\rho} m_\rho [\rho]\), the projected divisor is:

\[
\boxed{
\mathcal P_0(\mathcal D) = \sum_{\rho} m_\rho [\mathcal P_0(\rho)],
}
\]

and the radial defect divisor is:

\[
\boxed{
\Delta\mathcal D_{\mathrm{rad}} = \mathcal D - \mathcal P_0(\mathcal D).
}
\]

For a single symmetry-complete orbit \(\mathcal O(\rho) = \{1/2 \pm \delta \pm i\gamma\}\), the projected divisor is the critical-line pair \(2[1/2 + i\gamma] + 2[1/2 - i\gamma]\), and:

\[
\boxed{
\Delta\mathcal D_{\mathrm{rad}}(\mathcal O(\rho)) = [1/2 + \delta + i\gamma] + [1/2 - \delta + i\gamma] + [1/2 + \delta - i\gamma] + [1/2 - \delta - i\gamma] - 2[1/2 + i\gamma] - 2[1/2 - i\gamma].
}
\]

## 36.2 Exact finite-orbit second-order response

For an even, real-entire test function \(h(t)\) (with \(h(-t) = h(t)\) and \(h(t) \in \mathbb R\) for \(t \in \mathbb R\)), the evaluation on \(\mathcal O(\rho)\) is:

\[
\langle \mathcal O(\rho), h \rangle = 4 \Re\left[ h(\gamma + i\delta) \right].
\]

Holomorphic Taylor expansion along the imaginary displacement \(i\delta\) gives:

\[
h(\gamma + i\delta) = h(\gamma) + i\delta h'(\gamma) - \frac{\delta^2}{2} h''(\gamma) - i\frac{\delta^3}{6} h^{(3)}(\gamma) + \frac{\delta^4}{24} h^{(4)}(\gamma) + \mathcal O(\delta^6).
\]

Taking the real part:

\[
\Re\left[ h(\gamma + i\delta) \right] = h(\gamma) - \frac{\delta^2}{2} h''(\gamma) + \frac{\delta^4}{24} h^{(4)}(\gamma) + \mathcal O(\delta^6).
\]

Therefore, the pure radial defect response is:

\[
\boxed{
\Delta\mathcal C_h[\mathcal O(\rho)] = \langle \Delta\mathcal D_{\mathrm{rad}}(\mathcal O(\rho)), h \rangle = -2\delta^2 h''(\gamma) + \frac{\delta^4}{12} h^{(4)}(\gamma) + \mathcal O(\delta^6).
}
\]

Defining the non-negative second-order orbit variable \(u = \delta^2 \ge 0\):

\[
\boxed{
\Delta\mathcal C_h[\mathcal O(\rho)] = -2 u h''(\gamma) + \mathcal O(u^2).
}
\]

## 36.3 Multi-orbit linearized radial response matrix, quadratic energy, and finite compensation

For \(N\) hypothetical off-line zero orbits \(\{\mathcal O(\rho_n)\}_{n=1}^N\) with distinct ordinates \(\gamma_n\) and radial displacements \(u_n = \delta_n^2 \ge 0\) (\(u \in \mathbb R_+^N\)), the linearized radial defect vector across a family of test functions \(\{h_j\}_{j=1}^M\) is:

\[
\boxed{
\Delta\mathcal C^{\mathrm{linear}}_j = \sum_{n=1}^N K_{j,n} u_n, \qquad K_{j,n} = -2 h''_j(\gamma_n).
}
\]

The single-target quadratic radial energy for orbit \(n\) is:

\[
\boxed{
E(u_n) = \|K_{\cdot, n} u_n\|^2 = u_n^2 \|K_{\cdot, n}\|^2 \ge 0.
}
\]

### Mathematical Distinction: Single-Target Energy vs Subspace Cone Compensation
1. **Single-Target Positivity**: For any non-trivial test packet \(h\) where \(h''(\gamma_n) \ne 0\), the single-target energy \(E(u_n) > 0\) for \(u_n > 0\).
2. **Subspace Non-Negative Compensation**: Single-target positivity does **NOT** preclude non-negative linear combinations of the remaining columns \(K_{-n} u_{-n}\) with \(u_{-n} \ge 0\) from matching or canceling \(K_{\cdot, n} u_n\) in a finite-dimensional test space:
   \[
   \min_{u_{-n} \ge 0} \|K_{\cdot, n} u_n - K_{-n} u_{-n}\|^2.
   \]
3. **Finite Basis Nullity**: In any finite basis of \(M\) test functions (e.g. \(M=30\) channels across 100 zeros), the high numerical nullity (\(\approx 85\)) and ill-conditioning (\(\kappa \sim 10^{15}\)) produce threshold-dependent numerical behavior: compensation was found in the declared basis at the \(10^{-5}\) threshold for interior zeros (zeros 10 and 50 with relative residuals \(< 10^{-6}\)) and was not found at this threshold for peripheral zeros (zeros 1 and 100). This observational diagnostic does not prove nonexistence of a compensating measure or global radial rigidity.

## 36.4 The Projection Trap and Open Mathematical Obligations

1. **The Projection Trap**:
   - The actual zero divisor \(\mathcal D_\zeta = \sum_\rho [\rho]\) has an established arithmetic explicit-formula representation connecting its spectral sum to primes and poles: \(\operatorname{EF}[h; \mathcal D_\zeta, \mathcal A_\zeta] = 0\).
   - However, its critical-line projection \(\mathcal P_0(\mathcal D_\zeta) = \sum_\rho [1/2 + i\gamma_\rho]\) is **NOT** known to be the divisor of any Dirichlet series or Euler product, and has **NO** established independent arithmetic representation.
   - Consequently, \(\langle \mathcal P_0(\mathcal D_\zeta), h \rangle\) cannot be independently evaluated via arithmetic data without already assuming that all zeros lie on the critical line (\(\mathcal D_\zeta = \mathcal P_0(\mathcal D_\zeta)\)), which is circular.
2. **The Scoped One-Point No-Go Theorem**:
   - Let \(H\) be a holomorphic test function defined on a vertical strip containing the critical strip, and let \(G = H + H \circ (-\mathrm{id})\) be the symmetrized even holomorphic function.
   - If the quartet response \(A_H(\delta, \gamma) = 2 \Re G(\delta + i\gamma)\) is independent of \(\delta\) on an open interval \(I \ni 0\) for each \(\gamma\) in an open interval, then Cauchy-Riemann equations force \(G(z)\) to be identically constant.
   - **Scope**: Rigorously proves the **CLOSED** status of `OBL-EF-003` for fixed linear combinations and locally uniform limits of direct 1-point holomorphic Riemann–Weil evaluations.
   - Does **not** preclude nonlinear paired, sesquilinear, determinantal, operator, or zeta-divisor-specific comparison objects (`OBL-RDQ-001`, **OPEN**).

## 36.5 Countermodel Controls and Epistemic Classification

1. **Structural Countermodels**:
   - Davenport–Heilbronn and Epstein zeta functions possess functional-equation reflection symmetry \(\delta \mapsto -\delta\) and exact coordinate covariance, yet possess off-line zeros.
   - They serve as structural countermodels demonstrating that functional symmetry and coordinate covariance alone are mathematically insufficient to exclude off-line zeros.
   - We do not claim their off-line zeros are caused by one isolated missing ingredient unless proved.
2. **Epistemic Classification**:
   - The finite second-order radial response construction is classified as an **exact finite synthetic sensitivity diagnostic**.
   - It validates the local quadratic Taylor fidelity (\(\mathcal O(\delta^2)\) relative error \(< 0.04\%\)), while finite NNLS compensation remains heterogeneous and dependent on the chosen test family.

# 37. Radial-Defect Quotient \(Q(z)\), Limiting Invariant \(L_Q\), and Relative Fredholm Determinants

## 37.1 Centered coordinates and reference objects
In centered coordinate \(z = s - 1/2 = \delta + it\), let \(\Xi(z) = \xi(1/2 + z)\).
Product premises:
1. **Exclusion of Real Nontrivial Zeros**: \(\zeta(s) \ne 0\) for \(s \in (0, 1)\), so \(\gamma = \Im \lambda \ne 0\).
2. **Paired Hadamard Factorization**:
   \[
   \Xi(z) = \Xi(0) \prod_{\lambda \in \Lambda^+} \left(1 - \frac{z^2}{\lambda^2}\right)^{m_\lambda}.
   \]
3. **General Multiplicity Formula**: At each distinct zero height \(\gamma > 0\):
   \[
   m_\gamma = m_{0,\gamma} + 2 \sum_{j} n_{j,\gamma},
   \]
   where \(m_{0,\gamma} \ge 0\) is critical-line multiplicity (\(\delta=0\)) and \(n_{j,\gamma} \ge 0\) is off-line quartet multiplicity for radial orbit \(j\) (\(\delta_{j,\gamma} > 0\)).
4. **Baseline Reference Function**:
   \[
   \boxed{
   \Xi^\flat(z) = \prod_{\gamma > 0} \left(1 + \frac{z^2}{\gamma^2}\right)^{m_\gamma}.
   }
   \]
The Radial-Defect Quotient is:
\[
\boxed{
Q(z) = \frac{\Xi(z)}{\Xi(0) \Xi^\flat(z)} = \prod_{j} \left( Q_{\delta_j,\gamma_j}(z) \right)^{n_j}.
}
\]

## 37.2 Real-axis quartet factor and audited properties
For an off-line quartet \(\{\pm\delta \pm i\gamma\}\), the factor evaluated on \(z = x \in \mathbb R\) is:
\[
\boxed{
q_{\delta,\gamma}(x) = \frac{\gamma^4 \left[ (x^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2 \right]}{(\gamma^2+\delta^2)^2 (x^2+\gamma^2)^2}.
}
\]
Exact audited properties:
1. **Positivity, Boundedness, and Exact Defect Factorization**:
   \[
   0 < q_{\delta,\gamma}(x) \le 1 \quad \forall x\in\mathbb R,
   \qquad
   1 - q_{\delta,\gamma}(x) = \frac{\delta^2 x^2 \left[(\delta^2 + 2\gamma^2)x^2 + 2\gamma^2(\delta^2 + 3\gamma^2)\right]}{(\delta^2+\gamma^2)^2 (x^2+\gamma^2)^2} \ge 0.
   \]
   Equality \(q(x)=1\) holds iff \(x=0\) (for \(\delta \ne 0\)) and \(q_{0,\gamma}(x) \equiv 1\).
2. **Extremum in \(u = x^2\) and Real Minimizers**: Unique minimum in \(u = x^2 \ge 0\) at \(u_* = \delta^2 + 3\gamma^2\), corresponding to two real minimizers \(x = \pm\sqrt{\delta^2 + 3\gamma^2}\).
3. **Minimum Value**: \(q_{\min} = \frac{4}{(1+r)^2(4+r)}\) where \(r = \delta^2/\gamma^2\).
4. **Uniform Domination Estimate**:
   \[
   \sup_{x\in\mathbb R} |\log q_{\delta,\gamma}(x)| = 2\log(1+r) + \log\left(1 + \frac{r}{4}\right) \le \frac{9}{4}r.
   \]
5. **Limiting Invariant**:
   \[
   \boxed{
   L_Q = \lim_{x\to\infty} Q(x) = \prod_{j} \left(\frac{\gamma_j^2}{\gamma_j^2+\delta_j^2}\right)^{2n_j} = \prod_j (1 + r_j)^{-2n_j}.
   }
   \]
   Spectral equivalence: \(0 < L_Q \le 1\), and \(L_Q = 1 \iff \mathrm{RH}\).
6. **Grade-Indexed Covariance**: Under grade dilation \(s_K = \tau^K s \implies z_K = \tau^K z\):
   \[
   \boxed{
   Q_K(z_K) = Q_0(\tau^{-K} z_K),
   \qquad
   Q_K(\tau^K z) = Q_0(z),
   }
   \]
   while the displacement spectrum \(\{r_\lambda = \delta_\lambda^2/\gamma_\lambda^2\}\), \(L_Q\), and \(\operatorname{Tr}\mathcal R\) are strictly grade-invariant.

## 37.3 Relative Fredholm spectral formulation
Define the positive diagonal trace-class operator \(\mathcal R\) on \(\ell^2(\Lambda^+)\) by:
\[
\boxed{
\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda.
}
\]
Then:
\[
\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} < \infty,
\qquad
\det_{\mathrm F}(I + \mathcal R) = L_Q^{-1},
\qquad
-\log L_Q = \operatorname{Tr}\log(I + \mathcal R) = \log\det_{\mathrm F}(I + \mathcal R).
\]
Because \(\mathcal R \ge 0\):
\[
\operatorname{Tr}\mathcal R = 0 \iff \mathcal R = 0 \iff \mathrm{RH},
\qquad
\det_{\mathrm F}(I + \mathcal R) = 1 \iff \mathrm{RH}.
\]

## 37.4 Target hierarchy
1. **Minimal Scalar Target**: \(\operatorname{Tr}\mathcal R = \sum \frac{\delta^2}{\gamma^2}\) (RH equivalent, minimal complexity).
2. **Scalar Determinant Target**: \(D_\zeta(1) = \det_{\mathrm F}(I+\mathcal R) = L_Q^{-1}\).
3. **Full Determinant Family**: \(D_\zeta(t) = \det_{\mathrm F}(I + t\mathcal R)\).
4. **Operator Target**: Arithmetic operator isospectral to \(\mathcal R\).

# 38. Reflection-Paired Involution Kernel \(\kappa_1(z,w)\) and Arithmetic Trace Target

## 38.1 Rational involution pairing kernel
For \(z = \delta + i\gamma\), define the involution \(z^\# = -\bar z = -\delta + i\gamma\).
Define the rational kernel:
\[
\boxed{
\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1.
}
\]
Exact involution identity:
\[
z + z^\# = 2i\gamma \implies (z+z^\#)^2 = -4\gamma^2,
\qquad
z z^\# = -(\delta^2+\gamma^2).
\]
\[
\boxed{
\kappa_1(z, z^\#) = \frac{4(-(\delta^2+\gamma^2))}{-4\gamma^2} - 1 = \frac{\delta^2+\gamma^2}{\gamma^2} - 1 = \frac{\delta^2}{\gamma^2}.
}
\]
Therefore:
\[
\boxed{
\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \kappa_1(\lambda, \lambda^\#).
}
\]

## 38.2 Epistemic boundary and open research obligation
1. **Closure under involution**: Functional equation and Schwarz reflection guarantee that the zero set is closed under \(\lambda \mapsto \lambda^\#\).
2. **Open Research Theorem (OBL-RDQ-001)**: Can a divisor-independent arithmetic or spectral construction isolate the pairs \((\lambda, \lambda^\#)\) and evaluate \(\kappa_1\) to compute \(\operatorname{Tr}\mathcal R\) or \(D_\zeta(1)\)?
3. **Grade Invariance**: \(L_Q\), \(\{r_\lambda\}\), and \(\mathcal R\) are grade-invariant under \((x,\delta,\gamma)\mapsto(\tau^K x, \tau^K \delta, \tau^K \gamma)\); grade dilation alone does not force \(\operatorname{Tr}\mathcal R = 0\). Additional zeta-specific arithmetic content is required.

---

# 39. Arithmetic Radial Bridge and Candidate Evaluation Harness

## 39.1 Target distinction
1. **Determinant Target**:
   \[
   D := -\log L_Q = \log\det_{\mathrm F}(I+\mathcal R) = \sum_j 2n_j \log(1+r_j), \qquad \mathfrak A_{K,D}^{\mathrm{arith}} = D.
   \]
2. **Trace Target**:
   \[
   T := \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} = \sum_j 2n_j r_j, \qquad \mathfrak A_{K,T}^{\mathrm{arith}} = T.
   \]
3. **Regularized Weighted Target**:
   \[
   T_a := \sum_{\lambda\in\Lambda^+} w_a(\lambda) \frac{\delta_\lambda^2}{\gamma_\lambda^2}, \qquad w_a(\lambda) = m_\lambda e^{-a\gamma_\lambda^2} > 0.
   \]

## 39.2 Strict arithmetic input firewall
Permitted: prime powers, von Mangoldt \(\Lambda(n)\), Euler product (\(\Re(s)>1\)), pole at \(s=1\), gamma factor, functional equation \(\xi(s)=\xi(1-s)\), Schwarz reflection, admissible test functions, exact bilateral grades \(K\in\mathbb Z\), transcendental continuation \(\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)\).
Forbidden: zero lists, \(\delta_j, \gamma_j, \lambda_j^\#\), projected ordinates, projected divisor \(\mathcal P_0(\mathcal D_\zeta)\), \(\Xi^\flat\), \(Q, L_Q, \mathcal R, D, T\), or circular RH-equivalent definitions.

## 39.3 Grade-centering geometry
Under origin dilation \(s_K = \tau^K s\), the critical line \(\Re(s)=1/2\) maps to \(\Re(s_K) = \tau^K/2 = c_K\).
The centered grade coordinate is:
\[
z_K = s_K - c_K = \tau^K s - \frac{\tau^K}{2} = \tau^K\left(s - \frac{1}{2}\right) = \tau^K z.
\]
The centered completed xi function satisfies:
\[
\Xi_K(z_K) = \xi\left(\frac{1}{2} + \tau^{-K} z_K\right) \implies \Xi_K(\tau^K z) = \Xi_0(z).
\]

## 39.4 Covariance countermodel (Covariance \(\ne\) Rigidity)
The abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under reflection \(s \mapsto 1-s\), conjugation \(s \mapsto \bar s\), involution \(s \mapsto 1-\bar s\), and grade transport, proving that symmetry and covariance are fully compatible with \(\delta \ne 0\). Covariance alone does not force \(\delta = 0\); an independent arithmetic zero-valued anchor \(\mathfrak A_K = 0\) is required.

## 39.5 Candidate classifications
- **Candidate A (Linear Grade Differences)**: `FALSIFIED_FOR_BRIDGE` (collapses to native explicit formula \(\mathcal C_0[H\circ\tau^K]-\mathcal C_0[H]\)).
- **Candidate B (Bilinear Cross-Grade Explicit Formula)**: `FALSIFIED_FOR_PAIR_ISOLATION` (\(D_K(s)\overline{D_L(s)}\) yields unrestricted double sum over all zero pairs; off-diagonal terms contaminate).
- **Candidate C (Tensor-Square Trace Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (unrestricted double sum).
- **Candidate D (Log-Derivative Contour Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (residue cross-terms across critical strip).
- **Candidate E (Relative Determinant from Arithmetic Space)**: `OPEN_UNPROVED` (no zero-independent operator).
- **Candidate F (Grade-Indexed Prime-Power Pairing)**: `OPEN_UNPROVED` (pairing law unproved).
- **Candidate G (Weighted Regularized Bridge)**: `LIVE_UNDERIVED` (spectral detector \(T_a>0\) proved; arithmetic realization open).

---

# 40. Separated Signal Bridge & Arbitrary Algebraic Curvature Rigidity

## 40.1 Arbitrary Finite Curvature Identity
For any finite collection of real radial displacements \(\{d_i\}_{i=1}^N\), the double sum of squared pairwise sums decomposes exactly:
\[
\sum_{i,j=1}^N (d_i + d_j)^2 = 2N \sum_{i=1}^N d_i^2 + 2\left(\sum_{i=1}^N d_i\right)^2.
\]
1. **Unconditional Non-negativity**: \(\sum_{i,j=1}^N (d_i + d_j)^2 \ge 0\).
2. **Zero-Rigidity**: \(\sum_{i,j=1}^N (d_i + d_j)^2 = 0 \iff \forall i \in \{1,\dots,N\}, d_i = 0\).
3. **Symmetric Reduction**: When \(\sum_{i=1}^N d_i = 0\) (e.g. for reflection-symmetric pairs \(\{\delta, -\delta\}\)), the sum reduces to \(2N \sum d_i^2\).

## 40.2 Separated Signal Candidate Classifications
- **CANDIDATE_SS1 (Cauchy-Riemann Holomorphic Rigidity)**: `FALSIFIED_GATE_1_4` (Cauchy-Riemann forces holomorphic rigidity).
- **CANDIDATE_SS2 (Polarized Bilinear Cross-Difference)**: `FALSIFIED_GATE_2_5` (Unrestricted double-sum cross-term contamination).
- **CANDIDATE_SS3 (Cramér Logarithmic Phase Variance)**: `FALSIFIED_GATE_4_6` (Cramér transformation divergence; arithmetic firewall violation).
- **CANDIDATE_SS4 (Transcendental Scale Non-Resonance)**: `FALSIFIED_GATE_2_3` (Non-resonance does not eliminate off-diagonal zero-pair contamination).
- **CANDIDATE_SS5 (Direct Positive Quadratic Kernel)**: `FALSIFIED_GATE_1_6` (Holomorphic vanishing firewall).

---

# 41. Complete Finite Spectral Expansion & Exact Analytic Kernels

## 41.1 Completed Logarithmic Derivative Identity
For \(\Re(u) > 1\):
\[
P(u) := \sum_{n=2}^\infty \frac{\Lambda(n)}{n^u} = A(u) - \frac{\Xi'}{\Xi}\left(u - \frac{1}{2}\right),
\]
where \(A(u) = \frac{1}{u} + \frac{1}{u-1} - \frac{1}{2}\log \pi + \frac{1}{2}\psi(u/2)\).

## 41.2 Complete Finite Spectral Expansion
For any finite subset of zeros \(\mathcal Z_N = \{\lambda_k = \delta_k + i\gamma_k\}_{k=1}^N\) and \(z = a + it = \sigma - 1/2 + it\):
\[
S_{N, T}(\sigma) := \frac{1}{2T}\int_{-T}^T \left| A(\sigma+it) - \sum_{k=1}^N m_k \frac{2z}{z^2-\lambda_k^2} \right|^2 dt = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},
\]
where:
1. \(I_{AA} = \frac{1}{2T}\int_{-T}^T |A(\sigma+it)|^2 dt\);
2. \(I_{AZ} = \frac{1}{2T}\int_{-T}^T A(\sigma+it)\overline{Z_N(t)} dt\), \(I_{ZA} = \overline{I_{AZ}}\);
3. \(I_{ZZ} = \sum_{j,k=1}^N K_T(\lambda_j, \lambda_k; a)\), with closed paired zero-zero kernel:
   \[
   K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu),
   \]
   and exact analytic translation kernel:
   \[
   \boxed{J_T(p, q) := \frac{1}{2T}\int_{-T}^T \frac{dt}{(p+it)(q-it)} = \frac{\log\left(\frac{p+iT}{p-iT}\right) + \log\left(\frac{q+iT}{q-iT}\right)}{2Ti(p+q)}.}
   \]

## 41.3 Exact Real-Axis Spectral Defect Formula
For an off-line quartet \(\{\pm\delta \pm i\gamma\}\) vs on-line pair \(\{0, \pm i\gamma\}\) at \(z = \sigma - 1/2 > 0\):
\[
\boxed{\Delta(\delta) := \frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2 + \gamma^2)[(z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2]}.}
\]
Sign behavior: \(\Delta(\delta) < 0\) for \(z^2 < 3\gamma^2 + \delta^2\) (all critical strip ordinates \(\gamma > 14\) at \(z = O(1)\)), transitioning to positive only for \(z > \sqrt{3}\gamma\).

## 41.4 Earliest Infinite Analytic Obstruction (Gate G4)
Individual zero resolvent terms belong to \(L^2(\mathbb R, dt)\) with finite norm \(\frac{\pi}{\sigma-\Re\rho}\), so \(\frac{1}{2T}\int_{-T}^T \frac{dt}{|\sigma-\rho+it|^2} \to 0\) as \(T\to\infty\). The non-zero Besicovitch mean of the arithmetic side is carried by non-uniform infinite collective cancellation. Termwise infinite limit interchange \(\lim_{T\to\infty}\sum_{\lambda,\mu} K_T = \sum_{\lambda,\mu}\lim_{T\to\infty} K_T\) is unproved and false without regularized weighting.

---

# 42. Gate G4 Windowed Expansion & Boundary Layer Limits

## 42.1 Exact Fejér Windowed Kernel
For the triangular / Fejér window \(W_T(t) = \frac{1}{T}(1 - |t|/T)\mathbf 1_{[-T, T]}(t)\):
\[
\boxed{J_T^{\text{Fejér}}(p, q) := \int_{-T}^T \frac{1}{T}\left(1 - \frac{|t|}{T}\right) \frac{dt}{(p+it)(q-it)} = \frac{I_T(p) + I_T(q)}{T(p+q)},}
\]
where
\[
I_T(w) = -\frac{(w+iT)\log(w+iT) + (w-iT)\log(w-iT) - 2w\log w}{T}.
\]

## 42.2 Asymptotic Regimes of \(J_T\)
For \(p = a - i\gamma, q = a + i\gamma\) (\(a > 0\)):
1. \(|\gamma| \ll T\) (Plateau): \(J_T \sim \frac{\pi}{2a T}\).
2. \(\gamma / T \to c \in (0, \infty)\) (Boundary Transition): \(\frac{\arctan((T-\gamma)/a) + \arctan((T+\gamma)/a)}{2a T}\).
3. \(|\gamma| \gg T\) (Outer Tail): \(J_T \sim \frac{1}{\gamma^2 - T^2}\).

## 42.3 Cofinal Limit Independence Countermodel
For \(f(H, T) = H / T\), for any fixed \(H < \infty\), \(\lim_{T\to\infty} f(H, T) = 0\). However, for proportional cofinal schedule \(H(T) = cT\) (\(c \ne 0\)), \(f(cT, T) = c \ne 0\) for all \(T \ne 0\).
Proved in Lean 4 with Mathlib `Filter.Tendsto` and elementary characterizations (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`, `cofinal_sequence_fixed_limit_zero`, `cofinal_diagonal_not_tendsto_zero`, `cofinal_sequence_diagonal_witness`, `cofinal_schedule_distinct_from_fixed_limit`):
\[
\forall H,\ \operatorname{Tendsto}\left(n \mapsto \frac{H}{n+1}\right)\ \text{atTop}\ (\mathcal N(0)) \centernot\implies \operatorname{Tendsto}\left(n \mapsto \frac{n+1}{n+1}\right)\ \text{atTop}\ (\mathcal N(0)).
\]

## 42.4 Exact Radial Response Coefficient
For an on-line multiplicity-two fibre \(Z_0(z) = \frac{4z}{z^2+\gamma^2}\) replaced by an off-line quartet \(Z_\delta(z) = \frac{4z(z^2+\gamma^2-\delta^2)}{(z^2+\gamma^2-\delta^2)^2+4\delta^2\gamma^2}\):
\[
D_\gamma(z) := \lim_{\delta\to 0} \frac{Z_\delta(z) - Z_0(z)}{\delta^2} = \frac{4z(z^2-3\gamma^2)}{(z^2+\gamma^2)^3}.
\]
The leading variation of the windowed difference \(\Delta S_W = \int W_T(t) (|A-Z_\delta|^2 - |A-Z_0|^2) dt\) is:
\[
\boxed{\Delta S_W(\sigma, \gamma, \delta, T) = \delta^2 C_W(\sigma, \gamma, T) + O(\delta^4),}
\]
where
\[
\boxed{C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt.}
\]
Algebraic numerators verified in Lean 4 over \(\mathbb C\) and \(\mathbb R\) (`complex_radial_defect_difference_numerator`, `complex_radial_second_order_numerator_decomposition`).

## 42.5 Certified Arb Ball Witness and Candidate Classification Matrix
1. **Fejér Witness WIT-02 (Rigorous Arb Ball Certificate)**:
   For \(\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8\), outward-rounded Arb ball Riemann integration directly across the complete symmetric compact support \([-16.8, 16.8]\) with 50,000 subintervals encloses:
   \[
   \Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0).
   \]
   Status: `CERTIFIED_NEGATIVE_ARB_BALL`.
2. **Numerical Evidence Witnesses (WIT 1, 3, 4)**:
   - Rectangular (\(\sigma=2.0, \gamma=14.0, \delta=0.1, T=2.8\)): \(\Delta S_W \approx -5.9067 \times 10^{-7}\) (estimated error \(\pm 1.0 \times 10^{-154}\)).
   - Abel-Poisson (\(\sigma=1.01, \gamma=21.0, \delta=0.49, T=1.05\)): \(\Delta S_W \approx -3.4414 \times 10^{-6}\) (estimated error \(\pm 2.0 \times 10^{-6}\)).
   - Gaussian (\(\sigma=1.01, \gamma=14.0, \delta=0.49, T=1.4\)): \(\Delta S_W \approx -7.2473 \times 10^{-5}\) (estimated error \(\pm 2.0 \times 10^{-19}\)).
   Status: `NUMERICAL_EVIDENCE_NEGATIVE`.
3. **Candidate Classification Matrix**:
   - Raw finite Fejér window response: `FAIL_RADIAL_POSITIVITY`.
   - Every zero-independent additive scalar subtraction of that finite Fejér response: `FAIL_RADIAL_POSITIVITY`.
   - Full infinite/cofinal CMSA-1 & CMSA-2 functionals: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
   - Finite algebraic four-term quadratic expansion: `FINITE_IDENTITY_PROVED_G4_OPEN`.
   - Grade coordinate dilation: `GRADE_COORDINATE_REDUNDANT`.
   - `CERTIFIED_NEGATIVE_ARB_BALL`: strictly an evidence/certificate status for WIT-02, never a final candidate classification.
   - **Proved Obstruction Class**: Any candidate family containing the stated finite Fejér functional and modified only by a zero-independent additive scalar reference fails unconditional radial positivity. This does not cover non-additive operators, different pairings, or the complete infinite/cofinal limit.

## 42.6 Proved Absolutely Convergent \(\ell^1\) Dirichlet-Series Mean-Square Lemma
For complex coefficients with \(\sum_{n=1}^\infty |a_n| < \infty\) (including \(a_n = \Lambda(n)n^{-\sigma}, \sigma > 1\) since \(\Lambda(n) \le \log n\)):
1. **Finite Identity**: \(\frac{1}{2T}\int_{-T}^T |\sum_{n=1}^N a_n n^{-it}|^2 dt = \sum_{n=1}^N |a_n|^2 + \sum_{1\le m \ne n \le N} a_m \overline{a_n} \frac{\sin(T\log(n/m))}{T\log(n/m)}\).
2. **Fixed-\(N\) Limit**: For fixed \(N\), off-diagonal terms vanish as \(T \to \infty\).
3. **Uniform Tail**: \(\|P - P_N\|_\infty \le \sum_{n>N} |a_n| =: \varepsilon_N \implies |\|P\|_T^2 - \|P_N\|_T^2| \le 2\varepsilon_N \sum |a_n|\) uniformly in \(T\).
4. **Interchange**: \(\lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T |P(\sigma+it)|^2 dt = \sum_{n=1}^\infty |a_n|^2\).
This internal proof replaces all external Carlson (1914) dependency labels.

## 42.7 Additive-Reference Invariance No-Go Theorem
Let \(S_W(Z) = \int W_T(t) |A(t) - Z(t)|^2 dt\). For any scalar reference term \(R_W(A)\) independent of \(Z, \delta, \gamma\):
\[
\boxed{(S_W(Z_\delta) - R_W(A)) - (S_W(Z_0) - R_W(A)) \equiv S_W(Z_\delta) - S_W(Z_0).}
\]
Consequently, a divisor-independent additive scalar subtraction cannot alter the raw radial difference. It proves that the additive class shares identically whatever sign behaviour the raw functional exhibits. Formally proved in Lean 4 (`RiemannScope.additive_reference_subtraction_invariance`).

## 42.8 Conditional Hypotheses for Integrated Pointwise Expansions
The integrated leading variation \(\Delta S_W = \delta^2 C_W + O(\delta^4)\) is **conditional** on the following four mathematical hypotheses being established for the specified window and domain:
1. **Window Integrability**: \(W_T(t) \ge 0\) with \(W_T \in L^1(\mathbb R) \cap L^\infty(\mathbb R)\) and \(\int_{\mathbb R} W_T(t) dt = 1\).
2. **Denominator Separation**: For all \(\delta \in [0, \delta_0]\) with \(\delta_0 < a = \sigma - 1/2\), the denominators of \(Z_\delta(a+it)\) are separated from zero uniformly: \(|a \pm \delta + i(t \pm \gamma)| \ge a - \delta_0 > 0\).
3. **Uniform Domination**: The Taylor remainder function \(R_4(t, \delta) = \delta^{-4} (|A-Z_\delta|^2 - |A-Z_0|^2 + 2\delta^2 \Re(F_0 \overline{D_\gamma}))\) satisfies \(|R_4(t, \delta)| \le g(t)\) for all \(\delta \in [0, \delta_0]\), where \(g \in L^1(\mathbb R, W_T(t)dt)\).
4. **Legitimacy of Limit Interchange**: Under hypotheses 1–3, the Dominated Convergence Theorem justifies exchanging the limit \(\delta \to 0\) and the integral, establishing \(\lim_{\delta\to 0} \frac{\Delta S_W}{\delta^2} = C_W(\sigma, \gamma, T)\).

## 42.9 Finite Dirichlet-Polynomial Algebraic Identities, Schedule Covariance, and Subcritical Norm Bounds in Lean 4
Formalized in `formal/RiemannScope/ArithmeticBridge.lean`:
1. `complex_finset_sum_mul_star`: \((\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)} = \sum_{i \in s} \sum_{j \in s} b_i \overline{b_j}\).
2. `complex_finset_normSq_eq_double_sum_re`: \(\operatorname{normSq}(\sum_{i \in s} b_i) = \Re(\sum_{i \in s} \sum_{j \in s} b_i \overline{b_j})\).
3. `abstract_finite_kernel_decomposition`: \((\sum_{i \in s} \sum_{j \in s} K(i, j)) = (\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)}\) under hypothesis \(K(i, j) = b_i \overline{b_j}\).
4. `linear_operator_finite_double_sum_interchange`: \(L(\sum_{i \in s} \sum_{j \in s} K(i, j)) = \sum_{i \in s} \sum_{j \in s} L(K(i, j))\) for additive maps \(L : \mathbb C \to+ \mathbb C\).
5. `abstract_windowed_kernel_expansion`: \(L(\operatorname{normSq}(\sum_{i \in s} b_i)) = L((\sum_{i \in s} \sum_{j \in s} K(i, j)).\text{re})\).
6. `linear_schedule_grade_covariant`: \(\forall c, \tau\), \(H_c(T) = cT\) is discrete grade-covariant (\(H_c(\tau T) = \tau H_c(T)\)).
7. `grade_covariant_schedule_nonuniqueness`: Grade covariance alone does NOT uniquely select a schedule; for \(c_1 \ne c_2\), \(H_{c_1}\) and \(H_{c_2}\) are covariant and distinct for all \(T > 0\).
8. `periodic_modulated_schedule_covariant`: Periodic modulation in \(\log_\tau T\) preserves grade covariance.
9. `exact_remainder_cancellation`: \(R = F - Z \implies Z + R = F\) identically.
10. `functional_decomposition_independence`: \(\forall f, f(Z + R) = f(F)\) whenever \(R = F - Z\).
11. `complex_squared_norm_difference_expansion`: \(Q(F, \Delta) = \operatorname{normSq}(F+\Delta) - \operatorname{normSq}(F) = \operatorname{normSq}(\Delta) + 2\Re(F\bar\Delta)\).
12. `complex_squared_norm_difference_background_subtraction`: \(Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)\).
13. `complex_squared_norm_difference_not_background_independent`: Counterexample \(F=1, G=-1, \Delta=1 \implies Q(1, 1)=3 \ne -1=Q(-1, 1)\).
14. `fixed_finite_energy_scaling_zero`: For any constant \(E \in \mathbb R\), \(\lim_{T\to\infty} \left|\frac{E}{2T}\right| = 0\).
15. `subcritical_norm_response_bound_vanishes`: Pointwise/bound lemma establishing that if \(|V| \le x^2/2 + C|x|\) for \(C \ge 0\), then \(|V| < \varepsilon\) whenever \(|x| \le 1\) and \(|x| < \varepsilon / (1/2 + C)\).
16. `subcritical_norm_response_tendsto_zero`: Mathlib `Filter.Tendsto` theorem establishing that for sequence \(x_n \to 0\) and \(C \ge 0\), any sequence \(|V_n| \le x_n^2/2 + C|x_n|\) converges to 0.
17. `resolvent_difference_rational_identity`: \(1/(w-\delta) - 1/w = \delta / (w(w-\delta))\) for \(w \ne 0, w-\delta \ne 0\).
18. `resolvent_reflection_pair_cancellation`: \((1/(w-\delta) - 1/w) + (1/(w+\delta) - 1/w) = 2\delta^2 / (w(w^2-\delta^2))\) for \(w \ne 0, w \pm \delta \ne 0\).
19. `subcritical_norm_contrapositive`: \(\neg \operatorname{Tendsto} V \operatorname{atTop} (\mathcal N 0) \implies \neg \operatorname{Tendsto} x \operatorname{atTop} (\mathcal N 0)\).
20. `not_tendsto_zero_subsequential_lower_bound`: \(\neg \operatorname{Tendsto} x \operatorname{atTop} (\mathcal N 0) \implies \exists \varepsilon > 0, \forall N, \exists n \ge N, |x_n| \ge \varepsilon\).

## 42.10 Schedule Covariance, Background Dependence, and Fixed-Finite Invisibility
### Origin Coordinate Dilation and Schedule Covariance Law
In Transcendental Continuation (TC), the project uses **origin coordinate dilation**:
\[
s_K = \tau^K s, \quad c_K = \frac{\tau^K}{2}, \quad z_K = s_K - c_K = \tau^K\left(s - \frac{1}{2}\right).
\]
On the imaginary axis, ordinate dilates as \(t_K = \tau^K t \implies t' = \tau t\). Scale covariance between window width \(T\) and height cutoff \(H\) requires:
\[
\boxed{H(\tau T) = \tau H(T), \quad \tau = 2\pi.}
\]
- **General Solution (Paper Proved)**: \(H(T) = T \cdot q(\log_\tau T)\) with \(q : \mathbb R \to (0, \infty)\) 1-periodic.
- **Asymptotic Limit Collapse (Paper Proved)**: If \(\lim_{T\to\infty} H(T)/T\) exists and \(\tau > 1\), \(H(T) = cT\).
- **Selection Condition**: Unproved heuristic note; omitted zero bounds do not force \(c \ge 1\) by proved estimate alone.
- **Falsified Premise**: *"Bilateral discrete grade covariance uniquely determines the cofinal schedule."*

### Background-Dependence Theorem & Scope of Additive Invariance
For complex-valued background \(F\) and perturbation \(\Delta\), the squared-norm variation is:
\[
Q(F, \Delta) = |F + \Delta|^2 - |F|^2 = |\Delta|^2 + 2\Re(F\bar\Delta).
\]
For two distinct backgrounds \(F\) and \(G\), \(Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)\).
The theorem `additive_reference_subtraction_invariance` applies only to outer scalar subtractions \((S - R)\) and does NOT apply to backgrounds placed inside squared norms.
**Correction**: The claim that Case B automatically reduces to the certified finite Fejér response is withdrawn; the sign of \(Q(F_0, \Delta)\) depends explicitly on the completed-function background \(F_0\).

### Fixed Finite Perturbation Invisibility Theorem
**Proof Status**: `PROVED / EXACT / PARTIALLY_FORMALIZED`
- **Paper Proof**: Complete deductive analytic derivation (§42.10).
- **Formalized Lean 4 Component**: `RiemannScope.fixed_finite_energy_scaling_zero` formalizes the scalar sequence limit \(E/(2T) \to 0\) (`FORMALLY_PROVED COMPONENT`).
- **Python Verification**: `math_core.verify_fixed_finite_perturbation_invisibility` evaluates numerical quadrature of finite prime Dirichlet polynomial truncations across sampled windows (`NUMERICAL_EVIDENCE`).

Let \(\sigma > 1\) and \(P_\sigma(t) = \sum_{n=2}^\infty \Lambda(n) n^{-\sigma-it}\). Let \(\Delta(t) = \sum_{j=1}^N \frac{c_j}{a_j + i(t-\gamma_j)}\) with \(N < \infty, a_j > 0\).
Then \(\Delta \in L^2(\mathbb R)\) and:
\[
\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( |P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2 \right) dt = 0.
\]
A fixed finite divisor perturbation cannot produce a nonzero normalized infinite mean response.

### Perturbation Semantics and Candidate Classifications
- **Case A (Recomputed Remainder)**: \(Z_{H,\delta} + R_{H,\delta} \equiv F_\delta\) (collapses algebraically). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case B (Fixed Finite Perturbation)**: \(Z_{H,\delta} + R_{H,0} = F_0 + \Delta\) (vanishes under infinite mean). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case C (Growing / Cofinal Perturbation \(\Delta_{H(T)}\))**: Non-fixed perturbation with \(H(T) \to \infty\). Classification: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
- **Raw Finite Fejér Response**: Retained as `FAIL_RADIAL_POSITIVITY`.

## 42.11 Resolvent Algebra, Subcritical Norm Growth, and the Transcendental Continuation Activation Subgate
### Exact Resolvent Algebra and Reflection Pair Cancellation
For \(a = \sigma - 1/2 > 0, w = a + i(t-\gamma)\), and \(a - \delta > 0\):
\[
\boxed{\int_{-\infty}^\infty |r_\delta(t)|^2 dt = \frac{\pi \delta^2}{a(a-\delta)(2a-\delta)} = \frac{\pi \delta^2}{2a^3} + \mathcal O(\delta^3),}
\]
\[
\boxed{r_\delta(t) + r_{-\delta}(t) = \frac{2\delta^2}{w(w^2-\delta^2)}.}
\]
Exact first-order cancellation suppresses symmetric functional-reflection pairs to \(\mathcal O(\delta^2)\).

### Subcritical Norm Response Vanishing ($o(\sqrt{T})$ Threshold)
**Proof Status**: `PROVED / EXACT / PARTIALLY_FORMALIZED`
- **Paper Proof**: Complete deductive analytic derivation via Cauchy-Schwarz.
- **Formalized Lean 4 Component**: `RiemannScope.subcritical_norm_response_bound_vanishes`, `RiemannScope.subcritical_norm_response_tendsto_zero`, `RiemannScope.subcritical_norm_contrapositive`, `RiemannScope.not_tendsto_zero_subsequential_lower_bound` (`FORMALLY_PROVED COMPONENT`).
- **Python Evaluator**: `math_core.verify_cofinal_subcritical_norm_bound` evaluates the finite-sample bound (`NUMERICAL_EVIDENCE`).

Let \(T > 0\), and let \(P_T, \Delta_T \in L^2(-T, T)\) with \(\frac{1}{2T} \|P_T\|_{L^2(-T, T)}^2 \le M < \infty\) for all large \(T\).
Define the normalized mean-square variation:
\[
V_T = \frac{1}{2T} \int_{-T}^T \left( |P_T(t) - \Delta_T(t)|^2 - |P_T(t)|^2 \right) dt = \frac{\|\Delta_T\|^2}{2T} - \frac{1}{T}\Re\langle P_T, \Delta_T\rangle.
\]
Let \(x_T = \frac{\|\Delta_T\|_{L^2(-T, T)}}{\sqrt{T}}\). Then:
\[
\boxed{|V_T| \le \frac{1}{2} x_T^2 + \sqrt{2M} x_T.}
\]
In particular, if \(\|\Delta_T\|_{L^2(-T, T)} = o(\sqrt{T})\) as \(T \to \infty\) (i.e. \(x_T \to 0\)), then \(\lim_{T\to\infty} V_T = 0\).

**Contrapositive (Subsequential Non-Vanishing Consequence)**:
\[
\boxed{\limsup_{T\to\infty} |V_T| > 0 \implies \frac{\|\Delta_T\|_{L^2(-T, T)}}{\sqrt{T}} \not\to 0 \iff \exists \varepsilon > 0, T_k \to \infty \text{ s.t. } \|\Delta_{T_k}\| \ge \varepsilon\sqrt{T_k}.}
\]
*Distinction*: Does NOT imply an eventual \(\Omega(\sqrt{T})\) lower bound (Counterexample: \(x_n = 1\) for even \(n\), \(1/(n+1)\) for odd \(n\)).

### Withdrawal of the Riemann–von Mangoldt Norm Asymptotic
The assertion \(\|\Delta_{H(T)}\| \sim \sqrt{T \log T}\) based on Riemann–von Mangoldt counting is **WITHDRAWN** due to:
1. On-line zeros have \(\delta_j = 0\) and contribute \(r_j = 0\);
2. Unknown count and distribution of off-line zeros (could be 0, 4, finite, or sparse);
3. Defect variability across mode ordinates;
4. Off-diagonal spectral interference;
5. First-order reflection cancellation (\(r_\delta + r_{-\delta} = \mathcal O(\delta^2)\));
6. Finite interval boundary mode truncation on \([-T, T]\).

### Finite Off-Line Quartet Invisibility & Zero-Rigidity Failure
For any finite off-line zero configuration (such as a single off-line quartet \(\{1/2 \pm \delta \pm i\gamma\}\)), \(\Delta_{H(T)}(t) = \Delta(t) \in L^2(\mathbb R)\) for \(H(T) \ge \gamma\), giving \(\|\Delta_{H(T)}\| = \mathcal O(1) = o(\sqrt{T}) \implies V_T \to 0\).
The normalized mean functional cannot distinguish a finite off-line quartet from RH.
- Fixed / Subcritical Families: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- Growing Cofinal Families: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.

### The Transcendental Continuation Activation Theorem (Earliest Open Subgate)
\[
\boxed{\exists \rho \text{ with } \delta_\rho \ne 0 \implies \limsup_{T\to\infty} \frac{\|\Delta^{TC}_T\|_{L^2(-T, T)}}{\sqrt{T}} > 0.}
\]
Requires 8 structural specifications (grade combination operation, non-double-counting proof, grade weights, bilateral convergence over \(K \in \mathbb Z\), height truncation interaction, shift covariance, arithmetic representation, and non-pullback proof).
Designated as the **earliest open subgate** logically preceding \(E_T - C_T\) asymptotic evaluation.

---

# 43. Curvature-Transport Unification and Theta–Mellin Scaling

### Unified Transported Invariant
We distinguish continuous grade $k \in \mathbb R$ (for differentiation, character variation, zero worldlines $s_\rho(k) = \tau^k\rho$, and curvature $B_\rho''(0)$) from discrete integer grade checkpoints $K \in \mathbb Z$ (for bilateral lattices and circle circumferences).
At every integer grade $K \in \mathbb Z$, the circle radius $r_K = \tau^{-K}$, circle circumference $C_K = \tau^{1-K}$, and circle curvature $\kappa_K = \tau^K$ satisfy:
\[
\boxed{r_K \kappa_K = 1, \qquad C_1 = 1, \qquad \Delta\omega_K = \frac{\tau}{C_K} = \tau^K \implies L_K = \tau^K \mathbb Z.}
\]
For a nontrivial zero $\rho = 1/2 + \delta + i\gamma$, horizontal displacement at continuous grade $k \in \mathbb R$ is $d_{\rho}(k) = \tau^k \delta$. Multiplication by the transported radial unit $r(k) = \tau^{-k}$ recovers:
\[
\boxed{r(k) d_{\rho}(k) = \delta, \qquad (r(k) d_{\rho}(k))^2 = \delta^2.}
\]

### Grade Character and Reflection Curvature
The centered grade character $\chi_\rho(k) = \tau^{k(\rho-1/2)}$ satisfies $|\chi_{\rho^\#}(k)| = |\chi_\rho(k)|^{-1}$ for all $k \in \mathbb R$. The reflection-pair defect functional
\[
\boxed{B_\rho(k) = |\chi_\rho(k)| + |\chi_{\rho^\#}(k)| - 2 = 2(\cosh(k\delta\log\tau)-1) = 4\sinh^2\left(\frac{k\delta\log\tau}{2}\right) \ge 0}
\]
has native second grade variation $B_\rho''(0) = 2\delta^2(\log\tau)^2$, yielding the exact normalized curvature transport invariant:
\[
\boxed{\mathscr K_\tau(\rho) = \frac{B_\rho''(0)}{2(\log\tau)^2} = (r(k) d_{\rho}(k))^2 = \delta^2.}
\]

### Complete 4-Step Theta–Mellin Scaling Theorem
1. **Absolute Convergence & Fubini/Tonelli**: For $\Re(s) > 1$,
   \[
   \sum_{n=1}^\infty \int_0^\infty \left| e^{-\pi a^2 n^2 t} t^{s/2-1} \right| dt = a^{-\sigma} \pi^{-\sigma/2} \Gamma(\sigma/2) \zeta(\sigma) < \infty,
   \]
   justifying the interchange of summation and integration via Fubini/Tonelli.
2. **Complex Mellin Transform**:
   \[
   \int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{-s} \pi^{-s/2} \Gamma(s/2) \zeta(s) = a^{-s}\Lambda(s).
   \]
3. **Half-Density Normalization**:
   \[
   \boxed{a^{1/2} \int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{1/2-s}\Lambda(s) \implies \tau^{k/2}\int_0^\infty \Theta_{\tau^k}^+(t) t^{s/2-1} dt = \chi_s(k)^{-1}\Lambda(s).}
   \]
4. **Scaled Poisson Summation & Tail Bounds**: $\theta(a^2 t) = \frac{1}{a\sqrt{t}}\theta(1/(a^2 t))$, with Dirichlet tail bounds distinguishing unnormalized $a^{-\sigma}\pi^{-\sigma/2}|\Gamma(s/2)|\frac{N^{1-\sigma}}{\sigma-1}$ from half-density normalized $a^{1/2-\sigma}\pi^{-\sigma/2}|\Gamma(s/2)|\frac{N^{1-\sigma}}{\sigma-1}$.

### Scalar-Transport No-Go Theorem
For any grade multiplier $g(k,s)$ and grade-independent function $L(s)$, define $F(k,s) = g(k,s)L(s)$:
1. **Derivative Vanishing**: $L(\rho) = 0 \implies \left.\frac{\partial^m}{\partial k^m} F(k,\rho)\right|_{k=0} \equiv 0$ for all $m \ge 0$.
2. **Divisor Preservation**: If $g(k,s) \ne 0$, then $F(k,s) = 0 \iff L(s) = 0$.
3. **Logarithmic Derivative Splitting**: On $g(k,s)L(s) \ne 0$, $\partial_s \log F = \partial_s \log L - k\log\tau$, containing zero divisor data.
4. **Zero Worldline Pullback**: Along $s(k) = 1/2 + \tau^k(\rho-1/2)$, $F_k(s(k)) \equiv 0$ identically.
*Consequence*: Candidate CT-1 is classified as `GRADE_COORDINATE_REDUNDANT`; Candidate CT-2 (direct zero evaluation) is classified as `FAIL_ARITHMETIC_FIREWALL`.

### Scoped One-Point Holomorphic Obstruction
No fixed holomorphic local kernel $H(z)$ can equal $(\Re z)^2$ on an open set in $\mathbb C$ because $\partial_{\bar z}(\Re z)^2 = \Re z = \delta \ne 0$, violating the Cauchy-Riemann equations. Any valid non-scalar arithmetic functional must employ sesquilinear pairing, contour boundary terms, or regularized determinants.

### Symmetry-Complete Polynomial Countermodel
\[
\boxed{P_{\delta,\gamma}(z) = \left((z-i\gamma)^2-\delta^2\right)\left((z+i\gamma)^2-\delta^2\right)}
\]
satisfies even symmetry $P(-z)=P(z)$, Schwarz symmetry $\overline{P(\bar z)}=P(z)$, exact roots $\{\pm\delta \pm i\gamma\}$, and strictly positive grade curvature $B_\rho''(0) > 0$ for $\delta \ne 0$. Proves that geometric and reflection properties alone do not force $\delta = 0$ without arithmetic input.

### Transcendental Curvature Rigidity Theorem (Conditional Schema)
\[
\boxed{\mathscr A_\tau(\xi) = 0 \quad \text{and} \quad \mathscr A_\tau(\xi) = \sum_{\rho\in\Lambda^+/\#} W_\rho \delta_\rho^2 \quad (W_\rho > 0) \implies \forall \rho, \; \delta_\rho = 0 \iff \mathrm{RH}.}
\]

### Canonical Earliest Open Obligation: OBL-CT-001A
Constructing a zero-independent, non-scalar arithmetic functional $\mathscr A_\tau(\xi)$ is the program's canonical earliest open obligation (`OBL-CT-001A`). Curvature transport bypasses fixed-finite $L^2$ translation invisibility at the spectral detector level ($B_\rho''(0) > 0$), but does NOT solve CMSA Gate G4; whether a non-scalar arithmetic functional avoids or reproduces the pair-isolation/infinite-limit barrier remains an open research problem. Reference: `CURVATURE_TRANSPORT.md`.

---

# 44. Canonical Weil–Hermitian Curvature Bridge and Geometric Discrepancy

### Geometric Involution Discrepancy
For any nontrivial zero $\rho = \beta + i\gamma = 1/2 + \delta + i\gamma \in Z$, the functional reflection involution $J(\rho) = 1-\rho$ and complex conjugation involution $C(\rho) = \bar\rho$ satisfy:
\[
\boxed{J(\rho) - C(\rho) = (1 - \rho) - \bar\rho = 1 - 2\Re(\rho) = - 2\delta_\rho, \qquad |J(\rho) - C(\rho)|^2 = 4\delta_\rho^2.}
\]
*(Formally proved in Lean 4: `weil_involution_difference`, `weil_involution_norm_sq_discrepancy`).*
The second-order continuous grade curvature is proportional to the squared geometric involution discrepancy:
\[
\boxed{B_\rho''(0) = 2\delta_\rho^2(\log\tau)^2 = \frac{(\log\tau)^2}{2} |J(\rho) - C(\rho)|^2.}
\]

### Pointwise Rational Weil–Hermitian Curvature Identity
For any complex zero $\rho \notin \{0, 1\}$, with $|\rho|^2 = \beta^2+\gamma^2$, $|1-\rho|^2 = (1-\beta)^2+\gamma^2$:
\[
\boxed{\frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) - \Re\left(\frac{1}{\rho(1-\rho)}\right) = \frac{(1-2\beta)^2}{2|\rho|^2|1-\rho|^2} = \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0.}
\]
*(Formally proved in Lean 4: `pointwise_weil_curvature_identity_algebraic`, `pointwise_weil_curvature_nonneg`, `pointwise_weil_curvature_zero_iff`).*

### Discrete Zeta Divisor Summation and Hadamard Constant
Summing over all nontrivial zeros $Z$ counting multiplicity:
1. Symmetrized Hermitian sum: $\sum_{\rho \in Z} \frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) = \sum_{\rho \in Z} \frac{1}{|\rho|^2} =: N_\xi$.
2. Completed-$\xi$ Hadamard sum: $\sum_{\rho \in Z} \frac{1}{\rho(1-\rho)} = 2 + \gamma_{\text{Euler}} - \log(4\pi) =: C_\xi \approx 0.0461914179322420... \in \mathbb R$.
3. Exact Spectral Target:
\[
\boxed{N_\xi - C_\xi = \sum_{\rho \in Z} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \sum_{\rho \in Z} \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0,}
\]
with strict equality $N_\xi - C_\xi = 0$ if and only if every $\delta_\rho = 0$ (the Riemann Hypothesis).

### Arithmetic Weil Functional in Additive Coordinates and Hermitian Companion
In unified additive logarithmic coordinates $u = \log x \in \mathbb R$:
- Centered Fourier–Laplace transform: $\Phi_f(s) = \int_{\mathbb R} f(u) e^{(s-1/2)u} \, du$.
- Involution: $f^*(u) = \overline{f(-u)}$, satisfying $\Phi_{f * f^*}(s) = \Phi_f(s) \overline{\Phi_f(1-\bar s)}$.
- Hermitian Weil quadratic form: $Q_W(f) = \sum_{\rho \in Z} \Phi_f(\rho) \overline{\Phi_f(1-\bar\rho)} = \Phi_{f * f^*}(1) + \Phi_{f * f^*}(0) - \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}}[(f * f^*)(\log n) + (f * f^*)(-\log n)] + \mathcal W_{\text{arch}}(f * f^*)$.
- Hermitian companion functional: $Q_H(f) = \sum_{\rho \in Z} |\Phi_f(\rho)|^2$. On RH ($1-\bar\rho = \rho$), $Q_W(f) = Q_H(f)$.

### Test Function Audit and Probe Regularization
1. **Falsification of Naive Indicator (`FAIL_TEST_FUNCTION_IDENTIFICATION`)**:
   The naive function $g_0(x) = x^{-1/2} \mathbf 1_{[1, \tau]}(x)$ has Mellin transform $\widehat g_0(s) = \frac{\tau^{s-1/2}-1}{s-1/2} \ne 1/s$, so it does not evaluate directly to $C_\xi$ or $N_\xi$.
2. **Spectral Probe $\Phi_0(s) = 1/s$**:
   The formal probe is $\Phi_0(s) = 1/s$, corresponding to $f_0(u) = e^{u/2}\mathbf 1_{(-\infty, 0)}(u)$.
3. **Admissible Probe Regularization (`OPEN_ADMISSIBLE_PROBE_REGULARIZATION`)**:
   Because $f_0 \notin C_c^\infty(\mathbb R)$, an admissible smoothing family $f_\varepsilon \in C_c^\infty(\mathbb R)$ is required such that $\Phi_\varepsilon(s) \to 1/s$ with proved interchange of limits across spectral, prime, pole, and Archimedean terms.

### Positive-Type Factorization: Local Failure vs Global Status
1. **Local Prime Factorization Failure (`FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION`)**:
   The pure prime distribution diagonal weights $-\frac{\log p}{\sqrt{p}}$ are strictly negative, so naive diagonal prime-local Gram matrices are strictly negative-definite.
2. **Global Weil Positivity (`OPEN_GLOBAL_POSITIVE_TYPE_FACTORIZATION`)**:
   Global positivity $Q_W(f * f^*) \ge 0$ requires compensation from Archimedean and pole distributions and is globally equivalent to the Riemann Hypothesis (Weil 1952).

### Corrected Scalar vs Coordinate-Pulled Zero Worldlines
- Fixed-zero scalar multiplier: For $F(k,s) = g(k,s)L(s)$, $L(\rho) = 0 \implies F(k,\rho) = 0$ and $\partial_k^m F(k,\rho) = 0$ identically for all $m \ge 0$.
- Coordinate-pulled family: $L_k(s) = L(1/2 + \tau^{-k}(s-1/2))$ evaluated along the moving zero worldline $s_\rho(k) = 1/2 + \tau^k(\rho-1/2)$ vanishes identically: $L_k(s_\rho(k)) = L(\rho) = 0$.
- Unpulled static function: $L(s_\rho(k)) = (\tau^k - 1)(\rho - 1/2)$, which is generically non-zero for $k \ne 0, \rho \ne 1/2$.
*(Formally proved in Lean 4: `coordinate_pulled_affine_zero_worldline`, `unpulled_affine_zero_worldline_eval`).*

### Program Classification and Subgate Hierarchy
\[
\boxed{\textbf{Candidate Classification: } \texttt{EXACT\_CURVATURE\_IDENTITY\_PROVED\_ARITHMETIC\_NORM\_OPEN}}
\]
- Subgate 1: $\texttt{FAIL\_TEST\_FUNCTION\_IDENTIFICATION}$ (repaired)
- Subgate 2: $\texttt{OPEN\_ADMISSIBLE\_PROBE\_REGULARIZATION}$ (active obligation)
- Subgate 3: $\texttt{FAIL\_NAIVE\_PRIME\_LOCAL\_FACTORIZATION}$ (falsified diagonal candidate)
- Subgate 4: $\texttt{OPEN\_GLOBAL\_POSITIVE\_TYPE\_FACTORIZATION}$ (RH-equivalent barrier)

---

# 45. Integrated-$\sigma$ Resolvent Algebra and Bilateral Grade Second Variation

### Exact Quartet-Minus-Projection Resolvent Difference
For centered coordinate $z = a + it$ ($a = \sigma - 1/2 > |\delta|$):
\[
\boxed{\Delta Z_+(z) = \frac{1}{z - (\delta + i\gamma)} + \frac{1}{z - (-\delta + i\gamma)} - \frac{2}{z - i\gamma} = \frac{2\delta^2}{(z - i\gamma)((z - i\gamma)^2 - \delta^2)}.}
\]
For the complete off-line quartet (including $-i\gamma$):
\[
\Delta Z(z) = \Delta Z_+(z) + \Delta Z_-(z) = \frac{2\delta^2}{(z - i\gamma)((z - i\gamma)^2 - \delta^2)} + \frac{2\delta^2}{(z + i\gamma)((z + i\gamma)^2 - \delta^2)}.
\]
*(Formally proved in Lean 4: `exact_quartet_resolvent_identity`, **ALGEBRAIC_IDENTITY**).*

### Exact Integrability and $L^2(dt)$ Norms
For any $a > |\delta|$, $|\Delta Z_+(a+it)| = \mathcal O(|t|^{-3})$ as $t \to \pm\infty$, establishing $\Delta Z_\sigma \in L^1(\mathbb R, dt) \cap L^2(\mathbb R, dt)$ unconditionally.
Leading single-height $L^2(dt)$ norm:
\[
\boxed{\left\| \frac{2\delta^2}{(a + i(t - \gamma))^3} \right\|_{L^2(dt)}^2 = 4\delta^4 \int_{-\infty}^\infty \frac{dt}{(a^2 + (t - \gamma)^2)^3} = \frac{3\pi\delta^4}{2a^5}.}
\]
Integrating $d\sigma = da$ from $a_0 = \sigma_0 - 1/2$: $\int_{a_0}^\infty \frac{3\pi\delta^4}{2a^5} da = \frac{3\pi\delta^4}{8 a_0^4} < \infty$.

### CMSA–RDQ Logarithmic Derivative Identities
For upper height $i\gamma$, lower height $-i\gamma$, and complete quartet:
\[
q^+_{\delta, \gamma}(z) = 1 - \frac{\delta^2}{(z - i\gamma)^2}, \quad
q^-_{\delta, \gamma}(z) = 1 - \frac{\delta^2}{(z + i\gamma)^2}, \quad
q^{\mathrm{full}}_{\delta, \gamma}(z) = q^+_{\delta, \gamma}(z) q^-_{\delta, \gamma}(z).
\]
Exact logarithmic derivatives:
\[
\boxed{\frac{\partial}{\partial z} \log q^+_{\delta, \gamma}(z) = \Delta Z_+(z), \quad \frac{\partial}{\partial z} \log q^-_{\delta, \gamma}(z) = \Delta Z_-(z), \quad \frac{\partial}{\partial z} \log q^{\mathrm{full}}_{\delta, \gamma}(z) = \Delta Z_+(z) + \Delta Z_-(z) = \Delta Z_\sigma(z).}
\]

### Exact Fourier–Laplace Transforms
Under the Fourier kernel $\int_{-\infty}^\infty f(t) e^{it\xi} dt$ for $\xi > 0$ with centered coordinate $z = a + it$ ($a = \sigma - 1/2$):
- Upper single-height: $\widehat{\Delta Z_+}(\xi) = 4\pi e^{-a\xi} (\cosh(\delta\xi) - 1) e^{i\gamma\xi}$.
- Lower single-height: $\widehat{\Delta Z_-}(\xi) = 4\pi e^{-a\xi} (\cosh(\delta\xi) - 1) e^{-i\gamma\xi}$.
- Complete two-height quartet:
\[
\boxed{\widehat{\Delta Z_\sigma}(\xi) = \widehat{\Delta Z_+}(\xi) + \widehat{\Delta Z_-}(\xi) = 8\pi e^{-a\xi} (\cosh(\delta\xi) - 1) \cos(\gamma\xi).}
\]

### Prime Cross-Term Series & Continuum Sign Change
- Exact unnormalized prime cross-term (by Parseval pairing):
\[
\boxed{-2\Re \int_{\sigma_0}^\infty \int_{-\infty}^\infty P_\sigma(t) \overline{\Delta Z_\sigma(t)} dt d\sigma = -8\pi \sum_{n=2}^\infty \Lambda(n) \frac{n^{1/2 - 2\sigma_0}}{\log n} (\cosh(\delta\log n) - 1) \cos(\gamma\log n).}
\]
- Leading small-$\delta$ radial term: $-4\pi\delta^2 \sum_{n=2}^\infty \Lambda(n)(\log n) n^{1/2-2\sigma_0}\cos(\gamma\log n)$.
- Continuum sign change: At $\gamma = 0$, the series is strictly negative ($< 0$). At $\gamma = \pi/\log 2$, the $n=2$ term $-a_2\cos\pi = +a_2$ strictly dominates $\sum_{n\ge 3} a_n$, making the series strictly positive ($> 0$). Proved via certified interval arithmetic (`CONTINUUM_GAMMA_SIGN_CHANGE_PROVED`), while zero-ordinate sign remains open (`ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN`).

### Unnormalized Anchor Loss & Prime Diagonal
- Loss of arithmetic anchor: For any fixed $\sigma > 1$, $\int_{-\infty}^\infty |P_\sigma(t)|^2 dt = \infty$ diverges completely, establishing `FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT`.
- Integrated prime diagonal (matched finite truncation & tail-bounded infinite comparison):
\[
\boxed{\int_{\sigma_0}^\infty \sum_{n=2}^\infty \Lambda(n)^2 n^{-2\sigma} d\sigma = \sum_{n=2}^\infty \frac{\Lambda(n)^2}{2\log n} n^{-2\sigma_0} = -\frac{1}{2} \sum_{p \text{ prime}} \log p \log(1 - p^{-2\sigma_0}).}
\]
- External Attribution: The Hadamard spectral sum $\sum_{\rho} \frac{1}{|\rho|^2} = 2 + \gamma_{\mathrm{Euler}} - \log(4\pi)$ is established classical literature attributed to Edwards (1974, pp. 19–21) and Davenport (1980, Ch. 12), not an original discovery of this repository.

### Bilateral Grade Second Difference & Actual Zeta Cross-Term
For $\mathcal C_h = Q(F, \Delta_h) + Q(F, \Delta_{-h}) - 2Q(F, 0) = |\Delta_h|^2 + |\Delta_{-h}|^2 + 2\Re(F\overline{(\Delta_h+\Delta_{-h})})$:
1. **Exact Opposition**: If $\Delta_{-h} = -\Delta_h$, $\Delta_h+\Delta_{-h} = 0 \implies \mathcal C_h = 2|\Delta_h|^2 \ge 0$. *(Formally proved in Lean 4: `bilateral_squared_norm_centering_exact_opposite`, **ALGEBRAIC_IDENTITY**).*
2. **Generic Coordinate Dilation Cross-Term**: For $\Delta_{\pm h}(z) = \Delta Z(\tau^{\pm h} z)$, $\Delta_h+\Delta_{-h} = 2h^2 B(z) + \mathcal O(h^4) \ne 0$, leaving $4h^2\Re(F\bar B)$. *(Formally proved in Lean 4: `bilateral_second_order_asymmetry_cross_term`, **ALGEBRAIC_IDENTITY**, and `bilateral_asymmetry_cross_term_nonzero_of_re_nonzero`, **NO_GO_COMPONENT**).* Formalized load-bearing arithmetic descent count remains 0.
3. **Finite-T Pullback vs Asymptotic Redundancy**: $\mathcal C_{h,T} = \mathcal M_{0,\tau^h T} + \mathcal M_{0,\tau^{-h} T} - 2\mathcal M_{0,T}$ (`FINITE_GRADE_PULLBACK_IDENTITY`, Lean 4 `finite_grade_pullback_second_difference_identity`), but $\lim_{T\to\infty} \mathcal C_{h,T} = 0$ (`ASYMPTOTIC_GRADE_COORDINATE_REDUNDANCY`).
4. **Diagonal Cross-Term & Exact Cancelling Variances**: For the Dirichlet polynomial $P(z) = \sum_{n\ge 2} \Lambda(n) n^{-1/2-z}$, the grade family $F_h(z) = P(\tau^h z)$ has jet $F_0'(z) = -(\log\tau) z \sum \Lambda(n)(\log n) n^{-1/2-z}$ and $F_0''(z) = (\log\tau)^2 \sum \Lambda(n)(-z\log n + z^2(\log n)^2) n^{-1/2-z}$.
The reported diagonal cross-term is:
\[
\mathfrak X_{\zeta,\mathrm{diag}} = (\log\tau)^2 \sum_{n=2}^\infty \Lambda(n)^2 n^{-1-2a} \left[ -a\log n + (a^2 - v)(\log n)^2 \right] = (\log\tau)^2 \left[ (a^2 - v)S_2(a) - aS_1(a) \right],
\]
where $S_1(a) = \sum_{n\ge 2} \Lambda(n)^2 n^{-1-2a}\log n$ and $S_2(a) = \sum_{n\ge 2} \Lambda(n)^2 n^{-1-2a}(\log n)^2$.
- **Withdrawal of Universal Non-Vanishing**: The previous claim that $\mathfrak X_{\zeta,\mathrm{diag}} \ne 0$ for all $a > 0, v \ge 0$ is mathematically false and WITHDRAWN (`REPORTED_DIAGONAL_CROSS_TERM_UNIVERSAL_NONVANISHING_WITHDRAWN`).
- **Exact Cancellation Variance**: For any $a > 1/\log 2 \approx 1.442695$, because $S_2(a) \ge (\log 2) S_1(a)$, the variance $v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)} \ge a(a - 1/\log 2) > 0$ is strictly positive and cancels the diagonal cross-term identically: $\mathfrak X_{\zeta,\mathrm{diag}}(a, v_*(a)) = 0$ (`DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES`, Lean 4 `diagonal_crossterm_algebraic_reduction`, `diagonal_crossterm_cancelling_variance_zero`, `cancelling_variance_pos_of_bounds`, `cancelling_variance_pos_of_log2_bound`).
- **Window Realizability**: Any positive variance $v > 0$ is realizable by standard window scaling $W_\lambda(t) = \frac{1}{\lambda} W_0(t/\lambda)$ with $\lambda = \sqrt{v/v_0}$.
- **Corrected Dominance**: For fixed $n$ and $v$, the quadratic $a^2$ term dominates the linear $-a$ term as $a \to \infty$.
5. **Full Finite-Window Double Sum & Off-Diagonal Cross-Terms**: For a finite smooth window $W \in C_c^\infty(\mathbb R)$, the complete Dirichlet inner product is:
\[
\langle F_0, \ddot F_0 \rangle_W = \sum_{m,n=2}^\infty \Lambda(m)\Lambda(n)(mn)^{-1/2-a} (\log\tau)^2 \int_{-\infty}^\infty W(t) e^{-it\log(m/n)} \left[ -(a-it)\log n + (a-it)^2(\log n)^2 \right] dt.
\]
The diagonal terms ($m=n$) give $\mathfrak X_{\zeta,\mathrm{diag}}$, while the off-diagonal terms ($m\ne n$) are non-zero due to $\widehat W(\log(m/n)) \ne 0$ (`FULL_WINDOWED_ZETA_CROSS_TERM_DERIVED`, Lean 4 `finite_double_sum_2x2_decomp`). Knowing window variance alone does not diagonalize a finite-window inner product.
6. **Smooth Two-Bump Prime Gram Matrix**: With bump convolution $\psi_\varepsilon \in C_c^\infty(\mathbb R)$ of support $\varepsilon < \frac{1}{2}\min |\log n_1 - \log n_2|$, $W_{\text{prime}, p} = \begin{pmatrix} 0 & -w_p \\ -w_p & 0 \end{pmatrix}$ with eigenvalues $\pm w_p$, indefinite (`FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION`).

### Riemann Converter Scale Covariance and Prime Staircase Compatibility (TASK-TC-021)
1. **The Riemann Converter Formula**:
   The single-frequency building block converting complex frequency $s = \sigma + it$ into a spatial waveform along $x > 1$ is:
   \[
   \boxed{T_{\sigma,t}(x) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \int_{-\infty + i\,t\log(x)/n}^{(\sigma + it)\log(x)/n} \frac{e^z}{z} dz \right) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \operatorname{Ei}\left( \frac{(\sigma + it)\log x}{n} \right) \right) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \operatorname{Li}\left( x^{(\sigma + it)/n} \right) \right).}
   \]
   This equals the Möbius-inverted Gram/Riemann harmonic component of the prime-counting function $\pi(x)$, derived from the explicit formula for $J(x) = \sum_{n=1}^\infty \frac{1}{n} \pi(x^{1/n})$.
2. **Exact Scale-Covariance Theorem**:
   For any positive real scale factor $c > 0$, complex frequency $s = \sigma + it$, and coordinate $x > 1$:
   \[
   \boxed{T_{c\sigma, ct}\left(x^{1/c}\right) = T_{\sigma, t}(x).}
   \]
   *Proof*: The upper limit $(c\sigma + ict)\log(x^{1/c})/n = (\sigma + it)\log(x)/n$ and the lower contour imaginary height $(ct)\log(x^{1/c})/n = t\log(x)/n$ are identically invariant for every $n \ge 1$. The integrand $e^z/z$ and the weights $\mu(n)/n$ are unaltered. Specializing to $c = \tau^K$ yields exact TC covariance:
   \[
   \boxed{T_{\tau^K \sigma, \tau^K t}\left(x^{\tau^{-K}}\right) = T_{\sigma, t}(x).}
   \]
3. **Generic Scale Geometry**:
   Because the covariance holds identically for any real scale factor $c > 0$ ($c = 2, 3, \pi, \sqrt{2}$), it represents conformal scaling of the logarithmic integral $\operatorname{Li}(x^s) = \operatorname{Ei}(s\log x)$, classified as `GENERIC_CONVERTER_SCALE_COVARIANCE`.
4. **Prime-Side Counting Transformation**:
   Analytic TC dilation $\zeta_K(s) = \zeta(\tau^{-K} s)$ induces the prime-counting staircase:
   \[
   \boxed{\pi_K^{\mathrm{analytic}}(x) = \pi(x^{\tau^K}), \qquad J_K^{\mathrm{analytic}}(x) = J(x^{\tau^K}).}
   \]
   Its jumps occur at $x = p^{\tau^{-K}}$ for primes $p$, with exact integer height increment $\Delta \pi_K = 1 \in \mathbb{Z}$.
5. **Dilation vs. Translation of Prime Stations**:
   - Analytic TC embedding: $A_K(p) = p^{\tau^{-K}}$, with log-station $\log A_K(p) = \tau^{-K} \log p$ (multiplicative dilation $u \mapsto \tau^{-K} u$). Arithmetic status: `OPEN_TRANSCENDENCE_STATUS`.
   - Arithmetic TC realization: $G_K(p) = p\tau^K$, with log-station $\log G_K(p) = \log p + K\log\tau$ (additive translation $u \mapsto u + K\log\tau$). Arithmetic status: transcendental for rational $K \ne 0$ by Lindemann (1882).
6. **Centered Zero Harmonic Transformation**:
   For centered zero coordinate $w_\rho = \rho - 1/2 = \delta + i\gamma$ and normalized harmonic $H_\rho(x) = x^{w_\rho} = e^{w_\rho \log x}$ with modulus $|H_\rho(x)| = x^\delta$:
   - Analytic reciprocal scaling $w \mapsto \tau^K w$, $x \mapsto x^{\tau^{-K}}$ leaves both phase and modulus strictly invariant: $|H_{\rho, K}(x_K)| = |H_\rho(x)| = x^\delta$.
   - Arithmetic linear scaling $x \mapsto \tau^K x$ multiplies the harmonic by $\tau^{K w_\rho}$, transforming modulus by:
     \[
     \boxed{|H_\rho(\tau^K x)| = \tau^{K\delta} |H_\rho(x)|.}
     \]
   - Bilateral symmetrization recovers the canonical TC non-unitarity defect:
     \[
     \boxed{\frac{|H_\rho(\tau^K x)|}{|H_\rho(x)|} + \frac{|H_\rho(\tau^{-K} x)|}{|H_\rho(x)|} - 2 = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right) = B_\rho(K).}
     \]
7. **Multi-Prime Rigidity Theorem**:
   Dilation and translation cannot coincide on any two distinct primes $p_1 \ne p_2$:
   \[
   (\tau^{-K} - 1)\log p_1 = K\log\tau \quad \text{and} \quad (\tau^{-K} - 1)\log p_2 = K\log\tau \implies \log p_1 = \log p_2 \implies p_1 = p_2.
   \]
   Thus, no intrinsic prime-referent identity forces the converter to equal its translated counterpart.
8. **Classification**: `PURE_CONVERTER_COVARIANCE_AND_ARITHMETIC_REALIZATION_MISMATCH`.

### Faithful Tau-Graded Prime Algebra and Cross-Grade Constraint (TASK-TC-022)
1. **The TC Laurent Ring $R_\tau$**:
   The algebraic structure governing integer-grade arithmetic realizations is the subring:
   \[
   \boxed{R_\tau = \mathbb Z[\tau, \tau^{-1}] \subset \mathbb R, \qquad \tau = 2\pi.}
   \]
   Evaluation homomorphism $\operatorname{ev}_\tau : \mathbb Z[X, X^{-1}] \to R_\tau$ ($X \mapsto \tau$) is an isomorphism of rings by Lindemann (1882) transcendence of $\tau$:
   \[
   \boxed{R_\tau \cong \mathbb Z[X, X^{-1}].}
   \]
2. **Faithful Direct Sum Grading**:
   The canonical polynomial grading transfers isomorphically:
   \[
   \boxed{R_\tau = \bigoplus_{K \in \mathbb Z} \mathbb Z \tau^K.}
   \]
   Finite linear independence holds over $\overline{\mathbb Q}$: for any finite distinct integer grades $\{K_1, \dots, K_r\} \subset \mathbb Z$ and $a_j \in \overline{\mathbb Q}$,
   \[
   \sum_{j=1}^r a_j \tau^{K_j} = 0 \implies a_1 = \dots = a_r = 0 \qquad (`FINITE_CROSS_GRADE_LINEAR_INDEPENDENCE`).
   \]
3. **Grade-Zero Algebraicity Selection Theorem**:
   For any finite Laurent expression $F(X) = \sum_{K=-M}^N a_K X^K \in \overline{\mathbb Q}[X, X^{-1}]$,
   \[
   \boxed{F(\tau) \in \overline{\mathbb Q} \iff a_K = 0 \quad \forall K \ne 0 \iff F(\tau) = a_0 \in \overline{\mathbb Q} \qquad (`GRADE_ZERO_ALGEBRAICITY_SELECTION`).}
   \]
   Laurent grade decompositions are strictly unique: $F(\tau) = G(\tau) \iff F = G$.
4. **Units and Graded Prime Associates**:
   - Unit group: $U(R_\tau) = \{\pm \tau^K : K \in \mathbb Z\}$.
   - For rational prime $p \in \mathbb P$, $R_\tau / (p) \cong \mathbb F_p[X, X^{-1}]$ is an integral domain; hence $p$ is a prime element of $R_\tau$.
   - The element $p\tau^K = (\tau^K) p$ is an associate of $p$ in $R_\tau$, and therefore a prime element of $R_\tau$.
   - $P_K = \{p\tau^K : p \in \mathbb P\}$ forms the grade-$K$ homogeneous representative system of ordinary prime associate classes.
5. **No Algebraic Transfer Station**:
   For $x = m\tau^K \in L_K$ and $y = n\tau^J \in L_J$ with $m, n \in \overline{\mathbb Q}^\times$ and $K \ne J$, no algebraic scalar $\alpha \in \overline{\mathbb Q}^\times$ satisfies $\alpha x = y$ (`NO_ALGEBRAIC_TRANSFER_STATION`), since $\tau^{J-K} = \alpha m / n \in \overline{\mathbb Q}$ contradicts transcendence.
   Coordinate transfer exists exclusively via the transcendental grade unit multiplier $\tau^{J-K}$.
6. **Multiplicative Grade Conservation vs. Additive Rigidity**:
   - Additive combinations across distinct grades cannot cancel over $\overline{\mathbb Q}$.
   - Multiplicative combinations add grades: $\deg(xy) = \deg x + \deg y$.
   - Opposite grades cancel to grade zero: $(p\tau^K)(q\tau^{-K}) = pq \in \mathbb Z = R_0$. Transcendence cancels multiplicatively.
   - Total-grade-zero monomial rule: $M = a \prod_{j=1}^r (p_j \tau^{K_j})^{e_j} \in \overline{\mathbb Q} \iff \sum_{j=1}^r e_j K_j = 0$ (`TOTAL_GRADE_ZERO_ALGEBRAICITY`).
7. **Canonical Arithmetic TC Grid Zeta vs Auxiliary Analytic Pullback**:
   - **Canonical Arithmetic Grid Zeta**: For $L_K^+ = \{n\tau^K : n \ge 1\}$,
     \[
     \boxed{Z_K^{\mathrm{grid}}(s) = \sum_{n=1}^\infty (n\tau^K)^{-s} = \tau^{-Ks} \zeta(s).}
     \]
     Because $\tau^{-Ks} \ne 0$, $Z_K^{\mathrm{grid}}(s) = 0 \iff \zeta(s) = 0$. Zeros do not move under arithmetic grading.
   - **Auxiliary Analytic Pullback**: $Z_K^{\mathrm{pull}}(s) = \zeta(\tau^{-K} s)$ is an auxiliary coordinate dilation moving zeros to $\tau^K \rho$ and prime stations to $p^{\tau^{-K}}$.
   - Foundational classification: `ARITHMETIC_TC_IS_GRID_UNIT_TWIST`.
8. **Cross-Grade Constraint Audit**:
   No natural zeta identity equates a finite cross-grade expression to an algebraic number. Bilateral products $(p\tau^K)(p\tau^{-K}) = p^2$ and $|\eta_\rho(K)| \cdot |\eta_\rho(K)|^{-1} = 1$ balance total grade to zero identically.
   Constraint classification: `NO_CURRENT_ZETA_CROSS_GRADE_BRIDGE_AND_GRADE_CANCELLATION_TRIVIAL`.

---

# 21. Intrinsic Grade-Fiber Arithmetic & Canonical Four-Way Architecture (TASK-TC-025)

1. **Tagged Grade Fiber**: For each $K \in \mathbb A_{\mathbb R} = \overline{\mathbb Q} \cap \mathbb R$, the intrinsic arithmetic fiber is $\mathcal F_K = \{K\} \times \mathbb Z \cong \mathbb Z$, with operations $(K, m) \oplus_K (K, n) = (K, m + n)$, $(K, m) \odot_K (K, n) = (K, mn)$, unit $1_K = (K, 1)$, and normalized size $N_K(K, n) = n$.
2. **Canonical Transfer Isomorphisms**: $T_{J \leftarrow K}: (K, n) \mapsto (J, n)$ is an exact ring isomorphism and isometric coordinate transfer. Intrinsic zeta $\zeta_K^{\mathrm{int}}(s) = \sum N_K(K, n)^{-s} = \zeta(s)$ is strictly grade-invariant.
3. **Canonical Four-Way Classification**:
   - `INTRINSIC_FIBER_ARITHMETIC`: Intrinsic rings $\mathcal F_K \cong \mathbb Z$, intrinsic zeta $\zeta_K^{\mathrm{int}}(s) = \zeta(s)$.
   - `AMBIENT_REALIZATION`: Embedded points $n\tau^K \in \mathbb R$, ambient series $Z_K^{\mathrm{amb}}(s) = \tau^{-Ks}\zeta(s)$, local germ scaling $\tau^{-K(\rho - 1/2)}$.
   - `AMBIENT_CROSS_GRADE_ALGEBRA`: Group algebra $\mathbb A_{\mathbb R}[\mathbb A_{\mathbb R}]$ and evaluation $\operatorname{ev}_\tau: \mathbb A_{\mathbb R}[\mathbb A_{\mathbb R}] \to \mathbb R$ (or $\overline{\mathbb Q}[\mathbb A_{\mathbb R}] \to \mathbb C$), cross-grade algebra $(m\tau^K)(n\tau^J) = mn\tau^{K+J}$.
   - `ANALYTIC_PULLBACK`: Auxiliary coordinate dilation $\zeta(\tau^{-K} s)$ with moving zeros $\tau^K \rho$.
4. **Realization Kernel**: $\ker(\operatorname{ev}_\tau)$ controls finite cross-grade collapses $\sum a_j \tau^{K_j} = 0$. Injective on $\mathbb Z$ and $\mathbb Q$; open on $\mathbb A_{\mathbb R}$ (`OPEN_FINITE_ALGEBRAIC_CROSS_GRADE_COLLAPSE`).

---

# 22. Pure Unit-Rescaling No-Go Theorem & Zero-Divisor Invariance (TASK-TC-026)

1. **Dirichlet Factorization Theorem**:
   For any intrinsic Dirichlet series $D(s) = \sum_{n=1}^\infty a_n n^{-s}$, the series realized under ambient coordinate scaling $x_n = n\tau^K$ factors as:
   \[
   \boxed{D_K^{\mathrm{amb}}(s) = \sum_{n=1}^\infty a_n (n\tau^K)^{-s} = \tau^{-Ks} \sum_{n=1}^\infty a_n n^{-s} = \tau^{-Ks} D(s).}
   \]
2. **Zero-Divisor Preservation**:
   Because $\tau^{-Ks} = \exp(-Ks\log\tau) \ne 0$ for all $s \in \mathbb C$, multiplication by $\tau^{-Ks}$ preserves zero locations and multiplicities identically:
   \[
   \boxed{\operatorname{Div}_0(D_K^{\mathrm{amb}}) = \operatorname{Div}_0(D), \qquad \operatorname{mult}_\rho(D_K^{\mathrm{amb}}) = \operatorname{mult}_\rho(D).}
   \]
   Pure unit rescaling cannot create, move, or destroy any zero of $\zeta(s)$.
3. **Logarithmic Derivative Invariance**:
   \[
   \boxed{-\frac{(D_K^{\mathrm{amb}})'}{D_K^{\mathrm{amb}}}(s) = K\log\tau - \frac{D'}{D}(s).}
   \]
   The additive shift $K\log\tau$ is an entire constant function; residue at every zero $\rho$ is strictly $-\operatorname{mult}_\rho(D)$.
4. **Base-Independence**:
   For any real base $b > 0$, $D_{b,K}^{\mathrm{amb}}(s) = b^{-Ks}D(s)$. The no-go theorem is a general property of real dilations, independent of the transcendence of $\tau$.
5. **No-Go Conclusion**:
   Pure unit rescaling is an exact symmetry / gauge transformation of Dirichlet and Mellin transforms. It leaves zero divisors invariant.
   Principal classification: `PURE_UNIT_RESCALING_NO_GO_PROVED`.

---

# 23. Multi-Grade Naturality, Cocycle/Holonomy Triviality, and Scoped No-Go Theorem (TASK-TC-027)

1. **Transfer Functoriality and Loop Holonomy**:
   For the real algebraic grade set $G = \mathbb A_{\mathbb R}$, the canonical transfer maps $T_{J \leftarrow K}(K, n) = (J, n)$ form a canonically trivial pair groupoid:
   \[
   T_{K \leftarrow K} = \operatorname{id}_{\mathcal F_K}, \qquad T_{M \leftarrow J} \circ T_{J \leftarrow K} = T_{M \leftarrow K}.
   \]
   For any closed loop $K_0 \to K_1 \to \cdots \to K_r = K_0$, the composite transfer map satisfies $\prod_{i=0}^{r-1} T_{K_{i+1} \leftarrow K_i} = \operatorname{id}_{\mathcal F_{K_0}}$. There are no path-dependent or holonomy defects.

2. **Ambient Scale and Spectral Cocycles as Exact Coboundaries**:
   - The ambient coordinate scale transition factor $c(J, K) = \tau^{J-K} = g(J)/g(K)$ where $g(K) = \tau^K$.
   - The spectral grade transition factor $c_s(J, K) = \tau^{-(J-K)s} = g_s(J)/g_s(K)$ where $g_s(K) = \tau^{-Ks}$.
   - For every closed loop, the product around the cycle is identically $1$: $\prod_{i=0}^{r-1} c(K_{i+1}, K_i) = 1$ and $\prod_{i=0}^{r-1} c_s(K_{i+1}, K_i) = 1$. Both cocycles are exact 1-coboundaries.

3. **Natural Observable Reconstruction Theorem**:
   Any family of observables $O_K: \mathcal F_K \to X$ natural under transfers ($O_J \circ T_{J \leftarrow K} = O_K$) is uniquely determined by its value on reference grade 0: $O_K = O_0 \circ T_{0 \leftarrow K}$. Extends to all $r$-ary operations.

4. **Simultaneous Dirichlet Compatibility and Zero-Divisor Invariance**:
   Imposing all pairwise equations $D_J^{\mathrm{amb}}(s) = \tau^{-(J-K)s} D_K^{\mathrm{amb}}(s)$ simultaneously across all $K, J \in \mathbb A_{\mathbb R}$ is an identity of coboundaries. It introduces zero additional equations on $\zeta(s)$ and preserves the zero divisor identically: $\operatorname{Div}_0(D_K^{\mathrm{amb}}) = \operatorname{Div}_0(D_0)$.

5. **Ambient Realization Kernel Independence**:
   Trivial transfer holonomy does not resolve the ambient evaluation kernel $\ker(\operatorname{ev}_\tau) = \{\sum a_j [K_j] \in \mathbb A_{\mathbb R}[\mathbb A_{\mathbb R}] : \sum a_j \tau^{K_j} = 0\}$. Exhaustive audit of standard zeta identities yields `NO_ZETA_TO_REALIZATION_KERNEL_BRIDGE_FOUND`.

6. **Governing Classification**:
   Principal Classification: `MULTIGRADE_NATURALITY_NO_GO_PROVED`.
   Current TC axioms contain no demonstrated RH constraint beyond transport and unit covariance. The pure unit-rescaling, character unitarity, local germ, converter covariance, and multi-grade transfer compatibility routes are officially frozen.

---

# 24. Ambient Realization Kernel, Algebraic-Power Independence, and Zeta-Bridge Firewall (TASK-TC-028 / TASK-TC-028R)

1. **Ambient Evaluation Map & Translation Invariance**:
   For $\tau = 2\pi$, the evaluation map $\operatorname{ev}_\tau: \mathbb A_{\mathbb R}[\mathbb A_{\mathbb R}] \to \mathbb R$ (or $\overline{\mathbb Q}[\mathbb A_{\mathbb R}] \to \mathbb C$) acts by $\operatorname{ev}_\tau(\sum a_j [K_j]) = \sum a_j \tau^{K_j}$.
   Support translation invariance holds: $\sum a_j \tau^{K_j} = 0 \iff \sum a_j \tau^{K_j - K_0} = 0$ for any $K_0$. Kernel relations depend strictly on affine differences.

2. **Rational Support Rank $r(S)$ & Rank-Zero Triviality**:
   $r(S) = \dim_{\mathbb Q} \operatorname{span}_{\mathbb Q} \{K_j - K_0\}$ is base-grade invariant, computed via exact number-field primitive element embeddings.
   For $r(S) = 0$ (all grades coincide), $\sum a_j \tau^{K_0} = 0 \iff \sum a_j = 0$ (`RANK_ZERO_TRIVIAL_COEFFICIENT_CANCELLATION`).

3. **Exact Rank-One Classification ($r=1$)**:
   For grade differences along a rational line $\mathbb Q\alpha$ ($\alpha \in \mathbb A_{\mathbb R} \setminus \{0\}$), $\operatorname{ev}_\tau$ is injective on $\overline{\mathbb Q}[\mathbb Q\alpha]$ if and only if $\alpha \notin S_\tau = \{\alpha \in \mathbb A_{\mathbb R} : \tau^\alpha \in \overline{\mathbb Q}\}$.
   If $\alpha \in S_\tau$, an explicit kernel witness is $[\alpha] - A[0]$ with $A = \tau^\alpha \in \overline{\mathbb Q}$ (`RANK_ONE_KERNEL_CLASSIFIED`). By external Gelfond–Schneider, $\dim_{\mathbb Q} S_\tau \le 1$ (`ONE_EXCEPTIONAL_Q_DIRECTION_ONLY`).
   Base grade $1 \in \mathbb{A}_{\mathbb{R}}$ is algebraic; what is transcendental is $\tau^1 = 2\pi$, equivalently $1 \notin S_\tau$.

4. **Higher-Rank Reduction Theorem ($r \ge 2$)**:
   Finite support kernel relations of rational rank $r \ge 2$ reduce precisely to multivariate algebraic-dependence relations among $r$ algebraic powers of $2\pi$:
   \[
   \boxed{\operatorname{ev}_\tau \text{ injective on } \overline{\mathbb Q}[\mathbb Q\alpha_1 \oplus \cdots \oplus \mathbb Q\alpha_r] \iff \{\tau^{\alpha_1}, \dots, \tau^{\alpha_r}\} \text{ are algebraically independent over } \overline{\mathbb Q}.}
   \]
   Principal classification: `FINITE_KERNEL_REDUCES_TO_ALGEBRAIC_INDEPENDENCE`.

5. **Strengthened Schanuel Theorem & Minimal Open Case**:
   A rigorous two-case derivation (Case A: $1, \alpha_1, \dots, \alpha_r$ $\mathbb{Q}$-independent; Case B: $1 \in \operatorname{span}_{\mathbb{Q}}\{\alpha_1, \dots, \alpha_r\}$) proves $\operatorname{trdeg}_{\overline{\mathbb Q}} \overline{\mathbb Q}(\tau^{\alpha_1}, \dots, \tau^{\alpha_r}) = r$.
   Consequently, **Schanuel's conjecture implies full finite-rank injectivity of $\operatorname{ev}_\tau$ on every finite algebraic-grade support** (`SCHANUEL_IMPLIES_FULL_FINITE_RANK_INJECTIVITY`).
   The minimal open case is identified as $P(\tau^{\sqrt{2}}, \tau^{\sqrt{3}}) = 0$ ($r=2$).
   Certified absence of relations is established via Arb ball arithmetic with native algebraic ball construction (`expr_to_arb`) and certified interval lower bounds (`abs_lower()`) for 15,624 quadratic polynomials (height $\le 2$, certified distance $> 0.201733$) (`CERTIFIED_FINITE_RELATION_EXCLUSION`).

6. **Zeta-Bridge Firewall Audit**:
   Auditing familiar standard zeta candidates reveals they fail the algebraic-coefficient firewall: $\gamma_n, \rho_n, \zeta(2n+1), \Gamma(\rho)$ are `ALGEBRAICITY_UNPROVED` (inadmissible as proved algebraic coefficients; irrational $\ne$ transcendental), while $\log p, \zeta(2n)$ are `PROVED_TRANSCENDENTAL`.
   The finding `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` is strictly an audit finding, not a universal impossibility theorem. Zero-arithmetic research is logically distinct from the TC ambient kernel.

7. **Verification Scope Delineation**:
   - `LEAN_PROVED: algebraic skeleton / low arity`: 2- and 3-term translation invariance, 2- and 3-term rank-zero cancellation, real affine difference identity, bivariate monomial clearing identity, and abstract 2-term impossibility (`RiemannScope.AmbientKernel`).
   - `PROVED_PAPER_DERIVATION: full rank-one and higher-rank classification`: Full group algebra $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ injectivity, equality of $\mathbb{Q}$-spans and dimensions under base change, general multivariate Laurent reduction, and two-case Schanuel conditional theorem.



