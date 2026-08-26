# Decisions Log

Append-only record of consequential mathematical, numerical, provenance, and architectural decisions for `reimann_scope`.

Do not use this file for ordinary coding notes.

A decision belongs here only if changing it later would alter:

- mathematical semantics;
- transformation definitions;
- research interpretation;
- numerical trust;
- data provenance;
- formalization boundaries;
- core application architecture.

The current canonical documents remain authoritative for present behavior.

---

## Decision template

```text
## YYYY-MM-DD — Short title

Status: ACCEPTED | SUPERSEDED

Decision:
...

Reason:
...

Mathematical / operational consequence:
...

Supersedes:
...
```

---

## 2026-08-19 — Minimal research-instrument architecture

Status: ACCEPTED

Decision:

Use a Python-first application, preferably Plotly Dash, with the mathematical engine and UI kept in one small codebase.

Reason:

The application is an interactive mathematical instrument, not a production SaaS product. A separate frontend/API architecture would add unnecessary indirection and make the mathematics harder to audit.

Mathematical / operational consequence:

The path from UI control to transformation object to numerical evaluation should remain easy to trace.

Supersedes:

None.

---

## 2026-08-19 — Transform classes remain explicit and separate

Status: ACCEPTED

Decision:

Camera, height sampling, origin coordinate dilation, centered coordinate dilation, zeta argument transforms, kernel transforms, and non-holomorphic deformations remain different named operations.

Reason:

Different notions of scaling can become conflated.

Mathematical / operational consequence:

Every active mode must generate its mathematics card from the same object used by the evaluator.

Supersedes:

None.

---

## 2026-08-19 — Reference zeros are validation-only for discovery validation

Status: ACCEPTED

Decision:

External reference zeros must not seed a baseline zero finder when that run is intended to validate independent discovery.

Reason:

The app must demonstrate independent construction/refinement before comparison with trusted external data.

Mathematical / operational consequence:

Validation is discovery-first, comparison-second.

This does not prohibit separately labeled high-zero `research_input` blocks for structural experiments.

Supersedes:

None.

---

## 2026-08-19 — Analytic continuation is authoritative in the critical strip

Status: ACCEPTED

Decision:

Do not use the raw Dirichlet series

\[
\sum n^{-s}
\]

as the numerical definition of zeta inside the critical strip.

Reason:

The series does not converge there.

Mathematical / operational consequence:

Kernel transformations may be derived from Dirichlet-series algebra where valid, but critical-strip values use the analytically continued function from a trusted high-precision implementation.

Supersedes:

None.

---

## 2026-08-19 — Tau is the project-facing full-turn scale

Status: SUPERSEDED

Decision:

Use

\[
\tau=2\pi
\]

as the default scale base, without assuming it is a nontrivial zeta symmetry.

Reason:

Tau is the project-facing rotational scale.

Mathematical / operational consequence:

Tau transformations remain explicit and claimed invariances must be derived or experimentally tested.

Supersedes:

None.

Superseded by:

`2026-08-21 — Tau is the canonical transcendental-continuation generator`.

---

## 2026-08-19 — Future features require a prior mathematical statement

Status: ACCEPTED

Decision:

No new experiment or visualization is added merely because it is interesting.

Reason:

The instrument should remain minimal and proof-path focused.

Mathematical / operational consequence:

A future feature must correspond to an exact identity, candidate invariant, falsifiable statement, or explicit proof step.

Supersedes:

None.

---

## 2026-08-19 — Explicit Preview vs Audit precision boundaries

Status: ACCEPTED

Decision:

Maintain two computational tiers:

- Preview: reduced/float-friendly path for responsive UI;
- Audit: arbitrary/high precision for authoritative metrics.

Audit calculations must never cast authoritative decimal-string parameters to binary float before evaluation.

Reason:

Silent downcasting destroys precision and can manufacture or hide residual behavior.

Mathematical / operational consequence:

Core mathematical functions accept high-precision-compatible inputs. Preview output is not authoritative research output.

Supersedes:

None.

---

## 2026-08-19 — Exact Riemann remainder series

Status: ACCEPTED

Decision:

Use

\[
\int_x^\infty
\frac{du}{u(u^2-1)\log u}
=
\sum_{m=1}^{\infty}
E_1(2m\log x)
=
-
\sum_{m=1}^{\infty}
\operatorname{Ei}(-2m\log x)
\]

rather than an undocumented one-term asymptotic approximation.

Reason:

The exact converter contract includes the full remainder.

Mathematical / operational consequence:

Preview may use a fast implementation; Audit computes the declared series to tolerance.

Supersedes:

Any earlier one-term remainder approximation.

---

## 2026-08-19 — Independent discovery for transformed-zero validation

Status: ACCEPTED

Decision:

When validating an exact transformed zero map, transformed zeros should be independently discovered/refined before comparison against algebraically predicted locations where feasible.

Reason:

Seeding with predicted mapped locations would invalidate the independence claim.

Mathematical / operational consequence:

Predicted transform coordinates are comparison targets, not discovery seeds.

Supersedes:

None.

---

