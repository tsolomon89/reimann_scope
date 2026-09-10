# Research Hypothesis

## 0. Purpose

This document states the current proof-facing research programme for `reimann_scope`.

The project is explicitly searching for a path to proof of the Riemann Hypothesis. It does so by introducing a project-defined framework, **transcendental continuation**, and asking whether the additional grade structure exposes a global incompatibility between:

- the established critical-line radial class; and
- any hypothetical off-critical radial class.

The application may use visualization and finite computation to discover or falsify candidate laws. Those observations are not promoted to proof until the law is derived mathematically and, where practical, formalized.

---

# 1. RH in radial coordinates

Write a nontrivial zero as

\[
\boxed{
\rho=\frac12+\delta+i\gamma.
}
\]

Then

\[
\delta=\Re(\rho)-\frac12.
\]

RH is equivalent to

\[
\boxed{
\delta=0
\quad
\text{for every nontrivial zero.}
}
\]

The upper-half-plane zero ordinates usually quoted as

\[
14.1347\ldots,\ 21.0220\ldots,\ldots
\]

are the \(\gamma\)-coordinates of zeros whose full coordinates are

\[
\frac12+i\gamma.
\]

The trivial zeros

\[
-2,-4,-6,\ldots
\]

belong to a separate structural sector and are not the target of RH.

---

# 2. Why the completed function is useful

Define

\[
\boxed{
\xi(s)
=
\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s).
}
\]

The zeros of \(\xi\) are precisely the nontrivial zeros of \(\zeta\).

The proof-facing radial-class argument can therefore use \(\xi\) without losing the full zeta architecture used elsewhere in the instrument.

---

# 3. Transcendental continuation of the proof object

Define

\[
\boxed{
\mathcal X_\tau(s,k)
=
\xi(\tau^{-k}s),
}
\]

with

\[
\tau=2\pi.
\]

At native grade,

\[
\boxed{
\mathcal X_\tau(s,0)=\xi(s).
}
\]

If

\[
\xi(\rho)=0,
\]

then the corresponding zero worldline is

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

The critical surface is

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

Define normalized radial coordinate

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

For

\[
\rho=\frac12+\delta+i\gamma,
\]

\[
\boxed{
R_\tau(s_\rho(k),k)=\delta
}
\]

for every grade \(k\).

Thus each zero worldline belongs to one exact radial leaf

\[
\mathcal R_\delta.
\]

---

# 4. The contradiction programme

The current intended proof structure is:

\[
\boxed{
\begin{aligned}
1.&\ \textbf{Assume RH is false.}\\
2.&\ \textbf{Construct the counterexample worldline.}\\
3.&\ \textbf{Expose its bilateral radial defect across }\tau\text{-grades.}\\
4.&\ \textbf{Derive a global transcendental-coherence law.}\\
5.&\ \textbf{Prove radial rigidity / no mixed-leaf occupancy.}\\
6.&\ \textbf{Use the established critical class to select }\mathcal R_0.\\
7.&\ \textbf{Contradict the assumed off-critical leaf.}
\end{aligned}
}
\]

The exact content of steps 4–5 is not known. That is the research problem.

---

# 5. Step 1 — assume a counterexample

Assume there exists a nontrivial zero

\[
\boxed{
\rho_*=
\frac12+\delta+i\gamma,
\qquad
\delta\neq0.
}
\]

Because many nontrivial zeros are rigorously established on the critical line, a false RH would then imply at least two occupied radial classes in the actual nontrivial spectrum:

\[
\boxed{
\mathcal R_0
\quad\text{and}\quad
\mathcal R_\delta,\ \delta\neq0.
}
\]

By functional-equation and conjugation symmetry, an off-line zero also requires the corresponding reflected/conjugate structure. The counterexample is therefore not treated as a single isolated complex point.

---

# 6. Step 2 — construct the complete counterexample worldline

Transcendental continuation maps the assumed zero to

\[
\boxed{
\rho_{*,k}
=
\tau^k\rho_*.
}
\]

At integer grades,

\[
\boxed{
\rho_{*,K}
=
\tau^K\rho_*,
\qquad
K\in\mathbb Z.
}
\]

The worldline misses the critical surface at every grade because

\[
R_\tau(\rho_{*,k},k)=\delta\neq0.
\]

Compression and expansion alter absolute coordinates but do not change the normalized radial class.

Thus the assumed counterexample becomes an exact **transcendental radial defect worldline**.

---

# 7. Step 3 — bilateral grade signature

Define the zero character

\[
\boxed{
q_\rho
=
\tau^{\rho-\frac12}.
}
\]

For

\[
\rho=\frac12+\delta+i\gamma,
\]

\[
q_\rho^K
=
\tau^{K\delta}
e^{iK\gamma\log\tau}
\]

and therefore

\[
\boxed{
|q_\rho^K|
=
\tau^{K\delta}.
}
\]

For the critical class,

\[
\delta=0
\]

gives

\[
\boxed{
|q_\rho^K|=1
\quad
\forall K\in\mathbb Z.
}
\]

For an off-critical class,

\[
\delta\neq0,
\]

the modulus grows exponentially in one grade direction and contracts in the other.

The reflected partner supplies the complementary radial behavior.

Therefore a false RH introduces a bilateral family of nonunit radial modes into the same globally constrained spectrum.

This is exact algebra, not yet a contradiction.

---

# 8. Step 4 — derive Transcendental Coherence

The central missing theorem must come from the actual analytic/arithmetic structure of zeta or xi.

Call the desired law provisionally:

\[
\boxed{
\mathcal T[\Xi]=0
}
\]

or

\[
\boxed{
I_K=C.
}
\]

The exact notation is deliberately unspecified until the law is discovered.

A valid Transcendental Coherence Law must satisfy all of the following:

1. **Global**
   It must depend on the actual globally constrained zeta/xi object, not be defined independently zero-by-zero.

2. **Grade-wide**
   It must hold across a nontrivial family of \(K\)-states or arise from simultaneous constraints across them.

3. **Independent of RH**
   Its derivation must not assume
   \[
   \Re(\rho)=\frac12
   \]
   or any equivalent RH-strength bound.

4. **Stronger than coordinate covariance**
   It cannot merely restate
   \[
   \mathcal X_\tau(\tau^k s,k)=\xi(s).
   \]

5. **Arithmetic/analytic**
   It should be tied to the zeta/xi object, explicit formula, prime structure, functional equation, or another exact defining relation.

6. **Falsifiable**
   The Scope must be able to test candidate forms numerically across distinct actual regions and grades.

---

# 9. Step 5 — Transcendental Radial Rigidity

The desired consequence is a theorem of the form:

\[
\boxed{
\mathcal T
\Longrightarrow
\text{the actual nontrivial spectrum occupies only one radial leaf}.
}
\]

Equivalent possible forms include:

\[
\boxed{
\mathcal T
\Longrightarrow
R_\tau(W_{\rho_m})=R_\tau(W_{\rho_n})
\quad
\text{for all nontrivial zeros }\rho_m,\rho_n,
}
\]

or

\[
\boxed{
\mathcal T
+
\text{full bilateral grade constraints}
\Longrightarrow
\delta=0.
}
\]

The theorem may ultimately be phrased as a uniqueness, rigidity, no-compensation, or constraint-intersection statement.

This theorem is currently **OPEN**.

---

# 10. Constraint-intersection formulation

The train-line intuition is not used as a literal “no space remains” claim.

Instead, assign to each grade \(K\) the complete exact constraint set

\[
\mathcal C_K.
\]

The actual zeta/xi spectrum must satisfy all of them:

\[
\boxed{
\text{Spectrum}
\in
\bigcap_{K\in\mathbb Z}
\mathcal C_K.
}
\]

The proof question becomes:

\[
\boxed{
\text{Can the intersection of all grade constraints contain a spectrum}
\text{ occupying both }\mathcal R_0
\text{ and }\mathcal R_\delta,\ \delta\neq0?
}
\]

If the answer can be proved to be no, then the intersection of constraints enforces radial rigidity.

This is the mathematically preferred version of the original train-line intersection intuition.

---

# 11. No-compensation requirement

A simple growth argument is insufficient.

An off-critical reflected pair supplies complementary factors

\[
\tau^{K\delta}
\]

and

\[
\tau^{-K\delta}.
\]

Global sums may contain cancellation or compensation.

Therefore the missing theorem must show more than:

\[
\text{one component grows}.
\]

It must establish something like:

\[
\boxed{
\text{the exact grade-wide arithmetic/analytic object cannot compensate}
\text{ mixed radial exponents for all required grades}.
}
\]

This is the candidate **Transcendental No-Compensation** form of radial rigidity.

---

# 12. Existing exact spectrum-wide grade relation

The explicit formula already yields a genuine global grade relation.

For \(K>0\),

\[
\boxed{
\sum_\rho
\frac{q_\rho^K}{\rho}
=
\tau^{-K/2}
\left[
\tau^K
-\psi(\tau^K)
-\log\tau
-\frac12\log(1-\tau^{-2K})
\right].
}
\]

This is important because it proves that the grade characters participate in an exact spectrum-wide arithmetic identity.

But it does **not** by itself establish radial rigidity.

Attempting to impose an RH-strength bound on the right-hand side as the missing theorem risks circularity.

The task is to find a more structural uniqueness or compatibility condition.

---

# 13. Why the integer grades are privileged but not exclusive

The canonical grade family is

\[
K\in\mathbb Z.
\]

It is bilateral, multiplicatively generated by one full-turn scale, and gives pairwise noncoincident arithmetic lattices

\[
L_K=\tau^K\mathbb Z.
\]

Rational grades

\[
q\in\mathbb Q
\]

supply exact root refinements and preserve the same arithmetic noncoincidence property for distinct rational grades.

Real grades provide the full continuous interpolation.

The proof programme should begin with the integer skeleton because it is discrete, exact, bilateral, and computationally manageable.

It may use rational or real grades when a candidate theorem requires them.

---

# 14. Why high zeros still matter

A hypothetical RH counterexample may occur at an enormous finite ordinate.

The project must therefore test any proposed coherence law across widely separated actual heights.

The reason is not:

> more verified zeros make RH numerically more likely.

The reason is:

> a claimed height-independent law must survive actual high-height zeta geometry.

Negative grades allow high finite structures to be compressed into tractable coordinate ranges, but compression alone does not remove normalized radial defect.

---

# 15. Cross-height path normalization

For a verified simple critical-line zero

\[
\rho_n
=
\frac12+i\gamma_n,
\]

one baseline local scale is

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
s_n(u)
=
\frac12+i(\gamma_n+\Delta_n u)
\]

and

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

Then

\[
P_n(0)=0,
\qquad
P_n'(0)=1.
\]

This removes trivial local translation, chosen local scale, first-order magnitude, and first-order orientation.

It is an experimental instrument for discovering candidate coherence laws across genuinely different actual zeta regions.

It is not the definition of transcendental continuation itself.

---

# 16. What would count as a proof lead

A candidate law becomes proof-facing only if it passes all stages:

### Observed

A simple pattern survives the declared numerical controls.

### Normalized

The pattern is not explained by trivial coordinate covariance, arbitrary plotting scale, or precision artifacts.

### Derived

The pattern is proved as an exact identity of the zeta/xi system.

### Radially rigid

The exact identity excludes simultaneous occupancy of multiple radial leaves.

### Formalized

The logical implication is checked in Lean or another proof framework where practical.

The desired chain is:

\[
\boxed{
\text{transcendental coherence}
\Rightarrow
\text{radial rigidity}
\Rightarrow
\delta=0
\Rightarrow
\text{RH}.
}
\]

---

# 17. Falsification criteria

The programme must be weakened or killed if:

- every apparent transcendental-continuation invariant reduces to trivial coordinate covariance;
- integer-grade effects are reproduced identically by generic scale bases with no tau-specific structure;
- high-height actual paths show no stable global coherence beyond known local/statistical behavior;
- a proposed radial-rigidity theorem smuggles in RH or an equivalent bound;
- off-critical comparison functions satisfy the same proposed coherence law;
- mixed radial exponents can satisfy the exact grade constraints without contradiction;
- the constraint-intersection formulation leaves multiple radial leaves admissible.

A clean falsification is a successful research outcome.

---

# 18. Current missing statement

The current proof programme is concentrated in one unresolved implication:

\[
\boxed{
\text{Transcendental Coherence}
\Longrightarrow
\text{Transcendental Radial Rigidity}.
}
\]

Everything in the application should either:

- establish exact prerequisite structure;
- search for the coherence law;
- test candidate radial rigidity;
- or falsify an attempted formulation.

The project should not broaden into unrelated RH machinery unless the current programme produces a specific mathematical reason to do so.

---

# 19. Explicit Formula Discrimination Framework

The project has established the direct mathematical-discrimination campaign for the proposed role of transcendental continuation in explicit-formula constraints:

1. **Grade Covariance**: The grade-\(K\) representation correctly transports the explicit formula according to exact Fourier scaling \(\widehat h_{K,j}(x) = a_K^{-1} \widehat H_j(a_K^{-1} x)\).
2. **Defect Exposure**: Changing the zero divisor while holding arithmetic data \(\mathcal A_\zeta\) fixed produces a non-zero finite divisor defect \(\Delta \mathcal C_{K,j} = \langle\Delta\mathcal D, h_{K,j}\rangle\) that detects the perturbation on separating test functions while canceling all unchanged terms.
3. **Absence of Additional Grade Rigidity**: The combined \(K\)-family satisfies \(\mathcal C_{K,j}[H] \equiv \mathcal C_0[H(a_K \cdot)]\). The constraint space of the \(K\)-family is completely spanned by the expanded \(K=0\) native basis \(\{ H_j(a_K \cdot) : K \in \mathcal K, j \in \mathcal J \}\).
   - Exact theoretical classification:
     \[
     \boxed{\text{coordinate\_redundant}}
     \]
   - Finite basis enrichment relative to an unexpanded native basis:
     \[
     \boxed{\text{finite\_basis\_enrichment\_only}}
     \]

**Crucial Epistemic Distinction**:
- Detecting a local divisor perturbation with fixed arithmetic data demonstrates sensitivity of the explicit formula to isolated spectral modifications, but does not model an alternative zeta function or a zero belonging to an actual complete divisor (where the complete zero spectrum and the arithmetic data satisfy the explicit formula collectively).
- The explicit formula family \(\mathcal C_{K,j}\) operates purely via coordinate pullback \(\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K]\); any candidate for a genuine non-dilation joint arithmetic constraint remains an **OPEN / UNDEFINED CANDIDATE**.
- The missing theorem remains:
  \[
  \text{zeta-specific global constraint} \Longrightarrow \text{radial rigidity}.
  \]
  This implication is not assumed or axiomatized.

---

# 20. Second-Order Radial Sensitivity and Quadratic Energy Formulation

The research campaign evaluates the second-order radial response of the Riemann–Weil explicit formula under the radial projection operator \(\mathcal P_0\):

1. **Defect Divisor**:
   \[
   \Delta\mathcal D_{\mathrm{rad}} = \mathcal D - \mathcal P_0(\mathcal D).
   \]
2. **Second-Order Taylor Response**:
   For any even holomorphic test function \(h\) and orbit \(\mathcal O(\rho) = \{1/2 \pm \delta \pm i\gamma\}\), with \(u = \delta^2 \ge 0\):
   \[
   \Delta\mathcal C_h[\mathcal O(\rho)] = -2 u h''(\gamma) + \mathcal O(u^2).
   \]
3. **Single-Target Quadratic Energy vs Subspace Cone Compensation**:
   - Single-target energy \(E(u_n) = u_n^2 \|K_{\cdot, n}\|^2 \ge 0\) is strictly positive for any non-trivial test function where \(h''(\gamma_n) \ne 0\).
   - However, single-target positivity does **NOT** forbid compensation by other zero columns in a finite subspace:
     \[
     \min_{u_{-n} \ge 0} \|K_{\cdot, n} u_n - K_{-n} u_{-n}\|^2.
     \]
   - In the sampled 30-channel basis over 100 zeros, numerical nullity is high (\(\approx 85\)) and conditioning is \(\sim 10^{15}\); non-negative least squares yields heterogeneous diagnostic results (compensation was found at the \(10^{-5}\) threshold for zeros 10 and 50 with relative residuals \(\sim 10^{-10}\) and \(\sim 10^{-7}\); compensation was not found at this threshold for peripheral zeros 1 and 100).
4. **The Scoped Projection Trap (OBL-EF-003)**:
   - The actual zero divisor \(\mathcal D_\zeta\) has an arithmetic explicit-formula representation, while its critical-line projection \(\mathcal P_0(\mathcal D_\zeta)\) has no known independent arithmetic representation.
   - For any even holomorphic test function \(G\), the Cauchy-Riemann equations prove that \(\delta\)-independence of the quartet response \(2\Re G(\delta+i\gamma)\) forces \(G\) to be constant.
   - **Classification**: **CLOSED** for fixed linear combinations and locally uniform limits of direct 1-point holomorphic Riemann–Weil evaluations; **OPEN** for nonlinear paired, determinantal, operator, or independently constructed comparison objects (`OBL-RDQ-001`).
5. **Structural Countermodels**:
   - Davenport–Heilbronn and Epstein zeta functions demonstrate that functional-equation reflection symmetry and coordinate covariance alone do not exclude off-line zeros.
6. **Epistemic Classification**:
   - The construction is classified as an **exact finite synthetic sensitivity diagnostic**.

---

# 21. Radial-Defect Quotient, Relative Fredholm Formulation, and the Live Research Kernel

The project focuses its live research kernel on the canonical Radial-Defect Quotient and its relative Fredholm formulation:

1. **The Radial-Defect Quotient \(Q(z)\)**:
   In centered coordinates \(z = s - 1/2 = \delta + it\), let \(\Xi(z) = \xi(1/2 + z)\).
   Product premises:
   - Exclusion of real nontrivial zeros (\(\zeta(s) \ne 0\) on \((0,1) \implies \gamma = \Im \lambda \ne 0\)).
   - Paired Hadamard factorization: \(\Xi(z) = \Xi(0) \prod_{\lambda\in\Lambda^+} (1 - z^2/\lambda^2)^{m_\lambda}\).
   - General multiplicity formula: \(m_\gamma = m_{0,\gamma} + 2\sum_j n_{j,\gamma}\).
   - Baseline reference function: \(\Xi^\flat(z) = \prod_{\gamma > 0} (1 + z^2/\gamma^2)^{m_\gamma}\).
   Define:
   \[
   \boxed{
   Q(z) = \frac{\Xi(z)}{\Xi(0) \Xi^\flat(z)} = \prod_j \left( Q_{\delta_j, \gamma_j}(z) \right)^{n_j}.
   }
   \]
   On the real centered axis \(z = x \in \mathbb R\), each off-line quartet contributes a factor \(0 < q_{\delta,\gamma}(x) \le 1\) with exact defect factorization:
   \[
   1 - q_{\delta,\gamma}(x) = \frac{\delta^2 x^2 \left[(\delta^2 + 2\gamma^2)x^2 + 2\gamma^2(\delta^2 + 3\gamma^2)\right]}{(\delta^2+\gamma^2)^2 (x^2+\gamma^2)^2} \ge 0.
   \]
   Unique minimum in \(u = x^2 \ge 0\) at \(u_* = \delta^2 + 3\gamma^2\), corresponding to two real minimizers \(x = \pm\sqrt{\delta^2 + 3\gamma^2}\), with minimum value \(q_{\min} = \frac{4}{(1+r)^2(4+r)}\) (\(r = \delta^2/\gamma^2\)).

2. **The Limiting Invariant \(L_Q\)**:
   \[
   \boxed{
   L_Q = \lim_{x\to\infty} Q(x) = \prod_{j} \left(\frac{\gamma_j^2}{\gamma_j^2+\delta_j^2}\right)^{2n_j} = \prod_j (1 + r_j)^{-2n_j}.
   }
   \]
   Spectral equivalence: \(0 < L_Q \le 1\), and \(L_Q = 1 \iff \mathrm{RH}\).

3. **Relative Fredholm Spectral Formulation**:
   Define the positive diagonal trace-class operator \(\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda\) on \(\ell^2(\Lambda^+)\).
   Then:
   \[
   \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} < \infty,
   \qquad
   \det_{\mathrm F}(I + \mathcal R) = L_Q^{-1},
   \qquad
   -\log L_Q = \operatorname{Tr}\log(I + \mathcal R).
   \]
   Positivity \(\mathcal R \ge 0\) yields \(\operatorname{Tr}\mathcal R = 0 \iff \mathcal R = 0 \iff \mathrm{RH}\).

