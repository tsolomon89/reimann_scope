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
   as an exact algebraic 4-term decomposition validated numerically (closure residual $< 10^{-15}$) via exact closed-form translation kernel $J_T(p,q) = \frac{\log\frac{p+iT}{p-iT} + \log\frac{q+iT}{q-iT}}{2Ti(p+q)}$ and paired zero-zero kernel $K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu)$.
2. **Identification of Earliest Infinite Analytic Obstruction (Gate G4)**: Prove and document that every fixed finite collection of individual zero resolvents contributes zero after $1/(2T)$ normalization as $T\to\infty$ because $\frac{1}{\sigma-\rho+it} \in L^2(\mathbb R, dt)$ with norm $\frac{\pi}{\sigma-\Re\rho}$. This finite property does not justify interchanging the infinite spectral sum and the $T\to\infty$ limit. The non-zero Besicovitch mean of the arithmetic side is carried by non-uniform infinite collective cancellation; Gate G4 (Infinite Spectral Interchange) is the exact earliest open barrier in the present CMSA derivation.

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

---

## 2026-08-26 — Gate G4 Infinite-Regularization and Radial-Survival Resolution

Status: ACCEPTED

Decision:

1. **Gate G4 Sub-Gate Classification**: Systematically define, test, and classify the 7 sub-gates G4a–G4g for infinite regularization of the Completed Mean-Square Anchor:
   - G4a (Arithmetic Independence): PROVED / ENFORCED via mock firewall.
   - G4b (Exact Finite Expansion): PROVED / VERIFIED across Rectangular ($J_T, K_T$) and Fejér ($J_T^{\text{Fejér}}, K_T^{\text{Fejér}}$) windows.
   - G4c (Infinite Remainder Control): OPEN.
   - G4d (Limit-Order Control & Boundary Layer): OPEN / CHARACTERIZED. Proved asymptotic formulas across 4 regimes and formalized cofinal limit independence in Lean 4.
   - G4e (Radial Survival and Positivity): NUMERICAL EVIDENCE / OPEN PROOF ($\Delta S = \Delta I_{ZZ} + \Delta \text{Cross} > 0$ above resonance).
   - G4f (Pair Isolation): OPEN.
   - G4g (Grade Covariance): PROVED / GRADE_COORDINATE_REDUNDANT.
2. **Four Window Families (Loops 0–3)**: Derived exact Fejér closed kernel $J_T^{\text{Fejér}}(p,q) = \frac{I_T(p)+I_T(q)}{T(p+q)}$, evaluated Abel-Poisson and Gaussian windows, and classified all four families as `FINITE_IDENTITY_PROVED_G4_OPEN`.
3. **Formalization in Lean 4**: Formalized `finite_quadratic_expansion_identity`, `finite_quadratic_four_term_decomposition`, `cofinal_schedule_distinct_from_fixed_limit`, and `ConditionalG4RegularizedBridge.all_defects_zero` in `formal/RiemannScope/ArithmeticBridge.lean`.
4. **Epistemic Closure Status**: Keep `OBL-RDQ-001` and `OBL-CMSA-003` (Gate G4) **OPEN**. No proof of RH is claimed.

Reason:

Rigorous mathematical discovery and falsification sprint isolating the exact barrier to infinite regularization at Gate G4, proving cofinal boundary layer limit distinction, deriving exact windowed kernels, and synchronizing the full authority chain.

Mathematical / operational consequence:

Created canonical report `CMSA_GATE_G4.md`, updated `math_core.py` with Fejér kernels and G4 evaluators, added 17 comprehensive unit tests in `tests/test_cmsa_gate_g4.py`, compiled Lean 4 theorems with 0 errors/warnings, and updated all corpus registers.

Supersedes:

Any assumption that fixed-truncation zero-resolvent vanishing implies cofinal limit vanishing, or that infinite spectral passage can be achieved without regularizing the unnormalized arithmetic oscillation remainder.

---

## 2026-08-27 — Gate G4 Integrity Repair and Radial-Sign Theorem Resolution

Status: ACCEPTED (with partial correction/withdrawal below)

Decision:

1. **Exact Second-Order Radial Response Derivation**:
   Derived the exact second-order radial response coefficient:
   \[
   C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt,
   \]
   governing the leading variation \(\Delta S_W = \delta^2 C_W + O(\delta^4)\), where \(D_\gamma(z) = \frac{4z(z^2 - 3\gamma^2)}{(z^2+\gamma^2)^3}\).