## 2026-08-19 — Reproducible batch sweep runner

Status: ACCEPTED

Decision:

Use `research_runner.py` with finite declarative experiment specs and machine-readable artifacts.

Reason:

Interactive discoveries need reproducible verification without proof-framework sprawl.

Mathematical / operational consequence:

The runner evaluates only declared finite questions and does not output automated RH verdicts.

Supersedes:

None.

---

# 2026-08-21 decisions

## 2026-08-21 — Introduce Transcendental Continuation as the canonical framework

Status: ACCEPTED

Decision:

Define the project term **transcendental continuation** by

\[
\boxed{
\mathcal Z_\tau(s,k)
=
\zeta(\tau^{-k}s),
\qquad
(s,k)\in\mathbb C\times\mathbb R.
}
\]

Reason:

The project is not merely applying isolated scale widgets. It is studying zeta in an enlarged scale-graded domain.

Mathematical / operational consequence:

The application, docs, batch runner, and formal layer treat \(k\) as a first-class coordinate rather than an incidental slider.

Supersedes:

The weaker description of the project as only a microscope/macroscope of isolated transforms.

---

## 2026-08-21 — Native analytic continuation is the \(k=0\) state

Status: ACCEPTED

Decision:

Treat

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s)
}
\]

as the native transcendental-continuation slice.

Reason:

Ordinary analytic continuation is not conceptually outside the framework. It is the zero-grade state.

Mathematical / operational consequence:

The default application state remains ordinary zeta, but is now explicitly represented as \(k=0\).

Supersedes:

Any wording that presents analytic continuation and transcendental continuation as unrelated domains.

---

## 2026-08-21 — Separate continuous, integer, and rational grade semantics

Status: ACCEPTED

Decision:

Use:

\[
k\in\mathbb R
\]

for continuous scale coordinate,

\[
K\in\mathbb Z
\]

for canonical bilateral grades, and

\[
q\in\mathbb Q
\]

for rational/root refinements.

Reason:

The previous use of one `K` symbol for both continuous and integer scaling blurred distinct mathematical roles.

Mathematical / operational consequence:

Schemas, UI labels, tests, and code paths preserve grade type.

Supersedes:

Any prior contract treating grade `K` as an undifferentiated real parameter.

---

## 2026-08-21 — Tau is the canonical transcendental-continuation generator

Status: ACCEPTED

Decision:

Use

\[
\tau=2\pi
\]

as the canonical grade generator rather than merely a default zoom base.

Reason:

Tau is the full-turn constant, is transcendental, naturally supports the bilateral family \(\tau^K\), and is structurally aligned with the project's rotational/Fourier interpretation.

This does not prove tau-specific RH leverage.

Mathematical / operational consequence:

Tau remains canonical in the project. Generic-base controls remain mandatory for theorem-facing claims of tau specificity.

Supersedes:

`2026-08-19 — Tau is the project-facing full-turn scale`.

---

## 2026-08-21 — Parallel Construction Principle

Status: ACCEPTED

Decision:

Model the canonical arithmetic grade family as

\[
\boxed{
L_K=\tau^K\mathbb Z.
}
\]

Distinct integer grades satisfy

\[
L_J\cap L_K=\{0\}
\quad
(J\neq K).
\]

Treat grades as parallelly constructed scale systems, not as states reached by finitely traversing one infinite arithmetic line.

Reason:

Each line contains infinitely many scale-isomorphic stops but distinct nonzero integer-grade lines are arithmetically noncoincident.

Mathematical / operational consequence:

Grade membership is a structural coordinate. The app may display exact grade identity independently of its finite numerical realization.

Supersedes:

None.

---

## 2026-08-21 — Exact symbolic referent versus finite numerical realization

Status: ACCEPTED

Decision:

Use the project language:

```text
exactly specified, finitely realized
```

for transcendental grades.

Reason:

The project needs to distinguish exact symbolic expressions such as

\[
\tau^K
\]

from any finite positional numerical realization without requiring the repo to resolve broader philosophical disagreements over the technical word `computable`.

Mathematical / operational consequence:

Run artifacts preserve both symbolic grade and numerical approximation/precision.

Supersedes:

Any implementation that retains only a decimal scale value.

---

## 2026-08-21 — Zero Worldline and Critical Surface

Status: ACCEPTED

Decision:

For a native zero \(\rho\), define the transcendental-continuation worldline

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

Define the critical surface

\[
\boxed{
\Re(s)=\frac{\tau^k}{2}.
}
\]

Reason:

This is the natural geometry of zeros across the enlarged \((s,k)\)-domain.

Mathematical / operational consequence:

The application should visualize grade slices/worldlines and may include a 3D worldline view.

Supersedes:

Any implementation that treats transformed zero coordinates only as disconnected 2D copies.

---

## 2026-08-21 — Normalized radial leaves

Status: ACCEPTED

Decision:

Define

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

Along the worldline generated by

\[
\rho=\frac12+\delta+i\gamma,
\]

\[
R_\tau=\delta.
\]

Reason:

This is the exact grade-invariant radial class.

Mathematical / operational consequence:

