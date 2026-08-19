# Riemann Microscope / Macroscope — Canonical Spec

## 1. Purpose

Build a minimal, Desmos-like mathematical instrument for interactively exploring the Riemann zeta function, its zeros, scale transformations, and the explicit-formula relationship between zeros and primes.

The app has four jobs:

1. Plot the actual complex path of zeta.
2. Find and validate zeros.
3. Let the user scale/reparameterize the domain and arithmetic kernel without hiding what transformation is being applied.
4. Show how zeta zeros reconstruct the prime-counting staircase and how perturbing one zero changes that reconstruction.

This is **not** a proof engine, experiment registry, or theorem-scoring system.

---

## 2. Mathematical coordinates

Raw coordinate:

\[
s = \sigma + it.
\]

Centered coordinate:

\[
z = s - \frac12 = \delta + it.
\]

Thus

\[
s = \frac12 + z
\]

and the RH condition is

\[
\delta = 0.
\]

Use

\[
\tau = 2\pi
\]

as the default scale base.

Do not assume tau is a zeta symmetry or the unique possible base.

---

## 3. Transformation rule

The UI and code must make it impossible to confuse:

- camera zoom;
- sampling-range changes;
- coordinate transformations;
- zeta argument transformations;
- arithmetic-kernel transformations;
- non-holomorphic deformations.

Every active transform must show the exact equation being used.

### 3.1 Camera

Rendering only. No mathematical change.

### 3.2 Height microscope / macroscope

\[
s_K(u) = \frac12 + \delta + i(t_0 + \tau^K u).
\]

This changes the sampled height range only.

### 3.3 Origin coordinate dilation

\[
s' = \tau^K s.
\]

The image of the original critical line is

