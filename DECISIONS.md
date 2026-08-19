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
