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

## 24.6 Schedule Covariance, Exact Remainder Cancellation, and The Actual Question
### Schedule Covariance Classification
Under origin coordinate dilation \(s_K = \tau^K s\) (\(z_K = \tau^K(s-1/2)\)), ordinate scales as \(t_K = \tau^K t \implies t' = \tau t\). Covariance of height truncation \(H\) requires:
\[
\boxed{H(\tau T) = \tau H(T), \quad \tau = 2\pi.}
\]
- **General Solution (Paper Proved)**: \(H(T) = T \cdot q(\log_\tau T)\) with \(q : \mathbb R \to (0, \infty)\) 1-periodic.
- **Asymptotic Limit Collapse (Paper Proved)**: If \(\lim_{T\to\infty} H(T)/T\) exists and \(\tau > 1\), \(H(T) = cT\).
- **Selection Condition**: Unproved heuristic note; remainder bounds do not force \(c \ge 1\) by proved estimate alone.
- **Falsified Premise**: *"Bilateral discrete grade covariance uniquely determines the cofinal schedule."*

### Exact Remainder Cancellation Theorem & Candidate Collapse
Let \(Z_H(t) = \sum_{|\gamma_j| \le H} (\dots)\) and \(R_H(t) = \frac{\Xi'}{\Xi}(\sigma - 1/2 + it) - Z_H(t)\).
Then:
\[
\forall t, \quad Z_H(t) + R_H(t) \equiv \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right).
\]
Consequently, \(\mathcal S_T(Z_H; R_H) = \frac{1}{2\pi}\int_{-T}^T W_T(t) |Z_H(t) + R_H(t)|^2 dt \equiv \frac{1}{2\pi}\int_{-T}^T W_T(t) |\Xi'/\Xi|^2 dt\) is **identically independent of \(H\) and \(H(T)\)**.
- **Case A (Recomputed Remainder)**: \(Z_{H,\delta} + R_{H,\delta} \equiv F_\delta\) (collapses to full function, \(H\)-independent).
- **Case B (Fixed Unperturbed Remainder)**: \(Z_{H,\delta} + R_{H,0} = F_0 + (Z_{H,\delta} - Z_{H,0})\), which reduces by additive-reference invariance to the **finite raw Fejér response** (`FAIL_RADIAL_POSITIVITY`).
- **Classification**: `COLLAPSED_COFINAL_IDENTITY` / `FAIL_RADIAL_POSITIVITY`.

### The Actual Question & Open Obligation
The noncommutation defect between finite truncation and infinite completion is:
\[
\mathcal D = \mathcal R_{\mathrm{op}}(Z_\infty) - \lim_{H\to\infty} \mathcal R_{\mathrm{op}}(Z_H).
\]
Constructing a genuinely non-additive cofinal boundary functional that is neither algebraically collapsed nor trivially vanishing is the exact open mathematical obligation for Gate G4 (`OBL-CMSA-003-G4-BOUNDARY`).
Status: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
