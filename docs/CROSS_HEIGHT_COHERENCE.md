# Cross-Height Path Coherence Experiment

## 1. Purpose

This document specifies the next central experiment for `reimann_scope`.

The experiment is designed to distinguish:

1. **trivial coordinate covariance** — one mathematical path expressed in another coordinate system; from
2. **actual cross-height coherence** — genuinely different portions of the unmodified Riemann zeta function exhibiting a common normalized geometry.

The first is already an exact control. The second is the open research question.

---

## 2. Research question

Let

\[
\rho_n=\frac12+i\gamma_n
\]

be numerically verified simple nontrivial zeros at widely separated heights.

After applying a fixed, preregistered normalization to the actual zeta trajectory around each zero, do the resulting local paths share a nontrivial height-independent structure?

Formally:

\[
\boxed{
P_n(u)\stackrel{?}{\longrightarrow}P_\infty(u)
}
\]

or, more weakly, does there exist a simple functional \(I\) such that

\[
\boxed{
I[P_n]\stackrel{?}{=}C
}
\]

across widely separated heights?

No convergence or invariance is assumed.

---

## 3. Baseline local coordinate

For a selected zero ordinate \(\gamma_n\), define the initial local mean-spacing scale

\[
\boxed{
\Delta_n
=
\frac{\tau}{\log(\gamma_n/\tau)}.
}
\]

Define normalized height

\[
\boxed{
u
=
\frac{t-\gamma_n}{\Delta_n}.
}
\]

Thus

\[
t
=
\gamma_n+\Delta_nu.
\]

The active baseline sampling path is

\[
s_n(u)
=
\frac12+i(\gamma_n+\Delta_nu).
\]

---

## 4. Derivative-normalized path

For a numerically verified simple zero, define

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

Because \(\zeta(\rho_n)=0\),

\[
P_n(0)=0.
\]

Differentiating with respect to \(u\),

\[
P_n'(0)=1.
\]

This normalization removes:

- translation to the selected zero;
- the selected local height scale;
- first-order complex magnitude;
- first-order complex orientation.

The remaining path records higher-order local shape.

### Multiplicity safeguard

The derivative normalization is valid only for a zero verified numerically to be simple.

If a selected zero is not verified simple to the experiment's declared numerical standard:

- exclude it from the derivative-normalized experiment; or
- use a separately specified multiplicity-aware normalization based on the first nonzero derivative.

Do not silently divide by a nearly zero derivative.

---

## 5. Taylor shape coefficients

Expand

\[
P_n(u)
=
u
+
c_{2,n}u^2
+
c_{3,n}u^3
+\cdots.
\]

Then

\[
\boxed{
c_{m,n}
=
\frac{
(i\Delta_n)^{m-1}\zeta^{(m)}(\rho_n)
}{
m!\,\zeta'(\rho_n)
},
\qquad
m\ge2.
}
\]

These coefficients are compact algebraic descriptors of the same normalized local path.

The experiment should measure both:

- path-space distances;
- coefficient-space behavior.

No coefficient is assumed to be constant.

---

## 6. Required zero blocks

Do not use only a contiguous low-height list.

The experiment should support multiple non-contiguous blocks such as:

- low baseline block;
- medium-height block;
- high-height block;
- very-high-height sparse block;
- optional blocks selected for unusually small/large local gaps.

Each block must record:

- dataset/source;
- source reference;
- zero indices if available;
- ordinate range;
- number of zeros;
- stated source precision;
- local stored precision;
- checksum;
- retrieval/preparation code version;
- whether the block is discovery, validation, or research input.

A finite block never proves completeness outside its range.

---

## 7. Preregistered normalizations

The first campaign should use a small number of predefined normalizations.

### N1 — asymptotic mean-spacing normalization

\[
\Delta_n
=
\frac{\tau}{\log(\gamma_n/\tau)}.
\]

This is the primary normalization.

### N2 — local neighbor-spacing control

Use a declared local scale formed from neighboring verified zero gaps, for example

\[
\Delta_n^{\mathrm{local}}
=
\frac{\gamma_{n+1}-\gamma_{n-1}}{2}.
\]

This is a control, not a replacement for N1.

### N3 — raw-height control

Use no local scale normalization.

This should demonstrate how much apparent agreement is created by normalization itself.

Do not add adaptive normalization chosen after seeing which curves match best.

---

## 8. Path comparison metrics

For a fixed normalized domain

\[
u\in[-U,U],
\]

sample all paths on the same \(u\)-grid.

At minimum retain:

### Pointwise complex difference

\[
d_{nm}(u)
=
|P_n(u)-P_m(u)|.
\]

### Supremum distance