4. **Reflection-Paired Involution Kernel \(\kappa_1\)**:
   For \(z = \delta + i\gamma\) and \(z^\# = -\bar z = -\delta + i\gamma\), with \((z+z^\#)^2 = -4\gamma^2\) and \(zz^\# = -(\delta^2+\gamma^2)\), the rational pairing kernel:
   \[
   \kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1
   \]
   satisfies:
   \[
   \boxed{
   \kappa_1(\lambda, \lambda^\#) = \frac{\delta^2}{\gamma^2},
   \qquad
   \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \kappa_1(\lambda, \lambda^\#).
   }
   \]

5. **Grade-Indexed Covariance**:
   Under coordinate dilation \(s_K = \tau^K s \implies z_K = \tau^K z\):
   \[
   \boxed{
   Q_K(z_K) = Q_0(\tau^{-K} z_K),
   \qquad
   Q_K(\tau^K z) = Q_0(z),
   }
   \]
   while \(L_Q\), \(\{r_\lambda\}\), and \(\operatorname{Tr}\mathcal R\) are strictly grade-invariant.

6. **The Minimal Live Open Theorem (OBL-RDQ-001)**:
   \[
   \boxed{
   \text{Can a divisor-independent arithmetic construction isolate the } (\lambda, \lambda^\#) \text{ pairs and evaluate } \kappa_1?
   }
   \]
   - Functional equation and Schwarz reflection supply zero-set closure under \(\lambda \mapsto \lambda^\#\).
   - Isolating the pairs without direct access to the zero divisor is the exact unresolved barrier.
   - Ordinary grade dilation does not supply the rigidity law; the rigidity source must contain additional zeta-specific arithmetic content.

---

# 22. Arithmetic Radial Bridge Construction, Pair Isolation, and Falsification Boundaries

## 22.1 Target distinctions
1. **Determinant Target**: \(D := -\log L_Q = \log\det_{\mathrm F}(I+\mathcal R) = \sum 2n_j \log(1+r_j)\), candidate \(\mathfrak A_{K,D}^{\mathrm{arith}} = D\).
2. **Trace Target**: \(T := \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} = \sum 2n_j r_j\), candidate \(\mathfrak A_{K,T}^{\mathrm{arith}} = T\).
3. **Regularized Weighted Target**: \(T_a = \sum_{\lambda\in\Lambda^+} w_a(\lambda) \frac{\delta_\lambda^2}{\gamma_\lambda^2}\) with \(w_a(\lambda) > 0\).

## 22.2 Strict arithmetic input firewall
All candidate arithmetic evaluators \(\mathfrak A_{K,X}^{\mathrm{arith}}\) must be constructed purely from primes, \(\Lambda(n)\), Euler products (\(\Re(s)>1\)), the pole at \(s=1\), gamma factors, functional equation symmetries, and transcendental continuation \(\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)\). Arithmetic evaluators must reject zero lists, projected ordinates, \(\Xi^\flat\), \(Q, L_Q, \mathcal R, D\), and \(T\).

## 22.3 Grade centering geometry
Under origin dilation \(s_K = \tau^K s\), the critical line \(\Re(s)=1/2\) maps to \(\Re(s_K) = \tau^K/2 = c_K\). The centered coordinate is \(z_K = s_K - c_K = \tau^K z\), and the centered completed xi function satisfies \(\Xi_K(\tau^K z) = \Xi_0(z)\). Normalized radial ratios \((\tau^K\delta)^2/(\tau^K\gamma)^2 = \delta^2/\gamma^2\) are strictly grade-invariant.

## 22.4 Covariance countermodel (Covariance \(\ne\) Rigidity)
The abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under functional equation reflection, complex conjugation, and bilateral grade transport. This rigorously proves that reflection symmetries and coordinate covariance are jointly compatible with off-line zeros. Transport covariance alone cannot force \(\delta = 0\); an independent arithmetic zero-valued anchor \(\mathfrak A_K = 0\) is mandatory.

## 22.5 Candidate evaluation and falsification summary
- **Candidate A (Linear Grade Differences)**: `FALSIFIED_FOR_BRIDGE` (collapses to native explicit formula \(\mathcal C_0[H\circ\tau^K]-\mathcal C_0[H]\); 1-point direct sums fail pair isolation).
- **Candidate B (Bilinear Cross-Grade Explicit Formula)**: `FALSIFIED_FOR_PAIR_ISOLATION` (\(D_K(s)\overline{D_L(s)}\) yields unrestricted double sum over all zero pairs; off-diagonal terms contaminate).
- **Candidate C (Tensor-Square Trace Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (unrestricted double sum).
- **Candidate D (Log-Derivative Contour Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (residue cross-terms across critical strip).
- **Candidate E (Relative Determinant from Arithmetic Space)**: `OPEN_UNPROVED` (no zero-independent operator).
- **Candidate F (Grade-Indexed Prime-Power Pairing)**: `OPEN_UNPROVED` (pairing law unproved).
- **Candidate G (Weighted Regularized Bridge)**: `LIVE_UNDERIVED` (spectral detector \(T_a>0\) proved; arithmetic realization open).

---

# 23. Complete Finite Spectral Expansion, Arbitrary Curvature Formalization, and Gate G4 Obstruction

## 23.1 Complete Finite Spectral Expansion & Analytic Kernels
The finite spectral mean-square approximant decomposes into four exact terms:
\[
S_{N, T}(\sigma) := \frac{1}{2T}\int_{-T}^T \left| A(\sigma+it) - \sum_{k=1}^N m_k \frac{2z}{z^2-\lambda_k^2} \right|^2 dt = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},
\]
with exact closed-form kernels:
\[
J_T(p, q) = \frac{\log\left(\frac{p+iT}{p-iT}\right) + \log\left(\frac{q+iT}{q-iT}\right)}{2Ti(p+q)},
\]
\[
K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu).
\]
This finite identity closes to machine precision (\(< 10^{-18}\)) in arbitrary precision.

## 23.2 Exact Real-Axis Spectral Defect Formula
For an off-line quartet \(\{\pm\delta \pm i\gamma\}\) vs on-line pair \(\{0, \pm i\gamma\}\) at \(z = \sigma - 1/2 > 0\):
\[
\Delta(\delta) = \frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2 + \gamma^2)[(z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2]}.
\]
For all critical strip zeros (\(\gamma > 14\)) with \(z = O(1)\), \(z^2 < 3\gamma^2 + \delta^2\), forcing \(\Delta(\delta) < 0\). The unregularized real-axis spectral difference is negative, proving that the unregularized mean-square does not produce a positive quadratic radial defect directly.

## 23.3 Arbitrary Finite Curvature Lean 4 Proofs
Formally verified in Lean 4 (`formal/RiemannScope/ArithmeticBridge.lean`, 0 `sorry`, 0 `admit`):
- `list_pairs_sq_sum_eq`: \(\sum_{i,j} (d_i + d_j)^2 = 2N\sum d_i^2 + 2(\sum d_i)^2\) for arbitrary real lists.
- `list_pairs_sq_sum_symmetric`: reduces to \(2N\sum d_i^2\) when \(\sum d_i = 0\).
- `list_pairs_sq_sum_nonneg` & `list_pairs_sq_sum_eq_zero_iff`: unconditionally non-negative, vanishing iff \(\forall x \in l, x = 0\).
- `generic_scale_dilation_cancellation`: \(s D_s(su) = f(u)\) for any scale \(s > 0\).

## 23.4 Earliest Infinite Analytic Obstruction (Gate G4)
Individual zero resolvent terms belong to \(L^2(\mathbb R, dt)\) with finite norm \(\frac{\pi}{\sigma-\Re\rho}\), so \(\frac{1}{2T}\int_{-T}^T \frac{dt}{|\sigma-\rho+it|^2} \to 0\) as \(T\to\infty\). The non-zero Besicovitch mean on the arithmetic side is carried by collective non-uniform infinite cancellation. Gate G4 (Infinite Spectral Interchange) is the exact earliest open barrier. Raw finite Fejér response and additive scalar class are classified as `FAIL_RADIAL_POSITIVITY`, full infinite Candidate CMSA-1 and CMSA-2 as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`, and finite algebraic expansion as `FINITE_IDENTITY_PROVED_G4_OPEN`.

---

# 24. Gate G4 Infinite-Regularization and Radial-Sign Theorem Resolution

## 24.1 Four Window Families (Loops 0–3)
Evaluated across:
1. **Rectangular**: \(W_T(t) = \frac{1}{2T}\mathbf 1_{[-T, T]}(t)\).
2. **Fejér**: \(W_T(t) = \frac{1}{T}(1 - |t|/T)\mathbf 1_{[-T, T]}(t)\), with exact analytic kernel \(J_T^{\text{Fejér}}(p,q) = \frac{I_T(p)+I_T(q)}{T(p+q)}\).
3. **Abel-Poisson**: \(W_\beta(t) = \frac{\beta}{2}e^{-\beta|t|}\).
4. **Gaussian**: \(W_T(t) = \frac{1}{\sqrt{2\pi}T}e^{-t^2/(2T^2)}\).
All four window families achieve exact finite quadratic expansion closure and are classified as `FINITE_IDENTITY_PROVED_G4_OPEN`.

## 24.2 Cofinal Limit Independence & Boundary Layer
Proved in Lean 4 with Mathlib `Filter.Tendsto` (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`): fixed-truncation limits \(\forall H, \lim_{n\to\infty} f(H, n) = 0\) do not imply cofinal limit vanishing \(\lim_{n\to\infty} f(H(n), n) = 0\).

## 24.3 Exact Radial Response Coefficient & Certified Arb Ball Witness
The symmetric second-order coefficient:
\[
C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt, \qquad D_\gamma(z) = \frac{4z(z^2 - 3\gamma^2)}{(z^2+\gamma^2)^3},
\]
governs the leading variation \(\Delta S_W = \delta^2 C_W + O(\delta^4)\) conditionally under uniform domination hypotheses.
- **Fejér Witness WIT-02**: Rigorously certified negative via outward-rounded Arb ball arithmetic across the full symmetric support \([-16.8, 16.8]\) with 50,000 subintervals (`certify_g4_fejer_witness_arb`):
  \[
  \Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0).
  \]
  Status: `CERTIFIED_NEGATIVE_ARB_BALL`.
- **Witnesses WIT 1, 3, 4**: Evaluated with negative numerical estimates and mpmath estimated error bounds (`NUMERICAL_EVIDENCE_NEGATIVE`).
- **Classification Matrix**:
  - Raw Finite Fejér Window Response: `FAIL_RADIAL_POSITIVITY`.
  - Divisor-Independent Additive Class on Finite Fejér: `FAIL_RADIAL_POSITIVITY`.
  - Candidate CMSA-1 & CMSA-2 (Full Infinite/Cofinal): `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
  - Complete Finite Algebraic Spectral Expansion: `FINITE_IDENTITY_PROVED_G4_OPEN`.
  - Dilated Completed Log-Derivative: `GRADE_COORDINATE_REDUNDANT`.

## 24.4 Additive-Reference Invariance No-Go Theorem
For any scalar reference \(R_W(A)\) independent of \(Z, \delta, \gamma\), \((S_W(Z_\delta) - R_W(A)) - (S_W(Z_0) - R_W(A)) \equiv S_W(Z_\delta) - S_W(Z_0)\).
Thus, divisor-independent additive scalar subtraction cannot alter the raw radial difference. Formally verified in Lean 4 (`RiemannScope.additive_reference_subtraction_invariance`).

## 24.5 Earliest Open Subgate
$$\boxed{\text{Subgate G4-Open: Prove a negative raw response analytically or with validated outward-rounded interval arithmetic on the general infinite/regularized limit.}}$$

## 24.6 Schedule Covariance, Background Dependence, and Fixed-Finite Invisibility
### Schedule Covariance Classification
Under origin coordinate dilation \(s_K = \tau^K s\) (\(z_K = \tau^K(s-1/2)\)), ordinate scales as \(t_K = \tau^K t \implies t' = \tau t\). Covariance of height truncation \(H\) requires:
\[
\boxed{H(\tau T) = \tau H(T), \quad \tau = 2\pi.}
\]
- **General Solution (Paper Proved)**: \(H(T) = T \cdot q(\log_\tau T)\) with \(q : \mathbb R \to (0, \infty)\) 1-periodic.
- **Asymptotic Limit Collapse (Paper Proved)**: If \(\lim_{T\to\infty} H(T)/T\) exists and \(\tau > 1\), \(H(T) = cT\).
- **Selection Condition**: Unproved heuristic note; remainder bounds do not force \(c \ge 1\) by proved estimate alone.
- **Falsified Premise**: *"Bilateral discrete grade covariance uniquely determines the cofinal schedule."*

### Background-Dependence Theorem & Scope of Additive Invariance
For complex-valued background \(F\) and perturbation \(\Delta\), the squared-norm variation is \(Q(F, \Delta) = |F + \Delta|^2 - |F|^2 = |\Delta|^2 + 2\Re(F\bar\Delta)\).
The theorem `additive_reference_subtraction_invariance` applies only to outer scalar subtractions \((S - R)\) and does NOT apply to backgrounds placed inside squared norms.
**Correction**: The claim that Case B automatically reduces to the certified finite Fejér response is withdrawn; the sign of \(Q(F_0, \Delta)\) depends explicitly on the completed-function background \(F_0\).

### Fixed Finite Perturbation Invisibility Theorem
**Proof Status**: `PROVED / EXACT / PARTIALLY_FORMALIZED`
- **Paper Proof**: Complete deductive analytic derivation.
- **Formalized Lean 4 Component**: `RiemannScope.fixed_finite_energy_scaling_zero` formalizes the scalar sequence limit \(E/(2T) \to 0\) (`FORMALLY_PROVED COMPONENT`).
- **Python Verification**: `math_core.verify_fixed_finite_perturbation_invisibility` evaluates numerical quadrature of finite prime Dirichlet polynomial truncations across sampled windows (`NUMERICAL_EVIDENCE`).

For any prime Dirichlet polynomial \(P_\sigma\) (\(\sigma > 1\)) and any fixed finite resolvent sum \(\Delta = \sum_{j=1}^N \frac{c_j}{a_j + i(t-\gamma_j)}\) (\(N < \infty, a_j > 0\)):
\[
\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( |P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2 \right) dt = 0.
\]
A fixed finite divisor perturbation cannot produce a nonzero normalized infinite mean response.

### Perturbation Semantics and Candidate Classifications
- **Case A (Recomputed Remainder)**: \(Z_{H,\delta} + R_{H,\delta} \equiv F_\delta\) (collapses algebraically). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case B (Fixed Finite Perturbation)**: \(Z_{H,\delta} + R_{H,0} = F_0 + \Delta\) (vanishes under infinite mean). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case C (Growing / Cofinal Perturbation \(\Delta_{H(T)}\))**: Non-fixed perturbation with \(H(T) \to \infty\). Classification: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
- **Raw Finite Fejér Response**: Retained as `FAIL_RADIAL_POSITIVITY`.

## 24.7 Resolvent Algebra, Subcritical Norm Growth, and the Transcendental Continuation Activation Subgate
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

## 24.8 Curvature-Transport Unification and Transcendental Curvature Rigidity

The repository's geometric, spectral, and arithmetic structures are unified under the **Curvature-Transport Framework**:
- Circle geometry ($C_K = \tau^{1-K}, r_K = \tau^{-K}, \kappa_K = \tau^K$) at integer checkpoints $K \in \mathbb Z$ satisfies $r_K\kappa_K = 1, C_1 = 1$, generating the angular Fourier lattice $L_K = \tau^K\mathbb Z$.
- Zero displacement $d_{\rho}(k) = \tau^k\delta$ at continuous grade $k \in \mathbb R$ under the transported radial unit $r(k) = \tau^{-k}$ recovers the invariant: $(r(k) d_{\rho}(k))^2 = \delta^2$.
- Half-density dilation $(U_a f)(x) = a^{1/2}f(ax)$ on $L^2(\mathbb R_{>0})$ acts as $a^{1/2-s}x^{-s}$, with the critical line $\Re(s)=1/2$ as its exact unitary-character axis $|a^{1/2-s}|=1$.
- The reflection-pair defect $B_\rho(k) = |\chi_\rho(k)| + |\chi_{\rho^\#}(k)| - 2 = 2(\cosh(k\delta\log\tau)-1) \ge 0$ yields native continuous second grade variation $B_\rho''(0) = 2\delta^2(\log\tau)^2$ and normalized invariant $\mathscr K_\tau(\rho) = \delta^2$.
- **Theta–Mellin Scaling & Scalar No-Go**: The half-density Mellin transform $\tau^{k/2}\int_0^\infty \Theta_{\tau^k}^+(t) t^{s/2-1} dt = \chi_s(k)^{-1}\Lambda(s)$ is an exact theorem on $\Re(s)>1$. The **Scalar-Transport No-Go Theorem** proves that for scalar multipliers $F_k = g_k L$, all grade derivatives at zeros vanish identically ($0 \equiv 0$), and logarithmic derivatives on $gL \ne 0$ supply zero divisor data.
- **Scoped One-Point Holomorphic Obstruction**: No fixed holomorphic local kernel $H(z)$ can equal $(\Re z)^2$ on an open set ($\partial_{\bar z}(\Re z)^2 = \Re z = \delta \ne 0$), requiring non-scalar pairings, contour boundary terms, or regularized determinants.
- **Canonical Weil–Hermitian Curvature Bridge & GNS Barrier**:
  - Exact pointwise identity: $\frac{1}{2}(1/|\rho|^2 + 1/|1-\rho|^2) - \Re(1/(\rho(1-\rho))) = \frac{2\delta^2}{|\rho|^2|1-\rho|^2} = \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0$.
  - Geometric involution discrepancy: $|J(\rho) - C(\rho)|^2 = 4\delta_\rho^2$ for $J(\rho)=1-\rho, C(\rho)=\bar\rho$.
  - Exact zeta divisor summation target: $N_\xi - C_\xi = \sum_{\rho\in Z} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} \ge 0$ ($C_\xi = 2 + \gamma_{\text{Euler}} - \log(4\pi)$), with $N_\xi = C_\xi \iff \mathrm{RH}$.
  - Test function audit: naive $g_0(x) = x^{-1/2}\mathbf 1_{[1, \tau]}(x)$ yields $\widehat g_0(s) \ne 1/s$ (`FAIL_TEST_FUNCTION_IDENTIFICATION`), requiring an admissible smoothing family $\Phi_\varepsilon \to 1/s$ (`OPEN_ADMISSIBLE_PROBE_REGULARIZATION`).
  - Unified additive coordinates $u = \log x \in \mathbb R$ yield Hermitian Weil form $Q_W(f) = \sum \Phi_f(\rho)\overline{\Phi_f(1-\bar\rho)}$. Pure local prime weights are strictly negative-definite (`FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION`), and assuming global Weil positivity $Q_W(f * f^*) \ge 0$ is equivalent to RH (Weil's 1952 criterion; `OPEN_GLOBAL_POSITIVE_TYPE_FACTORIZATION`).
- **Transcendental Curvature Rigidity Theorem**:
  $$\mathscr A_\tau(\xi) = 0 \quad \text{and} \quad \mathscr A_\tau(\xi) = \sum_{\rho\in\Lambda^+/\#} W_\rho \delta_\rho^2 \quad (W_\rho > 0) \implies \forall \rho, \; \delta_\rho = 0 \iff \mathrm{RH}.$$
- **Canonical Earliest Open Obligation (`OBL-CT-001A`)**: Constructing a zero-independent, non-scalar arithmetic functional $\mathscr A_\tau(\xi)$ (or $Q_H(f)$) is the program's canonical earliest open obligation. Curvature transport operates at the orbit level and bypasses detector-level $L^2$ translation invisibility, but does NOT solve CMSA Gate G4; whether a non-scalar arithmetic functional avoids or reproduces the pair barrier remains an open problem. Reference: `CURVATURE_TRANSPORT.md`.

---

## 24.9 Integrated-$\sigma$ Branch Closure & Bilateral Grade Second Variation

1. **Integrated-$\sigma$ Resolvent Algebra & Anchor Loss**:
   - Exact quartet resolvent difference $\Delta Z_+(z) = \frac{2\delta^2}{(z-i\gamma)((z-i\gamma)^2-\delta^2)}$ (Lean 4 `exact_quartet_resolvent_identity`, **ALGEBRAIC_IDENTITY**, and `exact_full_quartet_resolvent_sum`).
   - $\Delta Z_\sigma \in L^1(dt) \cap L^2(dt)$ with leading single-height norm $\frac{3\pi\delta^4}{2a^5}$.
   - Fourier transforms: $4\pi e^{-a\xi}(\cosh(\delta\xi)-1)e^{\pm i\gamma\xi}$ single-height, $8\pi e^{-a\xi}(\cosh(\delta\xi)-1)\cos(\gamma\xi)$ complete quartet.
   - Prime cross-term $-8\pi \sum \Lambda(n)\frac{n^{1/2-2\sigma_0}}{\log n}(\cosh(\delta\log n)-1)\cos(\gamma\log n)$; leading term $-4\pi\delta^2 \sum \Lambda(n)(\log n)n^{1/2-2\sigma_0}\cos(\gamma\log n)$; continuum sign change certified (`CONTINUUM_GAMMA_SIGN_CHANGE_PROVED`, `ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN`).
   - Unnormalized integration diverges for fixed $\sigma > 1$ ($\int_{\mathbb R} |P_\sigma(t)|^2 dt = \infty$), losing arithmetic anchor (`FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT`).
   - Integrated prime diagonal closed form: $\int_{\sigma_0}^\infty \sum \Lambda(n)^2 n^{-2\sigma} d\sigma = -\frac{1}{2}\sum_p \log p \log(1-p^{-2\sigma_0})$.
   - External attribution: Hadamard sum $\sum 1/|\rho|^2 = 2+\gamma-\log(4\pi)$ is classical literature (Edwards 1974, pp. 19–21; Davenport 1980, Ch. 12).
2. **Bilateral Grade Radial Centering Second-Variation Analysis**:
   - Exact opposition $\Delta_{-h} = -\Delta_h$ eliminates background cross-terms ($2|\Delta|^2 \ge 0$, Lean 4 `bilateral_squared_norm_centering_exact_opposite`).
   - Coordinate dilation $\Delta_{\pm h}(z) = \Delta Z(\tau^{\pm h}z)$ expands as $\Delta_h+\Delta_{-h} = 2h^2 B(z) + \mathcal O(h^4) \ne 0$, leaving $4h^2\Re(F\bar B)$ (Lean 4 `bilateral_second_order_asymmetry_cross_term`, **ALGEBRAIC_IDENTITY**, and `bilateral_asymmetry_cross_term_nonzero_of_re_nonzero`, **NO_GO_COMPONENT**). Formalized load-bearing arithmetic descent count remains 0.
   - Finite pullback $\mathcal C_{h,T} = \mathcal M_{0,\tau^h T} + \mathcal M_{0,\tau^{-h} T} - 2\mathcal M_{0,T}$ (`FINITE_GRADE_PULLBACK_IDENTITY`, Lean 4 `finite_grade_pullback_second_difference_identity`) vs asymptotic redundancy $\lim_{T\to\infty} \mathcal C_{h,T} = 0$ (`ASYMPTOTIC_GRADE_COORDINATE_REDUNDANCY`).
   - Actual Zeta-Specific Diagonal Cross-Term: $\mathfrak X_{\zeta,\mathrm{diag}} = \Re\langle F_0, F_0''\rangle = (\log\tau)^2 [(a^2-v)S_2(a) - aS_1(a)]$; universal non-vanishing withdrawn (`REPORTED_DIAGONAL_CROSS_TERM_UNIVERSAL_NONVANISHING_WITHDRAWN`); exact cancelling variances $v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)} > 0$ exist for all $a > 1/\log 2$ (`DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES`). Full finite-window Dirichlet inner product includes non-zero off-diagonal terms (`FULL_WINDOWED_ZETA_CROSS_TERM_DERIVED`).
   - Dilation centering is scale-generic ($a > 1$, `SCALE_GENERIC_NOT_TAU_SPECIFIC`).
3. **Consolidated Master Obligation**:
   Surviving radial-defect extraction routes are consolidated under $\mathbf{OBL\text{-}RADIAL\text{-}DEFECT\text{-}DESCENT}$ across 4 child routes: RDQ (`OBL-RDQ-001`), Curvature Transport (`OBL-CT-001`), Weil-Hermitian (`OBL-WH-001`), and CMSA (`OBL-CMSA-003`).

---

## 25. Transcendental Continuation Mechanism Discovery: Arithmetic Separation vs Off-Line Zeros

### 25.1 Reset of the Active TC Question
The active research question governing transcendental continuation mechanism discovery is reset to:
> **Which exact prime–zeta relationship, after complete TC transport, forces an off-line zero to violate arithmetic separation, and why does it not force that violation for an on-line zero?**

The target contradiction endpoint is:
\[
m \tau^K = n \tau^J \quad (m, n \in \mathbb Z \setminus \{0\}, \; K \ne J \in \mathbb Z) \iff \tau^{K-J} = \frac{n}{m} \in \mathbb Q \setminus \{0\},
\]
which is strictly forbidden by the transcendence of $\tau = 2\pi$ (Lindemann 1882).

### 25.2 Cycle 1 Candidate Evaluation Matrix

| Candidate ID | Exact Object & Claim | Arithmetic Premise & Role of $\rho$ | Intermediate Bridge & Intended Consequence | Earliest Unproved Inference & Dependencies | Discriminating Test & Result | Scoped Finding & Next Justified Action |
|---|---|---|---|---|---|---|
| **TC-DISC-01** (Gap A) | Station lattice $L_K = \tau^K\mathbb Z$ vs Dirichlet frequencies $\{\tau^{-K}\log n\}$. Claim: transported prime sum forces $L_K$ collision if $\delta \ne 0$. | Euler product $\sum \Lambda(n) n^{-s}$, with $\rho$ entering via explicit formula. | Projecting prime frequencies onto integer station scaffolds $a_K \mathbb Z$ forces $m \tau^K = n \tau^J$. | Inference: prime-power Dirac delta or exponential frequencies lie in discrete lattice $a_K \mathbb Z$. | Falsified: $-F_K'/F_K + F_J'/F_J \equiv (K-J)\log\tau$ identically on $\mathbb C$. Frequencies are continuous Fourier arguments. | **FALSIFIED / REDUCED TO SCALAR PULLBACK**. Lattices are disjoint, but frequency differences reduce to a scalar constant containing zero data from $\delta$ or primes. |
| **TC-DISC-02** (Gap B) | Grade character $q_\rho^K = \tau^{K(\rho-1/2)}$ and symmetric defect $D_K(\rho) = 4\sinh^2(K\delta\log\tau/2)$. Claim: arithmetic consistency forces $\delta \in \mathbb Q$ or $K\delta \in \mathbb Z$. | Hypothetical off-line zero $\rho = 1/2 + \delta + i\gamma$ ($\delta \ne 0$). | Off-line zero forces character modulus $\tau^{K\delta} \in \mathbb Q$, creating an arithmetic layer collision. | Inference: that integer grades $K \in \mathbb Z$ discretize or quantize the continuous zero displacement $\delta$. | Falsified: $|q_\rho^K| = \tau^{K\delta}$ and $D_K$ are smooth real-analytic for all $\delta \in \mathbb R$. Tested on $\delta \in \{0, 1/10, \sqrt{2}/10, \log_\tau(1.5)\}$. | **FALSIFIED / NO DISCRETE RESTRICTION ON $\delta$**. No algebraic or analytic law quantizes $\delta$. Irrational displacements yield valid non-quantized characters without contradiction. |
| **TC-DISC-03** (Gap C) | Completed logarithmic derivative difference $\Delta G_{K,J}(s) = -\xi_K'/\xi_K - (-\xi_J'/\xi_J)$. Claim: off-line divisor fails cross-grade compatibility. | Complete zero divisor $Z = \{\rho\}$ entering via Hadamard product $\xi(s) = \xi(0)\prod (1-s/\rho)$. | Zero sums $\sum_\rho (s-\rho)^{-1}$ in $\xi_K$ and $\xi_J$ fail to cancel unless $\delta_\rho = 0$. | Inference: that twisted logarithmic derivatives retain a differential signature of $\delta$ across grades. | Falsified: $\Delta G_{K,J}(s) \equiv (K-J)\log\tau$ identically. The zero-pole singular parts cancel identically for every zero set. | **REDUCED TO SCALAR IDENTITIES / OBSTRUCTION CONFIRMED**. Cross-grade completed log-derivative differences cancel the entire zero divisor unconditionally, providing no exclusion mechanism. |
| **TC-DISC-004** (Candidate D / Cycle 2 Sprint) | Transported explicit formula test function differences $h_{K,J}(r) = \phi(\tau^{-K}r) - \phi(\tau^{-J}r)$. Claim: off-line zero forces isolated two-prime frequency collision $\tau^K \log(\ell^q) = \tau^J \log(\ell^p)$ for prime base $\ell$ and positive integers $p, q$, requiring $\tau^{K-J} = p/q \in \mathbb{Q}$. | Explicit formula $\sum_\rho h(r_\rho) = \int h \Phi - \sum \frac{\Lambda(n)}{\sqrt{n}} g(\log n) + \dots$; hypothetical off-line zero $\rho = 1/2 + \delta + i\gamma$. | Test function differences isolate off-line zero response against prime-power Dirac comb, forcing an isolated balance $(\ell^q)^{\delta \tau^K} = (\ell^p)^{\delta \tau^J}$. | Scope of Negative Result: Equality of the two complete linear explicit-formula evaluations does not imply equality of any selected pair of prime-power summands. Pairwise collision requires an additional isolation or independence theorem. | Linearity proves $h_{K,J}$ is another native test (coordinate redundant). Multiplicative collision $\tau^{K-J} = p/q$ is strictly impossible by Lindemann's theorem, but whole-sum compensation does not force pair isolation. | **REJECTED AS A MECHANISM FROM EXPLICIT-FORMULA LINEARITY ALONE**. Linear explicit-formula evaluations collapse by linearity to native evaluations; arithmetic separation holds for isolated prime pairs but fails to exclude off-line zeros due to infinite-sum compensation. |

---

# 26. Transcendental Continuation: The Common-Referent Bridge (Cycle 3)

## 26.1 The Common-Referent Collision Contract

The simplest formulation of the transcendental continuation hypothesis posits an observable $A$ evaluated on nontrivial zeros $\rho = 1/2 + \delta + i\gamma$ satisfying three simultaneous conditions across distinct integer grades $K \ne J \in \mathbb{Z}$:

1. **(CR1) Common Referent**: $A_K(\rho_K) = A_J(\rho_J) = A(\rho)$ as an exact external mathematical value in a common ambient space ($\mathbb{R}$ or $\mathbb{C}$).
2. **(CR2) Arithmetic Location**: $A_K(\rho_K) \in L_K = \tau^K \mathbb{Z}$ and $A_J(\rho_J) \in L_J = \tau^J \mathbb{Z}$.
3. **(CR3) Off-Line Non-Zero**: $\delta \ne 0 \implies A(\rho) \ne 0$.

### The Common-Referent Collision Theorem
\[
\boxed{
(CR1) + (CR2) + (CR3) \quad \text{and} \quad L_K \cap L_J = \{0\} \; (K \ne J) \implies \delta = 0.
}
\]

*Proof*:
From (CR1) and (CR2), the common value $A(\rho)$ lies in $L_K \cap L_J$. Since $K \ne J$, $L_K \cap L_J = \{0\}$ by the transcendence of $\tau = 2\pi$ (Lindemann 1882; Lean 4 `lattice_intersection_transcendental_char`). Thus $A(\rho) = 0$. By the contrapositive of (CR3), $\delta = 0$. Formalized in Lean 4 as `RiemannScope.common_referent_collision_theorem`.

### Invariant/Covariant Observable Vanishing Form
Equivalently, if an observable $A(X)$ in the same codomain is simultaneously:
- Representation-invariant: $A(T_K X) = A(X)$, and
- Homogeneous of real non-zero grade weight $w \ne 0$: $A(T_K X) = \tau^{wK} A(X)$,
then $(1 - \tau^{wK}) A(X) = 0$. Since $\tau^{wK} \ne 1$ for $wK \ne 0$, $A(X) = 0$. Formalized in Lean 4 as `RiemannScope.invariant_covariant_observable_vanishing`.

---

## 26.2 Naturality Diagram: The Coordinate Conversion vs Raw Equality Boundary

Coordinate redundancy establishes that internal geometric relationships agree **after conversion of units**. It does **not** assert that raw coordinates across different representations are equal.

```text
               Intrinsic Zero Object: ρ = 1/2 + δ + iγ
                       /                    \
              T_K     /                      \     T_J
                     v                        v
