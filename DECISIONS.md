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