2. **Sign Analysis of Raw Finite-Window Difference (CORRECTED / PARTIALLY WITHDRAWN)**:
   - *Withdrawn/Corrected Claim*: The claim that mpmath quadrature provided "rigorous error-bounded interval quadrature" is **WITHDRAWN**; `mpmath.quad(..., error=True)` returns an estimated numerical error rather than certified outward-rounded interval enclosures.
   - *Current Rigorous Status*: Compact Fejér WIT-02 is genuinely certified negative via outward-rounded Arb ball arithmetic (`certify_g4_fejer_witness_arb`), while WIT 1, 3, 4 represent high-precision numerical evidence.
   - Classification: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` on the general parameter domain; `FINITE_IDENTITY_PROVED_G4_OPEN` for the finite expansion; `GRADE_COORDINATE_REDUNDANT` for grade coordinate dilation.
3. **Internal Proof of Carlson Mean-Square Special Case**:
   Proved the mean-square identity for Dirichlet series with \(\sum |a_n| < \infty\) internally in 4 distinct limit steps (finite identity, fixed-\(N\) limit, uniform tail bound, and interchange) without external black-box theorems.
4. **Lean 4 Formalizations**:
   Formalized complex quadratic conjugation expansions, exact radial defect difference numerators, second-order response decompositions, and sequence countermodels in `formal/RiemannScope/ArithmeticBridge.lean`.
5. **Epistemic Authority**:
   Keep `OBL-RDQ-001` and `OBL-CMSA-003` **OPEN**. Earliest open subgate: prove a negative raw response analytically or with validated outward-rounded interval arithmetic on the general infinite/regularized limit.

Reason:

Epistemic and formal boundary repair sprint resolving the finite radial sign question, replacing preliminary conjectures with exact certified derivations and interval counterexamples.

Mathematical / operational consequence:

Updated `math_core.py`, `tests/test_cmsa_gate_g4.py`, `CMSA_GATE_G4.md`, `formal/RiemannScope/ArithmeticBridge.lean`, and all corpus registers.

Supersedes:

Any claim that the unmodified full finite-window difference \(\Delta S_W\) is unconditionally positive whenever \(T > \gamma\), or that scalar ring identities constitute a full complex analytic formalization.

---

## 2026-08-27 — Gate G4 Epistemic Repair and Additive-Renormalization No-Go Theorem

Status: ACCEPTED

Decision:

1. **Additive-Reference Invariance No-Go Theorem**:
   Proved that for any scalar reference term \(R_W(A)\) independent of \(Z, \delta, \gamma\):
   \[
   (S_W(Z_\delta) - R_W(A)) - (S_W(Z_0) - R_W(A)) \equiv S_W(Z_\delta) - S_W(Z_0).
   \]
   Therefore, a divisor-independent additive scalar subtraction cannot alter the raw radial difference. It proves that the additive class shares identically whatever sign behaviour the raw functional exhibits.
   Formalized in Lean 4 (`RiemannScope.additive_reference_subtraction_invariance`).
2. **Classification Standardization**:
   Classified the general raw candidate and zero-independent additive scalar-renormalization class as:
   `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
   Defined earliest open subgate: prove a negative raw response analytically or with validated outward-rounded interval arithmetic on the general infinite/regularized limit.
3. **Certified Arb Ball Integration for Fejér Witness WIT-02**:
   Implemented `certify_g4_fejer_witness_arb` in `math_core.py` enclosing the compact Fejér integral for $(\sigma=5, \gamma=14, \delta=0.49, T=16.8)$ in outward-rounded Arb ball arithmetic, proving $\Delta S_{\text{Fejér}} \in [-1.895 \times 10^{-4}, -1.542 \times 10^{-4}] \subset (-\infty, 0)$.
4. **Correction of Explanatory Sign Mechanism for WIT-02**:
   Corrected the mechanism analysis: local contribution at $t \in [0, 8]$ is strictly positive ($+8.43 \times 10^{-6}$ at $t=0$), while the dominant negative mass occurs around $t \in [9, 14]$ (peaking at $t=12$ with $-1.03 \times 10^{-4}$), driving the overall integral negative.
5. **Mathlib Filter.Tendsto Theorems in Lean 4**:
   Formalized genuine `Filter.Tendsto` theorems in `formal/RiemannScope/ArithmeticBridge.lean`:
   - `tendsto_cofinal_fixed_zero`: `Tendsto (fun (n : ℕ) => H / ((n : ℝ) + 1)) atTop (𝓝 0)`.
   - `not_tendsto_cofinal_diagonal_zero`: `¬ Tendsto (fun (n : ℕ) => ((n : ℝ) + 1) / ((n : ℝ) + 1)) atTop (𝓝 0)`.
   - `finite_sum_tendsto_interchange`: `Tendsto (fun n => ∑ i in s, f i n) atTop (𝓝 (∑ i in s, g i))`.
   Bringing total compiled project theorem declarations to 67.
6. **Pytest Tier Performance & API Refactoring**:
   Renamed `certify_g4_radial_sign_witness` to `evaluate_g4_radial_sign_evidence` (with deprecated wrapper) to accurately reflect numerical estimation vs Arb certification.

Reason:

Epistemic and formal boundary repair closing the additive renormalization candidate class, proving Mathlib Tendsto limits, certifying Fejér WIT-02 in Arb ball arithmetic, and standardizing classifications.

Mathematical / operational consequence:

Updated `math_core.py`, `tests/test_cmsa_gate_g4.py`, `CMSA_GATE_G4.md`, `MATH_CONTRACT.md`, `formal/RiemannScope/ArithmeticBridge.lean`, and all registers.

Supersedes:

Any claim that additive divisor-independent reference subtraction can renormalize the radial sign, or that mpmath estimated error constitutes a certified Arb interval ball.

---

## 2026-08-27 — Gate G4 Arb Certificate Hardening, Finite No-Go Closure, and Infinite/Cofinal Theorem Formulation

Status: ACCEPTED

Decision:

1. **Finite Candidate Class Closure (`FAIL_RADIAL_POSITIVITY`)**:
   For the compact Fejér window at $(\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8)$, outward-rounded Arb ball arithmetic proves $\Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0)$. Together with additive-reference invariance $(S_W(Z_\delta)-R)-(S_W(Z_0)-R) \equiv S_W(Z_\delta)-S_W(Z_0)$, this definitively closes:
   - The raw finite Fejér response claiming unconditional radial positivity;
   - Every zero-independent additive scalar subtraction of that finite Fejér response.
   Both candidate classes are classified strictly as `FAIL_RADIAL_POSITIVITY`.