Grade K Representative: s_ρ(K) = τ^K ρ       Grade J Representative: s_ρ(J) = τ^J ρ
                     |                        |
             A_K     |                        |     A_J
                     v                        v
Raw Observable:      τ^K δ                    τ^J δ
Codomain & Units:    Scale τ^K units          Scale τ^J units
                     |                        |
             C_K     | (× τ^-K)               | (× τ^-J)   C_J
                     v                        v
Converted Value:     δ           ===          δ  (Identical real number)
```

**The Central Distinction**:
- **Converted observables** satisfy (CR1): $C_K(A_K) = \delta = C_J(A_J)$.
- **Raw observables** fail (CR1): $\tau^K \delta \ne \tau^J \delta$ when $K \ne J$ and $\delta \ne 0$.
- **Layer membership** (CR2) applies to raw station coordinates $x \in L_K = \tau^K \mathbb{Z}$. Demanding that the *converted* (dimensionless) displacement $\delta$ belong to $L_K$ and $L_J$ forces $\delta \in \tau^K \mathbb{Z} \cap \tau^J \mathbb{Z} = \{0\}$, which assumes $\delta = 0$ at the outset.

---

---

## 26.3 The Observable Inventory Matrix (Ten Listed Existing Observables)

To systematically test the common-referent hypothesis, we audit the ten listed existing mathematical quantities developed across the project:

| Candidate Quantity | Exact Definition & Codomain | Grade Transformation Law | Common External Value? (CR1) | Proven Layer Membership? (CR2) | Nonzero iff Off-Line? (CR3) | Earliest Failed / Unproved Condition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Normalized Radial Displacement** | $R_\tau(s_\rho(k), k) = \tau^{-k}\Re(s_\rho(k)) - 1/2 \in \mathbb{R}$ | Grade-invariant: $R_\tau(s, k) = \delta$ | **YES** (Identical value $\delta$) | **NO** (No law proves $\delta \in \tau^K \mathbb{Z}$) | **YES** ($\delta \ne 0 \iff \Re\rho \ne 1/2$) | **(CR2) Layer membership**. Unproved; requiring $\delta \in L_K$ assumes discrete quantization. |
| **2. Raw Centered Displacement** | $d_\rho(K) = \Re(z_K(\rho)) = \tau^K \delta \in \mathbb{R}$ | Covariant of weight 1: $d_\rho(K) = \tau^K d_\rho(0)$ | **NO** ($\tau^K \delta \ne \tau^J \delta$ for $K \ne J$) | **NO** ($\tau^K \delta \in L_K \iff \delta \in \mathbb{Z}$, unproved) | **YES** ($\tau^K \delta \ne 0 \iff \delta \ne 0$) | **(CR1) Common external value** and **(CR2) Layer membership**. |
| **3. Curvature / Quartet Defect** | $\mathscr{K}_\tau(\rho) = B_\rho''(0)/(2(\log\tau)^2) = \delta^2 \in \mathbb{R}_{\ge 0}$ | Invariant under transported unit: $(r_K d_{\rho,K})^2 = \delta^2$ | **YES** (Identical value $\delta^2$) | **NO** (No law proves $\delta^2 \in \tau^K \mathbb{Z}$) | **YES** ($\delta^2 > 0 \iff \delta \ne 0$) | **(CR2) Layer membership**. Detects off-line position but is continuous real-valued. |
| **4. Grade Character & Defect** | $\chi_\rho(K) = \tau^{K(\rho-1/2)} = \exp(K(\delta+i\gamma)\log\tau) \in \mathbb{C}^\times$; $|\chi_\rho(K)| = \tau^{K\delta}$; $D_K(\rho) = 4\sinh^2(K\delta\log\tau/2)$ | Group character: $\chi_\rho(K+J) = \chi_\rho(K)\chi_\rho(J)$ | **NO** (Values scale as powers $q^K$ with modulus $\tau^{K\delta}$) | **NO** (Character values lie on complex spirals, not $L_K$) | **YES for $D_K$** ($D_K > 0 \iff \delta \ne 0$) | **(CR1) Common external value** and **(CR2) Layer membership**. |
| **5. Station Scaffold Locations** | $x_{n,K} = n\tau^K \in L_K$ ($n \in \mathbb{Z}$) | Dilation: $x_{n,K} = \tau^{K-J} x_{n,J}$ | **NO** ($n\tau^K \ne n\tau^J$ for $K \ne J, n \ne 0$) | **YES** ($x_{n,K} \in L_K$ by definition) | **NO** (Independent of zeros $\rho$; exists for all $n$) | **(CR1) Common value** and **(CR3) Off-line sensitivity**. |
| **6. Logarithmic Prime Frequencies** | Dilated: $\tau^{-K}\log n$; Translated: $\log n + K\log\tau$ | Dilated: $\tau^{-K}\omega_0$; Translated: $\nu_0 + K\log\tau$ | **NO** (Shifts under grade change) | **NO** ($\log n \notin \tau^K \mathbb{Z}$; frequencies lie in Fourier dual) | **NO** (Prime frequencies are independent of zero position $\delta$) | **(CR1), (CR2), and (CR3) all fail**. |
| **7. Zero-Counting / Winding Integers** | $N(T, \mathcal{C}_K) = \frac{1}{2\pi}\Delta_{\mathcal C_K} \arg\xi(s) \in \mathbb{Z}$ under transported contour $\mathcal C_K = \tau^K \mathcal C_0$ and height $T_K = \tau^K T$ | Invariant under transported contour $\mathcal C_K$ | **YES** ($N(T_K, \mathcal C_K) = N(T, \mathcal C_0) \in \mathbb{Z}$) | **NO** ($N \in \mathbb{Z} = L_0$, but $N \notin L_K = \tau^K \mathbb{Z}$ for $K \ne 0$) | **NO** ($N(T)$ counts all zeros, invariant under horizontal shift) | **(CR2) Layer membership** and **(CR3) Off-line sensitivity**. |
| **8. Logarithmic Derivative Residues** | Residue at zero: $\operatorname{Res}_{s=\rho}(-\xi_K'/\xi_K) = m_\rho \in \mathbb{Z}_{>0}$ | Multiplier adds constant shift; residue is invariant | **YES** (Multiplicity $m_\rho$ is identical) | **NO** ($m_\rho \in \mathbb{Z} = L_0$, but $m_\rho \notin L_K = \tau^K \mathbb{Z}$ for $K \ne 0$) | **NO** ($m_\rho \ge 1$ for all zeros, whether $\delta = 0$ or $\delta \ne 0$) | **(CR2) Layer membership** and **(CR3) Off-line sensitivity**. |
| **9. Linear Explicit-Formula Tests** | $\mathcal C_{K,j}[\phi] = \sum_\rho \phi(\tau^{-K}\gamma_\rho) - \dots$ | Pullback identity: $\mathcal C_{K,j}[\phi] \equiv \mathcal C_0[\phi \circ a_K]$ | **NO for raw evaluations** (Agrees only after converting test functions and units) | **NO** (Distributional evaluations, not lattice points) | **NO** (Vanishes identically for the complete zero distribution) | **(CR1) Raw Common Value**, **(CR2)**, and **(CR3)**. |
| **10. Completed-ξ Cross-Terms (Fixed Gaussian Instance)** | $\mathfrak X_{\xi, W} = \Re\langle G_0, \ddot G_0\rangle_W \in \mathbb{R}$ (Certified for $a=1.5, \sigma_W=1.0$) | Evaluated in base frame under dilation jet | **YES** (Invariant functional evaluated in fixed Gaussian frame) | **NO** (Continuous integral: $\mathfrak X_{\xi, W} \approx 0.02317 \notin \tau^K \mathbb{Z}$) | **NO** (Strictly positive on critical line; not a per-zero detector) | **(CR2) Layer membership** and **(CR3) Off-line sensitivity**. |

---

## 26.4 Research Mini-Sprint: Investigation of Candidate CR-1

### Ranking and Selection
Of the ten listed candidates, **Candidate CR-1 (Normalized Radial Displacement $\delta$)** is the closest to completing the bridge:
- **(CR1) Proved**: $R_\tau(s_\rho(k), k) = \delta$ identically across all grades (grade-invariant).
- **(CR3) Proved**: $\delta \ne 0 \iff \Re\rho \ne 1/2$ (strictly detects off-line zeros).
- **Missing Condition**: **(CR2) Layer Membership** ($\delta \in L_K = \tau^K \mathbb{Z}$ and $\delta \in L_J = \tau^J \mathbb{Z}$ for $K \ne J$).

### The Strong Unresolved Bridge Condition
We analyze the implication required to establish (CR2):
$$\mathbf{IMP\text{-}CR2}: \quad \text{The complete prime–zeta relationship forces } \delta \in L_K \cap L_J \quad (K \ne J).$$

1. **Exact Symbolic Reduction**:
   By Lindemann's theorem (1882), $\tau = 2\pi$ is transcendental, which implies $L_K \cap L_J = \{0\}$ for $K \ne J \in \mathbb{Z}$. Therefore:
   $$\delta \in L_K \cap L_J \iff \delta = 0.$$
2. **The Nature of the Obstacle**:
   For the normalized displacement candidate, (CR2) together with layer separation and (CR3) is sufficient to imply $\delta = 0$. Because $L_K \cap L_J = \{0\}$ for distinct integer grades, any candidate satisfying (CR1) and (CR2) forces $\delta = 0$ directly. This establishes layer membership as a **strong unresolved bridge condition** whose independent derivation without assuming the Riemann Hypothesis remains the core open obstacle.
3. **Euler Product Verification**:
   The Euler product $\zeta(s) = \prod_p (1 - p^{-s})^{-1}$ produces prime-power Dirac combs with frequencies $\{\log p^m\}$. These frequencies are dense on $\mathbb{R}$ and belong to the continuous Fourier dual, not to the discrete station lattices $\tau^K \mathbb{Z}$. No algebraic or analytic law forces zero ordinates or displacements into station lattices without an unproved quantization premise.

**Conclusion of Cycle 3 Mini-Sprint**:
None of the ten listed existing quantities in the transcendental continuation inventory simultaneously satisfies (CR1), (CR2), and (CR3).
- Status: `COMMON-REFERENT BRIDGE NOT FOUND IN EXISTING TC OBSERVABLES`.

---

# 27. Cycle 4: Bounded Grade-Character Bridge & Canonical Norm Audit

## 27.1 Foundations: The Canonical Grade Character and Modulus Law

For a nontrivial zero $\rho = 1/2 + \delta + i\gamma$, the canonical transcendental continuation grade character is defined by:
\[
\chi_\rho(K) = \tau^{K(\rho - 1/2)} = \exp\big(K(\delta + i\gamma)\log\tau\big), \quad \tau = 2\pi, \quad K \in \mathbb{Z}.
\]
Let $q_\rho = \exp\big((\delta + i\gamma)\log\tau\big) = \tau^{\delta + i\gamma}$. Then $\chi_\rho(K) = q_\rho^K$.

### Elementary Group Properties
1. **Group Homomorphism on $(\mathbb{Z}, +)$**:
   \[
   \chi_\rho(K + J) = q_\rho^{K+J} = q_\rho^K q_\rho^J = \chi_\rho(K)\chi_\rho(J), \quad \chi_\rho(0) = 1, \quad \chi_\rho(-K) = \frac{1}{\chi_\rho(K)}.
   \]
2. **Exact Modulus Law**:
   Since $\tau = 2\pi > 1$ and $\gamma \in \mathbb{R}$, $|\tau^{i K \gamma}| = 1$. Thus:
   \[
   |\chi_\rho(K)| = |\tau^{K\delta} \tau^{i K \gamma}| = \tau^{K\delta} = \exp(K\delta\log\tau).
   \]
3. **Modulus Defect**:
   The reflection-pair symmetric defect is given by:
   \[
   D_K(\rho) = |\chi_\rho(K)| + |\chi_\rho(-K)| - 2 = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right) \ge 0,
   \]
   which vanishes for fixed nonzero $K \in \mathbb{Z} \setminus \{0\}$ if and only if $\delta = 0$.

---

## 27.2 Theorems A and B: Character Criteria

### Theorem A (Unitary Grade-Character Criterion)
> **Theorem A**: Let $\tau > 1$. The grade character $\chi_\rho$ takes values in the unit circle $S^1 = \{z \in \mathbb{C} : |z| = 1\}$ for every $K \in \mathbb{Z}$ if and only if $\delta = 0$.
> Furthermore, unit modulus at any single non-zero grade $K_0 \in \mathbb{Z} \setminus \{0\}$ is necessary and sufficient:
> \[
> |\chi_\rho(K_0)| = 1 \iff \delta = 0.
> \]

*Proof*:
$|\chi_\rho(K_0)| = \tau^{K_0\delta}$. Since $\tau > 1$, $\log\tau > 0$.
Thus $\tau^{K_0\delta} = 1 \iff K_0\delta\log\tau = 0$.
Since $K_0 \ne 0$ and $\log\tau > 0$, this holds if and only if $\delta = 0$. $\blacksquare$

### Theorem B (Bilateral Boundedness Criterion)
> **Theorem B**: Let $\tau > 1$. The grade character sequence $\{\chi_\rho(K)\}_{K \in \mathbb{Z}}$ is bounded over the full bilateral group $\mathbb{Z}$:
> \[
> \sup_{K \in \mathbb{Z}} |\chi_\rho(K)| < \infty \iff \delta = 0.
> \]

*Proof*:
1. If $\delta = 0$, then $|\chi_\rho(K)| = \tau^0 = 1$ for all $K \in \mathbb{Z}$, so $\sup_{K \in \mathbb{Z}} |\chi_\rho(K)| = 1 < \infty$.
2. Conversely, suppose $M = \sup_{K \in \mathbb{Z}} |\chi_\rho(K)| < \infty$.
   - **Forward Grade Branch ($K \ge 0$)**:
     If $\delta > 0$, then $\tau^\delta > 1$. For $K \in \mathbb{Z}_{\ge 0}$, $|\chi_\rho(K)| = (\tau^\delta)^K \to +\infty$ as $K \to +\infty$, which contradicts boundedness by $M$. Hence boundedness on $K \ge 0$ forces $\delta \le 0$.
   - **Backward Grade Branch ($K \le 0$)**:
     If $\delta < 0$, then $-\delta > 0$, so $\tau^{-\delta} > 1$. Setting $K = -m$ with $m \in \mathbb{Z}_{\ge 0}$, $|\chi_\rho(-m)| = (\tau^{-\delta})^m \to +\infty$ as $m \to +\infty$, which contradicts boundedness by $M$. Hence boundedness on $K \le 0$ forces $\delta \ge 0$.
   - **Bilateral Intersection**:
     Combining the forward and backward branches:
     \[
     (\delta \le 0) \wedge (\delta \ge 0) \implies \delta = 0.
     \]
This proves that bilateral boundedness over $\mathbb{Z}$ forces $\delta = 0$. $\blacksquare$

---

## 27.3 Separation of the Three Core Claims

To maintain mathematical rigor, we strictly distinguish three logical layers:

1. **Abstract Character Fact (Proved)**:
   Any character of the form $\chi(K) = \tau^{K(\delta+i\gamma)}$ is unitary and bilaterally bounded on $\mathbb{Z}$ if and only if $\delta = 0$. This is an elementary property of exponential sequences in $\mathbb{C}$ that holds independently of primes, zeta functions, and arithmetic.
2. **Unitary Dilation Model (Proved Geometric Action)**:
   The dilation operator $U_a f(x) = a^{1/2}f(ax)$ is an exact unitary isometry on $L^2(\mathbb{R}^+, dx)$. Its generalized continuous spectrum corresponds to the unitary axis $\Re(s) = 1/2$. However, generalized eigencharacters $x^{-s}$ are not $L^2$ vectors, and standard dilation invariance holds for all functions regardless of whether their zeros lie on the critical line.
3. **Prime–Zero Membership Bridge (The Open Obligation)**:
   Does the complete prime–zeta relationship (Euler product, completed function $\xi$, explicit formula, or TC transport) force the character $\chi_\rho$ belonging to a non-trivial zeta zero to be unitary or bilaterally bounded?
   This is the substantive mathematical question. If derived independently, Theorems A and B yield an exclusion mechanism. If not derived, boundedness is merely an assumed premise equivalent to RH.

---

## 27.4 Audit of Five Canonical Norm and Space Models

We systematically audit five candidate mathematical frameworks to determine whether TC supplies an independent proof that $\chi_\rho$ must be unitary or bounded:

### Model A: Intrinsic Scalar Norm
- **Ambient Space**: $\mathbb{C}$ with standard modulus $|\cdot|$.
- **Analysis**: The raw modulus $|\chi_\rho(K)| = \tau^{K\delta}$ depends exponentially on $K$ whenever $\delta \ne 0$. Converting back to grade zero via the inverse coordinate map $C_K(|\chi|) = \tau^{-K\delta}|\chi|$ yields 1 identically, but this conversion explicitly multiplies by $\tau^{-K\delta}$, using the unknown displacement $\delta$ and tautologically producing 1 without constraining $\delta$.
- **Finding**: Coordinate redundancy guarantees that relations agree *after* conversion of units, but does not constrain the raw scalar exponent $\delta$.

### Model B: Multiplicative Haar Dilation on $L^2(\mathbb{R}^+, dx/x)$
- **Ambient Space**: $L^2(\mathbb{R}^+, dx/x)$ with dilation operator $U_\tau f(x) = f(\tau x)$ (or half-density dilation $V_\tau f(x) = \tau^{1/2}f(\tau x)$ on $L^2(\mathbb{R}^+, dx)$).
- **Analysis**: $U_\tau$ is an exact unitary operator because the Haar measure $dx/x$ is dilation-invariant. The Mellin transform diagonalizes $U_\tau$ with generalized eigencharacters $\phi_s(x) = x^{-s}$, where $U_\tau \phi_s = \tau^{-s}\phi_s$. Unimodularity of the multiplier $|\tau^{-s}| = 1$ requires $\Re(s) = 0$ (or $\Re(s) = 1/2$ for half-density).
- **The Gap**: The power functions $x^{-s}$ are not in $L^2(\mathbb{R}^+, dx/x)$; they are tempered distributions. Furthermore, non-trivial zeta zeros $\rho$ are zeros of $\xi(s)$, not eigenvalues of the dilation group $U_\tau$. No proved operator identity identifies the discrete zero set $\{\rho\}$ with the point spectrum or spectral projection of $U_\tau$.

### Model C: Group $C^*$-Algebra Characters of $\mathbb{Z}$
- **Ambient Space**: $C^*(\mathbb{Z}) \cong C(S^1)$.
- **Analysis**: By Gelfand's representation theorem and Bochner-Herglotz, all bounded multiplicative linear functionals (characters) on the group $C^*$-algebra $C^*(\mathbb{Z})$ correspond to points on the unit circle $S^1$.
- **The Gap**: An off-line zero with $\delta \ne 0$ produces a character $\chi_\rho(K) = q_\rho^K$ that is exponentially unbounded on $\mathbb{Z}$. It does **not** define a bounded linear functional on $\ell^1(\mathbb{Z})$ or $C^*(\mathbb{Z})$. Declaring that $\chi_\rho$ must belong to the spectrum of $C^*(\mathbb{Z})$ is an a priori restriction to unitary characters, which assumes $\delta = 0$ rather than proving it.

### Model D: Explicit Formula and Weil Positivity
- **Ambient Space**: Schwartz space $\mathcal{S}(\mathbb{R})$ and its dual $\mathcal{S}'(\mathbb{R})$.
- **Analysis**: Weil's explicit formula expresses the spectral sum $\sum_\rho \widehat{h}(\rho)$ in terms of prime-power distributions and Archimedean integrals.
- **The Equivalence Barrier**: Weil (1952) proved that the quadratic form $Q_W(f * f^*) \ge 0$ for all admissible test functions is **strictly equivalent to the Riemann Hypothesis**. Deriving that the zero characters enter a positive-definite distribution without assuming Weil positivity is an open problem identical to RH itself.

### Model E: Alternative Weighted Norms and Non-Euler Countermodels
- **Ambient Space**: Weighted sequence space $\ell^\infty_w(\mathbb{Z})$ with weight $w(K) = \tau^{-K\delta_0}$.
- **Analysis**: Under this weighted norm, an off-line zero with displacement $\delta = \delta_0$ satisfies $\sup_{K \in \mathbb{Z}} w(K)|\chi_\rho(K)| = 1 < \infty$.
- **Countermodel Exclusion**: The Davenport–Heilbronn zeta function:
  \[
  f(s) = \frac{1 - i\kappa}{2} L(s, \chi) + \frac{1 + i\kappa}{2} L(s, \bar\chi)
  \]
  satisfies the exact functional equation $\xi(s) = \xi(1-s)$ and dilation symmetry under TC, but possesses infinitely many zeros off the critical line ($\delta \ne 0$). Under TC, its zero characters $\chi_\rho(K) = \tau^{K(\delta+i\gamma)}$ are non-unitary and bilaterally unbounded. This rigorously proves that **functional equation symmetry and coordinate dilation together cannot force character unitarity or boundedness**. The Euler product is an indispensable premise, but the Euler product converges only in $\Re(s) > 1$ and does not directly bound zero characters in the critical strip.

---

## 27.5 Synthesis: Status of the Bounded Grade-Character Bridge

| Candidate ID | Name | Mathematical Content | Proved Status | Missing Bridge Implication | Final Epistemic Classification |
| :--- | :--- | :--- | :--- | :--- | :--- |
---

## 28. Cycle 5: Log-Haar Temperedness Bridge & Prime Error Distribution Audit

### 28.1 Logarithmic Coordinates and Additive Grade Translation

Under the logarithmic coordinate change:
\[
u = \log x, \quad x = e^u \in (0, \infty), \quad \frac{dx}{x} = du
\]
multiplicative dilation by grade scale $\tau^K$ ($x \mapsto \tau^K x$) becomes pure additive translation on the real log-line:
\[
u \mapsto u + K\log\tau, \quad \tau = 2\pi, \quad K \in \mathbb{Z}.
\]
For a non-trivial zero $\rho = 1/2 + \delta + i\gamma$, the centered spectral coordinate is $\lambda = \rho - 1/2 = \delta + i\gamma$. The centered zero mode in log coordinates is:
\[
\phi_\lambda(u) = e^{\lambda u} = e^{(\delta + i\gamma)u} = e^{\delta u} e^{i\gamma u}.
\]
Under grade translation by $t_K = K\log\tau$:
\[
\phi_\lambda(u + K\log\tau) = e^{(\delta + i\gamma)(u + K\log\tau)} = e^{K(\delta + i\gamma)\log\tau} \phi_\lambda(u) = \chi_\rho(K) \phi_\lambda(u),
\]
where $\chi_\rho(K) = \tau^{K(\delta + i\gamma)}$ is the canonical TC grade character.

Its modulus is strictly exponential:
\[
|\phi_\lambda(u)| = e^{\delta u}.
\]

---

### 28.2 Theorem C: Regular Tempered Distribution Classification

#### Statement
> Let $\lambda = \delta + i\gamma \in \mathbb{C}$ and $\phi_\lambda(u) = e^{\lambda u}$ for $u \in \mathbb{R}$. As a locally integrable function on $\mathbb{R}$, $\phi_\lambda$ defines a regular tempered distribution $T_{\phi_\lambda} \in \mathcal{S}'(\mathbb{R})$ via:
> \[
> \langle T_{\phi_\lambda}, \psi \rangle = \int_{-\infty}^\infty \phi_\lambda(u) \psi(u) \, du, \quad \psi \in \mathcal{S}(\mathbb{R})
> \]
> if and only if $\delta = 0$.

#### Proof
1. **Sufficiency ($\delta = 0$)**: When $\delta = 0$, $|\phi_\lambda(u)| = |e^{i\gamma u}| = 1$ for all $u \in \mathbb{R}$. A bounded continuous function satisfies $|f(u)| \le 1 \cdot (1 + |u|)^0$. By Schwartz's theorem (1950, *Théorie des distributions*, Tome II, Ch. VII), any locally integrable function bounded by a polynomial defines a continuous linear functional on $\mathcal{S}(\mathbb{R})$.
2. **Necessity ($\delta \ne 0$)**: Suppose $\delta \ne 0$. Without loss of generality assume $\delta > 0$ (the case $\delta < 0$ is identical under $u \to -u$). Then as $u \to +\infty$, $|\phi_\lambda(u)| = e^{\delta u}$ grows exponentially.
   Let $\psi_0 \in C_c^\infty(\mathbb{R})$ be non-negative with $\int \psi_0 = 1$, supported in $[0, 1]$. Define the test sequence $\psi_k(u) = e^{-\delta k / 2} \psi_0(u - k) \in \mathcal{S}(\mathbb{R})$ for $k \in \mathbb{N}$.
   For any Schwartz seminorm $p_{\alpha, \beta}(\psi) = \sup_u |u^\alpha \psi^{(\beta)}(u)|$:
   \[
   p_{\alpha, \beta}(\psi_k) \le C_{\alpha, \beta} (k + 1)^\alpha e^{-\delta k / 2} \to 0 \quad \text{as } k \to \infty.
   \]
   Thus $\psi_k \to 0$ in the Fréchet topology of $\mathcal{S}(\mathbb{R})$.
   However, the distributional action evaluates to:
   \[
   \langle \phi_\lambda, \psi_k \rangle = \int_k^{k+1} e^{(\delta + i\gamma)u} e^{-\delta k / 2} \psi_0(u - k) \, du = e^{\delta k / 2} e^{i\gamma k} \int_0^1 e^{(\delta + i\gamma)v} \psi_0(v) \, dv.
   \]
   Taking absolute values:
   \[
   |\langle \phi_\lambda, \psi_k \rangle| = e^{\delta k / 2} \left|\int_0^1 e^{(\delta + i\gamma)v} \psi_0(v) \, dv\right| \to \infty \quad \text{as } k \to \infty.
   \]
   This directly contradicts continuity of the functional on $\mathcal{S}(\mathbb{R})$. Therefore, $\phi_\lambda$ does not extend to a regular tempered distribution in $\mathcal{S}'(\mathbb{R})$ when $\delta \ne 0$.

#### Distinction of Distributional Categories
- **$L^2(\mathbb{R}, du)$ Vector**: $\int_\mathbb{R} |\phi_\lambda(u)|^2 du = \int_\mathbb{R} e^{2\delta u} du = \infty$ for all $\delta \in \mathbb{R}$ (including $\delta = 0$). Zero modes are **never in $L^2(\mathbb{R}, du)$**.
- **Bounded Character $C_b(\mathbb{R})$**: Bounded on all of $\mathbb{R}$ iff $\delta = 0$.
- **Regular Tempered Distribution $\mathcal{S}'(\mathbb{R})$**: Extends to unweighted Schwartz space iff $\delta = 0$.
- **Compactly Supported Distribution $\mathcal{D}'(\mathbb{R})$**: Locally integrable, so $\phi_\lambda \in \mathcal{D}'(\mathbb{R})$ for *every* $\delta \in \mathbb{R}$. Mere existence in $\mathcal{D}'(\mathbb{R})$ does not exclude off-line zeros.

---

### 28.3 The Prime-Side Distribution and the Riemann-Weil Explicit Formula

The Riemann-Weil explicit formula connects the prime-power sum to the zeros:
\[
\sum_\rho \widehat{h}(\rho - 1/2) = \widehat{h}(1/2) + \widehat{h}(-1/2) - \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} [h(\log n) + h(-\log n)] + \text{Archimedean terms}.
\]
In log coordinates $u = \log x$, the raw prime-power distribution is:
\[
d\Pi(u) = \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} \delta(u - \log n).
\]
Its cumulative mass on $[0, U]$ is:
\[
\int_0^U d\Pi(u) = \sum_{n \le e^U} \frac{\Lambda(n)}{\sqrt{n}} \sim \int_2^{e^U} \frac{dx}{\sqrt{x}} = 2\sqrt{e^U} = 2 e^{U/2}.
\]
The cumulative mass grows exponentially as $2e^{U/2}$. Therefore, the uncompleted prime measure is **not tempered** on $\mathbb{R}$. Centering by $1/2$ (the factor $n^{-1/2}$) does not cancel the leading density. The pole contribution $-e^{u/2} du$ must be subtracted to center the prime distribution:
\[
d\Pi_{\text{sub}}(u) = \sum_{n \ge 1} \frac{\Lambda(n)}{\sqrt{n}} \delta(u - \log n) - e^{u/2} du.
\]

---

### 28.4 Normalized Chebyshev Prime Error and Equivalence to RH

Define the Chebyshev prime-counting error:
\[
\Delta(x) = \psi(x) - x = \sum_{n \le x} \Lambda(n) - x.
\]
In logarithmic coordinate $u = \log x$, the normalized prime error is:
\[
E(u) = e^{-u/2}(\psi(e^u) - e^u) = \frac{\psi(x) - x}{\sqrt{x}}.
\]

1. **Unconditional Growth (Vinogradov-Korobov 1958)**:
   The best known unconditional bound is:
   \[
   \psi(x) - x = O\left(x \exp\left(-c \frac{(\log x)^{3/5}}{(\log\log x)^{1/5}}\right)\right).
   \]
   Dividing by $\sqrt{x} = e^{u/2}$:
   \[
   E(u) = O\left(e^{u/2} \exp\left(-c \frac{u^{3/5}}{(\log u)^{1/5}}\right)\right) = O\left(e^{u/2 - o(u)}\right).
   \]
   Because the sub-exponential decay cannot cancel $e^{u/2}$, the Vinogradov-Korobov bound establishes only an upper bound $O(e^{u/2 - o(u)})$, which is too weak to prove polynomial growth or temperedness. However, an upper bound cannot establish a lower-growth obstruction or prove non-temperedness. The true unconditional status of $E(u)$ is **UNKNOWN FROM THIS BOUND** (prior unconditional non-temperedness claim withdrawn in Cycle 6).
2. **Conditional Growth (von Koch 1901 under RH)**:
   If RH holds ($\delta = 0$ for all non-trivial zeros), then:
   \[
   \psi(x) - x = O(\sqrt{x} \log^2 x) \iff E(u) = O(u^2).
   \]
   Polynomial growth $O(u^2)$ guarantees that $E(u)$ defines a regular tempered distribution in $\mathcal{S}'(\mathbb{R})$.
3. **Cramér-Ingham Equivalence (1919, 1932)**:
   Cramér and Ingham proved:
   \[
   \Theta = \sup_\rho \Re(\rho) = \frac{1}{2} + \sup_\rho \delta = \limsup_{u \to \infty} \frac{\log |E(u)|}{u}.
   \]
   Consequently:
   \[
   E(u) \in \mathcal{S}'(\mathbb{R}) \iff \forall \epsilon > 0, E(u) = O(e^{\epsilon u}) \iff \Theta \le \frac{1}{2} \iff \text{RH holds}.
   \]
   **Finding**: The proposition that the normalized prime error $E(u)$ belongs to the tempered distribution space $\mathcal{S}'(\mathbb{R})$ is **strictly logically equivalent to the Riemann Hypothesis**. It cannot be proved unconditionally from arithmetic to serve as an exclusion bridge.

---

### 28.5 Pointwise Transport vs Bilateral Orbit Uniformity

Transcendental continuation acts by translation: $u \mapsto u + K\log\tau$.
We distinguish three distinct propositions:
- **(P1) Pointwise Transport**: For each fixed $K \in \mathbb{Z}$, the translate $T_K f(u) = f(u + K\log\tau)$ is well-defined.
- **(P2) Uniform Bilateral Orbit Bound**: There exists a single constant $M < \infty$ such that $\sup_{K \in \mathbb{Z}} \|T_K f\| \le M$.
- **(P3) Common Invariant Tempered Space**: The entire orbit $\{T_K f\}_{K \in \mathbb{Z}}$ belongs to a single translation-invariant tempered space $\mathcal{S}'(\mathbb{R})$ with uniform polynomial bounds.

#### Countermodel
Consider $f(u) = e^{\delta u}$ with $\delta \ne 0$.
- For every finite integer grade $K \in \mathbb{Z}$, $T_K f(u) = e^{\delta(u + K\log\tau)} = \tau^{K\delta} f(u)$. This is an exact, invertible, linear coordinate relation. Thus **(P1) holds unconditionally**.
- However, as $K \to \text{sgn}(\delta)\infty$, $\tau^{K\delta} \to +\infty$. The orbit is **exponentially unbounded** over $\mathbb{Z}$; **(P2) fails**.
- The function $f(u)$ is not a tempered distribution on $\mathbb{R}$; **(P3) fails**.

**Rigorous Conclusion**: Invertible coordinate transport (P1) is a consequence of coordinate redundancy at every finite grade. It does **not** imply bilateral orbit boundedness (P2) or common tempered space membership (P3) for an off-line zero.

---

### 28.6 Synthesis of the Log-Haar Temperedness Candidate

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-010** | **CLM-TC-010** | Log-Haar Temperedness Bridge & Prime Error Equivalence | Proved Theorem C ($\phi_\lambda \in \mathcal{S}' \iff \delta = 0$); proved prime error temperedness $E(u) \in \mathcal{S}' \iff \text{RH}$; proved (P1) $\not\Rightarrow$ (P2), (P3). | **CONDITIONAL ONLY** (Temperedness is an exact exclusion criterion, but its prime-side validity is strictly equivalent to RH) |

---

# 29. Cycle 6: Prime-Error Temperedness Equivalence Audit (Route I vs Route II)

In Cycle 6, the repository audited whether the continuous extension of the regular distribution $T_E$ to $\mathcal{S}'(\mathbb{R})$ genuinely forces the Riemann Hypothesis (RH) for this specific arithmetic error $E(u) = e^{-u/2}(\psi(e^u) - e^u)$.

### 29.1 Three Distinct Propositions
- **(A) The Riemann Hypothesis**: All nontrivial zeros of $\zeta(s)$ satisfy $\Re(\rho) = 1/2$.
- **(B) Pointwise Polynomial Bound**: $E(u) = O((1+u)^N)$ for some fixed $N \ge 0$ as $u \to +\infty$.
- **(C) Distributional Temperedness**: The distribution $T_E \in \mathcal{D}'(\mathbb{R})$ extends continuously to a tempered distribution $T \in \mathcal{S}'(\mathbb{R})$.

### 29.2 Equivalence Theorem: (A) $\iff$ (B) $\iff$ (C)
1. **$(A) \implies (B)$**: Proved by von Koch (1901) and Cramér (1919). Under RH, $\psi(x) - x = O(\sqrt{x}\log^2 x) \implies E(u) = O(u^2)$ ($N = 2$).
2. **$(B) \implies (C)$**: Standard Schwartz regular distribution theorem (1950). Any locally integrable function with polynomial growth $|f(u)| \le C(1+|u|)^N$ defines a regular tempered distribution $T_f \in \mathcal{S}'(\mathbb{R})$.
3. **$(B) \implies (A)$**: Proved by Ingham (1932, Theorem 30).
4. **$(C) \implies (A)$ (Proved in Cycle 6 via Route II)**:
   - For $u < \log 2$, $\psi(e^u) = 0$, so $E(u) = -e^{u/2}$ is smooth and analytic.
   - For a smooth cutoff $\chi \in C^\infty(\mathbb{R})$ with $\chi(u) = 0$ for $u \le 0.1$ and $\chi(u) = 1$ for $u \ge 0.5$, the truncated error $E_\chi(u) = \chi(u)E(u)$ is supported on $[0.1, \infty) \subset [0, \infty)$.
   - The tail $(1-\chi)E \in \mathcal{S}(\mathbb{R})$ is smooth and exponentially decaying like $-e^{u/2}$ as $u \to -\infty$ (unbounded toward $-\infty$, but in $\mathcal{S}(\mathbb{R})$). Thus $T_E \in \mathcal{S}'(\mathbb{R}) \iff T_{E_\chi} \in \mathcal{S}'(\mathbb{R})$.
   - The pairing $\langle T_{E_\chi}, e^{-zu}\rangle$ for $\Re(z) > 0$ is canonically defined by $\langle T_{E_\chi}, \rho(\cdot)e^{-z\cdot}\rangle$ where $\rho \in C^\infty(\mathbb{R})$ satisfies $\rho \equiv 1$ on $[0, \infty)$ and vanishes on $(-\infty, -0.5]$, independent of $\rho$.
   - By the Schwartz-Laplace theorem (Schwartz 1951, Tome II Chap. VIII Thm I; Hörmander 1983, Vol I Thm 7.4.2; Beffa 2024, Ch. 5), the Laplace transform of any tempered distribution supported on a half-line $[0, \infty)$ is **holomorphic on the entire open right half-plane $\Re(z) > 0$**.
   - For $\Re(z) > 1/2$, $\mathcal{L}[T_{E_\chi}](z) = G(z) - H(z)$, where $G(z) = -\frac{1}{z+1/2}\frac{\zeta'(z+1/2)}{\zeta(z+1/2)} - \frac{1}{z-1/2}$, and $H(z) = \int_0^{0.5} (\chi(u)-1)E(u)e^{-zu}du$ is an entire function whose integrand is supported on the compact interval $[0, 0.5]$.
   - At $z = 1/2$, the pole of $\zeta'/\zeta$ at $s = 1$ cancels identically with $-1/(z-1/2)$ (removable singularity).
   - If $\zeta(s)$ has any off-critical zero $\rho = 1/2 + \delta + i\gamma$ with $\delta > 0$, $G(z)$ has an isolated pole at $z_\rho = \delta + i\gamma \in \Re(z) > 0$ with residue $\text{Res}(G, z_\rho) = -m_\rho/\rho \ne 0$.
   - By the identity theorem for meromorphic functions, this pole cannot be cancelled by the entire function $H(z)$, contradicting the holomorphy of $\mathcal{L}[T_{E_\chi}]$ on $\Re(z) > 0$.
   - Hence no zero can have $\Re(\rho) > 1/2$, which by the functional equation forces all zeros to have $\Re(\rho) = 1/2$ (RH holds).
   - Thus **$(C) \implies (A)$ is rigorously proved**.

### 29.3 Route I: Why Real-Axis Tauberian Deconvolution Does Not Derive Slow Decrease Unconditionally
Route I investigates recovering pointwise bounds $(B)$ from smoothed averages $(E * \varphi)(U) = O((1+|U|)^N)$.
- In distribution theory, generic functions in $\mathcal{S}' \cap L^1_{\text{loc}}$ can oscillate wildly without pointwise polynomial bounds (e.g. $f(u) = e^u \cos(e^{2u}) = \frac{d}{du}\frac{\sin(e^{2u})}{2e^u} + \dots$).
- For $E(u)$, between prime powers $E'(u) = -\frac{1}{2}e^{-u/2}(\psi(e^u) + e^u) \approx -e^{u/2}$.
- The downward slope plunges exponentially as $-e^{u/2}$. Recovering pointwise bounds from smoothed convolutions without an a priori prime bound fails because Route I does not derive the required polynomial slow-decrease hypothesis unconditionally.
- Route I therefore stalls unconditionally, whereas Route II completely succeeds via half-line Laplace holomorphy.

### 29.4 Synthesis of Candidate TC-DISC-011 / CLM-TC-011

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-011** | **CLM-TC-011** | Prime-Error Distributional Temperedness Equivalence Theorem | Rigorously proved $(A) \iff (B) \iff (C)$ via Route II Schwartz-Laplace theorem and Hörmander Theorem 7.4.2; demonstrated Route I Tauberian slow-decrease obstruction. | **EQUIVALENCE PROVED** (Distributional temperedness genuinely implies RH, but is strictly equivalent to RH, providing no independent arithmetic shortcut) |

---

# 30. Cycle 7: TC Grade-Orbit Uniformity and Gluing Bridge (TC-DISC-012 / CLM-TC-012)

Cycle 7 addressed the decisive question:
> **Do the currently defined requirements of faithful Transcendental Continuation (TC) imply the uniform grade-orbit estimate needed for $T_E$ to be tempered?**

The answer is **NO**. Pointwise coordinate naturality and ambient distribution gluing hold identically for off-line modes; polynomial grade-orbit control is an independent condition equivalent to RH for the arithmetic prime error.

---

### 30.1 Theorem D — Local Grade-Orbit Characterization of Temperedness

Let $a = \log\tau > 0$ ($\tau = 2\pi$). Choose a smooth compactly supported partition of unity $\eta \in C_c^\infty((-a, a))$ satisfying:
\[
\sum_{K \in \mathbb{Z}} \eta(u - Ka) = 1 \quad \text{identically on } \mathbb{R}.
\]
Let $I = [-a, a]$ be a fixed compact fundamental neighborhood.

#### Theorem D Statement
For any distribution $T \in \mathcal{D}'(\mathbb{R})$, the following are equivalent:
1. $T$ extends continuously to a tempered distribution in $\mathcal{S}'(\mathbb{R})$.
2. There exist constants $C > 0$ and integers $N, m \ge 0$ such that for every $K \in \mathbb{Z}$ and every $\phi \in C_c^\infty(I)$,
\[
|\langle T, \phi(\cdot - Ka)\rangle| \le C (1 + |K|)^N \max_{0 \le j \le m} \|\phi^{(j)}\|_\infty.
\]

#### Proof Outline
- **$(1 \implies 2)$**: If $T \in \mathcal{S}'(\mathbb{R})$, by the Schwartz structure theorem (Hörmander Theorem 7.1.14), there exist $C_0, N_0, m_0$ such that $|\langle T, \psi\rangle| \le C_0 \sup_{u \in \mathbb{R}} (1 + |u|)^{N_0} \max_{j \le m_0} |\psi^{(j)}(u)|$. For $\psi_K(u) = \phi(u - Ka)$ with $\operatorname{supp}(\phi) \subseteq I$, on the support of $\psi_K$ we have $u \in I + Ka \implies 1 + |u| \le 1 + |Ka| + \sup_{t \in I}|t| \le C_I(1 + |K|)$. Thus $|\langle T, \phi(\cdot - Ka)\rangle| \le C (1 + |K|)^{N_0} \|\phi\|_{C^{m_0}(I)}$ uniformly in $K$.
- **$(2 \implies 1)$**: Let $\psi \in \mathcal{S}(\mathbb{R})$. Decompose $\psi = \sum_{K \in \mathbb{Z}} \psi_K$ where $\psi_K(u) = \eta(u - Ka)\psi(u)$. Then $\phi_K(v) = \psi_K(v + Ka) = \eta(v)\psi(v + Ka) \in C_c^\infty(I)$. By the Leibniz rule and Schwartz decay of $\psi$, $\|\phi_K\|_{C^m(I)} \le C' (1 + |K|)^{-(N+2)} p_{m, N+2}(\psi)$. Applying (2) termwise yields absolute convergence:
\[
|\langle T, \psi\rangle| \le \sum_{K \in \mathbb{Z}} |\langle T, \phi_K(\cdot - Ka)\rangle| \le C \sum_{K \in \mathbb{Z}} (1 + |K|)^N \|\phi_K\|_{C^m(I)} \le C'' p_{m, N+2}(\psi) < \infty.
\]
This proves continuous extension to $\mathcal{S}'(\mathbb{R})$. $\blacksquare$

#### Specialization to Prime Error
Combined with Cycle 6, Theorem D establishes the conditional reduction:
\[
\boxed{\operatorname{GradeOrbitBound}(E) \iff T_E \in \mathcal{S}'(\mathbb{R}) \iff \text{RH}.}
\]

---

### 30.2 Axiom Hierarchy: Levels P0, P1, and P2

We classify the structural levels of Transcendental Continuation:
1. **Level P0 (Pointwise Coordinate Naturality)**:
   At each finite grade $K \in \mathbb{Z}$, coordinates are related by an exact, invertible linear translation $u \mapsto u + Ka$.
   **Status**: ESTABLISHED. Satisfied by all modes, including off-line modes.
2. **Level P1 (Global Distribution Gluing / Common Referent)**:
   The family of grade-wise objects are restrictions/translates of one common ambient distribution $T \in \mathcal{D}'(\mathbb{R})$, rather than disjoint unrelated spaces.
   **Status**: ESTABLISHED. Any locally integrable mode $f \in L^1_{\text{loc}}(\mathbb{R})$ generates a regular distribution in $\mathcal{D}'(\mathbb{R})$ whose grade translates are genuine pullbacks under $u \mapsto u + Ka$.
3. **Level P2 (Uniform Finite-Order Polynomial Grade-Orbit Bound)**:
   The glued distribution obeys Theorem D's bound with constants $C, N, m$ independent of $K \in \mathbb{Z}$.
   **Status**: **NOT SUPPLIED BY TC AXIOMS**. Falsified by countermodel.

---

### 30.3 Countermodel Falsification: $f_{\delta, \gamma}(u) = \exp((\delta + i\gamma)u)$

Consider an off-line mode with $\delta \ne 0$:
\[
f_{\delta, \gamma}(u) = \exp((\delta + i\gamma)u).
\]
- **Level P0**: Exact translation covariance holds identically:
\[
f(u + Ka) = \tau^{K(\delta + i\gamma)} f(u).
\]
- **Level P1**: $f \in L^1_{\text{loc}}(\mathbb{R})$ defines an ambient distribution $T_f \in \mathcal{D}'(\mathbb{R})$.
- **Level P2**: For any test function $\phi \in C_c^\infty(I)$ with non-zero pairing $J_0 = \langle T_f, \phi\rangle$:
\[
|\langle T_f, \phi(\cdot - Ka)\rangle| = \tau^{K\delta} |J_0|.
\]
For $\delta > 0$, as $K \to +\infty$, $\tau^{K\delta}$ grows exponentially, outgrowing $(1 + |K|)^N$ for every fixed $N \ge 0$. For $\delta < 0$, the same exponential divergence occurs as $K \to -\infty$.

**Rigorous Falsification Conclusion**:
\[
\text{Coordinate Naturality (P0)} + \text{Distribution Gluing (P1)} \centernot\implies \text{Grade-Orbit Uniformity (P2)}.
\]
The abstract TC axioms alone do not exclude off-line modes or force polynomial grade-orbit bounds.

---

### 30.4 Lean 4 Formalization

The repository formalizes the bilateral polynomial growth obstruction in `formal/RiemannScope/Grade.lean`:
- **`exp_outgrows_pow`**: Proves that for any $c > 0, C \in \mathbb{R}, N \in \mathbb{N}$, there exists $K \in \mathbb{N}$ such that $C(1 + K)^N < \exp(K c)$, using Mathlib's `tendsto_pow_const_div_const_pow_of_one_lt`.
- **`polynomial_bilateral_grade_growth_implies_delta_zero`**: Proves that if $\tau > 1$ and an off-line mode modulus $\exp(K\delta\log\tau)$ satisfies a polynomial bilateral bound $C(1 + |K|)^N$ for all $K \in \mathbb{Z}$, then $\delta = 0$.
- Proved with zero `sorry`, zero `admit`, depending only on Mathlib foundational axioms `[propext, Classical.choice, Quot.sound]`.

---

### 30.5 Synthesis of Candidate TC-DISC-012 / CLM-TC-012

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-012** | **CLM-TC-012** | Discrete Grade-Orbit Criterion and Failure of Coordinate Naturality to Imply Grade-Uniform Temperedness | Proved Theorem D ($\operatorname{GradeOrbitBound}(T) \iff T \in \mathcal{S}'$); proved P0 + P1 $\not\implies$ P2 via exponential countermodel; Lean formalized `polynomial_bilateral_grade_growth_implies_delta_zero`. | **FAILURE OF COORDINATE NATURALITY TO IMPLY GRADE-UNIFORM TEMPEREDNESS** (Polynomial grade-orbit control is strictly equivalent to RH for prime error; not forced by TC axioms) |

---

# 31. Cycle 8: Canonical TC Diagram, Arithmetic Preservation, and Impossibility of Concrete Collision Witness (TC-DISC-013 / CLM-TC-013)

Cycle 8 returned the project to the original Transcendental Continuation (TC) hypothesis:
> **Does an off-critical zero force one nonzero arithmetic referent or event to be represented simultaneously in two distinct layers $L_K \cap L_J$ ($K \ne J$)?**

The sprint rigorously established:
1. **Preservation holds identically**: The grade representations $L_K = \tau^K \mathbb{N}_{\ge 1}$ are isomorphic ordered semirings, and the induced external Dirichlet series $D_K(s) = \tau^{-Ks}\zeta(s)$ has strictly fixed zero coordinates $\operatorname{div}(D_K) = \operatorname{div}(\zeta)$.
2. **Layer separation holds unconditionally**: By Lindemann's transcendence theorem (1882), $\tau^{K-J} = (2\pi)^{K-J}$ is transcendental for $K \ne J$, forcing $L_K \cap L_J = \emptyset$.
3. **No collision witness exists**: No mathematical arrow exists from an analytic zero back into a shared discrete arithmetic referent. Explicit formula zero modes $x^\rho/\rho$ are $C^\infty$ on $(0, \infty)$ with zero jump discontinuities; jumps occur strictly at intrinsic prime powers $\tau^K p^k \in L_K$. An off-critical zero ($\delta \ne 0$) alters continuous oscillatory amplitudes between jumps, but never shifts jump locations or creates new arithmetic events.

Therefore, **preservation and layer separation remain completely disconnected**.

---

### 31.1 Canonical Three-Level Construction

1. **Intrinsic Arithmetic Object $\mathcal{A}$**:
   - Carrier: $\mathbb{N}_{\ge 1} = \{1, 2, 3, \dots\}$.
   - Operations: standard integer addition $+$, standard multiplication $\cdot$, standard ordering $\le$.
   - Arithmetic invariants: primes $\mathcal{P} = \{2, 3, 5, \dots\}$, prime powers $p^k$, von Mangoldt weights $\Lambda(n)$.
2. **Grade Representation $L_K$ ($K \in \mathbb{Z}$)**:
   - External embedding: $\iota_K(n) = \tau^K n$ where $\tau = 2\pi$.
   - Discrete layer: $L_K = \iota_K(\mathbb{N}_{\ge 1}) = \{\tau^K, 2\tau^K, 3\tau^K, \dots\} \subset \mathbb{R}_+$.
   - Transported operations:
     \[
     \operatorname{add}_K(x, y) = x + y, \qquad \operatorname{mul}_K(x, y) = \tau^{-K} x y.
     \]
   - Transported order: $x \le_K y \iff x \le y$ (standard real order).
   - Exact semiring isomorphism:
     \[
     \iota_K(m + n) = \iota_K(m) + \iota_K(n), \qquad \iota_K(m \cdot n) = \tau^{-K} \iota_K(m) \iota_K(n).
     \]
3. **Analytic Zeta Construction**:
   - The Dirichlet series induced on the discrete layer $L_K$ with respect to raw external coordinates is:
     \[
     D_K(s) = \sum_{x \in L_K} x^{-s} = \sum_{n=1}^\infty (\tau^K n)^{-s} = \tau^{-Ks} \sum_{n=1}^\infty n^{-s} = \tau^{-Ks} \zeta(s).
     \]
   - Because $s \mapsto \tau^{-Ks} = \exp(-K s \log\tau)$ is an entire, everywhere non-vanishing function on $\mathbb{C}$, the zero divisor is **strictly invariant**:
     \[
     \operatorname{div}(D_K) = \operatorname{div}(\zeta) = \sum_\rho m_\rho [\rho].
     \]
   - The zero coordinates of $D_K$ are **identical to the zeros of $\zeta$**, not scaled.

---

### 31.2 Disambiguation of Zeta Objects

The repository previously grouped three distinct transformations under the name "Transcendental Continuation":

| Object | Definition | Origin | Zero Divisor | Relationship to Arithmetic |
| :--- | :--- | :--- | :--- | :--- |
| **$D_K(s)$** | $\tau^{-Ks}\zeta(s)$ | Direct Dirichlet summation over layer $L_K$ | $\operatorname{div}(D_K) = \operatorname{div}(\zeta)$ (**fixed**) | Canonical analytic image of $\iota_K$ |
| **$Z_K(s)$** | $\zeta(\tau^{-K}s)$ | Frequency dilation | $\operatorname{div}(Z_K) = \tau^K \operatorname{div}(\zeta)$ (**scaled**) | Dilated frequency coordinate; not induced by arithmetic sum |
| **$\xi_{\text{cent}, K}(s)$** | $\xi(1/2 + \tau^K(s - 1/2))$ | Centered coordinate dilation | $\rho_K = 1/2 + \tau^{-K}(\rho - 1/2)$ | Centered geometric rescaling around critical point |

These three constructions are **mathematically distinct transformations** with different zero behaviors. Arithmetic scaling $\iota_K(n) = \tau^K n$ induces $D_K(s) = \tau^{-Ks}\zeta(s)$, which preserves zero coordinates identically. It does *not* scale the zeros.

---

### 31.3 The Canonical Commutative Diagram

```
       Intrinsic Arithmetic A = (N_{>=1}, +, *, <=)
                     |
                     |  iota_K(n) = tau^K n   [Isomorphism]
                     v
             Grade Layer (L_K, +_K, *_K, <=)
                     |
                     |  Mellin / Dirichlet Summation
                     v
             External Dirichlet Series D_K(s) = tau^{-Ks} zeta(s)
                     |
                     |  Zero Divisor Mapping  [tau^{-Ks} != 0]
                     v
             Zero Divisor div(D_K) = div(zeta) = sum_rho m_rho [rho]
                     |
                     |  Conversion: div(D_K) -> div(A)
                     v
             Intrinsic Zero Set {rho : zeta(rho) = 0}
