# Coding Agent Prompt — Build the Riemann Microscope / Macroscope

Build a new standalone project implementing the instrument defined in `SPEC.md`.

Read `SPEC.md` first and treat it as canonical.

## Core objective

Create a minimal, Desmos-like application that lets me:

- plot the actual complex path of the Riemann zeta function;
- see the corresponding path in the s-plane;
- find zeta zeros computationally;
- validate the baseline k=0 zeros against an independent external zero dataset;
- scale/reparameterize the domain and arithmetic kernel interactively;
- see exactly where the critical line and zeros move under each transformation;
- reconstruct the prime staircase from zeta zeros;
- select a zero, perturb delta and gamma, and see the converter change immediately;
- visualize the exact tau-grade amplification
  q_rho^K = tau^{K(rho-1/2)}.

This is an instrument, not a proof engine.

## Hard constraints

- KISS.
- Python-first.
- Prefer Plotly Dash.
- Prefer `python-flint` / Arb for high-precision zeta/root work; use `mpmath` where appropriate.
- No Next.js unless Dash has a concrete blocker.
- No proof DAG.
- No experiment registry.
- No theorem verdict badges.
- No AI hypothesis framework.
- Do not copy the old `riemann_converter` architecture.
- Do not treat the Dirichlet series as the analytic continuation inside the critical strip.
- Do not assume the critical line stays at 1/2 under every transform.
- Do not assume zeta(tau^k s) = zeta(s).

## Canonical coordinates

Use

s = sigma + i t

and

z = s - 1/2 = delta + i t.

Keep both visible.

Use tau = 2*pi as the default scale base.

## Implement transformations as explicit objects

Every transform object must provide:

- transform class;
- exact coordinate map;
- exact function evaluated;
- original critical line;
- transformed/image critical line;
- predicted zero map if applicable;
- human-readable classification.

Required modes:

1. Camera only.
2. Height microscope/macroscope:
   s_K(u) = 1/2 + delta + i(t0 + tau^K u)