The app distinguishes absolute radial defect from normalized radial class.

Compression must not be described as moving an off-line class toward the critical class.

Supersedes:

Any interpretation of compression as a direct RH contradiction.

---

## 2026-08-21 — Replace literal space-filling contradiction with constraint intersection

Status: ACCEPTED

Decision:

Do not claim that transcendental continuation literally fills all geometric space and leaves no room for an off-line zero.

Instead frame the proof search as intersection of exact grade constraints:

\[
\boxed{
\text{Spectrum}
\in
\bigcap_{K\in\mathbb Z}
\mathcal C_K.
}
\]

Research whether this simultaneous constraint system permits more than one occupied radial leaf.

Reason:

Parallel noncoincident arithmetic lines can coexist in the real continuum; literal space-filling is not a valid contradiction.

Mathematical / operational consequence:

The central experiment seeks a zeta-specific no-compensation/radial-rigidity law rather than a geometric collision by assumption.

Supersedes:

Any draft claiming that an off-line zero must literally intersect another grade line because all space is filled.

---

## 2026-08-21 — Central proof target is Transcendental Radial Rigidity

Status: ACCEPTED

Decision:

The proof programme is concentrated in:

\[
\boxed{
\text{Transcendental Coherence}
\Longrightarrow
\text{Transcendental Radial Rigidity}.
}
\]

Reason:

All current exact grade/worldline identities describe radial classes but do not yet exclude mixed classes.

Mathematical / operational consequence:

New experiments and formal work should serve this implication or explicitly falsify it.

Supersedes:

The vaguer statement `all zeros are coupled, therefore two radial classes cannot coexist`.

---

## 2026-08-21 — Use xi for proof-facing nontrivial-zero work

Status: ACCEPTED

Decision:

Use

\[
\xi(s)
\]

and

\[
\mathcal X_\tau(s,k)=\xi(\tau^{-k}s)
\]

when the research question concerns only the nontrivial zero spectrum.

Reason:

The trivial zeros belong to a separate structural sector and should not clutter the RH-specific radial-class argument.

Mathematical / operational consequence:

The full zeta/trivial-zero/converter architecture remains in the app; proof-facing radial work may operate on xi.

Supersedes:

None.

---

## 2026-08-21 — High-zero blocks are structural research inputs, not RH evidence

Status: ACCEPTED

Decision:

Support sparse, widely separated high-zero blocks.

Reason:

A height-independent coherence claim must be tested at genuinely different actual heights, including very high finite ordinates.

Mathematical / operational consequence:

High-zero data may be labeled `research_input` and need not be independently rediscovered if discovery is not the experimental claim.

Finite high-zero verification is not interpreted as proof evidence for RH.

Supersedes:

The assumption that one contiguous low reference snapshot is sufficient for the central research campaign.

---

## 2026-08-21 — Current canonical run retention

Status: ACCEPTED

Decision:

Git history is the historical record. The live `research/index.json` and `research/runs` should retain only current canonical runs unless a current comparison explicitly requires more than one.

Reason:

A growing live archive obscures current research state and is unnecessary under version control.

Mathematical / operational consequence:

Canonical replacement runs supersede old live artifacts; superseded artifacts remain recoverable from Git history.

Supersedes:

Any earlier operational reading that every completed run must remain indefinitely in the live tree.

---

## 2026-08-21 — Lean is the proof firewall

Status: ACCEPTED

Decision:

Use Lean to formalize exact scale/grade/worldline identities and the logical contradiction skeleton before attempting large-scale formal analytic number theory.

Reason:

The project still needs to discover the missing coherence theorem. Formalizing the entire known theory first would not discover it.

Mathematical / operational consequence:

No unproved zeta-specific coherence law may be encoded as an axiom. A surviving candidate invariant is handed to Lean only after an exact theorem statement exists.

Supersedes:

Any interpretation that the project should be rebuilt entirely in Lean before discovery.

---

## 2026-08-21 — Riemann Scope remains an instrument, but explicitly serves a proof path

Status: ACCEPTED

Decision:

The application remains a numerical/visual research instrument and does not issue theorem verdicts.

However, its explicit purpose is now to support the contradiction programme documented in `RESEARCH_HYPOTHESIS.md`.

Reason:

The earlier phrase `not a proof engine` was correct but too easily interpreted as `not part of a proof programme`.

Mathematical / operational consequence:

The UI may display candidate proof steps and formalization targets, but finite computation never upgrades them to proof automatically.

Supersedes:

Any wording that prohibits a proof-path research layer altogether.

---

## 2026-08-21 — Rigorous mathematical certification engine and machine-verifiable certificates

Status: ACCEPTED

Decision:

Implement a rigorous, multi-tiered FLINT/Arb ball arithmetic certification engine (`certification.py`) producing standalone machine-verifiable JSON certificate artifacts under `data/certificates/`.
Explicit certification levels are:
- `candidate`
- `residual_verified`
- `isolated_zero_certified`
- `simple_zero_certified` (requiring $0 \notin \zeta'(B_n)$)
- `complete_block_certified` (Turing zero count matching isolated zeros)
- `worldline_certified` (bilateral propagation and radial leaf invariance)

Reason:

Numerical agreement and floating-point residuals are empirical heuristics, not certified mathematical objects. A proof-facing instrument requires certified ball enclosures, rigorous derivative non-vanishing, and cryptographic SHA-256 verification.

Mathematical / operational consequence:

Certificate generation (`scripts/generate_certificates.py`) is decoupled from fast verification (`scripts/verify_certificates.py`). Verification runs in CI and fails closed upon any schema, interval, derivative, or hash anomaly.

Supersedes:

Unconditional strings and heuristic float-based "Verified Simple" classifications.

---

## 2026-08-21 — Overwrite-only experiment run policy with atomic replacement

Status: ACCEPTED

Decision:

Ordinary experiment sweeps have exactly one canonical live result at `research/runs/<experiment-id>/`. Rerunning an experiment replaces its stable directory atomically via a temporary sibling directory (`.tmp_<exp_id>_<pid>`), updating `research/index.json` in place. No historical timestamped run directories are archived.

Reason:

Historical accumulation of ordinary runs clutters the repository without adding scientific value, as Git history provides complete historical versioning.

Mathematical / operational consequence:

Live repository runs reflect the current committed state with zero duplicate clutter. Reusable computations with declared downstream consumers are persisted under `data/` rather than historical run directories.

Supersedes:

Timestamped run directory accumulation (`research/runs/<timestamp>_<id>/`).

---

## 2026-08-21 — Classification of coupled-scale C_pi residual as a finite-m truncation diagnostic

Status: ACCEPTED

Decision:

Classify `cpi_covariance_residual` as `fixed_m_truncation_diagnostic` rather than an exact criterion component. The exact covariance criterion evaluates zeta coordinate representation covariance and single-zero $C_J$ wave covariance (which are exact to $\le 10^{-45}$).

Reason:

The single-zero $C_\pi$ explicit formula component involves an infinite Möbius-weighted series $\sum \frac{\mu(m)}{m} C_J(x^{1/m}, \dots)$. Truncating to finite $m \le 50$ produces an expected truncation error $\approx 0.150872$ that is a truncation diagnostic, not a failure of exact scale covariance.

Mathematical / operational consequence:

The observed $C_\pi$ truncation error remains reported and displayed as a diagnostic metric without falsely failing the exact coordinate covariance control.

Supersedes:

Treating $C_\pi$ truncation error as a criterion component of exact covariance.

---

## 2026-08-22 — Distinction between coordinate covariance gauge G_K, arithmetic constraint A_K, and infinite spectrum uniqueness

Status: ACCEPTED

Decision:

Explicitly separate the coordinate covariance gauge identity $\mathcal{G}_K$, positive-grade arithmetic constraints $\mathcal{A}_K$, and the unresolved infinite spectrum uniqueness problem across all mathematical contracts, research specifications, and verifiers:
1. **Coordinate Covariance Gauge $\mathcal{G}_K$**: The identity $\mathcal{Z}_\tau(\tau^K \rho, K) = \zeta(\rho) = 0$ is an exact coordinate gauge tautology holding for all continuous dilations and all $s \in \mathbb{C}$, imposing zero constraints on zero locations on or off the critical line ($\delta = 0$ vs $\delta \ne 0$).
2. **Arithmetic Constraint $\mathcal{A}_K$**: For integer $K \ge 1$, evaluating $\zeta(\tau^K s)$ relates dilated values to the native zeta function through Euler product and explicit formula structures, restricting admissible Dirichlet series.
3. **Unresolved Infinite Spectrum Intersection**: The central open conjecture of transcendental continuation is whether $(\bigcap_{K \ge 1} \mathcal{A}_K) \cap \mathfrak{S}_{\mathrm{mixed}} = \varnothing$.

Reason:

Conflating gauge covariance with arithmetic constraints creates false proof claims or hidden circularities. The repository must maintain absolute epistemic rigor by separating tautological coordinate transforms from non-trivial arithmetic spectrum restrictions.

Mathematical / operational consequence:

The verifier, certification engine, and frontend distinguish exact worldline gauge covariance ($R_\tau(s_\rho(K), K) = \delta$) from open arithmetic rigidity theorems. No stage of the research runner assumes radial rigidity as an external premise.

Supersedes:

Any formulation implying that bilateral coordinate dilation alone excludes off-line zeros.

---

## 2026-08-22 — Zero Family Ontology and Archimedean Separation in Explicit Prime Reconstruction

Status: ACCEPTED

Decision:

1. **Explicit Zero Family Segregation**: The repository strictly categorizes all evaluated zeros into three non-overlapping families:
   - `nontrivial`: Critical-strip zeros indexed $n \ge 1$ ($\rho_n = 1/2 + i\gamma_n$, $\gamma_n > 0$) with critical-surface worldlines $s_n(K) = \tau^K \rho_n$ and radial coordinate $R_\tau \equiv 0$.
   - `trivial`: Exact negative even integer zeros indexed $m \ge 1$ ($s_m = -2m$) with off-critical worldlines $s_m(K) = \tau^K (-2m)$ and radial coordinate $R_\tau \equiv -2m - 1/2 \ne 0$.
   - `synthetic`: Perturbed off-line test points ($\delta \ne 0$) for defect and sensitivity studies.
   The un-scoped identifier `zero_index` is deprecated in favor of `nontrivial_index` and `trivial_index`.

2. **Explicit Formula Summation Convention**: In Riemann explicit prime reconstruction $\pi_N(x)$ and $J_N(x)$, the sum over zeros $\sum_\rho \operatorname{Li}(x^\rho)$ runs strictly and exclusively over nontrivial zeros in the critical strip. The trivial zeros $s_m = -2m$ are completely and accurately accounted for by the archimedean integral term:
   \[
   -\frac{1}{2}\log(1 - x^{-2}) = \int_x^\infty \frac{dt}{t (t^2 - 1) \ln t} = \sum_{m=1}^\infty \operatorname{Li}(x^{-2m})
   \]
   No trivial zero ordinate or location shall ever be injected into the $\sum_\rho$ sum, preventing double-counting anomalies.

Reason:

Prevent conflation of trivial and nontrivial zeros, eliminate ambiguous indexing, and guarantee rigorous conformance to the Riemann explicit formula analytical contract.

Mathematical / operational consequence:

Certificates, batch runners, frontend badges, and validation suites enforce separate namespaces, explicit family tags, and distinct verification rules.

Supersedes:

Ambiguous generic `zero_index` and any potential double counting of trivial zeros.

---

## 2026-08-23 — Reconciling Explicit Formula Grade Covariance, Independent Quadrature Control, and Separation of Coordinate Redundancy from Undefined Arithmetic Constraints

Status: ACCEPTED

Decision:

1. **Test Function Enclosure Digits**: Ensure test function center ordinates (especially zero-50) are populated from certified ball enclosure midpoints (e.g. $\gamma_{50} \approx 143.1118458...$).
2. **Independent Fourier Quadrature Control**: Implement panel-subdivided tanh-sinh quadrature in native variable $u = a_K t$ over compact effective support $[0, t_0 + 15\sigma]$ to eliminate frequency oscillation instability and achieve $< 10^{-45}$ error control across all grades $K \in \{-2..2\}$ and test functions $j \in \{1..6\}$.
3. **Compound Exact-Control Pass/Fail Criterion**: Enforce simultaneous compound verification across Fourier scaling error, coordinate pullback error, independent Fourier quadrature error, expanded-native basis discrepancy, and cross-path matrix rank equality ($14 = 14 = 14$).
4. **Coordinate Redundancy Distinction**: Maintain explicit distinction between the exact infinite coordinate pullback identity $\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K]$ (`coordinate_redundant`) and comparison against an unexpanded finite basis (`finite_basis_enrichment_only`).
5. **Future Arithmetic Constraints**: Classify any prospective joint arithmetic constraint operating without test function dilation as an `OPEN / UNDEFINED CANDIDATE` distinct from $\mathcal C_{K,j}$.

