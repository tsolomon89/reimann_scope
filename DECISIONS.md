# Decisions Log

Append-only record of consequential implementation decisions for the Riemann Microscope / Macroscope.

Do not use this file for ordinary coding notes.

A decision belongs here only if changing it later would alter mathematical semantics, numerical trust, data provenance, transformation definitions, branch conventions, or core architecture.

`SPEC.md` and `MATH_CONTRACT.md` remain authoritative.

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

## 2026-08-19 — Minimal research-instrument architecture

Status: ACCEPTED

Decision:
Use a Python-first application, preferably Plotly Dash, with the mathematical engine and UI kept in one small codebase.

Reason:
The application is an interactive mathematical instrument, not a production SaaS product. A separate frontend/API architecture would add unnecessary indirection and make the math harder to audit.

Mathematical / operational consequence:
The path from UI control to transformation object to numerical evaluation should remain easy to trace.

## 2026-08-19 — Transform classes remain explicit and separate

Status: ACCEPTED

Decision:
Camera, height sampling, origin coordinate dilation, centered coordinate dilation, zeta argument transforms, kernel transforms, and non-holomorphic deformations must remain different named operations.

Reason:
Different notions of scaling can become conflated. This project is specifically intended to make that impossible.

Mathematical / operational consequence:
Every active mode must generate its mathematics card from the same object used by the evaluator.

## 2026-08-19 — Reference zeros are validation-only

Status: ACCEPTED

Decision:
External reference zeros must not seed the baseline zero finder.

Reason:
The app must demonstrate that it can construct the zeta trace and discover zeros independently before comparing to trusted external data.

Mathematical / operational consequence:
Baseline validation is discovery-first, comparison-second.

## 2026-08-19 — Analytic continuation is authoritative in the critical strip

Status: ACCEPTED

Decision:
The application will not use the raw Dirichlet series \(\sum n^{-s}\) as a numerical definition of zeta inside the critical strip.

Reason:
The series does not converge there. Kernel transformations may be derived from Dirichlet-series algebra where valid, but critical-strip values must use analytic continuation from a trusted high-precision implementation.

Mathematical / operational consequence:
The Kernel Lab must display the distinction between formal kernel algebra and the continued function actually evaluated.

## 2026-08-19 — Tau is default scale base, not assumed zeta symmetry

Status: ACCEPTED

Decision:
Use \(\tau=2\pi\) as the default scale base and full-turn normalization.

Reason:
Tau is the project-facing rotational scale. This choice does not establish a non-trivial automorphism of zeta.

Mathematical / operational consequence:
All tau transformations remain explicit, and any claimed invariance must be derived or experimentally examined rather than assumed.

## 2026-08-19 — Future features require a prior mathematical statement

Status: ACCEPTED

Decision:
No new experiment or visualization is added merely because it appears interesting.

Reason:
The instrument should remain minimal and avoid experiment-framework sprawl.

Mathematical / operational consequence:
A future feature must correspond to a separately stated identity, candidate lemma, or falsifiable proof step.

## 2026-08-19 — Explicit Preview vs Audit precision boundaries

Status: ACCEPTED

Decision:
Establish two distinct computational tiers: Preview (NumPy / SciPy / float for responsive UI rendering <200ms) and Audit (mpmath / Arb flint for certified arbitrary precision at declared dps). Audit calculations must never cast decimal string parameters to Python float or binary float before evaluation.

Reason:
Binary-float downcasting during parameter ingestion or constructor initialization destroys precision and prevents certified residue and slope error analysis.

Mathematical / operational consequence:
All core math functions accept exact decimal strings and mpmath objects. Audit mode evaluations and batch runner points operate directly at arbitrary precision.

## 2026-08-19 — Riemann remainder integral series formulation

Status: ACCEPTED

Decision:
Replace the 1-term asymptotic approximation in converter.py with the exact exponential integral series:
\[
\int_x^\infty \frac{du}{u(u^2-1)\log u} = \sum_{k=1}^\infty E_1(2k\log x) = -\sum_{k=1}^\infty \operatorname{Ei}(-2k\log x).
\]
Split into `riemann_remainder_integral_preview` (fast float using `scipy.special.exp1`) and `riemann_remainder_integral_audit` (arbitrary precision using `mpmath.e1`).

Reason:
The previous 1-term asymptotic formula \(\frac{x^{-2k}}{2k\log x}\) truncated the integral definition from `MATH_CONTRACT.md §12` and introduced noticeable truncation error at low \(x\).

Mathematical / operational consequence:
The explicit formula remainder integral is now exact to declared precision `dps` across the entire domain \(x \ge 2\).

## 2026-08-19 — Independent discovery for transformed zeros

Status: ACCEPTED

Decision:
Transformed functions \(f_K(s)\) must have their zeros independently discovered along their image critical line via `discover_transformed_zeros` without using mapped baseline zeros as seeds.

Reason:
Comparing discovered zeros against algebraically predicted zeros \(\rho' = T(\rho)\) is mathematically meaningless if the discovery algorithm was seeded with the predicted positions.

Mathematical / operational consequence:
Transformed zero validation performs independent numerical root discovery first, and compares against algebraically predicted locations second.

## 2026-08-19 — Reproducible Batch Sweep Runner

Status: ACCEPTED

Decision:
Implement `research_runner.py` according to `EXPERIMENT_PROTOCOL.md` to run finite, declarative YAML experiments that reuse the canonical mathematical engine and produce immutable run artifacts (manifest, results JSONL, summary, human README).

Reason:
Interactive discoveries need a reproducible, machine-readable format for verification without proof-program framework sprawl.

Mathematical / operational consequence:
The batch runner evaluates only explicitly declared criteria over finite parameter spaces and never outputs automated proof progress or RH claims.