```

Every square and triangle in this diagram commutes:
- Intrinsic arithmetic maps isomorphically to $(L_K, +_K, *_K)$.
- Analytic continuation and zero extraction yield the invariant divisor $\operatorname{div}(\zeta)$.
- The conversion back to intrinsic coordinates is the identity map on zero coordinates.

---

### 31.4 The Preservation Theorem

**Theorem (TC Arithmetic and Spectral Preservation)**:
*For every integer grade $K \in \mathbb{Z}$:*
1. *The map $\iota_K: \mathbb{N}_{\ge 1} \to L_K$ is an isomorphism of ordered semirings with identity.*
2. *The external Dirichlet series $D_K(s) = \sum_{x \in L_K} x^{-s}$ extends meromorphically to $\mathbb{C}$ with simple pole at $s = 1$ of residue $\tau^{-K}$ and zero divisor $\operatorname{div}(D_K) = \operatorname{div}(\zeta)$.*
3. *All intrinsic arithmetic relationships (primes, divisibility, prime powers, von Mangoldt weights) and all analytic zero coordinates $\rho$ are identically preserved across all grades.*

---

### 31.5 Impossibility of Concrete Collision Witness

We audited the five mandatory collision witness conditions:

| Condition | Requirement | Audit Result | Status |
| :--- | :--- | :--- | :--- |
| **W1** | Prime–zeta derivation | Explicit formula relates $\psi$ to zeros $\sum x^\rho/\rho$ | SATISFIED |
| **W2** | Arithmetic incidence: $m\tau^K = n\tau^J$ | Requires $\tau^{K-J} = n/m \in \mathbb{Q}$ ($K \ne J$). By Lindemann (1882), $2\pi$ is transcendental, so $\tau^{K-J} \notin \mathbb{Q}$. | **IMPOSSIBLE / FALSIFIED** |
| **W3** | Off-line forcing: $\delta \ne 0$ forces collision | Zero modes $x^\rho/\rho$ are $C^\infty(0, \infty)$ with zero jumps. Jumps occur strictly at $\tau^K p^k \in L_K$. Off-line zeros alter smooth envelopes, never jump locations. | **IMPOSSIBLE / FALSIFIED** |
| **W4** | Critical-line compatibility | Vacuously satisfied since no collision occurs for any zero. | VACUOUS |
| **W5** | No hidden RH premise | The impossibility proof uses only Lindemann's transcendence and distribution theory of jump discontinuities; no circular RH premise is invoked. | SATISFIED |

#### Absence of the Analytic-to-Arithmetic Incidence Arrow
In the explicit formula:
\[
\psi_K(X) = \psi(\tau^{-K} X) = \tau^{-K} X - \sum_\rho \frac{(\tau^{-K} X)^\rho}{\rho} - \frac{\zeta'(0)}{\zeta(0)} - \frac{1}{2}\log(1 - (\tau^{-K}X)^{-2}).
\]
- The jump discontinuities of $\psi_K(X)$ occur precisely when $\tau^{-K} X = p^k \iff X = \tau^K p^k \in L_K$.
- The spectral sum $\sum_\rho \frac{(\tau^{-K} X)^\rho}{\rho}$ converges conditionally on $(0, \infty) \setminus L_K$ and is real-analytic away from prime powers.
- Each individual mode $t_\rho(X) = \frac{(\tau^{-K} X)^\rho}{\rho}$ is infinitely differentiable ($C^\infty$) on $(0, \infty)$.
- Therefore, an individual zero $\rho$ does not possess an arithmetic location or referent.
- An off-critical zero ($\delta \ne 0$) alters the growth rate of the continuous remainder, but cannot shift the jump locations $\tau^K p^k$ or create cross-layer intersections $L_K \cap L_J$.

**Conclusion**: No mathematical arrow exists from an off-line zero to a shared arithmetic referent in $L_K \cap L_J$. Preservation and external layer separation remain disconnected.

---

### 31.6 Lean 4 Formalization

The formalization in `formal/RiemannScope/Grade.lean` establishes the algebraic foundations:
- **`arithmetic_isomorphism_add`**: $\iota_K(m + n) = \operatorname{add}_K(\iota_K m, \iota_K n)$.
- **`arithmetic_isomorphism_mul`**: $\iota_K(m \cdot n) = \operatorname{mul}_K(\iota_K m, \iota_K n)$ for $A_K \ne 0$.
- **`grade_exp_injective`**: $\exp(K c) = \exp(J c) \implies K = J$ for $c \ne 0$.
- **`grade_layer_scale_distinct`**: $\tau > 1 \implies \exp(K\log\tau) \ne \exp(J\log\tau)$ for $K \ne J$.
- Built cleanly via `lake build` with zero `sorry` and foundational Mathlib axioms `[propext, Classical.choice, Quot.sound]`.

---

### 31.7 Synthesis of Candidate TC-DISC-013 / CLM-TC-013

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-013** | **CLM-TC-013** | Canonical TC Commutative Diagram, Arithmetic Preservation, and Impossibility of Concrete Collision Witness | Proved exact semiring isomorphism $\iota_K$; proved $D_K(s) = \tau^{-Ks}\zeta(s)$ has fixed zeros $\operatorname{div}(D_K) = \operatorname{div}(\zeta)$; proved $L_K \cap L_J = \emptyset$ by transcendence of $2\pi$; proved explicit formula zero modes $x^\rho/\rho$ are continuous with zero jump incidence; proved impossibility of collision witness $W$. | **PROVED / EXACT PRESERVATION / FALSIFICATION OF COLLISION WITNESS UNDER PRESENT TC MAPS** (Preservation and separation are disconnected; no arrow exists from zeros to arithmetic collisions) |

---

# 32. Cycle 9: Dense Disjoint Grade Layers and Limit-Compatibility Bridge (TC-DISC-014 / CLM-TC-014)

Cycle 9 addressed the limit-coincidence hypothesis of Transcendental Continuation:
> **Although two grade layers never share a nonzero arithmetic stop, do sequences of stops from different grades approaching the same external point force a common prime–zeta limit? If so, does an off-critical zero make that limit depend on the chosen grade sequence?**

The sprint resolved this question with an exact negative answer:
1. **The layer union $S_\tau = \bigcup_{K \in \mathbb{Z}} L_K$ is dense in $\mathbb{R}$, and $S_\tau^+ = \bigcup_{K \in \mathbb{Z}} L_K^+$ is dense in $\mathbb{R}_{>0}$**, while layers remain arithmetically separated ($L_K \cap L_J = \{0\}$ and $L_K^+ \cap L_J^+ = \emptyset$ for $K \ne J$) by the transcendence of $2\pi$.
2. **Correctly converted observables have strictly sequence-independent limits**: Along any two competing grade sequences $x_r = n_r \tau^{K_r} \to x$ and $y_r = m_r \tau^{J_r} \to x$ with $K_r \ne J_r$, converted Dirichlet characters and zero modes satisfy $\lim_{r\to\infty} [A(x_r) - A(y_r)] = 0$.
3. **No limit defect occurs for off-critical zeros**: Centered zero modes $x^\rho/\rho$ are smooth continuous functions on $(0, \infty)$ for every complex zero $\rho = 1/2 + \delta + i\gamma$. The limit is identical along all grade sequences for both on-line ($\delta = 0$) and off-line ($\delta \ne 0$) zeros.

**Conclusion**: Density gives uniqueness of continuous extension to $\mathbb{R}_{>0}$, but does not distinguish on-line from off-line zeros. Limit compatibility provides no exclusion mechanism.

---

### 32.1 Corrections to Cycle 8's Mathematical Scope

1. **Arithmetic Carriers**:
   - The general layer is $L_K = \tau^K \mathbb{Z}$, satisfying $L_K \cap L_J = \{0\}$ for $K \ne J$.
   - The positive carrier for Dirichlet summation is $L_K^+ = \tau^K \mathbb{N}_{>0}$, satisfying $L_K^+ \cap L_J^+ = \emptyset$ for $K \ne J$.
   - $\mathbb{N}_{>0}$ has no additive identity; it is an ordered cancellative commutative semigroup under addition and multiplication (semiring without zero).
2. **Intrinsic vs Raw-Coordinate Zeta**:
   - Transported multiplication on $L_K^+$: $x \odot_K y = xy/\tau^K$, with multiplicative identity $\tau^K$.
   - Intrinsic unit-reading map: $\nu_K(x) = x/\tau^K$.
   - Multiplicative Dirichlet character: $\chi_{K,s}(x) = \nu_K(x)^{-s}$, satisfying $\chi_{K,s}(x \odot_K y) = \chi_{K,s}(x)\chi_{K,s}(y)$.
   - **Intrinsic transported zeta**: $\zeta_K^{\text{int}}(s) = \sum_{x \in L_K^+} \nu_K(x)^{-s} = \sum_{n=1}^\infty n^{-s} = \zeta(s)$.
   - **Raw external Dirichlet series**: $D_K^{\text{raw}}(s) = \sum_{x \in L_K^+} x^{-s} = \tau^{-Ks}\zeta(s)$.
   - They differ by the non-vanishing unit factor $\tau^{-Ks}$; both preserve the zero divisor identically.
3. **Collision-Witness Logic**:
   - W2 ($m\tau^K = n\tau^J$) being impossible is the desired contradiction, not a failure of strategy.
   - The missing link was W3: no theorem forces an off-critical zero ($\delta \ne 0$) to imply arithmetic coincidence W2.
   - Scope is precisely: *no collision witness is supplied by the presently audited canonical maps*.
4. **Infinite Zero Sums & Pair-Isolation Barrier**:
   - While each individual mode $x^\rho/\rho$ is smooth on $(0, \infty)$, the conditionally convergent infinite sum $\sum_\rho x^\rho/\rho$ reconstructs discontinuous jump steps in Chebyshev's $\psi(x)$.
   - We retain the Pair-Isolation Barrier: individual zeros cannot be assigned specific jump locations without an isolation and convergence theorem for the complete sum.

---

### 32.2 Theorems A and B: Pairwise Separation and Density

#### Theorem A (Pairwise Arithmetic Separation)
*For distinct integer grades $K \ne J \in \mathbb{Z}$:*
\[
L_K \cap L_J = \{0\}, \quad \text{and} \quad L_K^+ \cap L_J^+ = \emptyset.
\]
*Proof*: If $x = m\tau^K = n\tau^J$ with $m \ne 0$, then $\tau^{K-J} = n/m \in \mathbb{Q}$. Since $K \ne J$, $K - J \ne 0$. By Lindemann (1882), $\pi$ and $\tau = 2\pi$ are transcendental, so $\tau^{K-J}$ is transcendental and cannot equal the rational $n/m$. Thus $m = 0 \implies x = 0$ and $n = 0$. Since $0 \notin \mathbb{N}_{>0}$, $L_K^+ \cap L_J^+ = \emptyset$. $\blacksquare$

#### Theorem B (Countability and Density)
*For every real $\tau > 1$, $S_\tau = \bigcup_{K \in \mathbb{Z}} \tau^K \mathbb{Z}$ is countable and dense in $\mathbb{R}$, and $S_\tau^+ = \bigcup_{K \in \mathbb{Z}} \tau^K \mathbb{N}_{>0}$ is dense in $\mathbb{R}_{>0}$.*
*Proof*:
1. Countability: Each $\tau^K \mathbb{Z}$ is countable; a countable union of countable sets is countable.
2. Constructive Density: Given $x \in \mathbb{R}$ and $\varepsilon > 0$, choose an integer $K \le -\lceil \frac{\log(1/\varepsilon) + \log 2}{\log \tau} \rceil$ so that $\tau^K < 2\varepsilon$. Let $n = \lfloor x\tau^{-K} + 1/2 \rfloor \in \mathbb{Z}$ be the nearest integer to $x/\tau^K$. Then $|x/\tau^K - n| \le 1/2$, so:
\[
|x - n\tau^K| \le \frac{\tau^K}{2} < \varepsilon.
\]
For $x > 0$ and $\varepsilon < x$, $n \ge 1$, so $n\tau^K \in S_\tau^+$. $\blacksquare$

---

### 32.3 Competing Grade Sequences

For fixed external $x > 0$, we construct two sequences of points in $S_\tau^+$ from strictly disjoint layers:
- **Sequence A**: $K_r = -r$, $n_r = \lfloor x\tau^r + 1/2 \rfloor$, $x_r = n_r \tau^{-r} \in L_{-r}^+$.
  Approximation bound: $|x_r - x| \le \frac{1}{2}\tau^{-r} \to 0$.
- **Sequence B**: $J_r = -(2r + 1)$, $m_r = \lfloor x\tau^{2r+1} + 1/2 \rfloor$, $y_r = m_r \tau^{-(2r+1)} \in L_{-(2r+1)}^+$.
  Approximation bound: $|y_r - x| \le \frac{1}{2}\tau^{-(2r+1)} \to 0$.
- **Disjointness**: $K_r = -r \ne -(2r+1) = J_r$ for all $r \ge 1$, so $x_r$ and $y_r$ lie in disjoint layers: $L_{-r}^+ \cap L_{-(2r+1)}^+ = \emptyset$.

---

### 32.4 Evaluation of Canonical Observables (Candidates 1–5)

| Candidate Observable | Definition | Behavior along $x_r \to x$ | Limit Defect $\lim [A(x_r) - A(y_r)]$ | Distinguishes $\delta \ne 0$? |
| :--- | :--- | :--- | :--- | :--- |
| **Cand 1: Raw Dirichlet Kernel** | $A_K^{\text{raw}}(x_r; s) = x_r^{-s}$ | Converges to $x^{-s}$ | **0** (continuous in $x > 0$) | **NO** |
| **Cand 2: Intrinsic Character** | $A_K^{\text{int}}(n_r; s) = n_r^{-s} = x_r^{-s}\tau^{K_r s}$ | Decays to $0$ as $K_r \to -\infty$ for $\Re(s) > 0$ | $0 - 0 = 0$ (unconverted local artifact) | **NO** |
| **Cand 3: Converted Character** | $\tilde{A}_K(x_r; s) = \tau^{-K_r s} n_r^{-s} = x_r^{-s}$ | Identical to Candidate 1; converges to $x^{-s}$ | **0** (correct Dirichlet conversion $A_K^{\text{raw}} = \tau^{-Ks} A_K^{\text{int}}$) | **NO** |
| **Cand 4: Centered Zero Mode** | $x_r^\lambda = x_r^{\delta + i\gamma}$ | Modulus $x_r^\delta \to x^\delta$, phase $e^{i\gamma\log x_r} \to e^{i\gamma\log x}$ | **0** (continuous for all $\delta \in \mathbb{R}$) | **NO** |
| **Cand 5: Transported Chebyshev** | $\psi_K(X) = \psi(\tau^{-K}X)$ | Diverges as $\tau^{-K}X \to \infty$ ($K \to -\infty$) | **WITHDRAWN** from pointwise limit claims; classified as untested pending Jacobian-normalized measure analysis (Cycle 10) | **NO** |

**Crucial Finding on Candidate 4 (Zero Modes)**:
An off-critical zero has $\lambda = \delta + i\gamma$ with $\delta \ne 0$. The function $u \mapsto u^{\delta + i\gamma}$ is $C^\infty$ on $(0, \infty)$. Along any sequence $u_r \to x > 0$:
\[
\lim_{r\to\infty} u_r^{\delta + i\gamma} = x^{\delta + i\gamma}.
\]
The limit depends strictly on the target point $x$, not on the grade sequence $K_r \to -\infty$. Therefore:
\[
\lim_{r\to\infty} [A(x_r) - A(y_r)] = x^\lambda - x^\lambda = 0.
\]
No limit defect exists for $\delta \ne 0$. Limit compatibility holds identically for all zeros. Continuous observables cannot distinguish on-line from off-line zeros.

---

### 32.5 Lean 4 Formalization

Formalized in `formal/RiemannScope/Grade.lean` under standard Mathlib foundational axioms:
- **`nu_K_mul_scaled`**: $\nu_K(x \odot_K y) = \nu_K(x) \cdot \nu_K(y)$ (exact multiplicative homomorphism).
- **`dirichlet_summand_raw_eq_converted`**: $(A_K \cdot n)^{-s} = A_K^{-s} \cdot n^{-s}$ (conversion relation).
- **`conditional_pairwise_separation`**: $m\tau^K = n\tau^J \implies \tau^{K-J} = n/m$ (rational collision criterion).
- **`lattice_step_approx_bound`**: $|x - n\Delta| \le \Delta/2$ for nearest-integer grid rounding (constructive density bound).
- Verified with zero `sorry` and foundational axioms `[propext, Classical.choice, Quot.sound]`.

---

### 32.6 Synthesis of Candidate TC-DISC-014 / CLM-TC-014

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-014** | **CLM-TC-014** | Dense Disjoint Grade Layers and Limit-Compatibility Audit | Proved Theorem A (separation) and Theorem B (countable density); derived $\zeta_K^{\text{int}}$ vs $D_K^{\text{raw}}$ distinction; tested Candidates 1–5; proved absence of grade-limit defect for both on-line and off-line zeros; Lean formalized 4 core algebraic/density lemmas. | **PROVED / EXACT PRESERVATION / FALSIFICATION OF LIMIT-COMPATIBILITY EXCLUSION MECHANISM** (Density gives uniqueness of continuation but does not distinguish on-line from off-line zeros) |

---

## 33. Cycle 10 — Prime-Measure Scaling Limit and Half-Density Fluctuation

### 33.1 Mission and the Sharp Question

Cycle 9 proved that $S_\tau = \bigcup_{K \in \mathbb{Z}} \tau^K \mathbb{Z}$ is dense in $\mathbb{R}$, while distinct integer layers intersect only at zero. Correctly converted continuous pointwise observables showed no off-line-specific limit defect.

The remaining canonical non-continuous arithmetic object is the prime-power jump measure:
\[
\mu = \sum_{n \ge 1} \Lambda(n) \delta_n \quad \text{on } (0, \infty).
\]
For dilation scale $h = \tau^K$ ($K \in \mathbb{Z}$), we transport $\mu$ by coordinate dilation $d_h(x) = hx$, account for the coordinate Jacobian, and examine the canonically centered half-density fluctuation.

The sharp question of Cycle 10 is:
> The Jacobian-normalized prime measures converge toward a common continuous referent ($dx$). Does the canonically centered fluctuation remain grade-compatible only when every zero satisfies $\Re(\rho) = 1/2$?

---

### 33.2 Transported Prime Measure and Arithmetic Support Separation

Under dilation $d_h(x) = hx$, the pushforward measure is:
\[
\mu_h = (d_h)_* \mu = \sum_{n \ge 1} \Lambda(n) \delta_{hn}.
\]
Its action on an admissible test function $\phi \in C_c^\infty((0, \infty))$ is:
\[
\langle \mu_h, \phi \rangle = \sum_{n \ge 1} \Lambda(n) \phi(hn).
\]
Its exact support is:
\[
\operatorname{supp}(\mu_h) = \{ h p^r : p \text{ prime}, r \ge 1 \}.
\]

#### Theorem (Arithmetic Support Separation Across Integer Grades)
*For distinct integer grades $K \ne J \in \mathbb{Z}$ and $h_K = \tau^K, h_J = \tau^J$ with $\tau = 2\pi$:*
\[
\operatorname{supp}(\mu_{\tau^K}) \cap \operatorname{supp}(\mu_{\tau^J}) = \emptyset.
\]
*Proof*: Suppose $h_K p_1^{r_1} = h_J p_2^{r_2}$. Then $\tau^{K - J} = p_2^{r_2} / p_1^{r_1} \in \mathbb{Q}$. Because $K \ne J$, $M = K - J \ne 0$. By Lindemann's theorem (1882), $\pi$ and $\tau = 2\pi$ are transcendental; hence $\tau^M$ is transcendental and cannot equal the rational number $p_2^{r_2} / p_1^{r_1}$. Therefore, prime-power supports across distinct integer grades never intersect. $\blacksquare$

---

### 33.3 Coordinate Jacobian Normalization and the Weak PNT Limit

Under coordinate dilation $d_h(x) = hx$, Lebesgue continuum measure transforms by:
\[
(d_h)_* dx = h^{-1} dx.
\]
To compare with the fixed external continuum density $dx$, the measure must be scaled by the coordinate Jacobian $h$:
\[
\nu_h = h \mu_h = h \sum_{n \ge 1} \Lambda(n) \delta_{hn}.
\]
Its action on $\phi \in C_c^\infty((0, \infty))$ is:
\[
\langle \nu_h, \phi \rangle = h \sum_{n \ge 1} \Lambda(n) \phi(hn).
\]
Its cumulative mass on $(0, X]$ is:
\[
\nu_h((0, X]) = h \sum_{hn \le X} \Lambda(n) = h \psi(X/h).
\]

#### Theorem (Unconditional Weak PNT Continuum Limit)
*As $h \to 0^+$ (i.e. $K \to -\infty$), $\nu_h \to dx$ weakly on $C_c^\infty((0, \infty))$.*
*Proof*: Let $\phi \in C_c^\infty((0, \infty))$ with support in $[a, b] \subset (0, \infty)$. By summation by parts:
\[
\langle \nu_h, \phi \rangle = h \sum_{n \ge 1} \Lambda(n) \phi(hn) = h \int_0^\infty \phi(hx) \, d\psi(x) = -\int_0^\infty h \psi(x) \phi'(hx) h \, dx = -\int_0^\infty h \psi(y/h) \phi'(y) \, dy.
\]
By the Prime Number Theorem (Hadamard & de la Vallée Poussin 1896), $\psi(y/h) = y/h + o(y/h)$ as $h \to 0^+$. Thus $h \psi(y/h) \to y$ uniformly on compact subsets of $(0, \infty)$. Integrating by parts in reverse:
\[
-\int_a^b y \phi'(y) \, dy = \int_a^b \phi(y) \, dy = \int_0^\infty \phi(y) \, dy = \langle dx, \phi \rangle.
\]
This convergence is strictly unconditional and equivalent to PNT. Off-line zeros with $\Re(\rho) < 1$ do not disturb this first-order limit. $\blacksquare$

---

### 33.4 Centred Fluctuation and Half-Density Zero Scaling

Define the signed error measure:
\[
R_h = \nu_h - dx = h \mu_h - dx.
\]
Its cumulative distribution is $R_h((0, X]) = h \psi(X/h) - X$.
By the explicit formula, a zero $\rho$ contributes to $\psi(y) - y$ as $-y^\rho / \rho$.
At cumulative level:
\[
h \frac{(X/h)^\rho}{\rho} = \frac{X^\rho}{\rho} h^{1 - \rho}.
\]
For every nontrivial zero with $\Re(\rho) < 1$, $h^{1 - \rho} \to 0$ as $h \to 0^+$, confirming compatibility with the unconditional first-order limit.

To study fluctuation at the canonical scale of the functional equation, define the half-density fluctuation:
\[
F_h = h^{-1/2} R_h = h^{-1/2}(h \mu_h - dx).
\]
Its cumulative form is:
\[
F_h((0, X]) = h^{1/2}(\psi(X/h) - X/h).
\]
For a zero $\rho = 1/2 + \delta + i\gamma$, the zero mode scales as:
\[
h^{-1/2} h^{1 - \rho} = h^{1/2 - \rho} = h^{-\delta - i\gamma}.
\]
For the discrete TC grades $h = \tau^K$:
\[
h^{1/2 - \rho} = \tau^{-K(\delta + i\gamma)}.
\]
Taking the complex modulus:
\[
|h^{1/2 - \rho}| = \tau^{-K\delta}.
\]
Behavior as $K \to -\infty$ (fine grades $h \to 0^+$):
1. **On-line zero ($\delta = 0$)**: $|\tau^{-K(0 + i\gamma)}| = 1$ identically for all $K \in \mathbb{Z}$. The mode is a pure phase of constant unit modulus.
2. **Positive displacement ($\delta > 0$)**: $|\tau^{-K\delta}| = \tau^{|K|\delta} \to \infty$ exponentially as $K \to -\infty$.
3. **Negative displacement ($\delta < 0$)**: $|\tau^{-K\delta}| \to 0$ as $K \to -\infty$.
4. **Functional Equation Quartet Symmetry**: Any off-line zero $\rho$ is paired with $1 - \rho$, having displacement $-\delta$. Therefore, any off-line quartet always contains a mode with $\delta > 0$, guaranteeing exponential growth in the fine-grade direction $K \to -\infty$.

---

### 33.5 Audit of Hypotheses H1, H2, and H3 and Regularity Corrections

| Hypothesis | Content | Status in TC | Derivation / Epistemic Origin |
| :--- | :--- | :--- | :--- |
| **H1: Forced Jacobian Normalization** | $\nu_h = h \mu_h$ is the density-compatible measure | **FORCED** | Natural coordinate transport of 1D Lebesgue measure: $(d_h)_* dx = h^{-1} dx$ |
| **H2: Canonical Symmetry Centre** | Fluctuation exponent $1/2$ selected for centering | **FORCED** | Canonical fixed point of the zeta functional equation $s \mapsto 1 - s$ |
| **H3: Grade Regularity** | Family $\{F_{\tau^K}\}_{K \in \mathbb{Z}}$ is bounded or precompact | **NOT DERIVED FROM TC** | Imposing H3 is **mathematically equivalent to the Riemann Hypothesis** |

#### Crucial Epistemic Finding & Regularity Corrections:
1. **Meaning of Boundedness**: Stating that "$\{F_h\}$ is bounded" is mathematically meaningless until the exact topology, norm, seminorm, test-function class, and quantifiers in $h$ are specified.
2. **Growth of $E(u)$ under RH**: For normalized Chebyshev error $E(u) = e^{-u/2}(\psi(e^u) - e^u)$, the Riemann Hypothesis does **not** imply $L^\infty$ boundedness. Under RH, the classical theorem of von Koch (1901) gives $\psi(x) - x = O(x^{1/2} \log^2 x)$, which corresponds to polynomial pointwise growth:
\[
E(u) = O(u^2) \quad (u \to \infty).
\]
Furthermore, by Littlewood's theorem (1914), $E(u)$ changes sign infinitely often and oscillates as $\Omega_\pm(\log\log\log u)$, confirming that $E(u)$ is never bounded on $\mathbb{R}_+$.
3. **Temperedness**: Polynomial pointwise growth $E(u) = O(u^2)$ is a sufficient condition for the locally integrable function $E(u)$ to define a regular tempered distribution $T_E \in \mathcal{S}'(\mathbb{R})$. Asserting $E \in \mathcal{S}' \iff \text{RH}$ requires careful half-line Schwartz-Laplace representation (Cycle 6 / Hörmander 7.4.2) rather than naive Tauberian inversion.
4. **Separation of Scales**: Exact TC covariance holds at each finite grade; however, uniform control over all grades $K \in \mathbb{Z}$ is an external global condition equivalent to RH that is not supplied by TC coordinate transport alone.

---

### 33.6 Smoothed Explicit Formula and Spectral Isolation

For an admissible test function $\phi \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(\phi) \subset [a, b]$ ($0 < h < a$) and entire Mellin transform $\widetilde{\phi}(s) = \int_0^\infty \phi(x) x^{s-1} dx$, the complete smoothed explicit formula evaluates to:
\[
\langle h\mu_h, \phi \rangle = h \sum_{n \ge 1} \Lambda(n) \phi(hn) = \widetilde{\phi}(1) - \lim_{T \to \infty} \sum_{|\Im(\rho)| \le T} m_\rho \widetilde{\phi}(\rho) h^{1 - \rho} - \sum_{j=1}^\infty \widetilde{\phi}(-2j) h^{1 + 2j}.
\]
*(Correction Note: The previous display in §33.6 contained two defects: (1) double-counting the background trivial-zero contribution by subtracting both the series $\sum_{j \ge 1} \widetilde{\phi}(-2j) h^{1+2j}$ and the background integral $h \int_1^\infty \frac{\phi(hx)}{x(x^2-1)} dx$, which are mathematically identical by geometric expansion of $\frac{1}{x(x^2-1)}$; exactly one representation must be used; (2) including the constant $-\frac{\zeta'(0)}{\zeta(0)} \widetilde{\phi}(0) h$, which is identically zero because $\widetilde{\phi}(s)$ is entire and $-\zeta'/\zeta$ has no pole at $s=0$. Both defects are corrected here and in Cycle 12).*

Equivalently, using the integral background representation:
\[
\sum_{j=1}^\infty \widetilde{\phi}(-2j) h^{1+2j} = h \int_1^\infty \frac{\phi(hx)}{x(x^2-1)} dx.
\]
Subtracting the Lebesgue main term $\langle dx, \phi \rangle = \int_0^\infty \phi(x) dx = \widetilde{\phi}(1)$, the half-density fluctuation pairing is:
\[
\langle F_h, \phi \rangle = h^{-1/2} (\langle h\mu_h, \phi \rangle - \langle dx, \phi \rangle) = -\lim_{T \to \infty} \sum_{|\Im(\rho)| \le T} m_\rho \widetilde{\phi}(\rho) h^{1/2 - \rho} - \sum_{j=1}^\infty \widetilde{\phi}(-2j) h^{1/2 + 2j}.
\]
Cancellation and uniqueness analysis:
- Individual off-line modes grow as $\tau^{-K\delta}$ as $K \to -\infty$.
- In finite zero models $\sum_{j=1}^r a_j q_j^K = 0$, phase cancellation across grades cannot eliminate this growth because the exponential bases $q_j = \tau^{-\delta_j - i\gamma_j}$ are **pairwise distinct** (Proposition P2 / Vandermonde cancellation), which requires only distinct bases ($q_j \ne q_\ell$), NOT individual phase irrationality (P1) or joint rational independence (P3/P4).
- In the full infinite zero sum, Ingham/Landau oscillatory theorems show that if $\Theta = \sup \Re(\rho) > 1/2$, the fluctuation oscillates with amplitude $\Omega_\pm(x^{\Theta - \varepsilon})$.
- However, establishing that this divergence persists on the discrete sequence $h = \tau^K$ without assuming RH requires external complex-analytic uniqueness theorems, not TC axioms.

---

### 33.7 Lean 4 Formalization

Seven theorems were formalized in `formal/RiemannScope/Grade.lean` under standard Mathlib foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) with zero `sorry`:
1. `half_density_scaling_exponent_complex`: $(1 - s) - 1/2 = 1/2 - s$ in $\mathbb{C}$.
2. `half_density_real_centering`: $(1/2) - (1/2 + delta) = -\delta$ in $\mathbb{R}$.
3. `half_density_cumulative_factoring`: $h\psi - X = h(\psi - X/h)$ in $\mathbb{R}$.
4. `half_density_zero_exponent_scaling`: $K(1/2 - (1/2 + \delta))\log\tau = -K\delta\log\tau$.
5. `half_density_mode_modulus`: $|\exp(x)| = \exp(x)$ for real exponents.
6. `discrete_grade_growth_of_positive_delta`: for $\tau > 1$ and $\delta > 0$, $\tau^{-K\delta}$ exceeds any finite bound $B$ for sufficiently negative $K < 0$.
7. `conditional_prime_power_support_separation`: prime-power collision across grades forces rationality of $\tau^{K-J}$.

---

### 33.8 Synthesis of Candidate TC-DISC-015 / CLM-TC-015

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-015** | **CLM-TC-015** | Prime-Measure Scaling Limit and Half-Density TC Bridge Audit | Proved pushforward transport $\mu_h$, Jacobian normalization $\nu_h = h\mu_h$, arithmetic support disjointness by transcendence of $2\pi$, weak PNT convergence $\nu_h \to dx$, zero mode scaling $h^{1/2-\rho} = \tau^{-K(\delta+i\gamma)}$, and audited H1–H3; Lean formalized 7 algebraic/exponent theorems. | **PROVED / EXACT PRESERVATION / AUDIT OF HALF-DENSITY BRIDGE** (Jacobian normalization converges weakly to $dx$ unconditionally; half-density exposes $\tau^{-K\delta}$ growth; but TC covariance does not force boundedness of $\{F_h\}$ independently of RH) |

---

# 34. Cycle 11 — TC Phase Nonresonance, Certified Incommensurability Bounds, and Cycle 10 Corrections

## 34.1 Governing Purpose and Disentanglement of Incommensurability

Transcendental Continuation begins with one prime–zeta structure represented in different units:
\[
L_K = \tau^K \mathbb Z, \quad \tau = 2\pi, \quad K \in \mathbb Z.
\]
Cycle 10 asserted that finite zero modes cannot cancel across grades because the phases $\theta_j = \frac{\gamma_j \log\tau}{2\pi}$ are "incommensurate". Cycle 11 audits this assertion, replaces imprecise language with exact propositions, establishes the logical nonresonance theorems, certifies arithmetic bounds, and audits the candidate bridge to the Riemann Hypothesis.

Define:
\[
c_\tau = \frac{\log\tau}{2\pi}, \quad \theta_j = c_\tau \gamma_j, \quad q_j = e^{-2\pi i \theta_j} = \tau^{-i\gamma_j}.
\]
We separate five distinct mathematical propositions:
1. **P1 — Single-Phase Aperiodicity**: $\theta_j \notin \mathbb{Q}$.
   - Grade consequence: Orbit $K \mapsto q_j^K$ is nonperiodic and dense in the unit circle $S^1$.
   - Status: **OPEN** (no Riemann zero ordinate is known to be rational or irrational).
2. **P2 — Pairwise Phase Distinction**: $q_j \ne q_\ell \iff \theta_j - \theta_\ell \notin \mathbb{Z}$.
   - Grade consequence: The bases $q_j$ and $q_\ell$ are distinct complex numbers.
   - Status: **CERTIFIED_WITH_EXPLICIT_BOUNDS** for all certified zeros (minimum distance to $\mathbb{Z}$ exceeds $0.004$ for first 25 zeros).
   - Weakest required condition: This is the **only condition required** for finite Vandermonde uniqueness.
3. **P3 — Homogeneous Rational Independence**: $\sum_{j=1}^r a_j \theta_j = 0$ ($a_j \in \mathbb{Z}$) implies $a_1 = \dots = a_r = 0$.
   - Grade consequence: Equivalent to homogeneous $\mathbb{Q}$-linear independence of the zero ordinates $\gamma_j$.
   - Status: **OPEN** (certified in bounded integer boxes).
4. **P4 — Joint Grade-Orbit Density**: $1, \theta_1, \dots, \theta_r$ are linearly independent over $\mathbb{Q}$.
   - Grade consequence: Required by Kronecker–Weyl for $K \mapsto (K\theta_1, \dots, K\theta_r) \pmod 1$ to be dense in the $r$-torus $\mathbb{T}^r$.
   - Status: **OPEN** (different from and stronger than homogeneous linear independence of $\gamma_j$).
5. **P5 — Zero-Index Equidistribution**: $j \mapsto \theta_j \pmod 1$ is uniformly distributed as zeros are ordered by height $\gamma_j \le T$.
   - Grade consequence: None on the grade axis $K$. This varies the zero index $j$, not the dilation grade $K$.
   - Status: **PROVED** (Hlawka 1975, Ford & Zaharescu 2005).

---

## 34.2 TC Zero-Phase Nonresonance Theorem

Using primary literature from E. Hlawka (1975) and K. Ford & A. Zaharescu (2005, *J. reine angew. Math.*):
1. **Unconditional Equidistribution**: For any fixed non-zero real $\alpha$, the sequence of fractional parts $\{\alpha \gamma_j\}$ is uniformly distributed modulo 1 across the zero index. In Weyl form:
\[
\frac{1}{N(T)} \sum_{0 < \gamma \le T} e^{2\pi i m c_\tau \gamma} \longrightarrow 0 \quad (m \in \mathbb{Z} \setminus \{0\}).
\]
2. **Ford–Zaharescu Resonant Frequencies**: In the asymptotic expansion of smooth test functions, the limiting distribution acquires non-trivial arithmetic correction measures strictly at resonant frequencies of the form:
\[
\alpha = \frac{a \log p}{2\pi q} \quad (p \text{ prime}, a, q \in \mathbb{Z}_{>0}).
\]
3. **TC Nonresonance Implication**: For the TC scale $c_\tau = \frac{\log\tau}{2\pi} = \frac{\log(2\pi)}{2\pi}$:
\[
\frac{\log\tau}{2\pi} = \frac{a \log p}{2\pi q} \iff q \log\tau = a \log p \iff \tau^q = p^a.
\]
By Lindemann's theorem (1882), $\tau = 2\pi$ is transcendental, while $p^a \in \mathbb{Z}_{>0}$ is algebraic. Therefore $\tau^q \ne p^a$ for all $q, a \ge 1$ and all primes $p$.
4. **Conclusion**: $c_\tau$ is strictly outside all resonant classes, and the limiting Ford–Zaharescu correction density vanishes identically for TC test functions.
5. **Explicit Non-Proofs**:
   - It does not prove $\theta_j \notin \mathbb{Q}$ for any particular zero $j$. (A uniformly distributed sequence may consist entirely of rational numbers).
   - It does not prove P3 or P4 (joint grade-orbit density as $K$ varies).
   - It does not exclude a hypothetical off-line zero.
   - It is a population theorem over the zero index, not yet the grade-transport bridge.

---

## 34.3 Finite Exponential Uniqueness (Vandermonde Cancellation)

Over $\mathbb{C}$, let $q_1, \dots, q_r$ be distinct nonzero complex numbers. If:
\[
\sum_{j=1}^r a_j q_j^K = 0 \quad \text{for } K = 0, \dots, r-1,
\]
then the Vandermonde matrix $V(q_1, \dots, q_r)$ is invertible because $\det V = \prod_{1 \le j < \ell \le r} (q_\ell - q_j) \ne 0$, forcing $a_1 = \dots = a_r = 0$.
- **Crucial Distinction**: This cancellation theorem requires strictly **pairwise distinct bases** (Proposition P2), **not** irrationality (P1) or linear independence over $\mathbb{Q}$ (P3/P4).
- **Application to Zero Modes**: For $q_\rho = \tau^{-(\rho - 1/2)} = \tau^{-\delta - i\gamma}$:
  - Modes with distinct displacements $\delta_1 \ne \delta_2$ have distinct moduli $|q_1| = \tau^{-\delta_1} \ne |q_2| = \tau^{-\delta_2}$ under base $\tau > 1$, so their bases can never coincide.
  - Modes on the same critical line ($\delta_1 = \delta_2$) have distinct bases whenever $\theta_1 - \theta_2 \notin \mathbb{Z}$, which is rigorously certified for all tested zeros.
- **Cycle 10 Audit**: Cycle 10 inspected finite zero truncations rather than an exact finite identity for all $K$. The finite theorem cannot be extended to the infinite explicit formula distribution without establishing uniform convergence, summation order, and distributional uniqueness.

---

## 34.4 Certified Arithmetic Bounds (N1–N4)

Using the repository's Arb / python-flint infrastructure (`flint.arb` at 256-bit certified precision):
1. **N1 — Certified Pairwise Phase Distinction**: For the first $N = 25$ certified nontrivial zeros (300 pairs), every pair satisfies $\theta_j - \theta_\ell \notin \mathbb{Z}$ with minimum distance to the nearest integer:
\[
\min_{1 \le j < \ell \le 25} \operatorname{dist}(\theta_\ell - \theta_j, \mathbb{Z}) > 4.036 \times 10^{-3} > 0.
\]
Classification: `CERTIFIED_WITH_EXPLICIT_BOUNDS`.
2. **N2 — Bounded Rational Exclusion**: For each of the first $N = 20$ certified zeros, continued-fraction convergents of the Arb ball show that for all denominators $1 \le q \le 10^6$, the rational approximation distance satisfies:
\[
\min_{1 \le q \le 10^6, p \in \mathbb{Z}} \left| \theta_j - \frac{p}{q} \right| \ge 2.05 \times 10^{-15} \gg \operatorname{rad}(\theta_j) \approx 2.4 \times 10^{-76}.
\]
Every rational with $q \le 10^6$ is strictly excluded from the certified ball. Achieved $Q \in [1.05 \times 10^6, 7.57 \times 10^6]$.
Classification: `CERTIFIED_WITH_EXPLICIT_BOUNDS`.
3. **N3 — Bounded Integer-Relation Search**:
   - For $r = 2$, exhaustive box search over $(a_1, a_2) \in [-50, 50]^2 \setminus \{(0, 0)\}$ rigorously certifies that no integer relation $a_0 + a_1 \theta_1 + a_2 \theta_2 = 0$ exists, with minimum distance $7.904 \times 10^{-5} > 0$.
   - For $r = 4$, PSLQ search at 60 dps finds no relation (`NUMERICAL_EVIDENCE_ONLY`).
4. **N4 — Zero-Index Equidistribution Diagnostics**: For $N \in \{20, 50, 100\}$ zeros, circular discrepancy $D_N^*$ decreases ($0.1509 \to 0.0639 \to 0.0419$), Weyl sums decay ($|W_1|: 0.0543 \to 0.0400 \to 0.0133$), and histogram L1 deviation from Haar measure decreases ($0.5000 \to 0.2400 \to 0.0800$).
Classification: `NUMERICAL_EVIDENCE_ONLY` (illustrates the logical theorem, does not prove it).

---

## 34.5 Audit of the TC Forbidden-Coincidence Bridge

We tested the complete candidate implication chain:
\[
\delta \ne 0 \Longrightarrow \text{exact cross-grade identity} \Longrightarrow \text{mode isolation} \Longrightarrow m\tau^K = n\tau^J \ne 0.
\]
1. $\delta \ne 0 \implies$ individual zero mode scales as $\tau^{-K(\delta + i\gamma)}$ with modulus $\tau^{-K\delta}$. (**PROVED**).
2. Mode isolation in finite linear combinations holds by Vandermonde uniqueness on distinct bases. (**PROVED**).
3. Extension to the infinite explicit formula distribution is open. (**OPEN**).
4. Derivation of an exact non-zero point coincidence $m\tau^K = n\tau^J \ne 0$: Arithmetic layers $L_K = \tau^K \mathbb{Z}$ are externally disjoint ($L_K \cap L_J = \{0\}$ for $K \ne J$). Distributional fluctuation on the continuous axis does not force point collisions across layers. (**MISSING / UNPROVED**).

**Verdict**: `TC PHASE NONRESONANCE PROVED; RH EXCLUSION BRIDGE STILL OPEN`.

---

## 34.6 Lean 4 Formalization

Four new theorems formalized in `formal/RiemannScope/Grade.lean` under standard Mathlib foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) with zero `sorry`:
1. `finite_exponential_uniqueness_2`: 2-mode Vandermonde uniqueness over $\mathbb{C}$ requiring only $q_1 \ne q_2$ (P2).
2. `finite_exponential_uniqueness_3`: 3-mode Vandermonde uniqueness over $\mathbb{C}$ requiring pairwise distinct bases.
3. `tc_log_nonresonance_scaling`: algebraic deduction that $\frac{\log\tau}{2\pi} = \frac{a\log p}{2\pi q} \implies q\log\tau = a\log p$.
4. `tc_prime_power_nonresonance_of_transcendental`: deduction that transcendence of $\tau$ implies $\tau^q \ne p^a$.
5. `mode_modulus_distinct_of_delta_ne`: displacement difference $\delta_1 \ne \delta_2$ implies distinct moduli under base $\tau > 1$.

---

## 34.7 Synthesis of Candidate TC-DISC-016 / CLM-TC-016

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-016** | **CLM-TC-016** | TC Zero-Phase Nonresonance, Certified Incommensurability Bounds, and Vandermonde Cancellation | Proved zero-index phase equidistribution and prime-power nonresonance via Hlawka (1975), Ford-Zaharescu (2005), and Lindemann (1882); proved and Lean-formalized finite Vandermonde uniqueness requiring only distinct bases (P2); certified pairwise distinction for first 25 zeros, rational exclusion for $q \le 10^6$ on first 20 zeros, and box integer relation exclusion for $|a| \le 50$ via Arb; audited TC bridge implication chain. | **TC PHASE NONRESONANCE PROVED; RH EXCLUSION BRIDGE STILL OPEN** (Zero phases are strictly nonresonant with prime powers, but grade-axis incommensurability remains open, and the infinite distributional explicit formula does not force an exact cross-grade lattice collision) |

---

# 35. Cycle 12 — Complete TC Transport, Honest Certification, and Spectral Detectability

## 35.1 Governing Mission and Soundness Repairs

Cycle 12 addresses three ordered mathematical outcomes:
1. **Soundness Repairs**:
   - **Fail-Closed Inputs (N1)**: Replaced permissive empty certificate list acceptance with strict fail-closed input verification (requiring exact zero sequences $1..N$ and valid Arb enclosures; returning `INPUT_INVALID` on missing inputs).
   - **Farey Coverage Proof (N2)**: Continued fractions midpoint heuristics lacked a coverage proof across intervals. Replaced with constructive Farey neighbor brackets: constructing $a/b < \text{lower} \le \text{upper} < c/d$ with $bc - ad = 1$ and mediant denominator $b+d > 10^6$. By the Farey mediant coverage theorem (Hardy & Wright 1979, Ch. III), every rational in $(a/b, c/d)$ has denominator at least $b+d > 10^6$, rigorously proving exclusion of all denominators $q \le 10^6$ for tested zeros.
   - **Integer Relation Witness Sign Correction (N3)**: Fixed the sign of $a_0$ in the closest integer relation output ($a_0 = 37$ with $37 - 3\theta_1 - 4\theta_2 \approx 7.904 \times 10^{-5}$, resolving the previous sign bug where residual evaluated to $\approx 74$). Added synthetic relation detection (`RELATION_FOUND`).
   - **Explicit Formula Soundness (§33.6)**: Proved that the trivial-zero series $\sum_{j \ge 1} \widetilde{\phi}(-2j) h^{1+2j}$ and background integral $h \int_1^\infty \frac{\phi(hx)}{x(x^2-1)} dx$ represent the identical contour integral (verified to $10^{-13}$). Eliminated double-counting and proved that $-\zeta'(0)/\zeta(0)$ vanishes identically on $C_c^\infty((0, \infty))$.

## 35.2 Primary Mathematical Task: Complete Smoothed TC Transport

Let:
\[
\mu = \sum_{n \ge 1} \Lambda(n) \delta_n, \quad \mu_h = (x \mapsto hx)_* \mu, \quad \nu_h = h\mu_h, \quad F_h = h^{-1/2}(\nu_h - dx).
\]
For $\phi \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(\phi) \subset [a, b]$ ($0 < h < a$), the entire Mellin transform is:
\[
\widetilde{\phi}(s) = \int_0^\infty \phi(x) x^{s-1} dx.
\]
The independently derived and numerically verified smoothed transport theorem is:
\[
h \sum_{n \ge 1} \Lambda(n) \phi(hn) = \widetilde{\phi}(1) - \sum_\rho m_\rho \widetilde{\phi}(\rho) h^{1-\rho} - \sum_{j \ge 1} \widetilde{\phi}(-2j) h^{1+2j}.
\]
Subtracting the Lebesgue main term $\widetilde{\phi}(1)$ and multiplying by $h^{-1/2}$:
\[
\langle F_h, \phi \rangle = -\sum_\rho m_\rho \widetilde{\phi}(\rho) h^{1/2-\rho} - \sum_{j \ge 1} \widetilde{\phi}(-2j) h^{1/2+2j}.
\]
When $h = \tau^{-k}$ ($k \in \mathbb{Z}$), the zero mode base is $q_\rho = \exp((\rho - 1/2)\log\tau)$.
- On-line zeros ($\rho = 1/2 + i\gamma$): $|q_\rho| = |\tau^{i\gamma}| = 1$ (bounded unitary phase).
- Off-line zeros ($\rho = 1/2 + \delta + i\gamma$, $\delta \ne 0$): $|q_\rho| = \tau^\delta \ne 1$ (exponential growth $\tau^{k\delta}$ in grade $k$).

### Numerical Verification and Error Budget:
Tested on standard bump $\phi(x) = \exp(-1/((x-2)(4-x)))$ on $[2, 4]$ with $h = 1.0 < 2.0$:
- Prime side (sieved $\Lambda(n)$): $0.40415687...$
- Spectral side ($N=75$ zeros): $0.40424922...$
- Observed residual: $9.2349 \times 10^{-5}$.
- Theoretical zero truncation tail bound (via second-derivative integration by parts): $\le 7.69 \times 10^{-4}$.
- Background discrepancy between series and integral: $8.57 \times 10^{-14}$.
- Residual lies strictly within the certified tail budget.

## 35.3 Next Theorem: Quantitative Vandermonde Block Detectability

Let $q_1, \dots, q_r$ be $r$ distinct nonzero complex bases, and $S(k) = \sum_{j=1}^r a_j q_j^k$.
Let $V$ be the $r \times r$ Vandermonde matrix with $V_{\ell j} = q_j^\ell$ ($0 \le \ell < r, 1 \le j \le r$).
Since $q_j$ are distinct, $\det V = \prod_{i < j} (q_j - q_i) \ne 0$, so $V$ is invertible.
In vector form:
\[
\mathbf{S}_r(k) = \begin{pmatrix} S(k) \\ \vdots \\ S(k+r-1) \end{pmatrix} = V \begin{pmatrix} a_1 q_1^k \\ \vdots \\ a_r q_r^k \end{pmatrix}.
\]
Inverting $V$ and taking the matrix $\infty \to \infty$ norm gives the **Quantitative Vandermonde Block Lower Bound**:
\[
\max_{0 \le \ell < r} |S(k+\ell)| \ge c(q_1, \dots, q_r) \max_{1 \le j \le r} |a_j q_j^k|, \quad \text{where } c = \frac{1}{\|V^{-1}\|_\infty} > 0.
\]
This proves that exponential growth cannot remain hidden across any block of $r$ consecutive grades.
If at least one active mode has $|q_j| = \tau^\delta > 1$, then $\max_{0 \le \ell < r} |S(k+\ell)| \to \infty$ as $k \to \infty$.

### Formal Lean 4 Verification:
Formally proved in `formal/RiemannScope/Grade.lean` under standard Mathlib axioms (`propext`, `Classical.choice`, `Quot.sound`) with zero `sorry`:
1. `vandermonde_block_reconstruction_2`: exact 2-mode reconstruction $a_1 q_1^k = (S_k q_2 - S_{k+1}) / (q_2 - q_1)$.
2. `vandermonde_block_reconstruction_2_mode2`: exact 2-mode reconstruction for mode 2.
3. `vandermonde_block_reconstruction_3`: exact 3-mode reconstruction $a_1 q_1^k = (S_{k+2} - (q_2 + q_3) S_{k+1} + q_2 q_3 S_k) / ((q_1 - q_2)(q_1 - q_3))$.

## 35.4 Infinite-Extension Detectability and Collision Analysis

We separated three propositions for infinite extension:
1. **Single Fixed Annihilating Test**: A single test $\phi \in C_c^\infty((0, \infty))$ annihilating all zeros except one is **IMPOSSIBLE** (disproved by the Paley-Wiener theorem: the Mellin transform is an entire function of exponential type; an entire function vanishing at all Riemann zeros except one violates exponential type bounds or vanishes identically).
2. **Approximate Isolation Family**: A parameterized family of test functions (Beurling-Selberg / Fejér kernels) can approximate mode isolation with quantified tail remainders (**FEASIBLE**).
3. **Distributional Uniqueness**: If $\langle F_h, \phi \rangle = 0$ for all $\phi \in C_c^\infty((0, \infty))$, then $F_h = 0$ as a Schwartz distribution, uniquely determining all spectral coefficients (**PROVED**).

### Analysis of the Collision Mechanism:
Does off-line mode growth force an arithmetic coincidence $m\tau^K = n\tau^J \ne 0$?
**NO. THE RH EXCLUSION BRIDGE REMAINS OPEN.**
Transcendental continuation is a faithful coordinate transport of the prime-zeta explicit formula across unit systems. The explicit formula holds in each unit system $L_K$. Continuous distributional fluctuations under dilation do not force the support or value of any observable to collide on discrete lattice points. The arithmetic layers $L_K = \tau^K \mathbb{Z}$ remain unconditionally disjoint ($L_K \cap L_J = \{0\}$ for $K \ne J$) by the transcendence of $\tau = 2\pi$ (Lindemann 1882).

## 35.5 Synthesis of Candidate TC-DISC-017 / CLM-TC-017

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-017** | **CLM-TC-017** | Complete Smoothed TC Transport, Quantitative Vandermonde Block Detectability, and Honest Certification | Derived and numerically verified complete smoothed explicit formula without background double-counting or phantom pole at $s=0$; proved quantitative Vandermonde block estimate $\max_{0 \le \ell < r} |S(k+\ell)| \ge c \max |a_j q_j^k|$; formalized exact 2- and 3-mode Vandermonde reconstructions in Lean 4 without extra axioms; certified bounded rational exclusion for $q \le 10^6$ via Farey coverage intervals; fail-closed Arb phase distinction and signed relation audit; audited infinite extension and collision obstruction. | **COMPLETE TC TRANSPORT DERIVED AND VERIFIED; QUANTITATIVE BLOCK DETECTABILITY PROVED; CROSS-GRADE COLLISION BRIDGE STILL OPEN** (TC faithfully transports prime-zeta identities, and off-line modes cannot hide in finite blocks; but continuous distributional fluctuation does not force discrete cross-grade lattice collisions) |

---

# 36. Cycle 13 — Reliable Certification and the Complete TC Detection Problem

## 36.1 Governing Purpose and Certification Chain Repairs

Cycle 13 establishes trustworthy finite audits, resolves prior transport error budget inconsistencies, and investigates whether detection in the complete transported explicit formula can force an off-critical zero into an arithmetic coincidence $m\tau^K = n\tau^J$.

### 1. Common Input Contract (8 Mandatory Pre-Acceptance Gates)
Implemented `load_validated_zero_certificates(cert_dir, expected_count)` enforcing:
- Gate 1: Directory accessibility and non-empty listing.
- Gate 2: Certificate count matching expected count ($N$).
- Gate 3: Contiguous 1-based indexing ($1..N$).
- Gate 4: Schema version compliance (`2.0`).
- Gate 5: Mathematical status verification (`SIMPLE_ZERO_PROVED`).
- Gate 6: Arb ball mid/rad enclosure presence and finiteness.
- Gate 7: Non-negative finite radius ($0 \le \text{rad} < 10^{-6}$).
- Gate 8: Verified provenance.
Any violation returns `INPUT_INVALID`, preventing uncertified or corrupt inputs from entering the pipeline.

### 2. Exact Rational Farey Coverage and Strict Boundaries
- Constructor `find_farey_witness_coverage` uses exact integer arithmetic via `fractions.Fraction`.
- Checks unimodular identity $bc - ad = 1$ and strict containment:
  \[
  \frac{a}{b} < x_{\text{low}} \le x_{\text{high}} < \frac{c}{d}.
  \]
- Re-verifies strict positivity against the original Arb ball enclosures.
- **Counterexample Regression**: The review counterexample $[1/49, 1/49]$ at $Q=49$ was accepted by the old float implementation because float rounding yielded $0.9999999999999999 < 1$. The exact rational constructor strictly enforces $a/b < 1/49$ and $1/49 < c/d$, correctly returning `None` and refusing to certify exclusion through denominator 49.

### 3. Fail-Closed Bounded Integer Relations
- Residual enclosure that merely contains zero returns `INCONCLUSIVE`.
- `RELATION_FOUND` is strictly reserved for an exact mathematical or certified zero residual.
- Strict non-zero separation returns `CERTIFIED_WITH_EXPLICIT_BOUNDS`.
- Floating-point evaluations without ball arithmetic return `NUMERICAL_EVIDENCE_ONLY`.
- Precision state is restored across all paths via `try...finally`.

## 36.2 Multi-Grade Complete Transport and Rigorous Error Budget

For $\phi \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(\phi) \subset [a, b]$ ($0 < h < a$), the complete explicit formula identity is:
\[
h \sum_{n \ge 1} \Lambda(n) \phi(hn) = \widetilde\phi(1) - \sum_\rho m_\rho \widetilde\phi(\rho) h^{1-\rho} - B_h(\phi),
\]
where
\[
B_h(\phi) = \sum_{j \ge 1} \widetilde\phi(-2j) h^{1+2j} = h \int_1^\infty \frac{\phi(hx)}{x(x^2-1)} \, dx.
\]

### Mathematical Refinements:
1. **Holomorphy at $s=0$**: Mellin integrand has no pole at $s=0$ because $\zeta(0) = -1/2 \ne 0$ and $\widetilde\phi$ is entire. The residue is identically zero. The product $-\zeta'(0)\widetilde\phi(0)h/\zeta(0)$ is non-zero, but does not appear in the contour shift.
2. **Background Representation and Discrepancy Resolution**: The primary representation uses the exact background integral $B_h^{\text{integral}}$. The geometric tail of the trivial-zero series for $j > M$ is bounded by:
   \[
   \sum_{j=M+1}^\infty |\widetilde\phi(-2j)| h^{1+2j} \le \|\phi\|_{L^1} \frac{(h/a)^{2M+3}}{1 - (h/a)^2}.
   \]
   For $h=1.0, a=2.0, M=15$, this bound is $\le 6.89169 \times 10^{-11}$, which strictly encloses the observed discrepancy ($8.57 \times 10^{-14}$) from Cycle 12.
3. **Stieltjes Integral Zero Truncation Bound**: Using $N(t) \le \frac{t}{2\pi}\log t$ for $t \ge 14$, the tail integral is bounded via Stieltjes integration by parts:
   \[
   \int_T^\infty t^{-2} \, dN(t) \le \frac{1}{\pi} \frac{\log T + 1}{T}.
   \]
   Together with uniform Mellin derivative bounds $C_2=31, C_3=1200, C_4=135003$ over the full critical strip $0 \le \beta \le 1$, this provides a certified spectral tail bound without assuming $\beta = 1/2$.
4. **Multi-Grade Evaluations**: Evaluated across scales $h \in \{1.0, 0.5, \tau^{-1}, \tau^{-2}\}$ ($0 < h < a = 2.0$), confirming multi-grade transport agreement.

## 36.3 Remainder-Aware Vandermonde Block Detectability

Let $Y(k) = S(k) + R(k)$ where $S(k) = \sum_{j=1}^r a_j q_j^k$ with distinct nonzero $q_j$ and remainder $R(k)$.
The block reconstruction operator satisfies the quantitative lower bound:
\[
\max_{0 \le \ell < r} |Y(k+\ell)| \ge c \max_{1 \le j \le r} |a_j q_j^k| - \max_{0 \le \ell < r} |R(k+\ell)|, \quad c = \frac{1}{\|V^{-1}\|_\infty} > 0.
\]

### Formal Lean 4 Verification:
Formally proved in `formal/RiemannScope/Grade.lean` under standard Mathlib foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) with zero `sorry`:
1. `vandermonde_block_remainder_2`: exact 2-mode reconstruction with remainder $a_1 q_1^k = \frac{(Y_k - R_k)q_2 - (Y_{k+1} - R_{k+1})}{q_2 - q_1}$.
2. `vandermonde_block_remainder_2_mode2`: exact mode 2 reconstruction with remainder.
3. `vandermonde_block_remainder_3`: exact 3-mode reconstruction with remainder.
4. `reconstruction_remainder_lower_bound`: real triangle inequality lower bound establishing that $|Y_k| + |Y_{k+1}| \ge c |S_k| - (|R_k| + |R_{k+1}|)$.

### Regimes Tested:
- **Zero Remainder**: $R \equiv 0 \implies \max |Y| \ge c \max |a_j q_j^k| > 0$.
- **Subordinate Remainder**: $\max |R| \le 0.05 \ll c \cdot S \implies \max |Y| > 0$ strictly detected.
- **Dominant Remainder**: $\max |R| = 1.0 > c \cdot S \implies$ lower bound $\le 0$, detection masked.

## 36.4 Infinite Extension Obstructions & The Unbridged TC Bridge

1. **Synthetic Aliasing Control**: If $\Delta\gamma = 2\pi/\log\tau \approx 5.88488$, then $\tau^{i\Delta\gamma} = 1$, making $q_1 = q_2$. The Vandermonde matrix becomes singular ($c = 0$). Mode non-aliasing is an essential premise; pairwise distinction holds for the certified finite set of zeros, but cannot be inferred universally without zero-spacing theorems.
2. **Paley-Wiener / Jensen Non-Annihilation**: A single non-trivial test function $\phi \in C_c^\infty((0, \infty))$ cannot annihilate all nontrivial zeros except one. By Paley-Wiener, $\widetilde\phi$ is an entire function of exponential type, whose zero counting function satisfies $n(r) = O(r)$, whereas the Riemann zero counting function satisfies $N(r) \sim \frac{r}{\pi}\log r \gg O(r)$.
3. **Distributional Uniqueness vs Discrete Synthesis**: While $T = 0 \in \mathcal{D}' \iff \langle T, \phi \rangle = 0$ for all tests, this continuous property does not force exponential mode growth $\tau^{k\delta}$ into discrete lattice collisions.
4. **Layer Disjointness Obstruction**: Integer arithmetic layers $L_K = \tau^K \mathbb{Z}$ are unconditionally disjoint ($L_K \cap L_J = \{0\}$ for $K \ne J$) by the transcendence of $\tau = 2\pi$ (Lindemann 1882). However, the target bridge:
   \[
   \exists\rho (\Re\rho \ne 1/2) \Longrightarrow \exists K \ne J, m, n \in \mathbb{Z}\setminus\{0\} : m\tau^K = n\tau^J
   \]
   remains completely unproved. Deriving it would prove the Riemann Hypothesis. Neither coordinate covariance nor arithmetic separation supplies this implication.

## 36.5 Synthesis of Candidate TC-DISC-018 / CLM-TC-018

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-018** | **CLM-TC-018** | Reliable Certification, Multi-Grade Complete Transport, and Remainder-Aware Vandermonde Detection | Established 8-gate certificate loading; exact rational Farey coverage with strict bounds and Arb verification; regression of $[1/49, 1/49]$ counterexample at $Q=49$; fail-closed bounded relations; verified complete transport across multiple grades with Stieltjes zero bounds and geometric background tail bounds (resolving Cycle 12 discrepancy); proved remainder-aware Vandermonde block detectability and formalized 2- and 3-mode reconstructions with lower bounds in Lean 4 without extra axioms; analyzed synthetic aliasing control, Paley-Wiener obstruction, and layer disjointness. | **RELIABLE CERTIFICATION ESTABLISHED; MULTI-GRADE TRANSPORT VERIFIED; REMAINDER-AWARE DETECTABILITY FORMALIZED; ARITHMETIC COINCIDENCE BRIDGE STILL OPEN** (Finite audits are trustworthy and transport error budgets are closed; but continuous explicit formula fluctuations do not force discrete cross-grade point collisions) |

---

# 37. Cycle 14 — TC Test-Family Investigation, Complex Remainder Formalization, and Certification Repairs

## 37.1 Governing Purpose and Evidence Gap Closures

Cycle 14 executes the mandatory evidence repairs identified in the Cycle 13 review and conducts a rigorous investigation of an explicit test family in the complete Transcendental Continuation explicit formula.

### 1. Robust 8-Gate Certificate Loading and Canonical Self-Hash Validation
- Validated certificate loader `load_validated_zero_certificates(cert_dir, expected_count)` strictly enforces:
  1. Directory presence and readability.
  2. Exact certificate file count.
  3. Contiguous 1-based indexing (`zero_00001.json` .. `zero_00025.json`).
  4. Explicit schema version `2.0`.
  5. Mathematical status `SIMPLE_ZERO_PROVED`.
  6. Finite midpoint and radius components for both real and imaginary enclosures.
  7. Non-negative radius with precision sanity ($0 \le \text{rad} < 10^{-6}$).
  8. Canonical SHA-256 self-hash verification (excluding `sha256_hash` field).
- Any violation triggers immediate fail-closed rejection (`INPUT_INVALID`) with descriptive logging. No consumer may promote unvalidated reference decimals or fallback uncertified files to certified status.
- Global Arb precision is guaranteed to restore across all execution branches via `try ... finally`.

### 2. Certified Outward Distance Bounds for Integer Relations
- `audit_bounded_integer_relations` computes signed outward lower bounds on distance to the nearest integer:
  \[
  \text{dist}_{\mathbb{Z}}(X) \ge \min_{k \in \mathbb{Z}} \operatorname{lower\_bound}(|X - k|).
  \]
- Replaces optimistic floating-point approximations with certified Arb ball interval boundaries.
- Retains three-tier status:
  - `RELATION_FOUND`: strictly reserved for exact mathematical or certified zero residual.
  - `INCONCLUSIVE`: interval contains zero but is not certified exact zero.
  - `CERTIFIED_WITH_EXPLICIT_BOUNDS`: certified strictly separated from zero across all checked coefficients.

### 3. Exact Farey Coverage Exclusion Semantics
- Clarified denominator threshold semantics: a Farey bracket $[a/b, c/d]$ satisfying $bc - ad = 1$ and $b + d > Q$ proves exclusion of all rationals with denominator $q \le Q$ in the open interval $(a/b, c/d)$. It does *not* prove exclusion of the mediant denominator $b + d$.

## 37.2 Delimited Transport Certification and Rigorous Tail Bounds

The complete explicit formula for $\phi \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(\phi) \subset [a, b]$ ($0 < h < a$) is:
\[
P_h(\phi) := h \sum_{n \ge 1} \Lambda(n)\phi(hn) = \widetilde\phi(1) - \sum_\rho m_\rho \widetilde\phi(\rho)h^{1-\rho} - B_h(\phi),
\]
where $B_h(\phi) = h \int_1^\infty \frac{\phi(hx)}{x(x^2-1)} \, dx = \sum_{j \ge 1} \widetilde\phi(-2j)h^{1+2j}$.

### 1. Tail Bound Resolution and Enclosure
- **Background Trivial-Zero Series Tail**: For $j > M$,
  \[
  \left|\sum_{j > M} \widetilde\phi(-2j)h^{1+2j}\right| \le \|\phi\|_{L^1} \frac{(h/a)^{2M+3}}{1 - (h/a)^2}.
  \]
  For $a = 2.0, h = 1.0, M = 15$, $\|\phi\|_{L^1} \approx 0.4439938$, yielding:
  \[
  \text{Tail}_{bg}(15) \le 6.891691066 \times 10^{-11}.
  \]
  The observed discrepancy between the numerical integral and the $M=15$ series ($8.57 \times 10^{-14}$) is rigorously enclosed within this bound.
- **Nontrivial Zero Truncation via Trudgian (2012)**:
  By Theorem 1 and Corollary 1 of Trudgian (2012/2014), $N(t) \le \frac{t}{2\pi}\log t$ for $t \ge t_0 \approx 168\pi$. For $p > 1$, Stieltjes integration by parts yields:
  \[
  \int_{(T, \infty)} t^{-p} \, dN(t) = \left[ t^{-p} N(t) \right]_T^\infty + p \int_T^\infty t^{-p-1} N(t) \, dt \le \frac{p}{2\pi} \frac{(p-1)\log T + 1}{(p-1)^2 T^{p-1}},
  \]
  dropping the non-positive boundary term $-T^{-p}N(T) \le 0$.
- **Epistemic Delimitation**:
  While tail bounds are rigorous, the Mellin derivative constants $C_2=31, C_3=1200, C_4=135003$ and finite quadrature evaluations rely on high-precision numerical quadrature without certified ball enclosures. Therefore, transport is classified as `EMPIRICAL_QUADRATURE_WITH_RIGOROUS_TAIL_BOUNDS`, honestly delimiting its status.

## 37.3 Formal Complex Norm Remainder Lower Bound in Lean 4

In `formal/RiemannScope/Grade.lean`, the complex triangle inequality lower bound is formally proved:
- **Theorem `complex_reconstruction_remainder_lower_bound`**:
  For $M, Y_{\text{est}}, R_{\text{est}} \in \mathbb{C}$, if $M = Y_{\text{est}} - R_{\text{est}}$, then
  \[
  |M| - |R_{\text{est}}| \le |Y_{\text{est}}|.
  \]
  Proved using `Complex.abs.add_le` and `Complex.abs.map_neg` without extra axioms.
- **Theorem `vandermonde_2_reconstruction_bound`**:
  Connects `vandermonde_block_remainder_2` to the complex triangle lower bound, formalizing the 2-mode reconstruction lower bound:
  \[
  |Y_k \cdot q_2 - Y_{k+1}| \ge |a_1 q_1^k (q_2 - q_1)| - |R_k \cdot q_2 - R_{k+1}|.
  \]
  Mathlib foundational axioms only (`propext`, `Classical.choice`, `Quot.sound`); 0 `sorry`, 0 `admit`.

## 37.4 Explicit Mellin Test-Family Investigation

### 1. Concrete Candidate Family Definition
Let $w_0(v) = \exp\left(-\frac{1}{1 - 16(v - 3/2)^2}\right) \mathbf{1}_{|v - 3/2| < 1/4}$ and $I_0 = \int_{1.25}^{1.75} w_0(v) \, dv \approx 0.1110196$.
The normalized bump $w(v) = w_0(v)/I_0 \in C_c^\infty((1, 2))$ satisfies $\int_1^2 w(v) \, dv = 1$.
For $L > 0$ and target zero $\rho_0$, define:
\[
\phi_{L, \rho_0}(x) = \frac{1}{L} x^{-\rho_0} w\left(\frac{\log x}{L}\right), \quad x > 0.
\]
Support lies in $[e^L, e^{2L}] \subset (0, \infty)$. The Mellin transform is:
\[
\widetilde\phi_{L, \rho_0}(s) = \int_1^2 w(v) e^{L(s - \rho_0)v} \, dv.
\]
At $s = \rho_0$, $\widetilde\phi_{L, \rho_0}(\rho_0) = \int_1^2 w(v) \, dv = 1.0$ identically.

### 2. Decisive Remainder Ratio $\eta(L, k, F)$
The detection criterion compares the reconstruction remainder to the target mode signal:
\[
\eta(L, k, F) = \frac{\max_{0 \le \ell < r} |R_{L, F}(k+\ell)|}{c_F \max_j |a_j(L) q_j^k|}.
\]
For target $\rho_0 = 1/2 + 14.1347i$ paired with conjugate $\bar\rho_0$, $c_F = |\sin(\gamma_0 \log\tau)| \approx 0.7481$.
- At $L = 0.5$: $\eta \approx 2.67 > 1$ (remainder dominant; inconclusive).
- At $L = 1.0$: $\eta \approx 1.91 > 1$ (remainder dominant; inconclusive).
- At $L = 2.0$: $\eta \approx 0.4986 < 1$ (**target mode strictly detected**).
- At $L = 5.0$: $\eta \approx 0.0400 \ll 1$ (**strong spectral isolation on known critical zeros**).

### 3. Adversarial Competitor Analysis
Consider a hypothetical off-critical competitor $\rho_{\text{comp}} = 0.75 + 21.022i$ with $\Re\rho_{\text{comp}} > \Re\rho_0 = 0.5$.
The competitor amplitude scales as:
\[
|\widetilde\phi_{L, \rho_0}(\rho_{\text{comp}})| = \left|\int_1^2 w(v) e^{L(0.25 + i\Delta\gamma)v} \, dv\right| \ge e^{1.25 \cdot 0.25 L} \cdot \left|\widehat{w}\right|.
\]
- At $L = 10.0$: competitor amplitude is $\approx 0.2104$.
- At $L = 20.0$: competitor amplitude grows to $\approx 2.9566 > c_F \approx 0.7481$, driving $\eta > 3.95$.
- As $L \to \infty$, competitor amplitude diverges exponentially as $e^{1.25 L \Delta\beta} \to \infty$.
- **Finding**: While scaling $L$ suppresses known on-line zeros ($\Re\rho = 1/2$), any off-line zero to the right ($\Re\rho > \Re\rho_0$) experiences exponential amplification. Hence test-family parameter scaling alone cannot isolate a target zero without an a priori zero-free region.

## 37.5 Paley-Wiener / Jensen Zero Density Obstruction

1. **Farmer (1995) / Conrey (1989)**:
   At least $40\%$ of the zeros of $\zeta(s)$ are simple and on the critical line:
   \[
   N_{\text{distinct}}(T) \ge \frac{0.40}{2\pi} T \log T.
   \]
2. **Jensen's Formula for Entire Functions of Exponential Type**:
   For $\phi \in C_c^\infty((a, b))$, $\widetilde\phi(s)$ is entire of exponential type $\tau_0 = \log(b/a)$.
   The number of zeros $n(r)$ of $\widetilde\phi$ in $|s| \le r$ obeys $n(r) = O(r)$.
3. **Impossibility of Finite Annihilation**:
   Because $\lim_{T \to \infty} \frac{N_{\text{distinct}}(T)}{T} = \infty$ while $n(r)/r = O(1)$, no single fixed non-zero test $\phi \in C_c^\infty((0, \infty))$ can annihilate all but finitely many distinct zeta zeros.
4. **Decoupling of Distributional Uniqueness and Discrete Synthesis**:
   Distributional uniqueness in $\mathcal{D}'((0, \infty))$ is established (if $\langle T, \phi \rangle = 0$ for all $\phi$, then $T = 0$). However, discrete spectral synthesis (reconstructing infinite individual zero amplitudes from finite grade blocks) remains unproved due to potential dense ordinate aliasing and unverified zero spacing.

## 37.6 Persistent Open Arithmetic Collision Bridge

The core research question of Transcendental Continuation is:
\[
\text{nontrivial off-critical zero } \rho \ (\Re\rho \ne 1/2) \overset{?}{\Longrightarrow} \exists K \ne J, m, n \in \mathbb{Z}\setminus\{0\}: m\tau^K = n\tau^J.
\]
The Cycle 14 investigation establishes:
1. **Lattice Separation**: $L_K \cap L_J = \{0\}$ for $K \ne J$ is unconditionally true by the transcendence of $\tau = 2\pi$ (Lindemann 1882).
2. **Explicit Formula Transport**: The explicit formula holds identically at each grade $h = \tau^K$, preserving prime-zeta structure.
3. **Bridge Obstruction**: The observable $Y_\phi(k) = h_k^{-1/2}(\widetilde\phi(1) - P_{h_k}(\phi) - B_{h_k}(\phi))$ is a continuous functional of the test $\phi$, taking values in $\mathbb{C}$. No known prime-zeta law projects $Y_\phi(k)$ onto the discrete lattice $L_K = \tau^K \mathbb{Z}$. Consequently, off-line exponential growth of $Y_\phi(k)$ does not force an arithmetic collision $m\tau^K = n\tau^J$.
4. **Epistemic Verdict**: Establishing finite Vandermonde detectability or mode growth does not bridge continuous analytic fluctuations to discrete lattice collisions. The derivation of the arithmetic coincidence remains **COMPLETELY OPEN**.

## 37.7 Synthesis of Candidate TC-DISC-019 / CLM-TC-019

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-019** | **CLM-TC-019** | TC Test-Family Investigation, Complex Remainder Formalization, and Certification Repairs | Validated 8-gate certificate loading with canonical SHA-256 self-hash and fail-closed propagation; certified outward integer distance via signed Arb balls; verified exact Farey coverage semantics ($b+d > Q$); resolved background tail bound ($\le 6.89169 \times 10^{-11}$) enclosing observed discrepancy; formalized complex triangle remainder lower bound in Lean 4 without extra axioms; demonstrated on-line detection ($\eta(2.0) \approx 0.4986, \eta(5.0) \approx 0.0400$) and proved adversarial competitor blowup ($\Re\rho_{\text{comp}} > \Re\rho_0 \implies \eta \to \infty$) for normalized bump family $\phi_{L,\rho_0}$; established Paley-Wiener / Jensen zero density obstruction via Farmer (1995) / Conrey (1989); audited open arithmetic collision bridge ($L_K \cap L_J = \{0\}$). | **EVIDENCE REPAIRS COMPLETED; TEST-FAMILY BEHAVIOR CHARACTERIZED; COMPLEX DETECTABILITY FORMALIZED; ARITHMETIC COINCIDENCE BRIDGE REMAINS OPEN** (Finite audits are strictly certified; test family isolates on-line zeros but competitor blowup obstructs universal isolation; continuous explicit-formula fluctuations do not force discrete cross-grade lattice collisions) |

---

# 38. Autonomous TC Mechanism Discovery Epic — Starting State Reconciliation, Lean Formalization, Whole-Spectrum Isolation, and Arithmetic Bridge Audit

## 38.1 Starting State Reconciliation & Review Questions Resolution

1. **Quoted Integer-Grade Theorem Source Reconciliation**:
   - In `formal/RiemannScope/Grade.lean` (line 903), the source theorem `vandermonde_2_reconstruction_bound` was declared as `theorem vandermonde_2_reconstruction_bound (q₁ q₂ : ℂ) (a₁ a₂ : ℂ) (k : ℕ) (hq : q₂ - q₁ ≠ 0) ...`. The source already had `k : ℕ` and `hq : q₂ - q₁ ≠ 0`. The walkthrough text had misquoted it as `k : ℤ` and omitted the non-degeneracy condition `hq`.
   - In addition, integer-grade theorems for $k : \mathbb{Z}$ were formally proved in Lean 4: `vandermonde_block_remainder_2_zpow` and `vandermonde_2_reconstruction_bound_zpow` with explicit non-zero base hypotheses `hq1 : q₁ ≠ 0` and `hq2 : q₂ ≠ 0`, resolving Mathlib's totalized division behavior where $0^{-1} = 0$.
2. **Intermediate Tail Domain & Coarse Counting**:
   - The coarse upper bound $N(t) \le \frac{t}{2\pi} \log t$ holds unconditionally for all $t \ge 14.0$ (Lehman 1966; Backlund 1918; Trudgian 2014, Corollary 1).
   - At the 75-zero cutoff $T = \gamma_{75} \approx 192.026$, $N(192.026) = 75 < \frac{T}{2\pi}\log T \approx 160.68$, providing a safety margin of $85.68$ zeros. The intermediate interval $[192.03, 527.79]$ is fully covered with zero unaccounted gap.
3. **Exact Recomputed Constants**:
   - Normalization integral $I_0 = \int_{-1/4}^{1/4} \exp(-1/(1 - 16u^2)) \, du = 0.11099845404201986...$ via exact substitution $v = 4u$.
   - Geometric trivial-zero background tail bound for $M = 35$ at $h = 1.0, a = 2.0$:
     \[
     |\text{Tail}_{\text{bg}}(35)| \le \|\phi\|_{L^1} \frac{(h/a)^{73}}{1 - (h/a)^2} \le 6.2679565 \times 10^{-23}.
     \]

## 38.2 Formal Lean 4 Theorems (193 Compiled Targets)

Three new foundational theorems were proved in `formal/RiemannScope/Grade.lean` using only standard Mathlib foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) with zero `sorry`:
1. `vandermonde_block_remainder_2_zpow`: Proves the exact 2-mode reconstruction identity for all integer grades $k \in \mathbb{Z}$, with nonzero base hypotheses $q_1 \ne 0, q_2 \ne 0, q_2 - q_1 \ne 0$.
2. `vandermonde_2_reconstruction_bound_zpow`: Proves the integer-grade reconstruction norm lower bound $|M| - |R_{\text{est}}| \le |Y_{\text{est}}|$ for all $k \in \mathbb{Z}$.
3. `gaussian_exponent_band_bound`: Proves via nonlinear arithmetic that for all $|\sigma| \le 1$ and $|\tau_0| \ge 3$, $\sigma^2 + 6\sigma - \tau_0^2 \le -2$, ensuring $\Re(L z^2 + 6L z) \le -2L$ outside the canceled spectral band.

## 38.3 Track 1: Whole-Spectrum Log-Gaussian Spectral Isolation (Section 7E)

1. **Test-Family Construction**:
   For target nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ ($0 < \beta_0 < 1$), define $C = \{\rho \ne \rho_0 : |\Im\rho - \Im\rho_0| \le 3\}$. By compactness of $[0, 1] \times [\gamma_0 - 3, \gamma_0 + 3]$, $C$ is finite.
   Define the cancellation polynomial:
   \[
   P(z) = \prod_{\rho \in C} \left(1 - \frac{z}{\rho - \rho_0}\right).
   \]
   Let $g_L(t) = \frac{1}{c_L \sqrt{4\pi L}} \exp\left(-\frac{(t - 6L)^2}{4L}\right) \chi(t/L)$ with $\chi \in C_c^\infty((1, 17))$ equal to $1$ on $[2, 16]$.
2. **Cutoff Error & Normalization**:
   - Cutoff tail error: $\sup_{|\sigma| \le 1} \|\partial_t^p (e^{\sigma t} r_L(t))\|_{L^1} \le C_{p, \chi} L^{-1/2} e^{-2L}$.
   - Normalization error: $|1 - c_L| \le \frac{1}{2\sqrt{\pi L}} e^{-4L}$.
   - Support threshold: $\operatorname{supp}(\phi_L) \subset [e^L, e^{17L}]$ satisfies $0 < h_k < e^L$ for all $k \in I$ once $L > \max(0, -\min(I) \log\tau)$.
3. **Whole-Spectrum Limit & Quantifier Scoping**:
   \[
   \forall \rho_0 \in Z(\zeta) \, (0 < \Re\rho_0 < 1), \; \forall I \subset \mathbb{Z} \text{ (finite)}, \; \forall \varepsilon > 0, \; \exists L > 0 : \max_{k \in I} |Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k| < \varepsilon.
   \]
   - *Refutation of Dependency Jump $D \to E$*: Convergence on every fixed finite grade block does *not* establish growth or divergence of a single fixed observable under transport. Counterexample: for $q > 1$, $Y_L(k) = q^k e^{-k^2/L}$ converges uniformly to $q^k$ on every compact $k$-block as $L \to \infty$, yet for every fixed $L$, $Y_L(k) \to 0$ as $k \to \infty$. The graph step $D \to E$ is an unsupported quantifier leap and is refuted.
   - *Tail Bound Applicability vs Completeness*: Trudgian (2014 Cor. 1) unconditionally certifies that the Stieltjes tail integral applies above cutoff $T \approx 192.026$. However, finding 75 zeros beneath $\sim 160.68$ certifies tail applicability, but does *not* certify consecutive zero completeness below $T$; completeness remains an open Turing obligation.
   - *Sampling Caveat*: Sampled values at $L=2, 5$ do not certify $\eta < 1$ for all $L \ge 2$; universal boundedness is established by the complete analytic theorem and the Lean-proved band exponent bound.
   - *Paley-Wiener / Jensen*: Precludes a fixed test from annihilating all but finitely many distinct zeros (Farmer 1995).

## 38.4 Track 2: Arithmetic Measure Pushforward, Atom Extraction, & Disjointness (Section 8)

1. **Measure Pushforwards & Formula Pairing**:
   $\mu_K = (D_{\tau^K})_* \mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}$. For $h = \tau^{-k}$, $P_h(\phi) = h \langle \mu_{-k}, \phi \rangle$ ($K = -k$).
   - *Non-multiplicativity of $\Lambda$*: The von Mangoldt function is non-multiplicative ($\Lambda(6) = 0 \ne \Lambda(2)\Lambda(3) > 0$). The Euler product enters exclusively via $-\zeta'/\zeta(s) = \sum \Lambda(n) n^{-s}$.
   - *Nontrivial Zero Restriction*: The opening bridge formula must specify nontrivial zeros ($0 < \Re\rho < 1$); trivial zeros like $\rho = -2$ produce no off-line RH counterexample.
2. **Layer Disjointness (Lindemann 1882)**:
   $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$ for all $K \ne J$ because $\tau^{K-J} \notin \mathbb{Q}$.
3. **Atom Extraction Limit & Station-Level Limit**:
   Under shrinking test localization $\psi_{x, \varepsilon}(t) = \psi((t - x)/\varepsilon)$:
   - Prime powers yield delta atoms: $\lim_{\varepsilon \to 0} \langle \mu_K, \psi_{x, \varepsilon} \rangle = \Lambda(n) \delta_{x, \tau^K n}$.
   - Finite zero modes integrate to $O(\varepsilon) \to 0$. Discrete atomic masses $\Lambda(n)\delta_{x, \tau^K n}$ emerge exclusively from the complete infinite spectral sum where the limit $\varepsilon \to 0$ and the sum $\sum_\rho$ cannot be interchanged.
   - An off-line zero $\rho_0$ contributes a smooth $C^\infty$ background with empty singular support; it cannot shift existing delta atoms or force station collisions across disjoint layers $L_K$ and $L_J$.
4. **Candidate Bridge Controls & Status**:
   All 6 controls pass (unit conversion, linearity, distribution, prime-power, off-line, object). Mode isolation in continuous explicit-formula functional $Y_{\phi_L}(k)$ does not project values into the discrete lattice $L_K = \tau^K \mathbb{Z}$. The TC arithmetic coincidence bridge remains strictly **OPEN**.

## 38.5 Independent Research-Agent Loops & Synthesis of Candidate TC-DISC-020 / CLM-TC-020

Three independent research-agent loops were executed and persisted:
1. **Spectral Analyst**: Complete analytic whole-spectrum isolation proof with cutoff derivative estimates and limit interchanges in `research/epic/spectral_isolation_analytic_proof.md`.
2. **Arithmetic Researcher**: Atomic support and station-level localization limits under shrinking tests in `research/epic/arithmetic_spectral_atomic_limit.md`.
3. **Adversarial Challenger**: Counterexample audit, quantifier enforcement ($D \not\to E$), and overstatement extirpation in `research/epic/adversarial_challenger_review.md`.

| Candidate ID | Claim ID | Name | Mathematical Status | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DISC-020** | **CLM-TC-020** | Autonomous TC Mechanism Discovery Epic Synthesis | Starting state reconciled; integer-grade Vandermonde reconstruction (`k:Int`, $q_1, q_2 \ne 0$) and Gaussian band exponent bound proved in Lean 4 (193 compiled targets, 0 sorry); Lehman/Trudgian coarse counting bounds verified for $t \ge 14.0$; whole-spectrum log-Gaussian isolation $\lim_{L \to \infty} \max_{k \in I} |Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k| = 0$ established with proved cutoff decay; $D \to E$ jump refuted via $Y_L(k) = q^k e^{-k^2/L}$; arithmetic measure pushforward pairing $P_h(\phi) = h \langle \mu_{-k}, \phi \rangle$ verified; layer disjointness $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$ confirmed via Lindemann; atomic support localization limits derived; 6 bridge controls evaluated and passed; arithmetic coincidence bridge audited. | **EPIC DELIVERABLES FULLY EXECUTED; WHOLE-SPECTRUM ISOLATION PROVED; ARITHMETIC COINCIDENCE BRIDGE STRICTLY OPEN** (Integer-grade bounds and band exponents are formally proved; whole-spectrum isolation circumvents Paley-Wiener via dynamic scaling; continuous observable growth does not force discrete lattice point collisions $m\tau^K = n\tau^J$; RH exclusion bridge remains open) |