2. **Infinite Candidate Class Scoping (`INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`)**:
   The `FAIL_RADIAL_POSITIVITY` classification does NOT apply to the full infinite/cofinal CMSA functional. CMSA-1 and CMSA-2 remain classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
   `CERTIFIED_NEGATIVE_ARB_BALL` is retained strictly as an evidence/certificate status for WIT-02, never as a final candidate classification.
3. **Largest Proved Obstruction Class**:
   Any candidate family containing the stated finite Fejér functional and modified only by a zero-independent additive scalar reference fails unconditional radial positivity. This does not cover non-additive operators, different pairings, or the complete infinite/cofinal limit.
4. **Canonical WIT-02 Certificate Artifact**:
   Created `data/certificates/witnesses/witness_g4_fejer_wit02.json` integrated into `certification.py` and `verification_report.json`, with tamper detection verifying exact decimal parameters, interval enclosure, subdivision count (50,000 across $[-T, T]$), precision, FLINT versions, source hash, and producing commit.
5. **Lean 4 Formalization Completion**:
   Formalized complex Dirichlet polynomial squared norm expansions (`complex_finset_sum_mul_star`, `complex_finset_normSq_eq_double_sum_re`), abstract finite kernel decompositions (`abstract_finite_kernel_decomposition`), additive operator interchanges (`linear_operator_finite_double_sum_interchange`), and windowed kernel pairings (`abstract_windowed_kernel_expansion`) in `formal/RiemannScope/ArithmeticBridge.lean`, bringing total compiled project theorems to 72.
6. **Phase B — Next Live Cofinal Theorem Formulation**:
   Formulated the exact next infinite obligation: Given symmetrically truncated $Z_H(t)$ and remainder $R_H(t) = \frac{\xi'}{\xi}(a+it) - Z_H(t)$, define a canonical cofinal schedule $H = H(T)$ and non-additive functional $R_T$ controlling remainder bounds, unequal-height pairs, same-height reflection pairs, and grade covariance.

Reason:

Rigorous hardening of Gate G4 authority documents, certificate infrastructure, Lean formalization, and next live theorem obligations.

Mathematical / operational consequence:

Updated `certification.py`, `scripts/generate_certificates.py`, `math_core.py`, `formal/RiemannScope/ArithmeticBridge.lean`, `README.md`, and all 11 authority documents and registers.

---

## 2026-08-27 — Certificate Purity Refactoring, Schedule Covariance Classification, and Lean 4 Theorem Expansion

Status: ACCEPTED

Decision:

1. **Certificate Purity & Isolation**:
   - Refactored `certification.certify_g4_radial_witness` to be pure by default (`output_path: Optional[str] = None`), preventing unit tests from overwriting tracked canonical certificates.
   - Fixed `generate_all` return type annotation in `scripts/generate_certificates.py` to `Tuple[int, int, int, int, int]`.
   - Added regression test `test_unit_tests_do_not_modify_tracked_canonical_certificates` proving all 508 certificates remain untouched across test suite execution.
2. **Conjugation Explanatory Derivation & Premise Cleaning**:
   - Direct certified Arb integration is evaluated across the complete symmetric interval $[-T, T]$ without assuming evenness or reflection as an operational premise.
   - Explanatory conjugation symmetry is derived from explicit meromorphic terms of $A$ and quadruplet pairing of $Z_\delta$ without invoking zeta conjugation or a general Schwarz reflection hypothesis.
3. **Schedule-Covariance Law & Non-Uniqueness Classification**:
   - Derived discrete grade covariance law $H(\tau T) = \tau H(T)$ ($\tau = 2\pi$) from the grade transformation.
   - Proved that every linear schedule $H_c(T) = cT$ is grade-covariant, and formalized the non-uniqueness theorem in Lean 4 (`RiemannScope.linear_schedule_grade_covariant`, `RiemannScope.grade_covariant_schedule_nonuniqueness`, `RiemannScope.periodic_modulated_schedule_covariant`).
   - Proved general form $H(T) = T \cdot q(\log_\tau T)$ with 1-periodic $q$, which collapses to $H(T) = cT$ if $\lim_{T\to\infty} H(T)/T$ exists.
   - Falsified the implicit premise: *"Bilateral discrete grade covariance uniquely determines the cofinal schedule."*
   - Proved that selecting $c \ge 1$ requires sharp remainder domination $|\mathcal R_H(t)| \le M \log(|t|+2)$.
4. **Lean 4 Declaration Count**:
   - Formalized 3 new schedule-covariance theorems in `formal/RiemannScope/ArithmeticBridge.lean`, bringing the compiled project theorem declaration count to 75.

Reason:

Ensure absolute certificate generation purity, formalize schedule non-uniqueness, eliminate overstated premises, and advance Gate G4 mathematical precision.

Mathematical / operational consequence:

Updated `certification.py`, `scripts/generate_certificates.py`, `math_core.py`, `tests/test_certification.py`, `formal/RiemannScope/ArithmeticBridge.lean`, and all registers.

---

## 2026-08-27 — Corrective Decision: Exact Remainder Cancellation, TC Origin Dilation, and Downgraded Bounds

Status: ACCEPTED

Decision:

1. **Exact Remainder Cancellation & Candidate Collapse**:
   - Proved analytically and algebraically that for $R_H(t) = \frac{\Xi'}{\Xi}(\sigma - 1/2 + it) - Z_H(t)$, $Z_H(t) + R_H(t) \equiv \frac{\Xi'}{\Xi}(\sigma - 1/2 + it)$ identically.
   - Consequently, the candidate functional $\mathcal S_T(Z_H; R_H) = \frac{1}{2\pi}\int_{-T}^T W_T(t) |Z_H(t) + R_H(t)|^2 dt \equiv \frac{1}{2\pi}\int_{-T}^T W_T(t) |\Xi'/\Xi|^2 dt$ is **identically independent of $H$ and $H(T)$**, collapsing to full completed function evaluation.
   - Formalized in Lean 4: `RiemannScope.exact_remainder_cancellation` and `RiemannScope.functional_decomposition_independence`.
   - Classified $S_T(Z_H; R_H)$ as `COLLAPSED_COFINAL_IDENTITY` / `FAIL_RADIAL_POSITIVITY`.
2. **Corrected TC Coordinate Derivation of Schedule Covariance**:
   - In Transcendental Continuation (TC), origin coordinate dilation is $s_K = \tau^K s$, with real origin shift $c_K = \tau^K/2$ and centered coordinate dilation $z_K = s_K - c_K = \tau^K(s - 1/2)$.
   - On the imaginary axis, ordinate dilates as $t_K = \tau^K t \implies t' = \tau t$. Covariance between window width $T$ and zero truncation cutoff $H$ requires $H(\tau T) = \tau H(T)$.
3. **Downgraded Claims from Previous Decision**:
   - The assertion that a sharp Hadamard remainder estimate forces $c \ge 1$ is **downgraded** from a proved theorem to an unproved heuristic remark (preventing omitted zeros from entering the window).
4. **The Actual Question & Open Obligation**:
   - Formulated the exact noncommutation defect $\mathcal D = \mathcal R_{\mathrm{op}}(Z_\infty) - \lim_{H\to\infty} \mathcal R_{\mathrm{op}}(Z_H)$ across 12 specific mathematical criteria.
   - Recorded `OBL-CMSA-003-G4-BOUNDARY` as the open research obligation to construct a genuinely non-additive cofinal boundary functional.
5. **Lean 4 Declaration Count**:
   - Total compiled project theorem declarations reached **77**.

---

## 2026-08-27 — Corrective Decision: Background-Dependence Theorem, Fixed-Finite Perturbation Invisibility, and Standardized Candidate Classifications

Status: ACCEPTED

Decision:

1. **Background-Dependence Theorem & Scope of Additive Invariance**:
   - Proved analytically and algebraically that for complex background $F$ and perturbation $\Delta$, the squared-norm variation is $Q(F, \Delta) = |F + \Delta|^2 - |F|^2 = |\Delta|^2 + 2\Re(F\bar\Delta)$, with background difference $Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)$.
   - Constructed concrete counterexample witness $F=1, G=-1, \Delta=1 \implies Q(1, 1)=3 \ne -1=Q(-1, 1)$.
   - Clarified that `additive_reference_subtraction_invariance` applies exclusively to *outer* scalar subtractions $(S - R)$ and does NOT apply to backgrounds placed *inside* squared norms.
   - **Withdrew the claim** that Case B automatically reduces to the certified finite Fejér response; the sign of $Q(F_0, \Delta)$ depends explicitly on the completed-function background $F_0$.
   - Formalized in Lean 4: `RiemannScope.complex_squared_norm_difference_expansion`, `RiemannScope.complex_squared_norm_difference_background_subtraction`, `RiemannScope.complex_squared_norm_difference_not_background_independent`.
