# Transcendental Coherence Experiment

## 0. Purpose

This document defines the central experimental campaign for `reimann_scope`.

The experiment exists to discover or falsify a zeta-specific law strong enough to support the missing implication:

\[
\boxed{
\text{Transcendental Coherence}
\Longrightarrow
\text{Transcendental Radial Rigidity}.
}
\]

The experiment is not designed to verify more zeros merely to accumulate numerical support for RH.

It is designed to determine whether the exact \(\tau\)-graded continuation exposes a global constraint that is:

- stronger than coordinate covariance;
- stable across genuinely different actual zeta regions;
- compatible with the arithmetic/analytic structure;
- incompatible with mixed radial leaves.

---

# 1. Research layers

The campaign has four layers.

## Layer A — exact grade/gauge controls

Establish what is guaranteed by definition.

## Layer B — compression and transcendental-continuation geometry

Inspect actual zeta regions under positive and negative grades.

## Layer C — actual cross-height coherence

Compare genuinely different regions after trivial degrees of freedom are removed.

## Layer D — radial-perturbation rigidity

Only after a candidate coherence law exists, test whether off-line radial displacement violates it.

These layers must remain visibly and computationally separate.

---

# 2. Layer A — exact grade/gauge controls

Use

\[
\mathcal Z_\tau(s,k)
=
\zeta(\tau^{-k}s).
\]

For arbitrary test points \(u\),

\[
\boxed{
\mathcal Z_\tau(\tau^k u,k)
=
\zeta(u).
}
\]

For a zero \(\rho\),

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

For the critical surface,

\[
\boxed{
\Re(s)=\frac{\tau^k}{2}.
}
\]

For radial coordinate,

\[
\boxed{
R_\tau(s_\rho(k),k)=\delta.
}
\]

The application must show these identities visually and numerically.

Allowed conclusion:

```text
exact_coordinate_control_passed
```

Forbidden conclusion:

```text
supports_rh
```

This layer calibrates the instrument.

---

# 3. Layer B — compression and expansion

## 3.1 Motivation

A hypothetical counterexample may occur at a very large finite ordinate.

Negative grade gives

\[
\gamma(k)=\tau^k\gamma
\]

and can move such a region into a manageable plotting range.

At the same time,

\[
d(k)=\tau^k\delta
\]

for absolute radial displacement.

Normalized radial class remains

\[
\tau^{-k}d(k)=\delta.
\]

Therefore compression does not create a contradiction by itself.

Its purpose is to expose which structural features remain stable after raw coordinate magnitude is removed.

## 3.2 Required compression experiment

For selected actual zeta regions:

1. record the source region in native \(k=0\);
2. apply declared negative and positive grades;
3. display the transformed critical surface;
4. display zero worldlines;
5. compare the complex zeta trace under exact coordinate correspondence;
6. measure any proposed nontrivial feature separately from the exact gauge residual.

## 3.3 Required controls

For every candidate preserved feature, compare:

- origin dilation;
- centered dilation;
- raw camera zoom;
- generic-base scale \(b^k\);
- \(\tau\)-grade scale.

A feature that survives only because the same path was reparameterized is classified as gauge.

---

# 4. Layer C — actual cross-height coherence

## 4.1 Research question

Let

\[
\rho_n=\frac12+i\gamma_n
\]

and

\[
\rho_m=\frac12+i\gamma_m
\]

be distinct actual verified simple zeros with widely separated ordinates.

After fixed normalization, do the corresponding actual local zeta paths share a simple nontrivial invariant?

This is different from taking one path and transforming its coordinates.

---

# 5. Baseline local normalization

Use one preregistered asymptotic local spacing:

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
\boxed{
u
=
\frac{t-\gamma_n}{\Delta_n}.
}
\]

Then

\[
\boxed{
s_n(u)
=
\frac12+i(\gamma_n+\Delta_nu).
}
\]

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

Then

\[
\boxed{
P_n(0)=0,
\qquad
P_n'(0)=1.
}
\]

This removes:

- zero location;
- selected local mean-spacing scale;
- first-order magnitude;
- first-order orientation.

The remaining geometry is higher-order local path structure.

---

# 6. Local shape coefficients

Expand

\[
P_n(u)
=
u+c_{2,n}u^2+c_{3,n}u^3+\cdots.
\]

Then

\[
\boxed{
c_{r,n}
=
\frac{
(i\Delta_n)^{r-1}
\zeta^{(r)}(\rho_n)
}{
r!\zeta'(\rho_n)
},
\qquad
r\ge2.
}
\]

These coefficients are candidate observables.

No coefficient is assumed constant.

The experiment may discover:

- individual stabilization;
- invariant combinations;
- recurrence relations;
- distributional stabilization;
- no coherence.