Reason:

Guarantee rigorous independent mathematical control, eliminate numerical quadrature artifacts, publish reconstructible linearized compensation diagnostics, and ensure flawless epistemic integrity across the proof programme.

Mathematical / operational consequence:

The test suite, batch runner, certificate verifier, and UI dashboards verify exact covariance and quadrature controls, publish reconstructible `diagnostics.json`, and prevent any conflation between coordinate dilation and non-trivial Euler product automorphisms.

Supersedes:

Naive undivided Fourier quadrature in negative grades and any ambiguous classification of $\mathcal C_{K,j}$.

---

## 2026-08-23 — Second-Order Radial Sensitivity, Defect Divisors, and Non-Negative Least Squares Analysis

Status: ACCEPTED

Decision:

1. **Radial Projection Operator and Defect Divisor**: Formalize the critical-line projection operator \(\mathcal P_0(\rho) = 1/2 + i\gamma\) and the defect divisor \(\Delta\mathcal D_{\mathrm{rad}} = \mathcal D - \mathcal P_0(\mathcal D)\), ensuring exact separation between on-line spectrum and radial displacements.
2. **Second-Order Taylor Response**: Model the pure radial defect response under even holomorphic test functions as \(\Delta\mathcal C_h[\mathcal O(\rho)] = -2\delta^2 h''(\gamma) + \mathcal O(\delta^4) = -2 u h''(\gamma) + \mathcal O(u^2)\), where \(u = \delta^2 \ge 0\) is the non-negative orbit variable.
3. **Single-Target Quadratic Radial Energy vs Cone Compensation**: Define the single-target energy \(E(u_n) = u_n^2 \|K_{\cdot, n}\|^2 \ge 0\). Note that single-target positivity does not preclude non-negative linear combinations of remaining columns from matching target columns in a high-nullity finite basis.
4. **Non-Negative Least Squares (NNLS) Diagnostic**: Evaluate finite compensation feasibility under the cone constraint \(u \ge 0\). In the sampled 30-channel basis over 100 zeros (nullity \(\approx 85\), \(\kappa \sim 10^{15}\)), NNLS yields heterogeneous diagnostic results (compensation was found at the \(10^{-5}\) threshold for zeros 10 and 50; compensation was not found at this threshold for zeros 1 and 100).
5. **The Projection Trap & Epistemic Classification**: Classify the experiment as an exact finite synthetic sensitivity diagnostic. Formally note the Projection Trap: \(\mathcal P_0(\mathcal D_\zeta)\) lacks an independent arithmetic explicit formula, so inferring radial rigidity from \(\Delta\mathcal D_{\mathrm{rad}}\) remains an unproved theorem.