2. **Fixed-Finite Perturbation Invisibility Theorem**:
   - Proved that for $\sigma > 1$, bounded prime Dirichlet polynomial $P_\sigma$, and any fixed finite linear combination of zero resolvents $\Delta = \sum_{j=1}^N \frac{c_j}{a_j + i(t-\gamma_j)}$ ($N < \infty, a_j > 0$):
     $$\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( |P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2 \right) dt = 0.$$
   - Extended to all fixed finite single zeros, conjugate pairs $\{\delta \pm i\gamma\}$, same-height functional-reflection pairs $\{\pm\delta + i\gamma\}$, and symmetric quartets $\{\pm\delta \pm i\gamma\}$.
   - Established: *"A fixed finite divisor perturbation cannot produce a nonzero normalized infinite mean response."*
   - Formalized normalized energy scaling in Lean 4 (`RiemannScope.fixed_finite_energy_scaling_zero`).
3. **Standardized Candidate Classifications**:
   - Enforced exactly one authorized classification per candidate:
     - Recomputed exact remainder: `FAIL_LIMIT_ORDER_DEPENDENCE`
     - Fixed finite perturbation under normalized infinite mean: `FAIL_LIMIT_ORDER_DEPENDENCE`
     - Growing / cofinal perturbation $\Delta_{H(T)}$: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`
     - Raw finite Fejér response: `FAIL_RADIAL_POSITIVITY`
   - Retired `COLLAPSED_COFINAL_IDENTITY` as a final classification label (retained as descriptive rationale).
4. **Lean 4 Project Theorem Inventory**:
   - Reached **81 compiled project theorem declarations** (0 errors, 0 warnings, 0 sorry, 0 admit).
5. **Exact Live Growing-Perturbation Obligation**:
   - Clarified that any non-trivial cofinal response requires an infinite growing perturbation $\Delta_{H(T)}(t)$ along a schedule $H(T) \to \infty$, governed by live open obligation `OBL-CMSA-003-G4-BOUNDARY`.

Reason:

Rigorous audit and mathematical repair of background dependence and finite perturbation scaling, eliminating false reductions to isolated zero models and identifying the precise infinite growing-perturbation boundary.

Mathematical / operational consequence:

Updated `formal/RiemannScope/ArithmeticBridge.lean`, `math_core.py`, `tests/test_fixed_finite_perturbation_invisibility.py`, `CMSA_GATE_G4.md`, `MATH_CONTRACT.md`, `RESEARCH_HYPOTHESIS.md`, `RESEARCH_LEDGER.md`, `LEAN_FORMALIZATION_PLAN.md`, `README.md`, and all registers.

---

## 2026-08-28 — Gate G4 Proof-Status Authority Chain Repair, Subcritical Norm Growth Theorem, and Live Growing Perturbation Threshold

Status: ACCEPTED

Decision:

1. **Proof-Status Authority Chain Repair**:
   - Corrected proof-status classification of the Fixed Finite Perturbation Invisibility Theorem to `PROVED / EXACT / PARTIALLY_FORMALIZED`.
   - Explicitly distinguished:
     - The complete deductive paper proof recorded in `CMSA_GATE_G4.md` and `MATH_CONTRACT.md`;
     - The Lean 4 formalization of the scalar energy scaling component $E/(2T) \to 0$ (`fixed_finite_energy_scaling_zero`, `FORMALLY_PROVED COMPONENT`);
     - The Python numerical evaluation of finite prime Dirichlet polynomial truncations at finite $T$-samples (`NUMERICAL_EVIDENCE`).
   - Restored historical ledger entries `G4-018`, `G4-019` and claim `CLM-CMSA-022`.
2. **Numerical Evaluator Corrections**:
   - Refactored `verify_fixed_finite_perturbation_invisibility` in `math_core.py` to return calculation type `"FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"`.
   - Replaced misleading metric `is_decaying_to_zero` with `endpoint_magnitude_decreased`.
   - Added rigorous input validation for $\sigma > 1$, `max_prime_n >= 2`, $T > 0$, $a_j > 0$, and handled empty resolvent inputs cleanly.
3. **The Subcritical Cofinal Norm Growth Theorem**:
   - Proved analytically that for any $P_T, \Delta_T \in L^2(-T, T)$ with $(1/(2T))\|P_T\|^2 \le M < \infty$ and $x_T = \|\Delta_T\|_{L^2(-T, T)}/\sqrt{T}$:
     $$|V_T| \le \frac{1}{2} x_T^2 + \sqrt{2M} x_T.$$
   - Proved that if $\|\Delta_T\| = o(\sqrt{T})$, then $V_T \to 0$ as $T \to \infty$.
   - Established the contrapositive necessity condition: $\limsup |V_T| > 0 \implies \|\Delta_T\| \ne o(\sqrt{T})$ (i.e. $\|\Delta_T\| = \Omega(\sqrt{T})$ is necessary).
   - Clarified that critical/supercritical norm growth is **necessary but NOT sufficient** due to potential cross-term cancellation $V_T = E_T - C_T$.
   - Unconditionally specialized the bound for the prime background $P_\sigma(t)$ with $M = M_\sigma^2 = (-\zeta'/\zeta(\sigma))^2 < \infty$ for $\sigma > 1$.
4. **Lean 4 Formalization Expansion**:
   - Formalized `subcritical_norm_response_bound_vanishes` (pointwise bound lemma) and `subcritical_norm_response_tendsto_zero` (`Filter.Tendsto` / `Metric.tendsto_atTop`) in `formal/RiemannScope/ArithmeticBridge.lean`.
   - Total compiled project theorem declaration count reached **83**.
5. **Live Growing Perturbation Analysis & Open Obligation**:
   - Explicitly defined the live growing object $\Delta_{H(T)}(t) = \sum_{|\gamma_j| \le H(T)} r_j(t)$.
   - Decomposed the live response as $V_T = E_T - C_T$ with direct energy $E_T = \frac{1}{2T}\|\Delta_{H(T)}\|^2$ and arithmetic cross-term $C_T = \frac{1}{T}\Re\langle P_\sigma, \Delta_{H(T)}\rangle$.
   - Formulated the exact live open obligation `OBL-CMSA-003-G4-COFINAL-ESTIMATE`. Gate G4 remains strictly **OPEN**.

Reason:

Repair authority chains, formalize subcritical norm vanishing in Lean 4, correct numerical evaluator caveats, and establish the exact norm-growth threshold governing live growing cofinal perturbations.

Mathematical / operational consequence:

Updated `math_core.py`, `tests/test_fixed_finite_perturbation_invisibility.py`, `formal/RiemannScope/ArithmeticBridge.lean`, `CMSA_GATE_G4.md`, `MATH_CONTRACT.md`, `RESEARCH_HYPOTHESIS.md`, `RESEARCH_LEDGER.md`, `LEAN_FORMALIZATION_PLAN.md`, `ARITHMETIC_RADIAL_BRIDGE.md`, and all three corpus registers.

---

## 2026-08-28 — Deduplicated Authority Registers, Exact Resolvent Algebra, Withdrawal of Riemann–von Mangoldt Norm Asymptotic, Finite Quartet Invisibility, and the Transcendental Continuation Activation Subgate

Status: ACCEPTED

Decision:

1. **Deduplicated Authority Registers and Enforced Uniqueness**:
   - Cleaned `claim_register.md` and `RESEARCH_LEDGER.md`, ensuring every claim ID (`CLM-TC-001` through `CLM-RH-001`), ledger entry (`G4-001` through `G4-023`), contradiction ID, and obligation ID appears exactly once.
   - Added automated regression checks in `.agents/verification/test_harness_integrity.py` to prevent duplicate IDs or canonical headings.
2. **Exact Single-Zero and Reflection Pair Resolvent Algebra**:
   - Proved analytically: for $a = \sigma - 1/2 > 0, w = a + i(t-\gamma)$, and $a - \delta > 0$:
     $$\int_{-\infty}^\infty |r_\delta(t)|^2 dt = \frac{\pi \delta^2}{a(a-\delta)(2a-\delta)} = \frac{\pi \delta^2}{2a^3} + \mathcal O(\delta^3),$$
     $$r_\delta(t) + r_{-\delta}(t) = \frac{2\delta^2}{w(w^2-\delta^2)}.$$
   - Formalized rational identities in Lean 4 (`resolvent_difference_rational_identity`, `resolvent_reflection_pair_cancellation`).
   - Implemented exact symbolic and high-precision quadrature verifiers in `math_core.py` and test suites.
3. **Subcritical Contrapositive & Subsequential Non-Vanishing**:
   - Proved that $\limsup |V_T| > 0 \implies \exists \varepsilon > 0, T_k \to \infty$ such that $\|\Delta_{T_k}\|_{L^2(-T_k, T_k)} \ge \varepsilon\sqrt{T_k}$.
   - Clarified that this does NOT imply an eventual $\Omega(\sqrt{T})$ bound (counterexample $x_n = 1$ for even $n$, $1/(n+1)$ for odd $n$).
   - Formalized in Lean 4: `subcritical_norm_contrapositive`, `not_tendsto_zero_subsequential_lower_bound`.
4. **Withdrawal of Riemann–von Mangoldt Norm Asymptotic**:
   - Withdrew the historical heuristic $\|\Delta_{H(T)}\| \sim \sqrt{T\log T}$ everywhere.
   - Detailed the 6 mathematical obstructions preventing total zero counting from implying defect-resolvent norm growth.
   - Reclassified the cofinal growth problem as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
5. **Finite Off-Line Quartet Invisibility & Zero-Rigidity Failure**:
   - Proved that for any finite off-line zero configuration, $\Delta_{H(T)}(t) = \Delta(t) \in L^2(\mathbb R)$ for $H(T) \ge \max |\gamma_j|$, yielding $\|\Delta_{H(T)}\| = \mathcal O(1) = o(\sqrt{T}) \implies V_T \to 0$.
   - Concluded that the current normalized mean functional produces zero response for a finite off-line quartet and cannot distinguish it from RH.
   - Classified fixed/subcritical defect families as `FAIL_LIMIT_ORDER_DEPENDENCE` and growing cofinal families as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
6. **Transcendental Continuation Activation Theorem (Earliest Open Subgate)**:
   - Formulated the Activation Theorem: $\exists \rho \text{ with } \delta_\rho \ne 0 \implies \limsup_{T\to\infty} \|\Delta^{TC}_T\|_{L^2(-T, T)}/\sqrt{T} > 0$.
   - Specified the 8 structural requirements on $\Delta^{TC}_T$.
   - Designated this as the precise earliest open subgate logically preceding the $E_T - C_T$ asymptotic evaluation.
7. **Lean 4 Project Theorem Inventory**:
   - Reached **87 compiled project theorem declarations** (0 errors, 0 warnings, 0 sorry, 0 admit).

Reason:

Completely eliminate unsupported norm asymptotics, deduplicate corpus authority files, establish exact resolvent algebra and reflection cancellation, resolve the finite quartet zero-rigidity question, and isolate the Transcendental Continuation Activation Theorem as the true earliest open subgate.

Mathematical / operational consequence:

Updated `CMSA_GATE_G4.md`, `MATH_CONTRACT.md`, `RESEARCH_HYPOTHESIS.md`, `ARITHMETIC_RADIAL_BRIDGE.md`, `formal/RiemannScope/ArithmeticBridge.lean`, `math_core.py`, `tests/test_fixed_finite_perturbation_invisibility.py`, `.agents/verification/test_harness_integrity.py`, and all corpus registers.

---

## 2026-08-28 — Curvature-Transport Unification and Theta–Mellin Arithmetic Bridge Audit

Status: ACCEPTED

Decision:

1. **Curvature-Transport Framework Unification**:
   - Unified circle geometry ($C_K, r_K, \kappa_K$), Fourier lattice spacing ($L_K = \tau^K\mathbb Z$), TC zero worldlines ($s_\rho(k) = \tau^k\rho$), transported radial unit ($r_K = \tau^{-K}$), grade character ($q_\rho^K = \tau^{K(\rho-1/2)}$), reflection-pair reciprocal modes ($|\chi_{\rho^\#}(K)| = |\chi_\rho(K)|^{-1}$), exact $\cosh$ defect ($B_\rho(K) = 2(\cosh(K\delta\log\tau)-1)$), separated-signal curvature ($\sum\delta_\rho^2$), radial-defect quotient ($\delta_\rho^2/\gamma_\rho^2$), and half-density dilation Mellin scaling ($a^{1/2-s}$) as expressions of one transported invariant: $\mathscr K_\tau(\rho) = B_\rho''(0)/(2(\log\tau)^2) = (r_K d_{\rho,K})^2 = \delta^2$.
2. **Theta–Mellin Transport Derivation**:
   - Derived the exact half-density normalized Mellin transform of scaled theta series $\Theta_{\tau^K}^+(t)$, demonstrating that its scale multiplier $\tau^{-K(s-1/2)}$ matches the reciprocal grade character $\chi_s(K)^{-1}$.
3. **Audit of Arithmetic Curvature-Descent Candidates**:
   - Proved that Candidate CT-1 (Scalar Theta–Mellin Transport $F_K(s) = \tau^{-K(s-1/2)}\Lambda(s)$) vanishes identically at all zeros ($\Lambda(\rho)=0 \implies \frac{d^m}{dK^m}F_K(\rho) \equiv 0$), classifying it as `GRADE_COORDINATE_REDUNDANT` / `FAIL_ARITHMETIC_FIREWALL`.
   - Audited Candidates CT-2, CT-3, and CT-4, formulating the exact 8 requirements for the canonical Arithmetic Curvature-Descent Theorem (`OBL-CT-001`).
4. **Symmetry-Complete Polynomial Countermodel**:
   - Analyzed $P_{\delta,\gamma}(z) = ((z-i\gamma)^2-\delta^2)((z+i\gamma)^2-\delta^2)$, proving that geometric and reflection properties with strictly positive grade curvature do not force $\delta = 0$ without arithmetic input.
5. **Reader-Facing Conditional Rigidity Theorem**:
   - Established the Transcendental Curvature Rigidity Theorem schema: if a divisor-independent arithmetic functional $\mathscr A_\tau(\xi) = 0$ evaluates to the positive sum $\sum W_\rho \delta_\rho^2$ ($W_\rho > 0$), then every zero satisfies $\delta_\rho = 0$ (RH).
6. **Lean 4 Formalization Inventory**:
   - Created `RiemannScope.CurvatureTransport` with 20 formal declarations, bringing the repository total to **107 compiled formal declarations** (0 errors, 0 warnings, 0 sorry, 0 admit).
7. **Authority Register Subsequential Correction**:
   - Corrected historical overstatements to emphasize that non-vanishing response implies a subsequential lower bound $\exists \varepsilon > 0, T_j \to \infty \text{ s.t. } \|\Delta_{T_j}\| \ge \varepsilon\sqrt{T_j}$, rather than an eventual $\Omega(\sqrt{T})$ bound.

---

## 2026-08-28 — Curvature-Descent Boundary Audit and Non-Scalar Bridge Construction

Status: ACCEPTED

Decision:

1. **Continuous vs Discrete Grade Parameter Separation**:
   - Strictly separated continuous grade $k \in \mathbb R$ (used for differentiation, character variation, zero worldlines $s_\rho(k) = \tau^k\rho$, and curvature $B_\rho''(0)$) from discrete integer grade checkpoints $K \in \mathbb Z$ (used for bilateral lattices $L_K = \tau^K\mathbb Z$ and circle circumferences $C_K = \tau^{1-K}$).
2. **Complete 4-Step Theta–Mellin Integral Proof**:
   - Completed the full 4-step analytic proof of the theta–Mellin scaling law:
     - Step 1: Explicit absolute convergence and Tonelli/Fubini interchange on $\Re(s) > 1$;
     - Step 2: Complex Mellin evaluation $\int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{-s}\pi^{-s/2}\Gamma(s/2)\zeta(s) = a^{-s}\Lambda(s)$;
     - Step 3: Half-density dilation scaling $a^{1/2}\int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{1/2-s}\Lambda(s) = \chi_s(k)^{-1}\Lambda(s)$ for $a = \tau^k$;
     - Step 4: Scaled Poisson summation $\theta(a^2 t) = \frac{1}{a\sqrt{t}}\theta(1/(a^2 t))$ and explicit Dirichlet tail bounds distinguishing unnormalized from half-density normalized bounds.
3. **Scalar-Transport No-Go Theorem**:
   - Formulated and proved the Scalar-Transport No-Go Theorem for scalar multipliers $F(k,s) = g(k,s)L(s)$:
     - Vanishing of all grade derivatives at zeros: $L(\rho) = 0 \implies \partial_k^m F(k,\rho) \equiv 0$ for all $m \ge 0$;
     - Divisor preservation on $g \ne 0$;
     - Logarithmic derivative decomposition $\partial_s \log F = \partial_s \log L + \partial_s \log g$ on $gL \ne 0$, where $\partial_s \log g = -k\log\tau$ contains zero divisor data;
     - Vanishing along the zero worldline pullback $F_k(s(k)) \equiv 0$.
4. **Scoped One-Point Holomorphic Obstruction**:
   - Proved the scoped Cauchy-Riemann obstruction: no fixed holomorphic local kernel $H(z)$ can equal $(\Re z)^2$ on an open set, because $\partial_{\bar z}(\Re z)^2 = \Re z = \delta \ne 0$.
   - Determined that any non-scalar arithmetic functional must employ sesquilinear pairing, contour boundary terms, or regularized determinants.
5. **Curvature Transport vs CMSA Gate G4 Clarification**:
   - Documented the 8-point comparison matrix between Curvature Transport and CMSA Gate G4.
   - Clarified that Curvature Transport operates at the orbit level and bypasses fixed-finite $L^2$ translation invisibility at the spectral detector level ($B_\rho''(0) > 0$ for a single off-line quartet), but does NOT solve CMSA Gate G4; whether a non-scalar arithmetic functional avoids or reproduces the pair-isolation/infinite-limit barrier remains an open problem.
6. **Sharpened Canonical Open Obligations (OBL-CT-001A–D)**:
   - Sharpened the curvature descent program into four sequential gates, establishing `OBL-CT-001A` (Non-Scalar Arithmetic Functional Construction) as the canonical earliest open obligation.
7. **Lean 4 Project Theorem Inventory**:
   - Expanded `RiemannScope.CurvatureTransport` with 8 new theorems (continuous grade signatures, strictly positive curvature, scalar no-go algebraic lemmas, and exact quartet roots), bringing the project total to **114 compiled project theorem declarations** (0 errors, 0 warnings, 0 sorry, 0 admit).

Reason:

Correct remaining theorem-boundary overclaims, establish complete mathematical precision for theta-Mellin scaling, eliminate scalar candidate illusions via the No-Go Theorem, scope the non-holomorphic obstruction, and isolate the exact open gates for non-scalar arithmetic functional construction.

Mathematical / operational consequence:

---

## 2026-08-28 — Weil–Hermitian Curvature Bridge Construction and Involution Discrepancy

Status: ACCEPTED

Decision:

1. **Repaired Scalar vs Worldline Conflation**:
   - Strictly separated fixed-zero scalar multiplication ($F(k,s) = g(k,s)L(s) \implies F(k,\rho)=0, \partial_k^m F(k,\rho) \equiv 0$) from coordinate-pulled zero worldlines ($L_k(s_\rho(k)) = L(\rho) = 0$ for $L_k(s) = L(1/2 + \tau^{-k}(s-1/2))$ and $s_\rho(k) = 1/2 + \tau^k(\rho-1/2)$) and unpulled static evaluation ($L(s_\rho(k)) = (\tau^k-1)(\rho-1/2) \ne 0$).
   - Formally proved in Lean 4 (`coordinate_pulled_affine_zero_worldline`, `unpulled_affine_zero_worldline_eval`).
2. **Canonical Weil–Hermitian Curvature Identity**:
   - Derived and proved the exact pointwise rational identity:
     $$\frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) - \Re\left(\frac{1}{\rho(1-\rho)}\right) = \frac{(1-2\beta)^2}{2|\rho|^2|1-\rho|^2} = \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0$$
   - Formally proved in Lean 4 (`pointwise_weil_curvature_identity_algebraic`, `pointwise_weil_curvature_weight_pos`, `pointwise_weil_curvature_nonneg`, `pointwise_weil_curvature_zero_iff`).
3. **Geometric Involution Discrepancy**:
   - Formally proved the exact relationship between functional reflection $J(\rho) = 1-\rho$ and complex conjugation $C(\rho) = \bar\rho$:
     $$J(\rho) - C(\rho) = -2\delta_\rho, \qquad |J(\rho) - C(\rho)|^2 = 4\delta_\rho^2$$
   - Proved $B_\rho''(0) = \frac{(\log\tau)^2}{2}|J(\rho) - C(\rho)|^2$, interpreting continuous grade curvature as the weighted squared discrepancy between $J$ and $C$.
4. **Discrete Zeta Divisor Summation**:
   - Reindexed over all nontrivial zeros $Z$ using $\rho \leftrightarrow 1-\rho$ symmetry and absolute convergence of $\sum 1/|\rho|^2 < \infty$.
   - Linked to the classical completed-$\xi$ Hadamard sum constant $C_\xi = 2 + \gamma_{\text{Euler}} - \log(4\pi) \approx 0.046191417932242...$.
   - Concluded $N_\xi - C_\xi = \sum_{\rho \in Z} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} \ge 0$, with strict equality iff every $\delta_\rho = 0$ (RH).
5. **GNS Factorization Barrier & Local Prime Definiteness**:
   - Evaluated the arithmetic Weil form $Q_W(g_0) = C_\xi$ and Hermitian companion $Q_H(g_0) = N_\xi$.
   - Proved that pure local prime distribution weights $-\frac{\Lambda(n)}{\sqrt{n}}$ produce strictly negative eigenvalues, falsifying local-prime Hilbert space factorization without global Archimedean and pole cancellation.
   - Identified that assuming $Q_W(g * g^*) \ge 0$ a priori is circular (equivalent to RH via Weil's 1952 criterion).
6. **Candidate Classification**:
   - Classified the Weil–Hermitian Curvature Bridge as `EXACT_CURVATURE_IDENTITY_PROVED_ARITHMETIC_NORM_OPEN` (earliest open subgate: non-circular zero-independent construction of $Q_H(g)$ / `FAIL_POSITIVE_TYPE_FACTORIZATION`).
7. **Lean 4 Formalization Inventory**:
   - Added 9 new formal declarations to `RiemannScope.CurvatureTransport`, bringing the project total to **123 compiled project theorem declarations** (0 errors, 0 warnings, 0 sorry, 0 admit).
8. **Verification Suite**:
   - Created `tests/test_weil_curvature.py` (13 tests) and updated `tests/test_curvature_transport.py` (99 tests), achieving 112/112 passing tests.

Reason:

Establish the complete exact algebraic and geometric bridge between continuous grade curvature and the Weil explicit formula, prove the geometric involution discrepancy theorem, resolve the scalar vs coordinate-pulled worldline distinction, and isolate the exact GNS positive-type barrier on the arithmetic side.

Mathematical / operational consequence:

Updated `CURVATURE_TRANSPORT.md`, `formal/RiemannScope/CurvatureTransport.lean`, `math_core.py`, `tests/test_curvature_transport.py`, `tests/test_weil_curvature.py`, `MATH_CONTRACT.md`, `RESEARCH_LEDGER.md`, `ARITHMETIC_RADIAL_BRIDGE.md`, `CMSA_GATE_G4.md`, `TRANSCENDENTAL_CONTINUATION.md`, `RESEARCH_HYPOTHESIS.md`, `LEAN_FORMALIZATION_PLAN.md`, `README.md`, and all three corpus registers.



