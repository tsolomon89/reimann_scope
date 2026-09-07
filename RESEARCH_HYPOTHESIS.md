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
   E(u) = O\left(e^{u/2} \exp\left(-c \frac{u^{3/5}}{(\log u)^{1/5}}\right)\right).
   \]
   Because the sub-exponential decay cannot cancel $e^{u/2}$, **$E(u)$ has exponential growth unconditionally**, growing as $e^{u/2 - o(u)}$ as $u \to +\infty$. It is unconditionally non-tempered in $\mathcal{S}'(\mathbb{R})$.
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