All outcomes are acceptable.

---

# 7. Required zero blocks

The campaign must not use only a contiguous low-height list.

Support:

- low regression block;
- medium-height block;
- high block;
- very-high sparse block;
- optional unusual-gap blocks.

Each selected point must retain:

- source block ID;
- zero index if known;
- ordinate;
- source precision;
- local evaluation precision;
- derivative conditioning;
- block checksum;
- role in the experiment.

The purpose of high blocks is to test height-independent structure.

It is not to count more on-line zeros as evidence for RH.

---

# 8. Preregistered normalization controls

The first campaign should use a small fixed family.

## N1 — asymptotic mean spacing

\[
\Delta_n
=
\frac{\tau}{\log(\gamma_n/\tau)}.
\]

Primary normalization.

## N2 — local neighbor spacing

For example,

\[
\boxed{
\Delta_n^{\mathrm{local}}
=
\frac{\gamma_{n+1}-\gamma_{n-1}}{2}.
}
\]

Control for dependence on the asymptotic density approximation.

## N3 — raw-height control

Use no local spacing normalization.

Purpose:

> show what the normalization itself removes.

## N4 — generic-base grade control

For grade-character quantities, replace

\[
\tau
\]

by a declared

\[
b>1.
\]

If the effect is unchanged for generic \(b\), classify it as generic scale structure unless another exact tau-specific relation is derived.

Do not add post hoc adaptive normalization chosen because it makes curves agree.

---

# 9. Path metrics

For a fixed normalized domain

\[
u\in[-U,U],
\]

use the same sample grid for all paths.

## 9.1 Pointwise distance

\[
\boxed{
d_{nm}(u)
=
|P_n(u)-P_m(u)|.
}
\]

## 9.2 Supremum distance

\[
\boxed{
D_\infty(n,m)
=
\sup_{|u|\le U}
|P_n(u)-P_m(u)|.
}
\]

## 9.3 RMS distance

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

## 9.4 Coefficient distance

For fixed order \(M\),

\[
\boxed{
D_c(n,m)
=
\left(
\sum_{r=2}^{M}
w_r
|c_{r,n}-c_{r,m}|^2
\right)^{1/2}.
}
\]

Weights \(w_r\) must be declared before the sweep.

---

# 10. Candidate coherence object

The experiment is not committed to pointwise universal path convergence.

The useful result may instead be a functional

\[
\boxed{
I[P_n]=C
}
\]

or a relation

\[
\boxed{
F(c_{2,n},c_{3,n},\ldots)=C.
}
\]

A candidate is interesting only if it is:

1. simple;
2. stable across widely separated actual heights;
3. not guaranteed by the normalization;
4. not generic to arbitrary holomorphic functions;
5. connected to exact zeta/xi structure;
6. suitable for algebraic derivation.

---

# 11. Transcendental grade-constraint experiment

Cross-height comparison is only one route to a coherence law.

The runner should also support direct grade-wide observables.

For selected exact candidate quantity \(G\), evaluate

\[
\boxed{
G_K
}
\]

across

\[
K=-N,\ldots,N.
\]

The question is not whether a trivial coordinate identity holds.

The question is whether some zeta-specific relation remains grade-independent or obeys a constrained recurrence.

Candidate relation classes may include:

- grade invariance;
- finite-difference identities in \(K\);
- reciprocal \(K\leftrightarrow-K\) relations;
- exact product constraints;
- prime-side / zero-side dual constraints;
- uniqueness of bilateral exponential representation.

Each candidate must be written mathematically before implementation.

---

# 12. Constraint-intersection experiment

Suppose a candidate law supplies a grade constraint

\[
\mathcal C_K.
\]

The experiment should test finite subsets

\[
\boxed{
\bigcap_{K=-N}^{N}\mathcal C_K
}
\]

against:

- actual critical-line spectrum inputs;
- synthetic mixed radial classes;
- reflection-symmetric off-line quartets;
- generic-base controls.

Finite success does not prove the infinite intersection theorem.

The experiment is intended to discover whether increasing the number of independent grade constraints reveals a stable rigidity pattern worth deriving.

---

# 13. Layer D — radial perturbation

Only begin the central perturbation campaign once a baseline coherence observable exists.

Let

\[
I
\]

be the retained candidate invariant.

Introduce a declared radial displacement

\[
\rho
=
\frac12+i\gamma
\quad\mapsto\quad
\frac12+\delta+i\gamma
\]

with required reflection/conjugation partners.

Measure

\[
\boxed{
\Delta I(\delta,K)
=
I^{(\delta)}_K-I^{(0)}_K.
}
\]

The desired empirical pattern is:

\[
\Delta I(0,K)=0
\]

and

\[
\Delta I(\delta,K)\neq0
\]

for nonzero \(\delta\), in a way that cannot be cancelled across all required bilateral grades.

---

# 14. Symmetry-complete perturbation

A single off-line nontrivial zero is not a valid symmetry-complete model.

For

\[
\rho
=
\frac12+\delta+i\gamma,
\]

include the required reflected/conjugate quartet:

\[
\frac12+\delta+i\gamma,
\]

\[
\frac12-\delta+i\gamma,
\]

\[
\frac12+\delta-i\gamma,
\]

\[
\frac12-\delta-i\gamma.
\]

The baseline comparison must use the corresponding multiplicity-preserving critical-line configuration.

The experiment must state exactly which synthetic object is being modified.

---

# 15. Bilateral grade defect

For the zero character,

\[
q_\rho^K
=
\tau^{K\delta}
e^{iK\gamma\log\tau}.
\]

The exact symmetric defect is

\[
\boxed{
|D_K|
=
4\sinh^2
\left(
\frac{K\delta\log\tau}{2}
\right).
}
\]

This is a calibration diagnostic.

A useful global invariant must establish why such nonzero bilateral radial behavior cannot be compensated inside the actual global zeta/xi constraint system.

Do not infer contradiction from growth alone.

---

# 16. Falsification criteria

The current proof programme should be weakened or killed if any of the following occurs:

1. every apparent grade invariant reduces to exact coordinate covariance;

2. cross-height actual paths show no simple structure beyond zero-specific variation or known statistics;

3. a candidate law fails at sufficiently separated high blocks;

4. the result depends on a post hoc normalization;

5. the same candidate law holds for an appropriate off-critical comparison function;

6. mixed radial classes satisfy all tested grade constraints without a trend toward a derivable rigidity law;

7. tau-specific claims disappear under generic-base controls;

8. the candidate “coherence theorem” is already an RH-equivalent bound in different notation;

9. the apparent no-compensation effect is only finite truncation.

---

# 17. Allowed experimental conclusions

Allowed:

```text
exact_control_passed
exact_control_failed
compression_behavior_characterized
no_cross_height_coherence_observed
candidate_coherence_observed
candidate_constraint_relation_observed
normalization_sensitive
generic_scale_effect
tau_specific_candidate
synthetic_radial_defect_observed
mixed_leaf_constraints_not_excluded
insufficient_precision
inconclusive
```

Forbidden automatic conclusions:

```text
supports_rh
refutes_rh
rh_probability
proof_progress
proof_complete
```

---

# 18. Transition from experiment to proof

When a simple candidate law survives:

\[
\boxed{
I_K=C
}
\]

the numerical campaign should stop expanding.

The next tasks are:

1. derive \(I_K=C\) exactly;
2. determine its domain and assumptions;
3. test known counterexample classes;
4. prove or kill:
   \[
   I_K=C\ \forall K
   \Longrightarrow
   \text{one occupied radial leaf};
   \]
5. formalize the logical core.

The application should not substitute more computation for the missing derivation.

---

# 19. Suggested canonical experiment metadata

```yaml
schema_version: "2"

id: transcendental-coherence-001

title: Transcendental continuation coherence and radial-leaf rigidity

research_question: >
  Do the exact tau-grade constraints and fixed cross-height
  normalizations expose a zeta-specific coherence law that is
  incompatible with simultaneous occupation of multiple radial leaves?

epistemic_class: observational_pattern

object_relationship: actual_cross_height_comparison

prediction:
  statement: >
    A simple nontrivial coherence quantity may remain stable across
    widely separated actual zeta regions and/or bilateral integer grades.

falsification:
  statement: >
    The candidate disappears under gauge controls, high-height tests,
    generic-base controls, or admits stable mixed-radial synthetic examples.

interpretation_limit:
  statement: >
    Finite agreement is not a proof of RH or of the infinite grade-intersection theorem.

formalization_target:
  statement: >
    Derive any retained coherence identity exactly, then prove or
    falsify its radial-rigidity implication.
```

---

# 20. Definition of done

The first transcendental-coherence campaign is complete when:

1. exact \(k=0\), positive-grade, and negative-grade controls pass;
2. the app can visualize zero worldlines and the critical surface;
3. compression/expansion of actual high-height regions is auditable;
4. multiple widely separated zero blocks are available with provenance;
5. normalized actual cross-height paths can be compared;
6. grade-wide candidate constraints can be evaluated bilaterally;
7. generic-base controls exist;
8. symmetry-complete perturbation can test a retained invariant;
9. the strongest preregistered hypothesis is either killed or retained;
10. any retained simple law is handed to algebra/Lean before broadening the experiment.