Reason:

Provides an exact, non-circular mathematical instrument to evaluate local quadratic Taylor fidelity while honestly reporting finite basis subspace geometry without overstating proof implications.

Mathematical / operational consequence:

Implemented canonical experiment `explicit-formula-radial-second-variation-001`, verified Lean 4 formal foundations (`RiemannScope.RadialDefect`), and published categorical NNLS metrics and reconstructible diagnostics.

Supersedes:

Any interpretation of finite single-target positive energy as a universal proof of global non-compensation.

---

## 2026-08-24 — Radial-Defect Quotient Consolidation, Relative Fredholm Formulation, and Projection Trap Scoping

Status: ACCEPTED

Decision:

1. **Radial-Defect Quotient \(Q(z)\) and Limiting Invariant \(L_Q\)**: Encode the canonical quotient \(Q(z) = \frac{\Xi(z)}{\Xi(0)\Xi^\flat(z)} = \prod_j (Q_{\delta_j,\gamma_j}(z))^{n_j}\), based on the paired Hadamard factorization of \(\Xi(z)\), exclusion of real zeros, and general zero multiplicity \(m_\gamma = m_{0,\gamma} + 2\sum_j n_{j,\gamma}\) in baseline \(\Xi^\flat(z) = \prod_{\gamma>0}(1 + z^2/\gamma^2)^{m_\gamma}\). On off-line quartets along the real axis, \(0 < q_{\delta,\gamma}(x) \le 1\) with exact defect factorization \(1 - q = \frac{\delta^2 x^2 [(\delta^2+2\gamma^2)x^2 + 2\gamma^2(\delta^2+3\gamma^2)]}{(\delta^2+\gamma^2)^2(x^2+\gamma^2)^2} \ge 0\), unique minimum in \(u=x^2\) at \(u_* = \delta^2 + 3\gamma^2\) (two real minimizers \(x = \pm\sqrt{\delta^2+3\gamma^2}\)), and minimum value \(q_{\min} = \frac{4}{(1+r)^2(4+r)}\). The limiting invariant \(L_Q = \lim_{x\to\infty} Q(x) = \prod_j (1+r_j)^{-2n_j}\) satisfies \(0 < L_Q \le 1\) and \(L_Q = 1 \iff \mathrm{RH}\).
2. **Exact Relationship to EF-013 & Audited Claim Withdrawal**: Acknowledge that the defect \(-\log L_Q = 2\sum n_j d(\delta_j,\gamma_j)\) (where \(d(\delta,\gamma) = \log(1+\delta^2/\gamma^2)\)) is identically the projection-subtracted response for \(H(z) = \log z\). Formally **withdraw** the former conjecture that EF-013 had the "wrong \(\gamma\)-curvature" (`WDR-001`), while recording its three distinct failure reasons: test-class inadmissibility, absence of an independent arithmetic representation for \(\mathcal P_0(\mathcal D_\zeta)\), and unproved finite compensation.
3. **Scoped Projection Trap Classification**: Scoped `EF-018` / `OBL-EF-003` to: **CLOSED** for fixed linear combinations and locally uniform limits of direct one-point holomorphic Riemann–Weil statistics over an open displacement family (rigorously proved via Cauchy-Riemann equations on $2\Re G(\delta+i\gamma)$); **OPEN** for nonlinear paired, determinantal, operator, or independently constructed comparison objects (`OBL-RDQ-001`).
4. **Relative Fredholm Formulation**: Define the positive diagonal trace-class operator \(\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda\) with \(\operatorname{Tr}\mathcal R = \sum \frac{\delta^2}{\gamma^2}\) and \(\det_{\mathrm F}(I + \mathcal R) = L_Q^{-1}\). Vanishing of the trace \(\operatorname{Tr}\mathcal R = 0\) is the minimal scalar RH-equivalent criterion.
5. **Involution Pairing Kernel \(\kappa_1\)**: Establish the exact rational pairing identity \(\kappa_1(z, z^\#) = \frac{\delta^2}{\gamma^2}\) for \(\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1\) and \(z^\# = -\bar z\) (with \((z+z^\#)^2 = -4\gamma^2\) and \(zz^\# = -(\delta^2+\gamma^2)\)), identifying the arithmetic realization of \(\operatorname{Tr}\mathcal R = \sum \kappa_1(\lambda, \lambda^\#)\) without constructing the projected divisor as the minimal live research theorem (`OBL-RDQ-001`).
6. **Grade Covariance and Invariance**: Note that \(Q_K(z_K) = Q_0(\tau^{-K}z_K)\) and \(Q_K(\tau^K z) = Q_0(z)\), while \(L_Q\), \(\{r_\lambda\}\), and \(\mathcal R\) are grade-invariant; transcendental continuation preserves radial class, but ordinary coordinate dilation alone does not supply the rigidity law. Additional zeta-specific arithmetic content is necessary.

Reason:

Consolidates the audited mathematical breakthrough of the Radial-Defect Quotient into the canonical authority chain, resolves historical ambiguities, scopes the Projection Trap no-go boundary, and isolates the exact next mathematical theorem.

Mathematical / operational consequence:

Created canonical specification `RADIAL_DEFECT_QUOTIENT.md`, updated all authority documents and corpus registers (`RDQ-*`), added pure arbitrary-precision audit functions in `math_core.py`, added comprehensive targeted tests, and formalized finite algebraic firewall lemmas in Lean 4.

Supersedes:

Unscoped interpretation of EF-018 as a universal impossibility of all arithmetic representations, and former working conjecture that EF-013 had incorrect \(\gamma\)-curvature.

---

## 2026-08-25 — Arithmetic Radial Bridge Candidate Evaluation, Covariance Countermodel, and Rigidity Boundaries

Status: ACCEPTED

Decision:

1. **Target Hierarchy Distinction**: Maintain strict separation among the three bridge targets:
   - Determinant Target: \(D := -\log L_Q = \log\det_{\mathrm F}(I+\mathcal R) = \sum 2n_j \log(1+r_j)\);
   - Trace Target: \(T := \operatorname{Tr}\mathcal R = \sum 2n_j r_j\);
   - Regularized Weighted Target: \(T_a = \sum w_a(\lambda) \kappa_1(\lambda, \lambda^\#)\) (\(w_a(\lambda) > 0\)).
2. **Strict Arithmetic Input Firewall**: Enforce that arithmetic evaluators \(\mathfrak A_{K,X}^{\mathrm{arith}}\) receive only intrinsic arithmetic data (primes, \(\Lambda(n)\), Euler products for \(\Re(s)>1\), pole at \(s=1\), gamma factor, functional equation symmetries, and transcendental continuation \(\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)\)), strictly rejecting zero lists, projected ordinates, \(\Xi^\flat\), \(Q, L_Q, \mathcal R, D, T\).
3. **Correct Grade-Centering Geometry**: Reconcile grade center \(c_K = \tau^K/2\), centered coordinate \(z_K = s_K - c_K = \tau^K z\), centered completed xi \(\Xi_K(\tau^K z) = \Xi_0(z)\), and invariant ratio \((\tau^K\delta)^2/(\tau^K\gamma)^2 = \delta^2/\gamma^2\).
4. **Covariance Countermodel (Covariance \(\ne\) Rigidity)**: Establish that an abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under reflection, conjugation, and transport symmetries, proving that coordinate covariance alone does not force \(\delta = 0\). An independent arithmetic anchor \(\mathfrak A_K = 0\) is mandatory.
5. **Candidate Bridge Classifications**:
   - Candidate A (Linear Grade Differences): `FALSIFIED_FOR_BRIDGE` (collapses to native explicit formula \(\mathcal C_0[H\circ\tau^K]-\mathcal C_0[H]\)).
   - Candidate B (Bilinear Cross-Grade Explicit Formula): `FALSIFIED_FOR_PAIR_ISOLATION` (\(D_K(s)\overline{D_L(s)}\) yields unrestricted double sum over all zero pairs; off-diagonal terms contaminate).
   - Candidate C (Tensor-Square Trace Identity): `FALSIFIED_FOR_PAIR_ISOLATION` (unrestricted double sum).
   - Candidate D (Log-Derivative Contour Identity): `FALSIFIED_FOR_PAIR_ISOLATION` (residue cross-terms across critical strip).
   - Candidate E (Relative Determinant from Arithmetic Space): `OPEN_UNPROVED`.
   - Candidate F (Grade-Indexed Prime-Power Pairing): `OPEN_UNPROVED`.
   - Candidate G (Weighted Regularized Bridge): `LIVE_UNDERIVED` (spectral detector \(T_a>0\) proved; arithmetic realization open).
6. **Corpus and Formal Infrastructure**: Create canonical specification `ARITHMETIC_RADIAL_BRIDGE.md`, add pure arbitrary-precision harness in `math_core.py`, comprehensive test suite in `tests/test_arithmetic_radial_bridge.py`, and formal Lean 4 theorems in `RiemannScope.ArithmeticBridge` (arbitrary-list weighted positivity, covariance countermodel, conditional bridge rigidity).
7. **Epistemic Closure Status**: Keep `OBL-RDQ-001` **OPEN**. No arithmetic proof of RH is claimed without an independent, unconditional arithmetic bridge derivation and vanishing proof.

Reason:

Rigorous mathematical construction and falsification sprint isolating the exact barrier to the arithmetic radial bridge, proving that covariance is not rigidity, eliminating dead-end candidate mechanisms, and formalizing surviving structural theorems.

Mathematical / operational consequence:

Created canonical specification `ARITHMETIC_RADIAL_BRIDGE.md`, updated all authority documents, verified 23 targeted tests in `tests/test_arithmetic_radial_bridge.py`, compiled Lean 4 formalizations with 0 errors/warnings, and cataloged all 7 candidates in the candidate registry.

Supersedes:

Any conflation of coordinate transport covariance with radial rigidity, and any expectation that linear or naive bilinear explicit formulas isolate involution pairs without projected-divisor knowledge.

---

## 2026-08-26 — Complete Finite Spectral-Kernel Closure, Arbitrary Curvature Formalization, and Exact Gate G4 Analytic Obstruction

Status: ACCEPTED

Decision:

1. **Finite Spectral Expansion Closure**: Implement and verify the exact complete finite spectral expansion:
   $$S_{N, T}(\sigma) := \frac{1}{2T}\int_{-T}^T \left| A(\sigma+it) - \sum_{k=1}^N m_k \frac{2z}{z^2-\lambda_k^2} \right|^2 dt = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},$$
   closing to machine precision ($< 10^{-18}$) via exact closed-form translation kernel $J_T(p,q) = \frac{\log\frac{p+iT}{p-iT} + \log\frac{q+iT}{q-iT}}{2Ti(p+q)}$ and paired zero-zero kernel $K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu)$.
2. **Identification of Earliest Infinite Analytic Obstruction (Gate G4)**: Prove and document that the individual zero resolvents $\frac{1}{\sigma-\rho+it}$ belong to $L^2(\mathbb R, dt)$ with finite norm $\frac{\pi}{\sigma-\Re\rho}$, so under translation averaging $(1/2T)\int_{-T}^T \frac{dt}{|\sigma-\rho+it|^2} \to 0$ as $T\to\infty$. The non-zero Besicovitch mean of the arithmetic side is carried by non-uniform infinite collective cancellation; termwise infinite interchange $\lim_{T\to\infty} \sum_{\lambda,\mu} K_T = \sum_{\lambda,\mu} \lim_{T\to\infty} K_T$ is unproved and false without established regularization.
3. **Exact Real-Axis Spectral Defect Formula**: Establish the exact rational defect between an off-line quartet $\{\pm\delta \pm i\gamma\}$ and on-line pair $\{0, \pm i\gamma\}$ at $z = \sigma - 1/2 > 0$:
   $$\Delta(\delta) = \frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2 + \gamma^2)[(z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2]},$$
   proving that $\Delta(\delta) < 0$ for $z^2 < 3\gamma^2 + \delta^2$ (holding for all critical strip zeros $\gamma > 14$ at $z = O(1)$), transitioning to positive only for $z > \sqrt{3}\gamma$.