\[
\boxed{
D_{\infty}(n,m)
=
\sup_{|u|\le U}|P_n(u)-P_m(u)|.
}
\]

### RMS path distance

\[
\boxed{
D_2(n,m)
=
\left(
\frac1{2U}
\int_{-U}^{U}
|P_n(u)-P_m(u)|^2\,du
\right)^{1/2}.
}
\]

### Taylor-coefficient distance

For declared order \(M\),

\[
D_c(n,m)
=
\left(
\sum_{r=2}^{M}
w_r|c_{r,n}-c_{r,m}|^2
\right)^{1/2}.
\]

Weights \(w_r\) must be declared before the sweep.

---

## 9. What constitutes evidence of coherence

An observational result may be called **cross-height coherence** only if:

1. it compares genuinely different actual zeta heights;
2. the normalization was preregistered;
3. the effect is stronger than the raw/gauge controls;
4. it survives multiple widely separated blocks;
5. it is not dominated by precision loss;
6. it does not disappear under a reasonable alternative fixed normalization;
7. the same metric is used across all blocks.

The experiment must not output `supports_rh`.

Allowed conclusions include:

- `no_cross_height_collapse_observed`
- `height_stable_distribution_observed`
- `candidate_invariant_observed`
- `normalization_sensitive_pattern`
- `insufficient_precision`
- `inconclusive`

---

## 10. Falsification criteria

The strong universal-path hypothesis is falsified if, at adequate precision:

- \(D_\infty\) or \(D_2\) does not decrease or stabilize across higher blocks;
- between-zero variation remains of the same order as the paths themselves;
- path agreement exists only under a post hoc normalization;
- the same apparent collapse is reproduced by trivial coordinate copies;
- candidate invariants drift systematically with height.

A weaker distributional-coherence hypothesis may remain even if pointwise path collapse fails.

Do not preserve the strongest hypothesis by weakening its criterion after the run.

---

## 11. Generic-base control

Any grade-derived candidate invariant must be tested against a generic scale base

\[
b>1.
\]

Define

\[
q_{\rho,b}
=
b^{\rho-\frac12}.
\]

If an allegedly \(\tau\)-specific effect is unchanged under replacement

\[
\tau\to b,
\]

then classify it as generic scale geometry.

A genuinely \(\tau\)-specific claim requires an exact derivation showing where \(2\pi\) enters nontrivially.

---

## 12. Perturbation campaign — only after baseline

Do not begin with perturbation.

First establish whether the actual unmodified zeta path exhibits a candidate coherence pattern.

If a candidate invariant \(I\) is observed, then define a synthetic symmetry-complete perturbation and measure

\[
\boxed{
\Delta I(\delta)
=
I[P^{(\delta)}]-I[P^{(0)}].
}
\]

The perturbation is a **modified-object sensitivity test**.

It does not assert that the perturbed object is another valid Riemann zeta function.

The useful outcome is a simple defect law such as

\[
\Delta I(0)=0
\]

and

\[
\Delta I(\delta)\neq0
\quad
(\delta\neq0),
\]

followed by an exact algebraic derivation.

---

## 13. Proof-lead transition

If the experiment discovers a stable simple invariant, stop expanding the numerical campaign.

The next task becomes

\[
\boxed{
\text{derive }I[P_n]=C\text{ exactly from zeta/xi mathematics}.
}
\]

Then prove or kill

\[
\boxed{
I[P_n]=C
\Longrightarrow
\Re(\rho_n)=\frac12.
}
\]

Only that algebraic transition can create a proof mechanism.

---

## 14. Suggested experiment metadata

```yaml
research_question: cross-height-path-coherence

epistemic_class: observational_pattern

prediction:
  statement: >
    After preregistered translation, local-spacing normalization,
    and derivative normalization, actual zeta trajectories around
    widely separated verified simple zeros exhibit a stable
    nontrivial path geometry or invariant.

falsification:
  statement: >
    The normalized path distances or candidate invariants fail to
    stabilize across widely separated high-zero blocks, or the
    observed pattern is explained by a trivial coordinate control.

interpretation_limit:
  statement: >
    Finite cross-height coherence does not establish RH.

formalization_target:
  statement: >
    If a stable simple invariant is observed, derive it analytically
    before extending the numerical campaign.
```

---

## 15. Definition of done

The first cross-height campaign is complete when:

1. multiple widely separated zero blocks are loaded with provenance;
2. the same fixed normalizations are applied to every block;
3. authoritative high-precision paths are computed;
4. path and Taylor-coefficient metrics are persisted;
5. raw/gauge controls are run;
6. the strongest preregistered coherence hypothesis is either killed or retained;
7. no RH claim is inferred from finite agreement;
8. any retained simple invariant is handed to algebra/formalization before new experimentation.