3. Origin coordinate dilation:
   s' = tau^K s
   same-object coordinate function:
   f_K(s') = zeta(s'/tau^K)
   image critical line:
   Re(s') = tau^K/2
   zero map:
   rho' = tau^K rho
4. Centered coordinate dilation:
   s' = 1/2 + tau^K(s-1/2)
   image critical line remains 1/2
5. Argument transform:
   f_K(s) = zeta(tau^K s)
   zero map:
   s = rho/tau^K
   critical-zero line:
   Re(s) = 1/(2 tau^K)

Never conflate these.

## Kernel Lab

Use

n^{-s} = exp(-s log n).

Expose:

log n -> A log n + C

and

s -> B s + D.

Canonical transformed function:

Z_{A,C,B,D}(s)
=
exp(-C(Bs+D)) * zeta(A(Bs+D)).

Implement an Inverse Scale Lock:

AB = 1.

When locked, changing A sets B = 1/A.

Also support centered mode:

Z_ctr(A,B,z)
=
zeta(1/2 + AB z).

Optional advanced anisotropic deformation:

delta + i gamma
->
A_delta delta + i A_gamma gamma

and label it NON-HOLOMORPHIC DEFORMATION whenever A_delta != A_gamma.

## Build four synchronized panels

### A. Domain plane

Show:

- original critical line;
- transformed image line;
- active sampling path;
- program-discovered zeros;
- optional external-reference zeros;
- selected zero.

### B. Complex zeta trace

For active path s(u), plot:

(Re zeta(s(u)), Im zeta(s(u))).

This is the primary Desmos-like visual.

### C. Riemann Converter

Implement a faithful truncated explicit formula, then Mobius inversion.

Use:

J_N(x)
=
Li(x)
-
2 Re sum_rho Li(x^rho)
-
log 2
+
integral_x^infinity du/[u(u^2-1)log u]

and

pi_N(x)
=
sum_m mu(m)/m * J_N(x^(1/m))

until x^(1/m) < 2.

Plot:

- true pi(x);
- reconstructed pi_N(x);
- optional Li(x);
- clean vs perturbed reconstruction.

Use consistent complex branches and tests.

### D. Centrifuge

For selected/hypothetical:

rho = 1/2 + delta + i gamma

define

q_rho = tau^(rho-1/2).

Plot:

K -> log |q_rho^K| = K delta log tau.

Optionally show q_rho^K in the complex plane.

This panel is exact algebra and should not depend on numerical zeta approximation.

## Zero discovery

At k=0, the application must discover zeros itself.

Do not seed from a reference table.

Use the Hardy Z-function or an equivalent stable real-valued critical-line formulation.

Workflow:

1. scan selected t-range;
2. detect root candidates;
3. refine with high precision;
4. verify |zeta(1/2 + i gamma)| < epsilon;
5. only then compare against external reference data.

Do not rely only on coarse sign changes; guard against missed roots.

## External reference data

Use browsing during implementation to select a reputable public source of rigorously computed Riemann-zeta zeros.

Do not require internet at runtime.

Vendor a small immutable validation snapshot, roughly first 1,000–10,000 ordinates.

Record provenance:

- source;
- source URL;
- retrieval date;
- precision;
- count;
- checksum.

At baseline report:

- discovered count;
- matched count;
- max |Delta gamma|;
- RMS |Delta gamma|;
- unmatched discovered roots;
- unmatched reference roots.

For transformed functions with exact zero-map formulas, discover transformed zeros and separately compare them to predicted mapped positions.

## Single-zero perturbation

Allow editing:

delta = Re(rho) - 1/2

and

gamma = Im(rho).

Provide radial presets:

0, 1e-8, 1e-6, 1e-4, 1e-2.

Cache each zero's baseline explicit-formula contribution.

When one zero changes, update only the contribution delta instead of recomputing the full converter.

## Responsiveness

Preview tier while dragging:

- 30–40 dps;
- ~200–500 samples;
- cached/reduced work;
- target sub-200 ms where practical.

Audit tier on release / High Precision:

- 80+ dps;
- ~1,000–5,000 samples;
- full selected zero count;
- authoritative recomputation.

Show which tier is active.

## Active Mathematics card

Mandatory.

Generate it from the same transform object used by the math engine.

It must show:

- mode;
- exact map;
- exact function plotted;
- original critical line;
- transformed/image line;
- zero map;
- classification.

Example:

MODE: ORIGIN COORDINATE DILATION
BASE: tau
k = 1.25

s' = tau^k s

f_k(s') = zeta(s'/tau^k)

Original critical line:
Re(s)=1/2

Image line:
Re(s')=tau^k/2

Zero map:
rho'=tau^k rho

CLASS:
Exact coordinate re-expression of zeta.
Not a claim that zeta(tau^k s)=zeta(s).

## Numeric handling

Parse typed decimal strings directly into high-precision numeric types.

Avoid binary float until plotting serialization where unavoidable.

## Required tests before UI polish

1. trusted generic zeta values;
2. Schwarz conjugation;
3. functional equation at generic points;
4. baseline zero finder vs vendored reference;
5. critical-line image formulas for every transform;
6. zero-map formulas;
7. inverse kernel lock AB=1;
8. converter against known prime counts over a modest range;
9. perturbation delta-update vs full recomputation;
10. |q_rho^K| = tau^(K delta);
11. log-magnitude slope = delta log tau.

## Suggested repository

riemann-microscope/
    app.py
    math_core.py
    transforms.py
    zero_finder.py
    converter.py
    cache.py
    reference_data.py
    data/
    tests/
    SPEC.md
    README.md

Keep modules small.

## Implementation order

1. Read SPEC.md.
2. Scaffold the small Python/Dash app.
3. Implement/test math_core.
4. Implement transform objects + Active Mathematics card.
5. Implement domain plot + direct zeta trace.
6. Implement baseline zero discovery.
7. Browse/select external zero source and vendor validation snapshot.
8. Add zero-validation report.
9. Implement explicit-formula converter.
10. Add cached single-zero perturbation.
11. Add centrifuge plot.
12. Add Kernel Lab.
13. Add preview/audit tiers.
14. Polish layout only after math tests pass.

## Definition of done

Stop when I can:

- recognize a correct critical-line zeta trace;
- see exactly where in the s-plane it is sampled;
- see the program independently find and validate known zeros;
- move k, A, B, delta, and gamma while always knowing what mathematical object changed;
- see the critical line move or stay fixed according to the selected transformation;
- compare baseline and transformed traces;
- change the zero count in the converter and watch the prime staircase respond;
- move one zero off line and see the clean/perturbed difference immediately;
- inspect the exact tau^(K delta) amplification separately from noisy aggregate observables.

Do not add a proof-program layer after this works. Future experiments must begin from a separately stated mathematical lemma and only then earn a new visualization or calculation.