4. **Lean 4 Formalization of Arbitrary Finite Curvature**: Formally prove in `formal/RiemannScope/ArithmeticBridge.lean` (100% compiled with 0 `sorry`, 0 `admit`, 0 axioms):
   - `list_pairs_sq_sum_eq`: $\sum_{i,j} (d_i + d_j)^2 = 2N\sum d_i^2 + 2(\sum d_i)^2$ for arbitrary real lists of length $N$;
   - `list_pairs_sq_sum_symmetric`: reduces to $2N\sum d_i^2$ when $\sum d_i = 0$;
   - `list_pairs_sq_sum_nonneg` & `list_pairs_sq_sum_eq_zero_iff`: unconditionally non-negative, vanishing iff $\forall x \in l, x = 0$;
   - `generic_scale_dilation_cancellation`: $s D_s(su) = f(u)$ for any scale $s > 0$.
5. **Candidate Classification Updates**:
   - `CANDIDATE_CMSA1` & `CANDIDATE_CMSA2`: Classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4`.
   - `CANDIDATE_CMSA3`: Classified as `GRADE_COORDINATE_REDUNDANT`.
   - Sprint outcome classified as `FINITE_SPECTRAL_KERNEL_CLOSED_INFINITE_G4_OPEN`.
6. **Epistemic Closure Status**: Keep `OBL-RDQ-001` **OPEN**. No proof of RH is claimed.

Reason:

Rigorous mathematical sprint completing the finite spectral expansion, evaluating exact kernel cross-terms in arbitrary precision, proving arbitrary curvature identities unconditionally in Lean 4, and isolating Gate G4 (Infinite Spectral Interchange) as the exact earliest open analytic barrier.

Mathematical / operational consequence:

Implemented exact analytic kernels $J_T, K_T$, complete finite spectral expansion evaluator, and direct completed function control in `math_core.py`. Verified 61 targeted test cases across `tests/test_completed_mean_square_anchor.py`, `tests/test_separated_signal.py`, `tests/test_radial_defect_quotient.py`, and `tests/test_arithmetic_radial_bridge.py`. Formally compiled Lean 4 proofs. Updated all registers and specifications.

Supersedes:

Any claim that the finite spectral expansion is incomplete or that CMSA-1/CMSA-2 failure is due to low-height curvature anomalies rather than non-uniform infinite spectral limit interchange.