\[
\Re(s') = \frac{\tau^K}{2}.
\]

For the same object in transformed coordinates:

\[
f_K(s') = \zeta(s'/\tau^K).
\]

Predicted zero map:

\[
\rho' = \tau^K \rho.
\]

### 3.4 Centered coordinate dilation

\[
s' = \frac12 + \tau^K(s-\frac12).
\]

The image of the critical line remains

\[
\Re(s') = \frac12.
\]

Predicted zero map:

\[
\rho' = \frac12 + \tau^K(\rho-\frac12).
\]

### 3.5 Zeta argument transform

\[
f_K(s) = \zeta(\tau^K s).
\]

Predicted zeros:

\[
s = \rho/\tau^K.
\]

Critical-zero line:

\[
\Re(s)=\frac{1}{2\tau^K}.
\]

This is not the same operation as origin coordinate dilation.

---

## 4. Kernel Lab

Start from

\[
n^{-s}=e^{-s\log n}.
\]

The natural scaling variables are therefore \(s\) and \(\log n\).

Expose an advanced Kernel Lab with:

\[
\log n \mapsto A\log n + C
\]

and

\[
s \mapsto Bs + D.
\]

The transformed object is

\[
\mathcal Z_{A,C,B,D}(s)
=
e^{-C(Bs+D)}
\zeta(A(Bs+D)).
\]

This right-hand side is the canonical implementation in the critical strip.

### Inverse Scale Lock

When ON:

\[
AB=1.
\]

Changing \(A\) sets

\[
B=1/A.
\]

This preserves the exponent pairing \(s\log n\) exactly.

Label this:

**EXACT KERNEL PAIRING PRESERVED**

### Centered kernel mode

\[
\mathcal Z^{ctr}_{A,B}(z)
=
\zeta\left(\frac12 + ABz\right).
\]

When \(AB=1\), the zeta argument is exactly unchanged.

### Optional anisotropic deformation

\[
z=\delta+i\gamma
\mapsto
A_\delta\delta + iA_\gamma\gamma.
\]

If \(A_\delta \neq A_\gamma\), label it:

**NON-HOLOMORPHIC DEFORMATION**

---

## 5. Main UI

Keep four synchronized panels.

### Panel A — Domain plane

Show:

- original critical line;
- transformed image of the critical line;
- active sampling path;
- program-discovered zeros;
- optional external-reference zero overlay;
- selected zero.

### Panel B — Complex zeta trace

For active path \(s(u)\), compute

\[
w(u)=\zeta(s(u))
\]

and plot

\[
(\Re w(u), \Im w(u)).
\]

This is the primary Desmos-like view.

### Panel C — Riemann Converter

Use a faithful truncated explicit formula:

\[
J_N(x)
=
\operatorname{Li}(x)
-
2\Re\sum_{0<\Im\rho\le T_N}
\operatorname{Li}(x^\rho)
-
\log 2
+
\int_x^\infty
\frac{du}{u(u^2-1)\log u}.
\]

Then

\[
\pi_N(x)
=
\sum_{m\ge1}
\frac{\mu(m)}{m}
J_N(x^{1/m}),
\]

terminating when \(x^{1/m}<2\).

Plot:

- true \(\pi(x)\);
- reconstructed \(\pi_N(x)\);
- optional \(\operatorname{Li}(x)\);
- clean vs perturbed reconstruction.

### Panel D — Centrifuge / radial character

For

\[
\rho=\frac12+\delta+i\gamma,
\]

define

\[
q_\rho = \tau^{\rho-1/2}.
\]

Under grade \(K\),

\[
q_\rho^K
=
\tau^{K\delta}
e^{iK\gamma\ln\tau}.
\]

Plot

\[
K \mapsto \log|q_\rho^K|
=
K\delta\ln\tau.
\]

Optionally show \(q_\rho^K\) in the complex plane.

---

## 6. Zero discovery and validation

At baseline \(k=0\), the app must find zeros itself.

Do not seed the zero finder from the reference table.

On the critical line use the Hardy Z-function or an equivalent stable real-valued formulation.

Workflow:

1. Scan the selected t-range.
2. Detect candidate brackets / near-zero regions.
3. Refine each candidate at high precision.
4. Verify
   \[
   |\zeta(1/2+i\gamma)| < \varepsilon.
   \]
5. Compare only afterward against independent reference data.

Do not rely only on coarse sign changes; guard against missed roots from under-sampling.

### External reference zeros

During implementation, use web research to select a reputable public source of rigorously computed Riemann-zeta zeros.

Do not depend on live internet at runtime.

Vendor a small immutable validation snapshot, roughly first \(10^3\)–\(10^4\) ordinates.

Record:

- source name;
- source URL;
- retrieval date;
- precision;
- count;
- checksum.

At \(k=0\), report:

- discovered count;
- matched count;
- max ordinate difference;
- RMS difference;
- unmatched discovered roots;
- unmatched reference roots.

For transformed functions with exact zero maps, discover transformed zeros independently and compare them against the algebraically predicted positions.

---

## 7. Zero perturbation

Allow the user to select one zero and edit independently:

\[
\delta = \Re\rho - \frac12
\]

and

\[
\gamma = \Im\rho.
\]

Radial presets:

- 0
- \(10^{-8}\)
- \(10^{-6}\)
- \(10^{-4}\)
- \(10^{-2}\)

Cache each zero's baseline explicit-formula contribution.

When one zero moves, update using only

\[
\Delta C_n(x)
=
C(x,\rho'_n)-C(x,\rho_n)
\]

instead of recomputing the full converter.

---

## 8. Responsiveness

### Preview tier

While dragging:

- 30–40 decimal digits;
- ~200–500 path samples;
- cached or reduced work;
- target sub-200 ms interaction where practical.

### Audit tier

On slider release or **High Precision**:

- 80+ decimal digits;
- ~1,000–5,000 samples;
- selected full zero count;
- replace preview with audited result.

The UI must display the active tier.

---

## 9. Numeric input

Accept decimal-string input for \(k,A,B,C,D,\delta,\gamma\).

Do not force user input through binary float before high-precision parsing.

The mathematical parameters are real-valued; finite decimal UI input is only an implementation representation.

---

## 10. Active Mathematics card

Always display:

- mode name;
- exact domain map;
- exact function being evaluated;
- original critical line;
- transformed/image critical line;
- predicted zero map if applicable;
- classification:
  - camera;
  - exact coordinate re-expression;
  - analytic reparameterization;
  - kernel deformation;
  - non-holomorphic deformation.

Generate this card from the same transformation object used by the math engine.

Example:

```text
MODE: ORIGIN COORDINATE DILATION
BASE: τ
k = 1.25

Domain map:
s' = τ^k s

Function plotted:
f_k(s') = ζ(s'/τ^k)

Original critical line:
Re(s) = 1/2

Image critical line:
Re(s') = τ^k/2

Predicted zero map:
ρ' = τ^k ρ

CLASS:
Exact coordinate re-expression of ζ.
Not a claim that ζ(τ^k s)=ζ(s).
```

---

## 11. Stack

Preferred MVP:

- Python;
- Plotly Dash;
- `python-flint` / Arb where practical;
- `mpmath` as fallback/secondary;
- NumPy for arrays and caching.

Avoid a separate frontend unless a concrete limitation requires it.

Suggested repository:

```text
riemann-microscope/
    app.py
    math_core.py
    transforms.py
    zero_finder.py
    converter.py
    cache.py
    reference_data.py
    data/
        zeros_reference.*
        primes.*
        provenance.json
    tests/
        test_zeta_values.py
        test_zero_finder.py
        test_transforms.py
        test_kernel_lab.py
        test_converter.py
        test_perturbation.py
    SPEC.md
    README.md
```

---

## 12. Trust tests

Before exploratory use, require tests for:

1. generic high-precision zeta values;
2. Schwarz reality:
   \[
   \zeta(\bar s)=\overline{\zeta(s)};
   \]
3. the functional equation at generic points;
4. baseline zero finder vs external reference data;
5. exact transformed critical-line formulas;
6. exact zero-map formulas where applicable;
7. inverse kernel lock \(AB=1\);
8. converter against known prime counts over a controlled range;
9. perturbation delta-update vs full recomputation;
10. centrifuge identity:
    \[
    |q_\rho^K|=\tau^{K\delta};
    \]
11. slope:
    \[
    \frac{d}{dK}\log|q_\rho^K|
    =
    \delta\ln\tau.
    \]

---

## 13. Acceptance criteria

MVP is complete when:

1. `python app.py` starts locally.
2. Default view plots a recognizable correct critical-line zeta trace.
3. The app discovers zeros in the displayed range itself.
4. Those zeros match the vendored external reference snapshot to declared tolerance.
5. Camera, height, origin, centered, argument, and kernel transforms are visibly distinct.
6. The transformed critical line is derived and displayed live.
7. Directly discovered transformed zeros match predicted mapped zeros where an exact map exists.
8. The Riemann Converter reconstructs the prime staircase from a selectable number of zeros.
9. A single zero can be moved off line and the converter updates without a full expensive recomputation.
10. The centrifuge graph shows
    \[
    \log|q_\rho^K|=K\delta\ln\tau.
    \]
11. Preview interactions are responsive.
12. High-precision mode audits the current view.
13. No UI copy overclaims a proof or hides which mathematical object is being plotted.
14. The code remains small and auditable.

---

## 14. Rule for future additions

Do not add an experiment merely because it is interesting.

A future feature is admitted only when:

1. a specific mathematical identity or candidate proof step is written first;
2. the visualization/calculation directly tests that statement;
3. the allowed conclusion is explicit;
4. existing controls cannot already test it.

The software stays simple; the mathematics does the research.
